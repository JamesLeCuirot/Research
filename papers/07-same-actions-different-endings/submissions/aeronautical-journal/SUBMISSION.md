# Paper 07: submission to The Aeronautical Journal

**Journal:** *The Aeronautical Journal* (Royal Aeronautical Society; published by Cambridge University Press), research article.
**Status (4 November 2026):** package ready for James's read and edit, in the journal's template. **First choice for this paper**; the *Safety Science* package (`../safety-science/`) is the fallback if this journal declines. Not yet submitted.

## Why this journal

- **Readers:** operators, investigators, safety managers and regulators, and it is your own society's journal.
- **Single-anonymised review** ("a single-anonymized model of peer review"): reviewers see your name. This removes the anonymity problem the *Safety Science* route had, because the OSF preprint is public.
- **Preprints are fine:** "deposition of a preprint on the author's personal website, in an institutional repository, or in a preprint archive" is not prior publication.
- **AI use is allowed if declared.** Cambridge does not accept AI as an author, and asks you to declare AI use that generates text or analyses data. The manuscript has a declaration section.
- **Length and format:** "Papers should preferably not exceed 10,000 words" (this one has about 6,300 words of main text, including tables); single column; abstract up to 250 words (249); APA references; a nomenclature section is required (included). Journal-style formatting is only required at acceptance.
- **Process:** at least two referees; "typically lasts 3-6 months".
- **Fees:** none on the standard route; open access is optional (£2,610).

Checked on Cambridge's pages on 4 November 2026: [preparing your materials](https://www.cambridge.org/core/journals/aeronautical-journal/information/author-instructions/preparing-your-materials), [review process](https://www.cambridge.org/core/journals/aeronautical-journal/information/peer-review-information/review-process), [fees](https://www.cambridge.org/core/journals/aeronautical-journal/information/author-instructions/fees-and-pricing). The wider list of journals is in `papers/JOURNAL_OPTIONS.md`.

## What this version is

The same text as the *Safety Science* version, which an independent check compared with the preprint token by token, set in **the journal's own LaTeX class** (`aer.cls`, from the template files James downloaded on 4 November 2026), with these changes for this journal:
- your name, affiliation and email on the title page (the journal publishes them; ORCID is entered in Editorial Manager);
- a nomenclature list of every abbreviation and symbol in the text and figures, ordered as the journal asks (alphabetical, lower case before upper case, Greek symbols after);
- first-level headings in capitals and second-level headings in title case, as in the template;
- the end sections in the template's order and headings: Acknowledgements (which now holds the declaration of AI use for writing, with tool, versions and dates, as Cambridge asks), Competing interests, Financial support, Ethics, Data availability, References, Appendix;
- the dates of AI use added to the Method (Section 2.3), where Cambridge asks AI use in data collection and analysis to be declared;
- the two prompt listings in Appendix A labelled as Boxes 2 and 3 (Cambridge asks boxes and code to be labelled and numbered);
- the note on the earlier preprint moved from under the abstract into Data availability, so the abstract stands alone;
- line numbers for the reviewers; the journal's metadata commands left empty, as the template guide asks.

References stay in APA author–year style, as Cambridge's "Preparing your materials" page asks. The template's sample shows the journal's older numbered style; the page says formatting of references is not grounds for rejection at submission.

No number or finding changed.

## Checked against Cambridge's "Preparing your materials" page (4 November 2026)

| Requirement | This manuscript |
|---|---|
| Research Article, preferably under 10,000 words, single column | About 6,300 words of main text including tables, single column |
| Journal template (Word or LaTeX) | `aer.cls` |
| LaTeX: upload the PDF only at first submission | Upload `paper.pdf`; the source is sent after provisional acceptance |
| Abstract up to 250 words, standalone, no references; also pasted into the form | 249 words, no references |
| No keywords in the manuscript | Removed; enter them in the form |
| Nomenclature of all symbols and abbreviations, in the journal's order | Done |
| Tables titled, numbered, cited; figures captioned beneath, numbered in order, cited | Yes |
| Boxes and code snippets labelled and numbered | Box 1 (results), Boxes 2–3 (Appendix A) |
| Footnotes in Roman numerals | None used |
| APA in-text citations | Yes |
| Competing interests in the manuscript | Yes |
| Financial support section | Yes |
| AI use declared: writing in the acknowledgements, analysis in the methods, with tool, version, dates and access | Yes, except your own sentence (below) |
| Alt text for figures (accessibility form, or machine-generated and checked at proof) | Drafted below |
| Organisation and address for each author | "CitadelAero, Jersey, Channel Islands"; add a fuller postal address if you want one printed |

