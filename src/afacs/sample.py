"""Stage 3 - sample: choose which traces get coded.

Run:
    uv run afacs-sample calibration   # the ~34 traces James hand-codes
    uv run afacs-sample bulk          # the ~250 traces the LLM annotator codes later

Calibration set (all numbers live in design.py):
- 5 MAST-failed traces from each of 6 frameworks, picked at random from the
  eligible pool, plus 4 MAST-clean "controls" from 4 different frameworks.
- The order is shuffled and each trace gets an id C01, C02, ... so the coder
  cannot tell controls from failures, and frameworks are interleaved.
- The dev/test split is decided NOW, before any coding, and written only to the
  hidden key file. Fixing it in advance means we cannot (even unconsciously)
  pick a test set that flatters the annotator.

Outputs:
- annotations/human/calibration_sheet.csv : the blank coding sheet (committed).
- data/processed/calibration_key.csv      : which are controls, dev/test, MAST labels (hidden).
- data/calibration/C01.md ...             : rendered traces to read while coding.

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
    Groups that run out free up their share for the others ("water-filling").
    """
    alloc = {g: 0 for g in available}
    remaining = min(total, sum(available.values()))
    while remaining > 0:
        open_groups = sorted(g for g in available if alloc[g] < available[g])
        share, extra = divmod(remaining, len(open_groups))
        for i, g in enumerate(open_groups):
            give = min(share + (1 if i < extra else 0), available[g] - alloc[g])
            alloc[g] += give
            remaining -= give
    return alloc


# ---------------------------------------------------------------------------
# Calibration set
# ---------------------------------------------------------------------------


def pick_calibration(traces: list[dict], rng: random.Random) -> list[dict]:
    pool = [t for t in eligible(traces) if t["uid"] not in design.SEEN_BY_CODER]
    pool.sort(key=lambda t: t["uid"])  # sort first, so the seed alone decides
    chosen = []
    for fw in design.CALIBRATION_FRAMEWORKS:
        failed = [t for t in pool if t["framework"] == fw and t["mast_failed"]]
        picks = rng.sample(failed, design.CALIBRATION_PER_FRAMEWORK)
        for i, t in enumerate(picks):
            split = "test" if i < design.CALIBRATION_TEST_PER_FRAMEWORK else "dev"
            chosen.append({"trace": t, "role": "failed", "split": split})

    clean_by_fw = defaultdict(list)
    for t in pool:
        if t["mast_failed"] is False and t["framework"] in design.CALIBRATION_FRAMEWORKS:
            clean_by_fw[t["framework"]].append(t)
    control_fws = rng.sample(sorted(clean_by_fw), design.CALIBRATION_CONTROLS)
    for i, fw in enumerate(control_fws):
        t = rng.choice(clean_by_fw[fw])
        split = "test" if i < design.CALIBRATION_CONTROLS_TEST else "dev"
        chosen.append({"trace": t, "role": "control", "split": split})

    rng.shuffle(chosen)
    for i, c in enumerate(chosen, start=1):
        c["cal_id"] = f"C{i:02d}"
    return chosen


def write_calibration(chosen: list[dict], force: bool) -> None:
    if paths.CALIBRATION_SHEET.exists() and not force:
        raise SystemExit(
            f"{paths.CALIBRATION_SHEET.relative_to(paths.ROOT)} already exists and may contain coding. "
            "Refusing to overwrite. Use --force only if you are sure."
        )
    paths.HUMAN_ANNOTATIONS.mkdir(parents=True, exist_ok=True)
    with open(paths.CALIBRATION_SHEET, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cal_id", "uid", "framework", "model", "benchmark", *CODING_FIELDS, "minutes_spent"])
        for c in chosen:
            t = c["trace"]
            w.writerow([c["cal_id"], t["uid"], t["framework"], t["model"], t["benchmark"], *[""] * len(CODING_FIELDS), ""])

    paths.PROCESSED.mkdir(parents=True, exist_ok=True)
    with open(paths.CALIBRATION_KEY, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cal_id", "uid", "framework", "model", "benchmark", "role", "split", "mast_labels", "benchmark_outcome", "approx_tokens"])
        for c in sorted(chosen, key=lambda c: c["cal_id"]):
            t = c["trace"]
            w.writerow([c["cal_id"], t["uid"], t["framework"], t["model"], t["benchmark"], c["role"], c["split"],
                        mast_label_string(t), t["benchmark_outcome"] or "", t["approx_tokens"]])

    paths.CALIBRATION_RENDERS.mkdir(parents=True, exist_ok=True)
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
    ap.add_argument("--force", action="store_true", help="overwrite an existing calibration sheet")
    ap.add_argument("--size", type=int, default=design.BULK_SIZE, help="bulk sample size")
    args = ap.parse_args()

    traces = load_traces()
    if args.which == "calibration":
        rng = random.Random(design.SEED)
        chosen = pick_calibration(traces, rng)
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
