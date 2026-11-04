# Aviation safety science for AI alignment: five working papers

**James Le Cuirot** · CitadelAero

These five papers apply aviation safety science and human factors to problems on Anthropic's AI-safety research agenda. They are **working drafts for author review**. None is peer reviewed. Each sits in its own folder with its sources, audit trail and (where relevant) code and data, so any one can be developed further on its own.

Part of James Le Cuirot's [research repository](../README.md).

| # | Paper | Kind | Version | Read |
|---|---|---|---|---|
| 01 | **Just Culture for Machines:** Why Penalising Disclosure Teaches Concealment | Theory | **v1.0 preprint** | [PDF](01-just-culture-for-machines/paper.pdf) · [LaTeX](01-just-culture-for-machines/paper.tex) |
| 02 | **Do LLM Monitors Miss Rare Threats?** A Pre-registered Test of the Low-Prevalence Effect | Experiment (pre-registered) | **v1.0 preprint** | [PDF](02-do-llm-monitors-miss-rare-threats/paper.pdf) · [LaTeX](02-do-llm-monitors-miss-rare-threats/paper.tex) |
| 03 | **From RSP to SMS:** Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System | Theory and document analysis | **v1.0 preprint** | [PDF](03-from-rsp-to-sms/paper.pdf) · [LaTeX](03-from-rsp-to-sms/paper.tex) |
| 04 | **Checkride or Jump Seat?** What LOSA and Evidence-Based Training Teach About Evaluation Awareness in AI Systems | Theory and a small pilot | **v1.0 preprint** | [PDF](04-checkride-or-jump-seat/paper.pdf) · [LaTeX](04-checkride-or-jump-seat/paper.tex) |
| 05 | **Untrusted by Design:** Bringing AI Control into Aviation's Operational Oversight of AI | Theory and regulatory analysis | **v1.0 preprint** | [PDF](05-untrusted-by-design/paper.pdf) · [LaTeX](05-untrusted-by-design/paper.tex) |

## The papers in brief

**01 Just Culture for Machines.** Aviation learned that when reports of mistakes feed into blame, reporting stops and the mistakes continue. ASRS, ASAP, FOQA, EU Regulation 376/2014 and ICAO Annex 19 solved this with protected reporting, while keeping enforcement based on independent evidence. AI training meets the same incentive problem. If a model's own disclosures (its chain of thought, self-reports, confessions) set the penalty for what they reveal, training can make concealment pay. The paper states the conditions under which that holds and links them to the evidence (Baker et al. 2025 and later work). It reads OpenAI's "confessions" method as a just-culture design and turns aviation's structure into six design principles and five testable predictions.

**02 Do LLM Monitors Miss Rare Threats?** Airport screeners miss far more threats when threats are rare. This pre-registered experiment tested whether AI monitors reviewing code for backdoors do the same. The monitors were Claude Haiku 5.5 and Sonnet 5.5, making 30,880 judgments of items drawn from 419 verified clean/backdoored code pairs. The main prediction was reversed: both monitors caught *more* backdoors when backdoors were rare in a batch, and fewer when backdoors crowded the batch. A stated base rate mattered a little for Sonnet only. A screening-style calibration block did not help and doubled Sonnet's false alarms. Pre-registration, code, data and every raw output are in the folder.

**03 From RSP to SMS.** This paper maps Anthropic's Responsible Scaling Policy, OpenAI's Preparedness Framework (with its compliance framework), Google DeepMind's Frontier Safety Framework and Anthropic's 2026 risk reports, incident investigations and oversight metrics onto the twelve elements of ICAO's Safety Management System. The documents contain more SMS than the headline frameworks suggest. The remaining gaps concern the safety controls themselves: indicators with alert levels for monitors and classifiers, change control for their settings, an occurrence taxonomy and detection latency. The paper proposes twelve AI safety performance indicators to test.

**04 Checkride or Jump Seat?** Models that recognise evaluations may behave differently; crews perform for the examiner. Aviation's two answers are LOSA (non-jeopardy observation of normal flights, the jump seat) and evidence-based training (competencies graded through observable behaviours across varied scenarios). The paper maps both onto alignment evaluation and proposes a "jump-seat layer" and a competency-based alignment assessment. A small pilot found that AI graders agreed with each other only moderately on EBT-style grades: every inter-grader alpha on the grades fell below Krippendorff's 0.667. The rubric was not consistently more reliable than a single holistic score. The real validation step is grading by human EBT instructors.

