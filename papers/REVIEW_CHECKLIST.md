# Author review checklist

Working through the points each paper's README flags for James, one at a time. Each item records the decision and what was changed.

Status: ☐ open · ▶ in progress · ✔ done

## Part A: decisions that apply to all five papers

| # | Item | Papers | Status | Decision |
|---|---|---|---|---|
| A1 | Byline, author note and disclosure statements (affiliation, credentials, competing interests, AI-assistance wording, the Anthropic-sources note) | all | ✔ | Affiliation **CitadelAero**. Credentials as an author footnote: commercial pilot (Senior First Officer), aviation flight safety officer, aviation safety and compliance consultant (human factors); MSc Human Factors in Aviation. Competing-interest line and AI-assistance text **standardised across all five** (text in `STYLE.md`). Applied in the v0.4 LaTeX conversion. |
| A7 | **Format**: LaTeX-typeset single-column technical report (Latin Modern, A4, running header with rule, centred page numbers, simple title block without keywords, numbered sections, bold run-in headings, numbered equations, booktabs tables with captions above and source file, consistent Matplotlib colours, small bold-label captions, IEEE numeric citations, siunitx, British spelling, monospace code) | all | ✔ | Requested by James with A1. Shared style `_build/techreport.sty`; house rules rewritten in `STYLE.md`. All five converted to `paper.tex` + `references.bib` (v0.4), each checked independently for fidelity to v0.3: every sentence, number, quotation, table cell and citation carried over; conversion-check fixes applied. |
| A2 | Where and how the papers will be published (arXiv, website, journal/workshop), which sets length, format and whether repository links can be cited | all | ✔ | **Website/portfolio first**; journals, forums and arXiv later. **Make the Research repository public** (James's choice, AFACS included). Pre-publication scan on 4 Nov 2026: no secrets in history (5 pattern hits were base64 font data in old HTML builds), all commits authored as noreply@anthropic.com, no third-party PDFs committed, MBPP data CC BY 4.0 with attribution. James changes visibility in GitHub settings; Materials paragraphs then link to the public folders. |
| A3 | Voice: "I" or "this paper" | all (04, 05 used "I"; 01–03 mixed "we") | ✔ | **Impersonal** throughout ("this paper", passive for methods); no "I"/"we" outside quotations, so no check carried out by the AI assistant is claimed as the author's own. Applied after the v0.4 conversion. |
| A4 | ICAO Annex 19 Amendment 2 (applies 26 Nov 2026): which edition is the baseline | 01, 03 | ✔ | **Keep the 2nd edition** (papers dated 4 Nov 2026) and **flag the amendment clearly** (it renames component 1 and elements 3.1 and 3.3, deletes Appendix 2 Standard 3.1.2, redefines SPI, renumbers 5.3→5.4; corrected from "three elements" after checking the State letter). Update citations at the first revision after 26 Nov 2026. |
| A5 | ICAO manuals read from non-ICAO copies: spot-check quotes against licensed copies | 01, 03, 04 | ✔ | James has **no access to licensed ICAO copies**. Keep the provenance disclosures; cross-check each ICAO quotation against a second, independently hosted copy where one exists and record the result in each `sources.md`. Re-check against licensed copies before any journal submission. Results (v0.4): Annex 19 quotes in 01 matched the Swiss FOCA copy; Doc 9995 quotes in 04 matched the SKYbrary copy. **Open:** Doc 9868 §1.1.4 quote (paper 04) rests on one copy; ICAO's Asia–Pacific copy blocks automated access, so James could open it in a browser to confirm. Paper 03: Annex 19 (PNG AIC copy), Doc 9859 (CAA Nepal copy) and Annex 6 3.3.2–3.3.3 (Swiss FOCA copy) all matched. |
| A8 | Licence and merge | all | ✔ | Paper text **all rights reserved** (© 2026 James Le Cuirot); code MIT; MBPP-derived data CC BY 4.0. Open a **pull request** from the working branch into `main` after the conversion check, so public links point at `main`. The repo had no `main`: its default branch was `claude/zen-bardeen-sf0mtp` (AFACS work). James chose to **rename that default branch to `main`** in GitHub; the PR then targets `main`. **Done 4 Nov 2026:** James renamed the default branch to `main` and asked for the research to be pushed straight to `main`; the papers branch was merged into `main` (no conflicts, no files outside `papers/` changed, AFACS tests 57/57 passing). |
| A9 | Publication label: personal preprints or a numbered CitadelAero technical report series | all | ✔ | **Keep as personal preprints** ("Preprint v1.0, <date>. Not peer reviewed.") with **CitadelAero** as the affiliation; text © James Le Cuirot. Released papers are linked from James's website and the CitadelAero website. |
| A6 | Reliance on Anthropic research posts that are not peer reviewed | 01, 02, 03, 05 | ✔ | **Corroborate where possible**: keep them, labelled as company research reports; add independent sources alongside wherever they exist (e.g. UK AISI's own incident report, METR's investigation, peer-reviewed or arXiv versions); state in limitations where a fact rests on one company's account. |

## Part B: paper by paper

On 4 November 2026 James accepted the recommended defaults for the routine items (marked "Default accepted"). The items still open need his aviation judgement.

Other research repositories (pc24-study, CitadelAero research-studies and others) **stay separate** from this hub (James, 4 Nov 2026).

### 01 Just Culture for Machines — **released as Preprint v1.0 (4 Nov 2026)**
| # | Item | Status | Decision |
|---|---|---|---|
| B1.1 | Aviation accuracy and tone of §2 and Table 1 (S1 wording; why P2 departs from FOQA protection; Art. 16(6) carve-out; Danish case presented as confounded) | ✔ | Approved by James ("01 fine") after reviewing the condensed Section 2 passages. |
| B1.2 | Is the formal argument (§4.1, assumptions A1–A4) clear to aviation readers? | ✔ | Default accepted: keep §4.1 as audited (assumptions A1–A4 stated where the claim is summarised). |
| B1.3 | Reason (1997), Marx (2001), Dekker (2025) seen only via secondary sources: check wording and add page numbers if you hold the books | ✔ | Default accepted: keep the "as cited in" attribution; add page numbers only if the books are consulted later. |
| B1.4 | Reference-style choices (legal citation form; secondary-source entries; screen names) | ✔ | Superseded by A7: IEEE numeric style via BibTeX; legal designations kept in the text. |

### 02 Do LLM Monitors Miss Rare Threats? — **released as Preprint v1.0 (4 Nov 2026)**
| # | Item | Status | Decision |
|---|---|---|---|
| B2.1 | Disclose that each model call's context contained an account e-mail field (no address given)? | ✔ | Default accepted: keep the disclosure (no address printed). |
| B2.2 | H2 presentation: registered GLMM kept as the result, accurate refit reported post hoc | ✔ | Default accepted: registered GLMM stays the registered result; accurate refit and exact paired test reported as post hoc. |
| B2.3 | Length (~7,650 words of prose) | ✔ | Default accepted: no further cuts for the website; trim to a venue's limit when submitting. |

### 03 From RSP to SMS — **released as Preprint v1.0 (4 Nov 2026)**
| # | Item | Status | Decision |
|---|---|---|---|
| B3.1 | Table 2 ratings (single coder): the debatable cells (OpenAI 3.2 = D; Anthropic/OpenAI 4.1 = P; OpenAI 1.3 = P) | ✔ | Agreed by James as rated (single-coder judgements, disclosed). |
| B3.2 | Documents not read (Anthropic Frontier Compliance Framework; SB 53 statute; OpenAI web pages) | ✔ | Default accepted: keep the scope note naming documents that could not be read. |
| B3.3 | Secondary routes: Annex 6 Part I 3.3.3 (via CAA NZ checklist); Reg (EC) 300/2008 (UK text only) | ✔ | Resolved: Annex 6 3.3.2–3.3.3 matched a second (Swiss FOCA) copy in v0.4; Reg (EC) 300/2008 stays cited from the UK assimilated text with that noted. |
| B3.4 | The twelve proposed safety performance indicators (§6), reviewed as a practitioner | ✔ | Accepted by James as sensible proposals; kept labelled as untested. |
| B3.5 | Length (~8,700 words incl. tables) | ✔ | Default accepted: no further cuts for the website. |

### 04 Checkride or Jump Seat?
| # | Item | Status | Decision |
|---|---|---|---|
| B4.1 | Title: "Checkride or Jump Seat?" or "Checkride or Fly on the Wall?" | ☐ | |
| B4.2 | Definitions of checkride, line check, LOSA and mixed EBT against current practice | ☐ | |
| B4.3 | The rubric's observable behaviours, from an EBT instructor's view (restore EASA's "grade 3 = average" norm?) | ✔ | Default accepted: keep the pilot rubric as run; restoring EASA's norm reference (grade 3 = average) is listed as future work. |
| B4.4 | The non-jeopardy translation (§4): jeopardy ≈ optimisation pressure from training on observation data | ✔ | Default accepted: keep the non-jeopardy translation (§4). |
| B4.5 | Scripted "control" responses: keep, drop, or replace with ones you write | ✔ | Default accepted: keep the scripted controls, labelled post hoc and exploratory. |
| B4.6 | §5.3 framing of the ORO.FC.231(h)(3)(ii) parallel | ✔ | Default accepted: keep the narrowed §5.3 framing. |
| B4.7 | Name Delta Air Lines (as Klinect et al. do) or keep "one US airline" | ✔ | Default accepted: keep "one US airline". |

### 05 Untrusted by Design
| # | Item | Status | Decision |
|---|---|---|---|
| B5.1 | Spot-check EASA quotations (DHO-01–07, Table 2, RU-04, ET-01, MOC ET-02-2, RO-01, levelling table) | ✔ | Default accepted: quotations were verified verbatim against the official EASA PDFs by two audits, and the v0.4 check confirmed all 199 quotations unchanged. |
| B5.2 | The "alternating the end user" typo in MOC DHO-01: flag it or not | ✔ | Default accepted: keep the footnote flagging the apparent typo. |
| B5.3 | Fairness of the gap analysis: has EASA deliberately scoped out an adversarial AI? | ☐ | |
| B5.4 | AI Days slide statements characterised fairly as work in progress | ✔ | Default accepted: keep the slide-based statements characterised as work in progress. |
| B5.5 | Operational realism of §5.4 (audit budgets), §5.7 (reportable AI events), §7 (ground tools) | ☐ | |
| B5.6 | Paywalled standards (DO-178C, ARP4754B, ARP4761A): add precise references if you have access | ✔ | Default accepted: no access to the standards; keep the current references to FAA/EASA guidance and catalogue entries. |
| B5.7 | Digital Omnibus (Reg (EU) 2026/1744) and what it means for implementing rules | ✔ | Default accepted: keep the Digital Omnibus text as written. |
| B5.8 | Terminology: aviation-specific "trusted" (= conventionally assured) or AI-control usage | ☐ | |
