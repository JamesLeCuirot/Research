"""Stage 6 - analysis: answer the research questions and draw the figures.

Run:
    uv run afacs-analysis mast                      # figures about the MAST data itself (works now)
    uv run afacs-analysis afacs --run sonnet_bulk_p1   # RQ2-RQ4 from an annotator run on the bulk set
    uv run afacs-analysis afacs --human             # the same analysis on James's calibration coding

RQ2 (latent causes): share of failed traces with a code at each layer, and the
share with any contributor above the unsafe-act layer (L2, L3 or L4).
RQ3 (errors vs violations): share of failed traces with a violation code, by
framework and by model; and how MAST's FM-1.1 "Disobey Task Specification"
splits into errors and violations.
RQ4 (cross-walk): for traces carrying each MAST label, how often each AFACS
layer and code appears. A MAST label that maps to one layer is "one-to-one";
one spread across several layers, or across errors and violations, "conflates".

Proportions come with 95% Wilson confidence intervals (a standard interval for
a share, better behaved than "p ± 2 standard errors" when n is small or p is
near 0 or 1).
"""

from __future__ import annotations

import argparse
import csv
import textwrap
import json
import math
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")  # draw to files, no screen needed
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

from afacs import design, paths  # noqa: E402
from afacs.agreement import RESULTS, any_violation, codes_of, has_layer, load_human, load_llm, usable  # noqa: E402
from afacs.ingest import load_traces  # noqa: E402
from afacs.quotes import report_lines  # noqa: E402
from afacs.schema import CURRENT_CODEBOOK, EZELL_FUNCTIONS, load_codebook_codes, split_codes, split_labels  # noqa: E402

LAYERS = ["L4", "L3", "L2", "L1"]
LAYER_NAMES = {"L4": "L4 Organisational/design", "L3": "L3 Supervision", "L2": "L2 Preconditions", "L1": "L1 Unsafe acts"}

# ---- Figure style (reference palette from the dataviz guidance) -------------
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
SERIES_1 = "#2a78d6"
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
SEQ = LinearSegmentedColormap.from_list("afacs_blue", BLUE_RAMP)

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.labelcolor": INK_2, "xtick.color": INK_2, "ytick.color": INK_2,
    "axes.edgecolor": GRID, "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
})


def wilson(k: float, n: float, z: float = 1.96) -> tuple[float, float, float]:
    """Share k/n with its 95% Wilson interval: (p, low, high). n may be an effective (non-whole) size."""
    if n <= 0:
        return (float("nan"),) * 3
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    # min/max guard against floating-point rounding putting p a hair outside its own interval
    return p, max(0.0, min(p, centre - half)), min(1.0, max(p, centre + half))


def weighted_share(uids: list[str], flag, weights: dict[str, float]) -> tuple[float, float, float]:
    """Weighted share of `uids` for which flag(uid) is true, with a Wilson interval.

    The bulk sample is deliberately not proportional (small frameworks and models
    are over-sampled), so each trace carries a weight: how many traces in the
    eligible pool it stands for. The share is sum(weight x flag) / sum(weight).
    Weighting makes the estimate less precise, so the interval uses the "effective
    sample size" (Kish): (sum of weights)^2 / (sum of squared weights). With equal
    weights this is simply n, and the result is the ordinary share.
    """
    if not uids:
        return (float("nan"),) * 3
    w = [weights.get(u, 1.0) for u in uids]
    total = sum(w)
    p = sum(wi for u, wi in zip(uids, w) if flag(u)) / total
    n_eff = total**2 / sum(wi * wi for wi in w)
    return wilson(p * n_eff, n_eff)


def load_bulk_weights() -> dict[str, float]:
    if not paths.BULK_SAMPLE.exists():
        return {}
    with open(paths.BULK_SAMPLE) as f:
        return {r["uid"]: float(r["weight"]) for r in csv.DictReader(f)}


def pct(p: float, lo: float | None = None, hi: float | None = None) -> str:
    if p != p:
        return "n/a"
    return f"{p:.0%}" if lo is None else f"{p:.0%} ({lo:.0%}–{hi:.0%})"


