"""Step 7: the pre-registered analysis.

Usage:
  python scripts/07_analyse.py                                 analyses results/raw/main.jsonl
  python scripts/07_analyse.py --input results/sim/main.jsonl  analyses a simulated file

It writes results/analysis/summary.md, plus CSV tables, next to the input's analysis folder.
"""
import argparse
import csv
import json
import pathlib
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from stats import bootstrap_ci, fleiss_kappa, holm, wilcoxon  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
QUESTIONS = ["q1", "q1b", "q2", "q2b", "q3", "q3b", "q4", "q4b", "q5"]
CONTROL_EXPECTED = {"K1": 1, "K2": 1, "K3": 1, "K4": 6, "K5": 6, "K6": 6}


def load(path):
    recs = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r.get("valid") and r["call_id"] not in recs:
            recs[r["call_id"]] = r
    return list(recs.values())


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "results" / "raw" / "main.jsonl"))
    args = ap.parse_args()
    inp = pathlib.Path(args.input)
    out_dir = inp.parent.parent / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)

    cases = {c["case_id"]: c for c in json.loads((ROOT / "cases" / "cases.json").read_text(encoding="utf-8"))}
    recs = load(inp)
    models = sorted({r["model"] for r in recs})
    lines = ["# Results summary", "",
             f"*Input: `{inp.name}`, {len(recs)} valid replies. Main cases only unless stated; pilot cases excluded.*", ""]

    by = defaultdict(list)  # (model, case, version) -> records
    for r in recs:
        by[(r["model"], r["case_id"], r["version"])].append(r)
    main_ids = sorted(c for c, v in cases.items() if v["set"] == "main")

    def rank(r):
        return r["details"]["derived_rank"]

    # H1
    lines += ["## H1: outcome effect on culpability rank (higher = more culpable)", "",
              "| Model | Cases | Harsher | Same | More lenient | Mean shift (steps) | 95% CI | W+ | z | p | p (Holm) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    h1, h1_rows = [], []
    for m in models:
        d = []
        for c in main_ids:
            bad, safe = by[(m, c, "bad")], by[(m, c, "safe")]
            if bad and safe:
                d.append(mean([rank(r) for r in bad]) - mean([rank(r) for r in safe]))
        n, w, z, p = wilcoxon(d)
        lo, hi = bootstrap_ci(d)
        h1.append((m, d, n, w, z, p, lo, hi))
    adj = holm([x[5] for x in h1])
    for (m, d, n, w, z, p, lo, hi), pa in zip(h1, adj):
        harsher, same, lenient = sum(x > 0 for x in d), sum(x == 0 for x in d), sum(x < 0 for x in d)
        lines.append(f"| {m} | {len(d)} | {harsher} | {same} | {lenient} | {mean(d):+.2f} | "
                     f"[{lo:+.2f}, {hi:+.2f}] | {w:.1f} | {z:+.2f} | {p if p is None else f'{p:.4f}'} | "
                     f"{pa if pa is None else f'{pa:.4f}'} |")
        h1_rows.append({"model": m, "cases": len(d), "harsher": harsher, "same": same, "lenient": lenient,
                        "mean_shift": mean(d), "ci_low": lo, "ci_high": hi, "W_plus": w, "z": z, "p": p,
                        "p_holm": pa})
    lines.append("")

    # H2
    lines += ["## H2: substitution test, share of 'pass' answers (bad minus safe)", "",
              "| Model | Cases | Mean difference in pass rate | 95% CI | p | p (Holm) |", "|---|---|---|---|---|---|"]
    h2 = []
    for m in models:
        d = []
        for c in main_ids:
            bad, safe = by[(m, c, "bad")], by[(m, c, "safe")]
            sb = [r["details"]["substitution_independent"] == "yes" for r in bad
                  if r["details"]["substitution_independent"]]
            ss = [r["details"]["substitution_independent"] == "yes" for r in safe
                  if r["details"]["substitution_independent"]]
            if sb and ss:
                d.append(mean(sb) - mean(ss))
        n, w, z, p = wilcoxon(d)
        lo, hi = bootstrap_ci(d)
        h2.append((m, d, p, lo, hi))
    for (m, d, p, lo, hi), pa in zip(h2, holm([x[2] for x in h2])):
        lines.append(f"| {m} | {len(d)} | {mean(d):+.3f} | [{lo:+.3f}, {hi:+.3f}] | "
                     f"{p if p is None else f'{p:.4f}'} | {pa if pa is None else f'{pa:.4f}'} |")
    lines.append("")

    # H3
    lines += ["## H3: consistency across the 5 repeats", "",
              "| Model | Cells | All 5 repeats same outcome | Fleiss' kappa |", "|---|---|---|---|"]
    for m in models:
        cells = defaultdict(list)
        for r in recs:
            if r["model"] == m and r["case_id"] in main_ids:
                cells[(r["case_id"], r["version"], r["wording"])].append(r["details"]["derived_outcome"])
        full = [v for v in cells.values() if len(v) == 5]
        same = sum(len(set(v)) == 1 for v in full)
        k = fleiss_kappa(full)
        lines.append(f"| {m} | {len(full)} | {same}/{len(full)} ({same / len(full):.0%}) | "
                     f"{'n/a' if k is None else f'{k:.3f}'} |" if full else f"| {m} | 0 | n/a | n/a |")
    lines.append("")

    # Which question flips
    lines += ["## Which question flips between versions (share of cases whose majority answer differs)", "",
              "| Model | " + " | ".join(QUESTIONS) + " |", "|---|" + "---|" * len(QUESTIONS)]
    for m in models:
        row = []
        for q in QUESTIONS:
            flips, n = 0, 0
            for c in main_ids:
                bad, safe = by[(m, c, "bad")], by[(m, c, "safe")]
                if not bad or not safe:
                    continue
                def maj(rs):
                    return Counter(((r.get("reply") or {}).get(q) or {}).get("answer", "not on path")
                                   if isinstance((r.get("reply") or {}).get(q), dict) else "not on path"
                                   for r in rs).most_common(1)[0][0]
                n += 1
                flips += maj(bad) != maj(safe)
            row.append(f"{flips / n:.0%}" if n else "n/a")
        lines.append(f"| {m} | " + " | ".join(row) + " |")
    lines.append("")

    # Checks
    lines += ["## Checks", "", "| Model | Manipulation: bad rated more severe | Fixed-line 'yes' (substance or history) | "
              "Named outcome matches derived |", "|---|---|---|---|"]
    for m in models:
        higher, n = 0, 0
        for c in main_ids:
            sb = [r["details"]["severity"] for r in by[(m, c, "bad")] if r["details"]["severity"]]
            ss = [r["details"]["severity"] for r in by[(m, c, "safe")] if r["details"]["severity"]]
            if sb and ss:
                n += 1
                higher += mean(sb) > mean(ss)
        mine = [r for r in recs if r["model"] == m and r["case_id"] in main_ids]
        fixed_yes = sum(any(((r.get("reply") or {}).get(q) or {}).get("answer") == "yes"
                            for q in ("q2", "q5") if isinstance((r.get("reply") or {}).get(q), dict))
                        for r in mine)
        named = sum(r["details"]["named_matches"] for r in mine)
        lines.append(f"| {m} | {higher}/{n} ({higher / n:.0%}) | {fixed_yes}/{len(mine)} "
                     f"({fixed_yes / len(mine):.1%}) | {named}/{len(mine)} ({named / len(mine):.0%}) |"
                     if n and mine else f"| {m} | n/a | n/a | n/a |")
    lines.append("")

    # Controls
    ctrl_ids = sorted(c for c, v in cases.items() if v["set"] == "control")
    if ctrl_ids:
        lines += ["## Controls (modal derived outcome rank; expected in brackets)", "",
                  "| Model | " + " | ".join(f"{c} safe / bad ({CONTROL_EXPECTED.get(c, '?')})" for c in ctrl_ids) + " |",
                  "|---|" + "---|" * len(ctrl_ids)]
        for m in models:
            cells = []
            for c in ctrl_ids:
                def mode(v):
                    rs = by[(m, c, v)]
                    return Counter(rank(r) for r in rs).most_common(1)[0][0] if rs else "-"
                cells.append(f"{mode('safe')} / {mode('bad')}")
            lines.append(f"| {m} | " + " | ".join(cells) + " |")
        lines.append("")

    # Exploratory
    lines += ["## Exploratory (labelled as such in any write-up)", "",
              "### Mean shift by wording, category and primary problem", "",
              "| Model | W1 | W2 | " + " | ".join(f"cat {k}" for k in "ABCDF") + " | Human Factors | Procedure |",
              "|---|---|---|" + "---|" * 5 + "---|---|"]
    for m in models:
        def shift(filter_case=lambda c: True, wording=None):
            d = []
            for c in main_ids:
                if not filter_case(c):
                    continue
                bad = [r for r in by[(m, c, "bad")] if wording in (None, r["wording"])]
                safe = [r for r in by[(m, c, "safe")] if wording in (None, r["wording"])]
                if bad and safe:
                    d.append(mean([rank(r) for r in bad]) - mean([rank(r) for r in safe]))
            return f"{mean(d):+.2f} (n={len(d)})" if d else "n/a"
        cells = [shift(wording="W1"), shift(wording="W2")]
        cells += [shift(lambda c, k=k: cases[c]["category"] == k) for k in "ABCDF"]
        cells += [shift(lambda c: cases[c]["primary_problem"] == "Human Factors"),
                  shift(lambda c: cases[c]["primary_problem"] == "Procedure")]
        lines.append(f"| {m} | " + " | ".join(cells) + " |")
    lines.append("")

    # Exploratory: do the models remark that the ending seems implausible or inconsistent?
    import re as _re
    pat = _re.compile(r"implausib|inconsisten|unlikely (outcome|result|consequence)|contradict|does(n't| not) "
                      r"(match|fit|follow)|surpris(ing|ed) (outcome|result)|out of proportion", _re.I)
    lines += ["### Remarks that the ending looks implausible or inconsistent (share of replies)", "",
              "| Model | Safe version | Bad version |", "|---|---|---|"]
    for m in models:
        cells = []
        for v in ("safe", "bad"):
            rs = [r for r in recs if r["model"] == m and r["case_id"] in main_ids and r["version"] == v]
            hits = sum(bool(pat.search(json.dumps(r.get("reply") or {}, ensure_ascii=False))) for r in rs)
            cells.append(f"{hits}/{len(rs)} ({hits / len(rs):.1%})" if rs else "n/a")
        lines.append(f"| {m} | " + " | ".join(cells) + " |")
    lines.append("")

    (out_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    with (out_dir / "h1.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(h1_rows[0]) if h1_rows else ["model"])
        w.writeheader()
        w.writerows(h1_rows)
    print(f"wrote {out_dir / 'summary.md'}")


if __name__ == "__main__":
    main()
