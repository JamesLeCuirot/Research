# Submission plan

Where each paper could go after its preprint release, with the rules that matter. Researched on 4 November 2026 from official calls and author guidelines; dates marked "expected" are last year's, because the 2027 call was not yet published. **Re-check every deadline and policy on the venue's own page before submitting.**

## Journal packages (4 November 2026)

Four papers have a journal submission package in their own `journal/` folder. Each has a `SUBMISSION.md` that gives the reasons for the journal choice, what changed from the preprint, what an independent check found, the decisions James must make and the steps to submit. **None has been submitted**: James submits each one himself, after reading and editing it.

| Paper | Journal | Package | Main open points for James |
|---|---|---|---|
| 02 Do LLM Monitors Miss Rare Threats? | *Transactions on Machine Learning Research* (TMLR) | [`02-…/journal/`](02-do-llm-monitors-miss-rare-threats/journal/SUBMISSION.md) | OpenReview profile (moderation can take two weeks); his own read; whether to add a non-Claude monitor now or offer it in the rebuttal |
| 06 AFACS | TMLR | [`06-afacs/journal/`](06-afacs/journal/SUBMISSION.md) | TMLR allows a sole author two submissions a year, so submit after paper 02, ideally once the quota year turns; or run the human-coder study first |
| 07 Same Actions, Different Endings | *Safety Science* (Elsevier) | [`07-…/journal/`](07-same-actions-different-endings/journal/SUBMISSION.md) | Two anonymised OSF view-only links; Elsevier's rule that the text must reflect his own intellectual contribution; CitadelAero's 2 October rule against journal submissions |
| 01 Just Culture for Machines | *Safety Science* | [`01-…/journal/`](01-just-culture-for-machines/journal/SUBMISSION.md) | Elsevier's rule as above; strengthen the safety-science grounding (read and cite Reason, Dekker, research on under-reporting) or choose another venue |

The venue research for each paper, the original submission plan, follows. The AAAI-27 workshop route for paper 02 was dropped because it needs an in-person presentation.

## Rules that apply to every submission

- **AI-assisted drafting.** These papers were drafted with AI assistance, and say so. Venues differ:
  - **Accept disclosed AI assistance:** ICML (2026 policy), FAccT, TMLR, Elsevier journals (e.g. *Safety Science*), Cambridge University Press (*The Aeronautical Journal*), IEEE/DASC, arXiv.
  - **Restrict it:** AIES 2026 banned LLM-generated text (editing only); the NeurIPS 2026 position track required "substantially human-written" papers; *Human Factors* (SAGE) allows LLMs as a copyeditor only; LessWrong/Alignment Forum (March 2026 policy) wants LLM text in labelled blocks and is close to zero-LLM for first-time users. For these, the text would need rewriting in the author's own words first.
- **Double-blind venues.** Remove the author's name, CitadelAero, the credentials footnote, the Materials paragraph and any link to the GitHub repository. Preprints are allowed at every double-blind venue listed here, but do not cite or link the repository in the submission.
- **arXiv.**
  - *Endorsement:* since 21 January 2026, automatic endorsement needs an institutional email and a prior accepted paper in the same area. A first submission therefore needs a personal endorser who is an established arXiv author in that category.
  - *Position and review papers in computer science* must already be peer reviewed at a journal or conference before arXiv accepts them (policy of 31 October 2025). Papers on technology's impact on society in **cs.CY** are exempt. Original research (paper 02, and 04 with its pilot) is not affected.
  - *Suggested categories:* 01 cs.CY (cross-list cs.AI, cs.HC); 02 cs.LG or cs.AI (cs.CR, cs.SE, cs.HC); 03 cs.CY (cs.AI); 04 cs.AI (cs.HC, cs.CY); 05 cs.CY (cs.AI).
  - arXiv asks authors to report significant generative-AI use. Licence options include the arXiv non-exclusive licence (keeps all other rights) and CC BY variants.
- **Already closed for 2027:** FAccT (3 Nov 2026), SaTML (29 Sep 2026), AAAI-27 AI Alignment track (21 Aug 2026), ICLR 2027 main track (25 Sep 2026), CHI 2027 full papers (10 Sep 2026).

## Paper 02: Do LLM Monitors Miss Rare Threats? (empirical)

