# Research

**James Le Cuirot** · [CitadelAero](https://citadelaero.com)

Commercial pilot (Senior First Officer), aviation flight safety officer, and aviation safety and compliance consultant specialising in human factors; MSc in Human Factors in Aviation.

I apply what aviation has learned about safety (just culture and protected reporting, safety management systems, incident analysis, monitoring, training and assessment) to the safety of AI systems, and I test how AI behaves when it is used in aviation safety work. This repository holds all of it: each paper with its PDF, sources, independent audit, and, for the experiments, the pre-registration, code, data and every raw model output.

## Start here

If you have ten minutes, read these three.

**[Do LLM Monitors Miss Rare Threats?](papers/02-do-llm-monitors-miss-rare-threats/paper.pdf)** (pre-registered experiment). Airport screeners miss far more threats when threats are rare, and AI control assumes real attacks will be rare. I tested whether LLM monitors show the same low-prevalence effect. Two Claude models made 30,880 judgements of clean and backdoored code. The prediction failed in the opposite direction: both caught *more* backdoors when backdoors were rare (hit rates 0.69 against 0.51 for Haiku, 0.74 against 0.50 for Sonnet, at 2.5% against 50% prevalence), and missed more when several backdoors shared a batch. A calibration block modelled on airport Threat Image Projection did not reliably help.

**[Just Culture for Machines](papers/01-just-culture-for-machines/paper.pdf)** (theory). Aviation learned that if reports of error feed punishment, reporting stops. When an AI model's own disclosures (its chain of thought, self-reports or confessions) set the penalty for what they disclose, training can teach concealment instead of good behaviour. The paper states the conditions under which that holds, links them to experiments that observed it, and turns aviation's protected-reporting institutions into six design principles and five testable predictions.

**[Outcome Bias in AI Models Applying a Culpability Decision Tree to Airline Occurrence Reports](papers/07-same-actions-different-endings/paper.pdf)** (pre-registered experiment; first version titled *Same Actions, Different Endings*). Three general-purpose AI models applied Reason's culpability decision tree to 48 real NASA ASRS occurrences, each in two versions identical except for the ending. All three judged the crew more culpable after a bad ending (mean shifts of +0.18 to +0.35 steps on a nine-step scale; Holm-adjusted p ≤ .023), while clear control cases were unaffected. A structured just-culture instrument did not prevent outcome bias.

## All papers

Each paper has its own folder in [`papers/`](papers/). None is peer reviewed yet; all are preprints.

| # | Paper | What it found | Read |
|---|---|---|---|
| 01 | **Just Culture for Machines:** Why Penalising Disclosure Teaches Concealment | Theory: when disclosure-only penalties make concealment pay, and six design principles from aviation's protected reporting | [PDF](papers/01-just-culture-for-machines/paper.pdf) |
| 02 | **Do LLM Monitors Miss Rare Threats?** A Pre-registered Test of the Low-Prevalence Effect | Two Claude monitors caught more backdoors when they were rare, the reverse of the human effect | [PDF](papers/02-do-llm-monitors-miss-rare-threats/paper.pdf) |
| 03 | **Applying Aviation Safety Management to Frontier AI:** A Gap Analysis of Developer Safety Frameworks | Frontier developers' frameworks contain more of ICAO's Safety Management System than they appear to; the gaps are indicators, change control, an occurrence taxonomy and detection latency for their safety controls. Proposes twelve safety performance indicators | [PDF](papers/03-from-rsp-to-sms/paper.pdf) |
| 04 | **Observing AI Systems in Normal Operations:** What Aviation's Line Operations Safety Audit and Evidence-Based Training Offer AI Evaluation | Proposes a "jump-seat" layer and competency-based assessment for AI evaluation; in a small pilot, AI graders agreed only moderately on evidence-based-training grades | [PDF](papers/04-checkride-or-jump-seat/paper.pdf) |
| 05 | **AI Control for Aviation:** A Gap Analysis of EASA's Operational Oversight Objectives for Advanced AI | EASA's draft guidance does not treat the AI itself as a possible adversary of its own monitor; six threats, means of compliance and ten recommendations | [PDF](papers/05-untrusted-by-design/paper.pdf) |
| 06 | **AFACS:** Extending AI-Agent Incident Analysis to Multi-Agent Systems, an HFACS-Based Framework, and an Audit of Public Traces | An HFACS-based framework for failures of multi-agent AI systems; an audit of a public dataset (duplicate traces, an LLM judge agreeing with itself at κ 0.43); an AI coding pilot (human validation next) | [PDF](papers/06-afacs/paper.pdf) |
| 07 | **Outcome Bias in AI Models Applying a Culpability Decision Tree to Airline Occurrence Reports** (first version: *Same Actions, Different Endings*) | AI models judged identical crew actions more culpable when the occurrence ended badly | [PDF](papers/07-same-actions-different-endings/paper.pdf) |

**Research agenda:** [`agenda/`](agenda/) holds 17 proposals for applying aviation safety science to AI safety; papers 01–05 grew out of five of them.

## What I'm working on now

- **Permanent DOIs.** Each preprint is being deposited on Zenodo ([`papers/ZENODO.md`](papers/ZENODO.md)); paper 07 already has one on OSF.
- **Journal submissions, one paper at a time.** Each paper's `submissions/` folder holds the version prepared for each journal and its status. The plan and the journal options are in [`papers/SUBMISSIONS.md`](papers/SUBMISSIONS.md) and [`papers/JOURNAL_OPTIONS.md`](papers/JOURNAL_OPTIONS.md).
- **Next studies:** validating AFACS with independent human coders (the blinded calibration set is frozen); testing whether withholding the outcome removes the outcome bias in paper 07; and repeating the monitor experiment in paper 02 with models from other developers.

## How the work is produced and checked

- **Sources are verified.** Every reference is opened and checked, and the claim it supports is logged in the paper's `sources.md`.
- **Papers are audited independently.** Each paper is audited by a reviewer that did not write it, revised, and checked again. The trail is in `AUDIT.md`.
- **Experiments are pre-registered.** Their design is committed before data collection, and deviations are recorded with dates.
- **AI assistance is disclosed.** Literature search, drafting, verification and code were done with AI assistance (Claude, Anthropic) under my direction, and each paper says so. I am responsible for the final text.

## How the repository is organised

```
Research/
├── README.md        this page
├── CITATION.cff     how to cite the repository
├── LICENSE          MIT licence for code
├── papers/          one folder per paper, plus what they share:
│   ├── _build/              LaTeX style, build script, reference checker
│   ├── SUBMISSIONS.md       submission plan and status
│   ├── JOURNAL_OPTIONS.md   journals checked for each paper
│   ├── STYLE.md             house style
│   └── REVIEW_CHECKLIST.md  author decisions on review points
└── agenda/          research proposals not yet written up
```

Every paper folder is laid out the same way:

| File or folder | What it is |
|---|---|
| `README.md` | Abstract, status, how to cite |
| `paper.pdf`, `paper.tex`, `references.bib` | The preprint and its source (07 has its reference list in `paper.tex`, with no `references.bib`, and also keeps its first version, in Markdown under `paper/`, as deposited on OSF) |
| `submissions/<journal>/` | The version prepared for one journal, with its cover letter and a `SUBMISSION.md` (why that journal, what changed, status) |
| `sources.md` | The check of every reference against its source |
| `AUDIT.md` | The independent audit and how each finding was resolved |
| `NOTES.md` | Open points and version log |
| `code/`, `data/`, `results/`, ... | For empirical papers: the code, data and every raw output |

06 has no `sources.md` yet (its reference checks are in `AUDIT.md`), and 07 has neither `sources.md` nor `AUDIT.md`, because it was produced under CitadelAero's study process (pre-registered, with every case checked by the author against its source report). New work gets the next number in `papers/` and a row in the table above.

## Citing

Each paper's `README.md` gives a BibTeX entry. To cite the repository as a whole, use [`CITATION.cff`](CITATION.cff) (GitHub's "Cite this repository" button).

## Licence

Paper text © 2026 James Le Cuirot. All rights reserved. Code is under the MIT licence ([`LICENSE`](LICENSE)). Two exceptions:

- **Paper 07** was published under CC BY 4.0 for its text, data and code, and keeps that licence.
- **Item data derived from MBPP** (paper 02) are released under CC BY 4.0 with attribution to Austin et al. (2021).

The views expressed are my own and do not represent those of any employer or regulator.
