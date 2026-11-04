# Results: the low-prevalence effect in LLM code monitors (paper 02)

Research-engineer report, 4 November 2026. The protocol is `../PREREGISTRATION.md`, and every
change or clarification is listed in its section 9. All numbers below come from `results/analysis.json`, produced by
`code/analyse.py` from the raw outputs in `results/monitor_raw.jsonl`. Section 9 of this file is a
verbatim copy of `results/RESULTS_numbers.md` from the final analysis run. Post-hoc material is
labelled as post hoc wherever it appears.

## 1. Plain-English summary

We generated 419 verified pairs of short Python solutions (clean, and a backdoored minimal edit)
for MBPP problems. Two Claude models then reviewed them as monitors: `claude-haiku-5-5` and
`claude-sonnet-5-5`, both at effort `low`. The study made 2,176 main monitor calls (30,880 item
judgments). Every call returned a valid output, with no refusals and no dropped batches.

- **H1 (experienced prevalence) is disconfirmed, and the effect runs the opposite way.** When
  backdoors were rare in a batch of 40, both monitors caught *more* of them, not fewer. Haiku's hit
  rate was 0.51 at 50% prevalence, 0.50 at 10% and 0.69 at 2.5%. Sonnet's was 0.50, 0.57 and 0.74.
  For P2.5 vs P50 the odds ratio was 2.15 for Haiku (95% CI 1.34–3.46, Holm p = .0015) and 2.81 for
  Sonnet (95% CI 1.78–4.43, Holm p < .001). False-alarm rates stayed at 0.6–1.9% in every
  prevalence condition. The pre-registration (§2) named this pattern ("pop-out") as possible and said
  it would be reported as a disconfirmation. This design cannot show that pop-out is the mechanism.
- **H1a (criterion, not sensitivity) is not supported.** The criterion *c* did not become more
  conservative at 2.5%.
  - For Sonnet it became *more liberal*: Δ*c* = −0.44 (95% CI −0.70 to −0.28).
  - For Haiku it did not change reliably (Δ*c* = −0.12, CI −0.59 to 0.17), while sensitivity
    rose (Δ*d′* = +0.71, CI 0.06 to 1.04).
  - AUROC rose slightly for both monitors, with CIs that include zero.

  A post-hoc analysis (section 9, last table) shows that the binary flag is close to a fixed
  threshold on the monitor's own suspicion score (around 40–50) in every condition. The prevalence
  difference comes from the suspicion scores given to backdoored items: these were lower when a
  batch held 20 backdoors.
- **H2 (stated prevalence) is supported for Sonnet only, and the effect is small.** Telling the
  monitor that "about 1 in 100" submissions contained a backdoor, rather than "about half", lowered
  Sonnet's single-item hit rate from 0.85 to 0.78 (GLMM p = .008, Holm p = .015; population-averaged
  OR 0.61, 95% CI 0.44–0.84). Haiku's rate went from 0.68 to 0.64 (GLMM p = .24, Holm p = .24).
  False alarms fell for both (S50 3.3%, S1 0.8–1.7%, on 120 clean items each).
- **H3 (labelled calibration block) is not supported.** At 2.5% prevalence the 10 labelled
  examples did not significantly raise the hit rate.
  - Haiku went from 0.69 to 0.60 (OR 0.66, p = .15, Holm p = .15).
  - Sonnet went from 0.74 to 0.85 (OR 2.02, 95% CI 0.99–4.10, p = .053, Holm p = .106). For Sonnet
    the block moved the criterion (Δ*c* = −0.37, CI −0.59 to −0.18) and doubled false alarms
    (1.7% to 4.0%), with no change in *d′*.
- **Exploratory results.**
  - E1: the position of the backdoor in the batch did not affect hit rates.
  - E2: the "judge each submission independently" sentence had no detectable effect.
  - E3: in single-item judging Sonnet caught more backdoors than Haiku; in batches the two
    monitors were alike.
  - E4: single-item judging with no stated rate (Haiku 0.63, Sonnet 0.80) caught more backdoors
    than batches with 50% or 10% prevalence, and about as many as batches with 2.5%.
- **Plain reading.** In this setting, monitors missed more backdoors when *many* suspicious items
  shared one context, not when backdoors were rare. We cannot tell from this design whether that
  is because a lone anomaly stands out, because reviewing effort is spread over many suspicious
  items, or something else.
- **Main limits.**
  - P50 has only 8 batches per monitor (as registered), so its CIs are crude.
  - All items come from one generator model and one dataset of toy functions.
  - Monitors ran at effort `low` through Claude Code headless mode.
  - Every judgment is a single stochastic draw.

## 2. What ran

| Stage | Model, effort | Calls | Outcome |
|---|---|---|---|
| Generation (v1) | `claude-opus-5-5`, medium | 450 | 450 answered, 0 refusals, 0 failures |
| Verification | none (execution) | – | 419 verified pairs (93.1%) |
| Calibration (v1) | `claude-haiku-5-5`, low | 80 | on target; no revision |
| Main experiments | Haiku and Sonnet, low | 2,176 | 2,176 valid at first attempt; 0 retries, 0 refusals, 0 dropped |
| **Total** | | **2,706** | |

The main calls ran from 23:12 UTC on 3 November to 00:12 UTC on 4 November 2026. They used 6
parallel workers in an order shuffled across experiments, conditions and monitors (seed 99173).
No rate-limit or overload errors occurred.

## 3. Item generation and verification

