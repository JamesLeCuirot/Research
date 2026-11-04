# Research

**James Le Cuirot** · [CitadelAero](https://citadelaero.com)

Commercial pilot (Senior First Officer), aviation flight safety officer, and aviation safety and compliance consultant specialising in human factors; MSc in Human Factors in Aviation.

This repository holds my research, complete and in progress. Most of it applies aviation safety science and human factors (accident investigation, safety management systems, just culture, crew resource management, monitoring and training) to the safety of AI systems, and to the use of AI in aviation.

## Papers

Every paper has its own folder in [`papers/`](papers/). Click **PDF** to read it.

| # | Paper | Type | Status | Read |
|---|---|---|---|---|
| 01 | **Just Culture for Machines:** Why Penalising Disclosure Teaches Concealment | Theory | Preprint v1.0 (4 Nov 2026). Journal package for *Safety Science* drafted, not submitted ([status](papers/01-just-culture-for-machines/journal/SUBMISSION.md)) | [PDF](papers/01-just-culture-for-machines/paper.pdf) · [folder](papers/01-just-culture-for-machines/) |
| 02 | **Do LLM Monitors Miss Rare Threats?** A Pre-registered Test of the Low-Prevalence Effect | Pre-registered experiment | Preprint v1.0 (4 Nov 2026). Journal package for *TMLR* drafted, not submitted ([status](papers/02-do-llm-monitors-miss-rare-threats/journal/SUBMISSION.md)) | [PDF](papers/02-do-llm-monitors-miss-rare-threats/paper.pdf) · [folder](papers/02-do-llm-monitors-miss-rare-threats/) |
| 03 | **Applying Aviation Safety Management to Frontier AI:** A Gap Analysis of Developer Safety Frameworks | Theory and document analysis | Preprint v1.1 (4 Nov 2026) | [PDF](papers/03-from-rsp-to-sms/paper.pdf) · [folder](papers/03-from-rsp-to-sms/) |
| 04 | **Observing AI Systems in Normal Operations:** What Aviation's Line Operations Safety Audit and Evidence-Based Training Offer AI Evaluation | Theory and pilot study | Preprint v1.1 (4 Nov 2026) | [PDF](papers/04-checkride-or-jump-seat/paper.pdf) · [folder](papers/04-checkride-or-jump-seat/) |
| 05 | **AI Control for Aviation:** A Gap Analysis of EASA's Operational Oversight Objectives for Advanced AI | Theory and regulatory analysis | Preprint v1.1 (4 Nov 2026) | [PDF](papers/05-untrusted-by-design/paper.pdf) · [folder](papers/05-untrusted-by-design/) |
| 06 | **Extending AI-Agent Incident Analysis to Multi-Agent Systems: AFACS**, an HFACS-Based Framework, and an Audit of Public Traces | Framework and empirical study | Preprint v1.0 (4 Nov 2026). AI coding pilot complete (750 codings); human-coder validation planned. Journal package for *TMLR* drafted, not submitted ([status](papers/06-afacs/journal/SUBMISSION.md)) | [PDF](papers/06-afacs/paper.pdf) · [folder](papers/06-afacs/) |
| 07 | **Outcome Bias in AI Models Applying a Culpability Decision Tree to Airline Occurrence Reports:** A Pre-registered Within-Case Experiment (preprint title: *Same Actions, Different Endings*) | Pre-registered experiment | Preprint v1 (2 Oct 2026), on [OSF](https://doi.org/10.17605/OSF.IO/DHF38). Journal package for *Safety Science* drafted, not submitted ([status](papers/07-same-actions-different-endings/journal/SUBMISSION.md)) | [PDF](papers/07-same-actions-different-endings/paper/same-actions-different-endings-preprint-v1.pdf) · [folder](papers/07-same-actions-different-endings/) |

None is peer reviewed yet. Journal packages and where each paper could be submitted: [`papers/SUBMISSIONS.md`](papers/SUBMISSIONS.md).

**Research agenda:** [`agenda/`](agenda/) holds 17 proposals for applying aviation safety science to AI alignment; papers 01–05 grew out of five of them.

## How the repository is organised

```
Research/
├── README.md        this index
├── CITATION.cff     how to cite the repository
├── LICENSE          MIT licence for code
├── papers/          one folder per paper (see below), plus what they share:
│   ├── _build/          LaTeX style (techreport.sty), build script, reference checker
│   ├── STYLE.md         house style
│   ├── REVIEW_CHECKLIST.md  author decisions on review points
│   └── SUBMISSIONS.md   where each paper could be submitted
└── agenda/          research proposals not yet written up
```

Every paper folder is laid out the same way:

| File or folder | What it is |
|---|---|
| `README.md` | Start here: abstract, status, how to cite |
| `paper.pdf`, `paper.tex`, `references.bib` | The preprint and its source (07 is in Markdown, under `paper/`, as deposited on OSF) |
| `journal/` | The journal submission version and its cover letter, once one is being prepared |
| `sources.md` | The check of every reference against its source |
| `AUDIT.md` | The independent audit and how each finding was resolved |
| `NOTES.md` | Author notes: open points, version log |
| `code/`, `data/`, `results/`, ... | For empirical papers: the code, data and every raw output |

Gaps, being filled before journal submission: 06 has no `sources.md` yet (its reference checks are in `AUDIT.md`); 07 has neither `sources.md` nor `AUDIT.md`, because it was produced under CitadelAero's study process (pre-registered, with every case checked by the author against its source report).

New work gets the next number in `papers/` and a row in the table above.

## How the work is produced and checked

- **Sources are verified.** Every reference is opened and checked, and the claim it supports is logged in the paper's `sources.md`.
- **Papers are audited independently.** Each paper is audited by a reviewer that did not write it, revised, and checked again. The trail is in `AUDIT.md`.
- **Experiments are pre-registered.** Their design is committed before data collection, and deviations are recorded with dates.
- **AI assistance is disclosed.** Each paper states that literature search, drafting, verification and (where relevant) code were done with AI assistance (Claude, Anthropic) under the author's direction, and that the author is responsible for the final text.
- **Nothing is peer reviewed yet.** Working papers are labelled with their version.

## Citing

Each paper's `README.md` gives a BibTeX entry. To cite the repository as a whole, use [`CITATION.cff`](CITATION.cff) (GitHub's "Cite this repository" button).

## Licence

Paper text © 2026 James Le Cuirot. All rights reserved. Code is under the MIT licence ([`LICENSE`](LICENSE)). Two exceptions:

- **Paper 07** (Same Actions, Different Endings) was published under CC BY 4.0 for its text, data and code, and keeps that licence.
- **Item data derived from MBPP** (paper 02) are released under CC BY 4.0 with attribution to Austin et al. (2021).

The views expressed are the author's own and do not represent those of any employer or regulator.
