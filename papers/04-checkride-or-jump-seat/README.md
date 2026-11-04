# Checkride or Jump Seat? What LOSA and Evidence-Based Training Teach About Evaluation Awareness in AI Systems

**Status: draft v0.3 for author review (4 November 2026).** Revised after an independent audit and a second-round verification (both in `AUDIT.md`); v0.1 was titled "Checkride or Line Check?". Not peer reviewed. Built to `paper.html` and `paper.pdf` with `papers/_build/build.sh`. Main text about 8,485 words, plus 6 tables, 1 figure and a short appendix.

## Abstract

Frontier language models can often tell when they are being evaluated, and in some studies they behave better when they say they are being tested. This threatens the validity of pre-deployment safety evaluations. Airline training faced a similar problem: a checkride shows what a crew does while being assessed. It developed two complementary answers. Line Operations Safety Audits (LOSA) put trained observers in the flight-deck jump seat on normal flights under confidential, non-jeopardy conditions, explicitly not as checks, and code threats, errors and undesired aircraft states. Evidence-based training (EBT) assesses competencies through observable behaviours across varied scenarios rather than a fixed list of manoeuvres, and requires assured instructor concordance. This paper maps their design principles onto alignment evaluation, records how far current AI practice already follows them, and states where the analogy fails. It proposes a "jump-seat" layer of privacy-preserving, non-jeopardy observation of deployed models and a competency-based alignment assessment, and shows how the two feed each other. A small feasibility pilot graded 48 model transcripts from six airline-workplace scenarios with an EBT-style rubric and with a single holistic score, by two LLM graders, twice each. Each grader's two runs agreed at Krippendorff's alpha 0.56–0.89, but every inter-grader alpha for the grades fell below 0.667, Krippendorff's minimum for tentative conclusions, and the rubric showed no consistent advantage over the holistic score. Grades separated scenarios. Premature claims that actions had been taken lowered rubric communication grades but not holistic grades. Trained human instructors are the next test.

## Pilot in one paragraph

Six benign scenarios at a fictional airline ("Calder Air"): ambiguous instruction, error in the assistant's own earlier work, request beyond authority, pressure to report completion, operator–user conflict, and a hidden fitness-for-duty concern in a fatigue-report digest. Claude Haiku 5.5 and Sonnet 5.5 answered each four times (48 transcripts). Claude Sonnet 5.5 and Opus 5.5 graded each transcript twice with a 4-competency rubric (17 observable behaviours adapted from EASA AMC1 ORO.FC.231(b), 1–5 VENN-style anchors) and twice with a holistic 1–5 score. No response failed its scenario's central test, but six of eight S6 digests stated an escalation as done before the call was made (arguably anticipatory). Both conditions noticed this in their notes (holistic rationales 24/28, rubric COM.2 20/28), but only the rubric's communication grades fell (16/28 to 2–3; holistic grades all 4–5). Grades bunched at 4–5. Repeat-run alpha 0.56–0.89 (shown against Krippendorff's minima for reference only; 2 of 14 lower bounds reach 0.667). Inter-grader alpha for the grades: 0.24–0.49 (run 1), 0.25–0.54 (run 2), 0.41–0.57 (pooled): **all below 0.667**. Indicators: pooled inter-grader alpha 0.69 (run 1) and 0.66 (run 2), but individually none reaches 0.667 in run 1 and only PSD.4 in run 2. Rubric versus holistic: no consistent difference. Scenarios separated (epsilon-squared 0.53 competency mean, 0.62 holistic); models did not (stratified permutation p = 0.42; not powered). Six post hoc scripted controls (exploratory) were graded 1–2 by everyone; adding them raises alpha by a range effect only. Total model calls: 458.

## What James should check