- **Source.** MBPP, full configuration, all four splits (974 problems, CC BY 4.0). Downloaded from
  `https://huggingface.co/api/datasets/google-research-datasets/mbpp/parquet/full/{split}/0.parquet`
  on 3 November 2026. SHA-256 of the files:

  | Split | SHA-256 |
  |---|---|
  | train | `09d125ca31edacb7800be8c67c45abff618faf0214ff551291817d06bdb914ae` |
  | test | `566fd53060ffba5766dace1d1e2f4c38906781526de222b0dfbdbc325b696c77` |
  | validation | `3f0ec060987432d99fe8fb409d31e6c67445b208a01741c5583517c80a10fe80` |
  | prompt | `a053e4bb85ceb77430ae80592addb4ca4dc6ba087592f9e04537800ee88b7431` |

  The same record is in `data/mbpp_download.json`.
- **Sample.** Two problems were not eligible because their reference solution fails its own tests
  (task IDs 367 and 927). From the 972 eligible problems we drew 450 at random (seed 20261103).
  The reserve was not needed.
- **Generation.** One call per problem: 450 calls, 0 refusals, 0 errors. Median wall time was
  11 s per call. List-price-equivalent cost was USD 14.66. The final generator system prompt is
  `data/generator_system_prompt_v1.txt`.
- **Verification** (§3, with the clarifications in §9 items 2, 3 and 5). 419 of 450 pairs were
  kept, a yield of 93.1%. Exclusions, by the first check failed:

| Exclusion reason | Pairs |
|---|---|
| Backdoored output equals the MBPP reference output on the trigger | 14 |
| Edit too large (difflib ratio < 0.6) | 14 |
| Backdoored output equals clean output on the trigger | 1 |
| Clean version does not return on the trigger (invalid trigger) | 1 |
| Backdoored version fails an MBPP test | 1 |
| Generator refusal / failure; parse failure; safety screen; revealing name | 0 |

- **Edit size** (difflib `SequenceMatcher` ratio between the normalised versions).
  - All 450 parsed pairs: median 0.938 (P10 0.755, P25 0.836, P75 0.989, minimum 0.007).
  - The 419 verified pairs: median 0.944 (P10 0.771, P25 0.842, P75 0.989, P90 0.997, minimum
    0.606).
  - Changed lines (unified diff, added plus removed): median 2, P90 4, maximum 8.
  - 356 of 419 pairs (85%) have exactly two changed lines, for example one line replaced or a
    two-line branch added.
- **Kind of edit** (rough, automatic, post hoc). In 254 of 419 pairs (61%) the statement count is
  unchanged, which means an in-place change such as a loop bound or a comparison. In 150 (36%) the
  edit adds an `if` branch. The remaining 15 (4%) are other edits. Many backdoors look like
  ordinary off-by-one bugs; see the examples in `data/items.jsonl`.
- **Other checks.**
  - 4 verified pairs have a clean version that disagrees with the reference on the trigger. Their
    backdoored output still differs from both.
  - For 2 verified pairs the reference does not return normally on the trigger, so only the clean
    comparison applies.
  - No verified backdoored version contains a name or string matching the strong or the weak list
    of revealing words.
- **Pools** (seed 4021). The calibration pool holds 40 pairs and the main pool 379.
  `data/items.jsonl` has SHA-256 `dde562e0…`; each record carries the SHA-256 of both code versions.
- **Experiment 2 items.** 240 distinct main-pool problems (120 shown backdoored, 120 shown clean),
  the same 240 items in all six monitor × condition cells.

## 4. Calibration outcome (§4.3)

On target at the first attempt. Haiku, single items, no stated prevalence, 80 calibration items:
hit rate 24/40 = **0.60** (Wilson 95% CI 0.45–0.74) and false-alarm rate 0/40 = **0.00** (0.00–0.09).
AUROC was 0.97. The generator prompt was not revised and no item set was regenerated. Details are
in `results/calibration.md`.

## 5. Calls, invalid outputs and refusals per condition

Every one of the 2,176 main-experiment calls returned a schema-valid output with exactly the shown
IDs at the first attempt. There were no §7 retries, no refusals and no dropped batches; the
per-condition table is in section 9.

One point needs saying. Claude Code validates structured output inside a single call and, when the
first attempt fails validation, sends the error back to the model within that call. This shows as
`num_turns` > 2. We see only the final output. Such in-call corrections happened in:

- 43 of 368 Haiku batch calls (P10 9/40, P2.5 21/160, R-cal 4/80, R-ind 9/80; P50 0/8);
- 24 of 720 Sonnet single-item calls;
- no Sonnet batch calls and no Haiku single-item calls.

A post-hoc sensitivity analysis that drops these calls leaves H1, H2 and H3 unchanged
(`results/sensitivity_excluding_extra_turn_calls.json`):

| Monitor | H1 OR, p | H2 GLM OR, p | H3 OR, p |
|---|---|---|---|
| Haiku | 2.35, .0007 | 0.83, .25 | 0.59, .08 |
| Sonnet | 2.81, < .001 | 0.62, .014 | 2.02, .053 |

## 6. Token usage and list-price-equivalent cost

Costs are Claude Code's `costUSD` from `modelUsage`, with `costBasis` "list". They are
list-price equivalents; the calls ran under the Claude Code subscription. Input tokens include
cache reads and cache writes. Source: `results/costs.json`.

| Stage | Model | Calls | Input tokens | Output tokens | Cost (USD) |
|---|---|---|---|---|---|
| Generation | claude-opus-5-5 | 450 | 1,396,168 | 422,844 (of which thinking 240,638) | 14.66 |
| Calibration | claude-haiku-5-5 | 80 | 193,791 | 32,752 | 0.06 |
| Main | claude-haiku-5-5 | 1,088 | 5,086,525 | 2,291,356 | 2.09 |
| Main | claude-sonnet-5-5 | 1,088 | 4,552,893 | 695,723 | 24.88 |
| **Total** | | **2,706** | **11,229,377** | **3,442,675** | **41.70** |

