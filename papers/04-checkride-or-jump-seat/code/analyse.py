"""Step 3: agreement and discrimination analysis, tables and figure.

Run from the repository root:
    uv run --no-project --with krippendorff --with numpy --with scipy --with pandas --with matplotlib \
        python papers/04-checkride-or-jump-seat/code/analyse.py

Outputs go to results/ (CSV and JSON) and figures/ (PNG). Everything is
recomputed from data/grades.jsonl, data/transcripts.jsonl and
data/control_transcripts.jsonl.
"""

import json
from itertools import combinations

import krippendorff
import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, FIGURES, RESULTS
from rubric import ALL_INDICATORS, COMPETENCIES

RNG = np.random.default_rng(20261103)
N_BOOT = 2000
COMP = [c["code"] for c in COMPETENCIES]
GRADERS = {"claude-sonnet-5-5": "Sonnet", "claude-opus-5-5": "Opus"}
MEASURES = COMP + ["MEAN4", "OVERALL_R", "HOLISTIC"]
LEVEL = {m: "ordinal" for m in MEASURES} | {"MEAN4": "interval"}
LABEL = {"PRO": "PRO (procedures, scope)", "COM": "COM (communication)", "PSD": "PSD (problem solving)",
         "SAW": "SAW (situation awareness)", "MEAN4": "Mean of 4 competencies",
         "OVERALL_R": "Overall, after rubric", "HOLISTIC": "Holistic only"}


# ---------------------------------------------------------------- loading
def load():
    grades = [json.loads(l) for l in open(DATA / "grades.jsonl")]
    grades = [g for g in grades if not g.get("error")]
    rows, ind_rows = [], []
    for g in grades:
        key = dict(tid=g["transcript_id"], scenario=g["scenario"], agent=g["agent_model"], grader=GRADERS[g["grader"]],
                   run=g["run"])
        s = g["grades"]
        if g["condition"] == "rubric":
            vals = {c: s[c]["grade"] for c in COMP}
            vals["MEAN4"] = float(np.mean([s[c]["grade"] for c in COMP]))
            vals["OVERALL_R"] = s["overall"]
            for c in COMP:
                for ind, status in s[c]["indicators"].items():
                    ind_rows.append({**key, "indicator": ind, "status": status})
        else:
            vals = {"HOLISTIC": s["overall"]}
        for m, v in vals.items():
            rows.append({**key, "measure": m, "value": v})
    long = pd.DataFrame(rows).drop_duplicates(["tid", "grader", "run", "measure"], keep="last")
    ind = pd.DataFrame(ind_rows).drop_duplicates(["tid", "grader", "run", "indicator"], keep="last")
    return long, ind


def wide(long, measure, raters, tids):
    """Units (transcripts) x raters matrix for one measure; raters are (grader, run) pairs."""
    d = long[long.measure == measure]
    cols = {}
    for gr, run in raters:
        s = d[(d.grader == gr) & (d.run == run)].set_index("tid")["value"]
        cols[f"{gr}-r{run}"] = s.reindex(tids)
    return pd.DataFrame(cols)


# ---------------------------------------------------------------- agreement statistics
def k_alpha(mat: np.ndarray, level: str, domain=None) -> float:
    """Krippendorff's alpha; mat is units x raters (NaN = missing)."""
    data = mat.T.astype(float)
    if np.nanvar(data) == 0:
        return float("nan")
    kw = {"level_of_measurement": level}
    if level == "ordinal":
        kw["value_domain"] = domain if domain is not None else [1, 2, 3, 4, 5]
    elif level == "nominal" and domain is not None:
        kw["value_domain"] = domain
    try:
        return float(krippendorff.alpha(reliability_data=data, **kw))
    except ValueError:
        return float("nan")


def boot_ci(mat: np.ndarray, level: str, domain=None):
    n = mat.shape[0]
    vals = []
    for _ in range(N_BOOT):
        idx = RNG.integers(0, n, n)
        a = k_alpha(mat[idx], level, domain)
        if not np.isnan(a):
            vals.append(a)
    if len(vals) < N_BOOT * 0.5:
        return float("nan"), float("nan")
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def pct_agree(mat: np.ndarray, tol: float = 0.0) -> float:
    """Pairwise exact (or within-tol) agreement, averaged over rater pairs."""
    res = []
    for i, j in combinations(range(mat.shape[1]), 2):
        ok = ~np.isnan(mat[:, i]) & ~np.isnan(mat[:, j])
        res.append(np.mean(np.abs(mat[ok, i] - mat[ok, j]) <= tol + 1e-9))
    return float(np.mean(res))


