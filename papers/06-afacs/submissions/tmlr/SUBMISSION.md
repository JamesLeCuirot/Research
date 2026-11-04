# AFACS (paper 06): journal submission to TMLR

**Target:** *Transactions on Machine Learning Research* (TMLR), through OpenReview.
**Status (4 November 2026):** submission version drafted and anonymised; waiting for James's read and his OpenReview account. Not yet submitted.

## Why TMLR, and the alternative

TMLR's rules are summarised in `papers/02-do-llm-monitors-miss-rare-threats/submissions/tmlr/SUBMISSION.md` (checked on TMLR's own pages on 4 November 2026). In short: no fees, open access, double-blind, preprints allowed, and acceptance turns on whether the claims are supported by the evidence, not on novelty. AI assistance is allowed as a "general-purpose assistive tool", but submissions that "appear to be largely LLM-generated will be closely examined". AFACS's drafting, pipeline, analysis, documentation check and all coding were done by AI under James's direction, so expect that scrutiny, and make sure the paper is his own after his read.

**Quota.** TMLR allows a sole author two single-author submissions a year ("Generalized Harmonic Quota Rule, with parameters N_1 = 2"), and desk rejections count. Papers 02 and 06 together use the whole budget, leaving none for a resubmission. **Recommendation:** submit paper 02 first; submit AFACS once the year boundary has passed (check TMLR's quota tool), which also leaves time for the human-coder study if James wants it first.

AFACS fits TMLR because its claims are deliberately limited: a framework, an audit of a public dataset, and evidence that the framework can be applied *consistently*. TMLR's readers include the people who build and study multi-agent LLM systems; MAST, the dataset audited, was published at NeurIPS.

**The alternative is a safety journal** such as *Safety Science*, whose readers know HFACS. Those reviewers would almost certainly ask for human inter-rater reliability, which HFACS papers normally report and this paper does not yet have. That route therefore needs the human-coder study first (the calibration set is frozen; it needs at least two independent coders who can read software traces). The two routes don't conflict: the human validation can be its own paper.

## What changed from the preprint (`../../paper.pdf`)

| | Preprint v1.0 | Journal version (`paper.pdf` here) |
|---|---|---|
| Format | House style, IEEE numeric citations | TMLR style file, author-year citations |
| Length | 19 pages | 19 pages; main text about 11.5 pages (about 4,400 words plus tables), then appendices |
| Author | Named, CitadelAero, credentials | Anonymous |
| Repository | Linked | No link; materials in an anonymised supplement |
| Added | | Appendix E, the annotator prompt; a broader impact statement; AI-use and data availability statements |
| Removed | | The future-work paragraph on an aviation dispatch evaluation (off-topic for TMLR and it hints at the author's identity) |
| Reworded | "The codebook is the author's." | "The codebook was written for this study." |
| Reworded | Discussion opened "The extension earns its place." | "...which suggests that they capture something a single-agent framework misses; whether independent human coders would code them as often is the question for the validation study." AI-only coding can't support the stronger wording. Consider making the same change in the preprint's next version |
| Added sentence | | The contributions paragraph now says plainly that the pilot measures consistency, not correctness |

No result or number in the preprint was changed, but this version adds a post hoc analysis (next section).

## Independent check of this version (4 November 2026), and what changed as a result

A separate AI auditor compared this version with the preprint and recomputed the agreement figures. The conversion was faithful and the PDF anonymous and compliant. It found:

- **Layer agreement was inflated** (major). Kappa over all 250 traces includes the traces at least one coder judged failure-free, where every layer is absent for both. Recomputed on the traces both coders judged failed (checked independently; `results/agreement_both_failed.md`, made by `scripts/posthoc_both_failed.py`): between models, L4 0.68, **L3 0.49**, L2 0.65; between runs, 0.70, 0.64, 0.69; individual codes 0.49 and 0.57. The abstract and Results now lead with these figures, the all-trace figures are kept with the reason they are higher, and a new Appendix C table gives the both-failed results. *The preprint (v1.0) still reports only the all-trace figures; a v1.1 should add these.*
- **Claims softened:** "In the AI coding, supervision failures appear…" (abstract); "The quotes were genuine" (not "the evidence"); the comparison with MAST's judge is now "for context only" and "not directly comparable".
- **Caveats added:** labelled reasoning is logged in full in only two frameworks (OpenManus and HyperAgent), so the scarcity of the *stated* grade partly reflects logging, and HyperAgent's violation rate comes from 13 traces; the AppWorld match (21 of 23) is little better than calling every trace a failure (20 of 23); the documentation check was made by AI research agents in a single pass without a second rater.
- **Supplement leaks fixed:** a Claude session link in `scripts/pilot.py` (it appears in the public commit history, so it identified the repository); the coding guide written to the author (dropped); `docs/related_work.md`, an internal note that listed the aviation-evaluation material (dropped); "shown to him… he changed" in the codebooks; "the investigator hand-codes" in `sample.py`. The supplement now has `version_history.txt`: commit times, without identifiers, showing that the calibration key fingerprint (14:04 UTC, 3 November) and the final codebook and prompt (21:47) came before the first AI coding (22:07).
- **Smaller fixes:** `\citet` for Wiegmann and Shappell; "CC BY 4.0" spelt one way; Appendix E referenced from the Method; the AI statement says what each audit covered.

## Remaining weaknesses a reviewer may raise

1. **No human coders.** The most likely objection. The paper is open about it (Sections 4 and 8), and the frozen calibration set shows the validation is designed, not just promised. If reviewers insist, the answer is the second study.
2. **A Claude model coding traces, some of them produced by Claude models.** It may share their blind spots; stated in the limitations.
3. **Codebook contamination of the Ezell pairing.** Disclosed. Codebook v1.1 removes the stated pairing for future coding, but the pilot's pairing result stays untestable.
4. **One dataset.** MAST's labels are noisy and its traces are benchmark failures, not incidents with harm. Stated.
5. **Agreement on supervision is moderate** (κ 0.49 between models on both-failed traces). Now reported; the human study should check whether the L3 definitions need tightening.
6. **The design check is AI checking AI.** Now disclosed; a second rater would strengthen it.

## What James needs to do

1. **OpenReview profile:** the same account serves both TMLR submissions (see paper 02's `SUBMISSION.md`, step 1).
2. **Read the journal version** (`paper.pdf` in this folder).
3. **Build the supplement:** `python3 papers/06-afacs/submissions/tmlr/make_supplement.py` writes `submissions/tmlr/build/supplement.zip` (about 7 MB). It replaces your name in the codebook and code comments with "the investigator", removes session links, leaves out the plain-English guide, the coding guide, the internal related-work note and the full reference library, adds `version_history.txt`, and checks for a list of identifying patterns. The list can't catch everything, so look through `submissions/tmlr/build/supplement/` before uploading. Traces are not included (benchmark questions); the pipeline recreates them from MAST.
4. **Submit on OpenReview** (https://openreview.net/group?id=TMLR) with `paper.pdf` and `supplement.zip`.

Submitting both papers to TMLR is allowed but uses the whole year's quota (see above). They share no results, but their AI-use and data-availability statements are near-identical, which links the two anonymous submissions; reword one of them if that matters to you.

## Answers for the OpenReview form

- **Title:** Extending AI-Agent Incident Analysis to Multi-Agent Systems: AFACS, an HFACS-Based Framework, and an Audit of Public Traces
- **Abstract:** copy from `paper.tex`, turning `$\kappa$` into κ, `--` into an en dash, `\%` into %, and LaTeX quote marks (``…'') into ordinary quotes.
- **Submission length:** regular (main text about 11.5 pages), if the form asks.
- **Suggested action editors** (from TMLR's [editorial board page](https://jmlr.org/tmlr/editorial-board.html), 4 November 2026; confirm they are still listed):
  - Tianmin Shu (Johns Hopkins University): computational cognitive science, human-AI collaboration
  - Tim G. J. Rudner (University of Toronto): AI safety, AI alignment
  - A. Feder Cooper (Yale University): ML security, red teaming, evaluations
  - Masha Itkina (Toyota Research Institute): human behaviour modelling, failure detection
  - Paul Pu Liang (Massachusetts Institute of Technology): human-AI interaction

  As for paper 02, action editors at Anthropic are left out, because Claude models did the coding.
- **Competing interests:** "The author is the founder of CitadelAero, which builds AI tools for aviation. No financial relationship with Anthropic, whose models were used as annotators."
- **Funding:** none.
- **Human subjects:** not applicable; no human participants (the planned human-coder study is not part of this submission).
- **Previous publication:** preprint only (not linked).

## For the camera-ready version, if accepted

Switch to `\usepackage[accepted]{tmlr}`, fill in `\month`, `\year` and `\openreview`, add the author block, change "the authors" back to "the author", restore the competing-interests and disclaimer paragraphs, replace the data availability sentence with the repository link, and move the AI-use statement into the acknowledgements.
