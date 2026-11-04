# Paper 02: journal submission to TMLR

**Target:** *Transactions on Machine Learning Research* (TMLR), submitted through OpenReview.
**Status (4 November 2026):** fallback. James chose JAIR first for this paper (`../jair/`); use this package if JAIR declines. Not submitted.

## Why TMLR

TMLR rules checked on its own pages on 4 November 2026 ([author guide](https://jmlr.org/tmlr/author-guide.html), [editorial policies](https://jmlr.org/tmlr/editorial-policies.html), [acceptance criteria](https://jmlr.org/tmlr/acceptance-criteria.html)):

- **It judges evidence, not novelty.** Papers are accepted if the claims are "supported by accurate and convincing evidence" and the findings "should be of interest to some individuals in TMLR's audience". The terms "significant", "impactful" and "novel" are explicitly avoided. That suits a pre-registered result that came out the opposite way to the prediction.
- **No fees**, rolling submission, open access under CC BY 4.0 (authors keep copyright).
- **AI assistance is allowed, with a caveat.** "LLMs may be used as general-purpose assistive tools", and authors are "fully responsible" for the content. But "Low-quality contributions (be they submissions or reviews) that appear to be largely LLM-generated will be closely examined for evidence of the issues mentioned previously, such as scientific misconduct", and the acceptance criteria add: "If a paper fully is AI generated with little or no human involvement, then at least with current AI systems, it is unlikely to meet this criterion." This paper's drafting, code and analysis were done with AI help under James's direction, and it says so. So James's own read and edit before submitting (step 2 below) matters: the paper must be his.
- **Preprints are allowed.** The editorial policy names "preprint servers such as arXiv and bioRxiv"; a GitHub or Zenodo preprint should count the same way. Don't link it from the submission.
- **Submission quota.** TMLR limits submissions per author per year by a "Generalized Harmonic Quota Rule, with parameters N_1 = 2", which means two single-author submissions a year, and "Budget is spent for all submissions by an author, including those which are desk rejected". Papers 02 and 06 would use the whole budget. Check the year boundary with TMLR's quota tool before submitting; if it is the calendar year, submit paper 02 in 2026 and AFACS in 2027.
- **Double-blind review:** the submission must be anonymous.
- **No page limit,** but length must be justified and long papers take longer to review.

## What changed from the preprint (`../../paper.pdf`)

| | Preprint v1.0 | Journal version (`paper.pdf` here) |
|---|---|---|
| Format | House style, IEEE numeric citations | TMLR style file, author-year citations (`tmlr.bst`) |
| Length | 23 pages, about 7,650 words of prose | 18 pages; main text 10 pages (about 5,300 words), then appendices |
| Author | Named, CitadelAero, credentials | Anonymous |
| Repository | Linked; commit identifiers given | No link; commit identifiers withheld; materials in an anonymised supplement |
| Background | Three sections (human screening; AI control; LLM judges) | One section with four short subsections |
| Detail moved to appendices | | Pre-registration timing record; harness context; full table of registered SDT measures; H2 numerical check; four of the preprint's five figures (in three floats) |
| Added | | Appendix A, an example item pair (MBPP problem 3); Appendix B, the monitor prompt; a broader impact statement; a data and code availability statement |
| Removed | | "Implications for aviation AI developers" (outside TMLR's audience); "What the human analogy did and did not predict" (its points are kept in the discussion of mechanisms); the fifth contribution bullet (the account for aviation readers); the vigilance and alarm-reliability background; secondary citations (Kale et al., Liu et al., Remedios et al., Ye et al., and others in the cut background) |
| Clarified | "the research engineer" | "the AI coding agent that implemented the pipeline under the investigator's direction". A single-author paper that mentions a "research engineer" would puzzle reviewers, and the AI assistance statement already says the code was written with AI help |

No result or number changed; every number was carried over from the preprint, which takes them from `../../results/`.

**Independent check of this version (4 November 2026).** A separate AI auditor compared this version with the preprint. It confirmed every number, table row, quotation, citation key and appendix, and the PDF's anonymity. It found places where cutting had changed a claim or lost a hedge, and all of them have been put right:
- the second contribution had become "not a criterion shift"; it is again "not a *conservative* criterion shift", the wording the preprint's audit required (Sonnet's criterion became more liberal);
- restored hedges: the P50 intervals "may be too narrow"; most deployed monitors judge one transcript per call; the in-call schema corrections were not anticipated by the registered retry rule; "the code implementing *several* of them"; P2.5 batches were not significantly more inclusive than single-item review; lower hit rates in the first eight positions of P10 batches; the timing of the edit-size threshold rests on the implementing agent's record, with the history of its code comment; the audit-requested post hoc checks;
- "mainly" added where the effect is traced to scores rather than the flag threshold (the 40–59 band's flag rate also rose);
- smaller fixes: the log-linear correction applies to every cell; the Kapetanovic et al. wording; the harness block "cannot explain" differences between conditions (rather than "did not affect" them); citations attached to section locators; the broader impact statement acknowledges that the item pairs are released for reuse; the AI statement says what the audits covered and restores the note that several sources are Anthropic's.

The supplement builder was also fixed. It now removes the working title and "paper 02", ships the figure palette so the figure script runs, explains who "the research engineer" is (the AI coding agent), and adds `version_history.txt`: the times and files of every commit that touched the materials during the study, without identifiers. That lets reviewers check the pre-registration timing.

## The AAAI-27 workshop version

Another session prepared an anonymised 8-page version of this paper for the AAAI-27 Trustworthy Evolution of AI Agents workshop (`../aaai27-trust4rsi-workshop/`; deadline 20 November 2026). The workshop is non-archival, and TMLR's editorial policy accepts overlap with work shared at venues "publicly declared, in writing, to be non-archival, such as workshops". So both can be used. If both are submitted, mention the workshop submission on the TMLR form. James has said he couldn't present at AAAI; check with the organisers whether presentation in person is required.

## Remaining weaknesses a reviewer may raise

These don't block submission, but they are the likeliest requests:

1. **Only Claude models, run through Claude Code.** Both monitors and the generator are from one model family, and calls went through Claude Code rather than the API. A reviewer may ask for a monitor from another family (for example GPT or an open-weights model) called directly through an API. That means a new paid run (the whole original study, two monitors plus item generation, cost USD 41.70 at list prices), and it needs James's go-ahead. It could be offered during the rebuttal rather than done now.
2. **The P50 cell has 8 batches per monitor.** Already stated as a limitation.
3. **Pop-out against crowding.** The paper says the design cannot tell them apart. A reviewer may ask for the follow-up design (batch size and number of backdoors varied separately). It is listed as future work.
4. **Pre-registration timing.** Nine clarifications were committed minutes after the run began. This is disclosed (Section 3.6, Appendix C), and `version_history.txt` in the supplement lets reviewers check the times. It is honest, and should stay.
5. **Claims beyond two models.** The conclusion now says "the monitors" (these two), not "LLM monitors"; a reviewer may still want more models (item 1).
6. **H2 rests on a post hoc refit and an exact test,** because the registered model is numerically unreliable for Sonnet. The table points to the text that explains this.

## What James needs to do

1. **Create an OpenReview profile now.** TMLR requires every author to have "complete and active OpenReview profiles". Profiles without an institutional email address go through moderation that [can take up to two weeks](https://docs.openreview.net/getting-started/frequently-asked-questions/why-does-it-take-two-weeks-to-moderate-my-profile). To speed it up, use `james@citadelaero.com`, and add a homepage that shows your name and email (citadelaero.com or lecuirot.je), your ORCID (0009-0009-6014-1298) and your career history ([OpenReview: expediting activation](https://docs.openreview.net/getting-started/creating-an-openreview-profile/expediting-profile-activation)).
2. **Read the journal version** (`paper.pdf` in this folder) and decide whether to add a non-Claude monitor before submitting (weakness 1 above) or to offer it in the rebuttal.
3. **Build the supplement:** `python3 papers/02-do-llm-monitors-miss-rare-threats/submissions/tmlr/make_supplement.py` writes `submissions/tmlr/build/supplement.zip` (about 3 MB; TMLR allows up to 100 MB). The script checks for a list of identifying patterns. That list can't catch everything, so look through `submissions/tmlr/build/supplement/` before uploading.
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
- **Competing interests:** "The author is the founder of CitadelAero, which builds AI tools for aviation. The study's model calls ran under the author's paid Claude subscription (Anthropic), and Claude assisted with drafting and analysis; the author has no other relationship with Anthropic, whose models are tested."
- **Funding:** none. Model costs (about USD 42 at list prices) were met under the author's Claude Code subscription.
- **Human subjects / IRB:** not applicable; no human participants.
- **Previous submission / non-archival venues:** none. The paper was posted as a preprint (allowed; not linked).
- **Code:** in the supplementary material.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The anonymised TMLR submission. Build with `latexmk -pdf paper.tex` from this folder (figures are read from `../../figures/report/`) |
| `references.bib` | The preprint's references, with "n.d." added as the year of the two undated web pages, which author-year citations need |
| `tmlr.sty`, `tmlr.bst`, `fancyhdr.sty` | The official TMLR style files (github.com/JmlrOrg/tmlr-style-file, Apache 2.0; licence in `TMLR-STYLE-LICENSE`) |
| `make_supplement.py` | Builds the anonymised supplementary ZIP into `build/` (git-ignored) |
| `SUBMISSION.md` | This file |

## For the camera-ready version, if accepted

Switch to `\usepackage[accepted]{tmlr}`, fill in `\month`, `\year` and `\openreview`, add the author block (James Le Cuirot, CitadelAero), give the commit identifiers in Appendix C, replace the data-availability sentence with the repository link, change "the authors" back to "the author", and move the AI-assistance statement into the acknowledgements.

## Note on this file

This file is in the public repository, next to the anonymised paper, and names the author. TMLR allows public preprints, so this breaks no rule, but anyone who looks can connect the two. If you'd rather keep the submission package private, move the `submissions/` folders out of the public repository before submitting.
