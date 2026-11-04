# AFACS analysis: opus_bulk_r1

Coded traces: 250. Failure observed in 208 (83% (78%–87%) of the sample; 84% (78%–89%) weighted to the pool). Shares below are of traces with a failure observed.

Shares are **weighted** so they represent the eligible pool, not the balanced sample (the sample over-represents small frameworks and models). n is the number of coded traces.

## RQ2: where in the layers do failures sit?

| Group | n | L4 Organisational/design | L3 Supervision | L2 Preconditions | L1 Unsafe acts | Any latent (L2–L4) |
|---|---|---|---|---|---|---|
| All (weighted to eligible pool) | 208 | 63% (55%–71%) | 74% (66%–81%) | 54% (45%–62%) | 100% (97%–100%) | 85% (78%–90%) |
| AG2 | 35 | 22% (11%–40%) | 20% (9%–38%) | 6% (1%–21%) | 100% (88%–100%) | 38% (22%–57%) |
| AppWorld | 21 | 19% (8%–40%) | 67% (45%–83%) | 81% (60%–92%) | 100% (85%–100%) | 95% (77%–99%) |
| HyperAgent | 13 | 31% (13%–58%) | 100% (77%–100%) | 100% (77%–100%) | 100% (77%–100%) | 100% (77%–100%) |
| Magentic | 53 | 23% (13%–36%) | 83% (71%–91%) | 81% (69%–89%) | 100% (93%–100%) | 96% (87%–99%) |
| MetaGPT | 63 | 94% (85%–98%) | 94% (85%–98%) | 63% (50%–74%) | 100% (94%–100%) | 100% (94%–100%) |
| OpenManus | 23 | 87% (68%–95%) | 91% (73%–98%) | 83% (63%–93%) | 100% (86%–100%) | 100% (86%–100%) |

Deepest contributing layer: L4 63%, L3 19%, L2 2%, L1 15%

## RQ3: errors vs violations

| Group | n | Any violation code | Exceptional (V2) | Indeterminate (V?) | Evidence stated | Evidence inferred |
|---|---|---|---|---|---|---|
| All (weighted to eligible pool) | 208 | 13% (9%–20%) | 7% | 7% | 2% | 5% |
| AG2 | 35 | 36% (21%–55%) | 20% | 16% | 4% | 16% |
| AppWorld | 21 | 0% (0%–15%) | 0% | 0% | 0% | 0% |
| HyperAgent | 13 | 69% (42%–87%) | 46% | 31% | 23% | 23% |
| Magentic | 53 | 11% (5%–23%) | 8% | 4% | 4% | 4% |
| MetaGPT | 63 | 3% (1%–11%) | 0% | 3% | 0% | 0% |
| OpenManus | 23 | 9% (2%–27%) | 4% | 4% | 4% | 0% |

Evidence columns: share of failed traces whose violation rests on the agent's own words (stated) or only on the nature of the act (inferred); thin evidence is the V? column (codebook v1, section 2.1).

### Model-level patterns (framework and benchmark held fixed)

AFACS does not code model development (L4.4) from traces. Here the framework and benchmark are held fixed and only the model varies; a difference that follows the model suggests, but does not establish, a model-level contribution. Exploratory: the groups are small.

| Framework (benchmark) | Model | n | Any violation code | Evidence stated | L1 errors only |
|---|---|---|---|---|---|
| MetaGPT (ProgramDev) | Claude | 16 | 0% (0%–19%) | 0% | 100% |
| MetaGPT (ProgramDev-v2) | CodeLlama | 16 | 12% (3%–36%) | 0% | 88% |
| MetaGPT (ProgramDev) | GPT-4o | 15 | 0% (0%–20%) | 0% | 100% |
| MetaGPT (ProgramDev-v2) | Qwen | 16 | 0% (0%–19%) | 0% | 100% |
| AG2 (GSM-Plus) | Claude | 11 | 18% (5%–48%) | 0% | 82% |
| AG2 (GSM-Plus) | GPT-4o | 1 | 0% (0%–79%) | 0% | 100% |
| AG2 (Olympiad) | GPT-4o | 14 | 50% (27%–73%) | 7% | 50% |
| AG2 (MMLU) | GPT-4o-mini | 9 | 0% (0%–30%) | 0% | 100% |

Traces MAST labels **FM-1.1 Disobey Task Specification** (n=81): 22% (13%–35%) carry an AFACS violation code; the rest are coded as errors only. If both groups are substantial, FM-1.1 mixes capability failures and departures from known requirements.

## RQ1 (observed): HFACS error types × Ezell et al.'s cognitive functions

Traces with an L1 error: 205. Cells: number of traces in which that error type was assigned that cognitive function (one error can involve several functions). The cross-walk predicts E3 with observation and understanding, E2 with decision, and E1 with action.

| HFACS error | observation | understanding | decision | action | none given |
|---|---|---|---|---|---|
| L1.E1 (n=99) | 0 | 0 | 0 | 99 | 0 |
| L1.E2 (n=191) | 6 | 82 | 187 | 29 | 0 |
| L1.E3 (n=100) | 69 | 85 | 0 | 1 | 0 |

## RQ4: MAST × AFACS cross-walk

Each row: traces carrying that MAST label. Cells: share with an AFACS code at that layer, and with any violation code.

| MAST label | n | L4 | L3 | L2 | L1 | Violation |
|---|---|---|---|---|---|---|
| 1.1 Disobey Task Specification | 81 | 52% | 65% | 59% | 100% | 22% |
| 1.2 Disobey Role Specification | 7 | 79% | 31% | 57% | 100% | 5% |
| 1.3 Step Repetition | 117 | 66% | 85% | 82% | 100% | 16% |
| 1.4 Loss of Conversation History | 21 | 62% | 85% | 89% | 100% | 18% |
| 1.5 Unaware of Termination Conditions | 72 | 65% | 77% | 81% | 100% | 11% |
| 2.1 Conversation Reset | 8 | 65% | 100% | 100% | 100% | 65% |
| 2.2 Fail to Ask for Clarification | 66 | 44% | 80% | 67% | 100% | 13% |
| 2.3 Task Derailment | 62 | 61% | 74% | 73% | 100% | 17% |
| 2.4 Information Withholding | 4 | 17% | 100% | 100% | 100% | 34% |
| 2.5 Ignored Other Agent's Input | 49 | 77% | 78% | 69% | 100% | 14% |
| 2.6 Reasoning-Action Mismatch | 120 | 48% | 64% | 56% | 100% | 24% |
| 3.1 Premature Termination | 69 | 55% | 78% | 59% | 100% | 22% |
| 3.2 No or Incomplete Verification | 107 | 68% | 80% | 51% | 100% | 17% |
| 3.3 Incorrect Verification | 133 | 57% | 70% | 56% | 100% | 18% |
## Evidence check: are the annotator's quotes genuine?

Each of the annotator's 1328 evidence quotes (across 250 codings) was checked against the step it cites (codebook v1, note 5.6).

| Result | Quotes |
|---|---|
| Found in the cited step | 1327 (99.9%) |
| Found, but in a different step | 0 (0.0%) |
| Not found in any visible step (paraphrased or invented) | 0 (0.0%) |
| Cites a hidden or non-existent step | 0 (0.0%) |
| Too short to check | 1 (0.1%) |

Codings whose quotes were all found in the cited step: 246 of the 247 that gave quotes (codings of traces judged failure-free usually give none). Codings with at least one code that no evidence item supports: 0.