## Before you submit

1. ~~Decide CitadelAero's rule.~~ **Decided 4 November 2026:** James, as founder, overrides the company research plan's "No preprint or journal submissions" rule for this paper. Note it in CitadelAero's own records too.
2. **Read and edit the manuscript in your own words.** Then replace the placeholder `[AUTHOR TO DESCRIBE HIS OWN REVISION OF THE MANUSCRIPT]` in the "Use of AI" paragraph of the Acknowledgements in `paper.tex` with what you did, and rebuild (`latexmk -pdf paper.tex` in this folder).
3. **Read `cover_letter.txt`** and adjust it to your voice.

## How to submit

1. Go to the journal's submission system, **Editorial Manager**: https://www.editorialmanager.com/aeroj/ (checked 4 November 2026 on Cambridge's "submitting your materials" page). It needs its own account, separate from Cambridge Core. Link your ORCID (0009-0009-6014-1298), which the journal requires for the corresponding author. Queries go to aerojournal@aerosociety.com.
2. **Keywords go in the online form, not the manuscript** (the journal's rule; the manuscript's keywords line was removed on 4 November 2026). Use: just culture; outcome bias; hindsight bias; large language models; culpability; aviation safety reporting.
3. Choose the article type **Research Article**, and a main and a secondary subject classification that fit (likely human factors, safety, or air transport operations, from the journal's list; the guidance warns that a wrong classification can lead to an out-of-scope rejection).
4. Upload `paper.pdf` only (Cambridge: "The LaTeX source file should not initially be submitted alongside the PDF"). Paste the abstract into its box, and paste in the cover letter.
   - **Alt text** (Cambridge's accessibility form, if offered; otherwise check the machine-generated text at proof):
     - *Figure 1:* Dot plot in three rows, one per model (Claude Sonnet 5.5, GPT-6.1 Sol, DeepSeek V4 Pro). Each dot is one case's shift in mean culpability rank from the safe to the bad ending, on an axis from −1 to +3 steps. Most dots sit at 0 (28 cases for Claude, 31 for GPT, 28 for DeepSeek); most of the rest lie above 0 and a few below. A red square and bar mark each model's mean and 95% interval: Claude +0.35 [+0.19, +0.54], GPT +0.18 [+0.04, +0.34], DeepSeek +0.25 [+0.09, +0.44].
     - *Figure 2:* Stacked bar chart for each model, safe ending above bad ending, showing the share of 480 replies reaching each verdict on Reason's tree. Blameless error falls from 81 to 69% (Claude), 65 to 59% (GPT) and 86 to 80% (DeepSeek). Possible negligent error rises from 14 to 26%, 25 to 29% and 6 to 8%, and DeepSeek's possible reckless violation from 6 to 10%. System-induced error and violation are small segments.
5. Declarations in the form:
   - **Competing interests:** "The author is the founder of CitadelAero, which develops AI tools for aviation safety and compliance teams; no company product was tested."
   - **Funding:** none.
   - **Data:** OSF (osf.io/dhf38).
6. **Suggested reviewers,** if asked. These are candidates in the field; check their current affiliations and e-mail addresses:
   - Andrew Gilbey (outcome bias among pilots);
   - Markus Kneer (outcome effects in LLMs);
   - an author of Oğuz et al. (2026), for example Óscar Oviedo-Trespalacios.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex` | The manuscript, in the journal's class (named; single column). Build the PDF with `latexmk -pdf paper.tex`; the PDF is not kept in the public repository, because it carries the journal's name and the Society's line and could be taken for a published article |
| `aer.cls` | The journal's LaTeX class, from its template files |
| `fig1-case-shifts.pdf`, `fig2-outcomes.pdf` | The figures |
| `cover_letter.txt` | Cover letter |
| `SUBMISSION.md` | This file |

## Log

| Date | Event |
|---|---|
| 4 Nov 2026 | Package prepared |
| 4 Nov 2026 | James overrides CitadelAero's no-submission rule for this paper; he is reading the manuscript before submission |
| 11 Nov 2026 | Style revision: lists turned into prose, bold labels and signposting cut, "we" removed; checked independently against the previous text (no change of meaning; every number kept). Abstract now pairs each mean shift with its model, which it had listed in a different order |
| 4 Nov 2026 | Journal-styled PDF taken out of the public repository (kept locally and sent to James) |
| 4 Nov 2026 | Set in the journal's template (`aer.cls`) and checked against Cambridge's "Preparing your materials" page; submission system is Editorial Manager |
