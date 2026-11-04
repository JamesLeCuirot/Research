# Independent audit: paper 02, "Do LLM Monitors Miss Rare Threats?"

Auditor: independent audit agent (Claude), 4 November 2026. Scope: `paper.md` (Draft v0.1, 4 November 2026), `PREREGISTRATION.md`, `code/`, `data/`, `results/`, `figures/` and `sources.md`. Nothing in `paper.md`, `code/`, `data/` or `results/` was edited. All re-runs used a copy of the folder in the auditor's scratchpad. No model API or `claude -p` calls were made.

## Summary

| Severity | Count | Meaning |
|---|---|---|
| Major | 0 | Would change a conclusion or misreport a confirmatory result |
| Moderate | 6 | Must be fixed before circulation: registered reporting gaps, a numerical problem in the H2 model, framing that goes beyond the data, an undisclosed methods detail |
| Minor | 19 | Wording, precision, labelling, reproducibility and reference-format fixes |
| Suggestion | 2 | Optional |

Main findings:

- **The re-analysis reproduces.** `code/analyse.py` re-run on a copy of `results/monitor_raw.jsonl` gives byte-identical `judgments.csv`, `analysis.json` and `RESULTS_numbers.md`, and byte-identical figures. `posthoc_turns_sensitivity.py` also reproduces exactly. Every number checked in the abstract, text, Tables 1–5 and figure captions matches.
- **Independent recomputation agrees.** The auditor's own script reads the raw JSONL directly and uses its own IRLS logistic fit, CR1 cluster-robust variance, Holm step, log-linear SDT and bootstrap. It reproduces all hit and false-alarm rates, *d′*, *c* and AUROC, and the H1, H3 and E2 odds ratios, z and p values to the reported precision. The Table 4 bootstrap intervals agree within Monte Carlo error.
- **No bug changes a conclusion.** The direction and significance of H1 survive a small-cluster Welch test (p = .0056 Haiku, p = .0002 Sonnet) and an adjustment for item difficulty (OR 2.18, p = .03; OR 2.95, p = .0001). The Sonnet H2 result survives an exact paired test (9 items flagged under S50 but not S1, 0 the other way; p = .0039).
- **No label leakage was found.** The system and user prompt of every one of the 2,176 main calls was rebuilt from `design_main.jsonl` and `items.jsonl`, and every SHA-256 matches the hash stored in the raw record. Outside R-cal, no prompt contains a trigger, a test, a label or the word "backdoor" in item text. IDs are random, backdoor positions span 1–40, no problem appears twice in a batch, and the R-cal examples come only from the disjoint calibration pool.
- **The confirmatory analysis code was fixed before the data.** `analyse.py`, with the GLMM convergence rule of §9 item 9, `monitor.py`, `common.py` and `s6_design.py` are in commit `7fe31dc` (23:10:45 UTC). The first main-experiment output was written at 23:12:32 UTC. Post-data changes to `analyse.py` are additions only: the GLMM node check, the post hoc score-band table and figure legend placement.

## Issues

