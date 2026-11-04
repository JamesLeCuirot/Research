# Paper 07: journal submission to Safety Science

**Target:** *Safety Science* (Elsevier), research paper, through Elsevier's Editorial Manager.
**Status (4 November 2026):** submission package drafted. Waiting for James's decisions below, his read and edit, and the two OSF view-only links. Not yet submitted.

## Why Safety Science

- **Direct precedent.** *Safety Science* published Oğuz et al. (2026), "Responsibility attribution by large language models (LLMs) in road safety analysis", which this paper cites and builds on. Its readers know just culture, hindsight bias and occurrence reporting.
- **An empirical, pre-registered study** with open materials suits a safety-science journal better than paper 01 does.
- **Elsevier's AI policy** allows disclosed AI support, with conditions (see decision 1).
- **No fee on the standard route** (hybrid journal, as described by third-party sources).

Unverified points on the journal's guide (its page blocks automated access) are the same as for paper 01: see `papers/01-just-culture-for-machines/journal/SUBMISSION.md`. Here the abstract is 242 words, there are 5 highlights of 72–80 characters, and the references are in APA author-date style, which matches the journal's published author-date style.

## Decisions for James

1. **Elsevier's AI policy.** As for paper 01. Elsevier forbids "Generating sections of a manuscript without genuine intellectual contribution from the author", and the declaration must state "the extent of [your] oversight" ([policy, updated June 2026](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals)).
   - This paper is on stronger ground than paper 01. You designed the study, made every design decision, approved the cases, endings and controls, and checked every case against its source.
   - But the manuscript was drafted by Claude. Read and edit it in your own words before submitting, and adjust the declaration to say what you did.
   - The use of Claude in the *research* itself (screening and condensing the reports) is now also stated in the Methods (Section 2.3, "Who prepared the cases"), as Elsevier asks for AI used in research methods.
2. **CitadelAero's own rule.** The company research plan adopted on 7 October 2026 says, of company studies: "No preprint or journal submissions" (ruling of 2 October, in `2026-10-05-research-plan.md` in CitadelAero's study repository). This study was published as an OSF preprint anyway, and you have now asked for it to go to a journal, so I've treated your request as overriding the rule for this paper. You may want to record that decision in the company's shared repository.
3. **Two papers to one journal.** Paper 01 is also prepared for *Safety Science*. This one is the stronger fit. If you'd rather not have two concurrent submissions there, send this one first.

## What James needs to do

1. **Create two anonymised OSF view-only links** (on each OSF project: Settings → View-only links → Create, tick "Anonymize"). One is for the registration (osf.io/s8q24), one for the project (osf.io/dhf38). Paste them into the manuscript's Data availability section, which has the placeholders `[OSF VIEW-ONLY LINK 1]` and `[OSF VIEW-ONLY LINK 2]`, then rebuild with `latexmk -pdf paper.tex`.
2. **Read and edit the manuscript** (decision 1).
3. **Check the journal's guide** for the unverified points.
4. **Upload to Editorial Manager:**
   - the manuscript (`paper.pdf`, or `paper.tex` with `fig1-case-shifts.pdf` and `fig2-outcomes.pdf`);
   - `title_page.pdf`;
   - `highlights.txt`;
   - the text of `cover_letter.txt`.
5. **Enter in the system:** competing interest ("The author's company, CitadelAero, develops AI tools for aviation safety and compliance teams. No CitadelAero product was tested."), funding (none), and keywords.
6. **Suggested reviewers,** if asked. Candidates in the field; check current affiliations and e-mail addresses:
   - an author of Oğuz et al. (2026), for example Óscar Oviedo-Trespalacios;
   - Markus Kneer (outcome effects in LLMs);
   - Andrew Gilbey (outcome bias among pilots).

## What changed from the preprint (`../paper/same-actions-different-endings-preprint-v1.pdf`)

| | Preprint v1 | Journal version |
|---|---|---|
| Format | Markdown and PDF | Elsevier `elsarticle` review layout (double-spaced, line numbers); converted with pandoc and edited by hand |
| Abstract | Structured, about 400 words with bullet lists | One paragraph, 242 words, the same findings |
| Author block, ORCID, correspondence, OSF links in the header | On the paper | On the separate title page; manuscript anonymised |
| Commit identifier of the freeze tag | Given | Withheld (the tag name is kept) |
| "The author, a commercial pilot, flight safety officer, and safety and compliance consultant specialising in human factors" | | "The author, a commercial pilot and flight safety officer" (less identifying) |
| Use of Claude to screen and condense the reports | Only in the Limitations and the AI statement | Also stated in the Methods (Section 2.3) |
| Declarations (about the author, conflict of interest, funding, acknowledgements) | In the paper | On the title page |
| Use of AI | Bullet list in Declarations | Elsevier's declaration, immediately before the references, stating purpose and oversight |
| Data availability | OSF URLs | Placeholders for anonymised view-only links |
| Figures | With titles drawn inside the image | Titles removed from the images and given as LaTeX captions |
| DOIs in references | Plain text | Line-breakable links |

The main text (about 5,900 words) was not cut: it is already a normal length for the journal. No result, number or claim changed.

## Likely reviewer questions

All are stated in the paper's limitations; reviewers may still press on them:

1. **Claude prepared the cases, and one model tested is Claude.** The within-case design limits what this can do, but it cannot rule out an effect on baseline levels.
2. **No human baseline.** Listed as future work; it is the natural follow-up.
3. **The planned blind re-screen was not done** (D11).
4. **Fixed bad endings,** with category confounded with ending.
5. **Averaging ordinal ranks;** the verdict shares in Figure 2 avoid that assumption.
6. **The fourth registered model was dropped for cost** (D9), before any main-study call.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The anonymised manuscript (review layout) |
| `fig1-case-shifts.pdf`, `fig2-outcomes.pdf` | The figures, made from `../results/analysis/*.svg` without their drawn titles |
| `title_page.tex`, `title_page.pdf` | Title page with author details and declarations |
| `highlights.txt` | The highlights |
| `cover_letter.txt` | Cover letter (plain text) |
| `SUBMISSION.md` | This file |
