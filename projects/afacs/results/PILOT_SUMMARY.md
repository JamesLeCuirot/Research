# AI pilot: morning summary

*4 November 2026. Plain-English summary of the overnight runs. Full tables: `results/analysis_*.md` and `results/agreement_*.md`.*

## The bottom line

- **All 750 codings are done.** Claude coded the 250 bulk traces three times: Sonnet, Opus, then Sonnet again. There were no errors, no refusals and no invalid codings.
- **AFACS can be applied consistently.** At the level of layers, two different models agree with κ 0.63–0.76, and the same model agrees with itself at 0.74–0.87. For comparison, MAST's own AI judge agrees with itself at only 0.43 on its flat labels.
- **The evidence is genuine.** Of about 4,000 quotes across the three runs, 99.6–99.9% appear word for word in the step they cite, and none were invented.
- **The main findings hold across all three runs.** Most failures have a contributing factor below the sharp end. Violations are a minority (9–13% of failures) and cluster in two frameworks. MAST's "Disobey Task Specification" label mixes errors with violations.

## 1. How consistent is the coding? (RQ3)

Cohen's κ. Read it as: 0.41–0.60 moderate, 0.61–0.80 substantial, above 0.80 almost perfect.

| Measure | Sonnet vs Opus (two models) | Sonnet vs Sonnet (same model, run twice) |
|---|---|---|
| L4 design factor present | 0.71 | 0.74 |
| L3 supervision factor present | 0.63 | 0.74 |
| L2 precondition present | 0.75 | 0.76 |
| L1 unsafe act present | 0.76 | 0.87 |
| Individual codes (average) | 0.52 | 0.59 |
| Violation vs error | 0.67 | 0.68 |
| Deepest layer (partial credit) | 0.75 | 0.80 |
| Failure seen at all? | 0.69 | 0.80 |
| Error type, HFACS (E1–E3) | 0.55 | 0.71 |
| Error type, Ezell's four functions | 0.58 | 0.70 |
| Identical full set of codes | 24% of traces | 40% of traces |

What this means:
- **Layers are applied consistently; individual codes less so.** That is the usual pattern in HFACS studies.
- **The weakest codes:**
  - `L4.3` (no procedure): 0.19 and 0.23. It overlaps with `L4.1` (no verifier).
  - `L1.V?` (thin evidence for a violation): about 0. It is rare and borderline by definition.
  - `L3.4` and `L3.2`: about 0.3–0.6.

  These are candidates for clearer definitions.
- **HFACS's three error types and Ezell's four functions are about equally consistent** (0.55 vs 0.58; 0.71 vs 0.70).

## 2. Where in the layers do failures sit? (RQ2)

Shares of failed traces, weighted to represent the eligible MAST pool (Sonnet run 1, with the other two runs in brackets):

- an unsafe act (L1): 100% in every run;
- a supervision factor (L3): 71% (Opus 74%, Sonnet run 2 75%);
- a design factor (L4): 70% (63%, 74%);
- a precondition (L2): 55% (54%, 59%);
- any contributing factor below the sharp end (L2–L4): 88% (85%, 91%);
- deepest contributing layer L4: 70% (63%, 74%).

By framework, the pattern follows each system's architecture:
- **MetaGPT:** almost always L4 (98%), mostly "no verifier in the design".
- **HyperAgent:** L3 in 92% and L2 in 100%.
- **AppWorld and Magentic-One:** mostly preconditions (75% and 85%), i.e. broken tools, blocked websites and poor information.
- **AG2:** the fewest deeper factors, consistent with its simple single-assistant setup.

## 3. Errors or violations? (RQ3)

- **Violations are a minority:** 9% of failures (Opus 13%, Sonnet run 2 10%).
- **They cluster:** HyperAgent 69% and AG2 24%; MetaGPT and AppWorld 0%.
- **Most are "inferred" rather than "stated":** in Sonnet run 1, 15 inferred, 5 stated and 3 thin. The typical case is an agent inventing tool results it never received, or writing "verification" code that only returns a hard-coded answer.
- **Different models, different violation rates.** Within AG2 on the same Olympiad maths benchmark, GPT-4o has a violation code in 31% of failures; Claude, GPT-4o-mini and GPT-4o on other AG2 benchmarks have none. That is suggestive of a model-level effect but exploratory, because the groups are small.
- **Run-to-run stability:** 16 traces carry a violation code in all three runs, and 38 in at least one.

