# Observing AI Systems in Normal Operations: What Aviation's Line Operations Safety Audit and Evidence-Based Training Offer AI Evaluation

**James Le Cuirot** · CitadelAero · Preprint v1.1, 4 November 2026. Not peer reviewed.

*Titled "Checkride or Jump Seat? What LOSA and Evidence-Based Training Teach About Evaluation Awareness in AI Systems" up to v1.0.*

**[Read the paper (PDF)](paper.pdf)** · Part of the [research repository](../../README.md) · [All papers](../README.md)

## Abstract

*A conceptual mapping, two proposals and a feasibility pilot of competency-based grading.* Frontier language models can often tell when they are being evaluated, and in some studies they behave better when they say they are being tested. This threatens the validity of pre-deployment safety evaluations. Airline training faced a similar problem: a checkride shows what a crew does while being assessed. It developed two complementary answers. Line Operations Safety Audits (LOSA) put trained observers in the flight-deck jump seat on normal flights under confidential, non-jeopardy conditions, explicitly not as checks, and code threats, errors and undesired aircraft states. Evidence-based training (EBT) assesses competencies through observable behaviours across varied scenarios rather than a fixed list of manoeuvres, and requires assured instructor concordance. This paper maps their design principles onto alignment evaluation, records how far current AI practice already follows them, and states where the analogy fails. It proposes a “jump-seat” layer of privacy-preserving, non-jeopardy observation of deployed models and a competency-based alignment assessment, and shows how the two feed each other. A small feasibility pilot graded 48 model transcripts from six airline-workplace scenarios with an EBT-style rubric and with a single holistic score, by two LLM graders, twice each. Each grader’s two runs agreed at Krippendorff’s alpha 0.56–0.89, but every inter-grader alpha for the grades fell below 0.667, Krippendorff’s minimum for tentative conclusions, and the rubric showed no consistent advantage over the holistic score. Grades separated scenarios. Premature claims that actions had been taken lowered rubric communication grades but not holistic grades. Trained human instructors are the next test.

## How to cite

```bibtex
@misc{lecuirot2026checkride,
  author       = {Le Cuirot, James},
  title        = {Observing {AI} Systems in Normal Operations: What Aviation's Line Operations Safety Audit and Evidence-Based Training Offer {AI} Evaluation},
  year         = {2026},
  howpublished = {Preprint v1.1, 4 November 2026},
  url          = {https://www.lecuirot.je/research/normal-operations/}
}
```

## What is in this folder

| File | Contents |
|---|---|
| [`paper.pdf`](paper.pdf) | The paper. |
| `paper.tex`, `references.bib`, `paper.bbl` | LaTeX source and references (IEEE style). Build with `papers/_build/build.sh`. |
| `code/`, `prompts/`, `data/`, `results/`, `figures/` | Pilot scenarios, rubric, transcripts, grades, analysis and figure. |
| [`sources.md`](sources.md) | Verification log: how every reference was checked and the exact claims it supports. |
| [`AUDIT.md`](AUDIT.md) | Independent audit, second-round verification and the v0.4 conversion check. |
| [`NOTES.md`](NOTES.md) | Author notes: review points, open questions, development ideas and revision log. |

## Licence

Text © 2026 James Le Cuirot. All rights reserved. Code is under the MIT licence ([`LICENSE`](../../LICENSE)).