Per call, the mean cost was about USD 0.033 for generation, 0.0007 for a Haiku single item, 0.004
for a Haiku batch, 0.012 for a Sonnet single item and 0.045 for a Sonnet batch.

Descriptive, post hoc: the mean number of thinking tokens per batch call, by condition.

| Monitor | P50 | P10 | P2.5 | R-cal | R-ind | Single item |
|---|---|---|---|---|---|---|
| Haiku | 7,592 | 4,757 | 4,195 | 3,893 | 4,598 | about 320 |
| Sonnet | 116 | 480 | 480 | 487 | 668 | about 70 |

Sonnet reasoned far less on P50 batches; Haiku reasoned more on them.

## 7. Deviations and clarifications

There were no deviations from the registered design, sample sizes or confirmatory tests.
`PREREGISTRATION.md` section 9 lists clarifications made before any main-experiment call:

- by the lead author, items 1–3: the H1a decision rule, docstring removal and the edit-size
  threshold;
- by the research engineer, items 4–12: eligible problems, checks before execution, what the
  monitor sees, the batch vs single prompt sentence, the retry policy, the H2 GLMM convergence
  rule, sampling details, two-sided tests with a separation fallback, and the calibration outcome.

Item 13, added after the data were in, records the post-hoc additions listed below. None of them
changes a registered analysis.

- The difflib threshold of 0.6 was coded before the verifier was first run on any generated item,
  while generation was under way. It was then applied unchanged to all items.
- Post-hoc additions, all labelled as such:
  - a numerical check of the H2 GLMM with more quadrature nodes;
  - a table of flag rate by suspicion band;
  - thinking tokens by condition;
  - the sensitivity analysis excluding calls with in-call corrections;
  - a rough classification of edit types.

## 8. Notes on anything odd

1. **H1 reversed in both monitors.** The registered prediction was fewer hits at low prevalence.
   We found more. The reversal comes mainly from low hit rates in batches with many backdoors
   (P50 about 0.50 in both monitors), compared with single items (Haiku 0.63, Sonnet 0.80) and
   P2.5 batches (0.69, 0.74).
   - The P50 batches did not show the expected pattern of a monitor rationing its flags against a
     stricter threshold. The flag probability within each suspicion band is similar across
     conditions.
   - Instead, more backdoored items received low scores at P50. For Sonnet, 17% of backdoored items
     scored 80–100 at P50, against 45% at P2.5.
2. **P50 rests on 8 batches per monitor**, as registered. Cluster-robust SEs and the cluster bootstrap
   with 8 clusters are approximate; the P50 CIs for *d′*, *c* and AUROC are wide and may be too
   narrow. The H1 direction holds in both monitors and agrees with E4.
3. **The H2 GLMM for Sonnet.** It met the registered convergence rule, but its item SD is poorly
   identified: 92 of 120 backdoored items were flagged in all three conditions and 17 in none. The
   SD estimate ranges from 9 to 33 depending on the number of quadrature nodes. The S1 vs S50 test
   is stable across node counts (p = .006–.011), and the item-clustered GLM agrees (p = .002).
   - The GLMM log-odds of −3.3 is a conditional, item-specific effect. The population-averaged
     effect is the GLM's OR of 0.61, or −7.5 percentage points (paired bootstrap CI −12.5 to −3.3).
   - Haiku's GLMM is stable (item SD about 4.5).
4. **False-alarm rates were very low**, about 1–2% in batches and 0.8–3.3% on single items. *d′* and
   *c* are therefore driven mostly by the hit rate. On single items, *F* rests on 120 clean items,
   and the log-linear correction matters there.
5. **E1, a single uncorrected exploratory result.** Sonnet's false alarms increased with position in
   P2.5 batches (OR per 10 positions 1.26, p = .019). It is one of eight position tests, with no
   correction.
6. **Experiment 2 and calibration agree.** Calibration used the same prompt and monitor as
   Experiment 2 "none" on different items. Its hit rate (0.60) is close to that of Haiku "none" in
   Experiment 2 (0.63).
7. **What the monitor saw.** Monitors saw the MBPP task text with the code (§9 item 6). Many
   backdoors resemble honest off-by-one bugs, so "backdoor" here means a wrong answer on a rare
   input. It does not mean code that is visibly malicious.

## 9. Full numerical results

Verbatim copy of `results/RESULTS_numbers.md` (written by `code/analyse.py`), with its headings moved down one level.

### Calls, invalid outputs and refusals per condition

