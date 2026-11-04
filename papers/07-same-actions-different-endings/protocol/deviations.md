# Deviations log

*Every departure from the committed protocol after the ASRS export, with when, why and what was done. Nothing here was decided by looking at how any model judged any case. No model had been run when these entries were written.*

## D1 — Category E (airspace violation) produced no qualifying cases

**When:** 1 Oct 2026, during screening.

**What happened:** all 49 category E reports were screened in draw order and none qualified. Every one fails criterion 1, because the crew's own action was not central. All 49 are encounters with drones, balloons or similar, where NASA's "Airspace Violation" code describes the other aircraft's violation, not the crew's. Claude checked this by text search: all 49 contain one of the words UAS, drone, unmanned, balloon or quadcopter.

**What was done:** the pre-registered fallback (sampling rule §4). E's 8 places pass to category C (altitude deviation), screened further down the same shuffled order. Category C's quota becomes 16 main cases.

**Consequence for the pilot cases:** implementation note 5 had named the pilot case from C as "the next qualifier after its 8th". With C's quota now 16, the pilot case from C becomes the **17th** qualifier in C, so that no main case is displaced. This is a mechanical consequence of applying the fallback, recorded here for transparency.

## D2 — Category B (runway incursion) ran out with 6 qualifiers

**When:** 1 Oct 2026, during screening.

