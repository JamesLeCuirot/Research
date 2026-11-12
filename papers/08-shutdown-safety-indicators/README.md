# Paper 08: Did the 2025 US government shutdown change go-around rates?

**Status:** Working draft v0.2, 12 November 2026. Preregistered; analysed; revised after two independent AI reviews. Not yet read by the author against raw tracks.

## Result in brief

- Go-around rate at 50 US airports: 4.77 per 1,000 approaches (same weekdays 2024) and 4.64 (shutdown, 1 Oct–12 Nov 2025). Control airports (Canada, Europe): 3.44 and 3.66.
- Preregistered estimate (ratio of rate ratios): 0.93, 95% interval 0.76 to 1.13. Verdict under the registered rules: **inconclusive**. No change detected; interval too wide to declare no meaningful change.
- The September placebo failed (0.78; 0.66 to 0.93), and the same gap runs through 1–14 October. Adjusted for September: 1.19 (0.91 to 1.53).
- Robustness checks added after review lie between 0.90 and 1.08; all intervals include 1.
- The two secondary measures (tight landing pairs, TCAS RAs) gave statistically clear falls that are artefacts of receiver coverage, an archive logging change and local procedure changes. No conclusion is drawn from them.

## Files

| File | What it is |
|---|---|
| `PREREGISTRATION.md` | Registered 11 Nov 2026 (commit `bfb0eae`) before any study data were downloaded. Section 11 lists the addendum and all departures. |
| `paper.tex`, `paper.pdf`, `references.bib`, `figures/` | The paper. |
| `sources.md` | How each reference was checked. |
| `AUDIT.md`, `audit/` | Review record, the two reviewers' full reports and their scripts. |
| `code/run_day.sh`, `run_all.sh`, `extract.py`, `approaches.py` | Download and processing, one day at a time. |
| `code/analysis.py` | The preregistered analysis (committed before use, run once). |
| `code/weather.py` | Airport-day weather covariates from METAR. |
| `code/supplementary.py`, `post_review.py`, `post_review_ops.py` | Post-hoc: registered items the analysis script omitted, and exploratory checks. |
| `code/figures.py` | Figures. |
| `results/airport_day.csv` | Airport-day counts (approaches, go-arounds, pairs, tight pairs, RA events). |
| `results/*.json`, `weekly.csv`, `acas_daily.csv` | Outputs. |
| `data/weather_airport_day.csv` | Weather covariates. |

The raw archive (about 550 GB) and the per-day attempt files are not in the repository. `code/run_day.sh` rebuilds a day from the public archive.

## Open questions and next steps

1. Lodge the preregistration on OSF if a registry record is wanted. It will post-date the results, so say so.
2. Read a sample of raw tracks behind the go-arounds, especially at the high-rate airports.
3. A third comparison year, to settle whether autumn 2024 or autumn 2025 was unusual.
4. Reprocess with 2025 thinned to 2024 density, to remove the coverage difference.
5. Facility-level staffing exposure from the FAA command-centre advisories, if the archive can be retrieved.
6. Rebuild the PDF with `papers/_build/build.sh` and run `check_bib.py` (neither could be run in the analysis workspace; see `AUDIT.md`).

## Revision log

- v0.1, 12 Nov 2026: first draft from the preregistered analysis.
- v0.2, 12 Nov 2026: revised after independent statistical and flight-operations reviews. RA and spacing results reclassified as artefacts; per-airport claims replaced; robustness checks added; conditional wording on the upper limit; background and wording corrected.