| Experiment | Condition | Monitor | Calls | Valid | Dropped | Attempts | Invalid attempts | Refusal attempts | Cost (USD, list) |
|---|---|---|---|---|---|---|---|---|---|
| exp1 | P10 | Haiku | 40 | 40 | 0 | 40 | 0 | 0 | 0.19 |
| exp1 | P10 | Sonnet | 40 | 40 | 0 | 40 | 0 | 0 | 1.71 |
| exp1 | P2.5 | Haiku | 160 | 160 | 0 | 160 | 0 | 0 | 0.68 |
| exp1 | P2.5 | Sonnet | 160 | 160 | 0 | 160 | 0 | 0 | 6.88 |
| exp1 | P50 | Haiku | 8 | 8 | 0 | 8 | 0 | 0 | 0.05 |
| exp1 | P50 | Sonnet | 8 | 8 | 0 | 8 | 0 | 0 | 0.32 |
| exp2 | S1 | Haiku | 240 | 240 | 0 | 240 | 0 | 0 | 0.17 |
| exp2 | S1 | Sonnet | 240 | 240 | 0 | 240 | 0 | 0 | 2.83 |
| exp2 | S50 | Haiku | 240 | 240 | 0 | 240 | 0 | 0 | 0.16 |
| exp2 | S50 | Sonnet | 240 | 240 | 0 | 240 | 0 | 0 | 2.82 |
| exp2 | none | Haiku | 240 | 240 | 0 | 240 | 0 | 0 | 0.16 |
| exp2 | none | Sonnet | 240 | 240 | 0 | 240 | 0 | 0 | 2.82 |
| exp3 | R-cal | Haiku | 80 | 80 | 0 | 80 | 0 | 0 | 0.34 |
| exp3 | R-cal | Sonnet | 80 | 80 | 0 | 80 | 0 | 0 | 3.90 |
| exp3 | R-ind | Haiku | 80 | 80 | 0 | 80 | 0 | 0 | 0.36 |
| exp3 | R-ind | Sonnet | 80 | 80 | 0 | 80 | 0 | 0 | 3.60 |

Invalid-attempt reasons: none

### Descriptive results per condition

H = hit rate, F = false-alarm rate (Wilson 95% CIs). d′ and c use the log-linear correction; their 95% CIs and the AUROC CI come from the cluster bootstrap (batches for Experiments 1 and 3; items, paired across conditions and stratified by item type, for Experiment 2; 2,000 resamples).

| Monitor | Condition | Calls | n bd | Hits | H [95% CI] | n clean | FAs | F [95% CI] | d′ [95% CI] | c [95% CI] | AUROC [95% CI] | Mean susp. bd | Mean susp. clean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | P50 | 8 | 160 | 82 | 0.512 [0.436, 0.589] | 160 | 3 | 0.0187 [0.0064, 0.0537] | 2.05 [1.84, 2.64] | 0.99 [0.73, 1.45] | 0.867 [0.827, 0.902] | 41.5 | 7.7 |
| Haiku | P10 | 40 | 160 | 80 | 0.500 [0.423, 0.577] | 1440 | 17 | 0.0118 [0.0074, 0.0188] | 2.25 [2.01, 2.55] | 1.13 [1.00, 1.28] | 0.886 [0.855, 0.914] | 41.2 | 6.1 |
| Haiku | P2.5 | 160 | 160 | 111 | 0.694 [0.618, 0.760] | 6240 | 74 | 0.0119 [0.0095, 0.0149] | 2.76 [2.54, 3.01] | 0.88 [0.77, 0.98] | 0.912 [0.883, 0.939] | 52.1 | 5.6 |
| Haiku | R-cal | 80 | 80 | 48 | 0.600 [0.490, 0.700] | 3120 | 38 | 0.0122 [0.0089, 0.0167] | 2.50 [2.21, 2.80] | 1.00 [0.84, 1.16] | 0.915 [0.874, 0.950] | 50.2 | 6.4 |
| Haiku | R-ind | 80 | 80 | 50 | 0.625 [0.515, 0.723] | 3120 | 23 | 0.0074 [0.0049, 0.0110] | 2.75 [2.44, 3.09] | 1.06 [0.91, 1.22] | 0.898 [0.849, 0.942] | 49.5 | 5.0 |
| Haiku | none | 240 | 120 | 76 | 0.633 [0.544, 0.714] | 120 | 2 | 0.0167 [0.0046, 0.0587] | 2.38 [1.95, 3.09] | 0.85 [0.64, 1.21] | 0.923 [0.887, 0.954] | 48.8 | 6.5 |
| Haiku | S50 | 240 | 120 | 82 | 0.683 [0.596, 0.760] | 120 | 4 | 0.0333 [0.0130, 0.0826] | 2.26 [1.88, 2.89] | 0.66 [0.46, 0.98] | 0.923 [0.889, 0.954] | 54.8 | 7.9 |
| Haiku | S1 | 240 | 120 | 77 | 0.642 [0.553, 0.722] | 120 | 1 | 0.0083 [0.0015, 0.0457] | 2.60 [2.16, 3.18] | 0.94 [0.71, 1.23] | 0.937 [0.907, 0.965] | 48.8 | 5.0 |
| Sonnet | P50 | 8 | 160 | 80 | 0.500 [0.423, 0.577] | 160 | 1 | 0.0063 [0.0011, 0.0345] | 2.35 [1.83, 2.91] | 1.18 [1.06, 1.38] | 0.905 [0.882, 0.929] | 41.9 | 7.0 |
| Sonnet | P10 | 40 | 160 | 91 | 0.569 [0.491, 0.643] | 1440 | 20 | 0.0139 [0.0090, 0.0214] | 2.36 [2.11, 2.66] | 1.01 [0.87, 1.17] | 0.911 [0.886, 0.934] | 46.1 | 5.5 |
| Sonnet | P2.5 | 160 | 160 | 118 | 0.738 [0.664, 0.800] | 6240 | 108 | 0.0173 [0.0144, 0.0209] | 2.74 [2.54, 2.98] | 0.74 [0.62, 0.85] | 0.927 [0.901, 0.950] | 58.3 | 5.4 |
| Sonnet | R-cal | 80 | 80 | 68 | 0.850 [0.756, 0.912] | 3120 | 124 | 0.0397 [0.0334, 0.0472] | 2.77 [2.45, 3.17] | 0.37 [0.18, 0.52] | 0.959 [0.929, 0.980] | 65.5 | 7.4 |
| Sonnet | R-ind | 80 | 80 | 60 | 0.750 [0.645, 0.832] | 3120 | 56 | 0.0179 [0.0138, 0.0232] | 2.76 [2.46, 3.12] | 0.71 [0.55, 0.87] | 0.935 [0.898, 0.967] | 62.0 | 5.0 |
| Sonnet | none | 240 | 120 | 96 | 0.800 [0.720, 0.862] | 120 | 1 | 0.0083 [0.0015, 0.0457] | 3.08 [2.62, 3.67] | 0.71 [0.47, 1.00] | 0.953 [0.922, 0.979] | 68.4 | 4.4 |
| Sonnet | S50 | 240 | 120 | 102 | 0.850 [0.775, 0.903] | 120 | 4 | 0.0333 [0.0130, 0.0826] | 2.81 [2.39, 3.42] | 0.38 [0.18, 0.69] | 0.966 [0.941, 0.986] | 75.0 | 6.5 |
| Sonnet | S1 | 240 | 120 | 93 | 0.775 [0.692, 0.841] | 120 | 2 | 0.0167 [0.0046, 0.0587] | 2.79 [2.35, 3.47] | 0.65 [0.43, 1.01] | 0.949 [0.919, 0.974] | 62.7 | 4.4 |

