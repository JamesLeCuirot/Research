# Paper 02: journal submission to TMLR

**Target:** *Transactions on Machine Learning Research* (TMLR), submitted through OpenReview.
**Status (4 November 2026):** submission version drafted and anonymised; waiting for James's read and his OpenReview account. Not yet submitted.

## Why TMLR

TMLR rules checked on its own pages on 4 November 2026 ([author guide](https://jmlr.org/tmlr/author-guide.html), [editorial policies](https://jmlr.org/tmlr/editorial-policies.html), [acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html)):

- **It judges evidence, not novelty.** Papers are accepted if the claims are "supported by accurate and convincing evidence" and the findings "should be of interest to some individuals in TMLR's audience". The terms "significant", "impactful" and "novel" are explicitly avoided. That suits a pre-registered result that came out the opposite way to the prediction.
- **No fees**, rolling submission, open access under CC BY 4.0 (authors keep copyright).
- **AI assistance is allowed:** "LLMs may be used as general-purpose assistive tools", with the authors fully responsible.
- **Preprints are allowed**, including the GitHub preprint, as long as the submission does not link to it.
- **Double-blind review:** the submission must be anonymous.
- **No page limit,** but length must be justified and long papers take longer to review.

## What changed from the preprint (`../paper.pdf`)

| | Preprint v1.0 | Journal version (`paper.pdf` here) |
|---|---|---|
| Format | House style, IEEE numeric citations | TMLR style file, author-year citations (`tmlr.bst`) |
| Length | 23 pages, about 7,650 words of prose | 18 pages; main text about 10.5 pages (about 5,300 words), then appendices |
| Author | Named, CitadelAero, credentials | Anonymous |
| Repository | Linked; commit identifiers given | No link; commit identifiers withheld; materials in an anonymised supplement |
| Background | Three sections (human screening; AI control; LLM judges) | One section with four short subsections |
| Detail moved to appendices | | Pre-registration timing record; harness context; full table of registered SDT measures; H2 numerical check; four figures |
| Added | | Appendix A, an example item pair (MBPP problem 3); Appendix B, the monitor prompt; a broader impact statement; a data and code availability statement |
| Removed | | "Implications for aviation AI developers" (outside TMLR's audience); the vigilance and alarm-reliability background; some secondary citations |
| Clarified | "the research engineer" | "the AI coding agent that implemented the pipeline under the investigator's direction". A single-author paper that mentions a "research engineer" would puzzle reviewers, and the AI assistance statement already says the code was written with AI help |

No result, number or claim changed. Every number was carried over from the preprint, which takes them from `../results/`.

## Remaining weaknesses a reviewer may raise

These don't block submission, but they are the likeliest requests:

1. **Only Claude models, run through Claude Code.** Both monitors and the generator are from one model family, and calls went through Claude Code rather than the API. A reviewer may ask for a monitor from another family (for example GPT or an open-weights model) called directly through an API. That means a new paid run (the whole original study, two monitors plus item generation, cost USD 41.70 at list prices), and it needs James's go-ahead. It could be offered during the rebuttal rather than done now.
2. **The P50 cell has 8 batches per monitor.** Already stated as a limitation.
3. **Pop-out against crowding.** The paper says the design cannot tell them apart. A reviewer may ask for the follow-up design (batch size and number of backdoors varied separately). It is listed as future work.
4. **Pre-registration timing.** Nine clarifications were committed minutes after the run began. This is disclosed in full (Section 3.6, Appendix C). It is honest, and should stay.

## What James needs to do

1. **Create an OpenReview profile now.** TMLR requires every author to have "complete and active OpenReview profiles". Profiles without an institutional email address go through moderation that [can take up to two weeks](https://docs.openreview.net/getting-started/frequently-asked-questions/why-does-it-take-two-weeks-to-moderate-my-profile). To speed it up, use `james@citadelaero.com`, and add a homepage that shows your name and email (citadelaero.com or lecuirot.je), your ORCID (0009-0009-6014-1298) and your career history ([OpenReview: expediting activation](https://docs.openreview.net/getting-started/creating-an-openreview-profile/expediting-profile-activation)).
2. **Read the journal version** (`paper.pdf` in this folder) and decide whether to add a non-Claude monitor before submitting (weakness 1 above) or to offer it in the rebuttal.
3. **Build the supplement:** `python3 papers/02-do-llm-monitors-miss-rare-threats/journal/make_supplement.py` writes `journal/build/supplement.zip` (about 3 MB; TMLR allows up to 100 MB). The script checks that no identifying string is left.
4. **Submit on OpenReview** (TMLR venue: https://openreview.net/group?id=TMLR). Upload `paper.pdf` and `supplement.zip`, and fill in the form from the answers below.

## Answers for the OpenReview form

Check the field names against the live form; these were prepared from TMLR's author guide.

- **Title:** Do LLM Monitors Miss Rare Threats? A Pre-registered Test of the Low-Prevalence Effect
- **Abstract:** copy from `paper.tex` (between `\begin{abstract}` and `\end{abstract}`), replacing `\num{30880}` with 30,880, `\SI{2.5}{\percent}` with 2.5% (and so on), and `$p = .0015$` with p = .0015.
- **Submission length:** regular submission (main text about 10.5 pages, which is 12 pages or fewer), if the form asks.
- **Suggested action editors** (expertise as listed on TMLR's [editorial board page](https://jmlr.org/tmlr/editorial-board.html) on 4 November 2026; confirm that they are still listed):
  - Tim G. J. Rudner (University of Toronto): AI safety, AI alignment
  - A. Feder Cooper (Yale University): ML security, red teaming, evaluations
  - Chinmay Hegde (New York University): LLM benchmarking, AI safety, robustness
  - Erin Grant (University of Alberta): cognitive science, psychology
  - Tianmin Shu (Johns Hopkins University): computational cognitive science, human-AI collaboration

  The list leaves out action editors who work at Anthropic, because the paper tests Anthropic's models.
- **Competing interests:** "The author is the founder of CitadelAero, which builds AI tools for aviation. The author has no financial relationship with Anthropic, whose models are tested."
- **Funding:** none. Model costs (about USD 42 at list prices) were met under the author's Claude Code subscription.
- **Human subjects / IRB:** not applicable; no human participants.
- **Previous submission / non-archival venues:** none. The paper was posted as a preprint (allowed; not linked).
- **Code:** in the supplementary material.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The anonymised TMLR submission. Build with `latexmk -pdf paper.tex` from this folder (figures are read from `../figures/report/`) |
| `references.bib` | The preprint's references, with "n.d." added as the year of the two undated web pages, which author-year citations need |
| `tmlr.sty`, `tmlr.bst`, `fancyhdr.sty` | The official TMLR style files (github.com/JmlrOrg/tmlr-style-file, Apache 2.0; licence in `TMLR-STYLE-LICENSE`) |
| `make_supplement.py` | Builds the anonymised supplementary ZIP into `build/` (git-ignored) |
| `SUBMISSION.md` | This file |

## For the camera-ready version, if accepted

Switch to `\usepackage[accepted]{tmlr}`, add the author block (James Le Cuirot, CitadelAero), restore the commit identifiers in Section 3.6 and Appendix C, replace the data-availability sentence with the repository link, and move the AI-assistance statement into the acknowledgements.
