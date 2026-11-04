# Descriptive tables for the paper

*Produced by `scripts/09_paper_tables.py` after the registered analysis. Descriptive or exploratory only; the registered tests are in `summary.md`. Main cases only unless stated.*

## T1. Data collection, by model

| Model | Planned calls | Valid | Requests refused (HTTP 429) | Other invalid attempts | Cost (USD) | Mean input tokens | Mean output tokens | Providers serving the model |
|---|---|---|---|---|---|---|---|---|
| Claude Sonnet 5.5 | 1080 | 1080 | 1659 | 0 | 18.27 | 1,767 | 1,338 | Claude Platform on AWS (1076); Azure (4) |
| GPT-6.1 Sol | 1080 | 1080 | 1617 | 2 | 7.73 | 1,136 | 586 | OpenAI (1073); Azure (7) |
| DeepSeek V4 Pro | 1080 | 1080 | 0 | 20 | 1.20 | 1,150 | 2,345 | Baidu (560); StreamLake (505); Relace (9); GMICloud (1); SiliconFlow (1); Novita (1); NextBit (1); Reka (1); Parasail (1) |

## T2. Derived outcome, share of replies by version (descriptive)

| Model | Version | n | Blameless error | System-induced error | Possible negligent error | System-induced violation | Possible reckless violation |
|---|---|---|---|---|---|---|---|
| Claude Sonnet 5.5 | safe | 480 | 80.8% | 2.9% | 14.2% | 0.0% | 2.1% |
| Claude Sonnet 5.5 | bad | 480 | 69.2% | 2.5% | 26.2% | 0.0% | 2.1% |
| GPT-6.1 Sol | safe | 480 | 65.2% | 4.2% | 25.4% | 2.1% | 3.1% |
| GPT-6.1 Sol | bad | 480 | 59.2% | 5.6% | 29.2% | 2.1% | 4.0% |
| DeepSeek V4 Pro | safe | 480 | 85.8% | 0.0% | 6.5% | 1.2% | 6.5% |
| DeepSeek V4 Pro | bad | 480 | 79.6% | 0.6% | 8.3% | 1.9% | 9.6% |

