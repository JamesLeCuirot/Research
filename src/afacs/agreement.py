"""Stage 5 - agreement: how consistently can AFACS be applied? (RQ1)

Run:
    uv run afacs-agreement check-sheet                         # check James's coding sheet for mistakes
    uv run afacs-agreement human-vs-llm --run sonnet_test_p1 --split test
    uv run afacs-agreement llm-vs-llm --run-a sonnet_bulk_p1 --run-b opus_bulk_p1

What is measured, for the traces both coders coded:
- Layer presence: for each layer (L4, L3, L2, L1), did each coder put at least
  one code there? Cohen's kappa per layer. This is the headline: RQ2 rests on
  layers, not individual codes.
- Code presence: kappa for each of the 16 codes, and their average ("macro").
  We never pool codes into one list (that inflates kappa; see ingest.py).
- Error vs violation: kappa on "any violation code (V1, V2 or V?)" yes/no, and
  on the full violation_flag.
- Deepest layer: kappa, plus a weighted kappa that gives partial credit for
  near misses (L3 vs L4 counts as closer than L1 vs L4).
- failure_observed: kappa.

Each headline kappa gets a 95% bootstrap confidence interval: we resample the
traces with replacement 2,000 times and see how much kappa moves. With ~12 test
traces the intervals will be wide, and the write-up should say so. No interval
is shown when it would be meaningless: when either coder marked fewer than 3
traces "yes" (or fewer than 3 "no"), or when kappa is undefined in more than 5%
of resamples. The report always shows how many "yes" each coder gave.

Kappa reads roughly as: <0.20 slight, 0.21-0.40 fair, 0.41-0.60 moderate,
0.61-0.80 substantial, >0.80 almost perfect (Landis & Koch, 1977). It is
undefined (n/a) when both coders gave the same single value for every trace.
If only one coder did that, kappa comes out as 0 by construction, which says
"no information" rather than "no agreement"; check the "yes" counts.

Rows are tidied (spaces, capitals) and validated before scoring. Rows with
errors are left out and listed, so a typo can't silently change a result.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

from sklearn.metrics import cohen_kappa_score

from afacs import paths
from afacs.schema import (
    CODING_FIELDS,
    CURRENT_CODEBOOK,
    LAYER_COLUMNS,
    load_codebook_codes,
    normalise_row,
    split_codes,
    validate_coding,
)

RESULTS = paths.ROOT / "results"
LAYERS = ["L4", "L3", "L2", "L1"]
DEEPEST_ORDER = {"none": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4}
BOOTSTRAP_REPS = 2000
SEED = 7

# ---------------------------------------------------------------------------
# Loading codings (human CSV or LLM JSONL) into {uid: row}
# ---------------------------------------------------------------------------


def load_human(path: Path = paths.CALIBRATION_SHEET) -> dict[str, dict]:
    """Rows James has coded, tidied (rows with failure_observed still blank are skipped)."""
    with open(path) as f:
        return {r["uid"]: normalise_row(r) for r in csv.DictReader(f) if (r.get("failure_observed") or "").strip()}


def load_llm(run_name: str) -> dict[str, dict]:
    """Successful rows from an annotator run, tidied."""
    out = {}
    with open(paths.LLM_ANNOTATIONS / f"{run_name}.jsonl") as f:
        for line in f:
            r = json.loads(line)
            if not r.get("error") and "row" in r:
                out[r["uid"]] = normalise_row(r["row"])
    return out


def usable(rows: dict[str, dict], label: str) -> dict[str, dict]:
    """Drop rows that fail validation, saying which and why."""
    codes = load_codebook_codes(CURRENT_CODEBOOK)
    keep = {}
    for uid, row in rows.items():
        errors, _ = validate_coding(row, codes)
        if errors:
            print(f"  [{label}] left out {uid}: {'; '.join(errors)}")
        else:
            keep[uid] = row
    return keep


def load_key() -> dict[str, dict]:
    with open(paths.CALIBRATION_KEY) as f:
        return {r["uid"]: r for r in csv.DictReader(f)}


# ---------------------------------------------------------------------------
# Turning a row into the things we compare
# ---------------------------------------------------------------------------


def codes_of(row: dict) -> set[str]:
    return {c for col in LAYER_COLUMNS.values() for c in split_codes(row.get(col))}


def has_layer(row: dict, layer: str) -> int:
    return int(bool(split_codes(row.get(LAYER_COLUMNS[layer]))))


def any_violation(row: dict) -> int:
    return int(any(c.startswith("L1.V") for c in codes_of(row)))


def kappa(a: list, b: list, weights: str | None = None, labels: list | None = None) -> float | None:
    """Cohen's kappa, or None when it is undefined (no variation at all).

    `labels` fixes the full list of possible values. It matters for weighted kappa:
    without it, sklearn spaces whatever values happen to appear evenly, so "L1 vs
    L4" could count as only one step apart if L2 and L3 never occur.
    """
    if len(a) < 2 or len(set(a) | set(b)) < 2:
        return None
    k = cohen_kappa_score(a, b, weights=weights, labels=labels)
    return None if k != k else float(k)  # NaN -> None


def measures(A: dict, B: dict, uids: list[str], codes: list[str]) -> dict:
    """All agreement figures for one set of traces."""
    m = {"n": len(uids)}
    for layer in LAYERS:
        m[f"layer_{layer}"] = kappa([has_layer(A[u], layer) for u in uids], [has_layer(B[u], layer) for u in uids])
    per_code = {c: kappa([int(c in codes_of(A[u])) for u in uids], [int(c in codes_of(B[u])) for u in uids]) for c in codes}
    defined = [k for k in per_code.values() if k is not None]
    m["codes_macro"] = sum(defined) / len(defined) if defined else None
    m["per_code"] = per_code
    m["any_violation"] = kappa([any_violation(A[u]) for u in uids], [any_violation(B[u]) for u in uids])
    m["violation_flag"] = kappa([A[u]["violation_flag"] for u in uids], [B[u]["violation_flag"] for u in uids])
    da = [DEEPEST_ORDER.get(A[u]["deepest_layer"], 0) for u in uids]
    db = [DEEPEST_ORDER.get(B[u]["deepest_layer"], 0) for u in uids]
    m["deepest_layer"] = kappa(da, db)
    m["deepest_layer_weighted"] = kappa(da, db, weights="linear", labels=sorted(DEEPEST_ORDER.values()))
    # How many traces each coder marked "yes", for the binary measures (needed to judge the CIs).
    m["positives"] = {
        **{f"layer_{L}": (sum(has_layer(A[u], L) for u in uids), sum(has_layer(B[u], L) for u in uids)) for L in LAYERS},
        "any_violation": (sum(any_violation(A[u]) for u in uids), sum(any_violation(B[u]) for u in uids)),
    }
    m["failure_observed"] = kappa([A[u]["failure_observed"] for u in uids], [B[u]["failure_observed"] for u in uids])
    m["raw_agreement_layers"] = (
        sum(has_layer(A[u], L) == has_layer(B[u], L) for u in uids for L in LAYERS) / (4 * len(uids)) if uids else None
    )
    # Strictest level: both coders gave exactly the same set of codes (reported as a plain share,
    # because LLM HFACS coding studies find exact matches far rarer than partial ones).
    m["exact_code_set"] = sum(codes_of(A[u]) == codes_of(B[u]) for u in uids) / len(uids) if uids else None
    return m


HEADLINE = ["layer_L4", "layer_L3", "layer_L2", "layer_L1", "codes_macro", "any_violation", "deepest_layer_weighted", "failure_observed"]
LABELS = {
    "layer_L4": "L4 present (organisational/design)",
    "layer_L3": "L3 present (supervision)",
    "layer_L2": "L2 present (preconditions)",
    "layer_L1": "L1 present (unsafe act)",
    "codes_macro": "Individual codes (mean of per-code κ)",
    "any_violation": "Violation vs error (any L1.V code)",
    "violation_flag": "Violation flag (none/V1/V2/V?)",
    "deepest_layer": "Deepest layer (exact)",
    "deepest_layer_weighted": "Deepest layer (weighted, partial credit)",
    "failure_observed": "Failure observed (yes/no/unclear)",
}


def bootstrap(A: dict, B: dict, uids: list[str], codes: list[str]) -> dict[str, tuple[float, float] | None]:
    rng = random.Random(SEED)
    samples = {k: [] for k in HEADLINE}
    for _ in range(BOOTSTRAP_REPS):
        draw = [rng.choice(uids) for _ in uids]
        m = measures(A, B, draw, codes)
        for k in HEADLINE:
            if m[k] is not None:
                samples[k].append(m[k])
    full = measures(A, B, uids, codes)
    n = len(uids)
    cis = {}
    for k, vals in samples.items():
        too_few = False
        if k in full["positives"]:
            pos_a, pos_b = full["positives"][k]
            too_few = min(pos_a, pos_b, n - pos_a, n - pos_b) < 3
        if too_few or len(vals) < BOOTSTRAP_REPS * 0.95:
            cis[k] = None  # an interval here would look precise but mean nothing
        else:
            vals.sort()
            cis[k] = (vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1])
    return cis


def fmt(k: float | None) -> str:
    return "n/a" if k is None else f"{k:.2f}"


def report(name: str, A: dict, B: dict, uids: list[str], label_a: str, label_b: str) -> dict:
    codes = sorted(load_codebook_codes(CURRENT_CODEBOOK))
    if len(uids) < 2:
        raise SystemExit(f"Only {len(uids)} trace(s) coded by both; need at least 2.")
    m = measures(A, B, uids, codes)
    cis = bootstrap(A, B, uids, codes)
    lines = [
        f"# Agreement: {label_a} vs {label_b}",
        "",
        f"Traces coded by both: **{m['n']}**. Codebook {CURRENT_CODEBOOK}. Bootstrap: {BOOTSTRAP_REPS} resamples.",
        "",
        f"| Measure | Cohen's κ | 95% CI | \"Yes\" count ({label_a} / {label_b}) |",
        "|---|---|---|---|",
    ]
    for k in HEADLINE + ["violation_flag", "deepest_layer"]:
        ci = cis.get(k)
        pos = m["positives"].get(k)
        lines.append(
            f"| {LABELS[k]} | {fmt(m[k])} | {'—' if ci is None else f'{ci[0]:.2f} to {ci[1]:.2f}'} | "
            f"{'' if pos is None else f'{pos[0]} / {pos[1]}'} |"
        )
    lines += ["", "— = no meaningful interval (too few 'yes' or 'no' answers, or κ often undefined when resampling)."]
    lines += [
        "",
        f"Raw agreement on layer presence: {m['raw_agreement_layers']:.0%}. "
        f"Identical full code set: {m['exact_code_set']:.0%} of traces.",
        "",
        "Per-code κ:",
        "",
    ]
    lines.append(", ".join(f"`{c}` {fmt(k)}" for c, k in m["per_code"].items()))
    text = "\n".join(lines) + "\n"
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"agreement_{name}.md").write_text(text)
    (RESULTS / f"agreement_{name}.json").write_text(json.dumps({"measures": m, "ci95": cis}, indent=2))
    print(text)
    print(f"(saved to results/agreement_{name}.md)")
    return m


# ---------------------------------------------------------------------------


def check_sheet() -> None:
    codes = load_codebook_codes(CURRENT_CODEBOOK)
    with open(paths.CALIBRATION_SHEET) as f:
        rows = list(csv.DictReader(f))
    coded = [r for r in rows if (r.get("failure_observed") or "").strip()]
    print(f"{len(coded)} of {len(rows)} traces coded.")
    problems = 0
    for r in coded:
        errors, warnings = validate_coding({k: r.get(k, "") for k in CODING_FIELDS}, codes)
        for e in errors:
            print(f"  {r['cal_id']} ERROR   {e}")
        for w in warnings:
            print(f"  {r['cal_id']} warning {w}")
        problems += len(errors)
    print("No errors." if problems == 0 else f"{problems} error(s) to fix.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("check-sheet")
    p = sub.add_parser("human-vs-llm")
    p.add_argument("--run", required=True, help="annotator run name (annotations/llm/<run>.jsonl)")
    p.add_argument("--split", choices=["dev", "test", "all"], default="test")
    p = sub.add_parser("llm-vs-llm")
    p.add_argument("--run-a", required=True)
    p.add_argument("--run-b", required=True)
    args = ap.parse_args()

    if args.command == "check-sheet":
        check_sheet()
    elif args.command == "human-vs-llm":
        key = load_key()
        human, llm = usable(load_human(), "human"), usable(load_llm(args.run), args.run)
        in_split = [u for u in human if args.split == "all" or key[u]["split"] == args.split]
        missing = [u for u in in_split if u not in llm]
        if missing:
            print(f"  WARNING: {len(missing)} human-coded {args.split} trace(s) have no usable LLM coding "
                  f"(API error, refusal or invalid row) and are left out: {', '.join(missing)}")
        uids = sorted(u for u in in_split if u in llm)
        report(f"human_vs_{args.run}_{args.split}", human, llm, uids, "James", args.run)
    else:
        a, b = usable(load_llm(args.run_a), args.run_a), usable(load_llm(args.run_b), args.run_b)
        uids = sorted(set(a) & set(b))
        report(f"{args.run_a}_vs_{args.run_b}", a, b, uids, args.run_a, args.run_b)


if __name__ == "__main__":
    main()
