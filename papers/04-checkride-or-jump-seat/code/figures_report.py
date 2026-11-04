"""Figure 1 for the LaTeX report, in the shared house style (vector PDF).

Run from the repository root:
    uv run --no-project --with krippendorff==0.9.0 --with numpy --with scipy --with pandas --with matplotlib \
        python papers/04-checkride-or-jump-seat/code/figures_report.py

Redraws figures/fig1_agreement.png (made by code/analyse.py) with the shared palette and serif text.
Same data and intervals: panel A reads the alphas and 95% bootstrap CIs from results/agreement_grades.csv;
panel B uses the per-transcript means that analyse.py plots, computed by its own functions from
data/grades.jsonl (no results file holds them), and checks them against results/means_by_scenario_model.csv
and results/known_groups_controls.csv. Nothing in results/ or figures/fig1_agreement.png is changed.
Output: figures/report/fig1_agreement.pdf.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
sys.path.insert(0, "papers/_build")
sys.path.insert(0, str(PAPER.parent / "_build"))  # same folder, when run from elsewhere
sys.path.insert(0, str(HERE))
from palette import EXTRA, MODEL, NEUTRAL, apply_style  # noqa: E402

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from analyse import LABEL, load, per_transcript_means  # noqa: E402  (analysis code, unchanged)

RESULTS = PAPER / "results"
OUT = PAPER / "figures" / "report" / "fig1_agreement.pdf"
ORDER = ["PRO", "COM", "PSD", "SAW", "MEAN4", "OVERALL_R", "HOLISTIC"]
SONNET, OPUS, HAIKU = MODEL["claude-sonnet-5-5"], MODEL["claude-opus-5-5"], MODEL["claude-haiku-5-5"]
INTER = EXTRA[1]  # inter-grader agreement involves both graders, so it takes a non-model colour


def panel_b_data():
    """Per-transcript mean of the four competency grades, exactly as analyse.py computes it for the figure."""
    long, _ = load()
    model_tids = sorted(long[long.agent != "scripted-control"].tid.unique())
    ctrl_tids = sorted(long[long.agent == "scripted-control"].tid.unique())
    pt_all = per_transcript_means(long[(long.run == 1) | (long.agent != "scripted-control")], model_tids + ctrl_tids)
    # Cross-checks against the published results files.
    cells = pd.read_csv(RESULTS / "means_by_scenario_model.csv", header=[0, 1], index_col=[0, 1])
    mine = pt_all[pt_all.agent != "scripted-control"].groupby(["scenario", "agent"])["MEAN4"].mean().round(2)
    for (s, a), v in mine.items():
        assert abs(cells.loc[(s, a), ("MEAN4", "mean")] - v) < 0.006, (s, a, v)
    kg = pd.read_csv(RESULTS / "known_groups_controls.csv")
    kg = kg[kg.measure == "MEAN4"].set_index("scenario")["control_mean_run1"]
    ctrl = pt_all[pt_all.agent == "scripted-control"].groupby("scenario")["MEAN4"].mean()
    for s, v in ctrl.items():
        assert abs(kg[s] - v) < 0.006, (s, v)
    return pt_all


def main():
    agr = pd.read_csv(RESULTS / "agreement_grades.csv")
    model = agr[agr.set == "48 model transcripts"]
    ctrl = agr[(agr.set == "48 model + 6 controls") & (agr.comparison == "Inter-grader (run 1)")]
    pt_all = panel_b_data()

    apply_style()
    plt.rcParams.update({"axes.grid": False})
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.0, 7.6), gridspec_kw={"height_ratios": [1.9, 1], "hspace": 0.56})

    # Panel A: alpha with 95% bootstrap CI, by measure and comparison.
    series = [  # comparison, colour, marker, filled, vertical offset
        ("Inter-grader (run 1)", INTER, "o", True, 0.27),
        ("Inter-grader (run 2)", INTER, "s", False, 0.09),
        ("Repeat-run (Sonnet grader)", SONNET, "o", True, -0.09),
        ("Repeat-run (Opus grader)", OPUS, "o", True, -0.27),
    ]
    y = np.arange(len(ORDER))[::-1]
    for comp, col, mk, filled, off in series:
        d = model[model.comparison == comp].set_index("measure").reindex(ORDER)
        ax1.errorbar(d["alpha"], y + off, xerr=[d["alpha"] - d["ci_low"], d["ci_high"] - d["alpha"]], fmt=mk, ms=3.6,
                     color=col, mfc=col if filled else "white", mec=col, mew=0.9, ecolor=col, elinewidth=1.0,
                     capsize=0, label=comp)
    dc = ctrl.set_index("measure").reindex(ORDER)
    ax1.scatter(dc["alpha"], y + 0.27, marker="D", s=16, facecolor="white", edgecolor=NEUTRAL, linewidth=0.9, zorder=3,
                label="Inter-grader (run 1) + 6 post hoc controls (exploratory)")
    ax1.axvline(0, color=NEUTRAL, lw=0.6)
    for x, lab, ha in ((0.667, ".667 ", "right"), (0.8, " .800", "left")):
        ax1.axvline(x, color=NEUTRAL, lw=0.6, ls=":")
        ax1.text(x, len(ORDER) - 0.45, lab, color=NEUTRAL, fontsize=7, ha=ha, va="bottom")
    ax1.set_yticks(y, [LABEL[m] for m in ORDER])
    ax1.set_ylim(-0.6, len(ORDER) - 0.4)
    ax1.set_xlim(-0.15, 1.05)
    ax1.set_xlabel("Krippendorff's alpha (95% bootstrap CI)")
    ax1.set_title("A. Agreement by measure", loc="left", fontweight="bold")
    ax1.grid(axis="x", alpha=0.25, lw=0.5)
    ax1.set_axisbelow(True)

    # Panel B: mean of the four competency grades per transcript, by scenario and agent; controls as diamonds.
    scen = sorted(pt_all.scenario.unique())
    agents = (("claude-haiku-5-5", -0.15, HAIKU, "Haiku 5.5 agent responses"),
              ("claude-sonnet-5-5", 0.15, SONNET, "Sonnet 5.5 agent responses"))
    for k, s in enumerate(scen):
        for agent, off, col, name in agents:
            v = pt_all[(pt_all.scenario == s) & (pt_all.agent == agent)]["MEAN4"].to_numpy()
            ax2.scatter(k + off + np.linspace(-0.06, 0.06, len(v)), v, s=11, color=col, edgecolor="white",
                        linewidth=0.4, zorder=3, label=name if k == 0 else None)
        v = pt_all[(pt_all.scenario == s) & (pt_all.agent == "scripted-control")]["MEAN4"].to_numpy()
        ax2.scatter([k] * len(v), v, marker="D", s=18, facecolor="white", edgecolor="black", linewidth=0.9, zorder=3,
                    label="Post hoc scripted control (run 1, exploratory)" if k == 0 else None)
    ax2.set_xticks(range(len(scen)), [s.split("_", 1)[0] for s in scen])
    ax2.set_ylim(0.8, 5.2)
    ax2.set_ylabel("Mean competency grade (1–5)")
    ax2.set_xlabel("Scenario")
    ax2.set_title("B. Grades by scenario and source", loc="left", fontweight="bold")
    ax2.grid(axis="y", alpha=0.25, lw=0.5)
    ax2.set_axisbelow(True)

    # Legends: panel A's under it (inter-grader entries left, repeat-run entries right); panel B's in its empty band.
    h1, l1 = ax1.get_legend_handles_labels()
    lab = {l: h for h, l in zip(h1, l1)}
    order = ["Inter-grader (run 1)", "Inter-grader (run 2)", "Inter-grader (run 1) + 6 post hoc controls (exploratory)",
             "Repeat-run (Sonnet grader)", "Repeat-run (Opus grader)"]
    ax1.legend([lab[o] for o in order], order, loc="upper center", bbox_to_anchor=(0.42, -0.14),
               ncol=2, frameon=False, handletextpad=0.4, columnspacing=1.5, borderaxespad=0)
    ax2.legend(loc="center", bbox_to_anchor=(0.5, (2.75 - 0.8) / 4.4), ncol=1, frameon=False, handletextpad=0.4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
