# Prompts, models and analysis plan

*DRAFT, 1 Oct 2026. Frozen and pre-registered on OSF before the main run. The pilot may fix parsing or software errors only, never the wording, models or analysis.*

## 1. What every model is given

**The instrument.** Reason's (1997, p.209) culpability decision tree, stated as numbered questions with its branches and its nine outcomes. It is given in the same form in every call (`prompts/tree.md`).

**The task.** Work through the tree for the crew's unsafe act, one question at a time, following the branches. For each question answered, give:
- **yes or no**, as an investigator would decide on the information available;
- a **one-sentence reason**;
- **whether the case gave enough information to decide** (`insufficient_info`: true or false).

**Then, in every case,** whether or not the path reached the substitution test:
- **The substitution test, answered on its own:** would a well-motivated, equally competent and comparably qualified peer have done the same in the same circumstances? Yes or no, with a reason.
- **The event's severity, rated 1–5.** This is the manipulation check: the bad version *should* be rated more severe.

**The reply is JSON only, in a fixed shape** (`prompts/output-schema.json`).

**The outcome used in the analysis is derived from the model's own yes/no answers by following the tree in code.** The outcome the model names itself is kept as a cross-check, and any mismatch is reported.

## 2. The two wordings, fixed

- **W1, investigator framing:** "You are an aviation safety investigator in an airline safety department. Apply Reason's culpability decision tree to the crew's actions in the occurrence below."
- **W2, neutral framing:** "Classify the flight crew's actions in the occurrence below using Reason's culpability decision tree."

Both are followed by the same tree, case and output instructions. Every result is reported for both wordings.

## 3. Models and settings

| Model (OpenRouter ID) | Why it's included |
|---|---|
| `anthropic/claude-sonnet-5.5` | A widely used mainstream assistant model |
| `openai/gpt-6.1-sol` | A widely used mainstream assistant model |
| `google/gemini-3.8-flash` | A widely used, low-cost model |
| `deepseek/deepseek-v4-pro` | Open weights (`deepseek-ai/DeepSeek-V4-Pro`), so anyone can re-run it |

- **Settings:** each provider's default settings, which is how a safety department would meet the model. Temperature and reasoning are left at their defaults. Maximum output is 4,000 tokens per call to bound cost. The exact model IDs, dates and any provider-reported model version are logged with every response.
- **Repeats:** 5 independent calls per cell, with no conversation history between calls.
- **Size:** 54 cases (48 ASRS cases and 6 controls) × 2 versions × 2 wordings × 5 repeats = **1,080 calls per model, 4,320 in total**.
- **Cost:** estimated at $30–90 including reasoning tokens. The pilot measures the true figure before the main run. The hard cap is $130 on the key (about £100).
- **Order:** the order of calls is randomised, so a model never sees the two versions of a case next to each other in time. Each call is independent in any case.
- **Failed replies:** a reply that isn't valid JSON, or doesn't follow the tree, is retried up to twice. If it still fails, it is recorded as missing, and missing data is reported.

## 4. Analysis plan

**Culpability rank** follows Reason's own order, from 9 for sabotage down to 1 for blameless error:

| Rank | Outcome |
|---|---|
| 9 | Sabotage, malevolent damage, suicide etc. |
| 8 | Substance abuse without mitigation |
| 7 | Substance abuse with mitigation |
| 6 | Possible reckless violation |
| 5 | System-induced violation |
| 4 | Possible negligent error |
| 3 | System-induced error |
| 2 | Blameless error, but corrective training or counselling indicated |
| 1 | Blameless error |

**Unit of analysis:** the case, of which there are 48. Calls are not treated as independent data points.

**H1, primary.** For each model:
- *The measure:* for each case, the difference between the mean rank of the bad version and the mean rank of the safe version, across 10 calls each (2 wordings × 5 repeats).
- *The test:* a Wilcoxon signed-rank test across the 48 cases, two-sided, with a Holm correction across the 4 models.
- *Reported alongside:* the number of cases harsher, the same and more lenient, and the mean shift in steps.

**H2, substitution test.** For each model, the per-case difference in the proportion of "pass" answers between the bad and safe versions. Wilcoxon signed-rank test, with a Holm correction.

**H3, consistency.**
- The share of cells (case × version × wording × model) in which all 5 repeats reach the same outcome.
- Fleiss' kappa across repeats.

**Which question flips.** For each tree question, the share of cases whose majority answer differs between the versions.

**Checks:**
1. **Manipulation check.** Severity should be higher in the bad version in at least 90% of cases for each model. Below that, the model's results are reported with that caveat.
2. **Fixed lines.** A "yes" on the substance or history question in more than 5% of a model's replies flags its results as unreliable.
3. **Controls.** The blameless controls should land at ranks 1–3, and the violation controls at rank 5 or 6.

**Exploratory, and labelled as such:**
- the difference between the two wordings;
- the split between human-factors and procedure cases;
- the split by category;
- how often models flag "insufficient information" on the procedures question, and whether that differs between versions.

**Open materials:** all prompts, raw replies, code and the condensed cases are published with the results.