COMPARISONS = {
    "Inter-grader (run 1)": [("Sonnet", 1), ("Opus", 1)],
    "Inter-grader (run 2)": [("Sonnet", 2), ("Opus", 2)],
    # "Repeat-run" agreement: the same grader model sampled twice, independently, with the same prompt.
    # It measures sampling consistency, not stability over time (there is no interval and no memory).
    "Repeat-run (Sonnet grader)": [("Sonnet", 1), ("Sonnet", 2)],
    "Repeat-run (Opus grader)": [("Opus", 1), ("Opus", 2)],
    "All four ratings": [("Sonnet", 1), ("Sonnet", 2), ("Opus", 1), ("Opus", 2)],
}


def agreement_table(long, tids, comparisons, label):
    out = []
    for comp_name, raters in comparisons.items():
        for m in MEASURES:
            mat = wide(long, m, raters, tids).to_numpy(dtype=float)
            if np.isnan(mat).all():
                continue
            a = k_alpha(mat, LEVEL[m])
            lo, hi = boot_ci(mat, LEVEL[m])
            out.append({"set": label, "comparison": comp_name, "measure": m, "level": LEVEL[m], "n_units": len(tids),
                        "alpha": a, "ci_low": lo, "ci_high": hi,
                        "exact_agreement": pct_agree(mat, 0) if m != "MEAN4" else np.nan,
                        "within_1_agreement": pct_agree(mat, 1)})
    return pd.DataFrame(out)


def indicator_agreement(ind, tids, comparisons):
    code = {"demonstrated": 0, "not_demonstrated": 1, "not_required": 2}
    out = []
    for comp_name, raters in comparisons.items():
        if comp_name == "All four ratings":
            continue
        mats = {}
        for indicator in ALL_INDICATORS:
            d = ind[ind.indicator == indicator]
            cols = []
            for gr, run in raters:
                s = d[(d.grader == gr) & (d.run == run)].set_index("tid")["status"].map(code)
                cols.append(s.reindex(tids))
            mats[indicator] = pd.concat(cols, axis=1).to_numpy(dtype=float)
        for indicator, mat in mats.items():
            out.append({"comparison": comp_name, "indicator": indicator,
                        "alpha_nominal": k_alpha(mat, "nominal", [0, 1, 2]),
                        "exact_agreement": pct_agree(mat),
                        "pct_demonstrated": float(np.nanmean(mat == 0)),
                        "pct_not_demonstrated": float(np.nanmean(mat == 1)),
                        "pct_not_required": float(np.nanmean(mat == 2))})
        pooled = np.vstack(list(mats.values()))
        binary = np.where(np.isnan(pooled), np.nan, (pooled == 0).astype(float))
        out.append({"comparison": comp_name, "indicator": "ALL (pooled, 3 categories)",
                    "alpha_nominal": k_alpha(pooled, "nominal", [0, 1, 2]), "exact_agreement": pct_agree(pooled),
                    "pct_demonstrated": float(np.nanmean(pooled == 0)),
                    "pct_not_demonstrated": float(np.nanmean(pooled == 1)),
                    "pct_not_required": float(np.nanmean(pooled == 2))})
        out.append({"comparison": comp_name, "indicator": "ALL (pooled, demonstrated vs other)",
                    "alpha_nominal": k_alpha(binary, "nominal", [0, 1]), "exact_agreement": pct_agree(binary),
                    "pct_demonstrated": float(np.nanmean(binary == 1)), "pct_not_demonstrated": np.nan,
                    "pct_not_required": np.nan})
    return pd.DataFrame(out)


# ---------------------------------------------------------------- discrimination
def per_transcript_means(long, tids):
    d = long[long.tid.isin(tids)]
    return d.groupby(["tid", "scenario", "agent", "measure"])["value"].mean().unstack("measure").reset_index()


def stratified_permutation(pt, m, n_perm=10000):
    """Haiku minus Sonnet mean difference, with model labels permuted within scenario."""
    rng = np.random.default_rng(20261103)
    def diff(d):
        return d[d.agent == "claude-haiku-5-5"][m].mean() - d[d.agent == "claude-sonnet-5-5"][m].mean()
    obs = diff(pt)
    groups = [g for _, g in pt.groupby("scenario")]
    count = 0
    for _ in range(n_perm):
        shuffled = pd.concat([g.assign(agent=rng.permutation(g.agent.to_numpy())) for g in groups])
        count += abs(diff(shuffled)) >= abs(obs) - 1e-12
    return obs, (count + 1) / (n_perm + 1)


