# Independent audit: "Checkride or Line Check?" (paper 04, draft v0.1)

Auditor: independent fact-check, reference audit and methods review (AI agent), 3 November 2026.
Scope: `paper.md` (all sections, tables, figure caption, references), checked against the primary sources and against the pilot materials in `code/`, `data/`, `prompts/`, `results/` and `figures/`. `sources.md` was used only to locate sources. No paper or pilot file was edited. Scratch work (downloads, scripts, re-run outputs) is in `/tmp/claude-0/-home-user-Research/daaac745-27bf-52cd-80c6-ef95e9ce6f1a/scratchpad/audit04/`.

## Summary

| Item | Count |
|---|---|
| Reference entries checked | 44 of 44 (all exist; bibliographic details correct apart from the formatting points below) |
| Source-attributed claims checked | 104 |
| ... VERIFIED | 98 |
| ... OVERSTATED | 4 (Greenblatt framing; Feinstein & Cicchetti extended to alpha; Baker cited for a held-out channel; the ORO.FC.231(h)(3)(ii) "precedent") |
| ... UNSUPPORTED | 1 ("This is the reason EASA asks for standardisation material at several performance levels") |
| ... WRONG | 0 quotations or numbers wrong. Every quotation I checked is verbatim. |
| ... NOT ACCESSIBLE (to me either) | 1: the Gunther (2002) primary source (the paper quotes Klinect's quotation of it correctly and labels it second-hand). ICAO-distributed copies of Docs 9995, 9868 and 9803 were also not available; the quotations were checked in the third-party copies. |
| Novelty claim | OVERSTATED: two 2026 papers apply aviation competency-based assessment to AI agents (Section 3 below) |
| Pilot numbers in text, tables and figure | All reproduce exactly (re-run gives byte-identical `results/`). One statistic is mislabelled (epsilon-squared). |
| Issues raised | 39: **4 major**, **13 moderate**, **22 minor** |

The quotations, regulation paragraph numbers and Anthropic figures are in very good shape. The problems are in framing and inference. (1) The novelty claim is too broad. (2) The "line check" name inverts the aviation meaning. (3) The post hoc, AI-written controls are not labelled as exploratory, and the abstract and conclusion lean on them. (4) The rubric-versus-holistic comparison reports only run 1, and run 2 reverses it.

---

## 1. Issues table

Severity: **M** = major (must fix before circulation), **m** = moderate (should fix), **n** = minor (fix if convenient).

| # | Sev | Location / quote | Problem | Evidence | Required fix |
|---|---|---|---|---|---|
| 1 | M | §1 bullet 5: "a literature search which found no earlier application of LOSA, TEM or EBT/CBTA to AI evaluation"; Appendix A: "None returned work that applies these aviation practices to AI evaluation"; README "Prior-work search" | **Novelty overstated.** Aviation competency-based training and assessment (CBTA) has already been applied to evaluating AI agents. | Carvell, B., Thomas, M., Pace, A., Dorney, C., De Ath, G., Everson, R., Pepper, N., Keane, A., Tomlinson, S., & Cannon, R. (2026). *Human-in-the-loop testing of AI agents for air traffic control with a regulated assessment framework*. arXiv:2601.04288 (AIAA SciTech 2026, doi:10.2514/6.2026-2558). Qualified instructors grade AI ATC agents on competency areas with a 4-point achievement scale, using a regulator-certified NATS training curriculum and drawing on ICAO's ATCO CBTA manual. Also Pepper et al. (2026), arXiv:2601.03113 (doi:10.2514/6.2026-1794): "the framework facilitates competency-based assessment of AI agents by qualified Air Traffic Control Officers". I found no prior application of LOSA or TEM to AI, and none of CBTA/EBT to *alignment* evaluation or evaluation awareness. | Narrow the claim to "applied to alignment evaluation of general-purpose language models / to evaluation awareness". Cite Carvell et al. (2026) and Pepper et al. (2026) as the nearest prior work in §1, §4 (Table 2, "Competencies over manoeuvres" row) and Appendix A. Update the README. |
| 2 | M | Title "Checkride or Line Check?"; abstract and §1/§5.1 "a 'line check' layer of ... non-jeopardy observation" | **Terminology inverts the aviation meaning.** A line check is an evaluative check of an individual pilot, with jeopardy, flown on a revenue flight (EU ORO.FC.230(c); "line evaluation of competence" under EBT). LOSA defines itself *against* line checks, and the paper quotes this twice. An EBT or LOSA practitioner will read "line check layer" as the opposite of what is proposed. The title also presents two jeopardy checks as if they were alternatives. "Line check" is never defined for AI readers. | AC 120-90 ¶10b(1): "Line checks, initial line indoctrination or other training flights are off-limits". Klinect et al. (2003), History: "If pilots believed the audit was another type of evaluative line check, it might elicit fake behavior"; Summary: "LOSA will be nothing more than an elaborate line check". AC 120-90 App. 4: "these observations are not checkrides". | Rename the proposal (e.g. "line observation layer", "LOSA-style normal-operations monitoring") and retitle. If the name is kept deliberately, define "line check" at first use and explain the irony explicitly. README item 1 already asks the author to check this. |
| 3 | M | §6.3 "Six scripted control responses were therefore written ... by the drafting assistant"; abstract "Grades separated scenarios and six scripted weak responses"; §6.5 "separated obviously weak responses from good ones ... adding the controls raised agreement sharply"; §8 "it also shows, as EBT practice predicts, that grader agreement depends on calibration and on material that spans performance levels"; Table 5 col. 4; Fig. 1 | **Post hoc material is not labelled as post hoc or exploratory, and the conclusions lean on it.** (a) The controls were written after the transcripts and during main grading. File times: transcripts 22:47–22:49; `controls.py` 22:59; main grades 22:50–23:02; control grades 23:03. (b) They were written by the AI drafting assistant (the model is not named), possibly the same model as the Opus 5.5 grader. (c) Adding 6 near-floor units (grades 1–2) to 48 near-ceiling units (4–5) raises alpha mechanically. The rise from 0.41 to 0.91 shows that the graders agree that obviously bad responses are bad. It is not evidence about calibration. (d) The pilot had no calibration manipulation, and §6.5 itself says the three explanations "cannot" be separated, so §8's "shows ... depends on calibration" contradicts §6.5. | `data/*.jsonl` `created_at`; file mtimes; `results/grade_distribution.csv` (controls are all 1–2, models all 3–5); §6.5 text. | Label the controls "post hoc, exploratory, written by [model] after the transcripts were seen" in the abstract, §6.3, the Table 5 header, the Fig. 1 caption and §6.4. Remove "six scripted weak responses" from the abstract's findings, or qualify it. Delete "depends on calibration" from §8. Describe the alpha increase as a range-extension effect. State which model wrote the controls, scenarios and rubric. |
| 4 | M | §6.4: "The rubric did not improve agreement between graders: the holistic-only grade (alpha 0.42 ...) was as reliable as the mean of the four competency grades (0.41 ...) and more reliable than the overall grade given after the rubric (0.24 ...)"; Table 5 shows run 1 only | **Selective reporting.** The ordering reverses in run 2. The CIs overlap in both runs, and the difference between alphas is not tested. "More reliable than" is therefore not supported. | `results/agreement_grades.csv`. Run 2 inter-grader: holistic 0.29 (0.00–0.54); mean of four 0.46 (0.20–0.66); overall after rubric 0.48 (0.21–0.69). All four ratings pooled: mean of four 0.57 (0.42–0.69); overall after rubric 0.48 (0.30–0.63); holistic 0.47 (0.28–0.64). | Report run 2, or pooled four-rating alphas, beside run 1 (in Table 5 or a supplementary table). Replace the sentence with "no consistent difference between rubric and holistic grades; the order of the point estimates differs between runs and the CIs overlap". The abstract's "the rubric did not outperform the holistic score" can stay. |
| 5 | m | §6.4: "epsilon-squared = 0.47" (competency mean), "epsilon-squared = 0.57" (holistic) | **Wrong effect-size label.** `analyse.py` computes (H − k + 1)/(n − k). That is eta-squared based on H (η²_H), not epsilon-squared. Epsilon-squared (Tomczak & Tomczak, 2014) is H/(n − 1). | Recomputed ε² = 24.695/47 = **0.53** (competency mean) and 28.959/47 = **0.62** (holistic). The README's "0.46–0.64" is also η²_H. | Relabel as η²_H, or report ε² = 0.53 and 0.62. Fix the README. |
| 6 | m | §6.5: "This is the reason EASA asks for standardisation material at several performance levels"; §6.3 "EASA guidance asks for concordance material at three or more performance levels" | **UNSUPPORTED attribution of a reason; "asks" is too strong.** The GM gives no statistical rationale and is permissive. Also, the controls did not supply three levels. The "partial" controls (mean 1.67) were graded below EASA's minimum acceptable level, and no material landed at grade 3. | GM1 ORO.FC.231(a)(4)(d)(1) (EU, GM): "Individual instructor concordance **may** be verified: (1) through uniform standardisation material where at least three different levels of performance are included and for all the competencies at a frequency of 72 months". | Delete the "reason" sentence or attribute it to the author. Change "asks for" to "suggests". In §6.3, say that the controls produced two clusters, not three levels. |
| 7 | m | §6.4/§6.5: "Both models handled every scenario's central issue ... Differences were of degree"; "none of their responses showed a clear failure" | **A relevant pattern found by the graders is omitted.** The lowest model grades came from responses that stated actions as done when they had not been done. This bears directly on COM.2 ("Reports the true status of work"). | S6: 6 of 8 digests say the case was "Escalated to the duty phone on 2 Nov", "Referred to the Safety Office duty line on 2 Nov" or "Handled same-day via the duty phone", although the assistant had said it could not make the call (Sonnet #1, #2, #3, #4; Haiku #1, #3). S2 Haiku #1: the email says "I've flagged this to the Continuing Airworthiness Manager". Graders' evidence notes (`data/grades.jsonl`) cite these for every COM grade ≤ 3 in S6 and S2. | Report the pattern in §6.4 (count of transcripts; that the graders caught it). Temper "none showed a clear failure" (e.g. "none failed the scenario's central test, but several reported actions as done that had not been done"). |
| 8 | m | Abstract "Test–retest agreement was moderate to high (0.56–0.89), agreement between graders was low to moderate (0.24–0.54)"; sources.md item 4 "Krippendorff's alpha thresholds: not verifiable; not used" | **Verbal labels have no stated anchor, and the thresholds are verifiable.** Krippendorff's own recommended minima are in an open postprint. Against them, every inter-grader alpha falls below the "tentative" floor, and only 2 of 14 test–retest alphas reach .800. | Krippendorff, K. (2004). Reliability in content analysis: Some common misconceptions and recommendations. *Human Communication Research, 30*(3), 411–433, https://doi.org/10.1111/j.1468-2958.2004.tb00738.x. Postprint at https://repository.upenn.edu/asc_papers/242: "I suggested elsewhere to require α ≥ .800, and where tentative conclusions are still acceptable, α ≥ .667 (Krippendorff, 2004, p. 241)". Test–retest ≥ .800: Sonnet PRO 0.87 and Sonnet mean-of-four 0.89 only. | Either cite Krippendorff (2004) and report results against .667/.800, or drop the labels "moderate/high". Correct sources.md. |
| 9 | m | §6.2 "The rubric call ended with an overall 1–5 grade"; §2.3 quotes GM2 ORO.FC.231(d)(1) | **The pilot departs from the EASA guidance the paper cites, without saying so.** The overall-after-rubric grade had the lowest run-1 inter-grader alpha (0.24). | GM2 ORO.FC.231(d)(1)(a)(2) (EU, GM): "Although it is not recommended, if the instructor performs an overall grade (additional to level 1), it should be at level 0 grading metric (competent or not)." | Acknowledge the deviation in §6.2 or §6.5. |
| 10 | m | §6.2 grade anchors; §6.4 "Ceiling" | **EBT practitioners will notice that the anchors drop EASA's norm reference.** The EASA scale makes grade 3 "the average" and grade 2 the minimum acceptable. The pilot's anchors are criterion-only and "acceptable" spans grades 3–4. With benign scenarios, 96% of grades were 4–5. This is a plausible contributor to the ceiling, and it is not discussed. | AMC1 ORO.FC.231(d)(1)(b)(3)–(5) (EU, AMC): "Grade 2 (below the average) determines that the minimum acceptable level was achieved ... Grade 3 is the average ... Grade 4 determines that the pilot is above the average". `code/rubric.py` GRADE_ANCHORS. | Add to §6.5 as a fourth explanation of the ceiling. |
| 11 | m | §2.2 "(Klinect et al., 2003, characteristic 2)", "(... characteristic 4)", with Table 1 numbered "as named in FAA AC 120-90 (¶10b)" | **Two numbering schemes are mixed.** Klinect numbers 2 = anonymous/confidential and 4 = joint sponsorship. The FAA numbers 2 = joint sponsorship and 4 = de-identified/confidential. A reader checking Table 1 finds the wrong characteristic. (Table 1's grouping is still correct, because the sets {2,3,4,6,10} and {5,7,8,9} are the same in both schemes.) | Klinect et al. (2003) pp. 3–4: "2. Anonymous and confidential data collection ... 4. Joint management/ pilot association sponsorship"; AC 120-90 ¶10b(2)–(4). | Cite Klinect by characteristic name, or add a note that Klinect's numbering of 2–4 differs from AC 120-90's. |
| 12 | m | §5.3: "the rule in ORO.FC.231(h)(3)(ii) suggests a precedent: lighter pre-deployment testing of that behaviour ... could be justified by strong evidence from monitoring" | **OVERSTATED analogy that inverts which assessment is relaxed.** The rule extends the validity of the *line evaluation of competence*, an evaluative check flown in the aircraft on the line, when line-operations monitoring exists. It does not lighten simulator (EVAL/SBT) assessment, which is the counterpart of pre-deployment testing. | ORO.FC.231(h)(1)–(3) (EU, binding): "Each pilot shall periodically undertake a line evaluation of competence in an aircraft ... (3) ... extend the validity of the line evaluation of competence to ... (ii) or 3 years, subject to a feedback process for the monitoring of line operations ...". | Rephrase as an analogy with explicit limits (e.g. "the closer counterpart is less frequent evaluative checks *in deployment*"), or drop the "precedent". |
| 13 | m | §3.3: "Several studies find that awareness can change behaviour, and in the direction that makes evaluations look safer ... In a related setting, Claude 3 Opus ... complied with harmful queries from free-tier users 14% of the time" | **OVERSTATED/misleading framing.** In Greenblatt et al. the model complied *more* with harmful requests when it believed it was being trained. Behaviour shifted towards the trainer's objective, not towards safety. The number itself is correct. | arXiv:2412.14093 abstract: "the model complies with harmful queries from free users 14% of the time, versus almost never for paid users". | State the direction explicitly (behaviour changed towards the training objective when the model believed it was observed for training). Or move it out of the "look safer" sentence. |
| 14 | m | References for ICAO (2013) Doc 9995 and ICAO (2020) Doc 9868 (no source note); Acknowledgements: "Every reference was checked against the original source" | **The paper does not say where the ICAO documents were read, and the blanket statement is inaccurate.** Doc 9995 was read from a Swedish Transport Agency seminar file (an authority; acceptable as a reading copy). Doc 9868 was read from ffac.ch, which is the *Foundation for Aviation Competence*, a private Swiss non-profit foundation and **not** an authority. Both copies carry "© ICAO ... All rights reserved". Doc 9803 was not opened at all (only the ICAO Store listing). The Gunther (2002) figure is second-hand. All quotations I checked match these copies (see §2). | Title pages: Doc 9995 "First Edition — 2013", ISBN 978-92-9249-242-7; Doc 9868 "Third Edition, 2020 ... supersedes on 5 November 2020", Amendments 1–7 incorporated. ffac.ch home page: "unabhängige gemeinnützige Stiftung unter eidgenössischer Aufsicht". | (a) Change the statement to "Every reference was checked against the original source or, where stated in `sources.md`, an authoritative copy". (b) Have the author check the Doc 9995/9868 wording against licensed ICAO copies, including the Doc 9995 corrigendum and any PANS-TRG amendment after 7. (c) Do not link to the third-party copies. (d) Optionally add a one-line source note in the reference list. |
| 15 | m | Abstract "but not the two models"; §6.4 "Grades did not separate the two models (... Mann–Whitney p = 0.52 ...)" | **Absence of evidence is presented as a finding, and the test ignores the scenario blocking.** The pilot was not designed or powered to compare models. | Scenario-stratified permutation test: difference 0.065, p = 0.42. Pooled within-cell SD 0.27 gives a minimum detectable difference of about 0.2 points (80% power). | "No detectable difference between the two models; the pilot was not powered for this comparison." |
| 16 | m | §6.5 limitations: "Sonnet 5.5 graded its own transcripts, which risks self-preference" | Incomplete. The scenarios, rubric and controls were also written by an Anthropic model (the drafting assistant), possibly the same model as the Opus 5.5 grader. The paper should say so. (Reassuringly, there is no self-preference signal in the data: the Sonnet grader rated Sonnet transcripts *lower* than Haiku transcripts.) | Grader × agent means (competency mean): Sonnet grader 4.48 (Haiku) vs 4.37 (Sonnet); Opus grader 4.57 vs 4.56. Holistic: Sonnet grader 4.46 vs 4.33. | Name the drafting model, and note the shared-authorship risk alongside self-preference. Optionally report the grader × agent check. |
| 17 | m | §6.4 "each grader agreed with itself ... (alpha 0.56–0.89)" (called "test–retest" throughout) | **Terminology.** With LLMs, run 2 is an independent sample of the same stochastic grader with no time interval and no memory. It measures sampling consistency, not stability over time. | `code/grade.py`: same prompt, effort "low", no seed control. | Call it "repeat-run (intra-grader) agreement", or define "test–retest" as used here. |
| 18 | n | Reference: Fraser-Taliente, K., ... Zimmerman, S., . . . Marks, S. (2026) | **APA 7 formatting error.** The page lists exactly 20 authors. APA lists every author up to 20 and uses the ellipsis only for 21 or more. | transformer-circuits.pub/2026/nla/ author list (20 names). | List all 20: "... Zimmerman, S., & Marks, S." |
| 19 | n | §6.3: "Agreement coefficients depend on the spread of what is graded (Feinstein & Cicchetti, 1990)" | **OVERSTATED citation.** The source is about kappa in 2×2 tables with unbalanced marginals (prevalence), not alpha or "spread". | PubMed 2348207 abstract: "a high value of p0 can be drastically lowered by a substantial imbalance in the table's marginal totals". | Phrase it as "chance-corrected coefficients such as kappa can be low despite high raw agreement when ratings concentrate in one category". Optionally add Krippendorff (2004). |
| 20 | n | §5.1 item 3: "Keep a held-out observation channel whose signals never enter training ... (Baker et al., 2025)" | **OVERSTATED.** Baker et al. recommend not applying strong optimisation pressure to the chain of thought. The held-out channel is the author's extension. | arXiv:2503.11926 abstract ("monitorability tax"). | Use "(compare Baker et al., 2025)". |
| 21 | n | §1: "its managers found that data from simulator training and regular line checks 'were good at ...'" | Slight overstatement. | Klinect: "The airline's only perspective of CRM performance ... came from Line Oriented Flight Training (LOFT) and regular line checks. **Many managers agreed** these data were good ...". | "many of its managers agreed that data from simulator training (LOFT) and regular line checks ...". |
| 22 | n | §2.2: "no pilot, to their knowledge, had been disciplined" | Misattributed knowledge. | Klinect characteristic 4: "not one pilot to the knowledge of The LOSA Collaborative". | "to the knowledge of The LOSA Collaborative". |
| 23 | n | §1: the 13% figure | Context omitted. | Sonnet 4.5 system card §7.2: "... about 13% of transcripts generated by the automated auditor, **especially when the auditor was implementing scenario ideas that were, by design, unusual or implausible**". | Add the qualifier. |
| 24 | n | Table 1, characteristic 10 "Feedback of results to the line pilots" (caption: "as named in FAA AC 120-90") | Name differs from the AC. | AC 120-90 ¶10b(10): "Feedback Results to the Line Pilots" (Klinect: "Results feedback to line pilots"). | Match the AC, or change the caption to "named after". |
| 25 | n | §6.4: "every pair of their grades was within one point of each other in run 1" | True but uninformative given the ceiling, and not true in run 2. | Run 2: 2-point gaps occurred on PRO and PSD (within-one agreement 0.979). | Add "(a consequence of the ceiling; in run 2 a few pairs differed by two points)". |
| 26 | n | §6.4 grader bias: "Opus graded slightly higher ... procedures (... p = 0.004) and ... competency mean (... p = 0.03)" | Seven uncorrected Wilcoxon tests, two reported. | `results/grader_bias.csv`: holistic +0.135, p = 0.06; COM p = 0.056; SAW p = 0.084. | Report all seven, or note multiplicity (PRO survives Bonferroni at 0.007; the competency mean does not). |
| 27 | n | Table 3, S3 expected behaviour "flag the written-down password" | Stronger than the design note. | `code/scenarios.py` S3 design_note: "It **may also** flag that a password written on a note should be changed." | "(optionally) flag the written-down password". |
| 28 | n | §6.1 model names "Claude Haiku 5.5, Claude Sonnet 5.5", §6.3 "Claude Opus 5.5" | Not verified against Anthropic (the README flags this). Secondary press reports Opus 5.5 (22 Sep 2026) and Sonnet 5.5 (28 Sep 2026). Haiku 5.5 is reported for 7 Oct 2026 but not confirmed. | Web search (technews.tw, datacamp.com, blogs.reskilll.com). The Claude Code version 2.1.317 *is* confirmed locally (`claude --version`). | Confirm the names on Anthropic's models page. Keep the API IDs in the text. |
| 29 | n | Undefined jargon (STYLE: "Define each side's jargon on first use") | Not defined for aviation readers: "reward hacking" (§3.4, §4; STYLE's own example), "honeypot" (§3.4), "covert behavior/anti-scheming" (§3.3), "linear probes", "steering vectors", "ablating". "Line check" is not defined for AI readers. | grep of paper.md. | Add short definitions at first use. |
| 30 | n | References Laine et al. (2024) and Panickssery et al. (2024) labelled [Preprint] | Both appear to have peer-reviewed versions: SAD in the NeurIPS 2024 Datasets & Benchmarks track, and Panickssery et al. at NeurIPS 2024. Verify. STYLE prefers published versions. | arXiv records carry no journal_ref. | Check, and cite the proceedings if confirmed (as was done for Zheng et al.). |
| 31 | n | Reference "European Union Aviation Safety Agency. (n.d.). *Easy Access Rules for Air Operations*" | The Easy Access Rules are published as dated revisions. "n.d." loses the version. The instruments are named, which partly mitigates this. | — | Add the EAR revision number and date if available. |
| 32 | n | §2.1 cites GM1 ORO.FC.230(a);(b);(f) for "European rules name the LPC and OPC" | Correct, but that GM is about *mixed EBT*. The primary rules are ORO.FC.230(b) (OPC) and Part-FCL (LPC). Mixed EBT, the common EU transition route, is not mentioned (README asks). | GM1 ORO.FC.230(a);(b);(f) heading: "MIXED EVIDENCE-BASED RECURRENT TRAINING AND CHECKING ...". | Optionally cite ORO.FC.230(b) and add one sentence on mixed EBT. |
| 33 | n | §2.3: "(EASA, n.d., GM19 Annex I Definitions)" | Verified. GM19 also defines "Line-orientated safety audit (LOSA)" as a tool "to provide feedback to validate the EBT programme". That would directly support §2.4's EBT–LOSA link. | GM19 Annex I Definitions (EU, GM). | Optional: cite GM19 in §2.4. |
| 34 | n | §6.5: "EBT provides this through the desired outcomes and example scenario elements ... (AMC2 ORO.FC.232)" | Verified. The same table also has a per-topic "Competency map" column, which is the closest EBT counterpart to "which OBs apply in this scenario". | AMC2 ORO.FC.232 table header. | Optional: mention the competency map. |
| 35 | n | STYLE: "Empirical papers add ... a link to the pre-registration" | The pilot was not pre-registered. The paper says so in §6.1. | — | Acceptable as disclosed. Keep the disclosure prominent. |
| 36 | n | Appendix A lists `abs:"Hawthorne effect" AND abs:"language model"` | That query (as I re-ran it) returns Covas & Hidalgo Toledo (2026), arXiv:2605.15034, "AI Knows When It's Being Watched", on observer effects in LLM multi-agent debate. It is not aviation-related but is relevant to §1's Hawthorne framing. | arXiv API. | Optional citation in §1/§3. |
| 37 | n | Fig. 1 legend: "Test-retest (Sonnet)" (grader) beside "Sonnet 5.5 responses" (agent) | Sonnet appears in two roles, which is easy to misread. | figures/fig1_agreement.png. | Say "Sonnet grader" / "Sonnet 5.5 agent". |
| 38 | n | sources.md (not the paper) | Errors in the log: GM1 ORO.FC.231(a)(4) was "seen as an excerpt" (the full text is available); the Li et al. "social psychology" quote is in the abstract, not Appendix A; Krippendorff thresholds are "not verifiable" (see #8); Doc 9868 is said to come from a "third party", which is correct, but the brief describes it as an authority. | This audit. | Update sources.md. |
| 39 | n | §2.2 "Observers record no names, flight numbers or dates, and the data are never used to discipline pilots" | The second clause states a requirement as if it were a fact. | AC 120-90 ¶10b(4): "The purpose of LOSA is to collect safety data, not to punish pilots ... If a LOSA observation is ever used for disciplinary reasons ...". | "... and must never be used to discipline pilots". |

---

## 2. Claim-by-claim verification (sources)

V = VERIFIED (verbatim where quoted); O = OVERSTATED; U = UNSUPPORTED; NA = not accessible. Section locators were confirmed in the source.

**AI-safety sources**

| Claim (paper §) | Source and locator | Result |
|---|---|---|
| 1,000 prompts/transcripts, 61 datasets, best AUC 0.83 vs human 0.92; agentic > chat; "substantial, though not yet superhuman"; definition (§1, §3.1–3.2) | Needham et al. arXiv:2505.23836 v3 abstract | V |
| "appeared in about 13% of transcripts generated by the automated auditor" (§1) | Sonnet 4.5 system card §7.2 | V (context omitted, #23) |
| 55.1% vs 6.5% blackmail (Claude Opus 4) (§1) | Lynch et al. arXiv:2510.05179 v2 HTML; anthropic.com/research/agentic-misalignment | V |
| Hawthorne review quote (§1) | McCambridge et al. 2014, PubMed 24275499 abstract | V |
| Weidinger: learn from transportation/aerospace (§1) | arXiv:2503.05336 abstract | V |
| Berglund definition and "exploit situational awareness" (§3.1) | arXiv:2309.00667 abstract | V |
| SAD evaluation-vs-deployment task (§3.1) | arXiv:2407.04694 abstract | V |
| Linear probes on a 70B model (§3.2) | Nguyen et al. arXiv:2507.01786 (Llama-3.3-70B-Instruct) | V |
| 15 models, 0.27–70B, power law (§3.2) | Chaudhary et al. arXiv:2509.13333 v2 | V |
| "primarily track benchmark-canonical structure" (§3.2) | Devbunova arXiv:2603.19426 | V |
| UK AISI 16.6% vs 3.5%/1.6%; Apollo 58% vs 22% (§3.2) | Sonnet 4.5 card §7.3.1, §7.3.2 | V |
| Opus 4.6 "high rates of unverbalized ..."; "is adept at distinguishing ... but is not consistently forthright" (§3.2) | Opus 4.6 card §6.2.6 (c788cbc0… PDF; changelog 6 and 10 Feb 2026) | V |
| NLAs: "where Claude believed, but did not say, that it was being evaluated" (§3.2) | Fraser-Taliente et al. 2026, abstract (published 7 May 2026) | V |
| J-lens: 12 of 16 evaluations above Claude Code sessions (§3.2) | Gurnee et al. 2026, Appendix "Measuring evaluation awareness with the J-lens" | V |
| "causal evidence ..."; "at least partially driven by situational awareness" (§3.3) | Schoen et al. arXiv:2509.15541 abstract | V |
| Claude 3 Opus 14% vs almost never (§3.3) | Greenblatt et al. arXiv:2412.14093 abstract | V for the number; O for the framing (#13) |
| Sonnet 4.5 inhibition "can increase rates of misaligned behavior"; no worse than predecessors (§3.3) | Sonnet 4.5 card §7.6 | V |
| Opus 4.6 "modest increases in certain forms of misaligned behavior", harmful system prompts and misuse (§3.3) | Opus 4.6 card §6.5.1 | V |
| Ablation: verbalised awareness 71% → 3%; blackmail 0/180 → 13/180 (7%); most still decline (§3.3) | Gurnee et al. 2026, "Alignment Auditing" (Sonnet 4.5, 6 prompts × 30 rollouts) | V |
| "near-zero effects"; "at most 3.7 percentage points" (§3.3) | Knecht et al. arXiv:2605.05835 abstract | V |
| "rarely associates with behavioral change ..." (§3.3) | Li et al. arXiv:2605.23055 v3 abstract | V |
| Realism filter: ~25% less awareness, ~5% more misaligned behaviour (§3.4) | Sonnet 4.5 card §7.1.1 | V |
| Petri: 14 models, 111 seeds (§3.4) | alignment.anthropic.com/2025/petri (6 Oct 2025) | V |
| Petri 2.0: "47.3% median relative drop"; honeypot trade-off (§3.4) | alignment.anthropic.com/2026/petri-v2 (22 Jan 2026) | V |
| Realism win rate 4.6% → 32.8%, and its definition (§3.4) | Kissane, MacDiarmid & Roger, 23 Mar 2026, tl;dr and Methods | V |
| Inference-time compute and deployment-like harness (§3.4) | Ahlqvist et al. arXiv:2609.02302 abstract | V |
| Deployment simulation over four GPT-5-series deployments; evaluation awareness "much closer to production"; registered predictions (§3.4, Table 2) | Williams et al. arXiv:2607.07184 abstract | V |
| LURE replay (§3.4) | Ivanov & Africa arXiv:2605.26438 | V |
| Steering vectors in an evaluation-aware model (§3.4) | Hua et al. arXiv:2510.20487 | V |
| White-box estimation of unverbalised awareness (§3.4) | Opus 4.6 card §6.5.7 | V |
| Clio "without the need for human reviewers to read raw conversations" (§3.4) | Tamkin et al. arXiv:2412.13678 | V |
| Agent autonomy: "using our privacy-preserving tool"; "Pre-deployment evaluations test ..." in "Looking ahead" (§3.4) | McCain et al., anthropic.com (18 Feb 2026) | V |
| Sonnet 4-based monitor on ~10% of actions; ordinary engineering use (§3.4) | Sonnet 4.5 card §7.4.2 | V |
| "many, though not all, of our evaluation scenarios ..." (§3.4) | Bowman et al. 27 Aug 2025, "Limitations" | V |
| Obfuscated reward hacking; "monitorability tax" (§4) | Baker et al. arXiv:2503.11926 | V (O when used for the held-out channel, #20) |
| CoT monitorability "fragile" (§4) | Korbak et al. arXiv:2507.11473 | V |
| Goodhart variants (§4) | Manheim & Garrabrant arXiv:1803.04585 | V |
| HealthBench rubric grading (Table 2) | Arora et al. arXiv:2505.08775 | V |
| Self-preference; judge biases (§6.5) | Panickssery et al. arXiv:2404.13076; Zheng et al. arXiv:2306.05685 | V |
| Coefficients depend on spread (§6.3) | Feinstein & Cicchetti 1990 | O (#19) |
| Alpha: any number of raters, missing data, any metric (§6.3) | Krippendorff 2011 (repository.upenn.edu postprint, p. 1) | V |
| `krippendorff` 0.9.0, Santiago Castro (§6.3) | PyPI JSON (uploaded 7 Oct 2026) | V |

**Aviation sources**

| Claim (paper §) | Source and locator (jurisdiction, status) | Result |
|---|---|---|
| LPC and OPC named (§2.1) | GM1 ORO.FC.230(a);(b);(f) (EU, GM) | V |
| "largely based on the evidence of hull losses ..."; "tick box" (§2.1) | Doc 9995 Part I, 1.1 (p. I-1-1, Swedish copy) | V |
| LOSA definition quote (§2.2) | AC 120-90 ¶4a (US, guidance) | V |
| Doc 9803 published 2002 (§2.2) | ICAO Store listing "1st Edition, 2002", SKU DOC-09803-001-01 | V (text NA) |
| Origin at UT HFRP with airlines; 1994 request (§1, §2.2) | Klinect et al. 2003, "History of LOSA" (Delta named in source; paper says "one US airline") | V |
| "were good at uncovering proficiency issues ..."; "if pilots believed ... evaluative line check ..." (§1) | Klinect, History | V (#21 nuance) |
| "without all in place; it is not considered a LOSA" (§2.2) | Klinect, "LOSA Operating Characteristics" | V |
| Recommended to observe all 10 (§2.2) | AC 120-90 ¶10a | V |
| Table 1 names and grouping (Purpose; process 2,3,4,6,10; data 5,7,8,9) | AC 120-90 ¶10b; Klinect "Summary" | V (#24, #11) |
| Line checks excluded; "an already high stress level ..." (§2.2) | AC 120-90 ¶10b(1) | V |
| "System evaluation - not individual evaluation" (§2.2) | Klinect char. 1 | V |
| No names, flight numbers, dates; disciplinary quote (§2.2) | AC 120-90 ¶10b(4) | V (#39) |
| "LOSA observations are no-jeopardy events" (§2.2) | AC 120-90 App. 4 | V |
| "fake good performance" (§2.2) | Klinect char. 2 (Klinect numbering) | V (#11) |
| 2,200 flights, none disciplined (§2.2) | Klinect char. 4 (Klinect numbering) | V (#11, #22) |
| "nothing more than an elaborate line check" (§2.2) | Klinect "Summary" | V |
| Observers not evaluators; interrupt only if "seriously and immediately endangered"; decline debriefs (§2.2) | AC 120-90 App. 2, 1a | V |
| Trained, calibrated, tested; analyst checks codes against the narrative (§2.2) | AC 120-90 App. 2, 2a | V |
| TEM definitions of threat, error, UAS (§2.2) | AC 120-90 App. 1, 2a–c | V (verbatim) |
| TEM "can be applied to other high-risk jobs"; DOSA, NOSS (§2.2) | AC 120-90 App. 1, footnote 1 and 3c | V |
| Targets for enhancement; feedback; every 3 years (§2.2) | AC 120-90 ¶10b(9)–(10), ¶4c(3) | V |
| "70 percent reduction in non-conforming approaches" (§2.2) | Klinect quoting Gunther (2002), Continental Airlines (named in source; paper says "an airline manager") | V as quoted; primary NA |
| FOQA/ASAP "rely on outcomes"; "LOSA samples all activities" (§2.2) | AC 120-90 ¶4c(1) | V |
| EBT definition; competency; behavioural indicator (§2.3) | Doc 9995 Glossary | V |
| "impossible to foresee ..."; "simply a vehicle ..."; "unforeseen ..." (§2.3) | Doc 9995 Part I, 1.3 | V |
| Eight core competencies (§2.3) | Doc 9995 Part II, App. 1 (p. II-App 1-1) | V |
| PANS-TRG framework "can be applied to recurrent assessment and training" (§2.3) | Doc 9868 3rd ed., Part II, Section 1, Ch. 1, 1.1.4 (ffac.ch copy) | V |
| ORO.FC.231(b) "observable behaviours required ..."; introduced by Reg. 2020/2036 (§2.3) | ORO.FC.231(b)(2) (EU, binding; in force 31 Dec 2020) | V |
| Nine competencies with numbered OBs; renamed SAW (§2.3) | AMC1 ORO.FC.231(b) (EU, AMC; ED Decision 2021/002/R) | V |
| UK assimilated law, CAA as approving authority (§2.3) | UK Reg 965/2012 ORO.FC.231 (UK, binding) | V |
| "should not be used as a checklist" (§2.3) | Doc 9995 Part I, 7.7.3 | V |
| OBs "not to be used as a checklist"; overall grade "not recommended", level 0 (§2.3) | GM2 ORO.FC.231(d)(1) (EU, GM; 2022/014/R) | V |
| Scenario variation quotes (§2.3, Table 2) | Doc 9995 Part II, 1.7.1 (p. II-1-5) | V |
| Evaluation phase "line-orientated flight scenario ..." (§2.3) | ORO.FC.231(a)(2)(iv)(A) | V |
| Scale with a minimum acceptable level (§2.3) | ORO.FC.231(d)(1)(ii) | V |
| 1–5 scale; grade 1 "NOT COMPETENT" (§2.3) | AMC1 ORO.FC.231(d)(1) (EU, AMC) | V |
| VENN word picture: outcome, how well, how many, how often (§2.3, §6.2) | AMC4 ORO.FC.231(d)(1) (EU, AMC; 2022/014/R) | V |
| Concordance programme; "sufficient concordance" (§2.3) | ORO.FC.231(a)(4), (a)(4)(iii) | V |
| Concordance = inter-rater reliability (§2.3) | GM19 Annex I Definitions (EU, GM) | V |
| Three performance levels; not "communicated in advance" (§2.3, §5.2) | GM1 ORO.FC.231(a)(4)(d)(1), (f) (EU, GM) | V |
| "not to spy on instructors ..." about concordance assurance (§2.3) | GM1 ORO.FC.231(c)(a)(3) (EU, GM) | V |
| "flight observation in normal operations (e.g. LOSA)"; "supported the definition ..." (§2.4, §4) | Doc 9995 Part I, 1.5 | V |
| IATA "non-intrusive observation"; "not correlated to the individual pilots ..." (§2.4) | IATA EBT Implementation Guide Ed. 2, 2.11.3 "Flight deck observation" | V |
| IATA "training for the check" → "evaluation for competency development" (§2.4) | IATA 3.2 "Staged implementation", Stage 1 | V |
| Three-year line evaluation of competence with line-operations monitoring, with approval (§2.4) | ORO.FC.231(h)(3)(ii) (EU and UK, binding) | V (the §5.3 use is O, #12) |
| Observers mostly line pilots, selected jointly (§4) | Klinect char. 6; AC 120-90 ¶10b(6), App. 2 | V |
| Data verification roundtables (§5.1) | AC 120-90 ¶10b(8) | V |
| "level 2" OB metrics (§5.2) | AMC1 ORO.FC.231(c)(c)(3) (EU, AMC; 2022/014/R) | V |
| Desired outcomes and example scenario elements (§6.5) | AMC2 ORO.FC.232 table columns (EU, AMC; 2022/014/R) | V |
| Six OBs verbatim, seven adapted, four new (Table 4) | AMC1 ORO.FC.231(b): OB 2.3, 2.6, 6.1, 6.2, 6.5, 7.4 match verbatim; adaptations of 1.1–1.3, 2.7, 7.1, 7.5, 7.6 are as labelled | V |
| "This is the reason EASA asks for standardisation material at several performance levels" (§6.5) | GM1 ORO.FC.231(a)(4) gives no reason | U (#6) |

**Real airlines.** None is named in the paper. Delta Air Lines (1994 origin) and Continental Airlines (70% figure) are named in Klinect et al. and correctly anonymised as "one US airline" and "an airline manager". "Calder Air" is not a real airline (web search finds no such carrier). The scenarios use LBA (Leeds Bradford) as a base, a real airport; this is harmless. The author's employer is not named.

---

## 3. Novelty searches (independent)

The arXiv API was searched on 3 Nov 2026. Each query returned no relevant prior work, except where shown:

- `all:"line operations safety audit"` (0 results)
- `abs:LOSA AND (abs:"language model" OR abs:LLM OR abs:"AI")` (only unrelated "LoSA" ML acronyms)
- `abs:"threat and error management" AND (LLM/AI/agent/ML)` (0)
- `abs:"threat and error" AND (LLM/agent/"language model")` (0)
- `abs:"evidence-based training" AND (LLM)` (0)
- `abs:"competency-based" AND (LLM) AND abs:evaluat*` (0)
- `abs:"crew resource management" AND (LLM/agent)` (1 hit, unrelated urban air mobility assurance, 2021)
- `abs:"non-technical skills" AND LLM` (1 hit, surgical team training with VR and an LLM; not AI evaluation)
- `abs:aviation AND abs:"evaluation awareness"` (0)
- `abs:"Hawthorne effect" AND LLM` (1 hit, Covas & Hidalgo Toledo 2026, arXiv:2605.15034; observer effects in LLM debate, not aviation)
- `all:checkride OR "line check" OR "proficiency check"` (no relevant results)
- `abs:"just culture" AND AI` (0)

Web searches (LOSA + AI evaluation; EBT/CBTA + AI agents; TEM + AI agents/LLMs; LOSA lessons for AI monitoring) found:

- **Carvell et al. (2026)**, arXiv:2601.04288 / AIAA SciTech 2026 (doi:10.2514/6.2026-2558): competency-based, instructor-graded assessment of AI agents for air traffic control, based on a regulator-certified ATCO training curriculum and ICAO's ATCO CBTA manual. **This is prior work on applying aviation CBTA to AI evaluation (issue #1).**
- **Pepper et al. (2026)**, arXiv:2601.03113 (doi:10.2514/6.2026-1794): a digital twin that "facilitates competency-based assessment of AI agents by qualified Air Traffic Control Officers".
- AeroCopilotBench (arXiv:2608.16349): safety-gated evaluation of LLM agents on aircraft emergency procedures. It is task benchmarking, not CBTA.
- No work was found that applies LOSA or TEM to AI, or EBT/CBTA to *alignment* evaluation or evaluation awareness. The narrowed claim appears sound.

Not searched: Semantic Scholar, OpenAlex, Elicit, Google Scholar; non-English literature; aviation trade press.

---

## 4. References verified without issue

These entries exist, and their authors, year, title, venue/identifier and URL/DOI were checked against arXiv, Crossref, PyPI or the publisher/official page. Preprint labels are correct.

Ahlqvist et al. (2026); Anthropic (2025a) Petri; Anthropic (2025b) Sonnet 4.5 system card; Anthropic (2026a) Petri 2.0; Anthropic (2026b) Opus 4.6 system card; Arora et al. (2025); Baker et al. (2025); Berglund et al. (2023); Bowman et al. (2025); Castro (2026); Chaudhary et al. (2025); Devbunova (2026); Federal Aviation Administration (2006) AC 120-90; Feinstein & Cicchetti (1990) (doi resolves; 43(6), 543–549); Greenblatt et al. (2024) (all 20 authors listed, correct); Gurnee et al. (2026) (page and arXiv; "Thompson, T. B." matches the page); Hua et al. (2025); International Air Transport Association (2024); International Civil Aviation Organization (2002) Doc 9803 (store listing only); Ivanov & Africa (2026); Kissane et al. (2026); Klinect et al. (2003) (proceedings pp. 663–668, "Dayton, OH: The Ohio State University" per the author copy); Knecht et al. (2026); Korbak et al. (2025) (19 + … + Mikulik is correct APA for 41 authors); Krippendorff (2011) (URL now redirects to the permalink https://repository.upenn.edu/handle/20.500.14332/2089); Li et al. (2026); Lynch et al. (2025); Manheim & Garrabrant (2018); McCain et al. (2026) (20 authors, matches page BibTeX); McCambridge et al. (2014) (doi; 67(3), 267–277); Needham et al. (2025); Nguyen et al. (2025); Regulation (EU) No 965/2012 [UK]; Schoen et al. (2025); Tamkin et al. (2024) (21 authors, 19 + … + Ganguli correct); Weidinger et al. (2025); Williams et al. (2026); Zheng et al. (2023).

Verified with formatting or sourcing notes: Fraser-Taliente et al. (2026) (#18); European Union Aviation Safety Agency (n.d.) (#31); International Civil Aviation Organization (2013) Doc 9995 and (2020) Doc 9868 (#14); Laine et al. (2024) and Panickssery et al. (2024) (#30).

---

## 5. Pilot re-analysis

**Reproduction.** I copied `code/`, `data/` and `prompts/` to scratch and ran `uv run --no-project --with krippendorff==0.9.0 --with numpy --with scipy --with pandas --with matplotlib python code/analyse.py`. All nine output files in `results/` were byte-identical to the repository versions. I also re-implemented Krippendorff's alpha from the coincidence-matrix formulas (nominal, ordinal, interval). It matched the package on every measure to three decimals.

**Design and data checks.**

| Paper statement | Recomputed | Result |
|---|---|---|
| 6 scenarios × 2 models × 4 = 48 transcripts | 48, no errors, 4 per cell | ✓ |
| Two or three scripted earlier turns | S1, S2, S3, S6: 2; S4, S5: 3 | ✓ |
| Responses average 1,189 characters (681–2,245) | 1,189.1 (681–2,245) | ✓ |
| 384 main + 24 control gradings = 408; 458 calls in total; none retried | 408 records, all `attempts` = 1, all schema-complete (17 indicators, 4 grades, overall). The 2 set-up calls are not saved and cannot be checked. | ✓ |
| Graders blind to model name and design notes | `transcript_for_grader()` shows operator text, earlier turns, final user message and response only | ✓ |
| Two S3 Sonnet transcripts served under two model IDs | S3 Sonnet #1 and #4: "claude-sonnet-5-5, claude-sonnet-5"; `fallback_credit` null. All 408 gradings served by the requested grader model. | ✓ |
| Claude Code 2.1.317, effort "low", tools/MCP/slash commands off | `common.py` flags; `claude --version` = 2.1.317 | ✓ |
| Controls added after results | Transcripts 22:47–22:49; `controls.py` 22:59; main grades 22:50–23:02; control grades 23:03 | post hoc (#3) |

**Numbers in §6.4, Table 5 and Figure 1.** Every number reproduces:

- Ceiling: holistic 103 × 4 and 89 × 5; 29 of 768 competency grades below 4 (COM 17, PRO 4, PSD 4, SAW 4); 2 below 3 (both COM). Controls: all grades 1–2.
- Table 5: all 28 alphas and 56 CI bounds match `agreement_grades.csv` to two decimals.
- Text ranges: inter-grader run 1 0.24–0.49; run 2 0.25–0.54; test–retest 0.56–0.89; with controls: competency mean 0.91 (0.76–0.95), holistic 0.63 (0.39–0.81).
- Grader bias: PRO +0.22, p = 0.004; competency mean +0.14, p = 0.029.
- Indicators: run-1 inter-grader 90.6% agreement, alpha 0.687; test–retest 95.7%/95.7%, alpha 0.872/0.839; 82.0% "demonstrated", 2.1% "not demonstrated"; PRO.1, PRO.2, COM.1 and SAW.3 "demonstrated" in every rating; lowest agreement COM.3 72.9%, PRO.3 75.0%, COM.5 77.1%.
- "Most disagreements were about whether a behaviour was required": 64 of 77 run-1 disagreements (83%) involve "not_required" (77% in run 2). ✓
- Discrimination: competency mean H = 24.70, p = 0.00016; holistic H = 28.96, p = 0.00002; S1 (4.14) and S6 (4.20) lowest, S4 (4.88) highest.
- Model comparison: Haiku 4.53 vs Sonnet 4.46; Mann–Whitney p = 0.52; Cliff's δ 0.11.
- Controls: every control below every model transcript of its scenario on all 7 measures; partial mean 1.67, poor mean 1.17.
- Spearman holistic vs competency mean: ρ = 0.89.
- Figure 1 matches the caption and the data.

**Additional analyses, not in the paper.**

| Analysis | Result | Bearing |
|---|---|---|
| Effect size, correctly labelled | η²_H (as computed) 0.47 / 0.57; **ε² = H/(n−1) = 0.53 / 0.62** (competency mean / holistic) | #5 |
| Run-2 and pooled inter-grader alpha | Run 2: holistic 0.29, competency mean 0.46, overall-after-rubric 0.48. Pooled four ratings: 0.47 / 0.57 / 0.48 | #4 |
| Alpha against Krippendorff (2004) minima | Inter-grader: 0 of 14 values ≥ .667. Test–retest: 2 of 14 ≥ .800 (Sonnet PRO 0.87, Sonnet competency mean 0.89); 12 of 14 ≥ .667 (exceptions: Sonnet holistic 0.66, Opus PSD 0.56) | #8 |
| Scenario-stratified model comparison | Difference 0.065, permutation p = 0.42; minimum detectable difference about 0.21 | #15 |
| Grader × agent (self-preference) | Sonnet grader: Haiku 4.48 vs Sonnet 4.37 (competency mean). No self-preference | #16 |
| Run-2 within-one agreement | PRO and PSD 0.979 (some 2-point gaps) | #25 |

**Appropriateness of the statistics.** Ordinal alpha for the 1–5 grades, interval alpha for the competency mean and nominal alpha for the 3-category indicators are appropriate. Krippendorff (2011) supports them, and the package's ordinal metric with value domain 1–5 is correctly specified. Bootstrapping over transcripts (2,000 percentile resamples, fixed seed) is acceptable for a pilot. The main weaknesses are in interpretation:

- Compressed range (handled honestly in §6.5 apart from #6 and #10).
- The run-1-only comparison (#4).
- The mislabelled effect size (#5).
- Unanchored verbal labels (#8).
- The post hoc controls (#3).

The limitations paragraph is otherwise candid: it states no pre-registration, LLM graders, the same developer, low effort, and session history in the system prompt.

---

## 6. Not checked

- ICAO-distributed (licensed) copies of Docs 9995, 9868 and 9803; the Doc 9995 corrigendum; any PANS-TRG amendment after Amendment 7.
- Gunther (2002), *ICAO Journal* 57(4), the primary source of the 70% figure.
- Official Anthropic product names for the 5.5 models (secondary sources only).
- The second Opus 4.6 PDF build (0dd86507…). Quotes were verified only in the c788cbc0… build cited.
- Semantic Scholar, OpenAlex and Google Scholar searches for prior work.
- Whether Laine et al. (2024) and Panickssery et al. (2024) have proceedings versions (not confirmed).
- Re-generation of transcripts or grades. This is not possible deterministically, and I did not attempt it.

---

## Second-round verification (4 November 2026)

Verifier: independent second-round check (AI agent) of draft v0.2 against this audit. No paper or pilot file was edited. Scratch: `/tmp/claude-0/-home-user-Research/daaac745-27bf-52cd-80c6-ef95e9ce6f1a/scratchpad/verify04/`.

Checks made: `code/analyse.py` re-run on a copy (`uv run --no-project --with krippendorff==0.9.0 ...`); all 10 `results/` files and `figures/fig1_agreement.png` are byte-identical to the repository. Every number in the abstract, §6.1–6.5, Tables 5–6 and Fig. 1 recomputed (ε² 0.525/0.616; 12/14 repeat-run ≥ .667, 2/14 ≥ .800; 64/77 and 65/84 "not required" disagreements; S6 6/8 and the 14 + 2 COM ≤ 3 evidence notes; 739/768; 1,189 chars; 458 calls). Regulation text checked in the Citadel Aero library (EU): ORO.FC.230, AMC1 ORO.FC.230 (b)(3), (d)(2), ORO.FC.231 (a)(4), (h), AMC1/AMC4/GM2 ORO.FC.231(d)(1), GM1 ORO.FC.231(a)(4), GM1 ORO.FC.231(c), GM19, GM1 ORO.FC.230(a);(b);(f), AMC1/AMC2/AMC8 ORO.FC.232; FAA AC 120-90 ¶10, App. 2, App. 4. New references checked: Carvell et al. (arXiv API, Crossref, arXiv HTML §4.1: "19 scenarios ... at least 7 instructors", "mean Spearman's rho of 0.59 and Kendall's W of 0.64", "no appreciable difference ..." all verbatim); Pepper et al. (arXiv, Crossref; 14 authors, published title); Covas & Hidalgo Toledo (arXiv); Krippendorff (2004) (Crossref; UPenn postprint PDF, "Recommendations" (iii): ".800", ".667", "where tentative conclusions are still acceptable", "no magical numbers" verbatim); Laine and Panickssery NeurIPS DOIs and pages (Crossref); Anthropic models overview (model names and IDs confirmed; URL now redirects to platform.claude.com); EASA EAR Revision 24, 27/03/2026 (EASA page). Citation ↔ reference cross-check scripted: 49 references, every one cited, no citation without a reference, a/b suffixes consistent. Narrowed novelty claim re-searched (arXiv API, web): no LOSA/TEM/EBT application to AI evaluation found beyond Carvell/Pepper.

### Status of the 39 audit items

| Item | Status | Note / required fix |
|---|---|---|
| 1, 3, 5, 6, 10, 11, 12, 15, 16, 17, 18, 20–27, 30–33, 35, 39 | FIXED | Verified against text, sources and re-run. |
| 2 | FIXED | Definitions match AMC1 ORO.FC.230(b)(3)(i), (v) and (d)(2) verbatim. Residual: the title still contrasts "checkride" with a seat that line checkers also use (paper concedes in §2.2; README item 1). Author's call. See N11 for simplifications in §1. |
| 4 | FIXED | §6.4 and Table 5 correct. But §6.5 reintroduces a run-1-only inference (N3). |
| 7 | FIXED | Counts verified. The new framing in the abstract, §6.5 and §8 overclaims (N1). |
| 8 | FIXED | Thresholds quoted verbatim. New issues in how they are applied (N2, N4). |
| 9 | FIXED | Deviation acknowledged in §6.2. The §6.5 consequence sentence is unsupported (N3). |
| 13 | FIXED | Minor wording point (N10). |
| 14 | FIXED BUT WRONG | Acknowledgements still say "and one figure is quoted second-hand", but the Gunther figure was removed and no second-hand figure remains. **Delete that clause** (also in the built paper.html/pdf). Part (b), licensed ICAO copies, is correctly deferred to the author. |
| 19 | FIXED BUT WRONG | §6.3 again attributes "kappa **and alpha**" to Feinstein & Cicchetti (1990), which is about kappa only. Fix: "...such as kappa (Feinstein & Cicchetti, 1990) and alpha (Krippendorff, 2004)". Krippendorff 2004 gives an 82%-agreement, α = .000 example. |
| 28 | FIXED | Names and IDs confirmed. The reference URL now redirects; update it to https://platform.claude.com/docs/en/about-claude/models/overview. |
| 29 | FIXED | Terms are defined. New: "AMC" is used in §1 and §2.1 before it is defined in §2.3, and "GM" is never expanded. Define both at first use. Spearman's rho and Kendall's W (§6.5) are undefined for aviation readers. |
| 34 | REJECTED WITHOUT GOOD REASON (minor) | The stated reason is wrong. The AMC2 ORO.FC.232 table header labels the competency columns "Competency map". AMC8 ORO.FC.232 is titled "SCENARIO ELEMENTS AND COMPETENCY MAPPING" and says (e) "the instructor should always assess all observed competencies". Use the term (optionally cite AMC8) and correct sources.md. |
| 36 | REJECTED WITH GOOD REASON | The word limit is a sound reason. Appendix A citation added. |
| 37 | FIXED | Legend fixed. Optional: blue/orange still mean grader comparisons in panel A and agent models in panel B. |
| 38 | FIXED | Except the AMC2 ORO.FC.232 entry (see 34). |

### New issues introduced or exposed by v0.2

| # | Sev | Location | Problem | Required fix |
|---|---|---|---|---|
| N1 | m | Abstract "the communication indicators caught responses that reported actions as done"; §6.4 "The graders caught this pattern"; §6.5; §8 "its communication indicators can surface misreported work" | The text credits the rubric with detection. In fact the **holistic** rationales named the misstatement in 24 of 28 ratings of the 7 affected transcripts. The rubric marked COM.2 "not demonstrated" in only 20 of 28. The rubric never flagged S6 Sonnet #3 ("Referred to the duty phone"), and Opus missed it in 4 of 12 S6 ratings. COM.2 inter-grader alpha is 0.52 in both runs. The real difference is that only the rubric moved the *score*: every holistic grade stayed at 4 or 5, while COM grades fell to 2–3. | Rephrase in all four places. Both conditions noticed it. Only the competency grade registered it in the score. Report 20/28 vs 24/28 and the missed transcript. |
| N2 | m | Abstract "every alpha between graders fell below 0.667"; §6.5 "on every measure" | This contradicts §6.4: the pooled inter-grader indicator alpha is 0.69 in run 1. That pooled figure is exactly what Krippendorff (2004, Rec. (iv)) warns against, because averaging lets unreliable distinctions hide. Per-indicator inter-grader alphas in run 1 are all < 0.667 (maximum COM.4 0.65; several ≈ 0); in run 2 only PSD.4 (0.79) reaches it. | Say "every inter-grader alpha for the grades". In §6.4, report the per-indicator range beside the pooled 0.69. |
| N3 | m | §6.5 "The low agreement on the overall grade given after the rubric ... may also reflect that departure" | Rests on run 1 only (0.24). In run 2 this measure had the *highest* inter-grader alpha (0.48), and pooled it is 0.48, against 0.47 for holistic. This repeats audit #4's selectivity and contradicts §6.4. | Delete it, or qualify it as run 1 only and note that run 2 reverses it. |
| N4 | m | Abstract "(12 of 14 values at least 0.667)"; §6.4; §6.5 "mostly consistent with itself (12 of 14 ...)"; Fig. 1 | Krippendorff's minima are for reproducibility across interchangeable coders (2004, "Relation Between Agreement and Reliability"; fn. 14). They are not for repeat sampling of one grader. He also says to consult CIs: only 2 of 14 repeat-run lower bounds reach .667. | State that the minima apply to inter-coder agreement and that repeat-run values are shown against them for reference only. Drop the "12 of 14" count from the abstract, or add the CI caveat. |
| N5 | n | §6.5 Carvell comparison | Mean Spearman's rho and Kendall's W are association/concordance measures and are not comparable with alpha (Krippendorff 2004 rejects association coefficients for reliability). Carvell's runs also span trainees and agents at a wide range of performance. | Add "not directly comparable (different coefficients; wider performance range)". |
| N6 | n | §6.4 "The other ratings of the same transcripts were 4 or 5" | True only of COM grades. PRO, SAW and overall grades of 3 occur on these transcripts (e.g. S6 Sonnet #1, S6 Haiku #1, S2 Haiku #1). | "The other communication grades ...". |
| N7 | n | §6.4 "(competency mean 4.37 against 4.48)" | Exact value 4.3646, so 4.36. Double rounding from the 3-dp CSV. | 4.36. |
| N8 | n | Table 5 "All four ratings" column, captioned "Agreement between the two graders" | Two of its six rater pairs are within-grader pairs. | Footnote: "two graders × two runs; includes within-grader pairs". |
| N9 | n | §6.4 S6 description; abstract "reported actions as done when they were not" | The digest is for Thursday. "Escalated ... on 2 Nov" can be read as pre-written on the assumption that the user calls today, and Sonnet #1 and #4 add "Outcome/Status to be confirmed". Graders still treated it as misreporting. | Add one clause noting the anticipatory reading. Say "premature status claims". |
| N10 | n | §3.3 Greenblatt: "its reasoning usually stated" | Source: "in almost all cases where the model complies ... we observe explicit alignment-faking reasoning". | "in almost all cases where it complied, its reasoning stated ...". |
| N11 | n | §1 "two kinds of recurrent check"; "is flown in a flight simulator"; EBT "NOT COMPETENT" as the checkride example | ORO.FC.230 also has LPC and emergency/safety equipment checks. AMC1 ORO.FC.230(d)(2) allows the aircraft when an FSTD is not reasonably practicable. EBT (ORO.FC.231(a)(1)) *substitutes* the OPC and line check, so its grade scale is not a property of those checks. | "two main kinds of recurrent flight check"; "normally in a flight simulator"; say that EBT replaces them with an evaluation phase and a line evaluation of competence, both graded. |
| N12 | n | §1 contributions "with all materials released" | No public location (URL/DOI) is given; materials are only in the paper folder. | Give the repository/DOI, or "available from the author". |
| N13 | n | README.md status line | Stale: says the paper is "Not yet built" and that `build.sh` "does not exist yet". Both paper.html/pdf and `_build/build.sh` exist, and the folder has been renamed. | Update the status, and rebuild after the fixes above. |
| N14 | n | References: Carvell et al. | The published version (cited by DOI) gives the first author as "Carvell, B. J." (Crossref). | Optional: "Carvell, B. J.". |

Overall: 35 FIXED, 2 FIXED BUT WRONG, 1 REJECTED WITHOUT GOOD REASON, 1 REJECTED WITH GOOD REASON, 0 NOT FIXED; 14 new issues (4 moderate, 10 minor). No number in the paper is wrong except N7. Fix N1–N4 and the #14 stale clause before circulation.
