# AFACS paper (draft)

`afacs.tex` is the research paper. Its layout follows a plain LaTeX article style: 10pt A4, Latin Modern, running header, booktabs tables, numbered references.

## Build

From this folder, run pdfLaTeX twice (the second pass resolves cross-references):

```bash
pdflatex afacs.tex
pdflatex afacs.tex
```

Figures are read from `../figures/` (made by `uv run afacs-analysis mast`). Every number in the draft comes from `data/processed/audit.json`, `docs/data_audit.md` or `src/afacs/design.py`. Anything not yet known is marked `[Pending: ...]` in grey via the `\pending{}` macro; search for `\pending` to find them.

On Overleaf: upload `afacs.tex` and put the two PNGs from `figures/` in a `figures/` folder one level up, or change `\graphicspath`.