def discrimination(pt):
    out = []
    for m in MEASURES:
        groups = [g[m].to_numpy() for _, g in pt.groupby("scenario")]
        h, p = stats.kruskal(*groups) if pt[m].nunique() > 1 else (np.nan, np.nan)
        k, n = len(groups), len(pt)
        # Effect sizes for Kruskal-Wallis: epsilon-squared = H / (n - 1); eta-squared based on H = (H - k + 1) / (n - k).
        eps2 = h / (n - 1) if not np.isnan(h) else np.nan
        eta2_h = (h - k + 1) / (n - k) if not np.isnan(h) else np.nan
        hk = pt[pt.agent == "claude-haiku-5-5"][m].to_numpy()
        so = pt[pt.agent == "claude-sonnet-5-5"][m].to_numpy()
        u, pu = stats.mannwhitneyu(hk, so, alternative="two-sided") if pt[m].nunique() > 1 else (np.nan, np.nan)
        cliff = (np.sum(hk[:, None] > so[None, :]) - np.sum(hk[:, None] < so[None, :])) / (len(hk) * len(so))
        obs, p_perm = stratified_permutation(pt, m)
        # Pooled within-cell (scenario x model) SD and the difference detectable with 80% power (two-sided 5%).
        sd_within = float(np.sqrt(pt.groupby(["scenario", "agent"])[m].var(ddof=1).mean()))
        mdd = (stats.norm.ppf(0.975) + stats.norm.ppf(0.80)) * sd_within * np.sqrt(2 / len(hk))
        out.append({"measure": m, "kruskal_H_scenario": h, "kruskal_p": p, "epsilon_sq": eps2, "eta_sq_H": eta2_h,
                    "mean_haiku": hk.mean(), "mean_sonnet": so.mean(), "mannwhitney_U": u, "mannwhitney_p": pu,
                    "cliffs_delta_haiku_vs_sonnet": cliff, "stratified_perm_diff": obs, "stratified_perm_p": p_perm,
                    "pooled_within_cell_sd": sd_within, "min_detectable_diff_80pct": mdd,
                    "sd_transcript_means": pt[m].std(ddof=1)})
    return pd.DataFrame(out)


def distribution(long, tids, label):
    d = long[long.tid.isin(tids) & (long.measure != "MEAN4")]
    t = d.groupby("measure")["value"].value_counts().unstack(fill_value=0).reindex(columns=[1, 2, 3, 4, 5], fill_value=0)
    t.insert(0, "set", label)
    return t.reset_index()


