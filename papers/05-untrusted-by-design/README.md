# Untrusted by Design: Bringing AI Control into Aviation's Operational Oversight of AI

**James Le Cuirot** · Citadel Aero · Working draft v0.4, 4 November 2026. Not peer reviewed.

**[Read the paper (PDF)](paper.pdf)** · Part of the [research repository](../../README.md) · [All papers](../README.md)

## Abstract

The European Union Aviation Safety Agency (EASA) is moving its guidance on artificial intelligence (AI) towards run-time oversight. Its draft Concept Paper, Proposed Issue 03 (June 2026), would place Level 3 (“advanced automation”) systems under an independent “operational oversight system” that monitors the AI, overrides it and drives it to a safe state (Objectives DHO-01 to DHO-07). In AI-safety terms this is a run-time monitor. Research on “AI control” has studied such monitors under a stricter assumption than aviation’s: that the monitored system may itself evade or subvert its monitor, collude with other AI components, or behave differently when evaluated. This paper compares the two. It sets out the EASA texts verbatim and shows that their threat model covers random and systematic failure, distribution shift and attackers external to the AI, but not the monitored system as a source of adversarial behaviour. It reviews experimental evidence, mostly from coding and AI-laboratory settings, that current large language models can evade monitors, recognise evaluations, agree with users against the facts and bias their labels when acting as judges. After a gap analysis of six threats, it proposes means of compliance for EASA and EUROCAE: a stricter, aviation-specific classification of monitors as trusted or untrusted, managed dissimilarity, red-team control evaluations, audit budgets sized with human-factors evidence, planted-test monitoring of monitors, sycophancy test methods and occurrence reporting of AI events. In the other direction, it argues that frontier-AI safety cases could adopt aviation’s severity-graded assurance, operational design domains, independent verification and continued airworthiness.

## How to cite

```bibtex
@techreport{lecuirot2026untrusted,
  author      = {Le Cuirot, James},
  title       = {Untrusted by Design: Bringing AI Control into Aviation's Operational Oversight of AI},
  institution = {Citadel Aero},
  type        = {Working paper},
  number      = {v0.4},
  year        = {2026},
  month       = nov,
  note        = {Not peer reviewed},
  url         = {https://github.com/JamesLeCuirot/Research/tree/main/papers/05-untrusted-by-design}
}
```

## What is in this folder

| File | Contents |
|---|---|
| [`paper.pdf`](paper.pdf) | The paper. |
| `paper.tex`, `references.bib`, `paper.bbl` | LaTeX source and references (IEEE style). Build with `papers/_build/build.sh`. |
| [`sources.md`](sources.md) | Verification log: how every reference was checked and the exact claims it supports. |
| [`AUDIT.md`](AUDIT.md) | Independent audit, second-round verification and the v0.4 conversion check. |
| [`NOTES.md`](NOTES.md) | Author notes: review points, open questions, development ideas and revision log. |

## Licence

Text © 2026 James Le Cuirot. All rights reserved. Code is under the MIT licence ([`LICENSE`](../../LICENSE)).
