# Just Culture for Machines: Why Penalising Disclosure Teaches Concealment

**James Le Cuirot** · CitadelAero · Preprint v1.0, 4 November 2026. Not peer reviewed.

**[Read the paper (PDF)](paper.pdf)** · Part of the [research repository](../../README.md) · [All papers](../README.md)

## Abstract

Aviation learned that when reports of error feed punishment, people stop reporting and the hazards stay hidden. Its protected arrangements, among them NASA’s Aviation Safety Reporting System, the FAA’s Aviation Safety Action Program and flight data programmes, EU Regulation 376/2014 and ICAO Annex 19, keep the data that safety programmes gather, whether reported or recorded, out of blame and enforcement, leave enforcement to independently obtained evidence, and exclude wilful misconduct and gross negligence from protection. This paper argues that AI training faces a similar incentive structure. When a model’s own disclosures (its chain of thought, self-reports or confessions) set the reward or penalty for the behaviour they disclose, optimisation acts on the disclosure as well as on the behaviour. A simple argument makes the conditions explicit: if the task reward does not already penalise a misbehaviour, and the model can pair it, at no cost in task reward, with a disclosure the monitor scores no worse than an honest one, then no penalty computed only from the disclosure can make good behaviour score higher than concealed misbehaviour. The argument concerns the ordering of rewards, not what training will reach, but experiments that trained reasoning models against chain-of-thought monitors observed the predicted concealment. OpenAI’s confession method, which rewards confessions only for honesty, is in effect a just-culture design. The paper proposes six design principles and five falsifiable predictions, and sets out where the analogy fails: models are not moral agents, and the mechanism is optimisation pressure rather than fear.

## How to cite

```bibtex
@misc{lecuirot2026justculture,
  author       = {Le Cuirot, James},
  title        = {Just Culture for Machines: Why Penalising Disclosure Teaches Concealment},
  year         = {2026},
  howpublished = {Preprint v1.0, 4 November 2026},
  url          = {https://www.lecuirot.je/research/just-culture/}
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