# ---------------------------------------------------------------- figure
def make_figure(agr, agr_ctrl, pt_all):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    surface, ink, ink2, grid = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
    # Same hue for the two inter-grader runs, told apart by marker shape (secondary encoding).
    series = {"Inter-grader (run 1)": ("#2a78d6", "o", True), "Inter-grader (run 2)": ("#2a78d6", "s", False),
              "Repeat-run (Sonnet grader)": ("#eb6834", "o", True), "Repeat-run (Opus grader)": ("#1baf7a", "o", True)}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": ink2, "axes.labelcolor": ink,
                         "xtick.color": ink2, "ytick.color": ink2, "text.color": ink})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.6), gridspec_kw={"width_ratios": [1.35, 1]})
    fig.patch.set_facecolor(surface)

    # Panel A: alpha with 95% CI, by measure and comparison
    order = ["PRO", "COM", "PSD", "SAW", "MEAN4", "OVERALL_R", "HOLISTIC"]
    y = np.arange(len(order))[::-1]
    offs = {"Inter-grader (run 1)": 0.27, "Inter-grader (run 2)": 0.09, "Repeat-run (Sonnet grader)": -0.09,
            "Repeat-run (Opus grader)": -0.27}
    for comp, (col, mk, filled) in series.items():
        d = agr[agr.comparison == comp].set_index("measure").reindex(order)
        ax1.errorbar(d["alpha"], y + offs[comp], xerr=[d["alpha"] - d["ci_low"], d["ci_high"] - d["alpha"]],
                     fmt=mk, ms=4.5, color=col, mfc=col if filled else surface, mec=col, ecolor=col, elinewidth=1.3,
                     capsize=0, label=comp)
    dc = agr_ctrl[agr_ctrl.comparison == "Inter-grader (run 1)"].set_index("measure").reindex(order)
    ax1.scatter(dc["alpha"], y + 0.27, marker="D", s=26, facecolor=surface, edgecolor=ink2, linewidth=1.2, zorder=3,
                label="Inter-grader (run 1) + 6 post hoc controls (exploratory)")
    ax1.axvline(0, color=ink2, lw=0.8)
    for x, lab in ((0.667, ".667"), (0.8, ".800")):
        ax1.axvline(x, color=ink2, lw=0.7, ls=":")
        ax1.text(x, len(order) - 0.45, lab, color=ink2, fontsize=7.5, ha="center", va="bottom")
    ax1.set_yticks(y, [LABEL[m] for m in order])
    ax1.set_xlim(-0.15, 1.05)
    ax1.set_xlabel("Krippendorff's alpha (95% bootstrap CI)")
    ax1.set_title("A. Agreement by measure", loc="left", fontsize=10, fontweight="bold")
    ax1.grid(axis="x", color=grid, lw=0.6)
    ax1.set_axisbelow(True)
    ax1.legend(loc="upper center", bbox_to_anchor=(0.40, -0.14), ncol=2, fontsize=7.4, frameon=False)
    for s in ("top", "right"):
        ax1.spines[s].set_visible(False)

    # Panel B: mean of 4 competencies per transcript, by scenario and agent (dots), controls as diamonds
    scen = sorted(pt_all.scenario.unique())
    short = {s: s.split("_", 1)[0] for s in scen}
    cols_b = {"claude-haiku-5-5": "#2a78d6", "claude-sonnet-5-5": "#eb6834"}
    names = {"claude-haiku-5-5": "Haiku 5.5 agent responses", "claude-sonnet-5-5": "Sonnet 5.5 agent responses"}
    for k, s in enumerate(scen):
        for agent, off in (("claude-haiku-5-5", -0.15), ("claude-sonnet-5-5", 0.15)):
            v = pt_all[(pt_all.scenario == s) & (pt_all.agent == agent)]["MEAN4"].to_numpy()
            jitter = np.linspace(-0.06, 0.06, len(v))
            ax2.scatter(k + off + jitter, v, s=22, color=cols_b[agent], alpha=0.9, edgecolor=surface, linewidth=0.8,
                        label=names[agent] if k == 0 else None, zorder=3)
        v = pt_all[(pt_all.scenario == s) & (pt_all.agent == "scripted-control")]["MEAN4"].to_numpy()
        ax2.scatter([k] * len(v), v, marker="D", s=34, facecolor=surface, edgecolor=ink, linewidth=1.3, zorder=3,
                    label="Post hoc scripted control (run 1, exploratory)" if k == 0 else None)
    ax2.set_xticks(range(len(scen)), [short[s] for s in scen])
    ax2.set_ylim(0.8, 5.2)
    ax2.set_ylabel("Mean competency grade (1-5)")
    ax2.set_xlabel("Scenario")
    ax2.set_title("B. Grades by scenario and source", loc="left", fontsize=10, fontweight="bold")
    ax2.grid(axis="y", color=grid, lw=0.6)
    ax2.set_axisbelow(True)
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=1, fontsize=7.4, frameon=False)
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)
    for ax in (ax1, ax2):
        ax.set_facecolor(surface)
    fig.tight_layout()
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(FIGURES / "fig1_agreement.png", dpi=200, facecolor=surface)
    print("wrote", FIGURES / "fig1_agreement.png")


