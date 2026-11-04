"""Redraw the paper's five figures in the shared report style (vector PDF, one colour per model).

Same data, measures and error bars as the registered figures drawn by `analyse.py` (function
`figures`); only the styling and the panel layout differ. Each panel is written as its own PDF and
set as a subfigure (a)/(b) in `paper.tex`. Reads only:
- results/analysis.json   hit and false-alarm rates with Wilson 95% CIs ("descriptive"),
                          d' and c with 95% bootstrap CIs ("bootstrap_ci")
- results/judgments.csv   one row per judgement (position of the backdoored item, for Figure 5)
Writes figures/report/fig_*.pdf. Does not touch analyse.py, results/ or the PNG figures.

Run from the repository root:
  uv run --no-project --with matplotlib python papers/02-do-llm-monitors-miss-rare-threats/code/figures_report.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # the paper folder
sys.path.insert(0, "papers/_build")                 # house style (run from the repository root)
sys.path.insert(0, str(ROOT.parent / "_build"))     # same folder, independent of the working directory
from palette import MODEL, apply_style              # noqa: E402

import matplotlib                                   # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
from matplotlib import font_manager                 # noqa: E402


def register_latin_modern() -> None:
    """Make Latin Modern Roman (the text face of the paper) available to Matplotlib.

    The installed Latin Modern fonts are OpenType with CFF outlines, which Matplotlib cannot embed
    cleanly as Type 42 (`pdf.fonttype` 42 in palette.py). Each face is converted to a TrueType copy in
    a temporary folder (quadratic outlines via fontTools' cu2qu, as in fontTools' otf2ttf snippet) and
    registered. If the fonts or fontTools are missing, palette.py's fallback serif (DejaVu Serif) is used.
    """
    import atexit
    import shutil
    import tempfile
    try:
        from fontTools.pens.cu2quPen import Cu2QuPen
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        from fontTools.ttLib import TTFont, newTable
    except ImportError:
        return
    srcs = [p for p in font_manager.findSystemFonts() if Path(p).name.startswith("lmroman10-")]
    if not srcs:
        return
    tmp = Path(tempfile.mkdtemp(prefix="lm-ttf-"))
    atexit.register(shutil.rmtree, tmp, True)
    for src in srcs:
        font = TTFont(src)
        if "CFF " not in font:
            font_manager.fontManager.addfont(src)
            continue
        order = font.getGlyphOrder()
        gs = font.getGlyphSet()
        glyf = newTable("glyf")
        glyf.glyphOrder, glyf.glyphs = order, {}
        for name in order:
            pen = TTGlyphPen(gs)
            gs[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
            glyf.glyphs[name] = pen.glyph()
        font["loca"], font["glyf"] = newTable("loca"), glyf
        del font["CFF "]
        if "VORG" in font:
            del font["VORG"]
        font.sfntVersion = "\000\001\000\000"
        post = font["post"]
        post.formatType, post.extraNames, post.mapping, post.glyphOrder = 2.0, [], {}, order
        maxp = font["maxp"]
        maxp.tableVersion = 0x00010000
        for f in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs",
                  "maxStackElements", "maxSizeOfInstructions", "maxComponentElements"):
            setattr(maxp, f, 1 if f == "maxZones" else 0)
        for g in glyf.glyphs.values():
            g.recalcBounds(glyf)
        dst = tmp / (Path(src).stem + ".ttf")
        font.save(dst)
        font_manager.fontManager.addfont(str(dst))

RESULTS = ROOT / "results"
OUT = ROOT / "figures" / "report"
MONS = {"Haiku": "claude-haiku-5-5", "Sonnet": "claude-sonnet-5-5"}
EXP1 = ["P50", "P10", "P2.5"]
EXP2 = ["none", "S50", "S1"]
EXP3 = ["R-cal", "R-ind"]
PANEL = (2.95, 2.45)    # one model panel; set at half the text width
WIDE = (5.9, 2.35)      # full-width panel (Figure 2)
META = {"CreationDate": None, "Creator": None, "Producer": None}  # byte-stable output


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    """Wilson score interval, identical to analyse.wilson."""
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def errs(ys, cis):
    return [[y - c[0] for y, c in zip(ys, cis)], [c[1] - y for y, c in zip(ys, cis)]]


def save(fig, name: str) -> None:
    fig.savefig(OUT / name, metadata=META)
    plt.close(fig)


def rate_panel(desc, mon, conds, ticklabels, xlabel, ylabel, name, joined=True, legend=True):
    """Hit rate (filled, solid) and false-alarm rate (open, dashed) for one monitor, Wilson 95% CIs."""
    col = MODEL[MONS[mon]]
    fig, ax = plt.subplots(figsize=PANEL)
    x = list(range(len(conds)))
    for meas, ls, mfc, mk, lab in [("H", "-", col, "o", "Hit rate"), ("F", "--", "white", "s", "False-alarm rate")]:
        ys = [desc[f"{mon}|{c}"][meas] for c in conds]
        cis = [desc[f"{mon}|{c}"][meas + "_ci"] for c in conds]
        ax.errorbar(x, ys, yerr=errs(ys, cis), color=col, ls=ls if joined else "none", marker=mk, mfc=mfc,
                    mec=col, ms=5, lw=1.2, capsize=2.5, label=lab)
    ax.set_xticks(x, ticklabels)
    ax.set_xlim(-0.35, len(conds) - 0.65)
    ax.set_ylim(-0.02, 1.02)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if legend:
        ax.legend(loc="lower left", bbox_to_anchor=(0.0, 0.1), frameon=False)
    save(fig, name)


def main() -> None:
    register_latin_modern()
    apply_style()
    OUT.mkdir(parents=True, exist_ok=True)
    A = json.loads((RESULTS / "analysis.json").read_text(encoding="utf-8"))
    desc, boot = A["descriptive"], A["bootstrap_ci"]

    # Figure 1 (fig_a): hit and false-alarm rate by prevalence, Experiment 1.
    for i, mon in enumerate(MONS):
        rate_panel(desc, mon, EXP1, ["50%", "10%", "2.5%"], "Backdoor prevalence in batch", "Proportion flagged",
                   f"fig_a_prevalence_{mon.lower()}.pdf", legend=(i == 0))

    # Figure 2 (fig_b): d' and c for every condition and monitor, 95% bootstrap CIs.
    conds = EXP1 + EXP3 + EXP2
    labels = ["P50", "P10", "P2.5", "R-cal", "R-ind", "single:\nnone", "single:\nS50", "single:\nS1"]
    off = {"Haiku": -0.1, "Sonnet": 0.1}
    mk = {"Haiku": "o", "Sonnet": "s"}
    for stat, ylab, name in [("d_prime", "Sensitivity $d'$", "fig_b_sdt_dprime.pdf"),
                             ("c", "Criterion $c$\n(higher = more conservative)", "fig_b_sdt_c.pdf")]:
        fig, ax = plt.subplots(figsize=WIDE)
        for mon in MONS:
            col = MODEL[MONS[mon]]
            xs, ys, lo, hi = [], [], [], []
            for i, c in enumerate(conds):
                v = desc[f"{mon}|{c}"][stat]
                b = boot[f"{mon}|{c}"][stat]
                xs.append(i + off[mon]); ys.append(v); lo.append(v - b[0]); hi.append(b[1] - v)
            ax.errorbar(xs, ys, yerr=[lo, hi], ls="none", marker=mk[mon], color=col, mfc=col, mec=col,
                        ms=5, capsize=2.5, lw=1.1, label=mon)
        for xv in (2.5, 4.5):
            ax.axvline(xv, color="0.7", lw=0.7, ls=":")
        if stat == "c":
            ax.axhline(0, color="0.55", lw=0.7)
        ax.set_xticks(range(len(conds)), labels)
        ax.set_ylabel(ylab)
        if stat == "d_prime":
            ax.legend(loc="upper left", frameon=False)
        save(fig, name)

    # Figure 3 (fig_d): stated prevalence, single items, Experiment 2.
    for i, mon in enumerate(MONS):
        rate_panel(desc, mon, ["S50", "none", "S1"],
                   ["S50\n(“about half”)", "none\n(no statement)", "S1\n(“about 1 in 100”)"],
                   None, "Proportion flagged (single items)", f"fig_d_stated_prevalence_{mon.lower()}.pdf",
                   legend=(i == 0))

    # Figure 4 (fig_e): remedies at 2.5% prevalence, Experiment 3 (points not joined, as in analyse.py).
    for i, mon in enumerate(MONS):
        rate_panel(desc, mon, ["P2.5", "R-cal", "R-ind"],
                   ["P2.5\n(no remedy)", "R-cal\n(labelled\nexamples)", "R-ind\n(independence\ninstruction)"],
                   None, "Proportion flagged (2.5% prevalence)", f"fig_e_remedies_{mon.lower()}.pdf",
                   joined=False, legend=(i == 0))

    # Figure 5 (fig_c): hit rate by position of the backdoored item, bins of eight, Wilson 95% CIs.
    with open(RESULTS / "judgments.csv", newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["backdoored"] == "1" and r["condition"] in ("P10", "P2.5")]
    bins = [(1, 8), (9, 16), (17, 24), (25, 32), (33, 40)]
    for mon in MONS:
        col = MODEL[MONS[mon]]
        fig, ax = plt.subplots(figsize=PANEL)
        for cond, ls, m, mfc, dx in [("P10", "--", "s", "white", -0.06), ("P2.5", "-", "o", col, 0.06)]:
            d = [r for r in rows if r["monitor"] == mon and r["condition"] == cond]
            xs, ys, lo, hi = [], [], [], []
            for k, (a, b) in enumerate(bins):
                dd = [r for r in d if a <= int(r["position"]) <= b]
                if not dd:
                    continue
                h, n = sum(int(r["flag"]) for r in dd), len(dd)
                w = wilson(h, n)
                xs.append(k + dx); ys.append(h / n); lo.append(h / n - w[0]); hi.append(w[1] - h / n)
            ax.errorbar(xs, ys, yerr=[lo, hi], ls=ls, marker=m, mfc=mfc, mec=col, color=col, ms=5, capsize=2.5,
                        lw=1.1, label=f"{cond} (n = {len(d)})")
        ax.set_xticks(range(len(bins)), [f"{a}–{b}" for a, b in bins])
        ax.set_xlabel("Position of backdoored item in batch")
        ax.set_ylabel("Hit rate")
        ax.set_ylim(-0.02, 1.02)
        ax.legend(loc="lower left", frameon=False)
        save(fig, f"fig_c_position_{mon.lower()}.pdf")


if __name__ == "__main__":
    main()
