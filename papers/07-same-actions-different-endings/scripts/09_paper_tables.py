"""Step 9: descriptive tables and figures for the paper.

Usage:
  python scripts/09_paper_tables.py

Written on 2 Oct 2026, after the registered analysis (07_analyse.py) had run. Nothing here is a
new test of H1-H3. It describes the same replies in other ways, for the write-up, and every table
it writes is labelled descriptive or exploratory. It also covers one registered exploratory item
that 07_analyse.py left out: the "insufficient information" flags on the procedures question
(q3b), by version.

It writes results/analysis/paper-tables.md, fig1-case-shifts.svg and fig2-outcomes.svg.
"""
import json
import pathlib
import sys
from collections import Counter, defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from stats import bootstrap_ci  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "analysis"
SHORT = {"anthropic/claude-sonnet-5.5": "Claude Sonnet 5.5", "openai/gpt-6.1-sol": "GPT-6.1 Sol",
         "deepseek/deepseek-v4-pro": "DeepSeek V4 Pro"}
NAMES = {1: "Blameless error", 2: "Blameless error, training or counselling indicated",
         3: "System-induced error", 4: "Possible negligent error", 5: "System-induced violation",
         6: "Possible reckless violation", 7: "Substance abuse with mitigation",
         8: "Substance abuse without mitigation", 9: "Sabotage, malevolent damage, suicide etc."}
QUESTIONS = ["q1", "q1b", "q2", "q2b", "q3", "q3b", "q4", "q4b", "q5"]


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def pct(a, b):
    return f"{a}/{b} ({a / b:.0%})" if b else "n/a"


def pearson(x, y):
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return sxy / (sx * sy) if sx and sy else None


