# 08 · Landing on the Wrong Altimeter Setting

**Status:** working draft v0.8 (12 November 2026). Two pre-registrations (first sample; replication). Reviewed by three independent AI reviewers and one AI consistency check; not peer reviewed.

A study using open ADS-B data (adsb.lol) of how often aircraft land with the broadcast altimeter setting differing from the local setting, at 119 US and European airports, in two pre-registered samples of 30 days in 2026 (about 714,000 and 730,000 landings).

**Findings.** Compared at the same airport on the same day, business jets had about 3.5 to 4 times the odds of airline jets of landing with a setting at least 2 hPa from the consensus of other aircraft (second sample, pre-registered: 4.0, interval 3.5 to 4.7, or 2.7 to 5.4 resampling operators), and about 14 times for 5 hPa or more. The result is the same with the airport weather report as the reference. Nine in ten discrepancies are of 2 to 5 hPa and may not be operational errors. Overall rates in the second sample were 2.0, 0.19 and 0.06 per 1,000 landings at 2, 5 and 10 hPa. About half of the large errors recorded in Europe come from a few older aircraft through a second data source; without them, errors of 5 hPa or more were two to three times as frequent in the US as in Europe (post hoc). The first sample's second hypothesis (more "standard left set" in Europe) was not supported.

**Read first:** the abstract, Section 2.6 and the Discussion of [`paper.pdf`](paper.pdf), then [`AUDIT.md`](AUDIT.md).

| File | What it holds |
| --- | --- |
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | Plan, committed before any altimeter data from the study days was read (commit `be41aa0`) |
| `code/` | Frozen code (`HASHES.txt`), plus the post hoc scripts `posthoc_modal_extract.py`, `posthoc_after_review.py` and `make_figure.py` |
| `results/` | `confirmatory.json` and `secondary.json` (registered measure); `modal_*.json` and `after_review.json` (corrected measure, post hoc) |
| [`PREREGISTRATION_REPLICATION.md`](PREREGISTRATION_REPLICATION.md) | Plan for the second sample, committed before it was downloaded (commit `7306d3b`); `code/rep_analysis.py`, `code/HASHES_REPLICATION.txt`, `results/replication.json` |
| `results/after_review3_*.json` | Post hoc checks after the third review (`code/posthoc_after_review3.py`): weather reports cleaned, value source, clustered intervals |
| `results/pooled.json` | Both samples pooled, for the descriptive tables (`code/pooled_analysis.py`); exploratory |
| [`AUDIT.md`](AUDIT.md) | The three independent AI reviews and what changed |
| [`sources.md`](sources.md) | How each reference was checked |

**Open points.** The PDF was built with a fallback reference style (`ieeetr`) because `IEEEtran.bst` was not available where it was built; rebuild with `papers/_build/build.sh`. The processed landing tables are not in the repository. The EUROCONTROL paper has not been read in full. The weather-report files (Iowa Environmental Mesonet) are not in the repository. See "Still open" in `AUDIT.md`.

AI assistance: design, code, analysis and drafting by Claude (Anthropic) under the author's direction.