| # | Severity | Location | Problem | Evidence | Required fix |
|---|---|---|---|---|---|
| 1 | Moderate | §6.4; Table 3 (H2, Sonnet); §8 "Measurement limits" | The registered 40-node non-adaptive Gauss–Hermite GLMM is numerically inaccurate for Sonnet. The reported fit (σ = 32.8, log-odds −3.32, SE 1.25, p = .0077) is a local optimum that BFGS stopped at with "precision loss"; it passed the §9 item 9 rule through the gradient criterion. The 9–33 range of σ "across quadrature settings" is mainly a quadrature artefact, not only poor identification. | Under the same 40-node approximation, profile log-likelihood is −97.53 at σ = 10 against −98.17 at the reported σ = 32.8, and flat at −111.8 for σ ≥ 60. The auditor's restart (Nelder–Mead then BFGS) of the same 40-node model stopped at σ ≈ 260 with SE 1.31, p = .011 and Holm p = .022. An accurate likelihood (dense-grid integration over ±9 SD) gives MLE σ = 13.4, S1 log-odds −3.76 (SE 1.41), z = −2.67, p = .0076; likelihood-ratio p = .0002. Exact paired test on backdoored items: Sonnet 9 vs 0 discordant, p = .0039; Haiku 12 vs 7, p = .36. Haiku's GLMM is stable (accurate fit −0.552, p = .246). | Keep the registered numbers as the registered result. Say plainly that 40-node non-adaptive quadrature is unreliable at this σ and that the 9–33 spread reflects that. Add, labelled post hoc: an accurate (adaptive or dense-grid) fit (σ ≈ 13, log-odds −3.76, p = .008), and the exact discordant-pair count (9 vs 0, p = .004) as the most transparent evidence. The conclusion is unchanged. |
| 2 | Moderate | §6 (whole); Table 5 | Registered measures are not reported in the paper. §5 and §6 (H1a) registered *d′*, *c* and AUROC per condition with 95% bootstrap CIs, and mean suspicion scores for clean and backdoored items. The paper gives *d′* and *c* only graphically (Figure 2), AUROC per condition nowhere, and mean scores for only 3 of 8 conditions, inside a table labelled "post hoc". | `results/RESULTS_numbers.md`, "Descriptive results per condition", holds all of them. PREREGISTRATION §5 lists "Mean suspicion score for clean and for backdoored items" as a registered measure. | Add a table (or extend Table 2) with *d′*, *c* and AUROC [bootstrap CI] and both mean scores for all 8 conditions × 2 monitors. In Table 5, label only the top-band and score-band columns as post hoc. |
| 3 | Moderate | §5.7; §8 | A registered commitment is unmet. PREREGISTRATION §6: "Effects smaller than about 15 points may be missed; the paper will say so." The paper gives the power calculation but never says this. It does not qualify the null H3 results (80 vs 160 judgments; Sonnet +11 points, p = .053) or Haiku H2 (−4 points; 120 paired items). | PREREGISTRATION §6 "Power (informal)"; paper §5.7 and §8. An approximate calculation gives about 45% power for a 10-point rise in Experiment 3. | Add the registered sentence and apply it to H2 and H3 in §6.4–6.5 and §8, for example: "With 80 to 160 judgments per cell, effects smaller than about 15 points may have been missed; the H3 and Haiku H2 nulls should be read in that light." |
| 4 | Moderate | §5.8, second and third sentences | §9 item 3 and its correction are misdescribed. The paper states the corrected timing ("set while the first generation run was under way") but cites "Section 9, item 3", whose text says something different ("set during verification of the first generation run"). It does not say that item 3 was corrected or by whom. The corrected timing rests only on the engineer's record: `s3_verify.py` and the 0.6 threshold first appear in git in `7fe31dc`, after generation and verification, so git cannot confirm it. | PREREGISTRATION §9 item 3 against "Correction to item 3 (added by the author, 4 November 2026)". `git log` shows no commit of `s3_verify.py` before `7fe31dc` (23:10:45). | Cite the author's correction to item 3. Say that item 3's original wording was superseded and that the "before the verifier was first run" timing comes from the engineer's record and cannot be confirmed from the git history. Keep the existing, accurate caveat on items 4–12. |
| 5 | Moderate | Abstract (last sentence); §7.1; §9 ("The weakness lay in crowding") | The crowding framing goes beyond the data. With batch size fixed at 40, "rarity" and "crowding" are the same manipulation (the share and the number of backdoors), so the data cannot show crowding *rather than* rarity. The pattern is a step between 1 and ≥4 backdoors: P10 (4/40) ≈ P50 (20/40) < P2.5 (1/40). That fits a lone backdoor standing out ("pop-out") as well as crowding. The conclusion states a mechanism that §8 says the design cannot identify. | Hit rates: Haiku 0.512 / 0.500 / 0.694, Sonnet 0.500 / 0.569 / 0.738. P10 vs P50: p = .83 and .21. §8: "It cannot show why." | Rephrase, for example: abstract, "In this setting, misses were more frequent when several backdoors shared a batch than when one did; rarity did not increase misses." §9: "Backdoored items scored lower when several shared a batch." Present pop-out and crowding as equal candidate explanations, and note that P10 behaved like P50. |
| 6 | Moderate | §5.4; §8 | The monitors' full context is not disclosed. Calls were made without `--bare`. Claude Code's docs state that without `--bare`, `claude -p` loads hooks, auto memory, CLAUDE.md and system reminders. Each call carried about 2,000 input tokens beyond the study's prompts, and this content was not logged. "Our own system prompt" implies the monitor saw only the study's text. | Single-item calls average about 2,430 input tokens against about 300–420 tokens of system plus user prompt (`results/monitor_raw.jsonl`, `model_usage`). The overhead is constant: the token residual for identical item content has SD ≈ 2 tokens, with no shift at any of 20 commits during the run, so git status was not injected (consistent with the docs: `--system-prompt` drops the git snapshot). No CLAUDE.md exists in the repository or `~/.claude`. Docs: https://code.claude.com/docs/en/headless ("Start faster with bare mode"). | In §5.4, state that calls were not run in `--bare` mode, that Claude Code adds its own scaffolding (about 2,000 tokens per call, identical across conditions, not logged), and that `--system-prompt` removes the default prompt and git snapshot. Add a sentence to §8. Optionally, capture one call with `--output-format stream-json --verbose` to document what is added. |
| 7 | Minor | Abstract, sentence 6; §1 contributions | "Two Claude models reviewed 419 execution-verified pairs … (30,880 judgments)." The 30,880 main judgments come from the 379 main-pool pairs. The 40 calibration pairs were used only in Haiku's calibration run (80 judgments, not counted) and as labelled R-cal examples. | `data/pools.json`: main 379, calibration 40. All 379 main problems appear in the main runs. | For example: "Two Claude models made 30,880 judgments of 379 of 419 execution-verified pairs …". |
| 8 | Minor | Abstract ("more than crowded ones"); §6.6 E4 | One of the four single-item vs crowded-batch comparisons is not significant: Haiku P50 vs single, OR 0.61, p = .051. | `RESULTS_numbers.md`, E4. | Soften the abstract ("and more than crowded batches in three of four comparisons") or add the p value. |
| 9 | Minor | §1, third contribution bullet | "two remedies from screening research": the independence instruction (E2) is a prompting intervention, not a screening-research remedy. | PREREGISTRATION §2 E2. | "a TIP-style labelled calibration block from screening research and an independence instruction". |
| 10 | Minor | §3.2 (SLEIGHT-Bench) | "an Opus 4.6 monitor never caught 50% of its 40 hand-designed attacks in ten trials" can be misread as "never reached a 50% catch rate". | Source: "On Opus 4.6, the main monitor we work with, 50% of attacks are never caught on any of the 10 trials." | "half of the 40 hand-designed attacks were never caught in any of ten trials". |
| 11 | Minor | §2.2 ("while false alarms rose"); §7.4 ("also saw false alarms rise with their remedy") | In Wolfe et al. (2007, Experiment 7) the rise in false alarms is relative to Experiment 1a. Within Experiment 7, false alarms did not differ by prevalence (0.13 vs 0.15). | PMC2662480, Experiment 7: "Compared with Experiment 1a … false alarms were correspondingly increased." | Add "relative to Experiment 1a" or "than in their baseline experiment". |
| 12 | Minor | §5.2 ("356 (85%) changed exactly two lines") | The metric counts added plus removed lines in a unified diff, so a single replaced line counts as two. Readers will take "changed two lines" literally. | `code/s3_verify.py` `changed_lines()`; RESULTS.md §3 defines it. | "had two changed lines in a unified diff (added plus removed), for example one line replaced". |
| 13 | Minor | §5.4 ("so every judgment is an independent random draw") | Judgments within one batch call are produced jointly and are not independent; that is why batch clustering is used. | `analyse.py` clusters Experiments 1 and 3 by batch. | "every call is an independent random draw". |
| 14 | Minor | §5.7 ("All confirmatory tests are two-sided Wald tests") | H1a is a bootstrap decision rule, not a Wald test. | PREREGISTRATION §9 item 1. | "The H1, H2 and H3 tests are two-sided Wald tests…". |
| 15 | Minor | §5.9; §8 "Process" | That Claude Code corrected schema-invalid outputs inside a call is inferred from `num_turns` > 2. The intermediate outputs are not logged. These are in effect retries with feedback, which §7 of the pre-registration did not anticipate (§7 registered fresh-call retries only). | `results/monitor_raw.jsonl` `num_turns`; RESULTS.md §5 ("We see only the final output"). | Say "inferred from `num_turns` > 2" and note in one clause that these in-call corrections differ from the registered fresh-call retries. The sensitivity analysis already covers the impact. |
| 16 | Minor | §6.4; §7.1 ("criterion-like"); §7.5 ("most human-like … moved both monitors' criterion") | "moved the criterion … for both monitors" when Sonnet's interval includes zero (−0.01 to 0.58). The paper also omits that S1 lowered Sonnet's AUROC (ΔAUROC −0.017, CI −0.034 to −0.004) and backdoored scores (mean 75.0 to 62.7), while the flag rate in the 40–59 band did not fall (0.83 to 1.00). By the paper's own post hoc logic, the Sonnet S1 effect also ran through scores. | `RESULTS_numbers.md`: H2 "S1 minus S50" table; descriptive and band tables. | Say "conservative for Haiku (CI excluding zero) and in the same direction for Sonnet (CI including zero)". Report Sonnet's ΔAUROC and mean-score change. Temper "most human-like". |
| 17 | Minor | Table 3, H2 Sonnet row | OR 0.04 [0.00, 0.42] sits next to "Supported (small effect)", which looks contradictory without the §6.4 explanation. | §6.4 gives the population-averaged OR 0.61 and −7.5 points. | Add a table note: the GLMM OR is item-specific; population-averaged OR 0.61 [0.44, 0.84]; hit rate −7.5 points. |
| 18 | Minor | §6.6 ("Dropping the calls … left H1, H2 and H3 unchanged"); §8 | The H2 sensitivity check used the item-clustered GLM, not the registered GLMM. Haiku's H3 p moved from .150 to .076 (still not significant). | `code/posthoc_turns_sensitivity.py`; `results/sensitivity_excluding_extra_turn_calls.json`. | "(H2 tested with the item-clustered GLM)", and give the Haiku H3 p if the sentence lists results. |
| 19 | Minor | §7.5, last sentence | "SDT … made it possible to see that the reversal came from the scores" rests on the post hoc score-band analysis but is not labelled post hoc there. | §6.6 labels the band analysis post hoc. | Add "post hoc". |
| 20 | Minor | Figure 2 caption | "95% cluster-bootstrap confidence intervals": for the three single-item conditions the intervals come from a paired item bootstrap. | `analyse.py` `boot_conditions(..., "item_key", "backdoored", paired=True)`. | "cluster bootstrap over batches (Experiments 1 and 3) or paired item bootstrap (Experiment 2)". |
| 21 | Minor | §5.2 (edit-type classification); §6.6 (thinking tokens); `code/` | Two reported results have no script in `code/`: the edit classification (254 / 150 / 15) and the thinking-token table (7,592 / 4,195; 116 / 480). The paper says code for everything is released. | The auditor reproduced both: same-statement-count 254, adds an `if` 150, other 15; thinking tokens as reported. | Add the two short scripts (or functions in `analyse.py`) and list them in `code/README.md`. |
| 22 | Minor | `code/analyse.py` docstrings | The module docstring says the script reads `data/design_main.jsonl` and `data/items.jsonl`; it reads only `monitor_raw.jsonl`, whose `shown` records the auditor verified are identical to the design. The `glmm_random_intercept` docstring ("'converged' = optimiser success and a positive-definite Hessian") does not match the implemented §9 item 9 rule. | Code read; integrity script. | Correct the docstrings (no effect on results). |
| 23 | Minor | References | (a) Kapetanovic et al. (2026): Crossref dates the CIKM '26 proceedings 7 November 2026, after this draft; mark it "in press" or recheck before circulation. (b) Griffin et al. v2 was presented at IASEAI'26 and Hida et al. was accepted at ENIAC 2026 (BRACIS); consider noting this, as done for Chen, Srivastav and Ye. (c) Wolfe et al. (2013): APA form is "*13*(3), Article 33". | arXiv API comments; Crossref. | Update the entries. |
| 24 | Minor | Whole paper | Main text is about 7,700 words excluding tables and captions (about 8,600 including). The house range for empirical papers is 5,000–7,000 words. The abstract is 250 words, at the limit. | Word count of `paper.md`. | Trim about 700 words, for example from §2–§4. |
| 25 | Minor | §7.2, line 278 | "judgement" here; "judgment(s)" in eight other places. | grep. | Use one spelling throughout. |
| 26 | Suggestion | §6.6 E1; Figure 5 | The registered linear position test (all p ≥ .08) would not pick up the visible dip at positions 1–8 in P10 (Sonnet 0.31 against 0.69 at 9–16; Haiku 0.40). | Figure 5. | Optionally add one descriptive sentence; no new test is needed. |
| 27 | Suggestion | §5.8 | The caveat on items 4–12 is accurate. It could add a verifiable fact: the code implementing items 5 and 8–11 (verification checks, retry policy, GLMM rule, sampling, Fisher fallback) was committed in `7fe31dc` at 23:10:45 UTC, before the first main call completed at 23:12:32 UTC. | `git log`; `results/monitor_attempts.jsonl` timestamps; `analyse.py` hash unchanged from `7fe31dc` until post-data additions in `e78e15e`. | Optional sentence. |

