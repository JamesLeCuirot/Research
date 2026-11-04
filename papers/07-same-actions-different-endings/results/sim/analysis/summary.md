# Results summary

*Input: `main.jsonl`, 2160 valid replies. Main cases only unless stated; pilot cases excluded.*

## H1: outcome effect on culpability rank (higher = more culpable)

| Model | Cases | Harsher | Same | More lenient | Mean shift (steps) | 95% CI | W+ | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|---|---|
| sim/biased | 48 | 41 | 1 | 6 | +0.60 | [+0.42, +0.79] | 1058.0 | +5.23 | 0.0000 | 0.0000 |
| sim/fair | 48 | 17 | 17 | 14 | +0.01 | [-0.09, +0.10] | 274.0 | +0.51 | 0.6096 | 0.6096 |

## H2: substitution test, share of 'pass' answers (bad minus safe)

| Model | Cases | Mean difference in pass rate | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|
| sim/biased | 48 | -0.177 | [-0.244, -0.113] | 0.0000 | 0.0001 |
| sim/fair | 48 | +0.008 | [-0.019, +0.035] | 0.8274 | 0.8274 |

## H3: consistency across the 5 repeats

| Model | Cells | All 5 repeats same outcome | Fleiss' kappa |
|---|---|---|---|
| sim/biased | 192 | 79/192 (41%) | 0.572 |
| sim/fair | 192 | 126/192 (66%) | 0.791 |

## Which question flips between versions (share of cases whose majority answer differs)

| Model | q1 | q1b | q2 | q2b | q3 | q3b | q4 | q4b | q5 |
|---|---|---|---|---|---|---|---|---|---|
| sim/biased | 4% | 4% | 0% | 0% | 4% | 6% | 12% | 15% | 15% |
| sim/fair | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |

## Checks

| Model | Manipulation: bad rated more severe | Fixed-line 'yes' (substance or history) | Named outcome matches derived |
|---|---|---|---|
| sim/biased | 48/48 (100%) | 0/960 (0.0%) | 0/960 (0%) |
| sim/fair | 48/48 (100%) | 0/960 (0.0%) | 0/960 (0%) |

## Controls (modal derived outcome rank; expected in brackets)

| Model | K1 safe / bad (1) | K2 safe / bad (1) | K3 safe / bad (1) | K4 safe / bad (6) | K5 safe / bad (6) | K6 safe / bad (6) |
|---|---|---|---|---|---|---|
| sim/biased | 1 / 1 | 5 / 5 | 3 / 3 | 4 / 4 | 1 / 1 | 1 / 4 |
| sim/fair | 1 / 1 | 5 / 5 | 4 / 4 | 1 / 1 | 4 / 4 | 1 / 1 |

## Exploratory (labelled as such in any write-up)

### Mean shift by wording, category and primary problem

| Model | W1 | W2 | cat A | cat B | cat C | cat D | cat F | Human Factors | Procedure |
|---|---|---|---|---|---|---|---|---|---|
| sim/biased | +0.65 (n=48) | +0.55 (n=48) | +0.45 (n=8) | +0.55 (n=6) | +0.49 (n=20) | +0.95 (n=8) | +0.75 (n=6) | +0.62 (n=42) | +0.45 (n=6) |
| sim/fair | -0.07 (n=48) | +0.09 (n=48) | +0.06 (n=8) | +0.10 (n=6) | -0.03 (n=20) | -0.13 (n=8) | +0.17 (n=6) | +0.00 (n=42) | +0.07 (n=6) |

### Remarks that the ending looks implausible or inconsistent (share of replies)

| Model | Safe version | Bad version |
|---|---|---|
| sim/biased | 0/480 (0.0%) | 0/480 (0.0%) |
| sim/fair | 0/480 (0.0%) | 0/480 (0.0%) |
