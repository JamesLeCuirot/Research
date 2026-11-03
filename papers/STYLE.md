# House style for the papers in this folder

These rules apply to every paper under `papers/`. They exist so that each paper can be reviewed, cited and developed further without surprises.

## Files in each paper folder

| File | What it holds |
|---|---|
| `paper.md` | The paper. Pandoc Markdown with a YAML header (below). This is the source of truth. |
| `README.md` | One-page summary for the author: abstract, status, what to check, open questions, ideas for developing it further. |
| `sources.md` | Verification log. One entry per reference: how it was verified (URL/DOI opened, date), and the exact claim(s) in the paper it supports, with a short verbatim quote or locator (section, page, table) from the source. |
| `paper.pdf` / `paper.html` | Built from `paper.md` by `papers/_build/build.sh`. Do not edit by hand. |
| `code/`, `data/`, `results/`, `figures/` | Only for papers with empirical work. |

## YAML header for `paper.md`

```yaml
---
title: "Full title"
subtitle: "Optional subtitle"
author: "James Le Cuirot"
affiliation: "Citadel Aero"
date: "Draft v0.1, 3 November 2026"
status: "Working draft for author review. Not peer reviewed."
abstract: |
  150–250 words.
keywords: [comma, separated]
---
```

## Author and voice

- Single author: **James Le Cuirot** (Citadel Aero). Professional background that may be stated: airline Senior First Officer and Flight Safety Officer; MSc in Human Factors in Aviation. **Never name his airline employer** and never invent personal anecdotes, flight experiences, incidents or opinions attributed to him. Where operational experience is relevant, describe the practice from published sources ("in airline operations, ..."), not from invented memory.
- Write in UK English (behaviour, organisation, programme, analyse). Plain, precise academic prose: short sentences, defined terms, no hype. Avoid em-dash asides and rhetorical "not X, but Y" constructions where a plain sentence works.
- Readers are two audiences at once: AI-safety researchers who do not know aviation, and aviation safety professionals who do not know AI safety. Define each side's jargon on first use (for example "reward hacking", "chain of thought", "SMS", "LOSA").
- Make claims no stronger than the evidence. Mark analogies as analogies and give their limits ("disanalogies") explicitly.

## Required sections (theory papers)

Abstract; 1 Introduction (problem, contribution in 3–5 bullets); background on the aviation practice; background on the AI-safety problem; the mapping or argument; proposals/design principles/recommendations; limitations and disanalogies; conclusion; **Acknowledgements and AI-assistance statement**; **Disclaimer**; References. Empirical papers add Methods, Results, Discussion and a link to the pre-registration.

Standard closing statements (adapt wording, keep the substance):

> **AI-assistance statement.** Literature searches, drafting and source verification were carried out with AI assistance (Claude, Anthropic) under the author's direction. The author is responsible for the final text. Every reference was checked against the original source; see `sources.md`.
>
> **Disclaimer.** The views expressed are the author's own and do not represent those of any employer or regulator. Nothing here is operational, legal or regulatory advice.

## Citations

- **Author–date in text, APA 7 reference list.** In text: (Reason, 1997), (Baker et al., 2025), Wolfe et al. (2005). Three or more authors: "et al." from the first citation.
- Reference list: alphabetical by first author. Include DOI as `https://doi.org/...` when one exists; otherwise a stable URL (arXiv abstract page, official page). arXiv: `arXiv:XXXX.XXXXX` plus the abs URL. Regulations and standards: issuing body, title, edition/amendment, year, URL (e.g. "ICAO. (2018). *Safety Management Manual* (Doc 9859, 4th ed.)."). Web pages: include the date accessed (3 November 2026) where the content can change.
- **Every reference must be verified** by opening the abstract page, DOI record, publisher page or official document in this session. If a source cannot be opened, either drop it or say in `sources.md` exactly what was and was not seen. Never cite from memory alone. Never invent page numbers; use section or paragraph locators you actually saw.
- **Every number, quotation and specific factual claim** about a source (percentages, dates, sample sizes, quoted phrases, regulation paragraph numbers) must be traceable in `sources.md` to the place it came from. Quotations must be verbatim.
- Regulation text (FAA, EASA, UK, ICAO) may be checked with the Citadel Aero regulation library MCP tools (`mcp__CitadelAero_Regulations__lookup_citation` / `search_regulations`, loaded with ToolSearch) or the official source. Say whose law it is (EU, UK, US) and whether the text is binding, AMC/GM or guidance.
- Preprints are fine to cite but must be labelled as preprints (arXiv) in the reference list. Do not describe a preprint as peer reviewed.
- Prefer primary sources over secondary summaries. If a figure is only available from a secondary source, say so.

## Length

Theory papers: about 6,000–8,500 words of main text (excluding references). Empirical paper: about 5,000–7,000 words plus figures and tables.

## Things not to do

- No commits or pushes from agents; the lead session commits.
- Do not edit files outside your own paper folder (except reading shared files).
- Do not include the author's email address or any personal data.
- Do not present Citadel Aero commercially; a short, factual "implications for aviation AI developers" paragraph is fine.
