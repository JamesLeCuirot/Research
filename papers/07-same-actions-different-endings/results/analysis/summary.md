# Results summary

*Input: `main.jsonl`, 3240 valid replies. Main cases only unless stated; pilot cases excluded.*

## H1: outcome effect on culpability rank (higher = more culpable)

| Model | Cases | Harsher | Same | More lenient | Mean shift (steps) | 95% CI | W+ | z | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-sonnet-5.5 | 48 | 18 | 28 | 2 | +0.35 | [+0.19, +0.54] | 202.0 | +3.63 | 0.0003 | 0.0009 |
| deepseek/deepseek-v4-pro | 48 | 17 | 28 | 3 | +0.25 | [+0.09, +0.44] | 183.0 | +2.91 | 0.0036 | 0.0071 |
| openai/gpt-6.1-sol | 48 | 14 | 31 | 3 | +0.18 | [+0.04, +0.34] | 124.5 | +2.27 | 0.0230 | 0.0230 |

## H2: substitution test, share of 'pass' answers (bad minus safe)

| Model | Cases | Mean difference in pass rate | 95% CI | p | p (Holm) |
|---|---|---|---|---|---|
| anthropic/claude-sonnet-5.5 | 48 | -0.117 | [-0.179, -0.060] | 0.0004 | 0.0011 |
| deepseek/deepseek-v4-pro | 48 | -0.061 | [-0.103, -0.023] | 0.0071 | 0.0142 |
| openai/gpt-6.1-sol | 48 | -0.060 | [-0.119, -0.008] | 0.0530 | 0.0530 |

## H3: consistency across the 5 repeats

| Model | Cells | All 5 repeats same outcome | Fleiss' kappa |
|---|---|---|---|
| anthropic/claude-sonnet-5.5 | 192 | 157/192 (82%) | 0.767 |
| deepseek/deepseek-v4-pro | 192 | 139/192 (72%) | 0.510 |
| openai/gpt-6.1-sol | 192 | 154/192 (80%) | 0.823 |

## Which question flips between versions (share of cases whose majority answer differs)

| Model | q1 | q1b | q2 | q2b | q3 | q3b | q4 | q4b | q5 |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-sonnet-5.5 | 4% | 4% | 0% | 0% | 0% | 0% | 15% | 17% | 15% |
| deepseek/deepseek-v4-pro | 2% | 2% | 0% | 0% | 6% | 6% | 4% | 0% | 2% |
| openai/gpt-6.1-sol | 8% | 8% | 0% | 0% | 2% | 2% | 10% | 10% | 8% |

## Checks

| Model | Manipulation: bad rated more severe | Fixed-line 'yes' (substance or history) | Named outcome matches derived |
|---|---|---|---|
| anthropic/claude-sonnet-5.5 | 47/48 (98%) | 0/960 (0.0%) | 960/960 (100%) |
| deepseek/deepseek-v4-pro | 47/48 (98%) | 0/960 (0.0%) | 957/960 (100%) |
| openai/gpt-6.1-sol | 47/48 (98%) | 0/960 (0.0%) | 960/960 (100%) |

## Controls (modal derived outcome rank; expected in brackets)

| Model | K1 safe / bad (1) | K2 safe / bad (1) | K3 safe / bad (1) | K4 safe / bad (6) | K5 safe / bad (6) | K6 safe / bad (6) |
|---|---|---|---|---|---|---|
| anthropic/claude-sonnet-5.5 | 1 / 1 | 1 / 1 | 1 / 1 | 6 / 6 | 6 / 6 | 6 / 6 |
| deepseek/deepseek-v4-pro | 1 / 1 | 1 / 1 | 1 / 1 | 6 / 6 | 6 / 6 | 6 / 6 |
| openai/gpt-6.1-sol | 1 / 1 | 1 / 1 | 1 / 1 | 6 / 6 | 6 / 6 | 6 / 6 |

## Exploratory (labelled as such in any write-up)

### Mean shift by wording, category and primary problem

| Model | W1 | W2 | cat A | cat B | cat C | cat D | cat F | Human Factors | Procedure |
|---|---|---|---|---|---|---|---|---|---|
| anthropic/claude-sonnet-5.5 | +0.31 (n=48) | +0.40 (n=48) | +0.80 (n=8) | +0.15 (n=6) | +0.36 (n=20) | +0.05 (n=8) | +0.35 (n=6) | +0.40 (n=42) | +0.00 (n=6) |
| deepseek/deepseek-v4-pro | +0.34 (n=48) | +0.16 (n=48) | +0.96 (n=8) | +0.05 (n=6) | +0.10 (n=20) | +0.14 (n=8) | +0.17 (n=6) | +0.27 (n=42) | +0.13 (n=6) |
| openai/gpt-6.1-sol | +0.17 (n=48) | +0.20 (n=48) | +0.64 (n=8) | -0.10 (n=6) | +0.09 (n=20) | +0.20 (n=8) | +0.15 (n=6) | +0.21 (n=42) | +0.00 (n=6) |

### Remarks that the ending looks implausible or inconsistent (share of replies)

| Model | Safe version | Bad version |
|---|---|---|
| anthropic/claude-sonnet-5.5 | 2/480 (0.4%) | 4/480 (0.8%) |
| deepseek/deepseek-v4-pro | 0/480 (0.0%) | 2/480 (0.4%) |
| openai/gpt-6.1-sol | 4/480 (0.8%) | 4/480 (0.8%) |