## 4. MAST's flat labels (RQ4)

- **"Disobey Task Specification" (FM-1.1)** mixes two kinds of failure: 17% of those traces carry a violation code (Opus 22%, run 2 12%), and the rest are errors only.
- **The AI disagreed with MAST's judge that some traces failed at all.** All three runs judged 28 of the 250 failure-free (20 of them AG2 maths problems), and at least one run judged 50 failure-free.
- **A ground-truth check on AppWorld,** whose logs include the benchmark's own pass/fail verdict (hidden from the AI). Three of the 23 AppWorld traces MAST flagged had actually passed. The AI's judgement matched the benchmark in 21 of 23 (Sonnet) and 21 of 23 (Opus, with one "unclear"). This is a small sample, but encouraging.

## 5. Are the AI's quotes genuine? (codebook note 5.6)

| Run | Quotes | Found in the cited step | Found in another step | Not found anywhere |
|---|---|---|---|---|
| Sonnet run 1 | 1,350 | 99.6% | 3 | 0 |
| Opus | 1,328 | 99.9% | 0 | 0 |
| Sonnet run 2 | 1,350 | 99.6% | 2 | 0 |

The check proves the words are in the trace. It does not prove they support the code.

## 6. Things that need your judgement

1. **The Ezell cross-walk test is contaminated.** The table shows errors lining up with Ezell's labels almost exactly as predicted, but note 5.11, which the AI read, states that prediction. So the match shows the AI followed the codebook; it is not evidence for the cross-walk. The consistency comparison (section 1) is unaffected.
   - **My proposal:** report it as such in the paper, and remove the prediction from the codebook before any further coding, including paper 2.
2. **L4 may be over-coded.** The AI often infers a design flaw ("no verifier") from the trace alone. This is the best target for your expert case-study review.
3. **"No unsafe act" was never used.** Note 5.8 allows it, but in 606 failure codings across the three runs (201, 208 and 197) no run left L1 empty. Either such failures are genuinely rare in MAST, or the AI is reluctant to use the option.
4. **Hidden answers limit what the AI can see.** With benchmark answers hidden, the AI cannot tell whether a maths answer is wrong. That probably explains most of the AG2 traces it judged failure-free.
5. **Confidence was almost always "medium"** (86–87% of codings in every run), so as used, the confidence field carries little information.

## 6a. Update: the documentation check (L4)

The AI's 24 most frequent design claims were checked against each framework's paper, documentation and code (`docs/design_check.md`):
- 7 confirmed in full, 14 partly true, 2 contradicted, 1 not settled (corrected from 8 and 13 after the independent audit: one confirmed claim put a set-up problem at the design layer).
- **The typical error is overstating a weakness as an absence.** The AI says "no verifier" or "no loop detection" where a weak version of the mechanism exists. A trace can't tell the two apart.
- **Two claims put a failure at the wrong layer:** a run-time fault, and an environment set-up problem.
- **The check also found errors in MAST's own documentation:**
  - MetaGPT is not the system MAST describes.
  - The HyperAgent model label in MAST's paper (Claude-3.7-Sonnet) can't be right for a September 2024 submission.

## 7. What's next (as planned on 4 November; superseded)

*Update: you decided the case studies need technical reviewers, so they are now worked examples whose claims rest on the traces, the benchmark verdicts and the documentation (paper section 6); expert review moves to paper 2.*


1. **Case studies:** you review a handful of codings with the trace beside you. I'd pick:
   - a MetaGPT trace coded at L4;
   - a HyperAgent violation;
   - an AG2 trace the AI judged failure-free;
   - a Magentic-One precondition case.
2. **The paper:** fill in the RQ3 and RQ4 results and the abstract, and write up the points in section 6 as findings or limitations.
3. **Your decisions:** the Ezell contamination, and whether `L4.3` and `L1.V?` need clearer definitions (for paper 2).