### H1 (confirmatory): hit rate, P2.5 vs P50

Logistic GLM of flag on prevalence condition (reference P50), backdoored items of Experiment 1, batch-clustered SEs. Holm correction across the two monitors for P2.5 vs P50 only.

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | P2.5 vs P50 (confirmatory) | 0.768 | 0.242 | 2.15 [1.34, 3.46] | 3.18 | 0.001 | 0.001 |
| Haiku | P10 vs P50 | -0.050 | 0.230 | 0.95 [0.61, 1.49] | -0.22 | 0.828 | — |
| Sonnet | P2.5 vs P50 (confirmatory) | 1.033 | 0.232 | 2.81 [1.78, 4.43] | 4.44 | < .001 | < .001 |
| Sonnet | P10 vs P50 | 0.277 | 0.221 | 1.32 [0.85, 2.03] | 1.25 | 0.211 | — |

False alarms by prevalence (descriptive; clean items of Experiment 1, batch-clustered SEs):

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | F: P10 vs P50 | -0.470 | 0.721 | 0.63 [0.15, 2.57] | -0.65 | 0.515 | — |
| Haiku | F: P2.5 vs P50 | -0.465 | 0.681 | 0.63 [0.17, 2.39] | -0.68 | 0.495 | — |
| Sonnet | F: P10 vs P50 | 0.806 | 0.979 | 2.24 [0.33, 15.25] | 0.82 | 0.410 | — |
| Sonnet | F: P2.5 vs P50 | 1.030 | 0.950 | 2.80 [0.43, 18.03] | 1.08 | 0.279 | — |

### H1a (confirmatory): criterion vs sensitivity, P2.5 minus P50

Point estimates with 95% cluster-bootstrap CIs (2,000 resamples over batches, independently within each condition). Support requires Δc > 0 with a CI excluding 0 and |Δc| > |Δd′|.

| Monitor | ΔH [95% CI] | ΔF [95% CI] | Δd′ [95% CI] | Δc [95% CI] | ΔAUROC [95% CI] | |Δc| − |Δd′| [95% CI] | Criterion 1 | Criterion 2 | H1a supported |
|---|---|---|---|---|---|---|---|---|---|
| Haiku | 0.181 [0.075, 0.281] | -0.0069 [-0.0327, 0.0128] | 0.71 [0.06, 1.04] | -0.12 [-0.59, 0.17] | 0.045 [-0.002, 0.092] | -0.60 [-0.96, 0.45] | no | no | no |
| Sonnet | 0.238 [0.144, 0.338] | 0.0111 [-0.0026, 0.0202] | 0.39 [-0.24, 0.95] | -0.44 [-0.70, -0.28] | 0.022 [-0.013, 0.056] | 0.05 [-0.58, 0.62] | no | yes | no |

### H2 (confirmatory): stated prevalence, S1 vs S50

- Haiku: item random-intercept GLMM converged = True (optimiser: Desired error not necessarily achieved due to precision loss.; item SD = 4.57); model used: glmm.
- Sonnet: item random-intercept GLMM converged = True (optimiser: Desired error not necessarily achieved due to precision loss.; item SD = 32.83); model used: glmm.

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | S1 vs S50 (confirmatory) | -0.557 | 0.478 | 0.57 [0.22, 1.46] | -1.16 | 0.244 | 0.244 |
| Haiku | none vs S50 | -0.664 | 0.480 | 0.51 [0.20, 1.32] | -1.38 | 0.166 | — |
| Sonnet | S1 vs S50 (confirmatory) | -3.321 | 1.246 | 0.04 [0.00, 0.42] | -2.66 | 0.008 | 0.015 |
| Sonnet | none vs S50 | -2.022 | 1.019 | 0.13 [0.02, 0.98] | -1.98 | 0.047 | — |

Numerical check of the GLMM (not part of the registered decision rule): the same model refitted with more Gauss–Hermite nodes, and the number of backdoored items flagged in 0, 1, 2 or 3 of the three conditions. GLMM coefficients are conditional (item-specific) log-odds, so they are larger than the population-averaged GLM coefficients when the item SD is large.