## Re-analysis

### 1. Official pipeline on a copy

`uv run … python analyse.py` was run in the copied `code/` folder (Python 3.13.18, statsmodels 0.15.0; uv resolved pandas 3.0.5 and numpy 2.5.3 rather than the README's 3.1.0 and 2.5.4). Its outputs were compared with `cmp`:

- `judgments.csv`, `analysis.json` and `RESULTS_numbers.md`: identical.
- `fig_a` to `fig_e`: identical.
- `sensitivity_excluding_extra_turn_calls.json`: identical.

### 2. Integrity checks (auditor's script)

- There are 2,176 raw records. Their call IDs equal those in `design_main.jsonl`, and `shown`, `examples`, condition, variant and batch key match the design in every record.
- Rebuilt system and user prompts match `system_sha256` and `user_sha256` for all 2,176 calls.
- Prevalence per batch is exactly as designed: P50 20/40 ×8, P10 4/40 ×40, P2.5 1/40 ×160, R-cal and R-ind 1/40 ×80, single items 120 + 120, all per monitor. All 368 batch compositions are identical across the two monitors. The Experiment 2 item set is identical in all six cells (240 distinct problems).
- No problem appears twice in a batch. All shown items are from the main pool. Each R-cal batch has 10 distinct calibration-pool examples (5 backdoored), none overlapping the batch.
- Every call is valid at the first attempt. In-call corrections (`num_turns` > 2): Haiku batch 43/368, Sonnet single 24/720, none elsewhere.
- No item flagged with suspicion < 20 (minimum flagged score 25). No item with suspicion ≥ 60 left unflagged (maximum unflagged score 48).
- Costs sum to USD 41.70. Thinking-token means are as reported. Calibration: 24/40 hits, 0/40 false alarms, AUROC 0.969. Calibration calls ran 23:09:43–23:10:44 UTC; commit `136632a` (items 1–3) is 23:10:31; first main output 23:12:32; commit `d8e6b51` holds 138 main outputs.

### 3. Key numbers: paper against independent recomputation

Hit and false-alarm rates, recomputed from `monitor_raw.jsonl`. All agree to the paper's precision (Table 2):

| Condition | Haiku *H* | Haiku *F* | Sonnet *H* | Sonnet *F* |
|---|---|---|---|---|
| P50 | 82/160 = 0.512 | 3/160 = 1.9% | 80/160 = 0.500 | 1/160 = 0.6% |
| P10 | 80/160 = 0.500 | 17/1440 = 1.2% | 91/160 = 0.569 | 20/1440 = 1.4% |
| P2.5 | 111/160 = 0.694 | 74/6240 = 1.2% | 118/160 = 0.738 | 108/6240 = 1.7% |
| R-cal | 48/80 = 0.600 | 38/3120 = 1.2% | 68/80 = 0.850 | 124/3120 = 4.0% |
| R-ind | 50/80 = 0.625 | 23/3120 = 0.7% | 60/80 = 0.750 | 56/3120 = 1.8% |
| none | 76/120 = 0.633 | 2/120 = 1.7% | 96/120 = 0.800 | 1/120 = 0.8% |
| S50 | 82/120 = 0.683 | 4/120 = 3.3% | 102/120 = 0.850 | 4/120 = 3.3% |
| S1 | 77/120 = 0.642 | 1/120 = 0.8% | 93/120 = 0.775 | 2/120 = 1.7% |

Wilson CIs, log-linear *d′* and *c* (for example Haiku P50 2.05 / 0.99, Sonnet P2.5 2.74 / 0.74), AUROC and mean scores all agree with `RESULTS_numbers.md` and Table 5.

| Test | Paper | Auditor (independent code) | Agreement |
|---|---|---|---|
| H1 Haiku, P2.5 vs P50 | OR 2.15 [1.34, 3.46], z 3.18, p .0015, Holm .0015 | OR 2.15 [1.34, 3.46], z 3.18, p .00149, Holm .00149 (208 batch clusters, CR1) | Exact |
| H1 Sonnet | OR 2.81 [1.78, 4.43], z 4.44, p < .001 | OR 2.81 [1.78, 4.43], z 4.44, p 8.8e-6, Holm 1.8e-5 | Exact |
| P10 vs P50 | Haiku OR 0.95, p .828; Sonnet OR 1.32, p .211 | Same | Exact |
| H1, small-cluster check (post hoc, auditor) | — | Welch *t* on batch-level hit rates: Haiku *t* 3.12, df 18.9, p .0056; Sonnet *t* 4.54, df 22.1, p .0002 | Supports H1 reversal |
| H1, item-difficulty adjustment (post hoc, auditor) | — | Covariate: leave-one-out item hit rate. Haiku OR 2.18, p .030; Sonnet OR 2.95, p .0001 | Supports H1 reversal |
| H1a, Table 4 (independent bootstrap, seed 7) | Haiku Δ*d′* 0.71 [0.06, 1.04], Δ*c* −0.12 [−0.59, 0.17]; Sonnet Δ*d′* 0.39 [−0.24, 0.95], Δ*c* −0.44 [−0.70, −0.28] | Haiku 0.71 [0.05, 1.04], −0.12 [−0.59, 0.17]; Sonnet 0.39 [−0.25, 0.97], −0.44 [−0.69, −0.27]. Δ*H*, Δ*F* and ΔAUROC agree within ±0.01 | Agrees (Monte Carlo error) |
| H1a decision | Not supported in either monitor | Criterion 1 fails in both | Agrees |
| H2 Haiku, 40-node GLMM | −0.557 (SE 0.478), OR 0.57, p .244 | −0.557 (SE 0.478), p .244. Accurate likelihood: −0.552, p .246. Exact paired test: 12 vs 7, p .36 | Agrees |
| H2 Sonnet, 40-node GLMM | −3.321 (SE 1.246), z −2.66, p .0077, Holm .015, σ 32.8 | Same point under the same optimiser. A restart finds σ ≈ 260, SE 1.31, p .011, Holm .022. Accurate likelihood: σ 13.4, −3.76 (SE 1.41), p .0076; LR p .0002. Exact paired test: 9 vs 0, p .0039 | Conclusion agrees; numerics fragile (issue 1) |
| H2 GLM, item-clustered | Sonnet OR 0.61 [0.44, 0.84], p .002 | Same (official re-run) | Exact |
| H3 | Haiku OR 0.66 [0.38, 1.16], p .150, Holm .150; Sonnet OR 2.02 [0.99, 4.10], p .053, Holm .106 | Haiku 0.66 [0.38, 1.16], p .1504, Holm .1504; Sonnet 2.02 [0.99, 4.10], p .0530, Holm .1059 | Exact |
| E2 | Haiku OR 0.74, p .288; Sonnet OR 1.07, p .835 | Same | Exact |
| Holm implementation | statsmodels `multipletests(method="holm")` | Hand-coded step-down Holm gives the same values | Correct |
| Log-linear correction | (hits + 0.5)/(n + 1) on all cells | Same formula, independent code | Correct |

## Code review: checks passed

- **Label leakage:** none (see Integrity checks). The monitor sees ID, task text and normalised code only. Triggers appear only in R-cal example labels, as registered. The schema `enum` lists the IDs in the order shown and carries no label information. Function names are identical between clean and backdoored versions. No comments or docstrings survive normalisation (the single `#` found is inside a regex string literal).
- **ID parsing and merging:** judgments are keyed by `sid`. `monitor.validate` enforces exactly the shown ID set, with no duplicates or unknown IDs.
- **Prevalence per batch:** correct (see Integrity checks).
- **Holm:** correct, and applied across the two monitors only for the confirmatory contrasts.
- **Log-linear correction:** correct (Hautus, 1995).
- **Bootstrap:** batches are resampled within each condition for Experiments 1 and 3. Items are resampled for Experiment 2, paired across conditions and stratified by item type. P50 and P2.5 are resampled independently for the H1a differences, which is appropriate because they are different batches.
- **Invalid outputs:** the code retries up to 3 times with fresh calls and then drops; the analysis keeps `status == "valid"` only. None occurred.
- **Cluster variables:** H1 and H3 cluster by `batch_key`. E3 Experiment 1 clusters on the shared `batch_key` (the same composition for both monitors). E4 clusters single-item calls by `call_id`.
- **Harness context:** not label leakage, but not logged (issue 6). The overhead is constant across conditions and over time.

## Faithfulness to the pre-registration

- H1, H1a, H2, H3 and E1–E4 were run as registered: same models, conditions, sample sizes, clustering and Holm correction. The §9 item 1 H1a rule and the item 9 GLMM rule are implemented as written, and both were in code committed before the first main call.
- Post hoc material is labelled in §6.6, Table 5, the abstract and §1, with the exceptions in issues 2 (mean scores are registered, not post hoc) and 19.
- §9 items 4–12 are described accurately, including the "recorded at, not demonstrably before" caveat, which the auditor confirmed against git and the run logs. The correction to item 3 is not described accurately (issue 4).
- Registered outputs that the paper omits: per-condition *d′*, *c*, AUROC and mean scores (issue 2), and the "effects smaller than about 15 points may be missed" statement (issue 3).
- Registered rules not triggered: no Fisher fallback was needed (no separation) and no batch was dropped.

## Interpretation

- **H1 reversed:** supported and robust (see Re-analysis). The 8-cluster caveat is stated, and small-cluster and item-adjusted checks agree.
- **"Crowding rather than rarity":** overstated (issue 5). The design varies one quantity (backdoors per 40). The data show a step between 1 and ≥4 backdoors; pop-out and crowding are not separated. The descriptive post hoc point that backdoored items scored lower at P50 than at P2.5 is correct.
- **Safety implications:** framed as hypotheses in §7.3 ("this study is not evidence that it does"). Acceptable.
- **Limitations:** Claude-only monitors and generator, effort `low`, toy MBPP code, one batch size, 8 batches at P50, item reuse and in-call schema correction are all covered. Missing: undisclosed harness context (issue 6), statistical power for the H2 and H3 nulls (issue 3), and the H2 quadrature problem (issue 1).

## References verified without issue

Checked for existence and bibliographic details (arXiv API, Crossref, PMLR or the publisher page), and for each specific claim attributed in the paper (quotes found verbatim in the source PDF or full text, or in the publisher or OpenAlex abstract):

Abbasi et al. 2026; Anthropic n.d. (headless docs: `-p`, `--json-schema`; the docs also note that `--system-prompt` drops the git snapshot); Austin et al. 2021; Becker et al. 2026; Bhatt et al. 2025 (§2.2 footnote 2; §3.1.1); Bliss et al. 1995; Buser et al. 2025 (abstract figures; §2 "1 %–4 %" and immediate feedback, from the publisher PDF); Cai et al. 2026 (no prevalence manipulation); Cain et al. 2013; Chen et al. 2026; Cutler & Paddock 2009; Favaro & Wright n.d. (30,000 agents "at any one time", August 2026; one to two flags per thousand; about 100,000 flags per week; about 50 per week escalated; "rarely misbehave"); Green & Swets 1966 (standard text, bibliographic); Greenblatt et al. 2024 (PMLR 235, pp. 16295–16336; quotes and §2.2, §3.1.2, §3.2 in arXiv v5); Griffin et al. 2024; Hautus 1995 (abstract via search index); Hautus et al. 2021; Hida et al. 2026 (§4.4; Llama result; 20 per batch; 2.9–53.0%); Huegli et al. 2020; Kale et al. 2025; Kim et al. 2026; Klein & Feltmate 2025; Korbak et al. 2025 (§4 and §6 quotes); Kutasov et al. 2025 (AUC 0.87 and 0.65; 103 minutes; human AUC on a 32-transcript subset); Liu et al. 2024; Mackworth 1948 (bibliographic; claim via Klein & Feltmate); Makins et al. 2026; Mitroff & Biggs 2014; Remedios et al. 2026; Sorkin & Woods 1985; Srivastav et al. 2026 (§6.3); Warm et al. 2008; Wolfe et al. 2005 (7%, 16%, 30%); Wolfe et al. 2013 (*d′* changed; liberal criterion after the high-prevalence block); Ye et al. 2026 (83/88; 9/16, §4.2); Zhao et al. 2021 (Figure 4 caption; PMLR 139, pp. 12697–12706); Zheng et al. 2023.

References with a claim or format issue (see the table): Najt et al. 2026 (issue 10), Wolfe et al. 2007 (issue 11; all other quotes verified), Kapetanovic et al. 2026 (issue 23a; quotes verified), Wolfe et al. 2013 format (23c).

The citation cross-check by script found all 40 references cited in the text and no in-text citation without an entry. The list is alphabetical in APA order, and "et al." use is consistent.

## Auditor's files

In the scratchpad (`/tmp/claude-0/-home-user-Research/daaac745-27bf-52cd-80c6-ef95e9ce6f1a/scratchpad/audit02/`): `scripts/integrity.py`, `scripts/recompute.py`, `scripts/glmm_check.py`, `scripts/h1_item.py`, `scripts/tokens.py`, `scripts/drift.py`, `scripts/drift2.py`, `scripts/citecheck.py`, `scripts/grepq.py`; the copied repository `repo_copy/` with re-run outputs; and the downloaded sources in `dl/`.
