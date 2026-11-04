"""Post hoc (journal version, 4 November 2026): agreement restricted to traces both coders judged failed.

Run from papers/06-afacs: uv run python scripts/posthoc_both_failed.py
Writes results/agreement_both_failed.md. Needs the local working codings in annotations/llm/.
"""
from pathlib import Path
from afacs import agreement as ag
out = []
for a, b, label in [("sonnet_bulk_r1", "opus_bulk_r1", "Sonnet run 1 vs Opus"), ("sonnet_bulk_r1", "sonnet_bulk_r2", "Sonnet run 1 vs Sonnet run 2")]:
    A = ag.usable(ag.load_llm(a), a); B = ag.usable(ag.load_llm(b), b)
    uids = sorted(set(A) & set(B))
    both = [u for u in uids if A[u].get("failure_observed") == "yes" and B[u].get("failure_observed") == "yes"]
    codes = sorted(ag.load_codebook_codes(ag.CURRENT_CODEBOOK, trace_only=True))
    m = ag.measures(A, B, both, codes); ci = ag.bootstrap(A, B, both, codes)
    out.append(f"## {label}: traces both coders judged failed (n = {len(both)} of {len(uids)})\n")
    out.append("| Measure | Cohen's κ | 95% CI |\n|---|---|---|")
    for k in ["layer_L4", "layer_L3", "layer_L2", "layer_L1", "codes_macro", "any_violation", "violation_evidence", "hfacs_error_macro", "ezell_macro", "deepest_layer_weighted"]:
        c = ci.get(k)
        out.append(f"| {ag.LABELS.get(k, k)} | {ag.fmt(m.get(k))} | {'' if not c else f'{c[0]:.2f}–{c[1]:.2f}'} |")
    out.append("")
txt = "# Agreement on traces both coders judged failed (post hoc)\n\nComputed for the journal version (4 November 2026) after an independent check noted that layer agreement over all 250 traces is inflated by traces at least one coder judged failure-free, where every layer is absent for both. Same measures and bootstrap as `afacs-agreement`, restricted to traces with `failure_observed = yes` from both coders. L1 cannot be computed: every failure has an L1 code.\n\n" + "\n".join(out)
Path("results/agreement_both_failed.md").write_text(txt)
print(txt)
