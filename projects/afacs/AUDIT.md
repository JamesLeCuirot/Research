# Independent audit: AFACS paper (working draft v0.9, 4 November 2026)

**Auditors:** three independent fact-checkers (Claude, AI-assisted), run in parallel on 4 November 2026. None had written the paper or seen the author's reasoning, and none edited it. Two re-opened every cited source and checked each cited claim, quotation and reference entry (references 1–16 and 17–33). The third traced every number to the repository or recomputed it from the local data, re-checked the claims about MAST and the frameworks against primary sources, and checked the worked examples against the traces. Their full reports follow below. Working copies of the sources and the recomputation scripts were kept in the session scratchpad, not in the repository. No benchmark questions, answers or test data are reproduced here.

**Fixes:** applied to `paper/afacs.tex` and `paper/references.bib` after the audit, with matching corrections in `README.md`, `docs/design_check.md`, `docs/crosswalk_ezell.md`, `results/PILOT_SUMMARY.md`, `docs/GUIDE.md`, `src/afacs/design.py` and `src/afacs/analysis.py`. The bibliography was re-checked with `papers/_build/check_bib.py` afterwards; it shows no mismatches.

## Summary

| Category | References 1–16 | References 17–33 | Numbers and claims | Total |
|---|---|---|---|---|
| VERIFIED | 30 | 16 | 78 | 124 |
| WRONG | 0 | 0 | 7 | 7 |
| OVERSTATED | 6 | 0 | 11 | 17 |
| UNSUPPORTED | 1 | 2 | 2 | 5 |
| INCONSISTENT | – | – | 7 | 7 |
| NOT ACCESSIBLE | 4 books | 1 letter (full text) | 2 | 7 |
| Reference-entry issues | 5 | 4 | – | 9 |

**Overall judgement.** The empirical core holds:
- every kappa value and bootstrap interval reproduced;
- every weighted share reproduced except one, which was mislabelled;
- every number attributed to a cited source was exact;
- all five worked examples matched their traces.

The weak points were of three kinds:
- **Claims of absence about Ezell et al.** The paper said their framework had "no category" for deliberate departures and "has not been applied to real traces". In fact it folds departures into cognitive errors, and it illustrates the framework on one real incident.
- **Statements true of the primary run but not of all three.** The violation-grade pattern, "absent from MetaGPT", and the AppWorld match count.
- **A few stale or wrong facts.** A table row, a token range, a timestamp count, how the Magentic-One version is known, and one design claim counted as confirmed although it put a set-up problem at the design layer.

All were corrected, and the corrections soften the claims without changing the paper's conclusions.

## Resolutions

| ID | Issue (short) | Resolution |
|---|---|---|
| A1-O1 | "no category records such a departure" | Rewritten throughout (abstract, introduction, cross-walk table): Ezell et al. fold deliberate departures into cognitive errors, and nothing distinguishes a violation from an error. |
| A1-O2 | "has not been applied to real traces" | Scoped: illustrated on one real incident from public advisories, without logs; not used to code agent traces as far as this study found. |
| A1-U1 | "the first framework" | "the first" removed. |
| A1-O3 | Wiegmann & Shappell: company records vs flight recorder | Now states only their finding and their two explanations; the flight-recorder line in the Discussion is marked as the author's analogy. |
| A1-O4 | "AFACS adds what kind of act and what latent conditions" | Narrowed: AFACS adds the error/violation distinction with an evidence grade and a layered account; Raj et al.'s specification gaming and harness faults acknowledged. |
| A1-O5 | MAST "has no causal layers" | Reworded: MAST labels failures flatly; its categories and stages do not separate act from conditions, and it notes FM-1.1's mixed causes. |
| A1-O6, B-O11 | "five challenges" merged two items | "limited data access" dropped; the five are listed correctly. |
| A1-R1, R2 | Ezell and Shamsujjoha now formally published | Entries updated (AIES 8(1):865–878; IEEE ICSA 2025, pp. 37–48). |
| A1-R3–R5 | Cosmetic entry notes | MAST note tightened; Leveson note removed; Reason 1997 DOI moved into the note. |
| A1 advisory | STPA "looks forward" omits CAST | CAST acknowledged as backward-looking. |
| A2-U1 | Burnham letter cited as support for the review it disputes | Citation removed (and the entry dropped) until the letter is read. |
| A2-U2 | Feinstein & Cicchetti cited for the interval rule | Sentence now gives the reason the source supports (kappa unstable with imbalanced totals). |
| A2-R1–R4 | Cosmetic entry fixes | Feinstein "The" protected, "Pre-Flight" protected, AeroCopilotBench note quotes fixed, Krakovna URL updated. |
| A2 advisories | Ahmadi "agreement"; "standard term"; Hägele "tasks lengthen"; AeroCopilotBench | "accuracy against reference labels"; "a widely used term"; "the longer models reason and act"; AeroCopilotBench's own failure labels, including a reasoned deviation that parallels a stated violation, now acknowledged. |
| B-W1 | Failure shares called weighted but unweighted | Now weighted: 77–84%. The analysis header reports both sample and weighted shares. |
| B-W2 | Timestamps absent from "two" | Corrected to four. |
| B-W3 | Stale AG2 row in the information table | Corrected to 3 present, 4 partial, 8 absent. |
| B-W4 | ChatDev "60,000–500,000 tokens" | Corrected to about 40,000–495,000 (also in `design.py` and the guide). |
| B-W5 | Magentic-One version "only from a traceback" | Corrected: the version (autogen 0.4.9) is in each log's installation output (also in `design_check.md`). |
| B-W6 | "One run noted" the decision-error reading | Corrected to all three runs. |
| B-W7 | MetaGPT ProgramDev labels | Model-level note now says most MetaGPT groups apparently ran ProgramDev-v2 although MAST's metadata labels two ProgramDev. |
| B-O1 | "mostly inferred rather than stated" | Rewritten: few violations rest on stated reasoning; the primary run is mostly inferred, while Opus graded more as thin. |
| B-O2 | "absent from MetaGPT" etc. true of one run only | Qualified with all three runs (AppWorld none in any run; MetaGPT two, both Opus). |
| B-O3 | AppWorld "21 of 23" | Now "21 of 23 in two runs and 20 of 23 in the third". |
| B-O4 | "well above MAST's judge" | Replaced with the like-for-like comparison (0.52–0.59 vs 0.43) and its caveats. |
| B-O5 | "verification code" as typical | Now "a few". |
| B-O6 | L3.4 in FM-1.1 for one run only | Other runs added (16% and 6%). |
| B-O7 | "verbatim" quotes | Now "found in the step cited, after normalising"; "none of the checkable quotes" absent. |
| B-O8 | AG2 instruction presented as unconditional | Now describes the three options and the unconditional box-after-queries rule. |
| B-O9 | AG2 MMLU team "MAST's own, unpublished" | Now "adapts MAST's published three-agent topology, with unpublished MMLU prompts". |
| B-O10 | "24 most frequent design claims" | Now "the most frequent for each framework in the primary run". |
| B-I1 | A wrong-layer claim counted as confirmed | Reclassified as partly true: 7 confirmed, 14 partly true (paper, `design_check.md`, README, pilot summary). |
| B-I2 | "coded alike by all three runs" | Now "the same deepest factor and main codes". |
| B-I3 | Worked examples "do not depend on judging code" | Now "do not depend on judging whether the agents' answers were correct". |
| B-I4 | Table caption gave the wrong reason for missing intervals | Caption now says intervals are given for the headline measures only. |
| B-I5 | "MAST names models without versions" vs the Claude-3.7 label | Distinguished: the dataset names models without versions; the paper's label comes from MAST's paper. |
| B-I6 | "no record of task success" vs 60 verdicts | Now "no task-success field in MAST's metadata (60 logs carry a benchmark verdict)". |
| B-I7 | Weights refer to 867 traces, not 893 | Stated (pool outside the calibration set, 867 traces). |
| B-U1 | Empty-task example not AI-coded | Now says the trace was not in the AI sample and the coding is the author's illustration. |
| B-U2 | "where MAST's labels were least informative" | Now "MAST's FM-1.1 does not separate them from errors". |
| B-N1 | Original MAST annotation sheets not re-opened | Not re-checked in this audit (GitHub archive access was blocked); the earlier comparison stands, and the claim should be re-checked against the sheets before any journal submission. |
| B-N2 | OpenManus agents received the full task | Softened to "the agents' plans indicate that they received the full text". |

---

## Full reports

## Report 1: references 1–16

### A1: reference audit, 16 keys (afacs.tex, working draft v0.9)

Auditor: independent fact-check, read-only. Sources were opened in this session on 2026-11-04. Local copies and extracted text are in `(session scratchpad)/audit/src/`.

Scope: every `\cite` of the 16 keys, plus sentences that attribute something to these sources by name ("Ezell et al.'s ...", "MAST reports/describes ..."). Where one sentence makes several claims, each claim is judged separately.

Limits: the AIES version of record of Ezell et al. sits behind a bot check, so I used arXiv v1 (the only arXiv version) together with Crossref's VoR metadata. Four books could not be opened in full (marked NOT ACCESSIBLE). Semantic Scholar and DBLP rate-limited me, so I did not do a full check for published versions of every arXiv entry; Crossref found one (A1-R2).

#### Summary

| Category | Count | Notes |
|---|---|---|
| VERIFIED | 30 | 22 cited instances + 8 attributions by name |
| WRONG | 0 | |
| OVERSTATED | 6 | A1-O1 to A1-O6 (O1, O2, O3, O4 matter most) |
| UNSUPPORTED | 1 | A1-U1 |
| NOT ACCESSIBLE | 4 | reason1990human, reason1997managing, wiegmann2003human, leveson2012engineering. Secondary checks agree with the paper; none contradicts it. |
| Reference-entry issues | 5 | 2 substantive (A1-R1, A1-R2), 3 cosmetic (A1-R3 to A1-R5) |

