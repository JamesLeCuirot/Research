# Paper 01: journal submission to Safety Science

**Target:** *Safety Science* (Elsevier), research paper, through Elsevier's Editorial Manager.
**Status (4 November 2026):** submission package drafted; waiting for James's read and edit (needed for the AI declaration to be true; see below). Not yet submitted.

## Why Safety Science

- **Its readers know just culture.** Protected reporting, ASRS and Regulation 376/2014 are its home ground, so the aviation half of the argument will be read by people who can judge it, and the AI half is new to them.
- **Its AI policy allows this paper.** Elsevier allows generative AI in manuscript preparation if it is declared in a statement above the references ([Elsevier's policy, as summarised by CASRAI](https://casrai.org/guides/elsevier-generative-ai-authorship-policy); [Research Information on the update](https://www.researchinformation.info/news/elsevier-updates-generative-ai-policies-for-authors-and-editors/)). The manuscript has that statement.
- **No fee on the standard route.** It is a hybrid journal, so publishing on the subscription route is free; open access is optional and charged.

**Ruled out:**
- ***AI & Society*** (Springer). It fits the topic and allows Research articles of up to 10,000 words with double-blind review, but its guidelines say LLM use "for tasks other than grammar and translation" is "strongly discouraged" ([submission guidelines](https://link.springer.com/journal/146/submission-guidelines)). This paper was drafted with AI help, so it would start at a disadvantage.
- **ICML 2027 position track.** It needs an in-person presentation.

**Not verified.** Elsevier's guide page for *Safety Science* blocks automated access, so these points come from search results and need checking on [the guide](https://www.sciencedirect.com/journal/safety-science/publish/guide-for-authors) before submitting:
- Abstract of no more than 250 words (the journal version has 244).
- 3 to 5 highlights of no more than 85 characters each, in a separate file whose name contains "highlights" (done: `highlights.txt`).
- Not confirmed: the word limit, whether review is single- or double-anonymised, and whether the journal takes any reference style at first submission ("Your Paper Your Way", which most Elsevier journals offer). The package works either way:
  - The manuscript is anonymised, and the author details are on a separate title page.
  - References are numeric. If the journal requires its own style at first submission, change `\bibliographystyle{elsarticle-num}` to `elsarticle-harv` and the citation commands to author-year.

## What changed from the preprint (`../paper.pdf`)

| | Preprint v1.0 | Journal version (`paper.pdf` here) |
|---|---|---|
| Format | House style | Elsevier `elsarticle`, review layout (double-spaced, line numbers), numeric references |
| Length | About 7,840 words of body text | About 7,250 words of body text, abstract of 244 words |
| Author | Named on the paper | On a separate title page (`title_page.pdf`); the manuscript is anonymised |
| Aviation section | Full regulatory detail | Same structure and key quotations. Cut: NASA's ASRS history slides, the full list of waiver conditions, the UK and Regulation 965/2012 detail (now one sentence each), and the long Annex 19 Amendment 2 footnote |
| AI section | | Cut: secondary detail on MacDiarmid et al., Drori et al., Hopkins et al., Greenblatt and Fish, Wang et al., Li et al., Dietz et al. Each source is still cited for its main point |
| Removed | "Judging by its chapter titles and publisher's description (the text was not seen), Dekker contrasts…" | Gone: a journal paper shouldn't cite a book that wasn't read |
| Removed | "Semantic Scholar and OpenAlex were rate-limited, and Elicit was not available" | Gone (process detail; the search itself is still described) |
| Reworded | "Aviation safety professionals will recognise this problem." | "Safety scientists will recognise this problem." |
| Reworded | "The author writes from aviation safety practice…" | "The analysis is written from aviation safety practice…" (anonymisation) |
| Added | | Keywords, highlights, the Elsevier generative-AI declaration, a data availability statement |

The argument, the formal statement, the table, the six principles and the five predictions are unchanged.

## Before submitting: what James must do

1. **Read and edit the manuscript yourself.** The Elsevier declaration says "After using this tool, the author reviewed and edited the content as needed and takes full responsibility." It must be true when you submit. This matters more here than at TMLR: *Safety Science* reviewers will read the aviation sections as experts.
2. **Check the guide** (the four unverified points above).
3. **Register on Editorial Manager** for *Safety Science*. The submit button is on the journal's home page.
4. **Upload:**
   - `paper.pdf`, or `paper.tex` with `references.bib` (the manuscript, anonymised);
   - `title_page.pdf` (title page, with the declarations);
   - `highlights.txt`;
   - `cover_letter.md`, pasted into the cover letter field.
5. **Enter in the system:** the competing-interest declaration (Elsevier's form: "The author is the founder of CitadelAero, which builds AI tools for aviation"), funding (none), and keywords.
6. **Suggested reviewers,** if asked. Candidates from the literature, whose current affiliations and e-mail addresses need checking:
   - Sidney Dekker (just culture);
   - Barry Kirwan (AI and aviation safety culture);
   - an AI-safety researcher who works on chain-of-thought monitorability but not at OpenAI or Anthropic (for example an author of Emmons et al. 2025).

## Likely reviewer questions

1. **"Is AI training within scope?"** The cover letter answers this: a core safety-science concept, applied to a technology entering safety-critical work. If the editor disagrees, the fallback is a journal with a broader AI-and-society remit that allows declared AI drafting.
2. **"The formal argument is close to definitional."** The paper says so itself (Section 4.1). Its value is in making the conditions explicit and testable.
3. **"The aviation evidence is observational."** Stated in Section 2.5 and the limitations.
4. **"Most AI evidence comes from two companies."** Stated in the limitations.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex`, `paper.pdf` | The anonymised manuscript (45 pages in review layout) |
| `references.bib` | The preprint's references, unchanged |
| `title_page.tex`, `title_page.pdf` | Title page with author details and declarations |
| `highlights.txt` | The highlights |
| `cover_letter.md` | Cover letter |
| `SUBMISSION.md` | This file |