| Priority | Venue | Deadline | Length / format | Notes |
|---|---|---|---|---|
| 1 | **AAAI 2027 Workshop on Trustworthy Evolution of AI Agents** (Montréal, 22–23 Feb 2027) | **20 Nov 2026 AoE** (strict); notification 2 Dec 2026 | Up to 8 pp full paper, AAAI 2027 author kit; refs and appendices usually excluded | Verified on the official page. Non-archival; papers under review elsewhere welcome; double-blind. The page does not state an in-person requirement or an AI-text policy. Submit via OpenReview: https://openreview.net/group?id=AAAI.org/2027/Workshop/Trust4RSI-Agent |
| 2 | **TMLR** | Rolling | Any length | Accepts disclosed AI use; preprints allowed; no fees; keeps the full paper. https://jmlr.org/tmlr/author-guide.html |
| 3 | ICML 2027 main track | Expected late Jan 2027 | 8 pp + refs/appendix (2026) | Call not yet published |
| — | arXiv | Any time | — | cs.LG/cs.AI; needs an endorser |

## Paper 01: Just Culture for Machines (position)

| Priority | Venue | Deadline | Length / format | Notes |
|---|---|---|---|---|
| 1 | **ICML 2027 Position Paper track** | Expected late Jan 2027 (2026: 28 Jan AoE) | 8 pp + unlimited refs/appendix (2026) | Title must start "Position:" and include an "Alternative Views" section. Acceptance also satisfies arXiv's peer-review rule |
| 2 | **Safety Science** (Elsevier) | Rolling | Research Paper (limits not verified) | Readership knows just culture; Elsevier allows declared AI-assisted drafting |
| 3 | ICLR 2027 workshop | ~1 Feb 2027 (workshop list out 29 Nov 2026) | Per workshop | Feedback route; workshop review does not satisfy arXiv |
| — | arXiv | Any time | — | cs.CY, framed around the testable predictions |

## Paper 03: From RSP to SMS (governance)

| Priority | Venue | Deadline | Length / format | Notes |
|---|---|---|---|---|
| 1 | **Safety Science** or **Reliability Engineering & System Safety** (Elsevier) | Rolling | Research paper (limits not verified) | SMS and SPI-literate readership |
| 2 | **AI & Society** (Springer) | Rolling | Original ≤10,000 words; Open Forum ≤8,000 (from Springer call notices) | Policy argument fits |
| 3 | IASEAI '27 (Paris, 9–12 Feb 2027) | Talk proposals ~8–9 Jan 2027 (not verified on the official page) | Proposal | Governance audience |
| — | arXiv | Any time | — | cs.CY |

## Paper 04: Checkride or Jump Seat? (evaluation)

| Priority | Venue | Deadline | Length / format | Notes |
|---|---|---|---|---|
| 1 | ICLR 2027 evaluation/safety workshop | ~1 Feb 2027 | Per workshop | Evaluation-awareness community |
| 2 | **CHI 2027 Posters** | 21 Jan 2027 AoE | 4 pp single-column ACM, anonymous | Non-archival; suits the grading pilot |
| 3 | HFES ASPIRE 2027 (Grand Rapids, 27 Sep–1 Oct 2027) | Expected ~Feb 2027 | Per type | LOSA/EBT audience |
| 4 | ISAP 2027 (Auburn, 18–21 May 2027) | Call not open | — | Aviation psychology audience |
| — | arXiv | Any time | — | cs.AI (cs.HC, cs.CY) |

## Paper 05: Untrusted by Design (regulatory)

| Priority | Channel | Deadline | Format | Notes |
|---|---|---|---|---|
| 1 | **EASA RMT.0742 consultation** (Comment-Response Tool) | Q2 2027 | Comments | Step 2 NPA to be "published jointly with the updated Step 1 NPA" (EASA AI Days 2026). Step 2 covers airworthiness, ATM/ANS and drones; other domains are being replanned, so frame operational-oversight comments accordingly. https://hub.easa.europa.eu/crt/ |
| 2 | **The Aeronautical Journal** (RAeS / Cambridge) | Rolling | Research Article or Survey, <10,000 words preferred, APA | Preprints allowed; declare AI use |
| 3 | IEEE/AIAA DASC 2027 (Belfast, 12–16 Sep 2027) | Expected Feb 2027 abstract (2026: 7 Feb; full paper 25 Apr) | IEEE format | 2026 theme: AI in avionics; human factors track |
| 4 | EUROCAE WG-114 | Next meeting 7 Dec 2026 | Membership (individual, one WG: €700) or 3-month candidate trial | Non-members can comment on open consultations by registering |
| — | arXiv | Any time | — | cs.CY |

## Not verified

Several publisher author-guide pages (Elsevier, Taylor & Francis, Hogrefe, Springer) could not be opened; their preprint policies were confirmed from publisher-wide policy pages. The IASEAI and ISAP sites did not load. No 2027 calls yet for AIES, ICML, NeurIPS, HFES, SESAR Innovation Days or EAAP (next EAAP probably 2028).
