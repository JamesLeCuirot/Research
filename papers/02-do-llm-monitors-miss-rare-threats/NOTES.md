# Author notes: Do LLM Monitors Miss Rare Threats?

*Working notes for the author: review points, open questions, development ideas and the revision log. The reader-facing summary is [`README.md`](README.md).*

*A Pre-registered Test of the Low-Prevalence Effect* (paper 02; working title was "Rare Threats Are Missed Threats")

**James Le Cuirot** · CitadelAero · Working draft v0.4, 4 November 2026. Not peer reviewed.

## Abstract

AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to send the most suspicious items to a small human audit. Real attacks are expected to be rare. Human screeners miss rare targets far more often than common ones, mainly because they grow reluctant to say "yes"; airport security counters this with Threat Image Projection. A pre-registered experiment tested whether large language model (LLM) monitors show this low-prevalence effect. Two Claude models made 30,880 judgements of Python solutions drawn from 379 execution-verified pairs of clean and backdoored code. The prediction failed in the opposite direction. In batches of 40, both monitors caught more backdoors when backdoors were rare: hit rates rose from 0.51 at 50% prevalence to 0.69 at 2.5% for Haiku, and from 0.50 to 0.74 for Sonnet (Holm-adjusted p = .0015 and p < .001), with false-alarm rates below 2%. The decision criterion did not become more conservative. Single-item review caught about as many backdoors as 2.5% batches, and more than 10% and 50% batches in three of four comparisons. Stating that about 1 in 100 submissions contained a backdoor, rather than about half, slightly lowered Sonnet's single-item hit rate (0.85 to 0.78); Haiku's change was not significant. A labelled calibration block modelled on Threat Image Projection did not reliably raise hit rates and more than doubled Sonnet's false alarms. Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch than when one did.

## Results at a glance

| Hypothesis | Outcome |
|---|---|
| H1: fewer hits at 2.5% than 50% prevalence (batch) | **Disconfirmed, opposite direction** in both monitors (OR 2.15 Haiku, Holm p = .0015; 2.81 Sonnet, Holm p < .001). P10 behaved like P50 |
| H1a: the effect is a conservative criterion shift | **Not supported.** Sonnet's criterion became more liberal; Haiku's *d′* rose |
| H2: stating "1 in 100" lowers single-item hits | **Supported for Sonnet only**, small (−7.5 points). The registered GLMM is numerically unreliable for Sonnet, but an accurate post hoc refit (p = .0076) and an exact paired test (9 vs 0 items, p = .0039) agree. Haiku: 12 vs 7, p = .36 |
| H3: labelled calibration block raises hits at 2.5% | **Not supported.** It raised Sonnet's false alarms from 1.7% to 4.0%. Low power (80 judgements per cell) |
| E1–E4 (exploratory) | No linear position effect; independence instruction no effect; single items caught more than P50 and P10 batches in three of four comparisons (Haiku at P50: p = .051) |
| Interpretation | Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch; pop-out of a lone backdoor and crowding by several cannot be told apart |

## Status

| Part | State |
|---|---|
| Pre-registration and §9 clarifications | Done; timing of item 3 and items 4–12 disclosed in the paper (Section 5.8) |
| Experiment, analysis, figures, post hoc audit checks | Done (engineer); `results/RESULTS.md`, including §10 |
| Independent audit | Done; `AUDIT.md` (0 major, 6 moderate, 19 minor, 2 suggestions) |
| Paper | **Working draft v0.4**: the v0.3 text (all audit and second-round fixes applied) converted to the LaTeX house style with IEEE numeric references. About 7,650 words of prose (about 8,550 with tables and captions), 6 tables, 5 figures, 40 references (38 in v0.3, plus the arXiv versions of two Anthropic posts added under decision A6) |
| Built | `paper.pdf` (23 pages) built from `paper.tex` and `references.bib` with `papers/_build/build.sh`; `paper.bbl` kept for arXiv. Prose is above the house guide of 7,000 words; trim to the target venue's limit. |

## What James should check