**05 Untrusted by Design.** EASA's draft Concept Paper Issue 03 (June 2026) puts Level 3 AI inside an independent "operational oversight system", which is in effect a run-time monitor. Its threat model does not treat the AI itself as a possible source of adversarial behaviour. AI-control research does, and has evidence that monitors can be evaded. The paper sets out the EASA texts verbatim and runs a gap analysis of six threats. It proposes means of compliance (monitor classification, managed dissimilarity, red-team control evaluations, human-factors-sized audit budgets, planted-test monitoring, sycophancy tests, occurrence reporting) and ten recommendations. It also covers what aviation assurance offers frontier-AI safety cases. It is timed for EASA's Step 2 NPA, planned for Q2 2027.

## How each paper was produced and checked

1. **Research and drafting** by an AI writing agent working to the house rules in [`STYLE.md`](STYLE.md). Every reference had to be opened and checked, and every number and quotation logged in the paper's `sources.md`.
2. **Independent audit** by a separate AI agent that had not written the paper. It re-checked references and claims against the original sources and, for papers 02 and 04, re-ran the analysis. Findings are in each folder's `AUDIT.md`.
3. **Revision** by the writer against the audit, logged item by item in the folder's `README.md` ("Revision log").
4. **Second-round verification** of the revision by another fresh agent, with any remaining fixes applied. This is appended to `AUDIT.md`.
5. **Paper 02 only:** the design was **pre-registered and committed before data collection** ([`PREREGISTRATION.md`](02-do-llm-monitors-miss-rare-threats/PREREGISTRATION.md)). Clarifications and their timing are recorded in its §9, including one set that git cannot show was written before the main run started.

This is a strong process, but it is not peer review, and AI agents can share blind spots. Treat the drafts as well-sourced starting points that need your expert read.

## Format

Since v0.4 every paper is a LaTeX-typeset, single-column technical report in one house style (`_build/techreport.sty`): Latin Modern on A4, a running header, numbered sections, booktabs tables with captions above, numbered equations, vector figures in a shared colour scheme (one colour per model), and IEEE-style numbered references from `references.bib`. The rules are in [`STYLE.md`](STYLE.md).

## Submission plan

Where each paper could be submitted, with deadlines and the rules on AI-assisted drafting, arXiv endorsement and anonymisation: [`SUBMISSIONS.md`](SUBMISSIONS.md).

## Author review

Decisions taken on the review points are recorded in [`REVIEW_CHECKLIST.md`](REVIEW_CHECKLIST.md).

## Before you publish any of them

- **Read each folder's `NOTES.md` → "What James should check".** These list the judgement calls made on your behalf (framing, analogies, ratings, wording about Anthropic and CitadelAero).
- **ICAO documents.** ICAO's website blocked access, so Annex 19, Doc 9859, Doc 9995 and Doc 9868 were read from copies hosted by other authorities or third parties, and the papers say so. Check the quoted text against your own licensed copies.
- **Annex 19 Amendment 2 applies from 26 November 2026.** It renames some SMS elements and renumbers some provisions. Papers 01 and 03 use the 2nd edition and flag the change.
- **Disclosure statements.** Each paper has an AI-assistance statement and a disclaimer. Several note that many sources are Anthropic's own and that the drafting AI is Anthropic's. Paper 03 has a competing-interests line naming CitadelAero. Keep, edit or extend these as you see fit.
- **Venue formatting.** The LaTeX sources (`paper.tex`, `references.bib`, `paper.bbl`) are arXiv-ready. A journal template needs only the document class and bibliography style swapped.

## Folder layout

```
papers/
├── README.md            this index
├── STYLE.md             house style and citation rules used for all five
├── REVIEW_CHECKLIST.md  author decisions on the review points
├── _build/              LaTeX style, build script, bib checker, figure palette
├── 01-just-culture-for-machines/
├── 02-do-llm-monitors-miss-rare-threats/   (+ PREREGISTRATION.md, code/, data/, results/, figures/)
├── 03-from-rsp-to-sms/
├── 04-checkride-or-jump-seat/              (+ pilot code/, data/, prompts/, results/, figures/)
└── 05-untrusted-by-design/
```

Each paper folder has `paper.tex` and `references.bib` (the source), `paper.pdf` (built), `README.md` (abstract, how to cite, files), `NOTES.md` (author notes: review points, open questions, ideas for developing it, revision log), `sources.md` (verification log) and `AUDIT.md` (independent audit and second-round verification).

## Rebuilding the PDFs

```bash
papers/_build/build.sh                      # all papers
papers/_build/build.sh papers/03-from-rsp-to-sms   # one paper
```

Needs TeX Live with `latexmk` (the script installs the Debian/Ubuntu packages if they are missing). Helper scripts: `_build/check_bib.py` checks every reference against Crossref and arXiv; `_build/compare_text.sh` word-diffs a paper against its v0.3 Markdown.

## Licence

Paper text © 2026 James Le Cuirot. All rights reserved. Code in this repository is under the MIT licence (`LICENSE`). Item data derived from MBPP (paper 02) is released under CC BY 4.0 with attribution to Austin et al. (2021).
