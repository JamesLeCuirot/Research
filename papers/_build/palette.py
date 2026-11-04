"""Shared figure style for the papers: Okabe–Ito colours with one fixed colour per model,
serif (Latin Modern) text, vector PDF output. Import from figure scripts:

    import sys; sys.path.insert(0, "papers/_build"); from palette import MODEL, apply_style
"""
import matplotlib as mpl

MODEL = {  # one colour per model, used in every figure of every paper
    "claude-haiku-5-5": "#E69F00",   # orange
    "claude-sonnet-5-5": "#0072B2",  # blue
    "claude-opus-5-5": "#009E73",    # green
}
NEUTRAL = "#555555"
EXTRA = ["#D55E00", "#CC79A7", "#56B4E9", "#F0E442"]  # for non-model series

def apply_style():
    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Latin Modern Roman", "LM Roman 10", "CMU Serif", "DejaVu Serif"],
        "mathtext.fontset": "cm",
        "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "legend.fontsize": 8,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
        "savefig.bbox": "tight", "savefig.dpi": 300, "pdf.fonttype": 42,
        "figure.figsize": (5.5, 3.2),
    })
