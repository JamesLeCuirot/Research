# House style for the papers in this folder

All five papers use one format: a **LaTeX-typeset, single-column technical report** in the style of an engineering research paper or preprint, not tied to any journal template. The shared style is `papers/_build/techreport.sty`; build with `papers/_build/build.sh`.

## Files in each paper folder

| File | What it holds |
|---|---|
| `paper.tex` | The paper (source of truth). |
| `references.bib` | BibTeX entries for every cited work, rendered in IEEE style (`IEEEtran.bst`). |
| `paper.pdf` | Built by `papers/_build/build.sh`. Do not edit by hand. `paper.bbl` is kept for arXiv submission. |
| `figures/` | Figures as vector PDF (Matplotlib, shared palette in `papers/_build/palette.py`). |
| `README.md` | Author summary: abstract, status, checks, open questions, development ideas, revision log. |
| `sources.md` | Verification log: how each reference was verified and the exact claims it supports. |
| `AUDIT.md` | Independent audit and second-round verification. |
| `code/`, `data/`, `results/` | Empirical papers only. |

## Typesetting and layout (set by `techreport.sty`)

- Latin Modern serif, A4, single column, generous margins, 11 pt.
- Running header on every page: short title left (`\shorttitle{...}`), author right, rule underneath. Page number centred in the footer.
- Simple title block: bold title, author (with a credentials footnote), affiliation, date line. No masthead and no keywords.

## Preamble (identical in every paper except the title fields)

```latex
\documentclass[11pt]{article}
\usepackage{techreport}
\title{Full Title: Subtitle}
\shorttitle{Short Title}
\author{James Le Cuirot\thanks{Commercial pilot (Senior First Officer), aviation flight safety officer, and aviation safety and compliance consultant specialising in human factors; MSc in Human Factors in Aviation.}\\[2pt] \normalsize Citadel Aero}
\date{Working draft v0.4, 4 November 2026. Not peer reviewed.}
```

## Structure

Abstract; numbered sections (`\section`) and subsections (`\subsection`); an unnumbered **Acknowledgement** section (`\section*{Acknowledgement}`); References. Within sections, use **bold run-in paragraph headings** with `\paragraph{Heading.} Text...`. Appendices, if any, come after the references (`\appendix`).

## Standard closing text (Acknowledgement section)

Use these run-in paragraphs, in this order, in every paper. Square-bracketed parts apply only where stated.

```latex
\section*{Acknowledgement}
\paragraph{AI assistance.} Literature searches, drafting and source verification were carried out with AI assistance (Claude, Anthropic) under the author's direction[, as were the experimental code and analysis]. An independent AI-assisted audit checked the references, quotations[ and analysis] against their sources, and its findings were addressed before this version. The author is responsible for the final text. Several of the AI-safety sources cited are research reports by Anthropic, the developer of the assistant used. [Paper-specific sentence where Claude models were also study material, e.g. generator, monitors, transcript authors or graders.]
\paragraph{Competing interests.} The author is the founder of Citadel Aero, which builds AI tools for aviation.
\paragraph{Disclaimer.} The views expressed are the author's own and do not represent those of any employer or regulator. Nothing here is operational, legal or regulatory advice.
\paragraph{Materials.} The verification log and audit record for this paper[, and its code, data and raw outputs,] are at \url{https://github.com/JamesLEC1999/Research/tree/main/papers/<folder>}.
```

## Citations and references

- **Numeric, bracketed, in order of first citation**: `\cite{key}` → [1]; several: `\cite{a,b}` → [1], [2]. Narrative use: `Wolfe et al.~\cite{wolfe2005} showed ...`. Never write author–year citations in the text.
- **IEEE-style list** via `\bibliographystyle{IEEEtran}` and `\bibliography{references}`: initials, quoted article titles, italic venues, vol./no./pp.
- BibTeX entries must carry the verified bibliographic data: full author list (as given by the source), exact title (protect capitals with braces, e.g. `{AI}`, `{ICAO}`), journal/booktitle, volume, number, pages, year, `doi`, and `url` (use `https://doi.org/<doi>` when a DOI exists). Preprints: `@misc` with `howpublished = {arXiv preprint arXiv:XXXX.XXXXX}`. Web pages and blog posts: `@misc` with `howpublished`, `url` and `note = {Accessed: Nov. 3, 2026}`. Regulations and standards: `@misc` or `@manual` with the issuing body as `{{author}}` in double braces, the edition/amendment, and the URL. Where a document was read from a copy not distributed by its publisher, say so in `note`.
- Regulations may also be referred to in text by their legal designation (e.g. "14 CFR §91.25", "Art. 16(6)"), with the citation number where the source is first used.
- Run `uv run --no-project --with bibtexparser==1.4.3 --with requests python papers/_build/check_bib.py <folder>` before finishing; resolve every `CHECK`, `*-NOT-FOUND` and missing key.

## Tables, figures, equations, units, code

- **Tables**: booktabs (`\toprule`, `\midrule`, `\bottomrule`), horizontal rules only, no vertical lines. **Caption above the table.** Where a table comes from a data file, end the caption with `\source{\code{results/RESULTS\_numbers.md}}`; where it summarises documents, cite them. Long tables: `longtable`; wide text tables: `tabularx`.
- **Figures**: Matplotlib, vector PDF, shared style and colours (`palette.py`): one fixed colour per model across every figure in every paper (Haiku orange, Sonnet blue, Opus green). Captions are small with a bold label ("Figure 3:"), set automatically. Use `subcaption` for (a)/(b) panels.
- **Equations**: displayed equations numbered on the right (`equation`, `align`); define every symbol in the text immediately after.
- **Units and numbers**: `siunitx` (`\num{100000}`, `\SI{27000}{kg}`, `\SI{10}{\hour}`), thin-space digit grouping.
- **Code identifiers, file names and model IDs** in monospace: `\code{src/env/aircraft_env.py}`, `\code{claude-haiku-5-5}`.

## Author and voice

- **Impersonal voice** (decision A3): "this paper argues", "the documents were read"; no "I" or "we" outside quotations, so that no check carried out by the AI assistant is presented as the author's own.
- Single author: **James Le Cuirot** (Citadel Aero). Never name his airline employer, and never invent personal anecdotes or experience.
- **British spelling** throughout (behaviour, organisation, optimisation, judgement, centreline). Plain, precise prose: short sentences, defined terms, no hype. Mark analogies as analogies and give their limits.
- Write for two audiences at once: AI-safety researchers who do not know aviation, and aviation safety professionals who do not know AI safety.

## Verification rules (unchanged)

Every reference must have been opened and checked; every number, quotation and specific claim must be traceable in `sources.md`; quotations are verbatim; preprints are labelled as such; nothing is cited from memory alone.

## Things not to do

- Agents do not commit or push; the lead session does.
- Do not edit files outside your own paper folder (except reading shared files).
- No e-mail addresses or personal data.
- No commercial promotion of Citadel Aero.
