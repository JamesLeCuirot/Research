# Paper 07: journal submission to Safety Science

**Target:** *Safety Science* (Elsevier), research paper, through Elsevier's Editorial Manager.
**Status (4 November 2026):** package drafted and independently checked. **Not ready to submit** until James makes the decisions below, revises the text himself and completes the AI declaration. Not yet submitted.

## Why Safety Science

- **The nearest published work is there.** *Safety Science* published Oğuz et al. (2026) on responsibility attribution by LLMs in road safety; the paper cites it. Its readers know just culture, hindsight and outcome bias, and occurrence reporting.
- **It suits an empirical, pre-registered study** with open materials better than paper 01's theory.
- **Elsevier's AI policy** allows disclosed AI support, with conditions (decision 1).
- **No fee on the standard route** (hybrid journal, as described by third-party sources).

The journal's guide page blocks automated access, so its exact limits are unverified (see paper 01's `SUBMISSION.md`). Here the abstract is 242 words, there are 5 highlights of 72–85 characters, and the references are APA author-date, which matches the journal's published style.

## Decisions for James

1. **Elsevier's AI policy and the declaration.** Elsevier forbids "Generating sections of a manuscript without genuine intellectual contribution from the author", and the declaration must state "the extent of [your] oversight" ([policy, updated June 2026](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals)).
   - You designed the study, made every design decision, approved the materials and checked every case, which is real intellectual contribution.
   - But the manuscript was drafted by Claude. Revise it in your own words, then replace the placeholder `[AUTHOR TO DESCRIBE HIS OWN REVISION OF THE MANUSCRIPT]` in the declaration (near the end of `paper.tex`) with what you actually did, and rebuild.
   - The Methods (Section 2.3) now describe every way Claude was used in the research: protocol drafts, screening, condensing, the control cases, the exclusion checks, the scripts and the analysis. They also say the model versions used for those steps were not recorded.
2. **CitadelAero's rule against journal submissions.** The company research plan, adopted 7 October 2026, says of company studies: "No preprint or journal submissions" (ruling of 2 October; `2026-10-05-research-plan.md`, CitadelAero's study repository). Its later lines also say no journal papers "on purpose". You asked for this paper to go to a journal. Whether that overrides the company rule is your decision as founder, not mine. Please make it explicitly and record it in the company's shared repository before submitting, especially as the affiliation is CitadelAero.
3. **Anonymity can only be partial — decided: new title.** *Safety Science* appears to use double-anonymised review, but your OSF records are public, name you and carry the preprint's title, and the results are on the CitadelAero website. OSF's "Anonymize" option for view-only links hides contributor names but not what the files say, so the package uses an anonymised supplementary ZIP instead of OSF links (`make_supplement.py`). On 4 November you agreed to a different title for the journal version: **"Outcome Bias in AI Models Applying a Culpability Decision Tree to Airline Occurrence Reports: A Pre-registered Within-Case Experiment"**. The manuscript, title page, cover letter and supplement use it; the title page and cover letter (seen by the editor, not reviewers) give the preprint's title as prior dissemination. A reviewer who searches the abstract could still find the preprint; that is allowed.
4. **Two papers to one journal.** Paper 01 is also prepared for *Safety Science*. This one is the stronger fit; if you'd rather not have two concurrent submissions there, send this one first.

## What James needs to do

1. Decide points 1, 2 and 4 (3 is decided); revise the manuscript; complete the declaration; rebuild with `latexmk -pdf paper.tex`.
2. Build the supplement: `python3 papers/07-same-actions-different-endings/journal/make_supplement.py` writes `journal/build/supplement.zip` (about 2.5 MB). It replaces your name and company, removes contact details, registry links and the freeze commit, leaves out the preprint, and checks for a list of identifying patterns. The analysis reproduces from the supplement. The list can't catch everything, so look through `journal/build/supplement/` before uploading.
3. Check the journal's guide for the unverified points.
4. Upload to Editorial Manager:
   - the manuscript (`paper.pdf`, or `paper.tex` with the two figure PDFs);
   - `title_page.pdf`;
   - `highlights.txt`;
   - `supplement.zip` as supplementary material;
   - the text of `cover_letter.txt`.
5. Enter the competing interest (as on the title page), funding (none) and keywords in the system.
6. **Suggested reviewers,** if asked. Candidates in the field; check current affiliations and e-mail addresses:
   - an author of Oğuz et al. (2026), for example Óscar Oviedo-Trespalacios;
   - Markus Kneer (outcome effects in LLMs);
   - Andrew Gilbey (outcome bias among pilots).