1. **Length.** Prose is about 7,650 words, which is still above the 7,500 target the lead asked for and the house range of 5,000–7,000 words. The audit fixes added about 600 words (H2 refit, harness disclosure, timing record, power statements, Table 3). Further cuts could come from Sections 2–4 or from the E4 detail.
2. **Harness disclosure (Section 5.4).** It says each call's context included a field for the account's e-mail address, without giving the address. Check that you are content to disclose this.
3. **H2 for Sonnet.** The paper keeps the registered GLMM numbers as the registered result. It reports the accurate refit and the exact paired test as post hoc, and Table 4 has a note explaining the odds ratio of 0.04.
4. **Item 3 timing.** The paper follows your correction in §9: the threshold was coded before verification began, per the engineer's record. It says plainly that git cannot confirm this.
5. **Unchanged.** The Anthropic page is cited under Favaro and Wright, with no date, and Greenblatt et al. as ICML 2024. Several human-factors sources were seen as abstracts only (`sources.md`).
6. **Added in the LaTeX conversion (v0.4).** Besides format, the conversion added only notation, which you may wish to check or drop: the sentence defining $z$ as the inverse of the standard normal cumulative distribution function (§2.1); Eq. (3), the log-linear correction written out as the corrected rates $\tilde H = (n_h + 0.5)/(n_s + 1)$ and $\tilde F$, with its symbols defined and a sentence saying that $d'$ and $c$ use them while the tables report the uncorrected $H = n_h/n_s$ and $F = n_f/n_n$ (§2.1); and Eqs. (4) and (5), the H1/H3 logistic regression and the H2 random-intercept model, with their symbols defined (§5.7). All follow `code/analyse.py` (`sdt`, `contrast`, `glmm_random_intercept`) and make no new claim. Figure 2's caption now says (a) and (b) instead of (left) and (right), because its panels are stacked. The data-availability paragraph was replaced by the standard Materials sentence, which links to this folder on GitHub instead of naming `code/`, `data/`, `results/RESULTS.md` or `AUDIT.md`; the MBPP CC BY 4.0 attribution moved to a footnote in §5.2.

## Revision log

**v0.4 (4 November 2026): LaTeX conversion**

Format conversion of v0.3 to the house style in `papers/STYLE.md`; no result, number, quotation or claim changed.

