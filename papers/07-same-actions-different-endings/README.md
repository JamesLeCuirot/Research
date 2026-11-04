# Same Actions, Different Endings

**Outcome Severity Shifts How AI Models Apply Reason's Culpability Decision Tree to Airline Flight Crews**

James Le Cuirot · CitadelAero · ORCID [0009-0009-6014-1298](https://orcid.org/0009-0009-6014-1298)

**Paper (Preprint v1, 2 October 2026): [`paper/same-actions-different-endings-preprint-v1.pdf`](paper/same-actions-different-endings-preprint-v1.pdf)** · Markdown source: [`paper/preprint-v1.md`](paper/preprint-v1.md)

*Status: Preprint v1, 2 October 2026. Not peer reviewed. Part of James Le Cuirot's [research repository](../../README.md).*

**New title (4 November 2026):** the journal version, and the author's website, use the title *Outcome Bias in AI Models Applying a Culpability Decision Tree to Airline Occurrence Reports: A Pre-registered Within-Case Experiment*. The preprint and OSF record keep the original title. The journal submission package is in [`submissions/`](submissions/).

- **Pre-registration:** OSF, registered 1 October 2026 before any main-study data were collected: https://osf.io/s8q24
- **OSF project with the materials, data and code:** https://osf.io/dhf38 (DOI [10.17605/OSF.IO/DHF38](https://doi.org/10.17605/OSF.IO/DHF38))
- **Licence:** CC BY 4.0 for the text, data and code written for this study (this folder's terms, which take precedence over the repository-wide licence). The ASRS reports in `data/raw/` and `cases/sources/` are NASA's public records.

This folder is a copy of the study as published on OSF. It was carried out in CitadelAero's study repository and moved here on 4 November 2026 so that all of the author's papers sit in one place. Nothing in the study was changed; only this README was rewritten.

## Abstract

Just culture asks that people be judged on what they knew and did at the time, not on how events turned out. This pre-registered, within-case experiment tested whether general-purpose AI models judge identical crew actions as more culpable when an occurrence ends badly. Forty-eight Part 121 flight-crew reports from NASA's Aviation Safety Reporting System (2025) were drawn by a fixed random rule and condensed to a fixed template. Each case exists in two versions that differ only in the outcome: the safe ending as reported, or a fixed, plausible bad ending with minor injuries. Claude Sonnet 5.5, GPT-6.1 Sol and DeepSeek V4 Pro applied Reason's culpability decision tree to each version independently, under two prompt wordings, five times each (2,880 calls, plus 360 on six control cases). The outcome was derived in code from each model's yes/no answers.

All three models reached more culpable outcomes after a bad ending: mean shifts of +0.35, +0.25 and +0.18 steps on Reason's nine-step scale (Holm-adjusted p = .0009, .007, .023). Cases were judged more harshly in 14–18 of 48 cases and more leniently in 2–3. The share of replies pointing to crew culpability rose from 16% to 28% (Claude), 13% to 18% (DeepSeek) and 29% to 33% (GPT). The shift entered mostly through the substitution test. Models gave the same outcome on all five repeats in only 72–82% of cells. Clear control cases were unaffected. A structured just-culture prompt does not protect against hindsight; organisations using AI in occurrence analysis should test for it.

## What is here

| Folder | Contents |
|---|---|
| `protocol/` | The sampling rule, implementation notes, screening guide, case template and endings, prompts and analysis plan, condensing brief, approvals and freeze, and the deviations log (`deviations.md`, D1–D11) |
| `prereg/` | The text submitted to OSF |
| `data/raw/` | The ASRS Database Online export (761 reports, exported 1 Oct 2026), with its search criteria and SHA-256 hash |
| `data/` | The seeded draw order, every screening decision with its reason (`screening-log.csv`, 280 reports), the selected cases and the exclusions |
| `cases/` | The 48 main cases, 2 pilot cases and 6 controls as the models saw them (`cases.json`), and each case's source report (`sources/`) |
| `prompts/` | Reason's tree and the response instructions, exactly as sent |
| `scripts/` | Every step, from the draw (`01_draw.py`) to the registered analysis (`07_analyse.py`) and the paper's tables (`09_paper_tables.py`). Plain Python 3, no third-party packages |
| `results/raw/` | Every model reply: `pilot.jsonl`, and `main.jsonl` with 3,240 valid replies plus every failed or refused attempt, each with model ID, provider, token usage and cost |
| `results/analysis/` | The registered analysis (`summary.md`, `h1.csv`), the descriptive tables (`paper-tables.md`) and the figures |
| `results/sim/` | The simulated data the analysis was tested on before any real reply existed |
| `paper/` | The preprint (Markdown source and PDF) and its build script |

The materials were frozen at git tag `materials-frozen-2026-10-01` (commit `7260f7b`) in the original study repository before any model was run. That tag is recorded on OSF; it is not carried over into this repository.

## Reproducing the results

The analysis needs only Python 3.10 or later. From this folder:

```bash
python scripts/07_analyse.py
python scripts/09_paper_tables.py
```

Both read `results/raw/main.jsonl` and rewrite `results/analysis/`.

To rebuild every prompt without calling any model:

```bash
python scripts/03_run.py --stage dry
```

To run the models again, put an OpenRouter key in a file named `.env` in this folder (`OPENROUTER_API_KEY=...`; the file is git-ignored) and run `python scripts/03_run.py --stage main`. Models change over time, so a new run is a replication, not a copy. The original run used `anthropic/claude-sonnet-5.5`, `openai/gpt-6.1-sol` and `deepseek/deepseek-v4-pro` on 1–2 October 2026.

## How to cite

```bibtex
@misc{lecuirot2026sameactions,
  author       = {Le Cuirot, James},
  title        = {Same Actions, Different Endings: Outcome Severity Shifts How {AI} Models Apply {Reason's} Culpability Decision Tree to Airline Flight Crews},
  year         = {2026},
  howpublished = {Preprint v1, 2 October 2026. Not peer reviewed},
  doi          = {10.17605/OSF.IO/DHF38},
  url          = {https://osf.io/dhf38}
}
```

## Competing interests

The author is the founder of CitadelAero, which builds AI tools for aviation. No CitadelAero product was tested.