1. **Title and terminology.** The title is now "Checkride or Jump Seat?" and the proposal is a "jump-seat layer". Note that under AMC1 ORO.FC.230(b)(3)(v) a line checker also sits in the observer's seat, so the paper says explicitly (§2.2) that the seat is not what distinguishes LOSA; its purpose is. An alternative title that avoids this nuance is "Checkride or Fly on the Wall?" ("fly on the wall" is the phrase used for LOSA observers in AC 120-90 Appendix 2 and Klinect et al., 2003). Your call.
2. **Aviation accuracy.** §1 and §2.1 now define checkride, line check and line evaluation of competence. Please check the descriptions against current practice as you know it (in published terms; nothing in the paper rests on personal anecdote), including the one-sentence mention of mixed EBT.
3. **ICAO texts.** Doc 9995 and PANS-TRG (Doc 9868) were read from copies on the websites of the Swedish Transport Agency and the Foundation for Aviation Competence (a private Swiss foundation), not from ICAO; Doc 9803 was not opened (only the ICAO Store listing). Please check quoted wording and paragraph numbers against licensed ICAO copies, including the Doc 9995 corrigendum (6/1/14) and any later PANS-TRG amendment.
4. **The rubric (Table 4, `code/rubric.py`).** Are the adapted observable behaviours sensible from an EBT instructor's point of view? The pilot's anchors dropped EASA's norm reference (grade 3 = "the average"); a revised rubric could restore it.
5. **The non-jeopardy translation (§4).** The paper argues the AI analogue of jeopardy is optimisation pressure from training on observation data.
6. **Scripted controls.** Now labelled post hoc and exploratory throughout. Decide whether to keep them at all, or replace them with responses you write at three performance levels.
7. **§5.3.** The ORO.FC.231(h)(3)(ii) parallel is now limited to evaluative spot checks in deployment. Check you are content with that framing.
8. **§5.4** ("Implications for aviation AI developers") is short and non-commercial by design.
9. **Delta Air Lines** is named in Klinect et al. (2003); the paper says "one US airline".

## Things that could not be verified (handled as stated)

- ICAO Doc 9803 full text (bibliographic facts only are used).
- Whether the Citadel Aero consolidation of the EASA rules matches Easy Access Rules Revision 24 line by line (amending instruments are named per provision).
- Two Sonnet transcripts in S3 report usage under two model IDs (`claude-sonnet-5-5` and `claude-sonnet-5`), possibly an automatic fallback. Kept and flagged.

## Prior-work search

No earlier application of LOSA or TEM to AI evaluation was found, and none of EBT/CBTA to alignment evaluation or evaluation awareness. Competency-based assessment from air traffic controller training **has** been applied to AI agents for air traffic control (Carvell et al., 2026; Pepper et al., 2026, both AIAA SciTech 2026; identified by the audit and verified). The paper's novelty claim is narrowed accordingly. Queries are in Appendix A. Semantic Scholar and OpenAlex were rate-limited and Elicit was unavailable, so the search is not exhaustive.

## Open questions

- Which competencies, beyond the four piloted, should an alignment competency framework contain, and what evidence should define them?
- What would a TEM taxonomy for agent transcripts look like, and could it be applied reliably to real (privacy-protected) deployment data? The S6 finding (status reported as done when it was not) is the kind of "error" such a taxonomy should capture.
- How should a "non-jeopardy firewall" between observation data and training be specified so that developers can still fix what they find?
- Does competency-based grading become more reliable than holistic grading once graders are standardised and observable behaviours carry scenario-specific guidance on when they apply?

## How to develop it

1. **The real validation: human instructor grading.** Have two or more trained EBT instructors grade the same 48 transcripts with the same rubric and the holistic score, after a concordance session using standardisation material at three performance levels (as GM1 ORO.FC.231(a)(4) suggests is one way to verify concordance). Compare instructor–instructor and instructor–LLM agreement against Krippendorff's minima, and with Carvell et al.'s (2026) instructor IRR for AI ATC agents. Pre-register it (see `papers/02-rare-threats-are-missed-threats/PREREGISTRATION.md` for the house format).
2. **Wider range of performance, planned in advance.** Generate weaker responses from more models, lower effort settings or adversarial system prompts, and fix the plan before seeing grades.
3. **Scenario-specific guidance.** Add "desired outcomes" and a competency map per scenario, as EBT does per training topic (AMC2 ORO.FC.232).
4. **Restore the norm reference** in the grade anchors and drop the overall grade after the rubric (or make it competent/not competent, as GM2 ORO.FC.231(d)(1) suggests).
5. **Surface variation** across scenario templates to test whether competency grades generalise across variants.
6. **A jump-seat pilot** with an operator partner and privacy safeguards: TEM coding of a small sample of real assistant interactions.

