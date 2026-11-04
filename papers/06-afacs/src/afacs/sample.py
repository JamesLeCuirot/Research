"""Stage 3 - sample: choose which traces get coded.

Run:
    uv run afacs-sample calibration            # the 30 traces James hand-codes
    uv run afacs-sample calibration --verify   # check the frozen set is unchanged
    uv run afacs-sample bulk                   # the ~250 traces the LLM annotator codes later

Calibration set (all numbers live in design.py):
- 5 traces from each of 6 frameworks, picked at random from the eligible pool.
  In 4 of those frameworks, one of the 5 is a MAST-clean "control" instead of a
  MAST-failed trace. Every framework has 5 rows, so the sheet gives nothing away.
- The order is shuffled and each trace gets an id C01, C02, ... so the coder
  cannot tell controls from failures, and frameworks are interleaved.
- The dev/test split is decided NOW, before any coding, and written only to the
  hidden key file. Fixing it in advance means we cannot (even unconsciously)
  pick a test set that flatters the annotator. A fingerprint (SHA-256) of the key
  is committed, so anyone can later check the key was not changed.

Outputs:
- annotations/human/calibration_sheet.csv    : the blank coding sheet (committed).
- annotations/human/calibration_key.sha256   : fingerprint of the hidden key (committed).
- data/processed/calibration_key.csv         : which are controls, dev/test, MAST labels (hidden).
- data/calibration/C01.md ...                : rendered traces to read while coding.

Bulk set: stratified by framework with a "balanced" allocation (equal shares,
capped at what each framework has), and balanced across models within each
framework, excluding the calibration traces.
"""

from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict

from afacs import design, paths
from afacs.ingest import design_exclusion, load_traces
from afacs.render import render_markdown
from afacs.schema import CODING_FIELDS


def eligible(traces: list[dict]) -> list[dict]:
    """Traces that pass the data-quality checks and the design filters."""
    return [t for t in traces if t["quality_exclusion"] is None and design_exclusion(t) is None]


def mast_label_string(t: dict) -> str:
    return ";".join(c for c, v in t["mast_labels"].items() if v == 1)


def balanced_allocation(available: dict[str, int], total: int) -> dict[str, int]:
    """Split `total` as evenly as possible across groups, never exceeding what a group has.

    Example: available={A: 100, B: 100, C: 10}, total=90 -> {A: 40, B: 40, C: 10}.
    We visit groups from smallest to largest. Each takes an equal share of what is
    still left (or everything it has, if that is less), so a small group's unused
    share passes to the bigger groups after it.
    """
    remaining = min(total, sum(available.values()))
    alloc = {}
    order = sorted(available, key=lambda g: (available[g], g))  # smallest first
    for i, g in enumerate(order):
        share = remaining // (len(order) - i)
        alloc[g] = min(available[g], share)
        remaining -= alloc[g]
    # Rounding can leave a few units over: give them one at a time to groups with room.
    for g in sorted(order, key=lambda g: (alloc[g], g)):
        if remaining == 0:
            break
        if alloc[g] < available[g]:
            alloc[g] += 1
            remaining -= 1
    return alloc


# ---------------------------------------------------------------------------
# Calibration set
# ---------------------------------------------------------------------------


def pick_calibration(traces: list[dict], rng: random.Random) -> list[dict]:
    pool = [t for t in eligible(traces) if t["uid"] not in design.SEEN_BY_CODER]
    pool.sort(key=lambda t: t["uid"])  # sort first, so the seed alone decides

    # 1. Which frameworks get a control (a MAST-clean trace), and is it dev or test?
    clean_by_fw = defaultdict(list)
    for t in pool:
        if t["mast_failed"] is False and t["framework"] in design.CALIBRATION_FRAMEWORKS:
            clean_by_fw[t["framework"]].append(t)
    control_fws = rng.sample(sorted(clean_by_fw), design.CALIBRATION_CONTROLS)
    control_split = {fw: "test" if i < design.CALIBRATION_CONTROLS_TEST else "dev" for i, fw in enumerate(control_fws)}

    # 2. Fill each framework's 5 slots: its control (if any), then failed traces.
    #    Each framework ends up with exactly TEST_PER_FRAMEWORK test traces.
    chosen = []
    for fw in design.CALIBRATION_FRAMEWORKS:
        slots, n_test = [], design.CALIBRATION_TEST_PER_FRAMEWORK
        if fw in control_split:
            slots.append({"trace": rng.choice(clean_by_fw[fw]), "role": "control", "split": control_split[fw]})
            n_test -= control_split[fw] == "test"
        failed = [t for t in pool if t["framework"] == fw and t["mast_failed"]]
        for i, t in enumerate(rng.sample(failed, design.CALIBRATION_PER_FRAMEWORK - len(slots))):
            slots.append({"trace": t, "role": "failed", "split": "test" if i < n_test else "dev"})
        chosen += slots

    rng.shuffle(chosen)
    for i, c in enumerate(chosen, start=1):
        c["cal_id"] = f"C{i:02d}"
    return chosen


