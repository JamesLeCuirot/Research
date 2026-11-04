# Paper 01: journal submission to Safety Science

**Target:** *Safety Science* (Elsevier), research paper, through Elsevier's Editorial Manager.
**Status (4 November 2026):** submission package drafted and independently checked. **Not ready to submit until James decides the two questions below and reads and edits the paper himself.**

## Two decisions for James first

1. **Elsevier's AI policy needs your own intellectual contribution in the text.** Elsevier's generative AI policy for journals ([primary page](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals), "Policy updated June 2026"):
   - Allowed: "Summarizing research literature in preparation for manuscript writing" and "Improving language, clarity, and readability of text written by the authors".
   - Not allowed: "Generating sections of a manuscript without genuine intellectual contribution from the author."
   - The declaration must give "the name of the AI tool used, the purpose of its use, and the extent of their oversight".

   This paper was drafted by Claude under your direction. Before submitting, rework it in your own words where you can, especially Sections 2 (aviation, your field) and 5 (principles), until the declaration is plainly true. The draft declaration says you "chose the topic and the argument to be made, directed the work, and reviewed and edited the text". Edit it to describe what you actually did.
2. **Is Safety Science the right journal?** The independent check rated two weaknesses as major for this audience:
   - **Thin grounding in safety science.** The just-culture foundations are cited through secondary sources (Reason 1997 via the GAIN report; Marx 2001 via PSNet and GAIN). None of the 51 references is a safety-science journal article. There is no engagement with critiques of just culture or with empirical research on under-reporting.
   - **The contribution is aimed at AI developers.** The formal result is "close to definitional", the predictions can only be tested in ML labs, and the aviation payoff is two sentences. That invites a desk rejection on scope.

   Two ways forward:
   - **(a) Strengthen it for Safety Science.** Read and cite Reason (1997, ch. 9) and Dekker's *Just Culture* directly, add empirical work on reporting cultures and under-reporting (aviation and healthcare) and the main critiques of just culture, and expand the "implications for aviation" paragraph into a short section on AI systems used in aviation safety. You have the expertise; this is a few days' reading. It would also answer point 1.
   - **(b) Choose an AI-focused venue** whose AI policy allows disclosed AI drafting. *AI & Society* is ruled out (below); a conference position track needs in-person presentation. A suitable journal would need researching.

   Recommendation: (a). The paper's most original element is the safety-science side, and that is where you can add most.

## Why Safety Science (if option a)

- **Its readers know just culture**, so the aviation half will be read by people who can judge it.
- **Its AI policy allows disclosed AI support** (see decision 1), unlike some alternatives.
- **Double-anonymised review** (from a Safety Science special-issue page, found by the checker through search results; not confirmed on the guide). The manuscript is anonymised and the author details are on a separate title page.
- **No fee on the standard route** (third-party sources describe it as a hybrid journal; open access is optional and charged).

