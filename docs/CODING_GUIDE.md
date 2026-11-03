# How to hand-code the calibration traces

*Practical instructions for James. The codebook itself is `codebook/v0.md`.*

## Setup (once)

```bash
uv sync
uv run afacs-ingest
uv run afacs-sample calibration --renders-only   # checks the frozen set, writes data/calibration/C01.md ... (never touches your sheet)
```

The 30 traces are in `data/calibration/C01.md` … `C30.md`. Your sheet is `annotations/human/calibration_sheet.csv`. It opens in Excel, Numbers or Google Sheets; save it back as CSV.

## Rules that keep the coding blind

- Don't open `data/processed/calibration_key.csv`. It says which traces are controls and which are in the test set.
- Don't look up MAST's labels for these traces, and don't render them with `--show-mast`.
- Code in order (C01, C02, …). If you run out of time, stop where you are; a partial set is still usable.

## For each trace

1. Open `data/calibration/Cxx.md`. Read it end to end before coding. Note the task, what the system did, and where it went wrong.
2. Fill in the row for that trace:

| Column | What to write |
|---|---|
| `failure_observed` | `yes`, `no` or `unclear` |
| `l4_codes` | e.g. `L4.1` or `L4.1;L4.3`; empty if no evidence at this layer |
| `l3_codes` | e.g. `L3.3;L3.4` |
| `l2_codes` | e.g. `L2.1` |
| `l1_codes` | e.g. `L1.E2` or `L1.V2` or `L1.V?` |
| `deepest_layer` | `L4`, `L3`, `L2`, `L1`, or `none` if no failure |
| `violation_flag` | `none`, `V1`, `V2` or `V?` (it should match your L1 codes) |
| `confidence` | `high`, `medium` or `low` |
| `evidence_quotes` | 1–4 short quotes with step numbers, separated by ` \| `, e.g. `[S4] "I will skip the tests" \| [S9] "All tests pass"` |
| `notes` | Anything else, **especially where the codebook didn't fit**. These notes become codebook v1. |
| `minutes_spent` | Roughly how long the trace took (for the write-up's effort estimate) |

3. Every so often, check the sheet:

```bash
uv run afacs-agreement check-sheet
```

It reports **errors** (an unknown code, a code in the wrong column, a value not on the allowed list) and **warnings** (e.g. your deepest layer doesn't match the deepest code you gave, or your violation flag doesn't match your L1 codes). Fix errors; look at warnings, and leave them only if you mean it.

## Tips

- Steps marked **NOT VISIBLE TO THE AGENTS** are placeholders: the benchmark's answer or pass/fail verdict is hidden while you code. Code what the agents did. Once you have finished coding **all 30**, you can look with `uv run afacs-render C07 --show-benchmark` (looking earlier could reveal a control and colour the traces still to come). Don't change your coding because of it; note anything interesting in `notes` instead.
- Text marked **Note added by AFACS** is not part of the log. It explains a logging artefact (e.g. OpenManus logs print only the first ~50 characters of the task, although the agents received all of it).
- Steps marked **framework log** are the software's bookkeeping, not an agent's words.
- An agent turn shown as "(empty message ...)" means the agent produced nothing. That is evidence.
- Long tool outputs (web pages, API documentation) can be skimmed. The evidence usually sits in the agent's reaction to them.
- If you can't decide between two codes, pick one, set confidence to `medium` or `low`, and write the alternative in `notes`. Disagreements like that are exactly what calibration is meant to surface.
