# AFACS analysis: sonnet_bulk_r2

Coded traces: 250. Failure observed in 197 (79% (73%–83%) of the sample; 77% (70%–83%) weighted to the pool). Shares below are of traces with a failure observed.

Shares are **weighted** so they represent the eligible pool, not the balanced sample (the sample over-represents small frameworks and models). n is the number of coded traces.

## RQ2: where in the layers do failures sit?

| Group | n | L4 Organisational/design | L3 Supervision | L2 Preconditions | L1 Unsafe acts | Any latent (L2–L4) |
|---|---|---|---|---|---|---|
| All (weighted to eligible pool) | 197 | 74% (66%–81%) | 75% (67%–82%) | 59% (50%–67%) | 100% (97%–100%) | 91% (85%–95%) |
| AG2 | 28 | 43% (25%–64%) | 34% (17%–56%) | 33% (17%–55%) | 100% (84%–100%) | 63% (42%–80%) |
| AppWorld | 20 | 10% (3%–30%) | 50% (30%–70%) | 80% (58%–92%) | 100% (84%–100%) | 95% (76%–99%) |
| HyperAgent | 13 | 38% (18%–64%) | 92% (67%–99%) | 100% (77%–100%) | 100% (77%–100%) | 100% (77%–100%) |
| Magentic | 53 | 34% (23%–47%) | 72% (58%–82%) | 85% (73%–92%) | 100% (93%–100%) | 92% (82%–97%) |
| MetaGPT | 60 | 100% (94%–100%) | 92% (82%–96%) | 57% (44%–68%) | 100% (94%–100%) | 100% (94%–100%) |
| OpenManus | 23 | 87% (68%–95%) | 65% (45%–81%) | 91% (73%–98%) | 100% (86%–100%) | 100% (86%–100%) |

Deepest contributing layer: L4 74%, L3 10%, L2 7%, L1 9%

## RQ3: errors vs violations

| Group | n | Any violation code | Exceptional (V2) | Indeterminate (V?) | Evidence stated | Evidence inferred |
|---|---|---|---|---|---|---|
| All (weighted to eligible pool) | 197 | 10% (6%–16%) | 7% | 2% | 2% | 6% |
| AG2 | 28 | 30% (14%–51%) | 18% | 6% | 6% | 18% |
| AppWorld | 20 | 0% (0%–16%) | 0% | 0% | 0% | 0% |
| HyperAgent | 13 | 62% (36%–82%) | 62% | 0% | 31% | 31% |
| Magentic | 53 | 13% (7%–25%) | 11% | 2% | 2% | 9% |
| MetaGPT | 60 | 0% (0%–6%) | 0% | 0% | 0% | 0% |
| OpenManus | 23 | 13% (5%–32%) | 9% | 4% | 4% | 4% |

Evidence columns: share of failed traces whose violation rests on the agent's own words (stated) or only on the nature of the act (inferred); thin evidence is the V? column (codebook v1, section 2.1).

### Model-level patterns (framework and benchmark held fixed)

AFACS does not code model development (L4.4) from traces. Here the framework and benchmark are held fixed and only the model varies; a difference that follows the model suggests, but does not establish, a model-level contribution. Exploratory: the groups are small.

| Framework (benchmark) | Model | n | Any violation code | Evidence stated | L1 errors only |
|---|---|---|---|---|---|
| MetaGPT (ProgramDev) | Claude | 15 | 0% (0%–20%) | 0% | 100% |
| MetaGPT (ProgramDev-v2) | CodeLlama | 16 | 0% (0%–19%) | 0% | 100% |
| MetaGPT (ProgramDev) | GPT-4o | 13 | 0% (0%–23%) | 0% | 100% |
| MetaGPT (ProgramDev-v2) | Qwen | 16 | 0% (0%–19%) | 0% | 100% |
| AG2 (GSM-Plus) | Claude | 4 | 0% (0%–49%) | 0% | 100% |
| AG2 (GSM-Plus) | GPT-4o | 1 | 0% (0%–79%) | 0% | 100% |
| AG2 (Olympiad) | GPT-4o | 13 | 38% (18%–64%) | 8% | 62% |
| AG2 (MMLU) | GPT-4o-mini | 10 | 20% (6%–51%) | 10% | 80% |

Traces MAST labels **FM-1.1 Disobey Task Specification** (n=74): 12% (6%–24%) carry an AFACS violation code; the rest are coded as errors only. If both groups are substantial, FM-1.1 mixes capability failures and departures from known requirements.

## RQ1 (observed): HFACS error types × Ezell et al.'s cognitive functions

Traces with an L1 error: 197. Cells: number of traces in which that error type was assigned that cognitive function (one error can involve several functions). The cross-walk predicts E3 with observation and understanding, E2 with decision, and E1 with action.

| HFACS error | observation | understanding | decision | action | none given |
|---|---|---|---|---|---|
| L1.E1 (n=60) | 0 | 0 | 0 | 60 | 0 |
| L1.E2 (n=179) | 1 | 47 | 176 | 59 | 0 |
| L1.E3 (n=126) | 81 | 122 | 1 | 1 | 0 |

## RQ4: MAST × AFACS cross-walk

Each row: traces carrying that MAST label. Cells: share with an AFACS code at that layer, and with any violation code.

| MAST label | n | L4 | L3 | L2 | L1 | Violation |
|---|---|---|---|---|---|---|
| 1.1 Disobey Task Specification | 74 | 71% | 69% | 69% | 100% | 12% |
| 1.2 Disobey Role Specification | 7 | 42% | 57% | 62% | 100% | 0% |
| 1.3 Step Repetition | 114 | 78% | 86% | 86% | 100% | 10% |
| 1.4 Loss of Conversation History | 21 | 77% | 95% | 92% | 100% | 7% |
| 1.5 Unaware of Termination Conditions | 71 | 67% | 72% | 87% | 100% | 10% |
| 2.1 Conversation Reset | 8 | 58% | 100% | 100% | 100% | 28% |
| 2.2 Fail to Ask for Clarification | 66 | 50% | 67% | 69% | 100% | 8% |
| 2.3 Task Derailment | 63 | 71% | 72% | 75% | 100% | 10% |
| 2.4 Information Withholding | 4 | 50% | 100% | 100% | 100% | 67% |
| 2.5 Ignored Other Agent's Input | 45 | 84% | 80% | 83% | 100% | 11% |
| 2.6 Reasoning-Action Mismatch | 113 | 66% | 68% | 68% | 100% | 18% |
| 3.1 Premature Termination | 68 | 69% | 76% | 49% | 100% | 12% |
| 3.2 No or Incomplete Verification | 99 | 83% | 77% | 58% | 100% | 11% |
| 3.3 Incorrect Verification | 127 | 71% | 74% | 58% | 100% | 14% |
## Evidence check: are the annotator's quotes genuine?

Each of the annotator's 1350 evidence quotes (across 250 codings) was checked against the step it cites (codebook v1, note 5.6).

| Result | Quotes |
|---|---|
| Found in the cited step | 1344 (99.6%) |
| Found, but in a different step | 2 (0.1%) |
| Not found in any visible step (paraphrased or invented) | 0 (0.0%) |
| Cites a hidden or non-existent step | 0 (0.0%) |
| Too short to check | 4 (0.3%) |

Codings whose quotes were all found in the cited step: 212 of the 218 that gave quotes (codings of traces judged failure-free usually give none). Codings with at least one code that no evidence item supports: 0.

