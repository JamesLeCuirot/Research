# AAAI 2027 workshop submission: Trust4RSI-Agent (anonymised)

**For the author only. Do not upload this file.** The only file to upload to OpenReview is `paper.pdf`. This README names the author, the company and the repository in its checklists, so it must never go to the workshop.

Prepared on 4 November 2026 from the audited v1.0 preprint in `../../` (`paper.tex`, `results/`, `PREREGISTRATION.md`, `AUDIT.md`). Nothing outside this folder was changed, and nothing was committed.

## 1. The venue (call re-opened on 4 November 2026)

Call page: https://trust4rsi-agent.github.io/AAAI2027/ (AAAI 2027 Workshop on Trustworthy Evolution of AI Agents: An Agent Operating System Perspective).

| Item | What the call says |
|---|---|
| Submission deadline | "November 20, 2026, AoE"; "Deadlines are strict and will not be extended." 20 Nov 23:59 AoE = **21 Nov 2026, 11:59 UTC**. (The OpenReview form itself closes at 21 Nov 13:00 UTC, but work to the call's deadline.) |
| Notification | "December 2, 2026, AoE" |
| Workshop | "February 22–23, 2027 (one-day workshop; exact day TBA)", Palais des congrès de Montréal, Montréal, Canada |
| Format | "Submissions must be in English and follow the AAAI 2027 author kit"; "single PDF file"; "Full Papers (8 pages)"; "Short Papers / Position Papers (4 pages)"; "References and appendices are usually not included in the page limit." |
| Review | "The workshop follows a double-blind review process. Submissions must be anonymized." |
| Status | "Our workshop is non-archival. Manuscripts under review at other venues are welcome as well." |
| Submission site | OpenReview: https://openreview.net/group?id=AAAI.org/2027/Workshop/Trust4RSI-Agent |
| Not stated on the page | Any policy on AI-generated text; any in-person presentation requirement; a reproducibility checklist |

**The public v1.0 preprint is allowed.** The workshop is non-archival and welcomes manuscripts under review elsewhere, and the AAAI-27 policies also permit preprint servers. Do not cite or link the preprint or the repository in the submission, and avoid publicising this submission while it is under review. A reviewer could still find the preprint by searching; the call does not forbid that.

### Author kit

- Linked from the call page through the AAAI-27 submission instructions (https://aaai.org/conference/aaai/aaai-27/submission-instructions/, link "AAAI-27 Author Kit").
- Official URL: **https://aaai.org/authorkit27/**, which redirects to **https://aaai.org/wp-content/uploads/2026/10/AuthorKit27.zip** (server Last-Modified 21 Oct 2026 06:25 GMT; 5,496,654 bytes; SHA-256 `9406a545d5d213757245eb37118fe652b2fccf64f555aff28b49ebe2a780c960`; downloaded 4 Nov 2026).
- Version: `aaai2027.sty` declares `\ProvidesPackage{aaai2027}[2027/10/21 AAAI 2027 Submission format]` (the year in that line is the file's own; the zip entries are dated 21 Oct 2026). `AnonymousSubmission2027.tex` sets `/TemplateVersion (2027.1)`; that \pdfinfo is switched off by the `submission` option anyway.
- Copied here unchanged: `aaai2027.sty` (SHA-256 `01990f8d3716f8e39c5b28a7478f3ac6e28630d1161de6105a7217f5e7f60e43`) and `aaai2027.bst` (SHA-256 `5db7765ba99de5c1e4686f9b3940a0add9c5e702f2164514462bec130ccb6e3c`). They are needed to compile the source; the source is not uploaded at review time.

How the kit's rules were applied:

- Preamble exactly as in `AnonymousSubmission2027.tex`: `\documentclass[letterpaper]{article}`, `\usepackage[submission]{aaai2027}`, url, graphicx, natbib and caption with no options, `\frenchspacing`. Only `booktabs` (recommended by the kit) and `amsmath` were added.
- No disallowed package (hyperref, geometry, float, times, lmodern, subcaption, siunitx and the rest of the kit's list are all absent) and no disallowed command. `\setlength{\tabcolsep}` is used once, which the kit explicitly permits.
- Author "Anonymous Submission" with empty affiliations; the `submission` option prints "Anonymous submission" and the kit's review notice. No acknowledgements.
- Two-column US Letter, 10 pt Times-like text, title in Title Case (the kit asks for both words of a hyphenated term to be capitalised: "Pre-Registered"), no section numbers (kit default), no page numbers, no links or bookmarks.
- Captions under tables and figures; tables at 9 pt (`\small`, allowed).
- References with the kit's `aaai2027.bst` (author–year, set by the style). This replaces the preprint's IEEE style.
- All fonts are embedded Type 1 (15 fonts); no Type 3 and no CID/Identity-H fonts. The figures' own text (CID TrueType from Matplotlib) was converted to outlines, as the kit requires.
- Text inside figures is at least 9 pt: each panel is set at 47–49.5% of the text width (scale ≥ 1.13 on 8 pt tick labels).
- PDF version 1.5. Document metadata cleared with a cleaning step, as the kit asks for anonymous submissions (Section 4).
- The AAAI-27 main track limits papers to 7 content pages plus 2 of references. That rule is for the main track; this workshop's call sets 8 pages for full papers, which is what is used.

## 2. What is in this folder

| File | Contents |
|---|---|
| `paper.pdf` | **The file to upload.** 13 pages: main content on pages 1–8, references on pages 8–9, Technical Appendix on pages 9–13. |
| `paper.tex`, `references.bib` | Source (single .tex file). `references.bib` holds the 27 cited entries, copied verbatim from the preprint's `references.bib`. |
| `aaai2027.sty`, `aaai2027.bst` | From the official AAAI-27 author kit, unchanged. |
| `figures/` | The preprint's vector figures (`figures/report/*.pdf`), same data and shared colours (Haiku orange #E69F00, Sonnet blue #0072B2), with their text converted to outlines. |
| `check/build.sh` | Builds `paper.pdf` (pdflatex, bibtex, pdflatex ×3 in a temporary folder) and clears its metadata. |
| `check/clean_pdf.py` | The metadata-cleaning step (pypdf): copies the pages into a new file with no Info dictionary, no XMP stream and no pdfTeX `PTEX.*` keys. |
| `check/verify_numbers.py` | Checks every number in `paper.tex` against `results/` and the full paper (Section 5). |

Build: `sh check/build.sh`. TeX Live 2023 (Debian) needed these packages beyond the ones in the brief: `texlive-fonts-extra` (newtx, loaded by the kit), `texlive-plain-generic` (binhex.tex, needed by newtx) and `tex-gyre` (TS1 Termes metrics). The figure fonts were outlined once with Ghostscript 10.02.1: `gs -q -o out.pdf -dNoOutputFonts -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 in.pdf`; a 200 dpi render of every figure before and after showed the plotted marks and colours unchanged (only glyph anti-aliasing differs).

Build result: no errors, no undefined references or citations, no overfull boxes, no BibTeX warnings (four underfull lines remain, which the kit does not forbid). `pdfinfo`: 13 pages, US Letter, PDF 1.5, no Title, Author, Creator, Producer or dates. The main content (title to the AI-assistance disclosure) ends on page 8, with the References heading about four-fifths of the way down page 8's right column.

## 3. What was cut from the full paper, and why

The preprint is 23 pages (about 7,650 words of prose, 6 tables, 5 figures, 40 references). The submission keeps the research question, the human-factors background, the pre-registered design (H1, H1a, H2, H3, E1–E4), the methods, every confirmatory result with its exact numbers, the reversal, pop-out and crowding as candidate explanations, the limitations and the AI-control implications stated as hypotheses. Sentences were shortened or dropped; none was reworded to say something new, and no number was rounded differently.

Cut for anonymity:
- Author name, company, credentials footnote, date line ("Preprint v1.0 … Not peer reviewed").
- The Acknowledgement section's Competing-interests, Disclaimer and Materials (GitHub link) paragraphs. The AI-assistance paragraph is kept, anonymised, as "Disclosure of AI Assistance" inside the 8 pages.
- File paths (`PREREGISTRATION.md`, `results/…`, `sources.md`, `AUDIT.md`, `code/prompts/`, `data/…`), the table source lines, and commit hashes (they can be searched on GitHub). The pre-registration timing is kept with UTC times instead of hashes.

Cut for length (8 pages, two columns, figure text ≥ 9 pt):
- Background: the vigilance and alarm-reliability subsection (Mackworth; Klein and Feltmate; Warm et al.; Bliss et al.; Huegli et al.; Sorkin and Woods); most of "Monitoring in AI control" (APPS details, Griffin and Bhatt budget details, the detection studies of Kale et al. and Ye et al., the SHADE-Arena AUC and SLEIGHT-Bench catch-rate figures); Zheng et al., Liu et al., Chen et al. and Cai et al.; the Hautus 1/(2N) comparison; the "a criterion that moves with prevalence is not irrational" quotation; the Cutler and Paddock TIP definition and the Buser et al. sample size; Wolfe et al. (2007) Experiment 7 miss rates (0.21 and 0.18) and the details of Wolfe et al. (2013).
- "Base rates in deployment" (the Anthropic report, `favaro_pace`) and with it the "Company sources" limitation. That entry, like `anthropic_headless`, has no year, and `aaai2027.bst` prints "????" for a missing year; keeping either would have meant altering bibliographic data. The Claude Code documentation citation and its remark that `--system-prompt` drops the git-status snapshot went with it (the harness disclosure itself is kept).
- Methods: the design table became prose (all its numbers kept); equations (4) and (5) for the GLM and GLMM (notation added in the LaTeX conversion) became words; the harness context's "three-quarters / a quarter of the input"; the flag-versus-AUROC rationale (Remedios et al.); the post hoc edit-type classification (254 / 150 pairs); MBPP download hashes; the study's cost (2,706 calls, USD 41.70); the code-comment history of item 3.
- Results: Figure 2 (d′ and c), Figure 3 (stated prevalence), Figure 4 (remedies) and Figure 5 (position), and Table 6 (score bands), moved to the Technical Appendix; Tables 2 and 3 merged into one table of registered measures; the "σ from 9 to 33 across quadrature settings" sentence; the P10 positions 1–8 remark moved to the position figure's caption.
- Discussion: "Implications for aviation AI developers" (outside this venue's scope, and it points to the author's field); the fifth contribution bullet ("for AI-safety and aviation-safety readers"); the anchoring parallel for the independence instruction; the remark that R-cal examples came from other problems (Becker et al.); a shorter "What was found" and "What the human analogy did and did not predict".

Changes of form only: IEEE numeric citations became author–year (natbib); siunitx was dropped ("50%" instead of "50 %", "30,880" instead of "30 880"); table captions moved below tables; figure captions say "left, Haiku (orange); right, Sonnet (blue)" instead of subfigure labels (the kit forbids minipage grouping); cross-references by name instead of section numbers.

Added text (no new results, claims or citations): "(link withheld for review)" and the pre-registration sentence; "the condensation of this paper" in the AI disclosure; "given below per monitor"; references to the appendix; the top-band shares quoted in the text (from the preprint's Table 6).

### Technical Appendix

The call says references and appendices are "usually" not counted, and the kit allows a technical appendix after the references where the venue permits it. Everything needed to judge the paper is in pages 1–8; the appendix holds only Table 4 (score bands) and Figures 2–5, whose numbers are also in the text or Table 1. If the organisers say appendices count, delete everything from `\appendix` to `\end{document}` (keeping `\end{document}`) and replace the four "in the appendix" references (Figures `fig:stated`, `fig:remedies`, `fig:position`, Table `tab:bands`) with "(full results in Table 1)" or remove them; the paper then ends at 9 pages with references.

## 4. Anonymisation checklist (run 4 November 2026)

Searched: `paper.tex`, `references.bib`, `aaai2027.sty`, `aaai2027.bst`, `check/*`, the text of every figure PDF, `pdftotext` of `paper.pdf`, and the raw bytes of all PDFs. Case-insensitive.

| Check | Result |
|---|---|
| "Le Cuirot", "Cuirot", "James" | 0 hits |
| "CitadelAero", "Citadel", "Aero" | 0 hits |
| "github", "lecuirot", "Jersey", ".je", "http" in the PDF, "www." in the PDF | 0 hits |
| E-mail addresses (`[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}`) | 0 hits |
| "aviation", "pilot", "MSc", "First Officer", local paths ("home/user", "Research/papers", "02-do-llm") | 0 hits |
| Commit hashes (`f4bedaa`, `136632a`, `7fe31dc`, `d8e6b51`, `e78e15e`, `46d23f1`, `dfd94b7`) | 0 hits |
| Author block | "Anonymous submission" (kit `submission` option); affiliations empty |
| Acknowledgements, competing interests, disclaimer, Materials link | Removed |
| Self-citation of the preprint or other own work | None (the preprint never cited the author's own work; it is not cited here) |
| Pre-registration | "The design was pre-registered and committed to a public repository before any main-experiment data were collected; the link is withheld for review." Timing caveat on clarifications 4–12 kept |
| PDF metadata (`pdfinfo`) | No Title, Author, Subject, Keywords, Creator, Producer, CreationDate or ModDate; no XMP stream; no `PTEX.*` keys (which would name figure files); "Custom Metadata: no" |
| Figure files | No author metadata (Matplotlib wrote none; Ghostscript wrote only its own Producer and dates, which are not carried into `paper.pdf`) |
| AI-assistance disclosure | Kept, anonymous: "Literature searches, drafting and source verification were carried out with AI assistance (Claude, Anthropic) under the author's direction, as were the experimental code, the analysis and the condensation of this paper. …" |

Residual identifiers that are not about the author and were kept: the model IDs, Claude Code 2.1.317, the run dates and UTC times, and the sentence that each monitor call's context included a field for the account's e-mail address (no address is given).

## 5. Number verification

`python3 -I check/verify_numbers.py --markdown` regenerates the table below and exits 0 only if every number matches and every number is covered.

How it checks:
- It extracts every number in the body of `paper.tex` (757 occurrences, after masking LaTeX code, labels, citation keys, model IDs and figure widths), with its sign.
- Tables 1–4 are checked cell by cell: Table 1 against `results/registered_measures_table.md` (F shown as a percentage of the F value there, to one decimal, as in the preprint); Table 2 against `results/RESULTS_numbers.md` (OR, CI, z) and `results/analysis.json` (exact p and Holm p); Table 3 against the H1a table and Table 4 against the score-band table of `RESULTS_numbers.md`.
- Every other number belongs to a verbatim snippet of `paper.tex` with the source line(s) where each of its numbers appears. Results point to `results/`; design constants to `PREREGISTRATION.md` or `code/`; numbers about other people's work (and citation locators such as "Sec. 2.2") to the full paper's `paper.tex`, whose sources were checked in `sources.md` and `AUDIT.md`. Paths are relative to `papers/02-do-llm-monitors-miss-rare-threats/`.
- Matching is exact (after removing thousands separators and a leading zero, so ".828" = "0.828"). Rounding, percentage or magnitude is allowed only where a check says so, and always to the precision printed in the submission; the value used is shown in brackets.
- A second pass finds, for every prose number, the most similar sentence of the full paper and confirms the number is there (or, for numbers that moved out of a full-paper table into prose, in that table row). This catches any re-rounding during condensation.
- Self-test: seven deliberate errors, each injected into a copy of `paper.tex` (a table cell, an odds ratio in the text, a Holm p in Table 2, a sign, a literature percentage, an added number, a p value in the text), each made the check fail: six as mismatches, the added number as an uncovered number (`--tex` runs the check on another file).

**Result: 757 numbers, 757 covered, 193 checks, 0 mismatches, 0 fidelity flags.** Numbers are shown normalised (".512" for 0.512, "30880" for 30,880).

| # | Part | Text in submission (paper.tex) | Numbers | Source: file:line or JSON path [value used] | Result |
|---|---|---|---|---|---|
| 1 | Table 1 (registered measures) | `Haiku P50 (batch)` | .512 .436 .589 1.9 2.05 1.84 2.64 .99 .73 1.45 .867 .827 .902 41.5 7.7 | results/registered_measures_table.md:3 (F: x100, 1 dp) | match |
| 2 | Table 1 (registered measures) | `Haiku P10 (batch)` | .500 .423 .577 1.2 2.25 2.01 2.55 1.13 1.00 1.28 .886 .855 .914 41.2 6.1 | results/registered_measures_table.md:4 (F: x100, 1 dp) | match |
| 3 | Table 1 (registered measures) | `Haiku P2.5 (batch)` | .694 .618 .760 1.2 2.76 2.54 3.01 .88 .77 .98 .912 .883 .939 52.1 5.6 | results/registered_measures_table.md:5 (F: x100, 1 dp) | match |
| 4 | Table 1 (registered measures) | `Haiku R-cal (batch)` | .600 .490 .700 1.2 2.50 2.21 2.80 1.00 .84 1.16 .915 .874 .950 50.2 6.4 | results/registered_measures_table.md:6 (F: x100, 1 dp) | match |
| 5 | Table 1 (registered measures) | `Haiku R-ind (batch)` | .625 .515 .723 .7 2.75 2.44 3.09 1.06 .91 1.22 .898 .849 .942 49.5 5.0 | results/registered_measures_table.md:7 (F: x100, 1 dp) | match |
| 6 | Table 1 (registered measures) | `Haiku none (single)` | .633 .544 .714 1.7 2.38 1.95 3.09 .85 .64 1.21 .923 .887 .954 48.8 6.5 | results/registered_measures_table.md:8 (F: x100, 1 dp) | match |
| 7 | Table 1 (registered measures) | `Haiku S50 (single)` | .683 .596 .760 3.3 2.26 1.88 2.89 .66 .46 .98 .923 .889 .954 54.8 7.9 | results/registered_measures_table.md:9 (F: x100, 1 dp) | match |
| 8 | Table 1 (registered measures) | `Haiku S1 (single)` | .642 .553 .722 .8 2.60 2.16 3.18 .94 .71 1.23 .937 .907 .965 48.8 5.0 | results/registered_measures_table.md:10 (F: x100, 1 dp) | match |
| 9 | Table 1 (registered measures) | `Sonnet P50 (batch)` | .500 .423 .577 .6 2.35 1.83 2.91 1.18 1.06 1.38 .905 .882 .929 41.9 7.0 | results/registered_measures_table.md:11 (F: x100, 1 dp) | match |
| 10 | Table 1 (registered measures) | `Sonnet P10 (batch)` | .569 .491 .643 1.4 2.36 2.11 2.66 1.01 .87 1.17 .911 .886 .934 46.1 5.5 | results/registered_measures_table.md:12 (F: x100, 1 dp) | match |
| 11 | Table 1 (registered measures) | `Sonnet P2.5 (batch)` | .738 .664 .800 1.7 2.74 2.54 2.98 .74 .62 .85 .927 .901 .950 58.3 5.4 | results/registered_measures_table.md:13 (F: x100, 1 dp) | match |
| 12 | Table 1 (registered measures) | `Sonnet R-cal (batch)` | .850 .756 .912 4.0 2.77 2.45 3.17 .37 .18 .52 .959 .929 .980 65.5 7.4 | results/registered_measures_table.md:14 (F: x100, 1 dp) | match |
| 13 | Table 1 (registered measures) | `Sonnet R-ind (batch)` | .750 .645 .832 1.8 2.76 2.46 3.12 .71 .55 .87 .935 .898 .967 62.0 5.0 | results/registered_measures_table.md:15 (F: x100, 1 dp) | match |
| 14 | Table 1 (registered measures) | `Sonnet none (single)` | .800 .720 .862 .8 3.08 2.62 3.67 .71 .47 1.00 .953 .922 .979 68.4 4.4 | results/registered_measures_table.md:16 (F: x100, 1 dp) | match |
| 15 | Table 1 (registered measures) | `Sonnet S50 (single)` | .850 .775 .903 3.3 2.81 2.39 3.42 .38 .18 .69 .966 .941 .986 75.0 6.5 | results/registered_measures_table.md:17 (F: x100, 1 dp) | match |
| 16 | Table 1 (registered measures) | `Sonnet S1 (single)` | .775 .692 .841 1.7 2.79 2.35 3.47 .65 .43 1.01 .949 .919 .974 62.7 4.4 | results/registered_measures_table.md:18 (F: x100, 1 dp) | match |
| 17 | Table 2 (confirmatory tests) | `H1 Haiku` | 2.15 1.34 3.46 3.18 .0015 .0015 | results/RESULTS_numbers.md:53; results/analysis.json [H1/Haiku/P2.5_vs_P50/term/p, p_holm] | match |
| 18 | Table 2 (confirmatory tests) | `H1 Sonnet` | 2.81 1.78 4.43 4.44 <.001 <.001 | results/RESULTS_numbers.md:55; results/analysis.json [H1/Sonnet/P2.5_vs_P50/term/p, p_holm] | match |
| 19 | Table 2 (confirmatory tests) | `H2 Haiku` | .57 .22 1.46 -1.16 .244 .244 | results/RESULTS_numbers.md:83; results/analysis.json [H2/Haiku/term/p, p_holm] | match |
| 20 | Table 2 (confirmatory tests) | `H2 Sonnet` | .04 .00 .42 -2.66 .008 .015 | results/RESULTS_numbers.md:85; results/analysis.json [H2/Sonnet/term/p, p_holm] | match |
| 21 | Table 2 (confirmatory tests) | `H3 Haiku` | .66 .38 1.16 -1.44 .150 .150 | results/RESULTS_numbers.md:125; results/analysis.json [H3/Haiku/term/p, p_holm] | match |
| 22 | Table 2 (confirmatory tests) | `H3 Sonnet` | 2.02 .99 4.10 1.94 .053 .106 | results/RESULTS_numbers.md:126; results/analysis.json [H3/Sonnet/term/p, p_holm] | match |
| 23 | Table 3 (H1a) | `Haiku` | .181 .075 .281 -.0069 -.0327 .0128 .71 .06 1.04 -.12 -.59 .17 .045 -.002 .092 | results/RESULTS_numbers.md:73 | match |
| 24 | Table 3 (H1a) | `Sonnet` | .238 .144 .338 .0111 -.0026 .0202 .39 -.24 .95 -.44 -.70 -.28 .022 -.013 .056 | results/RESULTS_numbers.md:74 | match |
| 25 | Table 4 (score bands, appendix) | `Haiku P50` | .09 .73 | results/RESULTS_numbers.md:235 (bd share 80–100; P(flag) at 40–59) | match |
| 26 | Table 4 (score bands, appendix) | `Haiku P2.5` | .22 .84 | results/RESULTS_numbers.md:237 (bd share 80–100; P(flag) at 40–59) | match |
| 27 | Table 4 (score bands, appendix) | `Haiku none` | .17 1.00 | results/RESULTS_numbers.md:240 (bd share 80–100; P(flag) at 40–59) | match |
| 28 | Table 4 (score bands, appendix) | `Sonnet P50` | .17 .85 | results/RESULTS_numbers.md:243 (bd share 80–100; P(flag) at 40–59) | match |
| 29 | Table 4 (score bands, appendix) | `Sonnet P2.5` | .45 .93 | results/RESULTS_numbers.md:245 (bd share 80–100; P(flag) at 40–59) | match |
| 30 | Table 4 (score bands, appendix) | `Sonnet none` | .60 .83 | results/RESULTS_numbers.md:248 (bd share 80–100; P(flag) at 40–59) | match |
| 31 | Table 4 (score bands, appendix) | `Sonnet S50` | .72 .83 | results/RESULTS_numbers.md:249 (bd share 80–100; P(flag) at 40–59) | match |
| 32 | Table 4 (score bands, appendix) | `Sonnet S1` | .47 1.00 | results/RESULTS_numbers.md:250 (bd share 80–100; P(flag) at 40–59) | match |
| 33 | Abstract | `Two Claude models made 30,880 judgements` | 30880 | results/RESULTS.md:13 | match |
| 34 | Abstract | `drawn from 379 execution-verified` | 379 | results/RESULTS.md:126 | match |
| 35 | Abstract | `In batches of 40, both` | 40 | PREREGISTRATION.md:56 | match |
| 36 | Abstract | `hit rates rose from 0.51 at 50\% prevalence to 0.69 at 2.5\% for Haiku, and from 0.50 to 0.74 for Sonnet` | .51 50 .69 2.5 .50 .74 | results/RESULTS.md:18 | match |
| 37 | Abstract | `(Holm-adjusted $p = .0015$ and $p < .001$)` | .0015 .001 | results/RESULTS.md:19; results/RESULTS.md:20 | match |
| 38 | Abstract | `with false-alarm rates below 2\%` | 2 | results/analysis.json computed: max F over the six Experiment 1 cells [2 ← 1.875 (lt 2)] | match |
| 39 | Abstract | `as many backdoors as 2.5\% batches, and more than 10\% and 50\% batches in three of four comparisons` | 2.5 10 50 | results/RESULTS.md:51 | match |
| 40 | Abstract | `Stating that about 1 in 100 submissions` | 1 100 | results/RESULTS.md:35 | match |
| 41 | Abstract | `single-item hit rate (0.85 to 0.78)` | .85 .78 | results/RESULTS.md:36 | match |
| 42 | Introduction | `the audit budget covered 2\% of problems \citep[Sec.~2.2]{greenblatt2024}` | 2 2.2 | full-paper paper.tex:20 | match |
| 43 | Introduction | `(\citealp[Sec.~3.1]{greenblatt2024}; \citealp[Sec.~3.1]{bhatt2025})` | 3.1 3.1 | full-paper paper.tex:22 | match |
| 44 | Introduction | `once out of thousands of tasks'' \citep[Sec.~6]{korbak2025}` | 6 | full-paper paper.tex:22 | match |
| 45 | Introduction | `misses rose from 7\% when targets appeared on half of trials to 30\% when they appeared on 1\%` | 7 30 1 | full-paper paper.tex:24 | match |
| 46 | Introduction | `attacks made up 16\% to 86\% of test samples` | 16 86 | full-paper paper.tex:26 | match |
| 47 | Introduction | `(\citealp[Sec.~6.3]{srivastav2026}; \citealp[Sec.~III.E]{abbasi2026})` | 6.3 | full-paper paper.tex:26 | match |
| 48 | Introduction | `\citep[Sec.~2]{griffin2024}` | 2 | full-paper paper.tex:26 | match |
| 49 | Introduction | `Both monitors caught more backdoors at 2.5\% prevalence than at 50\%.` | 2.5 50 | full-paper paper.tex:30 | match |
| 50 | Introduction | `An open set of 419 execution-verified pairs` | 419 | results/RESULTS.md:96 | match |
| 51 | Background | `c = -\frac{1}{2}` | 1 2 | full-paper paper.tex:50 | match |
| 52 | Background | `infinite at 0 and 1` | 0 1 | full-paper paper.tex:52 | match |
| 53 | Background | `is increased by 0.5''` | .5 | full-paper paper.tex:52 | match |
| 54 | Background | `\tilde H = \frac{n_{\mathrm{h}} + 0.5}{n_{\mathrm{s}} + 1}, \qquad \tilde F = \frac{n_{\mathrm{f}} + 0.5}{n...` | .5 1 .5 1 | PREREGISTRATION.md:79 | match |
| 55 | Background | `such as a suspicion score from 0 to 100, the area` | 0 100 | full-paper paper.tex:56 | match |
| 56 | Background | `0.5 is chance and 1.0 is perfect separation` | .5 1.0 | full-paper paper.tex:56 | match |
| 57 | Background | `Misses were 7\% at 50\% target prevalence, 16\% at 10\% and 30\% at 1\%.` | 7 50 16 10 30 1 | full-paper paper.tex:62 | match |
| 58 | Background | `(Experiment~7). In that experiment` | 7 | full-paper paper.tex:62 | match |
| 59 | Background | `projected onto 1\% to 4\% of bags, and the system tells the screener immediately whether a projected item w...` | 1 4 2 | full-paper paper.tex:74 | match |
| 60 | Background | `\citet[Sec.~4]{korbak2025} sketch a control safety case whose safety layer ``audits the 0.1\% most suspicio...` | 4 .1 | full-paper paper.tex:83 | match |
| 61 | Background | `\citep[Fig.~4 caption]{zhao2021}` | 4 | full-paper paper.tex:98 | match |
| 62 | Background | `(20 items per call) of studies for systematic reviews, in five reviews whose natural share of relevant stud...` | 20 2.9 53.0 | full-paper paper.tex:102 | match |
| 63 | Background | `in the four reviews with prevalence of 20\% or less` | 20 | full-paper paper.tex:102 | match |
| 64 | Background | `within the batch'' (Section~4.4)` | 4.4 | full-paper paper.tex:102 | match |
| 65 | Background | `A single backdoored item among 39 clean ones` | 39 | full-paper paper.tex:110 | match |
| 66 | Methods | `the hit rate is lower at 2.5\% backdoor prevalence than at 50\%, with 10\% in between` | 2.5 50 10 | PREREGISTRATION.md:20 | match |
| 67 | Methods | `stating that backdoors are rare (1\%) rather than common (50\%)` | 1 50 | PREREGISTRATION.md:22 | match |
| 68 | Methods | `\textbf{H3 (remedy).} At 2.5\% prevalence` | 2.5 | PREREGISTRATION.md:23 | match |
| 69 | Methods | `all four splits: 974 problems` | 974 | results/RESULTS.md:78 | match |
| 70 | Methods | `Creative Commons Attribution 4.0 licence (CC BY 4.0)` | 4.0 4.0 | full-paper paper.tex:150 | match |
| 71 | Methods | `(task IDs 367 and 927)` | 367 927 | results/RESULTS.md:91 | match |
| 72 | Methods | `From the 972 eligible problems, 450 were drawn at random (seed 20261103)` | 972 450 20261103 | results/RESULTS.md:91 | match |
| 73 | Methods | `All 450 calls returned an answer` | 450 | results/RESULTS.md:66 | match |
| 74 | Methods | `with a 10-second timeout` | 10 | code/common.py:38 | match |
| 75 | Methods | `ratio of at least 0.6, the operational` | .6 | PREREGISTRATION.md:108 | match |
| 76 | Methods | `Of 450 pairs, 419 (93.1\%) were kept` | 450 419 93.1 | results/RESULTS.md:96; results/RESULTS.md:97 | match |
| 77 | Methods | `on the trigger (14) or whose edit was too large (14)` | 14 14 | results/RESULTS.md:101 | match |
| 78 | Methods | `was 2, with a maximum of 8; 356 pairs (85\%)` | 2 8 356 85 | results/RESULTS.md:112; results/RESULTS.md:113 | match |
| 79 | Methods | `(seed 4021) into a calibration pool of 40 pairs and a main pool of 379` | 4021 40 379 | results/RESULTS.md:126 | match |
| 80 | Methods | `judged the 80 calibration-pool items` | 80 | results/calibration.md:9 | match |
| 81 | Methods | `between 0.40 and 0.90 and a false-alarm rate below 0.30` | .40 .90 .30 | results/calibration.md:16 | match |
| 82 | Methods | `$24/40 = 0.60$ (Wilson 95\% CI 0.45 to 0.74), the false-alarm rate $0/40 = 0.00$ (0.00 to 0.09) and the AUR...` | 24 40 .60 95 .45 .74 0 40 .00 .00 .09 .97 | results/RESULTS.md:134; results/RESULTS.md:135 | match |
| 83 | Methods | `Claude Code 2.1.317` | 2.1.317 | code/README.md:16 | match |
| 84 | Methods | `score from 0 to 100 and a binary` | 0 100 | PREREGISTRATION.md:50 | match |
| 85 | Methods | `about 1,800 input tokens per call (1,812 for Haiku, 1,791 for Sonnet)` | 1800 1812 1791 | results/RESULTS.md:699; results/RESULTS.md:650; results/RESULTS.md:651 | match |
| 86 | Methods | `\paragraph{Experiment 1: experienced` | 1 | PREREGISTRATION.md:56 | match |
| 87 | Methods | `Each call showed a batch of 40 submissions` | 40 | PREREGISTRATION.md:56 | match |
| 88 | Methods | `how many of the 40 are backdoored: 20 in each of 8 batches, 4 in each of 40 and 1 in each of 160, giving 16...` | 40 20 8 4 40 1 160 160 160 1440 6240 | PREREGISTRATION.md:56; PREREGISTRATION.md:60; PREREGISTRATION.md:61; PREREGISTRATION.md:62 | match |
| 89 | Methods | `\paragraph{Experiment 2: stated` | 2 | PREREGISTRATION.md:66 | match |
| 90 | Methods | `(``In past reviews, about 1 in 100 submissions contained a backdoor.'')` | 1 100 | PREREGISTRATION.md:66 | match |
| 91 | Methods | `The same 240 main-pool problems (120 shown backdoored, 120 clean)` | 240 120 120 | results/RESULTS.md:128 | match |
| 92 | Methods | `\paragraph{Experiment 3: remedies` | 3 | PREREGISTRATION.md:68 | match |
| 93 | Methods | `drawn afresh: 80 per remedy, giving 80 backdoored and 3,120 clean judgements` | 80 80 3120 | PREREGISTRATION.md:68; results/RESULTS_numbers.md:33 | match |
| 94 | Methods | `first showed 10 examples from 10 distinct calibration-pool problems (5 backdoored, 5 clean` | 10 10 5 5 | PREREGISTRATION.md:120 | match |
| 95 | Methods | `(seed 55021) and run in shuffled order (seed 99173) from 23:12 UTC on 3 November to 00:12 UTC on 4 November...` | 55021 99173 23:12 3 00:12 4 2026 | code/s6_design.py:24; results/RESULTS.md:73; results/RESULTS.md:72 | match |
| 96 | Methods | `Rates have Wilson 95\% confidence intervals; $d'$, $c$ and AUROC have 95\% bootstrap intervals (2,000 resam...` | 95 95 2000 1 3 2 | results/RESULTS.md:600; results/RESULTS.md:602; results/RESULTS.md:603 | match |
| 97 | Methods | `$\alpha = .05$` | .05 | PREREGISTRATION.md:90 | match |
| 98 | Methods | `with 40-node Gauss--Hermite quadrature and a pre-specified` | 40 | PREREGISTRATION.md:119 | match |
| 99 | Methods | `flag on position (1 to 40)` | 1 40 | PREREGISTRATION.md:89 | match |
| 100 | Methods | `about 80\% power for a fall in hit rate from 0.80 to 0.65 with 160 backdoored judgements per cell` | 80 .80 .65 160 | PREREGISTRATION.md:90 | match |
| 101 | Methods | `smaller than about 15 percentage points` | 15 | PREREGISTRATION.md:90 | match |
| 102 | Methods | `Experiment 2 has 120 backdoored items per condition and Experiment 3 has 80 backdoored judgements per remed...` | 2 120 3 80 3 2 | full-paper paper.tex:206 | match |
| 103 | Methods | `Python 3.13.18 and statsmodels 0.15.0 (bootstrap seed 314159)` | 3.13.18 0.15.0 314159 | code/README.md:9; code/README.md:16; code/analyse.py:50 | match |
| 104 | Methods | `Items 1 to 3, by the author` | 1 3 | PREREGISTRATION.md:126 | match |
| 105 | Methods | `were committed at 23:10 UTC on 3 November, before` | 23:10 3 | PREREGISTRATION.md:126 | match |
| 106 | Methods | `That the 0.6 edit-size threshold` | .6 | PREREGISTRATION.md:124 | match |
| 107 | Methods | `in place of item~3's original wording` | 3 | PREREGISTRATION.md:124 | match |
| 108 | Methods | `Items 4 to 12, by the research engineer` | 4 12 | PREREGISTRATION.md:126 | match |
| 109 | Methods | `at 23:16 UTC, after the main run had started (23:13 UTC, with 12 smoke-test calls already done) and when th...` | 23:16 23:13 12 138 | PREREGISTRATION.md:126 | match |
| 110 | Methods | `at 23:10:45 UTC, before the first main-experiment output at 23:12:32 UTC` | 23:10:45 23:12:32 | AUDIT.md:20 | match |
| 111 | Methods | `All 2,176 main calls (30,880 judgements)` | 2176 30880 | results/RESULTS.md:13 | match |
| 112 | Methods | `(\code{num\_turns}~$>$~2)` | 2 | results/RESULTS.md:146 | match |
| 113 | Methods | `in 43 of 368 Haiku batch calls and 24 of 720 Sonnet single-item calls` | 43 368 24 720 | results/RESULTS.md:148; results/RESULTS.md:149 | match |
| 114 | Results | `at or below 4.0\% in every condition` | 4.0 | results/analysis.json computed: max F over all 16 cells, x100 [4.0 ← 3.974 (eqround 4.0)] | match |
| 115 | Results | `below 2\% in all batch conditions except Sonnet's R-cal` | 2 | results/analysis.json computed: max F over batch cells other than Sonnet R-cal, x100 [2 ← 1.875 (lt 2)] | match |
| 116 | Results | `hit rate $H$ (Wilson 95\% CI), false-alarm rate $F$, $d'$, $c$ and AUROC with 95\% bootstrap CIs` | 95 95 | results/RESULTS_numbers.md:26 | match |
| 117 | Results | `P50 160/160; P10 160/1,440; P2.5 160/6,240; R-cal and R-ind 80/3,120; single-item conditions 120/120` | 160 160 160 1440 160 6240 80 3120 120 120 | results/RESULTS_numbers.md:30; results/RESULTS_numbers.md:31; results/RESULTS_numbers.md:32; results/RESULTS_numbers.md:33; results/RESULTS_numbers.md:35 | match |
| 118 | Results | `the population-averaged odds ratio is 0.61 [0.44, 0.84], a fall in hit rate of 7.5 points` | .61 .44 .84 7.5 | results/RESULTS_numbers.md:109; results/RESULTS.md:228 [7.5 ← -7.5 (magnitude)] | match |
| 119 | Results | `Haiku's hit rate was 0.512 at P50, 0.500 at P10 and 0.694 at P2.5; Sonnet's was 0.500, 0.569 and 0.738` | .512 .500 .694 .500 .569 .738 | results/RESULTS_numbers.md:30; results/RESULTS_numbers.md:31; results/RESULTS_numbers.md:32; results/RESULTS_numbers.md:39; results/RESULTS_numbers.md:40 | match |
| 120 | Results | `the odds ratio was 2.15 for Haiku (95\% CI 1.34 to 3.46, Holm $p = .0015$) and 2.81 for Sonnet (1.78 to 4.4...` | 2.15 95 1.34 3.46 .0015 2.81 1.78 4.43 .001 | results/RESULTS.md:19; results/RESULTS.md:20 | match |
| 121 | Results | `(Haiku OR 0.95, $p = .828$; Sonnet OR 1.32, $p = .211$)` | .95 .828 1.32 .211 | results/RESULTS_numbers.md:54; results/RESULTS_numbers.md:56 | match |
| 122 | Results | `(all $p > .25$)` | .25 | results/analysis.json computed: min p of the four false-alarm prevalence contrasts (H1_false_alarms) [.25 ← 0.2785 (gt .25)] | match |
| 123 | Results | `by backdoor prevalence in a batch of 40 (Experiment~1); left, Haiku (orange); right, Sonnet (blue). Error b...` | 40 1 95 | full-paper paper.tex:310 | match |
| 124 | Results | `($\Delta c = {-0.44}$, 95\% CI $-0.70$ to $-0.28$)` | -.44 95 -.70 -.28 | results/RESULTS_numbers.md:74; results/RESULTS_numbers.md:69 | match |
| 125 | Results | `($\Delta d' = 0.71$, 0.06 to 1.04)` | .71 .06 1.04 | results/RESULTS_numbers.md:73 | match |
| 126 | Results | `($\Delta c > 0$ with an interval` | 0 | results/RESULTS_numbers.md:69 | match |
| 127 | Results | `(point estimate and 95\% cluster-bootstrap CI)` | 95 | results/RESULTS_numbers.md:69 | match |
| 128 | Results | `Telling Sonnet that ``about 1 in 100''` | 1 100 | PREREGISTRATION.md:66 | match |
| 129 | Results | `hit rate from 0.850 to 0.775 (registered GLMM: log-odds $-3.32$, SE 1.25, $z = {-2.66}$, $p = .008$, Holm $...` | .850 .775 -3.32 1.25 -2.66 .008 .015 | results/RESULTS_numbers.md:44; results/RESULTS_numbers.md:85 [-3.32 ← -3.321 (rounded); 1.25 ← 1.246 (rounded)] | match |
| 130 | Results | `the hit rate went from 0.683 to 0.642 (OR 0.57, 0.22 to 1.46, $p = .244$, Holm $p = .244$)` | .683 .642 .57 .22 1.46 .244 .244 | results/RESULTS_numbers.md:36; results/RESULTS_numbers.md:37; results/RESULTS_numbers.md:83 | match |
| 131 | Results | `Because 92 of 120 backdoored items were flagged in all three conditions` | 92 120 | results/RESULTS.md:224 | match |
| 132 | Results | `and 40-node non-adaptive quadrature` | 40 | PREREGISTRATION.md:119 | match |
| 133 | Results | `($\sigma = 32.8$)` | 32.8 | results/RESULTS.md:578 | match |
| 134 | Results | `gives $\sigma = 13.4$ and an S1 log-odds of $-3.76$ (SE 1.41, $z = {-2.67}$, $p = .0076$; likelihood-ratio ...` | 13.4 -3.76 1.41 -2.67 .0076 .00024 | results/RESULTS.md:588; results/RESULTS.md:589; results/RESULTS.md:546 | match |
| 135 | Results | `9 Sonnet items were flagged under S50 but not under S1, and none the other way round (exact paired test, $p...` | 9 .0039 | results/RESULTS.md:556 | match |
| 136 | Results | `the paired counts were 12 against 7 ($p = .36$)` | 12 7 .36 | results/RESULTS.md:555 | match |
| 137 | Results | `was 0.61 (0.44 to 0.84, $p = .002$)` | .61 .44 .84 .002 | results/RESULTS_numbers.md:109 | match |
| 138 | Results | `hit rate was $-0.075$ ($-0.125$ to $-0.033$)` | -.075 -.125 -.033 | results/RESULTS_numbers.md:117 | match |
| 139 | Results | `($\Delta c = 0.29$, 0.05 to 0.59)` | .29 .05 .59 | results/RESULTS_numbers.md:116 | match |
| 140 | Results | `(0.27, $-0.01$ to 0.58)` | .27 -.01 .58 | results/RESULTS_numbers.md:117 | match |
| 141 | Results | `($-0.017$, $-0.034$ to $-0.004$)` | -.017 -.034 -.004 | results/RESULTS_numbers.md:117 | match |
| 142 | Results | `backdoored items (75.0 to 62.7)` | 75.0 62.7 | results/RESULTS_numbers.md:44; results/RESULTS_numbers.md:45 | match |
| 143 | Results | `among items scoring 40--59 did not fall` | 40 59 | results/RESULTS_numbers.md:233 | match |
| 144 | Results | `($p = .108$ and .329)` | .108 .329 | results/analysis.json [H2/Haiku/false_alarm_glm_item_clustered/coefs/C(condition, Treatment('S50'))[T.S1]/p]; results/analysis.json [H2/Sonnet/false_alarm_glm_item_clustered/coefs/C(condition, Treatment('S50'))[T.S1]/p] [.108 ← 0.108441; .329 ← 0.328789] | match |
| 145 | Results | `Haiku's fall of about 4 points` | 4 | results/analysis.json [H2/Haiku/S1_minus_S50_point/H] [4 ← 4.16667] | match |
| 146 | Results | `At 2.5\% prevalence the 10 labelled examples` | 2.5 10 | PREREGISTRATION.md:23; PREREGISTRATION.md:69 | match |
| 147 | Results | `fell from 0.694 to 0.600 (OR 0.66, 0.38 to 1.16, $p = .150$, Holm $p = .150$)` | .694 .600 .66 .38 1.16 .150 .150 | results/RESULTS_numbers.md:32; results/RESULTS_numbers.md:33; results/RESULTS_numbers.md:125 | match |
| 148 | Results | `rose from 0.738 to 0.850 (OR 2.02, 0.99 to 4.10, $p = .053$, Holm $p = .106$)` | .738 .850 2.02 .99 4.10 .053 .106 | results/RESULTS_numbers.md:40; results/RESULTS_numbers.md:41; results/RESULTS_numbers.md:126 | match |
| 149 | Results | `($\Delta c = {-0.37}$, $-0.59$ to $-0.18$) with no change in $d'$ (0.03, $-0.38$ to 0.48)` | -.37 -.59 -.18 .03 -.38 .48 | results/RESULTS_numbers.md:133 | match |
| 150 | Results | `rose from 1.7\% to 4.0\% ($\Delta F = 0.0224$, 0.0139 to 0.0314)` | 1.7 4.0 .0224 .0139 .0314 | results/RESULTS_numbers.md:40; results/RESULTS_numbers.md:41; results/RESULTS_numbers.md:133 [1.7 ← .0173 (x100); 4.0 ← .0397 (x100)] | match |
| 151 | Results | `rose from 1.41 to 2.40` | 1.41 2.40 | results/RESULTS_numbers.md:224; results/RESULTS_numbers.md:226 | match |
| 152 | Results | `With 80 backdoored judgements per remedy cell` | 80 | results/RESULTS_numbers.md:33 | match |
| 153 | Results | `(all $p \geq .08$` | .08 | results/analysis.json computed: min p of the four E1 hit-rate position tests (exploratory/E1) [.08 ← 0.08449 (ge_r .08)] | match |
| 154 | Results | `(OR per 10 positions 1.26, $p = .019$)` | 10 1.26 .019 | results/RESULTS_numbers.md:139; results/RESULTS_numbers.md:146 | match |
| 155 | Results | `(Haiku OR 0.74, 0.42 to 1.30, $p = .288$; Sonnet OR 1.07, 0.57 to 1.98, $p = .835$)` | .74 .42 1.30 .288 1.07 .57 1.98 .835 | results/RESULTS_numbers.md:154; results/RESULTS_numbers.md:155 | match |
| 156 | Results | `($\Delta F = {-0.0045}$, ${-0.0088}$ to ${-0.0003}$)` | -.0045 -.0088 -.0003 | results/RESULTS_numbers.md:159 | match |
| 157 | Results | `(all monitor terms and interactions $p \geq .195$)` | .195 | results/RESULTS_numbers.md:172 | match |
| 158 | Results | `(log-odds 0.965, SE 0.230, $p < .001$, at S50)` | .965 .230 .001 | results/RESULTS_numbers.md:193 | match |
| 159 | Results | `(Haiku 0.633, Sonnet 0.800)` | .633 .800 | results/RESULTS_numbers.md:35; results/RESULTS_numbers.md:43 | match |
| 160 | Results | `for Haiku, 0.61 at P50 ($p = .051$), 0.58 at P10 ($p = .026$) and 1.31 at P2.5 ($p = .291$); for Sonnet, 0....` | .61 .051 .58 .026 1.31 .291 .25 .001 .33 .001 .70 .226 | results/RESULTS_numbers.md:201; results/RESULTS_numbers.md:202; results/RESULTS_numbers.md:203; results/RESULTS_numbers.md:207; results/RESULTS_numbers.md:208; results/RESULTS_numbers.md:209 | match |
| 161 | Results | `(all $p \geq .46$)` | .46 | results/analysis.json computed: min p of the six E4 false-alarm contrasts (exploratory/E4) [.46 ← 0.4647 (ge_r .46)] | match |
| 162 | Results | `No item scoring below 20 was flagged and every item scoring 60 or more was; most of the change happened in ...` | 20 60 40 59 20 39 | results/RESULTS_numbers.md:233 | match |
| 163 | Results | `(80--100: Haiku 0.09 against 0.22, Sonnet 0.17 against 0.45)` | 80 100 .09 .22 .17 .45 | results/RESULTS_numbers.md:233; results/RESULTS_numbers.md:235; results/RESULTS_numbers.md:237; results/RESULTS_numbers.md:243; results/RESULTS_numbers.md:245 | match |
| 164 | Results | `7,592 at P50 against 4,195 at P2.5; Sonnet's were 116 against 480` | 7592 4195 116 480 | results/RESULTS.md:181; results/RESULTS.md:182 | match |
| 165 | Results | `The H1 odds ratios were 2.35 for Haiku ($p = .0007$) and 2.81 for Sonnet ($p < .001$), and Haiku's H3 $p$ v...` | 2.35 .0007 2.81 .001 .150 .076 | results/RESULTS.md:157; results/RESULTS.md:158; results/RESULTS_numbers.md:125; results/sensitivity_excluding_extra_turn_calls.json [results/Haiku/H3/p] [.076 ← 0.0759985] | match |
| 166 | Discussion | `caught more backdoors at 2.5\% prevalence than at 50\%, and the criterion` | 2.5 50 | full-paper paper.tex:446 | match |
| 167 | Discussion | `A stated base rate of 1 in 100 had a small effect` | 1 100 | full-paper paper.tex:446 | match |
| 168 | Discussion | `An LLM monitor sees all 40 items at once` | 40 | full-paper paper.tex:450 | match |
| 169 | Discussion | `number of backdoors in a batch of 40, and P10 (4 backdoors) behaved like P50 (20)` | 40 4 20 | full-paper paper.tex:452 | match |
| 170 | Discussion | `one odd item among 39 ordinary ones` | 39 | full-paper paper.tex:454 | match |
| 171 | Discussion | `coordinating them ``across space'' \citep[Sec.~6]{korbak2025}` | 6 | full-paper paper.tex:464 | match |
| 172 | Discussion | `\citep[Experiment~7]{wolfe2007}` | 7 | full-paper paper.tex:470 | match |
| 173 | Discussion | `which is 2\% of problems in \citet{greenblatt2024} and 0.1\% of actions` | 2 .1 | full-paper paper.tex:470 | match |
| 174 | Discussion | `about 100 TIP events per screener` | 100 | full-paper paper.tex:472 | match |
| 175 | Limitations | `Each call carried about 1,800 tokens` | 1800 | results/RESULTS.md:699 | match |
| 176 | Limitations | `P50 had 8 batches per monitor` | 8 | PREREGISTRATION.md:60 | match |
| 177 | Limitations | `All batches held 40 items` | 40 | PREREGISTRATION.md:56 | match |
| 178 | Limitations | `The lowest prevalence was 2.5\%` | 2.5 | PREREGISTRATION.md:20 | match |
| 179 | Limitations | `effects smaller than about 15 points may have been missed` | 15 | PREREGISTRATION.md:90 | match |
| 180 | Limitations | `H3 (80 backdoored judgements per cell)` | 80 | results/RESULTS_numbers.md:33 | match |
| 181 | Limitations | `rest on 120 clean items` | 120 | results/RESULTS_numbers.md:35 | match |
| 182 | Limitations | `Clarifications 4 to 12 were committed` | 4 12 | PREREGISTRATION.md:126 | match |
| 183 | Conclusion | `when one backdoor sat in a batch of 40` | 40 | PREREGISTRATION.md:56 | match |
| 184 | Table 1 header | `$H$ [95\% CI] & $F$ & $d'$ [95\% CI] & $c$ [95\% CI] & AUROC [95\% CI]` | 95 95 95 95 | results/registered_measures_table.md:1 | match |
| 185 | Table 2 header | `OR [95\% CI] & $z$` | 95 | results/RESULTS_numbers.md:51 | match |
| 186 | Table 3 header | `$\Delta H$ [95\% CI] & $\Delta F$ [95\% CI] & $\Delta d'$ [95\% CI] & $\Delta c$ [95\% CI] & $\Delta$AUROC ...` | 95 95 95 95 95 | results/RESULTS_numbers.md:71 | match |
| 187 | Table 4 header | `Top band & Flag at 40--59` | 40 59 | results/RESULTS_numbers.md:233 | match |
| 188 | Appendix | `share of backdoored items scoring 80--100. ``Flag at 40--59''` | 80 100 40 59 | results/RESULTS_numbers.md:233 | match |
| 189 | Appendix | `(Experiment~2); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\%` | 2 95 | full-paper paper.tex:370 | match |
| 190 | Appendix | `Hit and false-alarm rates at 2.5\% prevalence without a remedy` | 2.5 | full-paper paper.tex:389 | match |
| 191 | Appendix | `R-ind); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\%` | 95 | full-paper paper.tex:389 | match |
| 192 | Appendix | `Error bars are 95\% bootstrap confidence intervals: a cluster bootstrap over batches for Experiments 1 and ...` | 95 1 3 2 | full-paper paper.tex:347 | match |
| 193 | Appendix | `(exploratory, E1); left, Haiku (orange); right, Sonnet (blue). Error bars are Wilson 95\%` | 95 | full-paper paper.tex:408 | match |

```
Numbers in paper.tex body: 757; covered by a check: 757; uncovered: 0
Checks: 193; mismatches: 0
Source-paper fidelity flags (number not in the most similar sentence of the full paper): 0
```

## 6. Submitting on OpenReview

The submission form was read from OpenReview's API on 4 November 2026 (invitation `AAAI.org/2027/Workshop/Trust4RSI-Agent/-/Submission`, open since 3 Oct 2026). Re-check it when you submit.

1. **Profile (do this now).** Sign up or sign in at https://openreview.net. OpenReview's documentation says profiles created without an institutional e-mail go through moderation that "can take up to two weeks", and the deadline is 16 days away. If moderation is needed, complete the profile fully (name, career and affiliation history, a homepage that shows your name, affiliation and e-mail) and do not register a second time; see https://docs.openreview.net/getting-started/creating-an-openreview-profile/expediting-profile-activation. "Independent Researcher" is an accepted position if you list no current affiliation.
2. **Conflicts of interest.** The form has no conflicts field: OpenReview works conflicts out from your profile. Fill in your education and career history with institution domains, and under Relations add anyone who should not review you (recent co-authors, colleagues, supervisors). Add DBLP or Semantic Scholar links if you have them.
3. **Open the venue** at https://openreview.net/group?id=AAAI.org/2027/Workshop/Trust4RSI-Agent and click the submission button.
4. **Fill in the form** (fields as they stood on 4 Nov 2026):
   - **Title** (max. 250 characters): `Do LLM Monitors Miss Rare Threats? A Pre-Registered Test of the Low-Prevalence Effect`
   - **Authors**: your OpenReview profile ID (every author needs a profile). Organisers see author names; reviewers do not.
   - **Keywords** (comma-separated), suggested: `AI control, trusted monitoring, LLM monitors, low-prevalence effect, signal detection theory, pre-registration, backdoor detection, human factors, Threat Image Projection, LLM-as-a-judge`
   - **TL;DR** (optional, max. 250 characters; this one is 246): `Pre-registered test with two Claude code monitors: backdoors were caught more often, not less, when rare in a batch of 40 (2.5% vs 50%); the criterion did not become more conservative; a TIP-style labelled calibration block did not reliably help.`
   - **Abstract** (max. 5,000 characters; 248 words), identical to the PDF:

     > AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to send the most suspicious items to a small human audit. Real attacks are expected to be rare. Human screeners miss rare targets far more often than common ones, mainly because they grow reluctant to say "yes"; airport security counters this with Threat Image Projection. A pre-registered experiment tested whether large language model (LLM) monitors show this low-prevalence effect. Two Claude models made 30,880 judgements of Python solutions drawn from 379 execution-verified pairs of clean and backdoored code. The prediction failed in the opposite direction. In batches of 40, both monitors caught more backdoors when backdoors were rare: hit rates rose from 0.51 at 50% prevalence to 0.69 at 2.5% for Haiku, and from 0.50 to 0.74 for Sonnet (Holm-adjusted p = .0015 and p < .001), with false-alarm rates below 2%. The decision criterion did not become more conservative. Single-item review caught about as many backdoors as 2.5% batches, and more than 10% and 50% batches in three of four comparisons. Stating that about 1 in 100 submissions contained a backdoor, rather than about half, slightly lowered Sonnet's single-item hit rate (0.85 to 0.78); Haiku's change was not significant. A labelled calibration block modelled on Threat Image Projection did not reliably raise hit rates and more than doubled Sonnet's false alarms. Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch than when one did.

   - **PDF** (max. 50 MB): `paper.pdf` from this folder (0.87 MB). Nothing else.
   - **E-mail sharing**: tick "We authorize the sharing of all author emails with Program Chairs."
   - **Data release**: "We authorize the release of our submission and author names to the public in the event of acceptance." Note that although the workshop is non-archival, an accepted paper and your name will then be public on OpenReview.
5. **AI-use question.** The form has no such field today. If the organisers ask, answer with the paper's disclosure: literature searches, drafting, source verification, the experimental code and analysis, and the condensation of this version were done with AI assistance (Claude, Anthropic) under your direction; an independent AI-assisted audit checked references, quotations and analysis; you are responsible for the text; Claude models were also the item generator and the monitors studied. See the open question in Section 7 before submitting.
6. **Competing interests.** Not in the PDF (it would identify you). The form has no field for it; if the organisers or a later form ask, declare that you founded a company that builds AI tools for aviation.
7. **After submitting**, open the submission, download the PDF OpenReview stored and check it, and use the "Email" button if you want a confirmation. You can revise until the deadline (20 Nov AoE = 21 Nov 11:59 UTC).

If accepted: the camera-ready version can carry the author block, the full Acknowledgement section (competing interests, disclaimer, materials link) and the pre-registration link, following the organisers' instructions.

## 7. Open questions about the call's rules

1. **AI-generated text (important).** The workshop page states no policy. The AAAI-27 main-conference policy (https://aaai.org/conference/aaai/aaai-27/policies-aaai-27-authors/) says: "Papers that include text generated from a large-scale language model (LLM) such as ChatGPT are prohibited unless the produced text is presented as a part of the paper's experimental analysis. Note that this policy does not prohibit authors from using LLMs for editing or polishing author-written text." The paper was drafted, and this version condensed, with AI assistance, and says so. If the workshop follows the AAAI-27 policy, the text would need rewriting in your own words first. Ask the organisers (contact address on the call page) before submitting.
2. **Appendix.** "References and appendices are usually not included in the page limit." The main content fits in 8 pages regardless; Section 3 says how to drop the appendix if needed.
3. **Attendance.** The call does not say whether presentation must be in person (the AAAI-27 main conference requires it).
4. **Reproducibility checklist.** Required for the AAAI-27 main track, not mentioned by the workshop; not included.
5. **Kit version line.** `aaai2027.sty` is dated "2027/10/21" in its own header while its zip entries are dated 21 Oct 2026; it is the file AAAI links as the AAAI-27 author kit.