**Ruled out:** *AI & Society* (Springer) says LLM use "for tasks other than grammar and translation" is "strongly discouraged" ([submission guidelines](https://link.springer.com/journal/146/submission-guidelines)); ICML 2027 position track (in-person presentation).

**Not verified** (Elsevier's guide page for *Safety Science* blocks automated access; check it [here](https://www.sciencedirect.com/journal/safety-science/publish/guide-for-authors)):
- the 250-word abstract limit (the abstract is 245 words, or 249 if hyphenated words are counted separately);
- 3–5 highlights of 85 characters or fewer, in a separate file (done: `highlights.txt`, 72–85 characters);
- any word limit, and whether any reference style is accepted at first submission. The references are numeric; if the journal requires its own style at first submission, switch `elsarticle-num` to `elsarticle-harv`.

## What changed from the preprint (`../../paper.pdf`)

Length, by one consistent count: about 7,690 words of body text in the preprint and about 7,380 in the journal version, excluding the table, footnotes and citation keys. The cut is modest, because the independent check led to several hedges being restored (below).

| | Preprint v1.0 | Journal version |
|---|---|---|
| Format | House style | Elsevier `elsarticle`, review layout (double-spaced, line numbers), numeric references. Table 1 is set single-spaced in small type so that it fits on one page |
| Author | Named on the paper | Separate title page (`title_page.pdf`); manuscript anonymised |
| Abstract | 245 words | 245 words, lightly reworded |
| Added | | Keywords, highlights, the Elsevier generative-AI declaration (immediately before the references), a data availability statement |

**Cut from the preprint:**
- **Aviation:**
  - NASA's ASRS history slides;
  - the competency-action and five-year conditions of the ASRS waiver ("among other conditions" now covers them);
  - Marx's "three classes of human fallibility" (the at-risk and reckless distinction is kept);
  - the UK detail (now one sentence) and the CAA;
  - the long Annex 19 Amendment 2 footnote (now one sentence: 5.3 becomes 5.4, and the principles quoted are substantively unchanged);
  - the sentence restating Amendment 2 at the end of Section 2.4.
- **AI:**
  - the objection-rate numbers in Greenblatt and Fish (the 16% to 1.4% result is kept);
  - "Misalignment is hardest to correct when it's concealed" (Hopkins et al.);
  - the detail of Anthropic's and OpenAI's reporting policies;
  - the content of the inoculation-prompting result (it is still cited);
  - the item-by-item list of single-company results in the limitations (now grouped by developer).
- **Other:**
  - Dekker (2025), which was cited from its chapter titles and publisher's description because the text was not seen;
  - the pointer to `sources.md`.

  Reason (1997) and Marx (2001) stay, because the paper cites them explicitly through the secondary sources it did read.

**Reworded:** "Aviation safety professionals will recognise this problem" became "Safety scientists will recognise this problem". "The author writes from aviation safety practice" became "The analysis is written from aviation safety practice" (anonymisation).

**Unchanged:** the argument, the formal statement (Section 4.1), Table 1's content, the six principles and the five predictions.

## Independent check of this version (4 November 2026)

A separate AI auditor word-diffed the journal body against the preprint and checked every condensed citation against `sources.md`. Fixed as a result:
- **Table 1 was cut off** in the review layout (rows 7–12 missing); it now fits.
- **Restored hedges and qualifiers:**
  - the search limits (Semantic Scholar and OpenAlex rate-limited, Elicit unavailable);
  - "should be checked by AI-safety researchers";
  - flight data monitoring "for larger aeroplanes", with the full quotation;
  - MacDiarmid et al.'s setting (a pretrained model given knowledge of hacking strategies; a classifier *prompt*);
  - Daniels et al.'s setting (GPT-4.1, single-turn environment, iterative DPO);
  - Drori et al.'s two mitigations;
  - "in the helpful-only setting";
  - P4 stated as a condition;
  - the air traffic controllers note;
  - FOQA de-identification;
  - Wang et al. as speculation;
  - "can generalise";
  - Dietz et al.'s citation placed on the factual claim;
  - the Art. 16(7) criminal-proceedings sentence;
  - Art. 16(12)'s "designated body" (P5 relies on it);
  - "binding EU law".
- **Highlights 3 and 4 overstated the paper.** They now read "can fail to put good behaviour above concealed misbehaviour" and "By default, correct AI behaviour on independent evidence…".
- **The abstract** again distinguishes data that are reported from data that are recorded.
- **The AI declaration** now follows Elsevier's primary template ("…of the published article") and placement (immediately before the references), and states the purpose and oversight.
- **The cover letter** no longer claims that safety science has "established" the reporting effect (Section 2.5 says the evidence is institutional consensus). It no longer says experiments showed concealment "instead of" behaving, and it says "disclosure-only". It is plain text, so it pastes cleanly.
- **The `references.bib` header comments** (internal notes) are removed.

## What James needs to do

1. Decide on points 1 and 2 above, and do the reading and rewriting that follows.
2. Check the four unverified points on the guide page.
3. Register on Editorial Manager for *Safety Science*.
4. Upload:
   - the manuscript (`paper.pdf`, or `paper.tex` with `references.bib`);
   - `title_page.pdf`;
   - `highlights.txt`;
   - the text of `cover_letter.txt` in the cover letter field.
5. Enter the competing interest ("The author is the founder of CitadelAero, which builds AI tools for aviation"), funding (none) and keywords in the system.
6. **Suggested reviewers,** if asked. These are candidates in the field, not drawn from the paper's references; check their current affiliations and e-mail addresses:
   - a just-culture researcher, for example Sidney Dekker;
   - a researcher on AI and aviation safety culture, for example Barry Kirwan;
   - a chain-of-thought monitorability researcher outside OpenAI and Anthropic, for example an author of Emmons et al. (2025).

## Note on sequencing

Paper 07 (Same Actions, Different Endings) is also prepared for *Safety Science*, and is the stronger fit (empirical; the journal published Oğuz et al., 2026, on LLM responsibility attribution). Submitting both to one journal is allowed. If you want to avoid two concurrent submissions there, send paper 07 first.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The anonymised manuscript (review layout) |
| `references.bib` | The preprint's references with the internal header comments removed |
| `title_page.tex`, `title_page.pdf` | Title page with author details and declarations |
| `highlights.txt` | The highlights |
| `cover_letter.txt` | Cover letter (plain text) |
| `SUBMISSION.md` | This file |