# ---------------------------------------------------------------- main
def main():
    RESULTS.mkdir(exist_ok=True)
    long, ind = load()
    model_tids = sorted(long[long.agent != "scripted-control"].tid.unique())
    ctrl_tids = sorted(long[long.agent == "scripted-control"].tid.unique())
    print(f"{len(model_tids)} model transcripts, {len(ctrl_tids)} scripted controls; {len(long)} grade values")

    agr = agreement_table(long, model_tids, COMPARISONS, "48 model transcripts")
    run1 = {"Inter-grader (run 1)": COMPARISONS["Inter-grader (run 1)"]}
    agr_ctrl = agreement_table(long, model_tids + ctrl_tids, run1, "48 model + 6 controls") if ctrl_tids else pd.DataFrame()
    pd.concat([agr, agr_ctrl]).to_csv(RESULTS / "agreement_grades.csv", index=False, float_format="%.4f")

    ia = indicator_agreement(ind, model_tids, COMPARISONS)
    ia.to_csv(RESULTS / "agreement_indicators.csv", index=False, float_format="%.3f")
    if ctrl_tids:
        ia_c = indicator_agreement(ind, model_tids + ctrl_tids, run1)
        ia_c.to_csv(RESULTS / "agreement_indicators_with_controls.csv", index=False, float_format="%.3f")

    pt = per_transcript_means(long, model_tids)
    disc = discrimination(pt)
    disc.to_csv(RESULTS / "discrimination.csv", index=False, float_format="%.4f")
    cell = pt.groupby(["scenario", "agent"])[MEASURES].agg(["mean", "std"]).round(2)
    cell.to_csv(RESULTS / "means_by_scenario_model.csv")

    dist = pd.concat([distribution(long, model_tids, "48 model transcripts (all 4 ratings)")] +
                     ([distribution(long, ctrl_tids, "6 scripted controls (run 1)")] if ctrl_tids else []))
    dist.to_csv(RESULTS / "grade_distribution.csv", index=False)

    # Systematic grader differences: per-transcript mean of each grader's two runs, paired by transcript
    gb = []
    d = long[long.tid.isin(model_tids)].groupby(["tid", "grader", "measure"])["value"].mean().unstack("grader")
    for m in MEASURES:
        x = d.xs(m, level="measure")
        diff = (x["Opus"] - x["Sonnet"]).to_numpy()
        w = stats.wilcoxon(x["Opus"], x["Sonnet"]) if np.any(diff != 0) else None
        gb.append({"measure": m, "mean_sonnet": x["Sonnet"].mean(), "mean_opus": x["Opus"].mean(),
                   "mean_diff_opus_minus_sonnet": diff.mean(), "pct_transcripts_opus_lower": float(np.mean(diff < 0)),
                   "pct_transcripts_opus_higher": float(np.mean(diff > 0)),
                   "wilcoxon_p": w.pvalue if w else np.nan})
    gb = pd.DataFrame(gb)
    gb["bonferroni_p"] = np.minimum(gb["wilcoxon_p"] * len(gb), 1.0)
    gb.to_csv(RESULTS / "grader_bias.csv", index=False, float_format="%.3f")
    print(gb.round(3).to_string(index=False))

    # Holistic-only vs competency grades (per-transcript means over the 4 ratings)
    rho, p = stats.spearmanr(pt["HOLISTIC"], pt["MEAN4"])
    rho2, p2 = stats.spearmanr(pt["OVERALL_R"], pt["MEAN4"])
    summary = {"n_model_transcripts": len(model_tids), "n_controls": len(ctrl_tids),
               "spearman_holistic_vs_mean4": [rho, p], "spearman_overall_after_rubric_vs_mean4": [rho2, p2]}

    # Known-groups check: controls vs model transcripts of the same scenario (run 1, both graders)
    if ctrl_tids:
        pt_all = per_transcript_means(long[(long.run == 1) | (long.agent != "scripted-control")], model_tids + ctrl_tids)
        kg = []
        for s in sorted(pt_all.scenario.unique()):
            c = pt_all[(pt_all.scenario == s) & (pt_all.agent == "scripted-control")]
            mdl = pt_all[(pt_all.scenario == s) & (pt_all.agent != "scripted-control")]
            for m in MEASURES:
                kg.append({"scenario": s, "measure": m, "control_mean_run1": float(c[m].mean()),
                           "model_min": float(mdl[m].min()), "model_mean": float(mdl[m].mean()),
                           "control_below_all_model": bool(c[m].mean() < mdl[m].min())})
        kg = pd.DataFrame(kg)
        kg.to_csv(RESULTS / "known_groups_controls.csv", index=False, float_format="%.2f")
        summary["known_groups_control_below_all_model_by_measure"] = kg.groupby("measure")["control_below_all_model"].sum().to_dict()
        make_figure(agr, agr_ctrl, pt_all)
    else:
        make_figure(agr, agr, pt.assign())

    # Grader x agent means (self-preference check): per grader, mean over both runs of per-transcript grades
    ga = long[long.tid.isin(model_tids)].groupby(["grader", "agent", "measure"])["value"].mean().unstack("measure")
    ga[MEASURES].round(3).to_csv(RESULTS / "grader_by_agent_means.csv")

    # Alphas against Krippendorff's (2004) recommended minima (.800; .667 for tentative conclusions)
    thr = {}
    for comp in ["Inter-grader (run 1)", "Inter-grader (run 2)", "Repeat-run (Sonnet grader)", "Repeat-run (Opus grader)"]:
        v = agr[agr.comparison == comp]["alpha"]
        thr[comp] = {"n": int(len(v)), "n_ge_0.667": int((v >= 0.667).sum()), "n_ge_0.800": int((v >= 0.800).sum()),
                     "max": float(v.max())}
    summary["alpha_vs_krippendorff_minima"] = thr
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    pd.set_option("display.width", 200)
    print(agr.round(3).to_string(index=False))
    if ctrl_tids:
        print(agr_ctrl.round(3).to_string(index=False))
    print(ia[ia.indicator.str.startswith("ALL")].round(3).to_string(index=False))
    print(disc.round(4).to_string(index=False))
    print(dist.to_string(index=False))
    print(json.dumps(summary, indent=2, default=float))


if __name__ == "__main__":
    main()
