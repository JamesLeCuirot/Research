# Do LLM Monitors Miss Rare Threats?

*A Pre-registered Test of the Low-Prevalence Effect* (paper 02; working title was "Rare Threats Are Missed Threats")

**James Le Cuirot** · Citadel Aero · Draft v0.1, 4 November 2026

## Abstract

AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to send the most suspicious items to a small human audit. Real attacks are expected to be rare. Human screeners miss rare targets far more often than common ones, mainly because they grow more reluctant to say "yes"; airport security counters this with Threat Image Projection. In a pre-registered experiment we tested whether large language model (LLM) monitors show this low-prevalence effect. Two Claude models reviewed 419 execution-verified pairs of clean and backdoored Python solutions to MBPP problems (30,880 judgments). The prediction failed in the opposite direction. In batches of 40, both monitors caught more backdoors when backdoors were rare: hit rates rose from 0.51 at 50% prevalence to 0.69 at 2.5% for Haiku, and from 0.50 to 0.74 for Sonnet (Holm-adjusted p = .0015 and p < .001), with false-alarm rates below 2%. The decision criterion did not become more conservative. Single-item review caught about as many backdoors as 2.5% batches and more than crowded ones. Stating that about 1 in 100 submissions contained a backdoor, rather than about half, slightly lowered Sonnet's single-item hit rate (0.85 to 0.78); Haiku's change was not significant. A labelled calibration block modelled on Threat Image Projection did not reliably raise hit rates and more than doubled Sonnet's false alarms. Post hoc analyses suggest that backdoors received lower suspicion scores when many shared a batch. In this setting, crowding rather than rarity was associated with misses.

## Results at a glance

| Hypothesis | Outcome |
|---|---|
| H1: fewer hits at 2.5% than 50% prevalence (batch) | **Disconfirmed, opposite direction** in both monitors (OR 2.15 Haiku, 2.81 Sonnet) |
| H1a: the effect is a conservative criterion shift | **Not supported.** Sonnet's criterion became more liberal; Haiku's *d′* rose |
| H2: stating "1 in 100" lowers single-item hits | **Supported for Sonnet only**, small (−7.5 points, population-averaged) |
| H3: labelled calibration block raises hits at 2.5% | **Not supported.** It raised Sonnet's false alarms from 1.7% to 4.0% |
| E1–E4 (exploratory) | No position effect; independence instruction no effect; single items caught more than P50 and P10 batches (significant except Haiku at P50, p = .051) |

## Status

| Part | State |
|---|---|
| Pre-registration and §9 clarifications | Done; the timing of items 4–12 is disclosed in the paper (Section 5.8) |
| Experiment, analysis, figures | Done (engineer); `results/RESULTS.md` |
| Paper | **Complete draft v0.1.** About 7,800 words of prose (about 8,400 with tables and captions), 5 tables, 5 figures, 40 references |
| Folder name | Still `02-do-llm-monitors-miss-rare-threats`; the lead will rename it to match the new title |
| Not done | `paper.html` / `paper.pdf` not built; nothing committed |

## What James should check

1. **Title.** The paper now uses the lead's suggested title, split into title and subtitle. The old title asserted the effect that was not found.
2. **How strongly the safety point is put.** Section 7.3 frames "clustered attacks in one batch may lower each item's suspicion" as a hypothesis for future testing, not a finding. Check you are comfortable with that framing, and with the abstract's last sentence: "crowding rather than rarity was associated with misses".
3. **H2 for Sonnet.** The registered GLMM gives an odds ratio of 0.04, which looks dramatic. The item-specific GLMM coefficient is inflated because 92 of 120 items were flagged in all conditions. The paper reports the population-averaged odds ratio (0.61) and the 7.5-point drop alongside it. Check that this explanation is clear enough.
4. **Pre-registration timing.** Section 5.8 says items 1–3 were committed before any main call, and that items 4–12 first appear in a commit made after the run had started, so they should be read as "recorded at, not demonstrably before" data collection. This follows your note in `PREREGISTRATION.md` §9 closely; please confirm the wording.
5. **Edit-size threshold timing.** §9 item 3 says the 0.6 threshold was "set during verification of the first generation run". `results/RESULTS.md` §7 says it "was coded before the verifier was first run on any generated item, while generation was under way". The paper says it "was set while the first generation run was under way and applied unchanged". The engineer may want to reconcile the two texts.
6. **New citation.** Cain, Adamo & Mitroff (2013) is cited (abstract only) as a loose human analogue for crowding: subsequent search misses, also called satisfaction of search.
7. **Reported precision.** Exact p values from `analysis.json` are used where the tables round them, for example Haiku's H1 Holm p = .0015, where the table shows .001.
8. **Aviation paragraph (Section 7.6).** It is a short, hedged suggestion for developers of document-screening tools. Delete it if it reads as off-topic.
9. **Unchanged from Phase 1.**
   - The Anthropic page is cited as Favaro & Wright (n.d.).
   - Greenblatt et al. is cited as the ICML 2024 paper.
   - Several human-factors sources were seen as abstracts only (listed in `sources.md`).
10. **Trims.** To stay near the length target, the background lost several quotes: the SHADE-Arena false-positive figure, the Ye et al. alert-fatigue sentence, the AUROC/precision sentence and the Mitroff & Biggs R². All are still verified in `sources.md` if you want them back.

## Open questions

- Is the crowding effect about the *number* of backdoors in a context or their *share*? All batches held 40 items, so the two were not separated.
- Does crowding carry over to agent transcripts, where several suspicious actions may share one monitor call?
- Would monitors that score items one at a time but keep a memory across items, or that run at higher effort, behave more like human screeners?

## How to develop it

- **Separate number from share.** Vary batch size and the number of backdoors independently, for example 1, 5 or 20 backdoors in batches of 40, 100 and 200.
- **Clustered attacks in agent settings.** Test whether placing several attacks in one transcript, or in one monitored batch of actions, lowers per-attack suspicion (BashBench, SHADE-Arena or LinuxArena-style tasks). This is the safety-relevant version of the finding.
- **Other monitor families and settings.** GPT, Gemini and open-weight monitors; higher effort; direct API calls rather than Claude Code.
- **Lower prevalence.** 1 in 100 or 1 in 400 with longer contexts, now that rarity did not hurt at 1 in 40.
- **Matched calibration examples.** Following Becker et al. (2026), compare calibration examples of the same backdoor type as the target with examples of a different type, and measure the false-alarm cost against an audit budget.
- **Human comparison.** Run people on the same items, singly and in batches, at the same prevalences. This tests the human effect directly in this task, and the crowding effect in people.
- **TIP for measurement.** Use inserted known attacks to estimate a deployed monitor's hit rate under its real input mix; Buser et al. (2025) give a target of about 100 events.

## Files

- `paper.md`: the paper (source of truth). Build with `papers/_build/build.sh`.
- `sources.md`: verification log, gap-search record and a table tracing every number in Methods and Results to the results files.
- `PREREGISTRATION.md`: the registered design and §9 clarifications.
- `code/`, `data/`, `results/`, `figures/`: experiment, by the research engineer; `results/RESULTS.md` is the full numerical report.