KEY_HASH_FILE = paths.HUMAN_ANNOTATIONS / "calibration_key.sha256"


def key_rows(chosen: list[dict]) -> list[list]:
    rows = [["cal_id", "uid", "framework", "model", "benchmark", "role", "split", "mast_labels", "benchmark_outcome"]]
    for c in sorted(chosen, key=lambda c: c["cal_id"]):
        t = c["trace"]
        rows.append([c["cal_id"], t["uid"], t["framework"], t["model"], t["benchmark"], c["role"], c["split"],
                     mast_label_string(t), t["benchmark_outcome"] or ""])
    return rows


def key_fingerprint(rows: list[list]) -> str:
    """SHA-256 of the key's content. Committed, so the hidden key can be checked later without revealing it."""
    import hashlib

    return hashlib.sha256("\n".join(",".join(map(str, r)) for r in rows).encode()).hexdigest()


def verify_calibration(chosen: list[dict]) -> None:
    """Re-draw the calibration set and check it matches the committed sheet and key fingerprint."""
    with open(paths.CALIBRATION_SHEET) as f:
        sheet = {r["cal_id"]: r["uid"] for r in csv.DictReader(f)}
    redrawn = {c["cal_id"]: c["trace"]["uid"] for c in chosen}
    expected = KEY_HASH_FILE.read_text().split()[0] if KEY_HASH_FILE.exists() else None
    actual = key_fingerprint(key_rows(chosen))
    print(f"Coding sheet matches re-drawn set: {'YES' if sheet == redrawn else 'NO'}")
    print(f"Key fingerprint matches committed value: {'YES' if expected == actual else 'NO'}")
    if sheet != redrawn or expected != actual:
        raise SystemExit("Mismatch: the data, parsers or design settings have changed since the set was frozen.")