def heatmap(matrix, row_labels, col_labels, title, path, row_note=None, fmt="{:.0%}", vmax=1.0, xlabel=""):
    """A one-hue (light->dark blue) heatmap with the value printed in each cell."""
    h = 0.42 * len(row_labels) + 1.6
    w = 0.62 * len(col_labels) + 3.6
    fig, ax = plt.subplots(figsize=(w, h), layout="constrained")
    im = ax.imshow(matrix, cmap=SEQ, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(col_labels)), col_labels, rotation=45, ha="right")
    ax.set_yticks(range(len(row_labels)), [f"{r}  {row_note[i]}" if row_note else r for i, r in enumerate(row_labels)])
    for i, row in enumerate(matrix):
        for j, v in enumerate(row):
            if v == v:  # skip NaN
                ax.text(j, i, fmt.format(v), ha="center", va="center", fontsize=8,
                        color="white" if v > 0.55 * vmax else INK)
    ax.set_xticks([x - 0.5 for x in range(1, len(col_labels))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(row_labels))], minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)  # 2px surface gap between cells
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.suptitle(textwrap.fill(title, 48), x=0.02, ha="left", fontweight="bold")  # wrapped so it is never clipped
    ax.set_xlabel(xlabel)
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(length=0)
    paths.FIGURES.mkdir(exist_ok=True)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path.relative_to(paths.ROOT)}")