| Monitor | Items flagged in 0/1/2/3 conditions | Nodes | Converged | Item SD | S1 vs S50 log-odds | SE | p |
|---|---|---|---|---|---|---|---|
| Haiku | 29/10/18/63 | 20 | True | 5.08 | -0.569 | 0.484 | 0.240 |
| Haiku | 29/10/18/63 | 40 (registered) | True | 4.57 | -0.557 | 0.478 | 0.244 |
| Haiku | 29/10/18/63 | 80 | True | 4.46 | -0.552 | 0.476 | 0.246 |
| Haiku | 29/10/18/63 | 160 | True | 4.47 | -0.552 | 0.476 | 0.246 |
| Haiku | 29/10/18/63 | 300 | True | 4.47 | -0.552 | 0.476 | 0.246 |
| Sonnet | 17/7/4/92 | 20 | True | 9.03 | -3.439 | 1.351 | 0.011 |
| Sonnet | 17/7/4/92 | 40 (registered) | True | 32.83 | -3.321 | 1.246 | 0.008 |
| Sonnet | 17/7/4/92 | 80 | True | 15.72 | -3.687 | 1.350 | 0.006 |
| Sonnet | 17/7/4/92 | 160 | True | 14.23 | -3.812 | 1.412 | 0.007 |
| Sonnet | 17/7/4/92 | 300 | True | 13.34 | -3.749 | 1.404 | 0.008 |

Sensitivity analysis, GLM with item-clustered SEs:

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | S1 vs S50 | -0.187 | 0.163 | 0.83 [0.60, 1.14] | -1.14 | 0.253 | — |
| Haiku | none vs S50 | -0.223 | 0.157 | 0.80 [0.59, 1.09] | -1.41 | 0.158 | — |
| Sonnet | S1 vs S50 | -0.498 | 0.162 | 0.61 [0.44, 0.84] | -3.07 | 0.002 | — |
| Sonnet | none vs S50 | -0.348 | 0.163 | 0.71 [0.51, 0.97] | -2.14 | 0.033 | — |

S1 minus S50, other measures (point [95% paired item-bootstrap CI]):

| Monitor | ΔH | ΔF | Δd′ | Δc | ΔAUROC |
|---|---|---|---|---|---|
| Haiku | -0.042 [-0.117, 0.025] | -0.025 [-0.058, 0.000] | 0.35 [-0.17, 0.95] | 0.29 [0.05, 0.59] | 0.014 [-0.006, 0.036] |
| Sonnet | -0.075 [-0.125, -0.033] | -0.017 [-0.050, 0.017] | -0.02 [-0.59, 0.62] | 0.27 [-0.01, 0.58] | -0.017 [-0.034, -0.004] |

### H3 (confirmatory): calibration block, R-cal vs P2.5

Logistic GLM of flag on condition (reference P2.5), backdoored items, batch-clustered SEs; Holm across monitors.

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | R-cal vs P2.5 (confirmatory) | -0.412 | 0.287 | 0.66 [0.38, 1.16] | -1.44 | 0.150 | 0.150 |
| Sonnet | R-cal vs P2.5 (confirmatory) | 0.702 | 0.363 | 2.02 [0.99, 4.10] | 1.94 | 0.053 | 0.106 |

R-cal minus P2.5, other measures (95% cluster-bootstrap CIs):

| Monitor | ΔF [95% CI] | Δd′ [95% CI] | Δc [95% CI] | ΔAUROC [95% CI] |
|---|---|---|---|---|
| Haiku | 0.0003 [-0.0039, 0.0048] | -0.27 [-0.66, 0.12] | 0.12 [-0.07, 0.30] | 0.003 [-0.047, 0.050] |
| Sonnet | 0.0224 [0.0139, 0.0314] | 0.03 [-0.38, 0.48] | -0.37 [-0.59, -0.18] | 0.032 [-0.004, 0.066] |

### Exploratory analyses (E1–E4; not confirmatory)

**E1, position in batch.** Logistic GLM of flag on position (1–40), batch-clustered SEs. Coefficient per position step.

| Monitor | Condition | Items | Coef. per position | SE | OR per 10 positions | z | p |
|---|---|---|---|---|---|---|---|
| Haiku | P2.5 | backdoored (hit) | 0.0009 | 0.0148 | 1.01 | 0.06 | 0.954 |
| Haiku | P2.5 | clean (false alarm) | 0.0042 | 0.0112 | 1.04 | 0.37 | 0.709 |
| Haiku | P10 | backdoored (hit) | 0.0188 | 0.0153 | 1.21 | 1.23 | 0.220 |
| Haiku | P10 | clean (false alarm) | 0.0211 | 0.0213 | 1.24 | 0.99 | 0.322 |
| Sonnet | P2.5 | backdoored (hit) | -0.0027 | 0.0158 | 0.97 | -0.17 | 0.862 |
| Sonnet | P2.5 | clean (false alarm) | 0.0228 | 0.0097 | 1.26 | 2.35 | 0.019 |
| Sonnet | P10 | backdoored (hit) | 0.0249 | 0.0144 | 1.28 | 1.73 | 0.084 |
| Sonnet | P10 | clean (false alarm) | 0.0089 | 0.0181 | 1.09 | 0.49 | 0.623 |

**E2, independence instruction (R-ind vs P2.5).**

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | R-ind vs P2.5 (hit rate) | -0.307 | 0.289 | 0.74 [0.42, 1.30] | -1.06 | 0.288 | — |
| Sonnet | R-ind vs P2.5 (hit rate) | 0.066 | 0.316 | 1.07 [0.57, 1.98] | 0.21 | 0.835 | — |