def main():
    cases = {c["case_id"]: c for c in json.loads((ROOT / "cases" / "cases.json").read_text(encoding="utf-8"))}
    attempts = [json.loads(l) for l in (ROOT / "results" / "raw" / "main.jsonl").read_text(encoding="utf-8").splitlines()]
    recs = {}
    for r in attempts:
        if r.get("valid") and r["call_id"] not in recs:
            recs[r["call_id"]] = r
    recs = list(recs.values())
    models = [m for m in SHORT if any(r["model"] == m for r in recs)]
    main_ids = sorted(c for c, v in cases.items() if v["set"] == "main")
    ctrl_ids = sorted(c for c, v in cases.items() if v["set"] == "control")
    by = defaultdict(list)
    for r in recs:
        by[(r["model"], r["case_id"], r["version"])].append(r)
    L = ["# Descriptive tables for the paper", "",
         "*Produced by `scripts/09_paper_tables.py` after the registered analysis. Descriptive or exploratory "
         "only; the registered tests are in `summary.md`. Main cases only unless stated.*", ""]

    # 1. Data collection
    L += ["## T1. Data collection, by model", "",
          "| Model | Planned calls | Valid | Requests refused (HTTP 429) | Other invalid attempts | Cost (USD) | "
          "Mean input tokens | Mean output tokens | Providers serving the model |", "|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        a = [r for r in attempts if r["model"] == m]
        v = [r for r in recs if r["model"] == m]
        refused = sum("429" in (r.get("error") or "") for r in a)
        other = sum(1 for r in a if not r.get("valid") and "429" not in (r.get("error") or ""))
        cost = sum(r.get("cost_usd") or 0 for r in a)
        pin = mean([r["usage"].get("prompt_tokens", 0) for r in v])
        pout = mean([r["usage"].get("completion_tokens", 0) for r in v])
        prov = Counter(r.get("provider") or "?" for r in v)
        L.append(f"| {SHORT[m]} | 1080 | {len(v)} | {refused} | {other} | {cost:.2f} | {pin:,.0f} | {pout:,.0f} | "
                 + "; ".join(f"{k} ({n})" for k, n in prov.most_common()) + " |")
    L.append("")

    # 2. Outcome distribution
    present = sorted({r["details"]["derived_rank"] for r in recs if r["case_id"] in main_ids})
    L += ["## T2. Derived outcome, share of replies by version (descriptive)", "",
          "| Model | Version | n | " + " | ".join(NAMES[k] for k in present) + " |",
          "|---|---|---|" + "---|" * len(present)]
    dist = {}
    for m in models:
        for ver in ("safe", "bad"):
            rs = [r for c in main_ids for r in by[(m, c, ver)]]
            cnt = Counter(r["details"]["derived_rank"] for r in rs)
            dist[(m, ver)] = {k: cnt[k] / len(rs) for k in present}
            L.append(f"| {SHORT[m]} | {ver} | {len(rs)} | " + " | ".join(f"{cnt[k] / len(rs):.1%}" for k in present) + " |")
    L.append("")
    L += ["Grouped: *blameless* = ranks 1–2; *system-attributed* = ranks 3 and 5; *crew culpability indicated* = "
          "ranks 4 and 6 (Reason's two \"possible\" culpable outcomes).", "",
          "| Model | Blameless, safe → bad | System-attributed, safe → bad | Crew culpability indicated, safe → bad |",
          "|---|---|---|---|"]
    for m in models:
        g = {}
        for ver in ("safe", "bad"):
            d = dist[(m, ver)]
            g[ver] = (sum(d.get(k, 0) for k in (1, 2)), sum(d.get(k, 0) for k in (3, 5)), sum(d.get(k, 0) for k in (4, 6)))
        L.append(f"| {SHORT[m]} | " + " | ".join(f"{g['safe'][i]:.1%} → {g['bad'][i]:.1%}" for i in range(3)) + " |")
    L.append("")

    # 3. Modal transitions per case
    L += ["## T3. Each case's most common outcome, safe version → bad version (cases where it changed; descriptive)", "",
          "Ties are broken towards the less culpable outcome, the same way for both versions.", "",
          "| Model | Transition | Cases |", "|---|---|---|"]

    def modal(rs):
        c = Counter(r["details"]["derived_rank"] for r in rs)
        top = max(c.values())
        return min(k for k, n in c.items() if n == top)
    for m in models:
        tr = Counter()
        for c in main_ids:
            s, b = modal(by[(m, c, "safe")]), modal(by[(m, c, "bad")])
            if s != b:
                tr[(s, b)] += 1
        for (s, b), n in sorted(tr.items(), key=lambda x: -x[1]):
            L.append(f"| {SHORT[m]} | {NAMES[s]} → {NAMES[b]} | {n} |")
        if not tr:
            L.append(f"| {SHORT[m]} | none | 0 |")
    L.append("")

    # 4. Substitution, severity, insufficient information
    L += ["## T4. Substitution test (answered separately), severity and \"insufficient information\" flags, by version", "",
          "| Model | Substitution 'pass', safe | Substitution 'pass', bad | Mean severity, safe | Mean severity, bad | "
          "Replies with any insufficient-information flag, safe | ... bad | q3b (procedures) flagged, safe | ... bad |",
          "|---|---|---|---|---|---|---|---|---|"]
    for m in models:
        row = []
        for ver in ("safe", "bad"):
            rs = [r for c in main_ids for r in by[(m, c, ver)]]
            row.append(pct(sum(r["details"]["substitution_independent"] == "yes" for r in rs), len(rs)))
        for ver in ("safe", "bad"):
            rs = [r for c in main_ids for r in by[(m, c, ver)]]
            row.append(f"{mean([r['details']['severity'] for r in rs if r['details']['severity']]):.2f}")
        for ver in ("safe", "bad"):
            rs = [r for c in main_ids for r in by[(m, c, ver)]]
            row.append(pct(sum(any((r["details"].get("insufficient_info") or {}).values()) for r in rs), len(rs)))
        for ver in ("safe", "bad"):
            rs = [r for c in main_ids for r in by[(m, c, ver)] if "q3b" in (r["details"].get("insufficient_info") or {})]
            row.append(pct(sum(bool(r["details"]["insufficient_info"]["q3b"]) for r in rs), len(rs)) + " of replies reaching q3b")
        L.append(f"| {SHORT[m]} | " + " | ".join(row) + " |")
    L.append("")

    # 5. Per-question answers by version
    L += ["## T5. Share of replies answering 'yes' at each question they reached, by version (descriptive)", "",
          "| Model | Version | " + " | ".join(QUESTIONS) + " |", "|---|---|" + "---|" * len(QUESTIONS)]
    for m in models:
        for ver in ("safe", "bad"):
            rs = [r for c in main_ids for r in by[(m, c, ver)]]
            cells = []
            for q in QUESTIONS:
                ans = [a for r in rs for (qq, a) in r["details"]["path"] if qq == q]
                cells.append(f"{sum(a == 'yes' for a in ans)}/{len(ans)}" if ans else "–")
            L.append(f"| {SHORT[m]} | {ver} | " + " | ".join(cells) + " |")
    L.append("")

    # 6. Controls
    L += ["## T6. Controls: mean derived rank by version (expected rank in brackets)", "",
          "| Model | " + " | ".join(f"{c} ({cases[c].get('expected_rank', '?')})" for c in ctrl_ids) + " |",
          "|---|" + "---|" * len(ctrl_ids)]
    for m in models:
        cells = []
        for c in ctrl_ids:
            s = mean([r["details"]["derived_rank"] for r in by[(m, c, "safe")]])
            b = mean([r["details"]["derived_rank"] for r in by[(m, c, "bad")]])
            cells.append(f"{s:.1f} / {b:.1f}")
        L.append(f"| {SHORT[m]} | " + " | ".join(cells) + " |")
    L.append("")

    # 7. Agreement between models on which cases shift
    shifts = {m: {c: mean([r["details"]["derived_rank"] for r in by[(m, c, "bad")]])
                  - mean([r["details"]["derived_rank"] for r in by[(m, c, "safe")]]) for c in main_ids} for m in models}
    L += ["## T7. Do the models shift on the same cases? (exploratory)", ""]
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            r = pearson([shifts[a][c] for c in main_ids], [shifts[b][c] for c in main_ids])
            L.append(f"- Pearson correlation of per-case shifts, {SHORT[a]} and {SHORT[b]}: r = {r:.2f}")
    all3 = sum(all(shifts[m][c] > 0 for m in models) for c in main_ids)
    any1 = sum(any(shifts[m][c] > 0 for m in models) for c in main_ids)
    none = sum(all(shifts[m][c] == 0 for m in models) for c in main_ids)
    L += [f"- Cases harsher for all three models: {all3} of {len(main_ids)}; for at least one: {any1}; "
          f"unchanged for all three: {none}.", ""]

    # 8. Case table
    L += ["## T8. Per-case shift in mean rank (bad minus safe), by model", "",
          "| Case | Category | Primary problem | " + " | ".join(SHORT[m] for m in models) + " |",
          "|---|---|---|" + "---|" * len(models)]
    for c in main_ids:
        L.append(f"| {c} | {cases[c]['category']} | {cases[c]['primary_problem']} | "
                 + " | ".join(f"{shifts[m][c]:+.1f}" for m in models) + " |")
    L.append("")
    (OUT / "paper-tables.md").write_text("\n".join(L), encoding="utf-8")

    # Figure 2: stacked bars of outcome shares
    colours = {1: "#d9e7f5", 2: "#b7d2ec", 3: "#9ec9a6", 4: "#f2b36b", 5: "#7fae86", 6: "#c8553d",
               7: "#8a3b2c", 8: "#6b2a1f", 9: "#3d1712"}
    order = [k for k in (1, 2, 3, 5, 4, 6, 7, 8, 9) if k in present]
    W, left, barw, barh, gap = 760, 120, 600, 26, 14
    y, svg = 44, []
    for m in models:
        svg.append(f'<text x="10" y="{y + 14}" font-size="14" font-weight="600">{SHORT[m]}</text>')
        y += 22
        for ver in ("safe", "bad"):
            x = left
            svg.append(f'<text x="{left - 10}" y="{y + 18}" font-size="12" text-anchor="end">'
                       f'{"Safe ending" if ver == "safe" else "Bad ending"}</text>')
            for k in order:
                w = dist[(m, ver)].get(k, 0) * barw
                if w > 0:
                    svg.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{barh}" fill="{colours[k]}" '
                               f'stroke="#ffffff" stroke-width="0.5"/>')
                    if w > 34:
                        svg.append(f'<text x="{x + w / 2:.1f}" y="{y + 17}" font-size="11" text-anchor="middle">'
                                   f'{dist[(m, ver)][k]:.0%}</text>')
                x += w
            y += barh + 4
        y += gap
    ly = y + 6
    lx = 10
    for k in order:
        svg.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" fill="{colours[k]}"/>')
        svg.append(f'<text x="{lx + 16}" y="{ly + 10}" font-size="11">{NAMES[k]}</text>')
        lx += 16 + 6.2 * len(NAMES[k]) + 16
        if lx > W - 150:
            lx, ly = 10, ly + 18
    H = ly + 30
    fig1 = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">'
            f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
            f'<text x="10" y="24" font-size="15" font-weight="700">Figure 2. Outcome reached on Reason\'s tree, '
            f'share of replies (48 cases, 480 replies per bar)</text>' + "".join(svg) + "</svg>")
    (OUT / "fig2-outcomes.svg").write_text(fig1, encoding="utf-8")

    # Figure 1: per-case shifts with mean and 95% CI
    lo_x, hi_x = -1.5, 3.0
    W, left, right = 760, 170, 730

    def sx(v):
        return left + (v - lo_x) / (hi_x - lo_x) * (right - left)
    svg, y = [], 60
    for t in [-1, 0, 1, 2, 3]:
        svg.append(f'<line x1="{sx(t):.1f}" y1="45" x2="{sx(t):.1f}" y2="{45 + 70 * len(models)}" '
                   f'stroke="{"#555555" if t == 0 else "#dddddd"}" stroke-width="{1.2 if t == 0 else 1}"/>')
        svg.append(f'<text x="{sx(t):.1f}" y="{62 + 70 * len(models)}" font-size="11" text-anchor="middle">{f"{t:+d}" if t else "0"}</text>')
    for m in models:
        d = [shifts[m][c] for c in main_ids]
        svg.append(f'<text x="10" y="{y + 18}" font-size="13" font-weight="600">{SHORT[m]}</text>')
        seen = Counter()
        for v in sorted(d):
            k = round(v, 2)
            off = (seen[k] % 9 - 4) * 3.2
            seen[k] += 1
            svg.append(f'<circle cx="{sx(v):.1f}" cy="{y + 14 + off:.1f}" r="3.2" fill="#4a6fa5" fill-opacity="0.55"/>')
        mu = mean(d)
        lo, hi = bootstrap_ci(d)
        svg.append(f'<text x="{sx(0) - 8:.1f}" y="{y + 42}" font-size="11" text-anchor="end">'
                   f'{sum(v == 0 for v in d)} cases at 0</text>')
        svg.append(f'<line x1="{sx(lo):.1f}" y1="{y + 38}" x2="{sx(hi):.1f}" y2="{y + 38}" stroke="#c8553d" stroke-width="2.5"/>')
        svg.append(f'<rect x="{sx(mu) - 4:.1f}" y="{y + 34}" width="8" height="8" fill="#c8553d"/>')
        svg.append(f'<text x="{sx(hi) + 8:.1f}" y="{y + 42}" font-size="11">mean {mu:+.2f} [{lo:+.2f}, {hi:+.2f}]</text>')
        y += 70
    H = y + 30
    fig2 = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">'
            f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
            f'<text x="10" y="24" font-size="15" font-weight="700">Figure 1. Per-case shift in mean culpability rank, '
            f'bad ending minus safe ending</text>'
            f'<text x="10" y="40" font-size="11">Each dot is one of the 48 cases (10 replies per version). '
            f'Square and bar: mean and 95% bootstrap CI. Above 0 = harsher when the ending was bad.</text>'
            + "".join(svg) + f'<text x="{(left + right) / 2}" y="{H - 8}" font-size="11" text-anchor="middle">'
            f'Shift in Reason\'s rank (steps)</text></svg>')
    (OUT / "fig1-case-shifts.svg").write_text(fig2, encoding="utf-8")
    print(f"wrote {OUT / 'paper-tables.md'} and two figures")


if __name__ == "__main__":
    main()
