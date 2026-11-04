# OSF pre-registration — draft for James to submit

*Drafted by Claude, 1 Oct 2026. Each section below maps to a field in OSF's standard "OSF Preregistration" template. Copy each one into the matching field.*

*Before submitting:*
1. *Read and approve the 48 cases and the 6 controls.*
2. *Claude then fills in the commit hash of the frozen materials (marked `7260f7bd4ede` (git tag `materials-frozen-2026-10-01`)).*
3. *Attach the materials bundle (listed at the end).*
4. *Choose an embargo, so the registration is time-stamped now but stays private until publication.*

---

## Title

Same Actions, Different Endings: Does Outcome Severity Change How AI Models Apply Reason's Culpability Decision Tree to Aviation Flight Crews?

## Description

Just culture holds that people should be judged on what they knew and did at the time, not on how events turned out. AI models are increasingly used to help triage and analyse aviation safety reports. This study tests whether general-purpose AI models judge identical crew actions as more culpable when an occurrence ends badly than when it ends safely.

**Materials.** 48 occurrences were drawn by a pre-specified random rule from NASA's public Aviation Safety Reporting System (ASRS) for 2025, and condensed to a fixed template. Each exists in two versions that are word for word identical except for the outcome: the safe ending as reported, or a standard, plausible bad ending of fixed wording.

**Procedure.** Four AI models apply James Reason's (1997) culpability decision tree to each version, independently, under two fixed prompt wordings, five times each.

**The question.** Whether the culpability outcome they reach shifts with the ending.

## Hypotheses

- **H1 (primary).** For identical crew actions, AI models reach a more culpable outcome on Reason's tree when the occurrence ends badly than when it ends safely. *Null:* outcome severity makes no difference.
- **H2.** When the occurrence ends badly, the models are less likely to judge that the crew pass the substitution test (whether a comparable peer would have done the same). *Null:* no difference.
- **H3.** Given the same version of the same case, a model does not always reach the same outcome across repeated runs. *Null:* outcomes are identical across repeats.

H1 and H2 are tested two-sided. A direction (harsher when the ending is bad) is expected from research on outcome bias in people, and on hindsight and outcome biases in AI models in other fields.

## Study type

Experiment: a manipulated variable, the outcome text, within each case, with AI models as the subjects. There are no human participants.

## Blinding

- **The models:** each call is independent, with no conversation history, so a model never sees both versions of a case.
- **The authors:** all materials (cases, endings, prompts, analysis script) are frozen at commit `7260f7bd4ede` (git tag `materials-frozen-2026-10-01`) before any model response is collected. James's read of the cases for realism took place before any results existed.

## Study design

Within-case matched pairs. The factors are:
- **outcome:** safe or bad (the manipulation);
- **prompt wording:** W1 (investigator framing) or W2 (neutral framing);
- **model:** 4 models;
- **repeat:** 1–5.

48 main cases, plus 6 control cases written by the author with clear-cut intended answers (3 blameless errors, 3 reckless violations), plus 2 pilot cases used only to test the software.

## Randomisation

- **Case selection:** a seeded random order within each event category, using `random.Random(20261001)`, with screening in that order.
- **Neutral case IDs:** assigned in a seeded random order (seed 20261003).
- **Call order:** shuffled with seed 20261002, so the two versions of a case are not sent next to each other.

## Existing data

Registration before any model response has been collected.

The stimuli were built from public ASRS reports, exported on 1 Oct 2026: 761 reports matching the search below. No model has been run on the materials, apart from the 2 pilot cases, which are excluded from all analysis.

## Explanation of existing data

**The ASRS search:**
- incidents dated January–December 2025;
- FAR Part 121;
- reporter function: flight crew;
- primary problem: Human Factors or Procedure;
- event types: altitude, track or heading and speed deviations; ground incursion; inflight event or encounter; airspace violation; procedural deviation.

**What came out of it:**
- 234 reports were screened against six written criteria. The 48 main cases are 8 unstabilised approaches, 6 runway incursions, 20 altitude deviations, 8 track or heading deviations, and 6 other deviations from an ATC clearance or restriction.
- Every screening decision is logged.
- **Departures from the plan before registration (D1–D7):**
  - the airspace-violation category held only drone encounters and produced no cases;
  - the runway-incursion category ran short;
  - a TCAS height rule was clarified;
  - a safe-ending sentence was adjusted for truthfulness;
  - a minimum-length guide was relaxed for short reports;
  - one safe ending was trimmed;
  - four cases were excluded by written rules and replaced.

  All are documented in `protocol/deviations.md`, and all were made before any model ran.

## Data collection procedures

**The models,** via OpenRouter, with each provider's default settings and a maximum of 4,000 output tokens:
- `anthropic/claude-sonnet-5.5`
- `openai/gpt-6.1-sol`
- `google/gemini-3.8-flash`
- `deepseek/deepseek-v4-pro` (open weights)

**What each call contains:** one prompt with the wording, Reason's tree (`prompts/tree.md`), the case (shared text, then "Outcome:" and one ending), two fixed lines, and the response instructions (`prompts/instructions.md`).

**The fixed lines:**
- "There is no indication of alcohol, drugs or a medical condition affecting either pilot."
- "No previous safety events are recorded for this crew."