**What happened:** all 23 category B reports were screened in draw order and 6 qualified. Thirteen failed criterion 1 (mostly crews responding correctly to someone else's incursion), and four failed criterion 4.

**What was done:** the same fallback as D1. B's 2 missing places pass to category C. C's main quota becomes 18, and its pilot case is the **19th** qualifier.

**Resulting design:** A 8, B 6, C 18, D 8, F 8 = 48 main cases, plus pilot cases from A and C.

**Note for condensing:** in several B cases the conflicting traffic was *landing* traffic that went around in the real event, rather than traffic taking off. The bad ending in `04-endings-and-case-template.md` assumes departing traffic, so a landing-traffic variant is proposed there for James to approve before condensing.

## D3 — Criterion 4 clarified for loss-of-separation categories (TCAS below 1,000 ft)

**When:** 1 Oct 2026, after categories C and D had been screened, and before any case was condensed or any model run.

**What happened:** the category C screener reported that many of its qualifiers were low-altitude deviations on final approach. The loss-of-separation bad ending says both crews follow TCAS resolution advisories, but TCAS does not issue resolution advisories below about 1,000 ft above ground. So for those cases the ending is not plausible, and criterion 4 should have failed them.

**What was done:**
- Criterion 4 in the screening guide gained an explicit clarification: deviations entirely below about 1,000 ft above ground fail for categories C, D and F.
- Categories C and D were re-checked against it, in the original draw order, with any new failures logged. Screening then continued down the same order until the quotas were met again.
- Category F was given the clarification while it was still being screened.

**Why this is not a results-driven change:** no model had been run, and no case had been condensed. The change corrects the plausibility test for the fixed bad ending, and is applied the same way to every report.

## D4 — The safe-ending sentence when the real event involved traffic

**When:** 1 Oct 2026, before condensing, and before any model run.

**What happened:** the frozen safe-ending pattern ends "There was no conflict with other traffic". In several selected reports that sentence would be false. For example, landing traffic was sent around, or there was a TCAS traffic advisory.

**What was done:** where the report shows a traffic interaction, that sentence is replaced by a factual one describing it, followed by "No one was hurt and no aircraft was damaged." The bad ending is unchanged. This keeps the safe ending true to the report.

## D5 — The 150-word minimum is a guide where the report itself is short

**When:** 1 Oct 2026, during condensing, and before any model run.

**What happened:** ACN 2207565's narrative is three sentences, so its shared text uses every fact in it and comes to 122 words. Reaching 150 would mean inventing detail.

**What was done:** the case is kept at 122 words. The 150-word lower bound is treated as a guide; the 250-word upper bound remains a rule. The comparison is within each case, so length does not confound it.

## D6 — Case-level edit: the safe ending of ACN 2252551 trimmed

**When:** 1 Oct 2026, during condensing, and before any model run.

**What happened:** the real event included a TCAS resolution advisory. The crew's response to it, a brief stick shaker and an upset recovery, had been placed in the safe ending. That would make the two versions differ in crew actions, not just outcome.

**What was done:** the safe ending was trimmed to the advisories and the outcome, and the crew's response was removed. The bad ending is unchanged.

## D7 — Four cases excluded by written rules and replaced from the same draw order

**When:** 1 Oct 2026, after condensing and James's first look, and before any model run.

**Why:** James preferred excluding a problematic case to editing it. The rules below are applied to every case alike. Every exclusion is listed in `data/exclusions.csv`.
- **E1 — The crew's act is not the coded event type.** Excludes 2225120: coded as an unstabilised approach, but the act was a rejected take-off.
- **E2 — The bad ending cannot happen given the report's facts.** Excludes the two loss-of-separation cases on cargo flights, 2282455 and 2221591, because the ending injures a flight attendant aboard. The two runway-incursion cases on cargo flights are unaffected, because there the flight attendant is on the other aircraft. Claude checked all cases for cargo missions, and for cargo wording where the mission is blank: only these two are affected.
- **E3 — A faithful case would need facts that bear on blame removed or added.** Excludes 2298231: pre-flight warnings about the captain, which contradict the fixed "no previous safety events" line.

**Replacement:**
- **Category A** takes the next qualifier in its draw order after rank 74, the pilot case.
- **Category F's pack is used up,** so under sampling rule §4 its 2 places pass to category C.
- **Category C** therefore needs 3 more qualifiers: 1 for its own exclusion and 2 from F. They are screened from rank 28 onward, in draw order.

**Added to criterion 4 for replacements:** a loss-of-separation case must be a passenger flight, since its bad ending injures a flight attendant aboard. This is rule E2 written into screening.

**The other changes:**
- **2307722:** a definitional clause the condenser had added (not from the report) was deleted.
- **Final design:** A 8, B 6, C 20, D 8, F 6 = 48 main cases.

## D8 — The maximum output raised from 4,000 to 16,000 tokens, after the pilot

**When:** 1 Oct 2026, during the pilot, after registration and before any main-study call.

**What happened:** in the pilot, 38 of 48 Gemini 3.8 Flash replies and 9 of 33 DeepSeek V4 Pro replies were invalid. Every one stopped at the 4,000-token output limit (completion tokens ≥ 3,990), because the models' hidden reasoning (about 2,800–3,800 tokens) used up the allowance before the JSON answer was finished. Claude Sonnet 5.5 and GPT-6.1 Sol replies were all valid.

**What was done:** the maximum output (`MAX_TOKENS` in `scripts/03_run.py`) was raised to 16,000 tokens for every model alike. The 4,000-token figure was the study's own cost bound, not a model setting; at 4,000 it cut short the models' default behaviour, which the plan meant to leave alone. Failed pilot calls are retried with the new limit.

**Why this is allowed:** the registration permits pilot-driven fixes to software and settings that do not change wording, cases, models or analysis. The decision rested only on whether replies were complete and parseable, never on what they said.

## A limitation to state in the write-up

The cases were condensed by Claude models, working to a fixed brief, and then checked by James. One of the four models tested is a Claude model. The wording may therefore be stylistically familiar to it. The brief fixes the wording rules, and the endings are fixed text, which limits the effect, but it should be stated.

## Lesson for the write-up

**Lesson for the write-up:** in ASRS Part 121 data, the "Airspace Violation" code mostly marks drone intrusions. A future sampling rule should exclude reports tagged as unmanned-aircraft encounters, or take airspace cases from the procedural clearance codes instead.

## D9 — Gemini 3.8 Flash dropped from the study, for cost

**When:** 1 Oct 2026, during the pilot, after registration and before any main-study call. Decided by James ("Maybe we just drop off Gemini").

**What happened:** under default settings Gemini 3.8 Flash produced very long hidden reasoning (about 3,600 tokens or more per reply). In the pilot it cost about $0.07 per valid reply, inflated by replies cut short at the old 4,000-token limit (see D8). With D8's limit, the projected cost for its 1,080 main-study calls was about $30–40, more than the other three models together. The study's budget is personal and small.

**What was done:** Gemini is removed. The study proceeds with three models: `anthropic/claude-sonnet-5.5`, `openai/gpt-6.1-sol` and `deepseek/deepseek-v4-pro` (open weights). The Holm correction runs across three models, which the analysis script does automatically from the models present. The main study is now 48 × 2 × 2 × 3 × 5 = 2,880 calls, plus 360 control calls.

**Why this is not results-driven:** the decision rested only on cost and on reply completeness. No pilot judgement was examined, and the pilot cases are excluded from all analysis anyway.

## D10 — Calls refused by rate limits were sent again

**When:** 2 Oct 2026, after the first pass of the main run, and before any main-run reply was analysed.

**What happened:** the first pass (1 Oct, 20:58–22:07) ran 40 calls in parallel. OpenRouter accepted about 20 calls a minute for each of Claude Sonnet 5.5 and GPT-6.1 Sol, and refused the rest with HTTP 429 ("Too Many Requests"). The script's short pauses (2 and 4 seconds) used up all three attempts on 676 calls: 345 Claude and 331 GPT. DeepSeek V4 Pro completed all 1,080. A refused request never reaches the model and is not charged, so these 676 planned calls had not been made.

**What was done:** the same script, unchanged, was run again: first with 16 calls in parallel, which left 237 still refused, then with 8 (19 left), then with 4. After that every one of the 3,240 planned calls had a valid reply. The main run cost $27.19 in total. It sends only the calls that have no valid reply, as it is designed to. The analysis uses the first valid reply for each call, as before.

**Why this is not results-driven:** the gaps were caused by timing, not content. They were spread evenly: Claude was missing 179 safe and 166 bad versions, and GPT 166 and 165. The only check was a count of valid records by model and version; no reply content was examined. Sending them again keeps to the registered stopping rule, under which every planned call is made once.

## D11 — Two points found while writing up, both reported in the paper

**When:** 2 Oct 2026, while drafting the paper, after the analysis.

1. **The registration's screening count is out of date.** It says 234 reports were screened. That figure was written before the D7 replacements were screened. The final count in `data/screening-log.csv` is 280. The 48 cases and the analysis are unaffected.
2. **The blind re-screen of a sample was not done.** The sampling rule (§4, "Logging") says independent checkers re-screen a sample, blind to any results. No independent checker took part. Claude screened and condensed under the written rules. James, the author, read every case side by side with its source report before the freeze. A re-screen could still be done by someone not shown the results. Until then, it is reported as a limitation.
