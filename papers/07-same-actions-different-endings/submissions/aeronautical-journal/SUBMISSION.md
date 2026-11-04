# Paper 07: submission to The Aeronautical Journal

**Journal:** *The Aeronautical Journal* (Royal Aeronautical Society; published by Cambridge University Press), research article.
**Status (4 November 2026):** package ready for James's read and edit. **First choice for this paper**; the *Safety Science* package (`../safety-science/`) is the fallback if this journal declines. Not yet submitted.

## Why this journal

- **Readers:** operators, investigators, safety managers and regulators, and it is your own society's journal.
- **Single-anonymised review** ("a single-anonymized model of peer review"): reviewers see your name. This removes the anonymity problem the *Safety Science* route had, because the OSF preprint is public.
- **Preprints are fine:** "deposition of a preprint on the author's personal website, in an institutional repository, or in a preprint archive" is not prior publication.
- **AI use is allowed if declared.** Cambridge does not accept AI as an author, and asks you to declare AI use that generates text or analyses data. The manuscript has a declaration section.
- **Length and format:** "Papers should preferably not exceed 10,000 words" (this one has about 5,900 words of main text); single column; abstract up to 250 words (242); APA references; a nomenclature section is required (included). Journal-style formatting is only required at acceptance.
- **Process:** at least two referees; "typically lasts 3-6 months".
- **Fees:** none on the standard route; open access is optional (£2,610).

Checked on Cambridge's pages on 4 November 2026: [preparing your materials](https://www.cambridge.org/core/journals/aeronautical-journal/information/author-instructions/preparing-your-materials), [review process](https://www.cambridge.org/core/journals/aeronautical-journal/information/peer-review-information/review-process), [fees](https://www.cambridge.org/core/journals/aeronautical-journal/information/author-instructions/fees-and-pricing). The wider list of journals is in `papers/JOURNAL_OPTIONS.md`.

## What this version is

The same text as the *Safety Science* version, which an independent check compared with the preprint token by token, with these changes for this journal:
- your name, affiliation, ORCID and correspondence address on the paper;
- a nomenclature section;
- the OSF links restored, and the freeze commit identifier restored;
- the author description in Methods: "a commercial pilot and flight safety officer";
- a line under the abstract naming the earlier preprint;
- competing interests, funding, acknowledgements and a declaration of AI use at the end;
- single column, 1.5 spacing, line numbers.

No number or finding changed.

## Before you submit

1. ~~Decide CitadelAero's rule.~~ **Decided 4 November 2026:** James, as founder, overrides the company research plan's "No preprint or journal submissions" rule for this paper. Note it in CitadelAero's own records too.
2. **Read and edit the manuscript in your own words.** Then replace the placeholder `[AUTHOR TO DESCRIBE HIS OWN REVISION OF THE MANUSCRIPT]` in the "Declaration of the use of AI" section of `paper.tex` with what you did, and rebuild (`latexmk -pdf paper.tex` in this folder).
3. **Read `cover_letter.txt`** and adjust it to your voice.

## How to submit

1. Go to the journal's submission system, **Editorial Manager**: https://www.editorialmanager.com/aeroj/ (checked 4 November 2026 on Cambridge's "submitting your materials" page). It needs its own account, separate from Cambridge Core. Link your ORCID (0009-0009-6014-1298), which the journal requires for the corresponding author. Queries go to aerojournal@aerosociety.com.
2. **Keywords go in the online form, not the manuscript** (the journal's rule; the manuscript's keywords line was removed on 4 November 2026). Use: just culture; outcome bias; hindsight bias; large language models; culpability; aviation safety reporting.
3. Choose the article type **Research Article**, and a main and a secondary subject classification that fit (likely human factors, safety, or air transport operations, from the journal's list; the guidance warns that a wrong classification can lead to an out-of-scope rejection).
4. Upload `paper.pdf`, or `paper.tex` with `fig1-case-shifts.pdf` and `fig2-outcomes.pdf`, and paste in the cover letter.
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
| `paper.tex`, `paper.pdf` | The manuscript (named; single column) |
| `fig1-case-shifts.pdf`, `fig2-outcomes.pdf` | The figures |
| `cover_letter.txt` | Cover letter |
| `SUBMISSION.md` | This file |

## Log

| Date | Event |
|---|---|
| 4 Nov 2026 | Package prepared |
| 4 Nov 2026 | James overrides CitadelAero's no-submission rule for this paper; he is reading the manuscript before submission |