**The model's reply,** in JSON:
- a yes or no for each tree question on its path, with a reason and an "insufficient information" flag;
- an outcome;
- a separate substitution-test answer;
- a severity rating from 1 to 5.

**Logging and retries:** every reply is logged with the provider-reported model version, the token usage and the cost. Invalid replies are retried up to twice.

## Sample size

48 main cases × 2 outcomes × 2 wordings × 5 repeats × 4 models = 3,840 calls. Plus the controls, 6 × 2 × 2 × 5 × 4 = 480 calls.

## Sample size rationale

The number of cases was set by the qualifying pool in one year of ASRS data under the pre-specified rule.

**Power, by normal approximation.** With 48 paired cases:
- at α = .05, two-sided, a signed-rank test has about 80% power to detect a standardised paired effect of about 0.4;
- at the strictest Holm threshold across four models (α = .0125), about 0.5.

## Stopping rule

Every planned call is made once, with up to 2 retries for invalid replies. The run stops early only if spending reaches the cap of USD 130. A stop is reported, along with how many calls were missed.

## Manipulated variables

**Outcome:**
- **Safe:** the report's own outcome.
- **Bad:** one of three fixed endings, all of similar severity (minor injuries; at most slight damage):
  - runway excursion;
  - runway conflict (departing or landing traffic variant);
  - loss of separation with TCAS resolution advisories.

**Secondary factor:** prompt wording, W1 or W2.

## Measured variables

1. **The culpability outcome, derived in code** from the model's own yes/no answers through Reason's tree. The outcome the model names itself is kept as a cross-check.
2. **The separate substitution-test answer** (yes or no).
3. **Severity** (1–5): the manipulation check.
4. **The yes/no answer to each tree question,** and its "insufficient information" flag.

## Indices

**Culpability rank,** in Reason's (1997) order from most to least culpable:

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

**The per-case outcome effect:** the mean rank in the bad version minus the mean rank in the safe version, over 10 calls each (2 wordings × 5 repeats), for each model.

## Statistical models

- **How the tests are computed:** in plain Python with no third-party libraries (`scripts/stats.py`). The Wilcoxon signed-rank test drops zero differences (Wilcoxon's method), averages tied ranks, and takes its two-sided p from the normal approximation with a tie-corrected variance. The whole analysis (`scripts/07_analyse.py`) was written and tested on simulated data (`results/sim/`) before any real response existed.
- **H1:** for each model, a Wilcoxon signed-rank test of the per-case difference across the 48 cases, two-sided, with a Holm correction across the 4 models. Also reported: the number of cases harsher, the same and more lenient, and the mean shift in steps.
- **H2:** for each model, a Wilcoxon signed-rank test on the per-case difference in the proportion of "pass" answers, with a Holm correction.
- **H3:**
  - the share of cells (case × version × wording × model) in which all 5 repeats reach the same outcome;
  - Fleiss' kappa across repeats.
- **Which question flips:** for each tree question, the share of cases whose majority answer differs between versions.

## Transformations

None beyond the rank mapping and the per-case means above.

## Inference criteria

α = .05, two-sided, after Holm correction across the four models. Effect sizes are reported with 95% confidence intervals (bootstrap over cases), whatever the significance.

## Data exclusion

- **Pilot cases** are excluded from all analysis.
- **Control cases** are reported separately, and never pooled into H1–H3.
- **The manipulation check.** If a model rates the bad version as more severe in fewer than 90% of cases, its results are reported with that caveat.
- **The fixed-line check.** If more than 5% of a model's replies answer "yes" to the substance or history question, its results are flagged as unreliable.

## Missing data

A call that still has no valid reply after 3 attempts is missing. Per-case means use the calls available. A case missing all calls in either version, for a given model, is dropped from that model's H1 test, and this is reported.

## Exploratory analysis

Labelled as exploratory:
- the effect by prompt wording;
- the effect by event category;
- the effect for human-factors against procedure cases;
- the "insufficient information" flags on the procedures question, by version;
- the controls' behaviour, including any shift between versions;
- agreement between the derived outcome and the outcome the model names itself;
- how often a model's reasons remark that the ending seems implausible or inconsistent, by version. The bad endings are fixed text, the same for every case of a type, so this checks whether any model treats them as odd. Each model sees only one case per call, so it never sees the repetition across cases.

## Other

**Conflict of interest.** The author's company, CitadelAero, builds AI tools for aviation safety and compliance teams. To manage this:
- no CitadelAero product is tested;
- results are published whichever way they come out;
- claims are limited to the models and conditions tested.

**AI assistance.**
- The cases were condensed from the reports by Claude models working to a fixed written brief, and checked by the author. One of the models tested is a Claude model; this is stated as a limitation.
- Claude also assisted with the protocol and the code.

**Materials** (attached; also in the study repository at commit `7260f7bd4ede` (git tag `materials-frozen-2026-10-01`)):
- the sampling rule, the implementation notes, the screening guide, and the deviations log;
- the case template and the endings, and the condensing brief;
- the raw ASRS export and the screening logs;
- `cases/cases.json` and the source reports;
- the prompts;
- the scripts.

**Reference:** Reason, J. (1997). *Managing the Risks of Organizational Accidents*. Ashgate. p.209.
