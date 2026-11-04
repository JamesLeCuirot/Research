# From RSP to SMS: Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System

**James Le Cuirot** · CitadelAero · Preprint v1.0, 4 November 2026. Not peer reviewed.

**[Read the paper (PDF)](paper.pdf)** · Part of the [research repository](../../README.md) · [All papers](../README.md)

## Abstract

Frontier AI developers publish safety frameworks, such as Anthropic’s Responsible Scaling Policy, OpenAI’s Preparedness Framework and Google DeepMind’s Frontier Safety Framework. In 2026 Anthropic also published risk reports, incident investigations and monitoring statistics. Commercial aviation manages operational safety through the Safety Management System (SMS) defined in ICAO Annex 19: four components and twelve elements, run in practice on safety performance indicators, management of change, occurrence reporting and monitoring of routine operations. This paper maps the three frameworks, OpenAI’s companion compliance framework and Anthropic’s 2026 operational artefacts onto the twelve SMS elements, with the EU General-Purpose AI Code of Practice as a reference point, using documents public on 3 November 2026. The documents contain more SMS-like machinery than a reading of the headline frameworks alone suggests: hazard identification and risk acceptance throughout, incident response plans, security change management and audits, and security detection targets set as goals. The remaining gaps are specific. In the documents assessed, no developer publishes indicators with targets, alert levels and trends for its safety controls, such as monitors and classifiers. None documents a change process aimed at those controls’ settings with hazard assessment. None publishes an occurrence taxonomy or measures detection latency. Training for safety-assurance roles is not described, and independent assurance covers security controls more than safety controls in practice. Anthropic’s oversight metrics (coverage, review latency and escalation rate) are safety performance indicators in all but name. The paper proposes twelve AI safety performance indicators for testing and notes practices aviation could adopt. No prior element-by-element mapping was found.

## How to cite

```bibtex
@techreport{lecuirot2026rsp2sms,
  author      = {Le Cuirot, James},
  title       = {From RSP to SMS: Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System},
  institution = {CitadelAero},
  type        = {Preprint},
  number      = {v1.0},
  year        = {2026},
  month       = nov,
  note        = {Not peer reviewed},
  url         = {https://github.com/JamesLeCuirot/Research/tree/main/papers/03-from-rsp-to-sms}
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
