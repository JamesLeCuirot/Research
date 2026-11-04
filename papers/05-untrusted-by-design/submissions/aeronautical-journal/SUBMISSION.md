# Paper 05: submission to The Aeronautical Journal

**Journal:** *The Aeronautical Journal* (Royal Aeronautical Society; published by Cambridge University Press), research article.
**Status (4 November 2026):** package ready for James's read and edit, in the journal's template. Not yet submitted. **The presubmission enquiry (below) is optional:** to submit straight away, skip it and let the cover letter make the case; the editor's desk decision answers the same question in days. the journal's scope is the main risk for this paper.

## Why this journal

- **Readers:** certification and systems engineers, operators, safety managers and regulators, and it is your own society's journal. The paper is about EASA's oversight objectives and how to show compliance with them.
- **A second paper there is allowed.** The rules set no limit per author, only that the same manuscript must not be under consideration elsewhere (`papers/JOURNAL_OPTIONS.md`). Paper 07 is going to the same journal (`../../../07-same-actions-different-endings/submissions/aeronautical-journal/`).
- **Single-anonymised review**, so the public preprint is no problem. Preprints on a personal website are not prior publication.
- **AI use is allowed if declared.** The manuscript declares it in the Acknowledgements, with tool, version, dates and access.
- **Length and format:** "Papers should preferably not exceed 10,000 words". This one has about 8,300 words of main text without the parenthetical citations, or about 8,600 as printed with them (headings, Table 1 and the footnote included); the abstract has 249 words. Single column; APA references; a nomenclature is required (included).
- **Process and fees:** at least two referees, typically 3–6 months; no fees on the standard route (open access optional, £2,610). A decision by spring 2027 would sit well with EASA's planned consultation in Q2 2027.

Cambridge's rules are those on its "Preparing your materials" page as checked on 4 November 2026 (the same check as for paper 07; see its `SUBMISSION.md` and `papers/JOURNAL_OPTIONS.md`).

## The scope risk and a presubmission enquiry

The journal's aims and scope never mention regulation, certification or AI. It has published certification papers, and AI reviews in 2025–26 that discuss regulatory challenges, but a regulatory gap analysis with no experiment or design work is at the edge of what it usually takes (`papers/JOURNAL_OPTIONS.md`, checked 4 November 2026). **Recommended:** a short presubmission enquiry to the editor at **aerojournal@aerosociety.com** before submitting, asking whether a regulatory AI-assurance paper is in scope and mentioning paper 07. A draft, to adjust to your voice:

> Subject: Presubmission enquiry: AI assurance and EASA's operational oversight objectives
>
> Dear Editor,
>
> Before I submit, could you tell me whether a paper of this kind would be in scope for The Aeronautical Journal? "AI Control for Aviation: A Gap Analysis of EASA's Operational Oversight Objectives for Advanced AI" (about 8,300 words) looks at the independent operational oversight system that EASA's draft AI concept paper (Proposed Issue 03, June 2026) would require for Level 3 AI. It compares the draft's threat model with research on monitoring AI systems that may work against their monitors, and proposes means of compliance for EASA and EUROCAE. It is a regulatory and assurance analysis with no experimental data. A preprint is at https://www.lecuirot.je/research/ai-control/.
>
> I am also submitting a separate experimental paper to the journal, on outcome bias in AI models applied to airline occurrence reports.
>
> Yours faithfully,
> James Le Cuirot
> CitadelAero, Jersey

If the answer is no, the fallbacks in `papers/JOURNAL_OPTIONS.md` are *Frontiers in Aerospace Engineering* (Intelligent Aerospace Systems section; best scope fit, but open access only at CHF 2,195), *CEAS Aeronautical Journal* and *IJAAA*.

`JOURNAL_OPTIONS.md` also suggested trimming to about 9,500 words in all (Section 6, "The other direction", being the natural cut) and leading with airworthiness and development assurance. **Neither was done here**: this version keeps the preprint's text word for word. Consider them in your own edit, or if the editor's reply points that way.

## What this version is