## What changed from the preprint (`../paper/same-actions-different-endings-preprint-v1.pdf`)

| | Preprint v1 | Journal version |
|---|---|---|
| Format | Markdown and PDF | Elsevier `elsarticle` review layout; converted with pandoc and edited by hand. Table captions above the tables; Appendix A shows the tree and instructions line by line, as in `prompts/` |
| Abstract | Structured, about 400 words | One paragraph, 242 words. It keeps the findings, including H2 not being supported for GPT and DeepSeek's route through "knowingly violating". "Did not protect against hindsight" became "did not prevent outcome bias", because the study has no unstructured condition |
| Highlights | | New; the mechanism highlight says DeepSeek also shifted at "knowingly violating" |
| Author block, ORCID, correspondence, OSF links | In the header | On the title page; the manuscript is anonymised and the materials are in an anonymised supplement |
| Freeze commit | Given | Withheld (the tag name is kept) |
| Author description | "a commercial pilot, flight safety officer, and safety and compliance consultant specialising in human factors" | "who has operational flight-safety experience" (less identifying) |
| AI in the research | Limitations and declarations only | Full description in the Methods (Section 2.3) |
| "one of the most widely used tools" | No citation | "a well-known tool" |
| "attributable to the outcome alone" | | "follows from the outcome alone", with a pointer to a new limitation |
| **New limitation** | | "The ending may be read as evidence": a bad ending may imply unstated facts, so part of the shift could be inference rather than bias. Raised by the independent check; consistent with the larger shifts in excursion cases and Claude's rise in "insufficient information" flags |
| Implications 1 and 5 | "A structured prompt does not protect against hindsight"; "Reviewers share the same bias" | "did not prevent the bias", noting there was no unstructured condition; and the human claim is now marked as resting on the cited literature, not tested here |
| Data availability | OSF, CC BY 4.0 | Supplement for review, with OSF links on acceptance; CC BY covers the study's own materials, and the ASRS reports are NASA public records |
| Declarations | In the paper | On the title page (fuller competing interests, accurate CRediT, prior dissemination) and Elsevier's AI declaration |
| Figures | Titles drawn inside the images | Titles removed; captions in LaTeX |

The main text was not cut: at about 5,900 words it is a normal length. No number changed. The claims changed only as listed above, by being qualified.

## Independent check (4 November 2026)

A separate AI auditor compared the manuscript with the preprint token by token and found no changed number, table cell, quotation, list item or reference, and every cross-reference correct. Its other findings were all addressed, except those that are decisions for James (2 and 3 above):
- the overgeneralised mechanism and the missing H2 result in the abstract;
- "did not protect";
- Appendix A's layout;
- table captions placed below the tables;
- a duplicate label;
- the widened licence claim;
- incomplete AI disclosure in the Methods;
- an AI declaration that asserted revision not yet done (now a placeholder for James);
- the unpublicised website write-up and company article (now disclosed);
- the incomplete competing-interest statement;
- the CRediT errors;
- OSF view-only links that would not anonymise (replaced by the supplement).

## Likely reviewer questions

1. **Is the bad ending evidence?** Now a stated limitation; the planned mitigation experiment addresses it.
2. **Claude prepared the cases, and one model tested is Claude;** no independent re-screen (D11).
3. **No unstructured condition and no human baseline.** Implications are now worded to match.
4. **Measurement.**
   - Averaging ordinal ranks; the verdict shares in Figure 2 avoid that.
   - Harsher and lenient counts include run-to-run noise.
   - Failing the substitution test leads almost automatically to "possible negligent error", because the cases carry no training information.
   - A reviewer may ask for a mixed-effects ordinal model as a sensitivity analysis. That would be a new (cheap, no model calls) post hoc analysis, if wanted.
5. **Scope:** three models over two days, fixed mild endings confounded with category, US ASRS reports only.
6. **Grounding in safety science:**
   - critiques of Reason's tree and the substitution test (for example Dekker);
   - hindsight in accident investigation;
   - prior NLP work on occurrence reports.

   Worth adding if you revise the introduction.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The anonymised manuscript (review layout) |
| `fig1-case-shifts.pdf`, `fig2-outcomes.pdf` | Figures from `../results/analysis/*.svg` without their drawn titles |
| `title_page.tex`, `title_page.pdf` | Title page with author details and declarations |
| `highlights.txt` | Highlights |
| `cover_letter.txt` | Cover letter (plain text) |
| `make_supplement.py` | Builds the anonymised supplementary ZIP into `build/` (git-ignored) |
| `SUBMISSION.md` | This file |