Every number attributed to these sources checks out exactly: 150 traces, κ=0.88, κ=0.77, o1 judge, 14 modes, 1642 traces / 7 frameworks, CC-BY-4.0, 21 claimed human-labelled traces (19 in the file), 18 items in Ezell's Table 1, 319 causal factors, κ=.71, aviation psychologist + commercially-rated pilot. The paper contains no direct quotation attributed to any of the 16 sources. (The two quotations near these cites, ``requires no inference about intent'' and ``hot mess'', belong to other keys.) Items named in the brief that do not appear in the current text: "11%" (TRAIL abstract: Gemini-2.5-pro "scoring a mere 11%"), "14.2%" (Who&When abstract), "thirteen open challenges" (Ezell Table 3 has 13; the text now says "lists open challenges" without a number). κ=0.76 appears only as the paper's own result. The figures in the sources match, so they would be correct if reintroduced.

#### Issues

| ID | Location (section + quoted sentence) | Problem | Evidence (URL + quote/locator) | Required fix |
|---|---|---|---|---|
| A1-U1 | Introduction, l.61-63: "Ezell, Roberts-Gaal and Chan~\cite{ezell2025incident} proposed the first framework for analysing incidents involving AI agents in this tradition." | This is a priority claim the cited source does not make, and the paper offers no evidence for it. Ezell et al. only say "we propose an incident analysis framework". Nothing in the paper shows a search for earlier frameworks. | https://arxiv.org/abs/2508.14231 (v1 PDF), abstract: "we propose an incident analysis framework for agents". The full text has no "first" or "novel" claim (grep of the extracted text). | Drop "the first", e.g. "proposed a framework for analysing incidents involving AI agents in this tradition". Alternatively write "to our knowledge, the first" and state the search that backs it. |
| A1-O1 | Introduction, l.67-70: "Its agent-level category holds errors only: the paper cites an agent that reasoned about cheating its unit tests before doing so~\cite{baker2025monitoring}, but no category records such a departure." Echoed in the abstract, l.24-25 ("has no category for deliberate departures from known requirements"), and in the Table 2 row "(mentioned, not categorised)". | Overstated claim of absence. Ezell et al. do record deliberate or undesirable departures: they place them inside "cognitive errors". They list "performing an unintended or undesirable task" as a cognitive error. In the EchoLeak case study, a possible knowing compliance is coded as a cognitive error. Their Baker reward-hacking example sits in the Cognitive Errors section. Reward hacking also has system-factor homes (feedback that specifies a proxy goal). What the framework lacks is a category that *distinguishes* a violation from an error, not a category that *records* the departure. "(mentioned, not categorised)" is inaccurate in the same way. | arXiv:2508.14231v1. §2.3 (p.3-4): "Performing an unintended or undesirable task, such as an AI agent that attempts to manipulate a user to buy a product". §4.1 EchoLeak, "Cognitive errors": "or it may have identified–but nevertheless complied with–malicious commands". §2.3: "OpenAI's models reasoned about reward hacking in their chain of thought before they engaged in it". App. A.1 Feedback: "Feedback specifies an undesirable proxy goal". App. A.3 Decision-making: "Incorrect selection and/or prioritization of goals". | Intro: "Its agent-level category is framed as cognitive errors and folds deliberate departures into it (it counts 'performing an unintended or undesirable task' as a cognitive error), so nothing distinguishes a violation from an error." Abstract: "does not distinguish deliberate departures from known requirements from errors". Table 2: replace "(mentioned, not categorised)" with "(folded into cognitive errors, not distinguished)". |
| A1-O2 | Introduction, l.70: "And it has not been applied to real traces." Abstract, l.25: "and has not been applied to real traces." | Literally true but incomplete, so it reads as an unscoped claim of absence. Ezell et al. themselves apply the framework to a real incident (EchoLeak) using public advisories, noting that logs were unavailable. Two later papers present structured analyses of real agent incidents from real logs as instances of Ezell's programme. Neither codes traces with Ezell's factor taxonomy, so the narrow claim survives, but readers may infer that no real-world application exists at all. | arXiv:2508.14231v1 §4.1: "Case Study: EchoLeak Incident ... Based on public information, the following assessment about contributing factors to the incident can be made". arXiv:2609.12748, p.3: "this paper is one such analysis carried out from outside". arXiv:2606.14589, p.3: "our corpus can be read as an existence proof of their program". (Semantic Scholar lists 9 citing papers; I read the four most relevant.) | Scope the claim, e.g. "Ezell et al. illustrate it on one real incident (EchoLeak) from public advisories, without logs; to our knowledge its taxonomy has not been used to code agent traces." Shorten the abstract the same way, e.g. "...and has been illustrated only on public incident reports, not traces". |
| A1-O3 | §3 Layered evidence, l.239-241: "HFACS met the same limit in aviation: organisational causes come from company records, not the flight recorder, and were rare in NTSB-based coding~\cite{wiegmann2001commercial}." | (a) The report says nothing about company records versus flight recorders. Its only mention of the flight data recorder concerns mechanical causes. (b) "Rare" is supported. (c) "Met the same limit" presents the rarity as an evidence limit. The report gives two competing explanations, one of which is that such factors may simply play a smaller role. | https://rosap.ntl.bts.gov/view/dot/15409/dot_15409_DS1.pdf (DOT/FAA/AM-01/3). Table 1 p.8: Org. Influences: Resource Mgmt 2.5%, Org. Climate 0.0%, Org. Process 8.4%. p.9-10: "only 16% of all aircrew-related accidents involved some form of either supervisory or organizational involvement". p.10 (two explanations): factors may "simply do not play as large of a role", or "they are rarely identified using existing accident investigation processes". | Cite only what the report says, e.g. "...organisational causes were rare in NTSB-based coding, which Wiegmann and Shappell attributed either to a smaller role or to investigation processes that rarely identify them". Keep "company records, not the flight recorder" only as the author's own remark, or give it a source. The uncited Discussion sentence at l.571 makes the same point and needs the same treatment. |
| A1-O4 | §2 Background, l.105-110: "Other taxonomies classify failures by error type~\cite{deshpande2025trail}, ... or by where the fix belongs~\cite{raj2026modelharness}. They answer ``what broke'' and ``who and when''; AFACS adds ``what kind of act'' and ``what latent conditions''." | Overstated as a summary of the cited works. Raj et al. include a named "Specification Gaming" mode, which is a violation-like kind of act. They also assign faults to harness, owner, environment or grader, which are design or set-up conditions. TRAIL classifies by "error type", which is itself a "kind of act", so the contrast reads as self-contradictory. What AFACS really adds is the error/violation distinction with an evidence grade, and layering. | https://arxiv.org/abs/2607.28802, taxonomy appendix: "Specification Gaming (MODEL). The model targets the evaluation channel itself, exploiting a flaw in the reward function or grading metric". Abstract: "harness-side failures point to scaffolding and tool-integration fixes". https://arxiv.org/abs/2505.08638 abstract: "a formal taxonomy of error types". | Narrow the claim, e.g. "...AFACS adds whether the act was an error or a violation, graded by evidence, and a layered account of the conditions behind it (Raj et al. name specification gaming and harness-side faults, but as flat modes)." |
| A1-O5 | §2 Background, l.103-105: "MAST ... reports human agreement of $\kappa=0.88$ and $\kappa=0.77$ ... but has no causal layers." | The numbers are verified (see V10). "No causal layers" is fair in the HFACS sense but understates MAST's own causal framing. MAST's FC1 is "System Design Issues", defined by where failures originate. The modes are mapped to stages "where their root causes commonly emerge". MAST itself says FM-1.1 has mixed deeper causes, which anticipates the paper's RQ4 finding. | https://arxiv.org/abs/2503.13657 (v3), §4: "FC1. System Design Issues. Failures originate from system design decisions, and poor or ambiguous prompt specifications". Also "map to MAS execution stages ... where their root causes commonly emerge". FM-1.1: "we identify deeper causes: (1) flaws in MAS design ... (2) poor user prompt specifications, or (3) limitations of the underlying LLM". | E.g. "...but labels each failure flatly: its three categories (one attributed to system design) and execution stages do not separate the act from the conditions behind it." In RQ4, consider noting that MAST itself flags FM-1.1's mixed causes. |
| A1-O6 (minor) | Introduction, l.73-76: "It takes up five of Ezell et~al.'s open challenges: non-exhaustive coverage, emerging factors, high-level cognitive errors, reconstruction difficulties with limited data access, and, in part, expertise shortages." | Ezell's Table 3 lists "Limited data access" and "Reconstruction difficulties" as separate challenges. "Limited data access" concerns privacy and security rules on *who* may see incident data, which AFACS does not address. As written, the phrase merges two items while still counting five. | arXiv:2508.14231v1, App. B, Table 3: "Limited data access: Privacy and security requirements restrict who can access sensitive incident information". Separately: "Reconstruction difficulties: Incident reconstruction may require access to proprietary system artifacts or model internals". | Write "reconstruction difficulties" without "with limited data access", or name both and recount, and drop "limited data access" if AFACS does not take it up. |
| A1-R1 | references.bib `ezell2025incident` | The version of record exists, but the entry lacks volume, issue, pages and DOI. The note "arXiv comment: to be published in the AIES 2025 proceedings" is stale and appears in the printed reference list (afacs.bbl l.60). | Crossref: https://api.crossref.org/works/10.1609/aies.v8i1.36596 gives "Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society", vol. 8, issue 1, pp. 865-878, published 2025-10-15. | Add `volume = {8}, number = {1}, pages = {865--878}, doi = {10.1609/aies.v8i1.36596}`, remove the note, and keep the arXiv eprint. |
| A1-R2 | references.bib `shamsujjoha2024swisscheese` | Cited as a 2024 arXiv preprint, but a peer-reviewed version exists. | Crossref: https://api.crossref.org/works/10.1109/icsa65012.2025.00014 gives "2025 IEEE 22nd International Conference on Software Architecture (ICSA)", pp. 37-48, same four authors, same title. | Cite the ICSA 2025 version (pp. 37-48, DOI 10.1109/ICSA65012.2025.00014), optionally keeping the arXiv ID. |
| A1-R3 (cosmetic) | references.bib `cemri2025mast` | The note hedges ("reported as Datasets and Benchmarks Track"). The paper itself states the track. | arXiv v3 p.1 footer: "39th Conference on Neural Information Processing Systems (NeurIPS 2025) Track on Datasets and Benchmarks". https://neurips.cc/virtual/2025/poster/121528: "Spotlight Poster". | Replace the note with "Datasets and Benchmarks Track; spotlight". |
| A1-R4 (cosmetic) | references.bib `leveson2012engineering` | The printed reference ends "commonly cited as 2011; open access" (afacs.bbl l.93), which is unusual in a reference list. IEEEtran does not print the DOI for this @book. The year itself is correct. | Crossref 10.7551/mitpress/8179.001.0001: MIT Press, issued 2012-01-13. | Remove the note or reduce it to the DOI/URL. Optional. |
| A1-R5 (cosmetic) | references.bib `reason1997managing` | The DOI field (10.4324/9781315543543) belongs to the Routledge 2016 reissue (Crossref issued 2016-01-29), while the entry describes the 1997 Ashgate edition. The note says it was reissued, and the DOI is not printed. | https://api.crossref.org/works/10.4324/9781315543543: Routledge, 2016-01-29. | Optional: move the DOI into the note, as done for `wiegmann2003human`. |