Grouped: *blameless* = ranks 1–2; *system-attributed* = ranks 3 and 5; *crew culpability indicated* = ranks 4 and 6 (Reason's two "possible" culpable outcomes).

| Model | Blameless, safe → bad | System-attributed, safe → bad | Crew culpability indicated, safe → bad |
|---|---|---|---|
| Claude Sonnet 5.5 | 80.8% → 69.2% | 2.9% → 2.5% | 16.2% → 28.3% |
| GPT-6.1 Sol | 65.2% → 59.2% | 6.2% → 7.7% | 28.5% → 33.1% |
| DeepSeek V4 Pro | 85.8% → 79.6% | 1.2% → 2.5% | 12.9% → 17.9% |

## T3. Each case's most common outcome, safe version → bad version (cases where it changed; descriptive)

Ties are broken towards the less culpable outcome, the same way for both versions.

| Model | Transition | Cases |
|---|---|---|
| Claude Sonnet 5.5 | Blameless error → Possible negligent error | 5 |
| Claude Sonnet 5.5 | Blameless error → System-induced error | 1 |
| GPT-6.1 Sol | Blameless error → System-induced error | 2 |
| GPT-6.1 Sol | Blameless error → Possible negligent error | 2 |
| GPT-6.1 Sol | System-induced error → Possible reckless violation | 1 |
| GPT-6.1 Sol | Possible negligent error → Blameless error | 1 |
| DeepSeek V4 Pro | Blameless error → Possible reckless violation | 2 |

## T4. Substitution test (answered separately), severity and "insufficient information" flags, by version

| Model | Substitution 'pass', safe | Substitution 'pass', bad | Mean severity, safe | Mean severity, bad | Replies with any insufficient-information flag, safe | ... bad | q3b (procedures) flagged, safe | ... bad |
|---|---|---|---|---|---|---|---|---|
| Claude Sonnet 5.5 | 388/480 (81%) | 332/480 (69%) | 2.38 | 3.25 | 214/480 (45%) | 277/480 (58%) | 9/10 (90%) of replies reaching q3b | 8/10 (80%) of replies reaching q3b |
| GPT-6.1 Sol | 323/480 (67%) | 294/480 (61%) | 2.95 | 4.25 | 318/480 (66%) | 333/480 (69%) | 6/25 (24%) of replies reaching q3b | 10/29 (34%) of replies reaching q3b |
| DeepSeek V4 Pro | 433/480 (90%) | 403/480 (84%) | 1.93 | 3.64 | 3/480 (1%) | 12/480 (2%) | 0/37 (0%) of replies reaching q3b | 0/55 (0%) of replies reaching q3b |

## T5. Share of replies answering 'yes' at each question they reached, by version (descriptive)

| Model | Version | q1 | q1b | q2 | q2b | q3 | q3b | q4 | q4b | q5 |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Sonnet 5.5 | safe | 287/480 | 0/287 | 0/480 | – | 10/480 | 10/10 | 388/470 | 14/82 | 0/388 |
| Claude Sonnet 5.5 | bad | 302/480 | 0/302 | 0/480 | – | 10/480 | 10/10 | 332/470 | 12/138 | 0/332 |
| GPT-6.1 Sol | safe | 342/480 | 0/342 | 0/480 | – | 25/480 | 15/25 | 313/455 | 20/142 | 0/313 |
| GPT-6.1 Sol | bad | 357/480 | 0/357 | 0/480 | – | 29/480 | 19/29 | 284/451 | 27/167 | 0/284 |
| DeepSeek V4 Pro | safe | 382/480 | 0/382 | 0/480 | – | 37/480 | 31/37 | 412/443 | 0/31 | 0/412 |
| DeepSeek V4 Pro | bad | 386/480 | 0/386 | 0/480 | – | 55/480 | 46/55 | 382/425 | 3/43 | 0/382 |

## T6. Controls: mean derived rank by version (expected rank in brackets)

| Model | K1 (1) | K2 (1) | K3 (1) | K4 (6) | K5 (6) | K6 (6) |
|---|---|---|---|---|---|---|
| Claude Sonnet 5.5 | 1.0 / 1.0 | 1.0 / 1.0 | 1.0 / 1.0 | 6.0 / 6.0 | 6.0 / 6.0 | 6.0 / 6.0 |
| GPT-6.1 Sol | 1.0 / 1.0 | 1.0 / 1.0 | 1.0 / 1.0 | 6.0 / 6.0 | 6.0 / 6.0 | 6.0 / 6.0 |
| DeepSeek V4 Pro | 1.0 / 1.0 | 1.0 / 1.0 | 1.0 / 1.0 | 6.0 / 6.0 | 6.0 / 6.0 | 6.0 / 6.0 |

## T7. Do the models shift on the same cases? (exploratory)

- Pearson correlation of per-case shifts, Claude Sonnet 5.5 and GPT-6.1 Sol: r = 0.39
- Pearson correlation of per-case shifts, Claude Sonnet 5.5 and DeepSeek V4 Pro: r = 0.21
- Pearson correlation of per-case shifts, GPT-6.1 Sol and DeepSeek V4 Pro: r = -0.10
- Cases harsher for all three models: 5 of 48; for at least one: 30; unchanged for all three: 16.

## T8. Per-case shift in mean rank (bad minus safe), by model

| Case | Category | Primary problem | Claude Sonnet 5.5 | GPT-6.1 Sol | DeepSeek V4 Pro |
|---|---|---|---|---|---|
| S01 | C | Human Factors | +0.0 | +0.3 | +0.0 |
| S02 | D | Human Factors | +0.0 | +0.0 | +0.0 |
| S03 | C | Human Factors | +0.2 | +1.0 | +0.2 |
| S04 | C | Human Factors | +0.3 | +0.3 | +0.0 |
| S05 | C | Human Factors | +1.2 | +0.0 | +0.0 |
| S06 | B | Human Factors | +0.0 | +0.0 | +0.0 |
| S07 | A | Human Factors | +0.0 | +0.0 | +1.2 |
| S08 | A | Human Factors | +2.1 | +1.2 | +0.9 |
| S09 | C | Human Factors | +1.8 | +0.0 | +0.3 |
| S10 | D | Procedure | +0.0 | +0.0 | +0.4 |
| S11 | C | Human Factors | +0.0 | -0.9 | +0.0 |
| S12 | A | Human Factors | +0.0 | +0.0 | +1.4 |
| S13 | C | Human Factors | -0.3 | +0.3 | +0.0 |
| S14 | C | Human Factors | +0.3 | +0.0 | +0.0 |
| S15 | D | Human Factors | +0.0 | +0.0 | +0.0 |
| S16 | C | Procedure | +0.0 | +0.0 | +0.0 |
| S17 | A | Human Factors | +0.0 | +0.0 | +0.0 |
| S18 | D | Human Factors | +0.0 | +0.0 | +0.0 |
| S19 | D | Human Factors | +0.0 | +0.0 | +0.3 |
| S20 | B | Procedure | +0.0 | +0.0 | +0.0 |
| S21 | B | Human Factors | +0.6 | +0.3 | +0.0 |
| S22 | F | Human Factors | +1.5 | +0.6 | +0.0 |
| S23 | C | Human Factors | +1.5 | +0.0 | +0.0 |
| S24 | C | Human Factors | +1.2 | +1.2 | +0.3 |
| S25 | A | Human Factors | +0.7 | +1.2 | +0.5 |
| S26 | C | Human Factors | +0.0 | +0.0 | +0.0 |
| S27 | B | Human Factors | +0.0 | +0.0 | +0.0 |
| S28 | C | Human Factors | +0.3 | -0.4 | +1.2 |
| S29 | F | Human Factors | +0.0 | +0.3 | +0.0 |
| S30 | B | Human Factors | +0.3 | -0.9 | +0.3 |
| S31 | C | Human Factors | +0.0 | +0.0 | +0.0 |
| S32 | D | Human Factors | +0.0 | +1.6 | +0.0 |
| S33 | C | Human Factors | +0.0 | +0.0 | -0.7 |
| S34 | F | Human Factors | +0.0 | +0.0 | +0.0 |
| S35 | C | Procedure | +0.0 | +0.0 | +0.0 |
| S36 | C | Human Factors | +0.0 | +0.0 | +0.0 |
| S37 | A | Human Factors | +2.1 | +0.2 | +2.8 |
| S38 | C | Human Factors | -0.3 | +0.0 | +0.3 |
| S39 | F | Human Factors | +0.0 | +0.0 | +1.1 |
| S40 | F | Human Factors | +0.0 | +0.0 | +0.0 |
| S41 | C | Human Factors | +1.0 | +0.0 | +0.3 |
| S42 | F | Human Factors | +0.6 | +0.0 | -0.1 |
| S43 | A | Human Factors | +1.5 | +2.1 | -1.0 |
| S44 | B | Procedure | +0.0 | +0.0 | +0.0 |
| S45 | D | Procedure | +0.0 | +0.0 | +0.4 |
| S46 | D | Human Factors | +0.4 | +0.0 | +0.0 |
| S47 | A | Human Factors | +0.0 | +0.4 | +1.9 |
| S48 | C | Human Factors | +0.0 | +0.0 | +0.0 |
