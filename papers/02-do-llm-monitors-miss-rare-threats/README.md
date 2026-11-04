# Do LLM Monitors Miss Rare Threats?

*A Pre-registered Test of the Low-Prevalence Effect* (paper 02; working title was "Rare Threats Are Missed Threats")

**James Le Cuirot** · Citadel Aero · Draft v0.2, 4 November 2026

## Abstract

AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to send the most suspicious items to a small human audit. Real attacks are expected to be rare. Human screeners miss rare targets far more often than common ones, mainly because they grow reluctant to say "yes"; airport security counters this with Threat Image Projection. In a pre-registered experiment we tested whether large language model (LLM) monitors show this low-prevalence effect. Two Claude models made 30,880 judgements of Python solutions drawn from 379 execution-verified pairs of clean and backdoored code. The prediction failed in the opposite direction. In batches of 40, both monitors caught more backdoors when backdoors were rare: hit rates rose from 0.51 at 50% prevalence to 0.69 at 2.5% for Haiku, and from 0.50 to 0.74 for Sonnet (Holm-adjusted p = .0015 and p < .001), with false-alarm rates below 2%. The decision criterion did not become more conservative. Single-item review caught about as many backdoors as 2.5% batches, and more than 10% and 50% batches in three of four comparisons. Stating that about 1 in 100 submissions contained a backdoor, rather than about half, slightly lowered Sonnet's single-item hit rate (0.85 to 0.78); Haiku's change was not significant. A labelled calibration block modelled on Threat Image Projection did not reliably raise hit rates and more than doubled Sonnet's false alarms. Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch than when one did.

## Results at a glance

| Hypothesis | Outcome |
|---|---|
| H1: fewer hits at 2.5% than 50% prevalence (batch) | **Disconfirmed, opposite direction** in both monitors (OR 2.15 Haiku, Holm p = .0015; 2.81 Sonnet, Holm p < .001). P10 behaved like P50 |
| H1a: the effect is a conservative criterion shift | **Not supported.** Sonnet's criterion became more liberal; Haiku's *d′* rose |
| H2: stating "1 in 100" lowers single-item hits | **Supported for Sonnet only**, small (−7.5 points). The registered GLMM is numerically unreliable for Sonnet, but an accurate post hoc refit (p = .0076) and an exact paired test (9 vs 0 items, p = .0039) agree. Haiku: 12 vs 7, p = .36 |
| H3: labelled calibration block raises hits at 2.5% | **Not supported.** It raised Sonnet's false alarms from 1.7% to 4.0%. Low power (80 judgements per cell) |
| E1–E4 (exploratory) | No linear position effect; independence instruction no effect; single items caught more than P50 and P10 batches in three of four comparisons (Haiku at P50: p = .051) |
| Interpretation | Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch; pop-out of a lone backdoor and crowding by several cannot be told apart |

## Status

| Part | State |
|---|---|
| Pre-registration and §9 clarifications | Done; timing of item 3 and items 4–12 disclosed in the paper (Section 5.8) |
| Experiment, analysis, figures, post hoc audit checks | Done (engineer); `results/RESULTS.md`, including §10 |
| Independent audit | Done; `AUDIT.md` (0 major, 6 moderate, 19 minor, 2 suggestions) |
| Paper | **Draft v0.2**, all audit fixes applied. About 7,650 words of prose (about 8,550 with tables and captions), 6 tables, 5 figures, 38 references |
| Not done | `paper.html` / `paper.pdf` not rebuilt; nothing committed |

## What James should check

1. **Length.** Prose is about 7,650 words, which is still above the 7,500 target the lead asked for and the house range of 5,000–7,000 words. The audit fixes added about 600 words (H2 refit, harness disclosure, timing record, power statements, Table 3). Further cuts could come from Sections 2–4 or from the E4 detail.
2. **Harness disclosure (Section 5.4).** It says each call's context included a field for the account's e-mail address, without giving the address. Check that you are content to disclose this.
3. **H2 for Sonnet.** The paper keeps the registered GLMM numbers as the registered result. It reports the accurate refit and the exact paired test as post hoc, and Table 4 has a note explaining the odds ratio of 0.04.
4. **Item 3 timing.** The paper follows your correction in §9: the threshold was coded before verification began, per the engineer's record. It says plainly that git cannot confirm this.
5. **Unchanged.** The Anthropic page is cited as Favaro & Wright (n.d.), and Greenblatt et al. as ICML 2024. Several human-factors sources were seen as abstracts only (`sources.md`).

## Revision log

**v0.2, 4 November 2026, after the independent audit (`AUDIT.md`)**