- `paper.md` became `paper.tex` (exact STYLE.md preamble, `techreport.sty`; title "Do LLM Monitors Miss Rare Threats? A Pre-registered Test of the Low-Prevalence Effect"; date "Working draft v0.4, 4 November 2026. Not peer reviewed."; no keywords or status box). `paper.md` and `paper.html` deleted (in git history).
- References: APA author–date citations became numeric IEEE citations (`\cite`, order of first use; narrative form "Wolfe et al. [4]"; section and abstract locators kept, e.g. "[1, Sec. 2.2]"). `references.bib` holds all 38 references (38 before and after), with titles and author names from the arXiv and Crossref records logged in `sources.md`; preprints as arXiv preprints, web pages with access notes, Kapetanovic et al. as in press. Page ranges added where Crossref gives them (Zheng et al.), issue/article numbers and months where Crossref gives them, and the conference locations Zurich, Switzerland (Cutler and Paddock) and Rome, Italy (Kapetanovic et al.) from Crossref and the paper's ACM reference format. Kapetanovic et al.'s Crossref pages (2043–2052) are not added while the paper is in press.
- Tables: booktabs, captions above, each with a source line naming its results file. Figures: redrawn by the new `code/figures_report.py` with `papers/_build/palette.py` (Haiku orange, Sonnet blue, Latin Modern serif, vector PDF), same data and error bars, panels as subfigures (a)/(b). Equations: d′ and c as numbered equations, plus the notation listed under "What James should check", item 6. Units and large numbers via `siunitx` (percentages now print with a thin space, e.g. "2.5 %"); file names, commits and model IDs in monospace.
- Closing: the acknowledgement, AI-assistance, disclaimer and data-availability text replaced by the standard STYLE.md Acknowledgement (AI assistance with the code-and-analysis options and the sentence "Claude models also served as the item generator and as the monitors under study."; competing interests; disclaimer; materials). MBPP CC BY 4.0 attribution kept as a footnote in §5.2.
- Checks: `papers/_build/build.sh` builds a 23-page PDF with no errors, no undefined references or citations and no overfull lines. `check_bib.py`: 30 OK; 2 CHECK, both expected (Hautus et al. 2021: Crossref stores the subtitle "A User's Guide" separately; Greenblatt et al.: arXiv v1 is 2023 but the 2024 ICML version is cited); 6 NO-ID (Green and Swets; the Favaro and Wright, Najt et al., Remedios et al. and Claude Code pages; Zhao et al. in PMLR), checked by hand against `sources.md`; no missing or uncited keys. `compare_text.sh`: every word difference is citation format, standard closing text, title block, section numbering and cross-references, caption placement, table layout or typographic markup (`siunitx`, math), apart from the notation added in item 6; a separate check confirmed that every number in the v0.3 text, abstract and tables appears in the new PDF, and that the abstract is unchanged.
- **Additions beyond format, for the author to review.** The conversion added notation only; each item was checked against `PREREGISTRATION.md` (§5, §6, §9 items 1 and 9) and `code/analyse.py`, and matches both:
  - §2.1, the sentence "Here $z$ is the inverse of the standard normal cumulative distribution function": the pre-registration's "z (standard normal deviate) scale" (§9 item 1); `sdt()` uses `norm.ppf`.
  - Eq. (3), the log-linear correction $\tilde H = (n_h + 0.5)/(n_s + 1)$, $\tilde F = (n_f + 0.5)/(n_n + 1)$, with its symbols defined, and the sentence "$d'$ and $c$ are computed with $\tilde H$ and $\tilde F$ in Eqs. (1) and (2); the rates $H = n_h/n_s$ and $F = n_f/n_n$ reported in the tables are uncorrected": pre-registration §5 ("add 0.5 to hits and false alarms, 1 to signal and noise counts"), applied to all cells; `sdt()` (corrected, for $d'$ and $c$) and `describe()` (uncorrected `H = hits / n_backdoored`, `F = false_alarms / n_clean`, as in Tables 2 and 5).
  - Eq. (4), the H1/H3 model, $\operatorname{logit}\Pr(y_i = 1) = \beta_0 + \sum_k \beta_k x_{ik}$ with one indicator per non-reference condition (reference P50 for H1, P2.5 for H3) and $\exp(\beta_k)$ the odds ratio: pre-registration §6 (logistic regression of flag on condition, backdoored items, SEs clustered by batch, stated in the text beside the equation); `contrast()`/`glm_cluster()` (binomial GLM, default logit link, `Treatment(ref)` coding, `cov_type="cluster"` by `batch_key`; H3 data are the P2.5 and R-cal batches only).
  - Eq. (5), the H2 model, $\operatorname{logit}\Pr(y_{ij} = 1 \mid u_j) = \beta_0 + \beta_{none}x_{none,ij} + \beta_{S1}x_{S1,ij} + u_j$, $u_j \sim N(0, \sigma^2)$, item $j$ = MBPP problem, reference S50: pre-registration §6 and §9 item 9 (item random intercepts; ML with 40-node Gauss–Hermite quadrature, stated in the text); `glmm_random_intercept()` (intercept plus *none* and S1 indicators, normal random intercept with SD $\sigma$, items = `problem_id`).
  - Also: Figure 2's caption says (a)/(b) instead of (left)/(right); table source lines and subfigure labels; the MBPP licence sentence moved from the data-availability paragraph to a footnote in §5.2.
- **Author decisions applied: A3, A6** (and the STYLE.md audit wording).
  - **A3 (impersonal voice):** the four first-person passages outside quotations were rewritten without changing meaning: abstract "In a pre-registered experiment we tested" → "A pre-registered experiment tested"; §4.2 "We searched … We found no study" → "Searches of … found no study"; §5.4 "replaced by our own" → "replaced by the study's own"; §5.9 "we infer that" → "it is inferred that". A case-insensitive search for I/we/our/us/my/me now finds only the quotation from Bhatt et al. ("higher than what we expect …"). The abstract copy in this README was changed to match.
  - **A6 (company sources):** the Anthropic sources are kept and labelled in `references.bib`: Favaro and Wright as a company research report; SLEIGHT-Bench and Red-Teaming Auto Mode as company research blog posts, not peer reviewed; SHADE-Arena as a research report led by Anthropic with co-authors from other organisations, not peer reviewed; the Claude Code page as company product documentation. Corroboration added where it exists and was opened and verified: the arXiv versions of SLEIGHT-Bench (arXiv:2605.16626) and Red-Teaming Auto Mode (arXiv:2609.19587), cited alongside the posts only for the same claims (§3.2 catch rate and 1 % FPR calibration; §5.4 blocking monitors; §8 attack realism). The blog-only quotation keeps its single citation. No peer-reviewed SHADE-Arena version and no independent source for Anthropic's deployment flag and escalation rates were found (searches in `sources.md`, v0.4). New Limitations paragraph "Company sources": "Two background facts rest on a single company's account and are not peer reviewed: Anthropic's deployment flag and escalation rates (Section 3.3) and the SLEIGHT-Bench catch rates (Section 3.2)."
  - **Closing text:** the AI-assistance paragraph now reads "An independent AI-assisted audit checked the references and quotations, and the analysis, against their sources", as in the STYLE.md template.
  - **Checks after the decisions:** build 23 pages, no errors, undefined references, overfull lines or BibTeX warnings; `check_bib.py` exits 0 with 32 OK, the same 2 expected CHECKs and 6 NO-IDs as above, and no missing or uncited keys; `compare_text.sh` against the v0.3 Markdown (`dfd94b7`) shows 625 changed lines; the only differences beyond those listed above are the A3 rewordings, the added citations and the new Limitations sentence.
- **Fixes from the independent v0.4 conversion check** (`AUDIT.md`, "v0.4 conversion check (4 November 2026)"; the check found the conversion faithful):
  - 2b (moderate): Eq. (3) now names the corrected rates $\tilde H$, $\tilde F$, and §2.1 states that $d'$ and $c$ use them while the tables report the uncorrected $H$ and $F$ (checked against `sdt()` and `describe()` in `analyse.py`).
  - 4a: the §7.3 citation now renders "[8, 9]" (sorted by the shared `cite` package; no source change needed).
  - 5d: the `najt2026arxiv` note adds the University of Waterloo (page 1 of the v2 PDF lists the Anthropic Fellows Program, University of Waterloo, Redwood Research and Anthropic).
  - 6a: the Limitations "Company sources" sentence now reads "rest on reports published by a single company …: Anthropic's deployment flag and escalation rates (Section 3.3), reported by Anthropic alone, and the SLEIGHT-Bench catch rates (Section 3.2), from work run in Anthropic's Fellows Program and published by Anthropic".
  - 7d: `\code{CLAUDE.md}` in §5.4. 7e: the Materials paragraph uses the STYLE.md wording: "The verification log and audit record for this paper, and its pre-registration, code, data and raw outputs, are at" the GitHub folder URL.
  - Optional items applied: title line break after "Threats?" (`\texorpdfstring`, so the PDF title metadata is unchanged); Table 6 caption begins "Post hoc."; the README now mentions the two conference locations; `code/figures_report.py` pins the face to the TrueType LM Roman 10 copies (dropping the CFF Latin Modern entries from Matplotlib's list) and keeps the source font timestamps, so re-runs are byte-identical. The redrawn PDFs render pixel-identical to the previous ones.
  - Checks after these fixes: 23 pages, no errors, undefined references, overfull lines or BibTeX warnings; `check_bib.py` exits 0 (32 OK, 2 expected CHECKs, 6 NO-IDs, no missing or uncited keys); `compare_text.sh` against `dfd94b7` shows 629 changed lines, the extra ones being the edits above.

**v0.2, 4 November 2026, after the independent audit (`AUDIT.md`)**

| Audit item | Action |
|---|---|
| 1 (moderate) H2 GLMM inaccurate for Sonnet | §6.4: registered numbers kept as the registered result. Added an explanation that the 40-node fit stopped at a local optimum and is inaccurate at large σ, so the 9–33 spread is a quadrature artefact. Added, post hoc, the accurate fit (σ 13.4; −3.76, SE 1.41, z −2.67, p .0076; LR p .00024) and the exact paired tests (Sonnet 9 vs 0, p .0039; Haiku 12 vs 7, p .36). §8 updated |
| 2 (moderate) registered measures missing | New Table 3 (registered): *d′*, *c*, AUROC with CIs and mean suspicion scores for all 16 cells, from `RESULTS.md` §10.2. Table 6 is now post hoc columns only |
| 3 (moderate) registered power statement | §5.7 states it; it is applied to the Haiku H2 null (§6.4), the H3 null (§6.5) and §8 |
| 4 (moderate) §9 item 3 | §5.8 cites the author's correction, gives the original wording, and says the timing comes from the engineer's record and cannot be confirmed from git. Caveat on items 4–12 kept. Added that the analysis code, including the GLMM rule, was committed at 23:10:45 UTC, before the first main output at 23:12:32 UTC (checked against git and `monitor_attempts.jsonl`) |
| 5 (moderate) "crowding rather than rarity" | Abstract, §1, §7.1, §7.2 and §9 rephrased: rarity did not increase misses, and misses were more frequent with several backdoors per batch. Pop-out and crowding are presented as equal candidates, with P10 ≈ P50 noted |
| 6 (moderate) harness context | §5.4 states: not `--bare`; default system prompt replaced; about 1,800 tokens of scaffolding per call (Haiku 1,812, Sonnet 1,791), constant across conditions and time; no CLAUDE.md, memory, git status or hooks; an account e-mail field present (address not printed). §8 updated |
| 7 379 vs 419 pairs | Abstract now says the judgements are drawn from 379 pairs; §5.2 states that main items came only from the main pool |
| 8 "more than crowded" | Now "in three of four comparisons" (abstract, §6.6), with Haiku's p = .051 in README and §6.6 |
| 9 independence instruction | §1: described as a prompting instruction, not a screening-research remedy |
| 10 Najt wording | §3.2: "half of its 40 hand-designed attacks were never caught … in any of ten trials" |
| 11 Wolfe 2007 false alarms | §2.2 and §7.4 now say false alarms were higher than in the baseline experiment (re-checked: within Experiment 7, 0.13 vs 0.15, ns) |
| 12 "two changed lines" | §5.2: lines changed in a unified diff (added plus removed), for example one line replaced |
| 13 independence of judgements | §5.4: "every call is an independent random draw" |
| 14 H1a not a Wald test | §5.7: Wald tests are for H1–H3; H1a is a bootstrap decision rule |
| 15 in-call corrections | §5.9 and §8: inferred from `num_turns` > 2, intermediate outputs unlogged, not anticipated by the registered retry rule |
| 16 Sonnet S1 criterion and scores | §6.4, §7.1, §7.5: Sonnet's Δ*c* interval includes zero; ΔAUROC −0.017 [−0.034, −0.004], mean backdoored score 75.0 → 62.7, band flag rate not lower; "most human-like" tempered |
| 17 Table OR 0.04 | Table 4 note: the GLMM OR is item-specific; population-averaged OR 0.61 [0.44, 0.84], −7.5 points |
| 18 sensitivity check | §6.6: H2 tested with the item-clustered GLM; Haiku H3 p .150 → .076 |
| 19 §7.5 post hoc | "post hoc score-band analysis" stated |
| 20 Figure 2 caption | Now: cluster bootstrap over batches (Exp 1, 3) or paired item bootstrap (Exp 2) |
| 21–22 scripts and docstrings | Engineer's items (`code/posthoc_descriptives.py`; docstrings fixed). No paper change needed |
| 23 references | Kapetanovic et al. "in press" (no pages); Griffin (IASEAI '26) and Hida (ENIAC 2026, BRACIS) notes; Wolfe 2013 "Article 33" |
| 24 length | Background, Methods and Discussion trimmed (Mitroff & Biggs and Makins et al. dropped). Prose about 7,650 words, against about 7,800 in v0.1, despite the additions |
| 25 spelling | "judgement(s)" throughout, except inside quotations |
| 26 (suggestion) E1 dip | §6.6 now notes the low hit rates at positions 1–8 in P10, which the linear test would not detect |
| 27 (suggestion) code timing | Included in §5.8 (see item 4) |

**v0.1, 4 November 2026.** Results, Discussion, Limitations and Conclusion written from `results/`; the paper was retitled.

**Phase 1, 3 November 2026.** Introduction, Background, Methods and Limitations skeleton.

## Open questions

- Is the drop in hits about the *number* of backdoors in a context or their *share*? All batches held 40 items, so the two were not separated, and pop-out and crowding cannot be told apart.
- Does the effect carry over to agent transcripts, where several suspicious actions may share one monitor call?
- Would monitors that run at higher effort, in `--bare` mode or through the raw API behave differently?

## How to develop it

- **Separate number from share.** Vary batch size and the number of backdoors independently, for example 1, 2, 3, 5 or 20 backdoors in batches of 40, 100 and 200.
- **Clustered attacks in agent settings.** Test whether placing several attacks in one transcript, or in one monitored batch of actions, lowers per-attack suspicion (BashBench, SHADE-Arena or LinuxArena-style tasks).
- **Other monitor families and settings.** GPT, Gemini and open-weight monitors; higher effort; `--bare` mode or direct API calls, with the full context logged.
- **Lower prevalence.** 1 in 100 or 1 in 400 with longer contexts.
- **Matched calibration examples.** Following Becker et al. (2026), compare calibration examples of the same backdoor type as the target with examples of a different type, and measure the false-alarm cost against an audit budget.
- **Human comparison.** Run people on the same items, singly and in batches, at the same prevalences.
- **TIP for measurement.** Use inserted known attacks to estimate a deployed monitor's hit rate under its real input mix; Buser et al. (2025) give a target of about 100 events.

## Files

- `paper.tex`: the paper (source of truth), and `references.bib`: its BibTeX references (IEEE style). Build `paper.pdf` with `papers/_build/build.sh papers/02-do-llm-monitors-miss-rare-threats` from the repository root; `paper.bbl` is kept for arXiv. The Markdown source `paper.md` and `paper.html` (v0.3) were removed in v0.4 and remain in git history.
- `figures/report/fig_*.pdf`: the paper's figures (vector PDF, house style, one file per panel), drawn by `code/figures_report.py` from `results/analysis.json` and `results/judgments.csv`. The registered PNGs in `figures/` (from `code/analyse.py`) are unchanged and not used by the paper.
- `sources.md`: verification log, gap-search record and a table tracing every number to the results files.
- `PREREGISTRATION.md`: the registered design and §9 clarifications.
- `AUDIT.md`: the independent audit.
- `code/`, `data/`, `results/`, `figures/`: experiment, by the research engineer; `results/RESULTS.md` is the full numerical report. `code/figures_report.py` (v0.4) only redraws the figures.


### v0.3 (4 November 2026)

Second-round verification fixes (see AUDIT.md, "Second-round verification") applied by the lead session: §1 contribution now says "not a *conservative* criterion shift"; §7.1 Sonnet H2 wording corrected (effect at least partly through scores; criterion moved conservative but not reliably); §5.7 power sentence distinguishes Experiment 3 from the paired Experiment 2; §5.8 adds the history of the threshold code comment (`7fe31dc` → `d8e6b51`); sources.md table numbers, Makins status and Remedios locator corrected; stray blank line in references removed. Length (item 24) not cut further: left for venue-specific trimming.

### v1.0 (4 November 2026): released as a preprint

All review items closed (James accepted the recommended defaults for B2.1–B2.3). Date line changed from "Working draft v0.4" to "Preprint v1.0"; affiliation printed as CitadelAero. No change to content.