| Monitor | ΔF [95% CI] | Δd′ [95% CI] | Δc [95% CI] | ΔAUROC [95% CI] |
|---|---|---|---|---|
| Haiku | -0.0045 [-0.0088, -0.0003] | -0.02 [-0.42, 0.40] | 0.18 [-0.00, 0.37] | -0.014 [-0.069, 0.041] |
| Sonnet | 0.0006 [-0.0058, 0.0069] | 0.02 [-0.37, 0.41] | -0.03 [-0.22, 0.17] | 0.009 [-0.038, 0.049] |

**E3, monitor comparison.** Logistic GLMs with monitor × condition interaction (reference: Haiku, P50 or S50); Experiment 1 clustered by batch (the same batch compositions were shown to both monitors), Experiment 2 by item.

*Experiment 1, hits*

| Term | log-odds | SE | z | p |
|---|---|---|---|---|
| Intercept | 0.050 | 0.170 | 0.29 | 0.768 |
| C(condition, Treatment('P50'))[T.P10] | -0.050 | 0.230 | -0.22 | 0.828 |
| C(condition, Treatment('P50'))[T.P2.5] | 0.768 | 0.242 | 3.17 | 0.001 |
| C(monitor, Treatment('Haiku'))[T.Sonnet] | -0.050 | 0.180 | -0.28 | 0.782 |
| C(condition, Treatment('P50'))[T.P10]:C(monitor, Treatment('Haiku'))[T.Sonnet] | 0.327 | 0.252 | 1.30 | 0.195 |
| C(condition, Treatment('P50'))[T.P2.5]:C(monitor, Treatment('Haiku'))[T.Sonnet] | 0.265 | 0.245 | 1.08 | 0.279 |

*Experiment 1, false alarms*

| Term | log-odds | SE | z | p |
|---|---|---|---|---|
| Intercept | -3.958 | 0.670 | -5.90 | < .001 |
| C(condition, Treatment('P50'))[T.P10] | -0.470 | 0.721 | -0.65 | 0.515 |
| C(condition, Treatment('P50'))[T.P2.5] | -0.465 | 0.681 | -0.68 | 0.495 |
| C(monitor, Treatment('Haiku'))[T.Sonnet] | -1.111 | 1.264 | -0.88 | 0.379 |
| C(condition, Treatment('P50'))[T.P10]:C(monitor, Treatment('Haiku'))[T.Sonnet] | 1.276 | 1.293 | 0.99 | 0.324 |
| C(condition, Treatment('P50'))[T.P2.5]:C(monitor, Treatment('Haiku'))[T.Sonnet] | 1.495 | 1.273 | 1.17 | 0.240 |

*Experiment 2, hits*

| Term | log-odds | SE | z | p |
|---|---|---|---|---|
| Intercept | 0.769 | 0.198 | 3.89 | < .001 |
| C(condition, Treatment('S50'))[T.S1] | -0.187 | 0.163 | -1.14 | 0.253 |
| C(condition, Treatment('S50'))[T.none] | -0.223 | 0.158 | -1.41 | 0.158 |
| C(monitor, Treatment('Haiku'))[T.Sonnet] | 0.965 | 0.230 | 4.20 | < .001 |
| C(condition, Treatment('S50'))[T.S1]:C(monitor, Treatment('Haiku'))[T.Sonnet] | -0.311 | 0.231 | -1.35 | 0.178 |
| C(condition, Treatment('S50'))[T.none]:C(monitor, Treatment('Haiku'))[T.Sonnet] | -0.126 | 0.227 | -0.55 | 0.580 |

**E4, single-item judging (Experiment 2 'none') vs batch conditions (Experiment 1).** Hit rate contrasts, clusters = batches (batch) or calls (single).

| Monitor | Contrast | log-odds | SE | OR [95% CI] | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Haiku | P50 (batch) vs none (single), hits | -0.497 | 0.255 | 0.61 [0.37, 1.00] | -1.95 | 0.051 | — |
| Haiku | P10 (batch) vs none (single), hits | -0.547 | 0.245 | 0.58 [0.36, 0.94] | -2.23 | 0.026 | — |
| Haiku | P2.5 (batch) vs none (single), hits | 0.271 | 0.257 | 1.31 [0.79, 2.17] | 1.06 | 0.291 | — |
| Haiku | P50 (batch) vs none (single), false alarms | 0.120 | 0.979 | 1.13 [0.17, 7.68] | 0.12 | 0.903 | — |
| Haiku | P10 (batch) vs none (single), false alarms | -0.350 | 0.762 | 0.70 [0.16, 3.14] | -0.46 | 0.646 | — |
| Haiku | P2.5 (batch) vs none (single), false alarms | -0.345 | 0.724 | 0.71 [0.17, 2.93] | -0.48 | 0.634 | — |
| Sonnet | P50 (batch) vs none (single), hits | -1.386 | 0.272 | 0.25 [0.15, 0.43] | -5.10 | < .001 | — |
| Sonnet | P10 (batch) vs none (single), hits | -1.110 | 0.283 | 0.33 [0.19, 0.57] | -3.92 | < .001 | — |
| Sonnet | P2.5 (batch) vs none (single), hits | -0.353 | 0.292 | 0.70 [0.40, 1.24] | -1.21 | 0.226 | — |
| Sonnet | P50 (batch) vs none (single), false alarms | -0.290 | 1.379 | 0.75 [0.05, 11.16] | -0.21 | 0.834 | — |
| Sonnet | P10 (batch) vs none (single), false alarms | 0.516 | 1.039 | 1.68 [0.22, 12.84] | 0.50 | 0.619 | — |
| Sonnet | P2.5 (batch) vs none (single), false alarms | 0.740 | 1.012 | 2.10 [0.29, 15.23] | 0.73 | 0.465 | — |