| Audit item | Action |
|---|---|
| 1 (moderate) H2 GLMM inaccurate for Sonnet | §6.4: registered numbers kept as the registered result. Added an explanation that the 40-node fit stopped at a local optimum and is inaccurate at large σ, so the 9–33 spread is a quadrature artefact. Added, post hoc, the accurate fit (σ 13.4; −3.76, SE 1.41, z −2.67, p .0076; LR p .00024) and the exact paired tests (Sonnet 9 vs 0, p .0039; Haiku 12 vs 7, p .36). §8 updated |
| 2 (moderate) registered measures missing | New Table 3 (registered): *d′*, *c*, AUROC with CIs and mean suspicion scores for all 16 cells, from `RESULTS.md` §10.2. Table 6 is now post hoc columns only |
| 3 (moderate) registered power statement | §5.7 states it; it is applied to the Haiku H2 null (§6.4), the H3 null (§6.5) and §8 |
| 4 (moderate) §9 item 3 | §5.8 cites the author's correction, gives the original wording, and says the timing comes from the engineer's record and cannot be confirmed from git. Caveat on items 4–12 kept. Added that the analysis code, including the GLMM rule, was committed at 23:10:45 UTC, before the first main output at 23:12:32 UTC (checked against git and `monitor_attempts.jsonl`) |
| 5 (moderate) "crowding rather than rarity" | Abstract, §1, §7.1, §7.2 and §9 rephrased: rarity did not increase misses, and misses were more frequent with several backdoors per batch. Pop-out and crowding are presented as equal candidates, with P10 ≈ P50 noted |
| 6 (moderate) harness context | §5.4 states: not `--bare`; default system prompt replaced; about 1,800 tokens of scaffolding per call (Haiku 1,812, Sonnet 1,791), constant across conditions and time; no CLAUDE.md, memory, git status or hooks; an account e-mail field present (address not printed). §8 updated |
| 7 379 vs 419 pairs | Abstract now says the judgements are drawn from 379 pairs; §5.2 states that main items came only from the main pool |
| 8 "more than crowded" | Now "in three of four comparisons" (abstract, §6.6), with Haiku's p = .051 in README and §6.6 |
| 9 independence instruction | §1: described as a prompting instruction, not a screening-research remedy |
| 10 Najt wording | §3.2: "half of its 40 hand-designed attacks were never caught … in any of ten trials" |
| 11 Wolfe 2007 false alarms | §2.2 and §7.4 now say false alarms were higher than in the baseline experiment (re-checked: within Experiment 7, 0.13 vs 0.15, ns) |
| 12 "two changed lines" | §5.2: lines changed in a unified diff (added plus removed), for example one line replaced |
| 13 independence of judgements | §5.4: "every call is an independent random draw" |
| 14 H1a not a Wald test | §5.7: Wald tests are for H1–H3; H1a is a bootstrap decision rule |
| 15 in-call corrections | §5.9 and §8: inferred from `num_turns` > 2, intermediate outputs unlogged, not anticipated by the registered retry rule |
| 16 Sonnet S1 criterion and scores | §6.4, §7.1, §7.5: Sonnet's Δ*c* interval includes zero; ΔAUROC −0.017 [−0.034, −0.004], mean backdoored score 75.0 → 62.7, band flag rate not lower; "most human-like" tempered |
| 17 Table OR 0.04 | Table 4 note: the GLMM OR is item-specific; population-averaged OR 0.61 [0.44, 0.84], −7.5 points |
| 18 sensitivity check | §6.6: H2 tested with the item-clustered GLM; Haiku H3 p .150 → .076 |
| 19 §7.5 post hoc | "post hoc score-band analysis" stated |
| 20 Figure 2 caption | Now: cluster bootstrap over batches (Exp 1, 3) or paired item bootstrap (Exp 2) |
| 21–22 scripts and docstrings | Engineer's items (`code/posthoc_descriptives.py`; docstrings fixed). No paper change needed |
| 23 references | Kapetanovic et al. "in press" (no pages); Griffin (IASEAI '26) and Hida (ENIAC 2026, BRACIS) notes; Wolfe 2013 "Article 33" |
| 24 length | Background, Methods and Discussion trimmed (Mitroff & Biggs and Makins et al. dropped). Prose about 7,650 words, against about 7,800 in v0.1, despite the additions |
| 25 spelling | "judgement(s)" throughout, except inside quotations |
| 26 (suggestion) E1 dip | §6.6 now notes the low hit rates at positions 1–8 in P10, which the linear test would not detect |
| 27 (suggestion) code timing | Included in §5.8 (see item 4) |

**v0.1, 4 November 2026.** Results, Discussion, Limitations and Conclusion written from `results/`; the paper was retitled.

**Phase 1, 3 November 2026.** Introduction, Background, Methods and Limitations skeleton.

## Open questions

- Is the drop in hits about the *number* of backdoors in a context or their *share*? All batches held 40 items, so the two were not separated, and pop-out and crowding cannot be told apart.
- Does the effect carry over to agent transcripts, where several suspicious actions may share one monitor call?
- Would monitors that run at higher effort, in `--bare` mode or through the raw API behave differently?

## How to develop it

- **Separate number from share.** Vary batch size and the number of backdoors independently, for example 1, 2, 3, 5 or 20 backdoors in batches of 40, 100 and 200.
- **Clustered attacks in agent settings.** Test whether placing several attacks in one transcript, or in one monitored batch of actions, lowers per-attack suspicion (BashBench, SHADE-Arena or LinuxArena-style tasks).
- **Other monitor families and settings.** GPT, Gemini and open-weight monitors; higher effort; `--bare` mode or direct API calls, with the full context logged.
- **Lower prevalence.** 1 in 100 or 1 in 400 with longer contexts.
- **Matched calibration examples.** Following Becker et al. (2026), compare calibration examples of the same backdoor type as the target with examples of a different type, and measure the false-alarm cost against an audit budget.
- **Human comparison.** Run people on the same items, singly and in batches, at the same prevalences.
- **TIP for measurement.** Use inserted known attacks to estimate a deployed monitor's hit rate under its real input mix; Buser et al. (2025) give a target of about 100 events.

## Files

- `paper.md`: the paper (source of truth). Build with `papers/_build/build.sh`.
- `sources.md`: verification log, gap-search record and a table tracing every number to the results files.
- `PREREGISTRATION.md`: the registered design and §9 clarifications.
- `AUDIT.md`: the independent audit.
- `code/`, `data/`, `results/`, `figures/`: experiment, by the research engineer; `results/RESULTS.md` is the full numerical report.
