# AFACS: author notes

`paper.tex` is the paper; `references.bib` holds its references (IEEE style); `paper.pdf` is the built copy and `paper.bbl` is kept for arXiv submission. The layout is the research repository's house style (`papers/_build/techreport.sty`; rules in `papers/STYLE.md`).

## Build

From the repository root:

```bash
papers/_build/build.sh papers/06-afacs
```

Figures are read from `figures/` as vector PDFs (made by `uv run afacs-analysis mast`, `uv run afacs-analysis afacs --run sonnet_bulk_r1` and `uv run afacs-info-audit`, run from this folder). The numbers come from `results/`, `docs/` and `data/processed/` (see the comment at the top of `paper.tex`). The independent audit is in `AUDIT.md`.

## Versions

| Version | Date | Change |
|---|---|---|
| Preprint v1.1 | 4 Nov 2026 | Layer agreement now reported on the traces both coders judged failed (between models κ 0.49–0.68), leading in the abstract and results, with a new appendix table (`results/agreement_both_failed.md`); the all-trace figures are kept with the reason they are higher. Claims softened and caveats added after an independent check of the journal version: AI-coded prevalence, "quotes were genuine", the MAST judge comparison for context only, reasoning logged in two frameworks, the AppWorld base rate, and the design check made by AI agents in one pass. |
| Preprint v1.0 | 4 Nov 2026 | Released after the independent audit (`AUDIT.md`) and the author's read-through. Same day: the project moved from `projects/afacs/` to `papers/06-afacs/` and the paper's two repository paths were updated; the text is otherwise unchanged. |
| Working draft v0.9 | 4 Nov 2026 | House style; independent audit and its fixes. |

## Open items

- **B-N1 (from the audit):** the MAST annotation sheets were not re-checked against the paper's MAST figures.
- **No `sources.md` yet.** The other papers keep a reference-by-reference verification log; for AFACS the checks are in `AUDIT.md` and the automatic Crossref/arXiv check (`papers/_build/check_bib.py`). A `sources.md` should be written before journal submission.