def write_calibration(chosen: list[dict], force: bool) -> None:
    if paths.CALIBRATION_SHEET.exists():
        if not force:
            raise SystemExit(
                f"{paths.CALIBRATION_SHEET.relative_to(paths.ROOT)} already exists and may contain coding. "
                "Refusing to overwrite. Use --verify to check it, or --force only if you are sure."
            )
        backup = paths.CALIBRATION_SHEET.with_suffix(".csv.bak")
        backup.write_bytes(paths.CALIBRATION_SHEET.read_bytes())
        print(f"  (previous sheet backed up to {backup.relative_to(paths.ROOT)})")
    paths.HUMAN_ANNOTATIONS.mkdir(parents=True, exist_ok=True)
    with open(paths.CALIBRATION_SHEET, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cal_id", "uid", "framework", "model", "benchmark", *CODING_FIELDS, "minutes_spent"])
        for c in chosen:
            t = c["trace"]
            w.writerow([c["cal_id"], t["uid"], t["framework"], t["model"], t["benchmark"], *[""] * len(CODING_FIELDS), ""])

    paths.PROCESSED.mkdir(parents=True, exist_ok=True)
    rows = key_rows(chosen)
    with open(paths.CALIBRATION_KEY, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    KEY_HASH_FILE.write_text(
        f"{key_fingerprint(rows)}  SHA-256 of the hidden calibration key (data/processed/calibration_key.csv), "
        f"frozen {design.CALIBRATION_FROZEN_ON}. Check with: uv run afacs-sample calibration --verify\n"
    )

    write_renders(chosen)


def write_renders(chosen: list[dict]) -> None:
    """Write data/calibration/Cxx.md for each calibration trace (the blind-coding view)."""
    paths.CALIBRATION_RENDERS.mkdir(parents=True, exist_ok=True)
    for old in paths.CALIBRATION_RENDERS.glob("C*.md"):  # remove renders from any earlier draw
        old.unlink()
    for c in chosen:
        md = render_markdown(c["trace"], title=f"Calibration trace {c['cal_id']}")
        (paths.CALIBRATION_RENDERS / f"{c['cal_id']}.md").write_text(md)


# ---------------------------------------------------------------------------
# Bulk set
# ---------------------------------------------------------------------------


def pick_bulk(traces: list[dict], exclude_uids: set[str], size: int, rng: random.Random) -> list[dict]:
    pool = sorted((t for t in eligible(traces) if t["mast_failed"] and t["uid"] not in exclude_uids), key=lambda t: t["uid"])
    by_fw = defaultdict(list)
    for t in pool:
        by_fw[t["framework"]].append(t)
    fw_alloc = balanced_allocation({fw: len(ts) for fw, ts in by_fw.items()}, size)

    chosen = []
    for fw in sorted(by_fw):
        by_model = defaultdict(list)
        for t in by_fw[fw]:
            by_model[t["model"]].append(t)
        model_alloc = balanced_allocation({m: len(ts) for m, ts in by_model.items()}, fw_alloc[fw])
        for m in sorted(by_model):
            for t in rng.sample(by_model[m], model_alloc[m]):
                # weight = how many pool traces each sampled trace stands for (for pool-level estimates)
                chosen.append({"trace": t, "weight": len(by_model[m]) / model_alloc[m]})
    return chosen


def write_bulk(chosen: list[dict]) -> None:
    paths.PROCESSED.mkdir(parents=True, exist_ok=True)
    with open(paths.BULK_SAMPLE, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["uid", "framework", "model", "benchmark", "mast_labels", "approx_tokens", "weight"])
        for c in sorted(chosen, key=lambda c: c["trace"]["uid"]):
            t = c["trace"]
            w.writerow([t["uid"], t["framework"], t["model"], t["benchmark"], mast_label_string(t), t["approx_tokens"], round(c["weight"], 4)])


def calibration_uids() -> set[str]:
    if not paths.CALIBRATION_KEY.exists():
        return set()
    with open(paths.CALIBRATION_KEY) as f:
        return {row["uid"] for row in csv.DictReader(f)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("which", choices=["calibration", "bulk"])
    ap.add_argument("--force", action="store_true", help="overwrite an existing calibration sheet (it is backed up first)")
    ap.add_argument("--verify", action="store_true", help="re-draw the calibration set and check it matches the frozen one")
    ap.add_argument("--renders-only", action="store_true",
                    help="check the frozen set, then (re)write data/calibration/Cxx.md without touching the coding sheet")
    ap.add_argument("--size", type=int, default=design.BULK_SIZE, help="bulk sample size")
    args = ap.parse_args()

    traces = load_traces()
    if args.which == "calibration":
        rng = random.Random(design.SEED)
        chosen = pick_calibration(traces, rng)
        if args.verify or args.renders_only:
            verify_calibration(chosen)
            if args.renders_only:
                write_renders(chosen)
                print(f"  wrote {len(chosen)} renders to {paths.CALIBRATION_RENDERS.relative_to(paths.ROOT)}/")
            return
        write_calibration(chosen, force=args.force)
        print(f"Calibration set: {len(chosen)} traces")
        print(f"  coding sheet : {paths.CALIBRATION_SHEET.relative_to(paths.ROOT)}")
        print(f"  renders      : {paths.CALIBRATION_RENDERS.relative_to(paths.ROOT)}/C01.md ...")
        print(f"  hidden key   : {paths.CALIBRATION_KEY.relative_to(paths.ROOT)} (don't open it while coding)")
    else:
        cal = calibration_uids()
        if not cal:
            raise SystemExit("Run `afacs-sample calibration` first, so the bulk set can exclude those traces.")
        rng = random.Random(design.SEED + 1)
        chosen = pick_bulk(traces, cal, args.size, rng)
        write_bulk(chosen)
        counts = defaultdict(int)
        for c in chosen:
            counts[c["trace"]["framework"]] += 1
        print(f"Bulk set: {len(chosen)} traces -> {paths.BULK_SAMPLE.relative_to(paths.ROOT)}")
        print("  per framework: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