The preprint's text (v1.1, 4 November 2026; `../../paper.tex`) set in **the journal's own LaTeX class** (`aer.cls`, the same file as paper 07's, from the template files you downloaded on 4 November 2026). These are the only changes:

- **Title block.** Title "AI Control for Aviation" and subtitle "A Gap Analysis of EASA's Operational Oversight Objectives for Advanced AI"; the preprint's date and version line removed; your name as "J. Le Cuirot", with "CitadelAero, Jersey, Channel Islands" and james@citadelaero.com, as in paper 07. The preprint's note under your name (credentials) is kept, as the template's author note; drop it if you prefer (see below).
- **Headings.** First-level headings in capitals and second-level headings in title case, as in the template. The run-in headings (T1–T6 and the four in Section 6) are unchanged; the class sets them as its fourth-level headings.
- **Citations: IEEE numbers to APA author–year** (`apacite.bst` through natbib, as the class expects). Of the 114 citations:
  - **57 textual.** Where the text named the author just before the number ("Greenblatt et~al.~[n]"), the citation is now textual and the typed name was taken out, so it prints once: "Greenblatt et al. (2023)". Five are possessives ("Kutasov et al.'s (2025) SHADE-Arena"). One is capitalised at the start of a sentence ("Van der Weij et al. (2024)").
  - **12 year-only.** Where EASA or the FAA is named in the same clause as the work cited, only the year (and locator) is given, so that the name does not appear twice: "EASA's Artificial Intelligence Roadmap 2.0 (2023)", "a column EASA describes as "only anticipated and not complete" (2026b, Chapter D)". These are the ones you might prefer in full ("(EASA, 2026b, Chapter D)"); either is APA.
  - **45 parenthetical**, with every locator kept ("(EASA, 2026b, Section C.5.2)"). In the four citations of EU legislation the article that followed the number now comes before the author–year citation, inside the same parentheses: "(Regulation (EU) No 376/2014, Art. 4(1)(b); European Parliament and Council of the European Union, 2014)". "(compare [n, slide 22])" is now "(compare EASA, 2026a, slide 22)". Several works in one citation are in alphabetical order, as APA has it.
  - EASA and the FAA are cited by those short forms (both defined in the nomenclature, and the FAA in the text where it is first cited); the reference list gives the full names. APA 7's "et al." is used from the first citation (apacite would otherwise list up to five names the first time).
- **Nomenclature** added after the abstract: every abbreviation and identifier in the text and Table 1, alphabetical, lower case before upper case. There are no Greek symbols. EASA's objective identifiers (CRA, DHO, ET, IS, ORG, R-MDP, RO, RS, RU, SU-IMP) are described by what the paper says they cover, without spelling out the prefixes, which the paper does not do. Model and benchmark names (Claude, SHADE-Arena) are left out, as in paper 07; GPT is in.
- **The one footnote** is numbered in Roman numerals (i), as Cambridge asks.
- **End sections in the template's order:** Acknowledgements (the preprint's AI-assistance statement, completed as Cambridge asks, then the preprint's disclaimer paragraph), Competing interests (paper 07's wording, adapted), Financial support (new), Data availability (the preprint's Materials sentence, with a statement that no new data were created and the documents analysed are public and cited, and a note of the preprint), References. No ethics section (no participants) and no appendix.
- **Line numbers** for the reviewers; the journal's metadata commands left empty, as the template's guide asks.
- **References.** `references.bib` is the paper's own file with format-only changes for apacite, listed in its header: `@manual` entries made `@misc` (apacite prints `@manual` as "[Computer software manual]"); dates as month and day fields; "Accessed" notes moved to `lastchecked` ("Retrieved 3 November 2026, from …"); URLs that only repeated a DOI dropped (DOIs print as https://doi.org/ links); short citation forms for EASA and the FAA; braces to keep a few capitals. No bibliographic fact changed. The list follows APA as apacite implements it, which is the 6th edition in some details (for example, six authors, an ellipsis, then the last author, where APA 7 lists up to 20). Cambridge says the formatting of references is not grounds for rejection at submission, and the publisher sets them at acceptance.

**No word, number, quotation or claim in the abstract or main text changed.** A script stripped citations and markup from both versions (rendering the textual citations as printed) and compared the words: 8,527 words each, **no differences**; the only case differences are the 80 heading words. The abstract is byte-identical to the preprint's.

## Checked against Cambridge's "Preparing your materials" page (4 November 2026)

| Requirement | This manuscript |
|---|---|
| Research Article, preferably under 10,000 words, single column | About 8,300 words of main text (about 8,600 with citations as printed; about 11,100 with the abstract, nomenclature, end sections and references; the limit is "preferably", and word limits usually leave out references), single column |
| Journal template (Word or LaTeX) | `aer.cls` |
| LaTeX: upload the PDF only at first submission | Upload `paper.pdf`; the source is sent after provisional acceptance |
| Abstract up to 250 words, standalone, no references or citations; also pasted into the form | 249 words, no citations; unchanged from the preprint. It describes what the paper does, including that "it argues" for four transfers to frontier-AI safety cases |
| No keywords in the manuscript | None; enter them in the form |
| Nomenclature of all symbols and abbreviations, alphabetical, lower case before upper case, English before Greek | Done (no Greek symbols are used) |
| Tables titled, numbered and cited | Table 1, cited in Section 4.2 |
| Figures captioned beneath, numbered, cited | No figures |
| Boxes and code snippets labelled and numbered | None |
| Footnotes in Roman numerals, avoided if possible | One footnote (i), kept from the preprint; it could go into the text (below) |
| APA in-text citations | Yes |
| Competing interests in the manuscript | Yes |
| Financial support section | Yes ("no specific grant") |
| AI use declared: text generation in the acknowledgements, with tool, version, dates, access and a full description | Yes, except your own sentence (below). No AI was used for data analysis; there are no data |
| Organisation and address for each author | "CitadelAero, Jersey, Channel Islands"; add a fuller postal address if you want one printed |
| Alt text for figures | Not needed: no figures |

## The AI declaration and the records behind it

The Acknowledgements' "Use of AI" paragraph keeps the preprint's statement and adds what Cambridge asks. Each fact comes from the records, not from memory:

| Statement in the manuscript | Record |
|---|---|
| Literature searches, drafting and source verification with Claude (Anthropic), under your direction; an independent AI-assisted audit; several sources are Anthropic research reports | The preprint's own AI-assistance statement (closing text from `papers/STYLE.md`) |
| Used through Claude Code (claude.ai/code) | The `Claude-Session: https://claude.ai/code/session_…` trailers on the commits for this paper |
| On 3 and 4 November 2026 | `git log -- papers/05-untrusted-by-design`: first commits 3 November 2026 (`7fe31dc`, `d8e6b51`), last before this one 4 November (`5b9f9c2`); `sources.md`: "All sources were opened on 3 November 2026", additions in v0.4 on 4 November |
| The version history records the model as Claude Opus 5.5 | "Co-Authored-By: Claude Opus 5.5" on every commit that touches the paper's folder. This records the model of the sessions that committed the work; the records do not name the models of any separate drafting or checking agents |
| Audit 3 November; second-round verification and conversion check 4 November; tool and model version not recorded | `AUDIT.md`: "Auditor: independent fact-checker (AI), 3 November 2026", "Second-round verification (4 November 2026)", "v0.4 conversion check (4 November 2026)"; no tool or model is named there or in `papers/README.md` ("a separate AI agent") |
| This journal version prepared with the same tool and model on 4 November 2026 | This package's commit and its trailers |

The preprint's "The author is responsible for the final text" is replaced by the placeholder and Cambridge-style closing: "[AUTHOR TO DESCRIBE HIS OWN REVISION OF THE MANUSCRIPT]. The author is responsible for the content."

## Before you submit

1. **Optional:** send the presubmission enquiry (draft above) and wait for the reply, or skip it and submit directly.
2. **Read and edit the manuscript in your own words.** Then replace the placeholder `[AUTHOR TO DESCRIBE HIS OWN REVISION OF THE MANUSCRIPT]` in the "Use of AI" paragraph of the Acknowledgements in `paper.tex` with what you did, and rebuild (`latexmk -pdf paper.tex` in this folder). If you know which tool and model the audit agents used, put them in place of "tool and model version not recorded".
3. **CitadelAero's rule.** Paper 07's notes record that you overrode CitadelAero's research-plan rule against preprint and journal submissions for that paper. Decide whether the rule covers this paper too, and record the decision.
4. **Points you may want to change in your own edit.** None was changed here, because this version keeps the preprint's text:
   - Section 3.2 refers to "(Table 2)" and "Table 4" of Greenblatt et al.'s paper. This manuscript has only Table 1, so a reviewer may look for a Table 2 here; "(their Table 2)" would avoid that.
   - The one footnote (the "alternating" typo in MOC DHO-01). Cambridge asks for footnotes to be avoided where possible; the sentence could move into the text or be dropped.
   - The author note under your name (pilot, flight safety officer, consultant, MSc). Journal title pages usually carry only the name, affiliation and email, and the cover letter already says who you are.
   - The trim and reframing suggested in `JOURNAL_OPTIONS.md` (above).
5. **Read `cover_letter.txt`** and adjust it to your voice.

## How to submit

1. Go to the journal's submission system, **Editorial Manager**: https://www.editorialmanager.com/aeroj/ (Cambridge's "submitting your materials" page, checked 4 November 2026). It needs its own account, separate from Cambridge Core. Link your ORCID (0009-0009-6014-1298), which the journal requires for the corresponding author. Queries go to aerojournal@aerosociety.com.
2. **Keywords go in the online form, not the manuscript.** Use: artificial intelligence; AI control; EASA; certification; run-time monitoring; large language models.
3. Choose the article type **Research Article**, and a main and a secondary subject classification from the journal's list (likely certification or airworthiness, avionics and systems, or safety). The guidance warns that a wrong classification can lead to an out-of-scope rejection.
4. Upload `paper.pdf` only (Cambridge: "The LaTeX source file should not initially be submitted alongside the PDF"). Paste the abstract into its box, and paste in the cover letter. There are no figures, so no alt text is needed.
5. Declarations in the form:
   - **Competing interests:** "The author is the founder of CitadelAero, which develops AI tools for aviation safety and compliance teams. No CitadelAero product is discussed in this paper."
   - **Funding:** none.
   - **Data:** no new data; the documents analysed are public and cited; verification log and audit record at https://github.com/JamesLeCuirot/Research/tree/main/papers/05-untrusted-by-design.
