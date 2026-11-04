# AFACS analysis: sonnet_bulk_r1

Coded traces: 250. Failure observed in 201 (80% (75%–85%)). Shares below are of traces with a failure observed.

Shares are **weighted** so they represent the eligible pool, not the balanced sample (the sample over-represents small frameworks and models). n is the number of coded traces.

## RQ2: where in the layers do failures sit?

| Group | n | L4 Organisational/design | L3 Supervision | L2 Preconditions | L1 Unsafe acts | Any latent (L2–L4) |
|---|---|---|---|---|---|---|
| All (weighted to eligible pool) | 201 | 70% (62%–77%) | 71% (63%–78%) | 55% (46%–63%) | 100% (97%–100%) | 88% (81%–92%) |
| AG2 | 31 | 35% (19%–55%) | 35% (19%–55%) | 17% (7%–36%) | 100% (86%–100%) | 51% (32%–70%) |
| AppWorld | 20 | 15% (5%–36%) | 45% (26%–66%) | 75% (53%–89%) | 100% (84%–100%) | 90% (70%–97%) |
| HyperAgent | 13 | 54% (29%–77%) | 92% (67%–99%) | 100% (77%–100%) | 100% (77%–100%) | 100% (77%–100%) |
| Magentic | 54 | 30% (19%–43%) | 65% (51%–76%) | 85% (73%–92%) | 100% (93%–100%) | 93% (82%–97%) |
| MetaGPT | 60 | 98% (91%–100%) | 89% (79%–95%) | 57% (44%–69%) | 100% (94%–100%) | 100% (94%–100%) |
| OpenManus | 23 | 83% (63%–93%) | 65% (45%–81%) | 91% (73%–98%) | 100% (86%–100%) | 100% (86%–100%) |

Deepest contributing layer: L4 70%, L3 12%, L2 5%, L1 12%

## RQ3: errors vs violations

| Group | n | Any violation code | Exceptional (V2) | Indeterminate (V?) | Evidence stated | Evidence inferred |
|---|---|---|---|---|---|---|
| All (weighted to eligible pool) | 201 | 9% (5%–15%) | 7% | 2% | 1% | 6% |
| AG2 | 31 | 24% (11%–44%) | 19% | 5% | 0% | 19% |
| AppWorld | 20 | 0% (0%–16%) | 0% | 0% | 0% | 0% |
| HyperAgent | 13 | 69% (42%–87%) | 62% | 8% | 15% | 46% |
| Magentic | 54 | 13% (6%–24%) | 11% | 2% | 4% | 7% |
| MetaGPT | 60 | 0% (0%–6%) | 0% | 0% | 0% | 0% |
| OpenManus | 23 | 9% (2%–27%) | 9% | 0% | 4% | 4% |

Evidence columns: share of failed traces whose violation rests on the agent's own words (stated) or only on the nature of the act (inferred); thin evidence is the V? column (codebook v1, section 2.1).

### Model-level patterns (framework and benchmark held fixed)

AFACS does not code model development (L4.4) from traces. Here the framework and benchmark are held fixed and only the model varies; a difference that follows the model suggests, but does not establish, a model-level contribution. Exploratory: the groups are small.

| Framework (benchmark) | Model | n | Any violation code | Evidence stated | L1 errors only |
|---|---|---|---|---|---|
| MetaGPT (ProgramDev) | Claude | 15 | 0% (0%–20%) | 0% | 100% |
| MetaGPT (ProgramDev-v2) | CodeLlama | 16 | 0% (0%–19%) | 0% | 100% |
| MetaGPT (ProgramDev) | GPT-4o | 14 | 0% (0%–22%) | 0% | 100% |
| MetaGPT (ProgramDev-v2) | Qwen | 15 | 0% (0%–20%) | 0% | 100% |
| AG2 (GSM-Plus) | Claude | 4 | 0% (0%–49%) | 0% | 100% |
| AG2 (GSM-Plus) | GPT-4o | 1 | 0% (0%–79%) | 0% | 100% |
| AG2 (Olympiad) | GPT-4o | 16 | 31% (14%–56%) | 0% | 69% |
| AG2 (MMLU) | GPT-4o-mini | 10 | 0% (0%–28%) | 0% | 100% |

Traces MAST labels **FM-1.1 Disobey Task Specification** (n=79): 17% (9%–28%) carry an AFACS violation code; the rest are coded as errors only. If both groups are substantial, FM-1.1 mixes capability failures and departures from known requirements.

## RQ1 (observed): HFACS error types × Ezell et al.'s cognitive functions

Traces with an L1 error: 199. Cells: number of traces in which that error type was assigned that cognitive function (one error can involve several functions). The cross-walk predicts E3 with observation and understanding, E2 with decision, and E1 with action.

| HFACS error | observation | understanding | decision | action | none given |
|---|---|---|---|---|---|
| L1.E1 (n=56) | 0 | 0 | 0 | 56 | 0 |
| L1.E2 (n=177) | 0 | 44 | 175 | 61 | 0 |
| L1.E3 (n=128) | 83 | 124 | 0 | 4 | 0 |

## RQ4: MAST × AFACS cross-walk

Each row: traces carrying that MAST label. Cells: share with an AFACS code at that layer, and with any violation code.

| MAST label | n | L4 | L3 | L2 | L1 | Violation |
|---|---|---|---|---|---|---|
| 1.1 Disobey Task Specification | 79 | 62% | 71% | 62% | 100% | 17% |
| 1.2 Disobey Role Specification | 7 | 74% | 90% | 62% | 100% | 15% |
| 1.3 Step Repetition | 118 | 72% | 79% | 80% | 100% | 9% |
| 1.4 Loss of Conversation History | 21 | 76% | 74% | 92% | 100% | 12% |
| 1.5 Unaware of Termination Conditions | 73 | 70% | 74% | 87% | 100% | 11% |
| 2.1 Conversation Reset | 8 | 72% | 86% | 100% | 100% | 42% |
| 2.2 Fail to Ask for Clarification | 66 | 48% | 71% | 68% | 100% | 10% |
| 2.3 Task Derailment | 64 | 65% | 75% | 72% | 100% | 7% |
| 2.4 Information Withholding | 4 | 17% | 100% | 100% | 100% | 34% |
| 2.5 Ignored Other Agent's Input | 47 | 85% | 73% | 74% | 100% | 7% |
| 2.6 Reasoning-Action Mismatch | 114 | 58% | 62% | 57% | 100% | 17% |
| 3.1 Premature Termination | 70 | 57% | 62% | 54% | 100% | 20% |
| 3.2 No or Incomplete Verification | 101 | 78% | 77% | 49% | 100% | 11% |
| 3.3 Incorrect Verification | 131 | 64% | 62% | 50% | 100% | 13% |
## Evidence check: are the annotator's quotes genuine?

Each of the annotator's 1350 evidence quotes (across 250 codings) was checked against the step it cites (codebook v1, note 5.6).

| Result | Quotes |
|---|---|
| Found in the cited step | 1344 (99.6%) |
| Found, but in a different step | 3 (0.2%) |
| Not found in any visible step (paraphrased or invented) | 0 (0.0%) |
| Cites a hidden or non-existent step | 0 (0.0%) |
| Too short to check | 3 (0.2%) |

Codings whose quotes were all found in the cited step: 209 of the 215 that gave quotes (codings of traces judged failure-free usually give none). Codings with at least one code that no evidence item supports: 1.

