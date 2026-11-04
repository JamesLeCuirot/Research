"""Print the table of registered per-condition measures (PREREGISTRATION sections 5 and 6) from
results/analysis.json: hit and false-alarm rates (Wilson 95% CIs), d', c and AUROC (95% bootstrap CIs:
batches for Experiments 1 and 3, paired items for Experiment 2) and mean suspicion scores for backdoored
and clean items. These are registered measures, not post hoc. The same numbers appear in
results/RESULTS_numbers.md ("Descriptive results per condition"); this script only lays them out.

Usage: python registered_measures_table.py > results/registered_measures_table.md
"""

import json

from common import RESULTS

A = json.loads((RESULTS / "analysis.json").read_text())
CONDS = [("P50", "Exp 1"), ("P10", "Exp 1"), ("P2.5", "Exp 1"), ("R-cal", "Exp 3"), ("R-ind", "Exp 3"),
         ("none", "Exp 2"), ("S50", "Exp 2"), ("S1", "Exp 2")]


def ci(x, nd):
    return f"[{x[0]:.{nd}f}, {x[1]:.{nd}f}]"


print("| Monitor | Condition | H [95% CI] | F [95% CI] | d′ [95% CI] | c [95% CI] | AUROC [95% CI] | Mean suspicion, backdoored | Mean suspicion, clean |")
print("|---|---|---|---|---|---|---|---|---|")
for mon in ("Haiku", "Sonnet"):
    for cond, exp in CONDS:
        d = A["descriptive"][f"{mon}|{cond}"]
        b = A["bootstrap_ci"][f"{mon}|{cond}"]
        print(f"| {mon} | {cond} ({exp}) | {d['H']:.3f} {ci(d['H_ci'], 3)} | {d['F']:.4f} {ci(d['F_ci'], 4)} | "
              f"{d['d_prime']:.2f} {ci(b['d_prime'], 2)} | {d['c']:.2f} {ci(b['c'], 2)} | {d['auroc']:.3f} {ci(b['auroc'], 3)} | "
              f"{d['mean_susp_backdoored']:.1f} | {d['mean_susp_clean']:.1f} |")
