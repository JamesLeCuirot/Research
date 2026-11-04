# Paper 02: submission to the Journal of Artificial Intelligence Research (JAIR)

**Journal:** *Journal of Artificial Intelligence Research*, full-length article.
**Status (4 November 2026):** package ready for James's read and two decisions (below). Chosen instead of TMLR on 4 November 2026; the TMLR package (`../tmlr/`) stays as a fallback, and leaves both TMLR submissions this year free for paper 06. Not yet submitted.

## Why JAIR

Checked on JAIR's own pages on 4 November 2026 ([submissions](https://www.jair.org/index.php/jair/about/submissions), [formatting](https://www.jair.org/index.php/jair/formatting)):

- **Free:** "There is no charge to submit a paper, nor are there any publication fees once an article is accepted." Open access under CC BY.
- **No length limit,** but "We strongly encourage authors to be concise." This version is 20 pages, of which about 10 are main text.
- **Decision in "approximately 8-12 weeks".** A paper "may be revised and resubmitted at most once".
- **Preprints are fine:** "Authors may submit their JAIR papers to arXiv and similar services."
- **Named review:** the template carries the authors' names, and the guidelines describe reviewer anonymity only, so the paper is not anonymised.
- **AI policy:** authors are fully responsible. AI may help with editing, ideas or data analysis, but "the core contributions of a paper must come from the authors", and AI cannot be an author or a cited source. See decision 2.

## What this version is

The text of the TMLR version, which an independent check compared with the preprint, adapted to JAIR's rules:
- **Template:** the official JAIR Author Kit (`jair.cls`, ACM-based, biblatex author-year), unchanged as JAIR requires. JAIR rejects other formats without review.
- **Named:** your name, ORCID and correspondence address; commit identifiers restored in Section 3.6 and Appendix C; the repository linked for data and code.
- **Details put back:** the Claude Code version, Python and statsmodels versions, and the bootstrap seed.
- **Closing sections:** acknowledgements, competing interests, and data and code availability.
- **The required JAIR reproducibility checklist,** filled in, as the final appendix. Papers without it are desk-rejected.

No number or finding changed.

## Two decisions before you submit

1. **The acknowledgements need your own words.** JAIR requires that "the core contributions of a paper must come from the authors". The acknowledgements now say the study was "conceived, designed, pre-registered and run under the author's direction" with AI assistance. Replace the placeholder `[AUTHOR TO STATE HIS OWN CONTRIBUTIONS…]` with what you contributed: for example the research question, the design decisions, your interpretation, and your revision of the text after reading it. If you are not comfortable that the core contributions are yours, TMLR's policy ("general-purpose assistive tools") is the better fit.
2. **Licence for the raw outputs.** The checklist asks whether the raw data has a licence that allows reuse. The code is MIT and the item pairs are CC BY 4.0, but the raw monitor outputs have no stated licence, so the checklist says "partially". To make it "yes", decide on CC BY 4.0 for the outputs. Then I'll add that to the repository and update the checklist.

## The three questions in the submission form

JAIR says submissions "for which these three questions are not clearly answered will not be considered". Each answer must be 150 words or fewer. Drafts:

**1. Why does this work matter to AI researchers?** (about 110 words)
> AI control protocols rely on language-model monitors to flag rare attacks by more capable models, and monitor evaluations usually assume that detection rates measured on balanced test sets carry over to deployment, where attacks are rare. Human screeners violate that assumption: they miss rare targets far more often. This pre-registered experiment is, as far as we found, the first to manipulate target prevalence within an LLM monitor's context while holding the item pool fixed. The human effect did not appear; instead, backdoors were missed more when several shared a batch. The results show that batch composition changes measured monitor performance, and they release 419 execution-verified clean/backdoored code pairs for further work.

**2. Which 1–3 JAIR papers are closest, and how does this work differ?** (about 90 words)
> The closest JAIR paper we found is Fraser, Dawkins and Kiritchenko (2025), "Detecting AI-Generated Text: Factors Influencing Detectability with Current Methods" (JAIR 82). It surveys what makes AI-generated text detectable under different scenarios. Our work differs in three ways: it tests LLMs as detectors of deliberately inserted code backdoors rather than detectors of AI text; it manipulates one factor, the prevalence of targets in the reviewer's context, experimentally and with a pre-registered design; and it analyses the result with signal detection theory. JAIR appears to have published little on AI-control monitoring itself.

**3. Has any part been published or is it under review elsewhere?**
> No part has been published in a journal or conference proceedings, and it is not under review elsewhere. A preprint (v1.0, 4 November 2026) is publicly available in the author's research repository.

If you also submit the 8-page version to the non-archival AAAI-27 workshop, add: "An 8-page version is under review at the non-archival AAAI-27 Workshop on Trustworthy Evolution of AI Agents."

## How to submit

1. Register at jair.org, then use "Make a Submission".
2. Enter the title, author and contact details, and the abstract: copy it from `paper.tex`, turning `\num{30880}` into 30,880, `\SI{2.5}{\percent}` into 2.5%, and `$p = .0015$` into p = .0015.
3. Confirm the declarations: original work, proofread, track, and the Open Access Publication Agreement.
4. Paste the three answers above into the comments section.
5. Upload `paper.pdf`. Build it with `latexmk -pdf paper.tex` in this folder; this needs `biber`.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The manuscript (named; JAIR template; checklist in the last appendix) |
| `references.bib` | The preprint's references (one date field adjusted for biblatex) |
| `jair.cls`, `acmart.cls`, `acmauthoryear.bbx`, `acmauthoryear.cbx`, `acmdatamodel.dbx` | The official JAIR Author Kit files, unchanged (downloaded 4 November 2026 from jair.org) |
| `SUBMISSION.md` | This file |

## Log

| Date | Event |
|---|---|
| 4 Nov 2026 | James chooses JAIR over TMLR; package prepared |
