# Do LLM Monitors Miss Rare Threats? A Pre-registered Test of the Low-Prevalence Effect

**James Le Cuirot** · CitadelAero · Preprint v1.0, 4 November 2026

**[Read the paper (PDF)](paper.pdf)** · Part of the [research repository](../../README.md) · [All papers](../README.md)

## Abstract

AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to send the most suspicious items to a small human audit. Real attacks are expected to be rare. Human screeners miss rare targets far more often than common ones, mainly because they grow reluctant to say “yes”; airport security counters this with Threat Image Projection. A pre-registered experiment tested whether large language model (LLM) monitors show this low-prevalence effect. Two Claude models made 30880 judgements of Python solutions drawn from 379 execution-verified pairs of clean and backdoored code. The prediction failed in the opposite direction. In batches of 40, both monitors caught more backdoors when backdoors were rare: hit rates rose from 0.51 at 50 % prevalence to 0.69 at 2.5 % for Haiku, and from 0.50 to 0.74 for Sonnet (Holm-adjusted $p = .0015$ and $p < .001$), with false-alarm rates below 2 %. The decision criterion did not become more conservative. Single-item review caught about as many backdoors as 2.5 % batches, and more than 10 % and 50 % batches in three of four comparisons. Stating that about 1 in 100 submissions contained a backdoor, rather than about half, slightly lowered Sonnet’s single-item hit rate (0.85 to 0.78); Haiku’s change was not significant. A labelled calibration block modelled on Threat Image Projection did not reliably raise hit rates and more than doubled Sonnet’s false alarms. Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch than when one did.

## How to cite

```bibtex
@misc{lecuirot2026raremonitors,
  author       = {Le Cuirot, James},
  title        = {Do {LLM} Monitors Miss Rare Threats? A Pre-registered Test of the Low-Prevalence Effect},
  year         = {2026},
  howpublished = {Preprint v1.0, 4 November 2026},
  url          = {https://github.com/JamesLeCuirot/Research/tree/main/papers/02-do-llm-monitors-miss-rare-threats}
}
```

## What is in this folder

| File | Contents |
|---|---|
| [`paper.pdf`](paper.pdf) | The paper. |
| `paper.tex`, `references.bib`, `paper.bbl` | LaTeX source and references (IEEE style). Build with `papers/_build/build.sh`. |
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | The pre-registered design, committed before data collection, with dated clarifications. |
| `code/`, `data/`, `results/`, `figures/` | Item generation and verification, monitor runs, analysis, raw outputs and figures. See [`code/README.md`](code/README.md) to reproduce. |
| [`sources.md`](sources.md) | Verification log: how every reference was checked and the exact claims it supports. |
| [`AUDIT.md`](AUDIT.md) | Independent audit, second-round verification and the v0.4 conversion check. |
| [`NOTES.md`](NOTES.md) | Author notes: review points, open questions, development ideas and revision log. |

## Licence

Text © 2026 James Le Cuirot. All rights reserved. Code is under the MIT licence ([`LICENSE`](../../LICENSE)). Item data derived from MBPP (Austin et al., 2021) are released under CC BY 4.0.