def hbar_panels(panels: dict[str, list[tuple[str, float, float, float, int]]], title: str, path, xlabel="Share of failed traces"):
    """Small multiples: one panel per layer, horizontal bars per group with CI whiskers."""
    n = len(panels)
    rows = max(len(v) for v in panels.values())
    fig, axes = plt.subplots(1, n, figsize=(2.9 * n + 1.2, 0.36 * rows + 1.6), sharey=True)
    axes = [axes] if n == 1 else axes
    for ax, (name, items) in zip(axes, panels.items()):
        labels = [it[0] for it in items]
        ys = range(len(items))
        vals = [it[1] for it in items]
        err = [[it[1] - it[2] for it in items], [it[3] - it[1] for it in items]]
        ax.barh(ys, vals, height=0.62, color=SERIES_1, edgecolor=SURFACE, linewidth=2)
        ax.errorbar(vals, ys, xerr=err, fmt="none", ecolor=INK_2, elinewidth=1, capsize=0)
        ax.set_yticks(list(ys), [f"{lab} (n={it[4]})" for lab, it in zip(labels, items)])
        ax.set_xlim(0, 1)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(length=0)
        ax.set_title(name, loc="left", fontsize=10)
    axes[0].invert_yaxis()  # first group on top; the panels share this axis, so flip it once
    fig.suptitle(title, x=0.01, ha="left", fontweight="bold")
    fig.supxlabel(xlabel, color=INK_2, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    print(f"  wrote {path.relative_to(paths.ROOT)}")


# ---------------------------------------------------------------------------
# MAST-only figures (no AFACS coding needed)
# ---------------------------------------------------------------------------


def mast_figures() -> None:
    traces = [t for t in load_traces() if t["quality_exclusion"] is None]
    fws = sorted({t["framework"] for t in traces}, key=lambda f: (f in design.EXCLUDED_FRAMEWORKS, f))
    matrix = []
    for c in design.MAST_CODES:
        row = []
        for fw in fws:
            ts = [t for t in traces if t["framework"] == fw]
            row.append(sum(t["mast_labels"][c] == 1 for t in ts) / len(ts))
        matrix.append(row)
    col_labels = [f"{fw}{' (excl.)' if fw in design.EXCLUDED_FRAMEWORKS else ''}\nn={sum(t['framework'] == fw for t in traces)}" for fw in fws]
    heatmap(
        matrix, design.MAST_CODES, col_labels, "How often MAST's judge flags each failure mode, by framework",
        paths.FIGURES / "mast_prevalence_by_framework.png", row_note=[design.MAST_NAMES[c] for c in design.MAST_CODES],
    )

    audit = json.loads(paths.AUDIT_JSON.read_text())
    retest = audit["duplicates"]["test_retest"].get("magentic_cross_group")
    if retest:
        items = [(c, k) for c, k in retest["per_code_kappa"].items()]
        fig, ax = plt.subplots(figsize=(7.2, 5.2))
        ys = list(range(len(items)))
        vals = [k if k is not None else 0 for _, k in items]
        ax.barh(ys, vals, height=0.62, color=SERIES_1, edgecolor=SURFACE, linewidth=2)
        ax.set_yticks(ys, [f"{c}  {design.MAST_NAMES[c]}" for c, _ in items])
        ax.invert_yaxis()
        for y, (_, k) in zip(ys, items):
            ax.text((k if k is not None else 0) + 0.02 if (k or 0) >= 0 else 0.02, y, "n/a" if k is None else f"{k:.2f}",
                    va="center", fontsize=8, color=INK_2)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.axvline(0, color=INK_2, linewidth=0.8)
        ax.set_xlim(-0.2, 1.0)
        ax.set_xlabel("Cohen's κ between two judge runs on the same trace\n"
                      "(Landis & Koch: 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial)", fontsize=9)
        ax.tick_params(length=0)
        fig.suptitle(f"MAST's LLM judge, run twice on the same {retest['pairs']} traces\n"
                     f"Mean per-code κ = {retest['macro_kappa']:.2f}", x=0.01, ha="left", fontweight="bold", fontsize=11)
        fig.tight_layout()
        path = paths.FIGURES / "mast_judge_test_retest.png"
        fig.savefig(path, dpi=200)
        plt.close(fig)
        print(f"  wrote {path.relative_to(paths.ROOT)}")


# ---------------------------------------------------------------------------
# AFACS analysis (RQ2-RQ4)
# ---------------------------------------------------------------------------


RUN_LABELS = {"sonnet_bulk_r1": "AI pilot, Sonnet run 1", "opus_bulk_r1": "AI pilot, Opus",
              "sonnet_bulk_r2": "AI pilot, Sonnet run 2", "human_calibration": "human coding"}


def afacs_analysis(rows: dict[str, dict], name: str, weights: dict[str, float] | None = None,
                   extra: list[str] | None = None) -> None:
    """RQ2-RQ4 tables and figures. With `weights` (bulk run), shares are weighted to the eligible pool."""
    traces = {t["uid"]: t for t in load_traces()}
    codes = list(load_codebook_codes(CURRENT_CODEBOOK, trace_only=True))  # codebook order: L4 first, L1 last
    # Weights only make sense if every coded trace came from the bulk sample.
    weights = weights or {}
    weighted = bool(rows) and all(u in weights for u in rows)
    if weights and not weighted:
        print("  (some traces are not in the bulk sample, so shares are left unweighted)")
    if not weighted:
        weights = {}
    failed = {u: r for u, r in rows.items() if r["failure_observed"] == "yes"}
    by_fw = defaultdict(list)
    for u in failed:
        by_fw[traces[u]["framework"]].append(u)
    all_label = "All (weighted to eligible pool)" if weighted else "All"
    groups = [(all_label, sorted(failed))] + [(fw, us) for fw, us in sorted(by_fw.items())]

    def share(us, flag):
        return weighted_share(us, flag, weights)

    out = [f"# AFACS analysis: {name}", "",
           f"Coded traces: {len(rows)}. Failure observed in {len(failed)} "
           f"({pct(*wilson(len(failed), len(rows)))}). Shares below are of traces with a failure observed.", "",
           ("Shares are **weighted** so they represent the eligible pool, not the balanced sample "
            "(the sample over-represents small frameworks and models). n is the number of coded traces."
            if weighted else
            "Shares are **unweighted**: they describe these traces, which were chosen for balance, not to "
            "represent MAST as a whole."), ""]

    # RQ2 - layers and latent contributors
    out += ["## RQ2: where in the layers do failures sit?", "",
            "| Group | n | " + " | ".join(LAYER_NAMES[L] for L in LAYERS) + " | Any latent (L2–L4) |",
            "|---|---|" + "---|" * (len(LAYERS) + 1)]
    panels = {LAYER_NAMES[L]: [] for L in LAYERS}
    for label, us in groups:
        cells = []
        for L in LAYERS:
            p = share(us, lambda u, L=L: has_layer(failed[u], L))
            cells.append(pct(*p))
            panels[LAYER_NAMES[L]].append((label.split(" (")[0], *p, len(us)))
        latent = share(us, lambda u: any(has_layer(failed[u], L) for L in ("L2", "L3", "L4")))
        out.append(f"| {label} | {len(us)} | " + " | ".join(cells) + f" | {pct(*latent)} |")
    all_us = sorted(failed)
    out += ["", "Deepest contributing layer: " + ", ".join(
        f"{L} {pct(share(all_us, lambda u, L=L: failed[u]['deepest_layer'] == L)[0])}" for L in LAYERS), ""]
    if failed:
        hbar_panels(panels, f"Share of failed traces with a contributing factor at each layer ({RUN_LABELS.get(name, name)}; weighted, 95% intervals)",
                    paths.FIGURES / f"layers_by_framework_{name}.png")

    # RQ3 - violations
    out += ["## RQ3: errors vs violations", "",
            "| Group | n | Any violation code | Exceptional (V2) | Indeterminate (V?) | Evidence stated | Evidence inferred |",
            "|---|---|---|---|---|---|---|"]
    for label, us in groups:
        v = share(us, lambda u: any_violation(failed[u]))
        v2 = share(us, lambda u: "L1.V2" in codes_of(failed[u]))
        vq = share(us, lambda u: "L1.V?" in codes_of(failed[u]))
        st = share(us, lambda u: failed[u].get("violation_evidence") == "stated")
        inf = share(us, lambda u: failed[u].get("violation_evidence") == "inferred")
        out.append(f"| {label} | {len(us)} | {pct(*v)} | {pct(v2[0])} | {pct(vq[0])} | {pct(st[0])} | {pct(inf[0])} |")
    out += ["", "Evidence columns: share of failed traces whose violation rests on the agent's own words (stated) "
            "or only on the nature of the act (inferred); thin evidence is the V? column (codebook v1, section 2.1)."]
    # Model-level patterns. L4.4 (model development) is never coded from a trace
    # (codebook v1, section 1.1). Instead we look across many traces: with the
    # framework and benchmark held fixed, does a pattern follow the model?
    out += ["", "### Model-level patterns (framework and benchmark held fixed)", "",
            "AFACS does not code model development (L4.4) from traces. Here the framework and benchmark are held fixed "
            "and only the model varies; a difference that follows the model suggests, but does not establish, a "
            "model-level contribution. Exploratory: the groups are small.", "",
            "| Framework (benchmark) | Model | n | Any violation code | Evidence stated | L1 errors only |", "|---|---|---|---|---|---|"]
    for fw in ("MetaGPT", "AG2"):
        by_model = defaultdict(list)
        for u in by_fw.get(fw, []):
            by_model[(traces[u]["model"], traces[u]["benchmark"])].append(u)
        for (model, bench), us in sorted(by_model.items()):
            v = share(us, lambda u: any_violation(failed[u]))
            st = share(us, lambda u: failed[u].get("violation_evidence") == "stated")
            err = share(us, lambda u: bool(split_codes(failed[u].get("l1_codes"))) and not any_violation(failed[u]))
            out.append(f"| {fw} ({bench}) | {model} | {len(us)} | {pct(*v)} | {pct(st[0])} | {pct(err[0])} |")
    fm11 = [u for u in failed if traces[u]["mast_labels"].get("1.1") == 1]
    if fm11:
        v = share(fm11, lambda u: any_violation(failed[u]))
        out += ["", f"Traces MAST labels **FM-1.1 Disobey Task Specification** (n={len(fm11)}): "
                f"{pct(*v)} carry an AFACS violation code; the rest are coded as errors only. "
                "If both groups are substantial, FM-1.1 mixes capability failures and departures from known requirements.", ""]

    # RQ1, observed: how the two ways of typing an error line up in practice.
    # Pairs (error code, function) come from the annotator's `error_functions`; a coder who
    # gave functions only per trace (e.g. a human sheet) contributes trace-level pairs instead.
    errs = [u for u in failed if any(c in codes_of(failed[u]) for c in ("L1.E1", "L1.E2", "L1.E3"))]
    if errs:
        def pairs(u):
            given = [p.split(":", 1) for p in split_labels(failed[u].get("error_functions")) if ":" in p]
            if given:
                return {(c.upper(), f) for c, f in given}
            return {(c, f) for c in codes_of(failed[u]) if c.startswith("L1.E")
                    for f in split_labels(failed[u].get("ezell_functions"))}
        out += ["## RQ1 (observed): HFACS error types × Ezell et al.'s cognitive functions", "",
                f"Traces with an L1 error: {len(errs)}. Cells: number of traces in which that error type was "
                "assigned that cognitive function (one error can involve several functions). The cross-walk "
                "predicts E3 with observation and understanding, E2 with decision, and E1 with action.", "",
                "| HFACS error | " + " | ".join(EZELL_FUNCTIONS) + " | none given |", "|---|" + "---|" * (len(EZELL_FUNCTIONS) + 1)]
        for code in ("L1.E1", "L1.E2", "L1.E3"):
            us = [u for u in errs if code in codes_of(failed[u])]
            cells = [sum((code, f) in pairs(u) for u in us) for f in EZELL_FUNCTIONS]
            none = sum(not any(c == code for c, _ in pairs(u)) for u in us)
            out.append(f"| {code} (n={len(us)}) | " + " | ".join(map(str, cells)) + f" | {none} |")
        out += [""]

    # RQ4 - cross-walk
    out += ["## RQ4: MAST × AFACS cross-walk", "",
            "Each row: traces carrying that MAST label. Cells: share with an AFACS code at that layer, and with any violation code.", "",
            "| MAST label | n | " + " | ".join(LAYERS) + " | Violation |", "|---|---|" + "---|" * (len(LAYERS) + 1)]
    layer_matrix, code_matrix, row_labels, row_n = [], [], [], []
    for c in design.MAST_CODES:
        us = [u for u in failed if traces[u]["mast_labels"].get(c) == 1]
        if not us:
            continue
        lrow = [share(us, lambda u, L=L: has_layer(failed[u], L))[0] for L in LAYERS]
        vio = share(us, lambda u: any_violation(failed[u]))[0]
        layer_matrix.append(lrow + [vio])
        code_matrix.append([share(us, lambda u, code=code: code in codes_of(failed[u]))[0] for code in codes])
        row_labels.append(c)
        row_n.append(len(us))
        out.append(f"| {c} {design.MAST_NAMES[c]} | {len(us)} | " + " | ".join(f"{x:.0%}" for x in lrow) + f" | {vio:.0%} |")
    if layer_matrix:
        notes = [f"{design.MAST_NAMES[c]} (n={n})" for c, n in zip(row_labels, row_n)]
        heatmap(layer_matrix, row_labels, LAYERS + ["Violation"], f"AFACS layers within each MAST label ({RUN_LABELS.get(name, name)})",
                paths.FIGURES / f"crosswalk_layers_{name}.png", row_note=notes)
        heatmap(code_matrix, row_labels, codes, f"AFACS codes within each MAST label ({RUN_LABELS.get(name, name)})",
                paths.FIGURES / f"crosswalk_codes_{name}.png", row_note=notes)

    out += extra or []
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"analysis_{name}.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"\n(saved to results/analysis_{name}.md)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("mast")
    p = sub.add_parser("afacs")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", help="annotator run name")
    g.add_argument("--human", action="store_true", help="use James's calibration coding sheet")
    args = ap.parse_args()

    if args.command == "mast":
        mast_figures()
    elif args.human:
        afacs_analysis(usable(load_human(), "human"), "human_calibration")
    else:
        from afacs.annotate import check_quotes  # the AI's evidence quotes, checked against the traces

        traces = {t["uid"]: t for t in load_traces()}
        quote_lines = report_lines(check_quotes(args.run, traces, verbose=False))
        afacs_analysis(usable(load_llm(args.run), args.run), args.run, weights=load_bulk_weights(), extra=quote_lines)


if __name__ == "__main__":
    main()