#### NOT ACCESSIBLE (secondary checks)

- **reason1990human** (Introduction l.49-51, latent conditions behind the sharp-end act). Full text not opened. The Cambridge Core TOC (https://www.cambridge.org/core/product/identifier/9781139062367/type/book) shows ch. 7 "Latent errors and systems disasters", pp. 173-216. HFACS 2000 (p.1-2) attributes the Swiss-cheese model of latent and active failures to "James Reason (1990)". The bib entry is correct: CUP, print 26 Oct 1990, DOI resolves to "Human Error", J. Reason.
- **reason1997managing** (same sentence). Full text not opened; T&F returned 403. AHRQ PSNet (https://psnet.ahrq.gov/issue/managing-risks-organizational-accidents): "Aldershot, Hants, England: Ashgate: 1997", "the now-famous 'Swiss cheese model'", "the difference between active and latent errors". Open Library (ISBN 9781840141054): Ashgate, 1997. Consistent with the claim and the bib entry (see A1-R5).
- **wiegmann2003human** (Introduction l.52-54, HFACS as a four-tier coding scheme). Full text not opened. The Routledge product page (https://www.routledge.com/products/9780754618737 resolves; pubDate 17-07-2003) says "a complete description of the Human Factors Analysis and Classification System (HFACS), which incorporates James Reasons model of latent and active failures". Crossref 10.4324/9781315263878 gives Routledge, 2017, Wiegmann & Shappell. The claim itself is fully supported by shappell2000hfacs (V2).
- **leveson2012engineering** (§2 l.101-102, "STPA look[s] forward, at ... hazards"). Full text blocked (MIT Press, OAPEN and DOAB returned 403). Crossref chapter record 10.7551/mitpress/8179.003.0013: "STPA: A New Hazard Analysis Technique", pp. 211-250. The claim is consistent. *Advisory, not counted as an issue:* the same book's ch. 11 (Crossref 10.7551/mitpress/8179.003.0016) is "Analyzing Accidents and Incidents (CAST)", pp. 349-390. This is a backward-looking, systems-theoretic incident-analysis method, so citing Leveson only for forward-looking STPA, and contrasting it with "incident analysis looks back", leaves CAST out. A clause acknowledging CAST would be fairer.

#### VERIFIED

Cited instances:
- V1 `reason1990errors`, Intro l.55-57: errors and violations "call for different remedies and appear to be different kinds of behaviour". PubMed 20073122 abstract: "may have different psychological origins and demand different modes of remediation"; "errors and violations are indeed mediated by different psychological mechanisms". Bib entry correct: Ergonomics 33(10-11):1315-1332, DOI 10.1080/00140139008925335, 5 authors (Crossref).
- V2 `shappell2000hfacs`, Intro l.52-54: four tiers, organisational influences down to unsafe acts. FAA 00_07.pdf p.2: "HFACS describes four levels of failure: 1) Unsafe Acts, 2) Preconditions for Unsafe Acts, 3) Unsafe Supervision, and 4) Organizational Influences". The error/violation definitions in l.54-56 ("willful disregard for the rules and regulations") are on p.2-3. Bib entry correct: DOT/FAA/AM-00/7, Feb 2000, URL resolves.
- V3 `ezell2025incident`, Intro l.63-65: system, contextual and cognitive factors; information needs; open challenges. arXiv:2508.14231v1 §2 "three complementary categories of incident factors"; §3 information categories; App. B "Table of Open Questions and Challenges for Future Work".
- V4 `ezell2025incident`, Intro l.66-67: treats a single agent, with no place for a supervising orchestrator or inter-agent breakdowns. Fair: the taxonomy (§2, App. A) frames every factor around "an AI agent", and a grep finds no orchestrator, supervision or coordination category. HFACS's "unsafe supervision" is mentioned only in the introduction. Nuance: §3.1 notes that "an AI system can also consist of multiple AI models" (activity logs only).
- V5 `baker2025monitoring`, Intro l.68-69: the paper cites an agent that reasoned about cheating its unit tests before doing so. Ezell §1: "a strategy to cheat the evaluation by skipping unit tests was evident in the agent's chain of thought (Baker et al. 2025)". Baker arXiv:2503.11926 Fig. 1: the agent "notes it could 'fudge' and circumvent the tests by making verify always return true". Bib entry correct: 9 authors, title, ID.
- V6 `cemri2025mast`, Intro l.76: the public MAST dataset. HF `mcemri/MAST-Data` is public, sha 95118ac951421753cf1deb87ddea3b01e693c41b. Bib entry: authors, title, ID and NeurIPS 2025 D&B all correct.
- V7 `ezell2025incident`, §2 l.96-101: the factor lists and "eighteen items of information investigators need (their Table 1)". App. A headings: Training data, Feedback, Learning methods, System prompt, Scaffolding; Information, Tools, Task definition; Observation, Understanding, Decision-making, Action execution. Table 1 has 7 + 4 + 7 = 18 rows; caption "Information needs to identify incident factors from Section 2 and/or enable incident reconstruction".
- V8 `shamsujjoha2024swisscheese`, §2 l.101-102: Swiss-cheese guardrail designs look forward at defences. arXiv:2408.02205 abstract: "we also propose a reference architecture for designing multi-layered runtime guardrails". Authors and title correct; see A1-R2 for the published version.
- V9 `mylius2025stpa`, §2 l.101-102: STPA looks forward at hazards. arXiv:2506.01782 abstract: "STPA ... is a systematic methodology for identifying how complex systems can become unsafe, leading to hazards". Bib entry correct.
- V10 `cemri2025mast`, §2 l.103-105: 150 traces, human κ=0.88, o1 judge κ=0.77 against experts. arXiv:2503.13657v3 §3.1: "we first collect 150 traces from five MAS frameworks". §1: "high inter-annotator agreement (κ = 0.88)". §3.3: "an LLM (OpenAI's o1 model)"; Table 2: "o1 (few shot) ... 0.77".
- V11 `deshpande2025trail`, l.106: classify by error type. Abstract: "introduce a formal taxonomy of error types encountered in agentic systems". Bib entry: 6 authors, title and ID correct.
- V12 `zhu2025agenterrorbench`, l.107: classify by the component that broke. Abstract: "a modular classification of failure modes spanning memory, reflection, planning, action, and system-level operations". Bib entry: 18 authors match arXiv (the title has a trivial "Can"/"can" case difference).
- V13 `zhang2025whowhen`, l.108: classify by the agent and step responsible. Abstract: "identifying the agent and step responsible for task failures". Bib entry correct per PMLR page: v267, pp. 76583-76599, zhang25cq, 11 authors.
- V14 `raj2026modelharness`, l.108-109: classify by where the fix belongs. arXiv:2607.28802 abstract: "a fault side indicating where the repair belongs". Bib entry correct: 7 authors, title, ID, primary category cs.AI. The follow-on sentence is A1-O4.
- V15 `wiegmann2001commercial`, §2 l.112-114: an aviation psychologist and a pilot re-coded 319 NTSB causal factors at κ=0.71. AM-01/3 p.7: "The 119 aircrew-related accidents yielded 319 causal factors ... coded independently by both an aviation psychologist and a commercially-rated pilot"; "The obtained kappa value was .71". Bib entry correct: DOT/FAA/AM-01/3, Feb 2001, URL resolves.
- V16 `baker2025monitoring`, l.126-127: reasoning traces reveal reward hacking; models trained against monitors learn to hide it. Abstract: "agents learn obfuscated reward hacking, hiding their intent within the CoT while still exhibiting a significant rate of reward hacking".
- V17 `wiegmann2001commercial`, §3 l.199-200: L4.4 by analogy with HFACS resource management. AM-01/3 p.6: "resource management, refers to the management, allocation, and maintenance of organizational resources, including human resource management (selection, training, staffing)".
- V18 `baker2025monitoring`, §3 l.257-259: written reasoning may not reflect what produced an action, and models can learn to hide it. Baker §1: "questions remain regarding whether chains-of-thought are fully faithful"; §5.1 on faithfulness; abstract on obfuscation.
- V19 `zhang2025whowhen`, Future Work l.608-609: datasets with verified outcomes and human attribution. Who&When uses GAIA/AssistantBench queries with ground truth, and failure logs are annotated by "three human experts" (arXiv:2505.00212 §3).
- V20 `cemri2025mast`, Materials l.621: the dataset is CC-BY-4.0. HF API for mcemri/MAST-Data: `license:cc-by-4.0`.
- V21 `cemri2025mast`, App. A l.656-657: "MAST reports κ=0.77 between its judge and experts". Same as V10 (§3.3, Table 2).
- V22 `ezell2025incident`, Table 7 (tab:evsource) caption and Ezell column (Activity logs; tool information; system documentation and change logs; system artefacts; model access; system configuration). All are row or category names in Ezell's Table 1.

Attributions by name (no `\cite` at that spot):
- V23 Table 2 left column (Ezell factors): matches App. A, including "System prompt is underspecified", "inadvertently encourages undesirable behavior", "Scaffolding does not function as intended", "Inadequate memory capacity" under Observation, and "Forgets or gets distracted from goal(s)" under Decision-making. The exception is the last row; see A1-O1.
- V24 l.278: "Ezell et al. analyse incidents, events that cause or could cause harm". Ezell §1: "events involving AI agent use that directly or indirectly cause harm". §2: the framework "can also be used to identify the contributing factors to hazards".
- V25 Fig. 1 caption and l.306-307: the eighteen items, and "Items marked * matter mainly for reconstruction". Ezell Table 1 caption: "Asterisks denote information primarily useful for reconstruction".
- V26 l.377: "an empirical instance of Ezell et al.'s reconstruction challenge". Ezell Table 3, "Reconstruction difficulties": access to "proprietary system artifacts or model internals ... not readily available".
- V27 l.288-290: 1642 traces, seven frameworks, 14 binary labels from an o1 judge. MAST v3 §3.4: "MAST-Data, comprising 1642 annotated traces from seven popular MAS frameworks"; o1 annotator in §3.3.
- V28 l.85: "MAST's fourteen flat labels". MAST v3 §4: "identifies 14 fine-grained failure modes".
- V29 l.694-695: "MAST describes MetaGPT as having an explicit verifier". MAST v3 §4: "Systems with explicit verifiers like MetaGPT and ChatDev generally show fewer total failures".
- V30 l.676-677: "MAST's human-labelled file holds 19 traces (not 21)". MAST v3 §1: "MAST-Data-human, a smaller dataset featuring 21 traces". `MAD_human_labelled_dataset.json` at revision 95118ac is a JSON list of 19 records (checked).


---

## Report 2: references 17–33

### A2: Citation audit, 17 references in afacs.tex

Paper: `/home/user/Research/projects/afacs/paper/afacs.tex` (working draft v0.9). Bibliography: `references.bib`, checked against the rendered `afacs.bbl` and `afacs.pdf`.
Scope: 17 BibTeX keys, cited at 13 places. That makes 18 key-citation instances, because `ahmadi2025hfacsgrpo` is cited twice.
Method: I opened every source in this session (arXiv API metadata and full-text PDFs, PubMed via NCBI E-utilities, the Crossref API, publisher and project web pages, GitHub). Source copies and extracted text are in `(session scratchpad)/audit/src/`.

#### Summary

| Category | Count | Items |
|---|---|---|
| VERIFIED | 16 | olsen, cohen2015, ahmadi (x2), krakovna, zhong, meinke, lynch, smyth, hagele, cohen1960, landis, aisi, brooker, wu, yuan |
| WRONG | 0 | |
| OVERSTATED | 0 | (3 wording points are in the advisory notes below) |
| UNSUPPORTED | 2 | burnham2017letter (A2-U1), feinstein1990paradox (A2-U2) |
| NOT ACCESSIBLE | 0 whole citations | I could not open the full text of the Burnham letter. The A2-U1 verdict rests on its PubMed and ERAU records (see A2-U1). |
| Reference-entry issues | 4, all cosmetic | A2-R1 to A2-R4. All authors, titles, venues, years, volumes, pages, DOIs and arXiv IDs are correct. |

#### Issues (every item that is not VERIFIED)

| ID | Location (section + quoted sentence) | Problem | Evidence (URL + quote/locator) | Required fix |
|---|---|---|---|---|
| A2-U1 (important) | Background, "HFACS and its reliability" (tex l.114-117): "Reliability is contested: a modified HFACS showed low agreement~\cite{olsen2010hfacsadf}, and a review found it higher with training and fewer departures from the original~\cite{cohen2015reliability,burnham2017letter}." | Burnham (2017) is a letter to the editor commenting on the Cohen et al. review, and Shappell published a reply to it. A letter about the review cannot be a source for what the review found. Every indication is that the letter disputes the review, so it is cited in support of the opposite position. I could not open the letter's full text. | PubMed 28539151 (https://pubmed.ncbi.nlm.nih.gov/28539151/): record type "Letter", listed as "Comment on Aerosp Med Hum Perform. 2015 Aug;86(8):728-35. doi: 10.3357/AMHP.4218.2015", no abstract. PubMed 28539150 (https://pubmed.ncbi.nlm.nih.gov/28539150/): "Letter to the Editor re: ... : Response. Shappell SA." ERAU portfolio (https://portfolio.erau.edu/en/publications/letter-to-the-editor-re-evaluating-the-reliability-of-the-human-f/): "Dr. Shappell's letter addresses Mr. Burnham's comments about the HFACS." The author's own notes (`projects/afacs/docs/related_work.md` l.187) say "the review drew a published letter disputing it (Burnham 2017 ...) ... I did not read the letter itself." A search-engine summary, which I could not open at source, says the letter argues the review misrepresented three studies and that the data are insufficient to support HFACS reliability. **Routes tried for the full text:** doi.org, which redirects to asma.kglmeridian.com (a JavaScript-only page; WebFetch got 403); the publisher's downloadpdf URLs (403 or an HTML shell); IngentaConnect (403 challenge); Europe PMC ("Subscription required"); Semantic Scholar API (429); scholar.archive.org (rate-limited). I stopped there rather than work around access controls. | Remove `burnham2017letter` from the review clause. Cite it for the contestation instead, after reading it. For example: "Reliability is contested~\cite{olsen2010hfacsadf,burnham2017letter}: ... a review found it higher with training and fewer departures from the original~\cite{cohen2015reliability}, though a published letter disputed its reading of the evidence~\cite{burnham2017letter}." Describe what the letter argues only after reading it. |
| A2-U2 (minor) | Data and Method, "Consistency measures" (tex l.329-331): "...and whether a failure was observed, with 95\% bootstrap intervals omitted where answers are too few to support one~\cite{feinstein1990paradox}." | Feinstein & Cicchetti is about the kappa paradoxes: under imbalanced marginals, high observed agreement can give low kappa. It does not discuss bootstrap or confidence intervals, or a minimum-count rule for reporting them. As placed, the citation appears to support the interval-omission rule, which the source does not address. The underlying rationale (kappa is unstable when one category is rare) is supported, but the sentence does not state it. | PubMed 2348207 (https://pubmed.ncbi.nlm.nih.gov/2348207/), abstract: "a high value of p0 can be drastically lowered by a substantial imbalance in the table's marginal totals". The abstract says nothing about intervals. | Say why: "...omitted where either coder gave fewer than three positive or negative answers; with such imbalanced marginals kappa is unstable and can be paradoxically low~\cite{feinstein1990paradox}." Alternatively, move the citation to where near-zero kappas for rare codes are reported (Results, RQ3: "the rare L1.V? (about zero)"). |
| A2-R1 (cosmetic) | Bibliography `feinstein1990paradox` | It renders as "High agreement but low kappa: I. the problems of two paradoxes". IEEEtran lowercases "The" after "I.". | afacs.bbl / afacs.pdf ref [29]. The PubMed title is "High agreement but low kappa: I. The problems of two paradoxes." | Use `title = {High agreement but low Kappa: {I. The} problems of two paradoxes}` or brace `{The}`. |
| A2-R2 (cosmetic) | Bibliography `brooker2026preflight` | The title renders as "Pre-flight: ...". The benchmark's name is "Pre-Flight". | afacs.pdf ref [31]. arXiv title: "Pre-Flight: A Benchmark for Evaluating Large Language Models on Aviation Operational Knowledge" (https://arxiv.org/abs/2607.01829). | Brace the name: `{Pre-Flight}`. |
| A2-R3 (cosmetic) | Bibliography `yuan2026aerocopilotbench`, `note` field | The v1 title in the note is wrapped in straight `"..."`, which LaTeX typesets as two closing quotes. The content is correct: the v1 title and both dates match arXiv. | references.bib l.345. arXiv v1 PDF title page: "AeroCopilotBench: A Two-Tier Benchmark for Evaluating LLM Agents as Aviation Copilots in an Interactive Virtual Cockpit Environment", 17 Aug 2026. v2: 27 Sep 2026 (https://arxiv.org/abs/2608.16349v2). | Use ``...'' (two backticks and two apostrophes) in the note. |
| A2-R4 (cosmetic) | Bibliography `krakovna2020specgaming`, `url` | The URL still resolves, but it redirects. The canonical URL is now `https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/`. The authors and date match (page date "April 21, 2020"). | curl -L: the final URL is deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ (HTTP 200). | Optional: update the URL. Add the day (21 April 2020) if wanted. |

#### VERIFIED items

1. **olsen2010hfacsadf**: "a modified HFACS showed low agreement". The source evaluates HFACS-ADF, the Australian Defence Force adaptation, at an ATC unit. PubMed 20159064 abstract: "For all studies, agreement was low at the level of both fine-level HFACS-ADF descriptors and high-level HFACS-type categories." Bib entry matches Crossref: Accid. Anal. Prev. 42(2):437-444, 2010, doi 10.1016/j.aap.2009.09.005.
2. **cohen2015reliability**: "a review found it higher with training and fewer departures from the original". PubMed 26387897 (systematic review of 14 papers): "Reliability levels were higher with increased training and sample sizes. Likewise, when deviations from the original framework were minimized, reliability levels increased." Bib matches Crossref: AMHP 86(8):728-735, 2015.
3. **ahmadi2025hfacsgrpo (1st, l.117-119)**: "LLMs coding aviation reports reach far lower exact-match than partial-match agreement". arXiv 2508.21201 abstract: exact match "from 0.0400 to 0.1800" against partial match "0.8800". §3.3: Gemini-2.5-flash 0.12 exact vs 0.83 partial; GPT-5-mini 0.07 vs 0.88. The data are NTSB general-aviation narratives (§2.2). See advisory note (a).
4. **ahmadi2025hfacsgrpo (2nd, l.331-332)**: "The share of identical full code sets is also reported". Abstract: the paper "proposes exact match accuracy in multi-label HFACS classification problem as a new benchmarking methodology". §3: exact match "requires both precision and recall of 100%". This supports the citation as a precedent for the metric. Bib matches arXiv: authors Ahmadi, Sharif, Banad; title exact; 2025.
5. **krakovna2020specgaming**: "Specification gaming is the standard term for many behaviours AFACS would code as violations". Blog (https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/): "Specification gaming is a behaviour that satisfies the literal specification of an objective without achieving the intended outcome." Its example is a student who "might copy another student ... and thus exploit a loophole". All nine authors and the date match. See advisory note (b).
6. **zhong2025impossiblebench**: "ImpossibleBench builds tasks that can be passed only by breaking the specification". arXiv 2510.20270 abstract: "introducing direct conflicts between the natural-language specification and the unit tests ... any pass necessarily implies a specification-violating shortcut". Bib matches.
7. **meinke2024scheming**: "Frontier models in constructed scenarios reason about constraints and circumvent them". arXiv 2412.04984 abstract: models "placed in environments that incentivize scheming ... attempt to disable their oversight mechanisms"; "models explicitly reason about these deceptive strategies". Bib matches: six authors in arXiv order, 2024.
8. **lynch2025agentic**: same sentence. arXiv 2510.05179 abstract: "hypothetical corporate environments", "Models often disobeyed direct commands". PDF p.2: "they acknowledged the ethical constraints and yet still went ahead with harmful actions." Bib matches: eight authors, title.
9. **smyth2026overclaim**: "OverclaimBench measures false claims of completion with a criterion that ``requires no inference about intent''". The quotation is verbatim. arXiv 2609.20812v3 abstract: "This criterion requires no inference about intent and does not depend on whether the delivered work is correct". Bib matches: nine authors, title, 2026.
10. **hagele2026hotmess**: "failures look increasingly like an incoherent ``hot mess'' as tasks lengthen". arXiv 2601.23045v2 abstract: "fail by being a hot mess" (the quotation is verbatim) and "the longer models spend reasoning and taking actions, the more incoherent their failures become". Fig. 2 caption: "for questions where models reason longer and take many actions, their errors are dominated by variance". The PDF header reads "Published as a conference paper at ICLR 2026", so the ICLR booktitle is correct. See advisory note (c).
11. **cohen1960kappa**: Cohen's kappa. Crossref (https://api.crossref.org/works/10.1177/001316446002000104) gives "A Coefficient of Agreement for Nominal Scales", J. Cohen, Educ. Psychol. Meas. 20(1):37-46, 1960. Wikipedia "Cohen's kappa": "The seminal paper introducing kappa ... was published by Jacob Cohen in the journal Educational and Psychological Measurement in 1960". The publisher's page (Sage) returned 403.
12. **landis1977measurement**: Cohen's kappa, methodological reference. PubMed 843571: "measures of interobserver agreement are developed as generalized kappa-type statistics". Biometrics 33(1):159-74, 1977, which matches the bib. Crossref confirms doi 10.2307/2529310.
13. **aisi2024inspect**: "built in Inspect". The site (https://inspect.aisi.org.uk/) says: "Inspect is a framework for frontier AI evaluations developed by the UK AI Security Institute and Meridian Labs". The site's own BibTeX gives the title "Inspect AI: Framework for Large Language Model Evaluations", author "AI Security Institute, UK", date 2024-05. The bib matches.
14. **brooker2026preflight**: the claim of absence, "do not code their failures with a human-factors framework", holds. In arXiv 2607.01829 (9 pp.), §5.2 is item and category accuracy, and §6 "Qualitative analysis of failure modes" consists of three illustrative probes ("Reasoning versus pattern matching", "Physical and temporal constraints", "Complex visual reasoning"). A full-text search for human factors, HFACS, taxonomy, slip/lapse/violation and Reason found no human-factors framework. The bib note is correct: https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/pre_flight exists, and its README credits Brooker and Hughes and cites arXiv 2607.01829. Authors and title match, apart from the casing in A2-R2.
15. **wu2026pilotbench**: the claim of absence holds. arXiv 2604.08987 (6 pp.) evaluates trajectory and attitude prediction with Pilot-Score. Its only failure analysis is §IV: "Key failure patterns include numerical anomalies, flight-logic errors, structural issues, refusal responses, and temporal discontinuities". There is no human-factors framework. The arXiv comment reads "Accepted at the 2026 IEEE International Joint Conference on Neural Networks (IJCNN 2026)", so the booktitle is correct, and the authors match.
16. **yuan2026aerocopilotbench**: the claim of absence holds. arXiv 2608.16349v2 §5.4: "We review all 557 of their failed episodes and derive six labels from recurring patterns" (M1-M6). v1 has four inductive failure modes. Neither version cites HFACS, Reason or any other human-factors framework. See advisory note (d). Authors, v2 title, v1 title and dates match, apart from the quote marks in A2-R3.

#### Advisory notes (not counted as issues; the authors may want to act on them)

- (a) ahmadi: Ahmadi's figures are *accuracy against reference labels* (GAHFACS), not agreement between coders. Their "partial match" means at least one predicted code is correct, which is very lenient. "exact-match than partial-match accuracy" would be more precise in a paragraph about inter-coder reliability.
- (b) krakovna: the blog defines the term but does not itself show that it is "the standard term". In Krakovna's definition, gaming *satisfies the literal specification* and is "caused by misspecification of the intended task". AFACS violations are departures from a requirement in context, so the overlap is partial. "Many behaviours" already hedges this adequately.
- (c) hagele: the variable Hägele et al. measure is how long a model reasons and acts ("even when controlling for task difficulty"), not task length as such. "As models reason and act for longer" would be more exact. The step "so most should be errors" is the author's inference, not a finding of the source. It reads as an inference, which is acceptable.
- (d) yuan (AeroCopilotBench): the absence claim is literally true. But AeroCopilotBench does code its failures, with an inductive six-label scheme. Its "M2: Reasoned deviation from POH" ("The model states a reason in its reasoning text and acts on it in a way that conflicts with the POH") closely parallels AFACS's *stated* violation grade, and "M6: Misreading the observed state" parallels a perceptual error. A fairer sentence would acknowledge this. For example: "...code failures with inductive or output-level categories (AeroCopilotBench's 'reasoned deviation' is the closest to a violation code), not with a human-factors framework."


---

## Report 3: numbers, claims about MAST and the frameworks, worked examples

### Audit B: numbers and factual claims in `paper/afacs.tex` (draft v0.9, 4 Nov 2026)

Auditor scope: every number, the MAST and framework facts, the five worked examples, and internal consistency. I worked read-only. Recomputation scripts are in `(session scratchpad)/audit/scripts/` (`recompute.py`, `prec.py`, `agree.py`, `data_checks.py`, `pooled.py`, `logcounts.py`, `show.py`, `codings.py`). The bootstrap output is in `.../audit/boot_out.txt`. I checked that the built PDF text matches the .tex for every issue below (pdftotext of `afacs.pdf`).

Primary sources opened in this session:
- MAST paper, arXiv 2503.13657 v1 to v3 (HTML).
- MAST repo `traces/HyperAgent/README.md`.
- SWE-bench `evaluation/lite/20240925_hyperagent_lite1/metadata.yaml`.
- HF `mcemri/MAST-Data` API and README at rev 95118ac.
- autogen `python-v0.4.7` and `python-v0.4.9`: agbench GAIA MagenticOne `scenario.py`, the Magentic-One orchestrator, `_prompts.py`, `_magentic_one_group_chat.py`, and the MultimodalWebSurfer and FileSurfer sources.
- OpenManus `app/agent/base.py` @964b2af.
- AG2 v0.7.5 `math_user_proxy_agent.py`.
- MetaGPT v0.8.2 `examples/build_customized_multi_agents.py`.
- HyperAgent paper (arXiv 2409.16299) and `src/hyperagent/tools/gen_tools.py` (main branch).
- Ezell et al. arXiv 2508.14231 (HTML).
- Wiegmann & Shappell DOT/FAA/AM-01/3 (PDF).
- Anthropic's Claude 3.7 Sonnet announcement.

#### Summary

| Category | Count |
|---|---|
| VERIFIED | 78 |
| WRONG | 7 |
| OVERSTATED | 11 |
| UNSUPPORTED | 2 |
| NOT ACCESSIBLE | 2 |
| INCONSISTENT | 7 |

Most consequential:
- **B-W1:** the failure share is labelled "weighted" but is unweighted.
- **B-W5:** the paper says Magentic-One's version can be inferred "only from traceback line numbers", but every log states it.
- **B-W2:** timestamps are absent from four frameworks, not two.
- **B-W3:** Table 8's AG2 row contradicts Figure 1.
- **B-W4:** the ChatDev token range is wrong.
- **B-O1:** "mostly inferred" fails for the Opus run.
- **B-I1:** the "8 confirmed" count includes a claim the paper itself calls wrong-layer.
- **B-W7:** a MetaGPT benchmark mislabel affects Appendix B.

#### Issues

| ID | Location (section + quoted sentence) | Problem | Evidence | Required fix |
|---|---|---|---|---|
| B-W1 | §5.3 RQ3: "Weighted to the eligible pool, the annotator found a failure in 79–83% of the MAST-failed traces." | The 79–83% figures are **unweighted** (201/250, 208/250, 197/250). Weighted, they are 80%, 84% and 77%. | `src/afacs/analysis.py` builds the header line with `wilson(len(failed), len(rows))`, which is unweighted. Recomputed with `weighted_share` and the bulk weights: Sonnet r1 80.2% (73–86), Opus 84.0% (78–89), Sonnet r2 77.2% (70–83). | Either write "77–84%" (weighted) or drop "Weighted to the eligible pool" and keep 79–83% as sample shares. Also fix the analysis header so that it is weighted or labelled unweighted. |
| B-W2 | §5.2 RQ2: "Labelled reasoning appears in only two frameworks, and timestamps are absent from two" | Line timestamps are absent from **four** of seven frameworks. Only the composite "log metadata" item is rated absent in two. | `docs/information_audit.md`, timestamp sub-shares: AG2 0%, Magentic 1%, AppWorld 0% ("no timestamps"), HyperAgent 0% ("no timestamps"); MetaGPT, ChatDev and OpenManus 100%. | "timestamps are absent from four (AG2, Magentic-One, AppWorld, HyperAgent)" or "log metadata is absent from two". |
| B-W3 | App C, Table 8 (tab:info), AG2 row: "597 & 15 & 2 & 5 & 8" | Present/partial counts are wrong. They also contradict Figure 1, which shows AG2 "Tool errors" as present. | `info_audit.json` and `.md`: AG2 has 3 present (user prompts, responses, tool errors), 4 partial, 8 absent, 3 n/a. The other six rows match. | Change the AG2 row to 15 / 3 / 4 / 8. The table is probably stale from before the last `afacs-info-audit` run (11:42). Regenerate it from the JSON. |
| B-W4 | §4 Data: "excluding ChatDev (traces of 60,000–500,000 tokens)" | The lower bound is wrong. | `audit.json`, ChatDev kept traces: approx_tokens min 39,927, median 83,893, max 494,824. 64 of 226 kept ChatDev traces are under 60,000. (`design.py` repeats the 60k figure in a comment.) | "about 40,000–495,000 tokens (median 84,000)". |
| B-W5 | App A: "the Magentic-One version could be inferred only from line numbers in a traceback." | False. All 195 raw Magentic logs contain the pip install output, which names the versions. The project's own information audit says so. | The raw `MAD_full_dataset.json` has "Successfully installed … autogen-agentchat-0.4.9 autogen-core-0.4.9 autogen-ext-0.4.9" in 195/195 Magentic rows; the wheels are built from a local `/autogen_python` checkout. `docs/information_audit.md` (System configurations, Magentic): "Scaffolding package versions (autogen 0.4.9) appear in the install log" (detector 100%). `docs/design_check.md` §5 makes the same wrong claim as the paper. | Say that the install log reports autogen 0.4.9 (built from a local source checkout, so the exact commit is unknown). Remove "only from line numbers". Reconcile design_check.md with information_audit.md. |
| B-W6 | App D, AG2 example: "One run noted that a reviewer could code it as a decision error only" | **All three** runs say this. | `sonnet_bulk_r1` notes: "A reviewer could code this as E2 only." `opus_bulk_r1`: "A stricter reader could drop L1.V2 and keep only L1.E2." `sonnet_bulk_r2`: "A coder could treat the hardcoding as an error rather than a violation." | "All three runs noted that…" (this strengthens the point). |
| B-W7 | App B Model-level comparisons: "(MetaGPT on ProgramDev, Claude against GPT-4o; on ProgramDev-v2, Qwen against CodeLlama…)" | Very likely mislabelled. The MetaGPT Claude group and 100 of the 130 GPT-4o traces (source groups `MetaGPT_ProgramDev2_Claude` and `MetaGPT_ProgramDev2_GPT4o`) are **ProgramDev-v2**. Their `benchmark_name` "ProgramDev" in MAST's metadata is an uncorrected error. In the bulk sample, 16/16 Claude and 14/16 GPT-4o MetaGPT traces come from the "ProgramDev2" groups. | MAST v3 Table 1: "MetaGPT ProgramDev GPT-4o … 30 … MetaGPT ProgramDev-v2 GPT-4o LA 100, MetaGPT ProgramDev-v2 Claude-3.7-Sonnet LA 100". Internal evidence: task `__099` is empty in all five groups `MetaGPT_ProgramDev2_GPT4o`, `MetaGPT_ProgramDev2_Claude`, `ChatDev_ProgramDev2_GPT4o`, `MetaGPT_ProgramDev-v2_Qwen` and `MetaGPT_ProgramDev-v2_CodeLlama`, so they share one task list. The analysis tables likewise label these groups "MetaGPT (ProgramDev)". | Add this to `BENCHMARK_CORRECTIONS` (ProgramDev2 → ProgramDev-v2) and re-run. Then describe the MetaGPT comparison as four models on ProgramDev-v2, plus 2 GPT-4o traces on ProgramDev. In §5.2/App A, add the metadata discrepancy (and note that the information audit's "benchmark_name wrong for OpenManus and imprecise for AG2" misses it). |
| B-O1 | Abstract: "violations in 9–13%, mostly inferred from the act rather than stated". §5.3: "mostly inferred from the act (6%) rather than stated (1%)". §7 Discussion: "the evidence grade showed that most rested on the act rather than on stated reasoning." | True for both Sonnet runs, **not for Opus**. The 13% upper end of the abstract's range is the Opus run, and most of its violations are V? (thin). | Unweighted counts among failures: r1 15 inferred / 5 stated / 3 thin. Opus **12 thin** / 9 inferred / 7 stated. r2 14 inferred (+1 V1 stated) / 7 stated / 3 thin. Weighted Opus: V? 7%, inferred 5%, stated 2% (`analysis_opus_bulk_r1.md`). | Qualify the claim: "in the Sonnet runs, mostly inferred; the Opus run graded more of them thin (V?)". Give the stated/inferred/thin split for each run. |
| B-O2 | §5.3: "…concentrated in HyperAgent … and AG2 … and absent from MetaGPT and AppWorld." App B: "No MetaGPT group carried a violation code. AG2's Olympiad traces … 31% … against none in its GSM-Plus and MMLU traces" | These are Sonnet run 1 only, and are not labelled as such. Other runs contradict "absent" and "none". | Opus: MetaGPT 2 violations (CodeLlama group 12%, MetaGPT 3%) and AG2 GSM-Plus Claude 18% (2/11). Sonnet r2: AG2 MMLU 20% (2/10). Olympiad: 31% / 50% / 38%. | Label these as Sonnet run 1, or rewrite them for all three runs (e.g. "rare in MetaGPT (0–2 traces per run)"). |
| B-O3 | §6 AppWorld: "the annotator's judgement matched the benchmark in 21 of 23." | Holds for two runs, not all three. | Benchmark verdicts for the 23 sampled AppWorld traces (20 fail, 3 pass): r1 matched 21/23. Opus matched 21/23 (one pass coded "unclear"). r2 matched **20/23** (one pass coded "unclear", one fail coded "no"). | "in 21 of 23 (Sonnet run 1 and Opus) and 20 of 23 (Sonnet run 2)". |
| B-O4 | §7 Discussion: "An AI annotator applied the layers consistently, well above MAST's judge on its own labels." | This compares unlike things. Layer presence is 4 coarse binary categories (κ 0.63–0.87). MAST's 0.43 is a mean over 14 fine labels, on 30 Magentic traces only. The like-for-like figure, the mean per-code κ (0.52 / 0.59), is above 0.43, not "well above". App A itself says figures on different traces "are not directly comparable". | `agreement_*.md`; `docs/data_audit.md`. | Compare per-code with per-mode (0.52–0.59 vs 0.43), name the caveats (different traces, different label sets), and drop "well above". |
| B-O5 | §5.3: "The typical violation was an agent reporting results of tool calls it never received, or 'verification' code that only returned a hard-coded answer." | The first pattern is typical. The second is rare: 1 to 3 cases per run. | Keyword scan of violation codings' summaries, notes and evidence. Fabricated or unreceived results: r1 13/23, Opus 20/28, r2 13/25. Hard-coded verification: r1 1, Opus 2, r2 3. | "The typical violation was … ; a few were 'verification' code that only returned a hard-coded answer." |
| B-O6 | §5.5 RQ4: "while a deficient specification was coded in only 6%" (FM-1.1) | Run 1 only. Opus coded L3.4 in 16% of FM-1.1 traces. The sentence gives other-run values for the violation share but not for this figure. | Weighted L3.4 within FM-1.1: r1 5.8%, Opus 15.7%, r2 5.5%. | "in 6% (16% and 6% in the other runs)". |
| B-O7 | §5.3: "99.6–99.9% of about 4000 quotes appeared verbatim in the step cited, and none was absent from the trace" | (a) The match is made after normalising case, whitespace, quote marks and markdown, and allows ellipsis splitting, so "verbatim" is loose. (b) 8 quotes (3/1/4) were "too short to check", so "none absent" is not established for them. Minor. | `src/afacs/quotes.py` (`normalise`, `MIN_CHARS = 5`); `analysis_*.md` quote tables. Totals: 1,350 + 1,328 + 1,350 = 4,028. | "found in the cited step (after normalisation; App B)" and "none of the checkable quotes was absent". |
| B-O8 | App D AG2: "the assistant is told to use Python for calculations, wait for the results, and box its answer only after the queries have run (S1)." | The instruction to wait for results is step 3 of "Case 3" only. S1 also lets the agent "solve it by yourself directly" (Case 2). The unconditional instruction is only to box "after all the queries are run". The paragraph presents a conditional instruction as unconditional, and this bears on violation condition (1). | Trace S1 is the AG2 MathChat prompt template. The same template appears in AG2 v0.7.5 `math_user_proxy_agent.py` (default prompt; the "Wait for me to give the results" step is under Case 3). Sonnet r1's coding of `AG2_GSM_Plus_Claude__000` notes this conditionality. | "is offered three ways to solve the problem and told to box the answer only after its queries have run". |
| B-O9 | App A: "The multi-agent AppWorld set-up and the AG2 MMLU team are MAST's own constructions with unpublished prompts" | True for AppWorld. For AG2, MAST v3 publishes the three-agent topology's system prompts (Appendix L.3–L.5, GSM-Plus case study). Only the MMLU-specific variant is unpublished. Minor. | MAST v3 §H.1 and Appendix L list of contents; `docs/design_check.md` AG2 section ("MMLU variant unpublished"). | "…the AG2 MMLU team adapts MAST's published three-agent topology, with unpublished MMLU prompts". |
| B-O10 | §5.4: "Only two of the annotator's 24 most frequent design claims were wrong outright" | `design_check.md` took the most frequent claims **per framework** (2–6 each, some backed by about 2 traces) from **Sonnet run 1 only**. These are not the 24 most frequent claims overall. Minor. | `docs/design_check.md` header ("from the primary Sonnet run, sonnet_bulk_r1") and the per-claim "~n" counts. | "24 claims, the most frequent for each framework in Sonnet run 1". |
| B-O11 | §1: "It takes up five of Ezell et al.'s open challenges: … reconstruction difficulties with limited data access, and, in part, expertise shortages." | Ezell's Appendix B lists "Reconstruction difficulties" and "Limited data access" as two separate challenges, so the list covers six. Minor wording. | arXiv 2508.14231, Appendix B table (Limited data access is under Privacy and Legal Constraints; Reconstruction difficulties under Operational Constraints). | "six" (or list them separately). |
| B-I1 | §5.4 / Table 5 / Abstract: "only eight held in full" … "Two claims placed a failure at the wrong layer (a run-time fault and an environment set-up problem coded as design)" | The environment set-up claim (OpenManus missing packages) is **counted among the 8 "Confirmed"** ("Confirmed (deployment)"). Under the paper's own codebook, L4.5 covers "a misconfigured environment", so a design code (L4.2) there is wrong-layer. On the paper's own logic, at most 7 held in full. | `docs/design_check.md` OpenManus table ("Confirmed (deployment) … Comes from MAST's environment set-up, not OpenManus's design") and "Two claims put a failure at the wrong layer". `codebook/v1.md` L4.5. | Reclassify it as partly true (7 / 14 / 2 / 1) and update the abstract, §5.4, Table 5 and PILOT_SUMMARY. Or explain why a wrong-layer claim counts as "held in full". |
| B-I2 | §6 intro: "Three short traces, each coded alike by all three runs" | Contradicted within the same section: the Magentic paragraph says L3.2 was coded by "only one run". The code sets differ. | MetaGPT 043: r2 has no L2.3. Magentic 029: r1 adds L3.2, r2 adds L1.E1. AppWorld 000: identical. (`annotations/llm/*.jsonl`) | "each given the same deepest factor and main codes by all three runs". |
| B-I3 | §4: "Worked examples illustrate what the coding records, using evidence that does not depend on judging the agents' code" | The MetaGPT example rests on reading the code ("a pair the table lacks, so the test would fail"), and so does the AG2 example (a constant assigned and printed). | §6 and App D text; traces S3/S6 (MetaGPT 043) and S2 (AG2 150). | "…evidence that does not depend on judging whether the agents' answers are correct". |
| B-I4 | Table 4 caption: "intervals are omitted where either coder gave fewer than three positive or negative answers." | For violation evidence grade, HFACS error type, Ezell functions and the identical code set, no interval was ever computed. `agreement.py` bootstraps only the 8 HEADLINE measures. The stated reason is not the actual reason. | `src/afacs/agreement.py`: `HEADLINE = [...]`; `bootstrap()` loops only over HEADLINE. | "Intervals are given for the headline measures only, and omitted where …". |
| B-I5 | §5.2: "MAST names models without versions." App A: HyperAgent traces "are labelled Claude-3.7-Sonnet" | The dataset metadata names bare models ("Claude"). MAST's *paper* (v3 Table 1) names Claude-3.7-Sonnet, Qwen2.5-Coder-32B-Instruct and CodeLlama-7b-Instruct-hf. The HyperAgent label the paper criticises comes from MAST's paper, not the dataset. | `MAD_full_dataset.json`: HyperAgent `llm_name` "Claude". MAST v3 Table 1: "HyperAgent SWE-Bench Lite Claude-3.7-Sonnet". | "MAST's dataset names models without versions or snapshot dates" and "MAST's paper labels them Claude-3.7-Sonnet". |
| B-I6 | §4: "…five runs launched with an empty task; no record of task success" | App A says "Only 60 traces carry a benchmark verdict in the log", and §6 relies on those verdicts. Minor. | `docs/data_audit.md` (AG2 26/4, AppWorld 26/4). | "no task-success field in MAST's metadata (60 logs carry a verdict)". |
| B-I7 | §4 / App B: "Shares are weighted back to the eligible pool" and "Each trace is weighted by the number of eligible traces it represents" | The weights sum to 867, which is the 893-trace pool minus the 26 MAST-failed calibration traces. So the estimates refer to 867 traces. Minor. | `bulk_sample.csv`: Σweight = 867.0 (AG2 282, MetaGPT 404, Magentic 122, AppWorld 23, OpenManus 23, HyperAgent 13). `sample.py` `pick_bulk` excludes the calibration uids. | Say "the eligible pool excluding the calibration set (867 traces)". |
| B-U1 | App D: MetaGPT_ProgramDev2_GPT4o__099 "The deepest factor is the run's set-up, L4.5 Operation set-up." | Nothing says who coded this trace. It is not in the AI sample: none of the five empty-task traces were sampled, and this one is in `design.SEEN_BY_CODER`. The L4.5 coding is therefore the author's own and unvalidated, while §6 frames the appendix as further examples of the pilot coding. (The step-level claims S2–S5 are correct.) | `bulk_sample.csv` and the annotation files contain no `__099` uid. `src/afacs/design.py` `SEEN_BY_CODER`. | State that the trace was not in the AI sample and that the coding is the author's illustration. |
| B-U2 | §7 Discussion: "violations, though rare, were where MAST's labels were least informative" | No measure of how informative labels are, by category, is reported. The evidence shown is only that FM-1.1 mixes errors and violations (and FM-1.3 and FM-3.2 are similarly split). Minor. | §5.5 results. | Rephrase as "MAST's FM-1.1 does not separate violations from errors". |
| B-N1 | App A: "within every round different traces carry identical label vectors, contradicting the original annotation sheets" | The identical-vector part is verified (2 distinct vectors per round). I could not open the original annotation sheets (MAST GitHub PDFs) because GitHub archive and API access is blocked in this session. | `data/processed/audit.json` human_labelled_file. | Spot-check against the PDF sheets before release, or cite the specific sheet. |
| B-N2 | App A: "In 29 of 30 OpenManus logs the task is printed truncated (the agents received the full text)" | The count is verified (29). The parenthetical claim about what the agents received cannot be checked from the logs or any source I opened. | `audit.json` truncated_task_traces = 29. | Cite the basis (e.g. OpenManus reads the task from a file, per design_check) or soften to "presumably". |

#### VERIFIED items

Abstract and §5 headline numbers
1. LLM judge self-agreement: mean per-mode κ 0.43. Evidence: `audit.json` macro_kappa 0.432.
2. κ 0.63–0.76 between models (L3 0.628 to L1 0.764) and 0.74–0.87 between runs. Evidence: `agreement_*.json`; recomputed with `agree.py`.
3. Individual codes 0.52 and 0.59. Evidence: recomputed 0.516 / 0.588.
4. Supervision (L3.1–L3.3) 67% (59–75%), other runs 69% and 71%. Evidence: recomputed weighted 67.0 (58.6–74.5), 69.2, 71.2.
5. Coordination (L2.3) 40% (32–48%), other runs 41% and 41%. Evidence: recomputed 39.9 (31.9–48.5), 41.3, 40.9.
6. Violations 9% (5–15%), other runs 13% and 10%. Evidence: recomputed 9.0 (5.2–15.1), 13.3, 9.6.
7. Run 1: inferred 6%, stated 1%; HyperAgent 69%, AG2 24%. Evidence: recomputed 6.5%, 1.0%, 69.2%, 24.0%.
8. Unsafe act in all failures; L2–L4 factor in 85–91%. Evidence: recomputed 100% each; 87.6 / 84.7 / 91.3.
9. L4 in 63–74% of failures and usually the deepest layer. Evidence: 70.0 / 63.3 / 74.2; deepest L4 70 / 63 / 74%.
10. No run left L1 empty. Evidence: 0 of 201, 208 and 197 failure codings.
11. Confidence "medium" in 86–87% of codings. Evidence: 86.4%, 86.8%, 86.8%.
12. Low vs medium confidence: the Sonnet runs agree on failure_observed in 67% vs 96%. Evidence: 16/24 vs 207/216, conditioned on run 1's rating. (Conditioned on run 2's rating it is 56% vs 97%; worth stating the basis.)
13. 750 codings, all valid, no refusals or errors. Evidence: 250 × 3 records, `error` null, no validation_errors.
14. Models claude-sonnet-5-5 ×2 and claude-opus-5-5, codebook v1, prompt annotator_v1, one instruction hash. Evidence: annotation metadata (requested = served).
15. Headless Claude Code, tools disabled, system prompt replaced, JSON schema with enumerated codes. Evidence: `annotate.py` (`--tools ""`, `--system-prompt`, `--json-schema`).
16. Quote shares: Sonnet 99.6%, 99.6%; Opus 99.9%; about 4,000 quotes. Evidence: 1,344/1,350, 1,327/1,328, 1,344/1,350 (total 4,028); 0 not found.

Table 4 (tab:rq3)
17. Every κ and every 95% interval in Table 4. Evidence: matches `agreement_*.md`; bootstrap re-run (seed 7, 2,000 resamples) reproduces every interval.
18. Identical full code set 24% and 40%. Evidence: `exact_code_set` 0.24 / 0.40.
19. Weakest codes L4.3 (0.19 / 0.23), L1.V? (0.11 / −0.01, "about zero"), L3.2 and L3.4 within 0.32–0.62. Evidence: per-code κ in `agreement_*.md`.
20. Error types vs Ezell functions about equally consistent. Evidence: 0.55 vs 0.58; 0.71 vs 0.70.

RQ1, RQ4 and Figure 3
21. Skill-based errors always paired with action, decision errors mostly with decision, perceptual errors with understanding and observation, in all runs. Evidence: E1 56/56, 99/99, 60/60.
22. The prediction is removed in v1.1; v1.1 differs only in that note. Evidence: `diff codebook/v1.md codebook/v1.1.md`.
23. FM-1.1 (n=79): 17% violations, with 22% and 12% in the other runs. Evidence: 16.5 / 22.2 / 12.3%.
24. FM-1.1 L3.4 6% (run 1). Evidence: 5.8% (see B-O6 for the other runs).
25. L2.3 in 52% of FM-2.3 and 62% of FM-2.5. Evidence: 51.8%, 62.2%.
26. FM-1.3: L4.1 60% vs L3.3 27%. FM-3.2: L3.1 69% and L4.1 69%. Evidence: 59.8 / 27.4; 69.4 / 68.8. (FM-1.3 direction holds in all runs.)
27. Figure 3 values. Evidence: match `analysis_sonnet_bulk_r1.md` RQ4 table (weighted).

Sample, pool and audit numbers
28. 1,642 rows; 1,537 distinct texts. Evidence: raw JSON recount.
29. Seven frameworks; MAST-Data revision 95118ac; CC-BY-4.0; o1 judge; 14 labels. Evidence: HF API (sha 95118ac…, license cc-by-4.0); file SHA-256 values match `design.py`.
30. A group of 100 rows holds 30 distinct texts (ChatDev–CodeLlama); 96 corrupt plus 4 no-label. Evidence: raw recount.
31. Exclusion table 1,505 / 96 / 35 / 4 / 2 = 1,642. Evidence: `traces.jsonl` quality_exclusion counts.
32. 65 duplicate groups, 166 rows, 59 with differing labels. Evidence: `audit.json`.
33. Magentic test–retest: 30 pairs, range −0.05 to 0.67, raw agreement 0.80, 4 identical pairs. Evidence: `audit.json`.
34. Pooled κ would be 0.54. Evidence: recomputed 0.540 (`pooled.py`).
35. ChatDev–CodeLlama −0.04 over 111 pairs. Evidence: `audit.json`.
36. Five runs with an empty task. Evidence: `audit.json` empty_task_traces (5).
37. Eligible pool 893 failed and 373 clean; AG2 286, MetaGPT 408, Magentic 127, AppWorld 27, OpenManus 27, HyperAgent 18. Evidence: `audit.json`.
38. Exclusion of traces over 30,000 tokens and of ChatDev. Evidence: `design.py`.
39. Sample allocation AG2 64, AppWorld 23, HyperAgent 13, Magentic 63, MetaGPT 64, OpenManus 23 (250). Evidence: `bulk_sample.csv`.
40. Four frameworks ran a single model; "Claude" carries no version. Evidence: kept-trace models per framework; dataset `llm_name`.
41. OpenManus is GAIA; AG2 "GSM" is GSM-Plus (corrected). Evidence: `design.py`; MAST v3 Table 1 ("GSMPlus").
42. 29 of 30 OpenManus logs have a truncated task. Evidence: `audit.json` (but see B-N2).
43. Human-labelled file has 19 traces, not 21. Evidence: `audit.json`; MAST v3 says "21 traces"; HF README lists 19.
44. 60 traces carry a benchmark verdict (AppWorld 30, AG2 GSM-Plus 30). Evidence: `traces.jsonl` benchmark_outcome.
45. Calibration set: 30 traces (26 failed, 4 controls; 18 dev, 12 test), no overlap with the bulk sample, fingerprint matches. Evidence: `calibration_key.csv`; recomputed key fingerprint 90fbd248… equals the committed `.sha256`.
46. 425 of 430 MetaGPT traces follow Coder, Tester, Reviewer, Tester, Reviewer. Evidence: role-sequence recount.

RQ2 and the information audit
47. Responses and actions present in all 7 frameworks. Evidence: `info_audit.json`.
48. No framework provides system documentation, artefacts or access. Evidence: all 7 rated absent.
49. No framework logs a seed; only ChatDev logs sampling settings. Evidence: configuration sub-shares.
50. Only ChatDev logs system prompts (rated present; AG2 and Magentic partial). Evidence: `info_audit.json`.
51. The only logged model identifier (ChatDev) contradicts MAST's metadata for one group of 30 traces. Evidence: model_identity table (GPT_45 vs GPT-4o, 30 traces).
52. Labelled reasoning in only two frameworks (OpenManus, HyperAgent). Evidence: `info_audit.json`.
53. Table 8: all rows except AG2. Evidence: counts recomputed from JSON.
54. Ezell et al. list 18 information items (their Table 1). Evidence: arXiv 2508.14231 Table 1 (18 rows).
55. Ezell's factor lists (system, contextual, cognitive). Evidence: Ezell Appendix A headings.
56. Ezell cite an agent that reasoned about cheating unit tests (Baker et al.). Evidence: Ezell §2 text.
57. Ezell's open challenges named in §1 exist in their Appendix B. Evidence: Ezell Appendix B (see B-O11 on the count).

MAST and framework facts
58. MAST built from 150 traces; human inter-annotator κ = 0.88. Evidence: MAST v3 ("rigorous analysis of 150 traces … κ = 0.88").
59. o1 judge vs experts κ = 0.77. Evidence: MAST v3 Table 2, "o1 (few shot) … 0.77" (zero-shot o1 was 0.58).
60. MAST describes MetaGPT as having an explicit verifier. Evidence: MAST v3: "Systems with explicit verifiers like MetaGPT and ChatDev…"; B.2: "agents such as a Coder and a Verifier".
61. MetaGPT ran as the three-role example; the reviewer comments only on the tests; the coder never revises. Evidence: MetaGPT v0.8.2 example (`SimpleWriteReview`: "Review the test cases and provide one critical comments"; `SimpleCoder._watch([UserRequirement])`).
62. The HyperAgent traces come from SWE-bench submission `20240925_hyperagent_lite1`. Evidence: MAST `traces/HyperAgent/README.md`.
63. MAST labels them Claude-3.7-Sonnet, a model released later. Evidence: MAST v3 Table 1; Anthropic announcement dated 2025-02-24, after Sept 2024.
64. The submission's metadata names GPT-4o. Evidence: `metadata.yaml`: `model: gpt-4o-2024-08-06`.
65. The multi-agent AppWorld set-up is MAST's own. Evidence: MAST v3: "We create a multi-agent system over AppWorld derived from the baseline ReAct agent".
66. Magentic-One's 20-turn budget. Evidence: agbench GAIA `scenario.py` (v0.4.7 and v0.4.9): `max_turns=20`.
67. The orchestrator asks itself each turn whether it is in a loop and re-plans on stall. Evidence: v0.4.9 `_prompts.py` ("Are we in a loop…"); orchestrator `is_in_loop` and n_stalls; `max_stalls` default 3.
68. OpenManus's duplicate-response detector only adds a prompt. Evidence: base.py @964b2af: `is_stuck()` → `handle_stuck_state()` prepends "Observed duplicate responses…"; it does not stop the run.
69. MathChat detects repeated results. Evidence: AG2 v0.7.5 proxy: `if self.last_reply == reply` → "Your query or result is same from the last…"; 26 of 429 MathChat traces.
70. HyperAgent's editor rejects edits that fail a syntax check. Evidence: HyperAgent `gen_tools.py` (main) runs autopep8 then flake8 (`E999` etc.) and writes the file only on exit 0. The paper's tool table says it is "addressing syntax and indentation issues". (I checked the main branch, not the Sept-2024 commit.)
71. WebSurfer works from screenshots and can open local files. Evidence: autogen-ext v0.4.9 `_multimodal_web_surfer.py` (set-of-mark screenshot; `visit_url` accepts `file://`). Image handling is absent from FileSurfer.
72. Design-check table: 24 / 8 / 13 / 2 / 1 and the per-framework rows. Evidence: matches `docs/design_check.md` (but see B-I1).
73. HFACS reliability κ = .71 on 319 causal factors, coded by an aviation psychologist and a pilot. Evidence: DOT/FAA/AM-01/3, p.7–8.

Worked examples (step claims checked against `traces.jsonl` and the three annotation files)
74. MetaGPT 043. Checked:
    - Eight-pair table that rejects other pairs (S3).
    - Reviewer suggests an indirect test (S5).
    - kg→oz test added, which the table lacks (S6).
    - Nothing executes code.
    - Reviewer replies in Chinese, approves the tests and reports a non-existent extra bracket (S7).
    - Code never revised.
    - MAST labels 2.6, 3.1, 3.3.
    - All three runs code L4.1, L3.1 and L1 errors.
    - Design check confirms.
75. AppWorld 000. Checked: MAST label 2.6 only; benchmark verdict "pass"; all three runs coded failure_observed = no, noting inefficiencies; 3 of 23 sampled AppWorld traces passed.
76. Magentic 029. Checked:
    - Orchestrator asks FileSurfer to read the image (S5, S7; S3 was a locate request).
    - FileSurfer says it cannot interpret images (S8).
    - OCR install and run (S11–S12) garble the sample-problem section.
    - Assistant works from the OCR text (S14).
    - Unchecked FINAL ANSWER (S15).
    - All three runs code L4.2 as the deepest factor; only Sonnet r1 coded L3.2 (Opus mentions it in notes only).
77. AG2 Olympiad 150. Checked:
    - Code under "Perform calculation/verification" assigns and prints a constant.
    - The answer is boxed in the same turn (S2).
    - The proxy echoes it (S3).
    - The assistant restates it as its result (S4).
    - All three runs code L1.V2, graded inferred.
    - Correctness is not determinable from the log.
    - (See B-O8 and B-W6.)
78. MetaGPT 099. Checked: empty task (S2); placeholder code (S3); template tests (S4); reviewer asks for concrete inputs without noting the missing task (S5); MAST labels 1.1 and 2.2 (see B-U1 on attribution).