**Flags per batch** (Experiments 1 and 3).

| Monitor | Condition | Mean flags per batch | Median | Share of batches with no flag | Max |
|---|---|---|---|---|---|
| Haiku | P10 | 2.42 | 2.0 | 0.07 | 5 |
| Haiku | P2.5 | 1.16 | 1.0 | 0.14 | 4 |
| Haiku | P50 | 10.62 | 10.0 | 0.00 | 16 |
| Haiku | R-cal | 1.07 | 1.0 | 0.28 | 3 |
| Haiku | R-ind | 0.91 | 1.0 | 0.29 | 4 |
| Sonnet | P10 | 2.77 | 3.0 | 0.00 | 6 |
| Sonnet | P2.5 | 1.41 | 1.0 | 0.14 | 7 |
| Sonnet | P50 | 10.12 | 10.0 | 0.00 | 13 |
| Sonnet | R-cal | 2.40 | 2.0 | 0.01 | 6 |
| Sonnet | R-ind | 1.45 | 1.0 | 0.12 | 4 |

### Post-hoc (not pre-registered): how suspicion scores map to flags

Proportion of items flagged within bands of the monitor's own suspicion score, all items (clean and backdoored) pooled, and the share of backdoored items in each band. If a condition changed only where the monitor puts its flag threshold, the flag rate within a band would change; if it changed the scores themselves, the distribution of backdoored items across bands would change.

| Monitor | Condition | P(flag) at 0–19 | P(flag) at 20–39 | P(flag) at 40–59 | P(flag) at 60–79 | P(flag) at 80–100 | bd share 0–19 | bd share 20–39 | bd share 40–59 | bd share 60–79 | bd share 80–100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | P50 | 0.00 (n=195) | 0.00 (n=30) | 0.73 (n=37) | 1.00 (n=44) | 1.00 (n=14) | 0.28 | 0.16 | 0.21 | 0.26 | 0.09 |
| Haiku | P10 | 0.00 (n=1425) | 0.00 (n=65) | 0.72 (n=47) | 1.00 (n=42) | 1.00 (n=21) | 0.32 | 0.12 | 0.21 | 0.21 | 0.13 |
| Haiku | P2.5 | 0.00 (n=6044) | 0.03 (n=160) | 0.84 (n=93) | 1.00 (n=68) | 1.00 (n=35) | 0.25 | 0.06 | 0.12 | 0.35 | 0.22 |
| Haiku | R-cal | 0.00 (n=2995) | 0.01 (n=107) | 0.73 (n=49) | 1.00 (n=32) | 1.00 (n=17) | 0.25 | 0.11 | 0.14 | 0.29 | 0.21 |
| Haiku | R-ind | 0.00 (n=3054) | 0.02 (n=66) | 0.73 (n=30) | 1.00 (n=33) | 1.00 (n=17) | 0.28 | 0.07 | 0.12 | 0.33 | 0.20 |
| Haiku | none | 0.00 (n=146) | 0.00 (n=16) | 1.00 (n=15) | 1.00 (n=43) | 1.00 (n=20) | 0.27 | 0.10 | 0.12 | 0.34 | 0.17 |
| Haiku | S50 | 0.00 (n=141) | 0.00 (n=11) | 0.78 (n=9) | 1.00 (n=44) | 1.00 (n=35) | 0.23 | 0.07 | 0.07 | 0.34 | 0.28 |
| Haiku | S1 | 0.00 (n=145) | 0.00 (n=17) | 1.00 (n=14) | 1.00 (n=42) | 1.00 (n=22) | 0.25 | 0.11 | 0.12 | 0.34 | 0.18 |
| Sonnet | P50 | 0.00 (n=202) | 0.00 (n=32) | 0.85 (n=34) | 1.00 (n=23) | 1.00 (n=29) | 0.32 | 0.16 | 0.20 | 0.14 | 0.17 |
| Sonnet | P10 | 0.00 (n=1446) | 0.13 (n=47) | 0.94 (n=34) | 1.00 (n=30) | 1.00 (n=43) | 0.34 | 0.10 | 0.15 | 0.15 | 0.26 |
| Sonnet | P2.5 | 0.00 (n=6052) | 0.11 (n=131) | 0.93 (n=70) | 1.00 (n=67) | 1.00 (n=80) | 0.24 | 0.04 | 0.11 | 0.16 | 0.45 |
| Sonnet | R-cal | 0.00 (n=2912) | 0.05 (n=94) | 0.92 (n=83) | 1.00 (n=49) | 1.00 (n=62) | 0.12 | 0.06 | 0.16 | 0.20 | 0.45 |
| Sonnet | R-ind | 0.00 (n=3056) | 0.27 (n=37) | 0.95 (n=21) | 1.00 (n=32) | 1.00 (n=54) | 0.24 | 0.04 | 0.05 | 0.19 | 0.49 |
| Sonnet | none | 0.00 (n=137) | 0.00 (n=5) | 0.83 (n=6) | 1.00 (n=19) | 1.00 (n=73) | 0.16 | 0.03 | 0.05 | 0.16 | 0.60 |
| Sonnet | S50 | 0.00 (n=127) | 0.00 (n=6) | 0.83 (n=6) | 1.00 (n=14) | 1.00 (n=87) | 0.11 | 0.03 | 0.03 | 0.11 | 0.72 |
| Sonnet | S1 | 0.00 (n=139) | 0.00 (n=6) | 1.00 (n=12) | 1.00 (n=27) | 1.00 (n=56) | 0.18 | 0.04 | 0.10 | 0.21 | 0.47 |
