# Research

**James Le Cuirot** · [CitadelAero](https://citadelaero.com)

Commercial pilot (Senior First Officer), aviation flight safety officer, and aviation safety and compliance consultant specialising in human factors; MSc in Human Factors in Aviation.

This repository holds my research, complete and in progress. Most of it applies aviation safety science and human factors (accident investigation, safety management systems, just culture, crew resource management, monitoring and training) to the safety of AI systems, and to the use of AI in aviation.

## Research index

| Work | Type | Status | Where |
|---|---|---|---|
| **Extending AI-Agent Incident Analysis to Multi-Agent Systems: AFACS**, an HFACS-based framework and an audit of public multi-agent traces | Framework and empirical study | **In progress.** Paper draft written and AI coding pilot complete (250 traces); human-coder validation planned as a second study | [`projects/afacs/`](projects/afacs/) |
| **Just Culture for Machines:** Why Penalising Disclosure Teaches Concealment | Theory | **Preprint v1.0** (4 Nov 2026), not peer reviewed | [`papers/01-just-culture-for-machines/`](papers/01-just-culture-for-machines/) |
| **Do LLM Monitors Miss Rare Threats?** A Pre-registered Test of the Low-Prevalence Effect | Pre-registered experiment | **Preprint v1.0** (4 Nov 2026), not peer reviewed | [`papers/02-do-llm-monitors-miss-rare-threats/`](papers/02-do-llm-monitors-miss-rare-threats/) |
| **From RSP to SMS:** Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System | Theory and document analysis | **Preprint v1.0** (4 Nov 2026), not peer reviewed | [`papers/03-from-rsp-to-sms/`](papers/03-from-rsp-to-sms/) |
| **Checkride or Jump Seat?** What LOSA and Evidence-Based Training Teach About Evaluation Awareness in AI Systems | Theory and pilot study | **Preprint v1.0** (4 Nov 2026), not peer reviewed | [`papers/04-checkride-or-jump-seat/`](papers/04-checkride-or-jump-seat/) |
| **Untrusted by Design:** Bringing AI Control into Aviation's Operational Oversight of AI | Theory and regulatory analysis | **Preprint v1.0** (4 Nov 2026), not peer reviewed | [`papers/05-untrusted-by-design/`](papers/05-untrusted-by-design/) |
| **Research agenda:** aviation safety science for AI alignment | Proposals | 17 proposals; 5 written up as the papers above | [`agenda/`](agenda/) |

Each paper folder has a PDF, its LaTeX source, a citation block, a verification log for every reference (`sources.md`) and the record of its independent audit (`AUDIT.md`). Empirical work includes its code, data, raw outputs and, where applicable, its pre-registration.

## How this repository is organised

```
Research/
├── README.md        this index
├── CITATION.cff     how to cite the repository
├── LICENSE          MIT licence for code
├── papers/          working papers: one folder per paper, plus the shared LaTeX style (_build/),
│                    house style (STYLE.md) and author review checklist (REVIEW_CHECKLIST.md)
├── projects/        longer-running research projects with their own pipelines
│   └── afacs/       AFACS: layered failure analysis of LLM multi-agent traces (in progress)
└── agenda/          research proposals not yet written up
```

New work goes in `papers/` (a self-contained paper) or `projects/` (a project with a pipeline, data and several outputs), and gets a row in the index above.

## How the work is produced and checked

- **Sources are verified.** Every reference is opened and checked, and the claim it supports is logged in the paper's `sources.md`.
- **Papers are audited independently.** Each paper is audited by a reviewer that did not write it, revised, and checked again. The trail is in `AUDIT.md`.
- **Experiments are pre-registered.** Their design is committed before data collection, and deviations are recorded with dates.
- **AI assistance is disclosed.** Each paper states that literature search, drafting, verification and (where relevant) code were done with AI assistance (Claude, Anthropic) under the author's direction, and that the author is responsible for the final text.
- **Nothing is peer reviewed yet.** Working papers are labelled with their version.

## Citing

Each paper's `README.md` gives a BibTeX entry. To cite the repository as a whole, use [`CITATION.cff`](CITATION.cff) (GitHub's "Cite this repository" button).

## Licence

Paper text © 2026 James Le Cuirot. All rights reserved. Code is under the MIT licence ([`LICENSE`](LICENSE)). Item data derived from MBPP (paper 02) are released under CC BY 4.0 with attribution to Austin et al. (2021).

The views expressed are the author's own and do not represent those of any employer or regulator.