6. **Suggested reviewers,** if asked. These are authors of work the paper cites; check their current affiliations, e-mail addresses and any conflicts:
   - Robin Bloomfield or John Rushby (assurance of AI systems from a dependability perspective);
   - John McDermid or Ibrahim Habli (AI safety cases and safety assurance);
   - Heidy Khlaaf (risk assessment and assurance of AI-based systems).

## Build

`latexmk -pdf paper.tex` in this folder (BibTeX runs automatically). On 4 November 2026: 25 pages, no errors, no undefined citations or references, no overfull lines. The log has one "Overfull \vbox … while \output is active" warning per page from the class's page layout; paper 07 shows the same.

## Files in this folder

| File | What it is |
|---|---|
| `paper.tex` | The manuscript, in the journal's class (named; single column). The PDF is not kept in the public repository, because it carries the journal's name and the Society's line and could be taken for a published article |
| `references.bib` | The paper's references, adapted for `apacite.bst` (format only; the changes are listed in its header) |
| `aer.cls` | The journal's LaTeX class, from its template files |
| `cover_letter.txt` | Cover letter |
| `SUBMISSION.md` | This file |
| `.gitignore` | Keeps `paper.pdf` and the LaTeX and BibTeX by-products out of the repository |

## Log

| Date | Event |
|---|---|
| 4 Nov 2026 | Package prepared in the journal's template (`aer.cls`) and checked against Cambridge's "Preparing your materials" page; word-level check against the preprint: no differences. Not submitted; presubmission enquiry not yet sent |