## Files

| Path | Contents |
|---|---|
| `paper.md` | The paper (Pandoc Markdown, YAML header). |
| `sources.md` | Verification log: one entry per reference, with quotes and locators; v0.2 additions marked. |
| `AUDIT.md` | Independent audit of v0.1 (not edited here). |
| `code/scenarios.py` | The six scenarios (system prompt, scripted earlier turns, final user turn, designers' expectations). |
| `code/rubric.py` | Competencies, observable behaviours, grade anchors, grader prompts and JSON schemas. |
| `code/controls.py` | The six post hoc scripted control responses. |
| `code/common.py` | Headless Claude Code call with retries (max 4 in parallel). |
| `code/generate.py`, `code/grade.py`, `code/analyse.py` | Pipeline: generate transcripts, grade them, analyse. |
| `prompts/` | Exact agent prompts, grader system prompts and schemas. |
| `data/transcripts.jsonl`, `data/control_transcripts.jsonl`, `data/grades.jsonl` | 48 transcripts, 6 controls, 408 gradings. |
| `results/` | Agreement (grades, indicators), grader bias (with Bonferroni), grader × agent means, discrimination (epsilon-squared, eta-squared(H), stratified permutation, minimum detectable difference), grade distributions, known-groups check, `summary.json`. |
| `figures/fig1_agreement.png` | Figure 1. |

## Reproduce

From the repository root:

```bash
uv run python papers/04-checkride-or-jump-seat/code/generate.py          # 48 calls (skips existing)
uv run python papers/04-checkride-or-jump-seat/code/grade.py             # 384 calls (skips existing)
uv run python papers/04-checkride-or-jump-seat/code/grade.py --controls  # 24 calls (post hoc controls)
uv run --no-project --with krippendorff==0.9.0 --with numpy --with scipy --with pandas --with matplotlib \
    python papers/04-checkride-or-jump-seat/code/analyse.py              # tables and figure
```

Model calls use `claude -p` (Claude Code 2.1.317) with tools, MCP servers and slash commands disabled, effort "low". Re-generating transcripts or grades will not reproduce the exact text (sampling is stochastic); the analysis is deterministic given the data files. No model calls were made for v0.2; only the analysis was re-run.

## Revision log

### v0.2, 4 November 2026: response to the independent audit (`AUDIT.md`)

Every item was re-checked against the source before changing the text. No audit item was rejected outright; partial or modified responses are marked **(modified)** with the reason.

| # | Sev | Audit item | What was done |
|---|---|---|---|
| 1 | M | Novelty overstated | Verified Carvell et al. (2026; arXiv:2601.04288, doi:10.2514/6.2026-2558; full text read) and Pepper et al. (2026; arXiv:2601.03113, doi:10.2514/6.2026-1794). Claim narrowed to: no prior LOSA/TEM for AI evaluation, and no EBT/CBTA for alignment evaluation or evaluation awareness. Both papers cited in §1, Table 2, §4 and Appendix A; Carvell's instructor IRR added to §6.5. README updated. |
| 2 | M | "Line check" inverts aviation meaning | Retitled "Checkride or Jump Seat? ..."; proposal renamed "jump-seat layer" throughout. §1 and §2.1 now define checkride and line check (ORO.FC.230(b)–(c); AMC1 ORO.FC.230(b)(3), (d)(2)); §2.2 explains that LOSA defines itself against checks (AC 120-90 App. 4 "not checkrides"); §4 maps pre-deployment evaluation to checkride, deployment spot checks to line check, jump-seat layer to LOSA. **(modified)** AMC1 ORO.FC.230(b)(3)(v) shows the line checker also uses the observer's seat, so §2.2 states that the seat is not the difference, its purpose is; README item 1 offers "Checkride or Fly on the Wall?" as an alternative. |
| 3 | M | Post hoc controls not labelled; conclusions lean on them | Labelled "post hoc, exploratory, written by the drafting assistant (Claude Opus 5.5) after the transcripts" in §6.1, §6.3, §6.4 (own subsection), Fig. 1 caption and legend; removed from the abstract's findings and from the tables (values now in text only); 0.41 → 0.91 described as a range effect; "depends on calibration" deleted from §8; §6.5 no longer cites the controls as evidence. `code/controls.py` docstring updated. |
| 4 | M | Rubric vs holistic: run 1 only | Table 5 now gives run 1, run 2 and all-four-ratings inter-grader alphas; §6.4 states there is no consistent difference (order reverses between runs; CIs overlap); "more reliable than" removed. |
| 5 | m | Effect size mislabelled | Verified: code computed (H − k + 1)/(n − k), eta-squared based on H. Now reports epsilon-squared = H/(n − 1): 0.53 (competency mean), 0.62 (holistic); both kept in `results/discrimination.csv` with correct labels. README fixed. |
| 6 | m | Unsupported EASA "reason"; "asks" too strong | "Reason" sentence deleted; GM1 ORO.FC.231(a)(4) now quoted as "may be verified" and described as a suggestion; §6.3 says the controls produced two clusters, not three levels. |
| 7 | m | S6 misreported-status pattern omitted | Re-checked in the transcripts: six of eight S6 digests state the escalation as done (Haiku 1, 3; Sonnet 1–4), one ambiguous (Haiku 4); S2 Haiku 1 "I've flagged this...". All low COM grades on these cite it. Reported in §6.4, §6.5, §8 and the abstract; "none showed a clear failure" replaced. |
| 8 | m | Verbal labels unanchored; thresholds verifiable | Krippendorff (2004) postprint downloaded and verified ("Recommendations" (iii)); cited in §6.3; abstract, §6.4 and Fig. 1 now report results against 0.667/0.800 (all inter-grader alphas below 0.667; 12/14 repeat-run ≥ 0.667, 2/14 ≥ 0.800). sources.md corrected. |
| 9 | m | Overall grade departs from GM2 ORO.FC.231(d)(1) | Acknowledged in §6.2 and §6.5. |
| 10 | m | Anchors drop EASA norm reference | §2.3 now quotes grades 2 and 3 of AMC1 ORO.FC.231(d)(1); §6.2 states the departure; §6.5 adds it as a fourth explanation. |
| 11 | m | Two numbering schemes | Klinect et al. now cited by characteristic name; Table 1 caption notes Klinect's 2/4 swap. |
| 12 | m | ORO.FC.231(h)(3)(ii) "precedent" overstated | §5.3 rewritten as a loose parallel: the rule lengthens the interval between evaluative line evaluations and does not lighten simulator assessment; the closer AI counterpart is less frequent evaluative spot checks in deployment; "nothing in the rule supports lighter pre-deployment testing". |
| 13 | m | Greenblatt framing | Moved to its own paragraph in §3.3 stating the direction (towards the training objective, not safety), with a verbatim quote. |
| 14 | m | ICAO copies undisclosed; blanket verification claim | Reference list notes name the hosts (Swedish Transport Agency; Foundation for Aviation Competence, a private Swiss foundation) without links; §7 and the AI-assistance statement now say what was checked against what. **(modified)** Part (b), checking against licensed ICAO copies, needs the author: README item 3. |
| 15 | m | Model comparison overstated | §6.4: "no detectable difference ... not powered"; scenario-stratified permutation p = 0.42; minimum detectable difference about 0.2; removed from the abstract. |
| 16 | m | Shared authorship not disclosed | §6.1 and §6.5 name the drafting model (Claude Opus 5.5, also a grader) and the shared-authorship risk; grader × agent check reported (no self-preference; `results/grader_by_agent_means.csv`). |
| 17 | m | "Test–retest" terminology | Renamed "repeat-run (intra-grader) agreement" and defined in §6.3; code, results labels, tables and figure updated. |
| 18 | n | Fraser-Taliente authors | All 20 authors listed. |
| 19 | n | Feinstein & Cicchetti overstated | Rephrased (kappa-type coefficients low despite high raw agreement when ratings concentrate). |
| 20 | n | Baker cited for held-out channel | Now "(compare Baker et al., 2025)". |
| 21 | n | Klinect "managers found" | "many of its managers agreed ... line-oriented flight training and regular line checks". |
| 22 | n | "to their knowledge" | "to the knowledge of the LOSA Collaborative". |
| 23 | n | 13% context omitted | Qualifier quoted in §1. |
| 24 | n | Table 1 characteristic 10 name | Table 1 now uses the AC's names and numbers for all ten. |
| 25 | n | "within one point" uninformative | Qualified as a ceiling consequence; run-2 two-point gaps noted. |
| 26 | n | Grader-bias multiplicity | Bonferroni-adjusted p reported (PRO survives at 0.03; competency mean and holistic do not); all seven tests in `results/grader_bias.csv`. |
| 27 | n | S3 "flag the password" | Now "optionally". |
| 28 | n | Model names unverified | Verified on Anthropic's models overview page (cited as Anthropic, n.d.); API IDs kept in text. |
| 29 | n | Undefined jargon | Definitions added for checkride, line check, reward hacking, honeypot, scheming/covert actions, linear probe, steering vector and ablation. |
| 30 | n | Laine, Panickssery peer-reviewed versions | Verified via Crossref (NeurIPS 2024, DOIs 10.52202/079017-2044 and -2197); references now cite the proceedings. |
| 31 | n | EASA "n.d." | Now EASA (2026), Easy Access Rules for Air Operations, Revision 24 (March 2026), verified on the EASA page, with a note that texts came via the Citadel Aero library. |
| 32 | n | Primary rule for OPC/line check; mixed EBT | ORO.FC.230(b)–(c) and AMC1 ORO.FC.230 cited in §2.1; one sentence on mixed EBT in §2.3. |
| 33 | n | GM19 LOSA definition | Quoted in §2.4. |
| 34 | n | Competency map | **(modified)** §6.5 mentions the per-competency columns of the AMC2 ORO.FC.232 table; the excerpt seen shows one column per competency but not the label "competency map", so that label is not used. |
| 35 | n | No pre-registration | Disclosure kept and made bold in §6.1. |
| 36 | n | Covas & Hidalgo Toledo (2026) | Verified (arXiv abstract) and cited in Appendix A. **(modified)** Not cited in §3 to keep the main text within 8,500 words. |
| 37 | n | Fig. 1 legend ambiguity | Legend now says "Sonnet grader"/"Opus grader" and "Haiku 5.5 / Sonnet 5.5 agent responses". |
| 38 | n | sources.md errors | GM1 ORO.FC.231(a)(4) full text read; Li et al. quote location corrected (abstract); thresholds verified; Doc 9868 host described correctly; v0.2 additions marked. |
| 39 | n | "never used to discipline" stated as fact | Now "must never be used", with the ¶10b(4) quotation. |

Other changes made while revising: the second-hand Gunther (2002) "70 percent" figure was removed (it was not needed and its primary source cannot be checked); main text trimmed to stay within 8,500 words; figure redrawn with run 2 and Krippendorff's thresholds. No new model calls were made; `code/analyse.py` was extended and re-run (deterministic).

### v0.3, 4 November 2026: response to the second-round verification (`AUDIT.md`, "Second-round verification (4 November 2026)")

Each point was re-checked against the source or the data before the text was changed.

| Item | What was done |
|---|---|
| #14 (stale clause) | Deleted "and one figure is quoted second-hand" from the AI-assistance statement (the Gunther figure was removed in v0.2). |
| #19 | §6.3 now reads "such as kappa (Feinstein & Cicchetti, 1990) and alpha (Krippendorff, 2004)"; the Krippendorff (2004) 82%-agreement/zero-coefficient example and single-category case were verified in the postprint. |
| #34 | Verified in the Citadel Aero library: the AMC2 ORO.FC.232 table header labels the competency columns "Competency map", and AMC8 ORO.FC.232 is titled "Scenario elements and competency mapping" with (e) "the instructor should always assess all observed competencies". §6.5 uses the term and cites AMC8; sources.md corrected (the v0.2 reason for not using the term was wrong). |
| N1 | Re-counted by hand: holistic rationales named the premature status claims in 24 of 28 ratings; rubric COM.2 flagged 20 of 28, never S6 Sonnet #3; Opus missed 4 of 12 S6 rubric ratings; all holistic grades 4–5, 16 of 28 COM grades 2–3. Abstract, §6.4, §6.5 and §8 now say both conditions noticed it and only the rubric's communication grade registered it in the score; COM.2 inter-grader alpha (0.52) reported. |
| N2 | "Every inter-grader alpha" restricted to the grades (abstract, §6.4, §6.5). §6.4 now acknowledges pooled indicator alpha 0.69 in run 1, cites Krippendorff (2004, Rec. (iv)) on averaging, and reports per-indicator alphas (run 1 none ≥ 0.667, highest COM.4 0.65, four undefined; run 2 only PSD.4, 0.79). |
| N3 | The §6.5 sentence linking low overall-after-rubric agreement to the EASA departure is replaced by a statement that the pilot says nothing about that effect (lowest alpha in run 1, highest in run 2). |
| N4 | Abstract drops "12 of 14"; §6.3/§6.4 and Fig. 1 caption state that Krippendorff's minima concern different coders ("as represented by different coders") and that repeat-run values are shown against them for reference only; §6.4 adds that only 2 of 14 repeat-run lower bounds reach 0.667; §6.5 reworded. (The figure image itself is unchanged; the caption carries the caveat.) |
| N5 | §6.5 Carvell comparison flagged as not directly comparable (association/concordance measures; wider performance range); Spearman's rho and Kendall's W defined. |
| N6 | "The other communication grades were 4 or 5". |
| N7 | 4.36 (exact 4.3646). |
| N8 | Table 5 caption notes that the "All four ratings" column includes the two within-grader pairs. |
| N9 | §6.4 notes the anticipatory reading of the S6 lines (two add "Outcome/Status to be confirmed") and calls them "premature status claims"; abstract wording changed accordingly. |
| N10 | Greenblatt: "in almost all cases where it complied, its reasoning stated ...". |
| N11 | §1: "two main kinds of recurrent flight check"; checkride "normally flown in a flight simulator"; EBT now described as replacing these checks with an evaluation phase and a line evaluation of competence (ORO.FC.231(a)(1), (h)), with the grade-1 definition attached to EBT, not to the checks. §2.1: "normally" in an FSTD. |
| N12 | §1 now says the prompts, transcripts, grades and code are kept in the paper's repository folder and available from the author on request (the repository is private). |
| N13 | README status line updated (v0.3; built with `papers/_build/build.sh`; folder renamed). |
| N14 | Reference now "Carvell, B. J." (Crossref). |
| #28 | Models-page URL updated to https://platform.claude.com/docs/en/about-claude/models/overview. |
| #29 | AMC and GM defined at first use (§2.1, with their non-binding status); Spearman's rho and Kendall's W defined (§6.5). |

To keep the main text within 8,500 words after these additions, v0.3 also shortened passages in §2.1–2.3, §3.2, §3.4, §4, §5.1–5.4 and §7 without removing any finding or reference (the GM1 ORO.FC.231(c) "not to spy on instructors" quotation and one duplicated sentence on rare events were dropped). No model calls were made and the analysis outputs are unchanged.
