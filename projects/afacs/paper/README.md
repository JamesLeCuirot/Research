# AFACS paper

`afacs.tex` is the paper; `references.bib` holds its references (IEEE style); `afacs.pdf` is the built copy and `afacs.bbl` is kept for arXiv submission. The layout is the research repository's house style (`papers/_build/techreport.sty`; rules in `papers/STYLE.md`).

## Build

From this folder:

```bash
TEXINPUTS="../../../papers/_build//:" BSTINPUTS="../../../papers/_build//:" latexmk -pdf afacs.tex
```

Figures are read from `../figures/` as vector PDFs (made by `uv run afacs-analysis mast`, `uv run afacs-analysis afacs --run sonnet_bulk_r1` and `uv run afacs-info-audit`, run from `projects/afacs`). The numbers come from `results/`, `docs/` and `data/processed/` (see the comment at the top of `afacs.tex`). The independent audit is in `../AUDIT.md`.

## Versions

| Version | Date | Change |
|---|---|---|
| Preprint v1.0 | 4 Nov 2026 | Released after the independent audit (`../AUDIT.md`) and the author's read-through. |
| Working draft v0.9 | 4 Nov 2026 | House style; independent audit and its fixes. |
