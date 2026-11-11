# Audit record: paper 08

Two independent AI reviewers (Claude, Anthropic), neither of which had seen the work being produced, reviewed working draft v0.1 on 11 November 2026 with access to the code, outputs and data. One covered statistics, reproducibility and pre-registration compliance. The other covered avionics, flight operations and human factors. Draft v0.2 is the revision.

## Confirmed

- Every number in v0.1 matched the output files.
- The reference, the classification and both confirmatory tests were re-implemented independently and matched exactly (H1 3.419, 2.941 to 3.976; H2 ratio 1.966).
- Hashes of the eight frozen files match the pre-registration commit `be41aa0`. The first study-day file was written 13 seconds after that commit.
- H1 survived conditional logistic and fixed-effects models (3.4 to 3.5), an airline-only reference (3.7), restriction to airport-dates with 90% coverage of both classes (3.7), and a worst case in which every unanalysed business-jet landing was error-free.
- Stuck or default-value transponders do not explain H1: 533 of 542 business-jet errors came from aircraft that broadcast other values on other flights.
- The cited facts about the 2022 Paris incident and the French study were confirmed. The revision date of EASA SIB 2023-03R1 could not be confirmed by the reviewer.

## Major findings and what changed

| Finding | Response in v0.2 |
| --- | --- |
| The registered "last value" measure picks up a spurious switch to 1013 around touchdown from a second, 0.1 hPa data source, mostly on European airliners (about half of European airline errors) | Verified. Registered results kept as run; a corrected measure (modal value, unstable landings excluded) added as a disclosed post hoc deviation and used for all descriptive claims |
| H2 and every Europe-versus-US statement depended on that artefact | H2 reported as registered (not supported) and as corrected (ratio 0.95). Regional statements rewritten. Agreement with EUROCONTROL withdrawn |
| About a third of business-jet errors of 10 hPa or more were corrupt broadcast values | Landings with three or more values in the window excluded. The 10 hPa odds ratio is reported with its interval and event counts and described as imprecise |
| "The gap widened with the size of the error" overstated; crude ratios do not widen below 10 hPa | Replaced with separate bands and a warning against reading a trend |
| The "five minutes before" contrast was a regional mix effect | Analysis and the inference drawn from it removed |
| "A large share of the gap is the standard setting" unsupported; the odds ratio of 13 unstable | Removed. Standard at landing redefined at 5 hPa and reported as about half of large business-jet errors |
| Abstract attached crude pooled rates to "same airport and day" | Crude rates labelled as crude; only the odds ratio carries the stratified claim |
| Most of H1 is discrepancies of 2.4 to 3.2 hPa that do not look like the Paris kind of error | Stated in the abstract and discussion |
| The effect shrinks with aircraft utilisation and varies as much between operators as between classes | Added (Table 3 and the operator paragraph) |
| Which altimeter the broadcast reflects is unknown; on single-pilot light jets it may be the unused side | Moved from a limitation to a co-equal explanation in the discussion |
| "The measure is direct" untenable | Removed; first limitation now says the opposite |
| "No indication" and "the error changes little on an ILS" could mislead | Reworded |

## Not resolved

- The source of the second data stream was not confirmed against the receiver software.
- The reference was not validated against weather reports.
- The corrected measure was chosen after seeing the problem; a second sample would be needed to confirm results on it.
- Operator and aircraft random-effects models, an other-station test for US small errors, and timing of when each error began were suggested and not done.
- Military and government callsigns were not removed from the airline class.
- The EUROCONTROL paper has still not been read in full.
- The reviewers' figures quoted in the paper (alternative models, the stuck-transponder check, coverage by type) were not all re-derived by the analysis author. The corrected-measure results were.

## Added 11 November 2026, after v0.2: weather-report check on the first sample (post hoc)

Hourly and special weather reports for 118 of the 119 airports (Iowa State University archive; Palm Beach missing from the download) were compared with the consensus reference for the first sample, using the script frozen for the replication (`code/rep_analysis.py`). Results are in `results/sample1_weather_check.json`.

- The consensus reference was within 1.0 hPa of the most recent weather report for 97.4% of 708,227 landings (96.9% in Europe, 97.7% in the US) and within 1.7 hPa for 99.9%.
- With the weather report as the reference in place of the consensus, the business-jet against airline odds ratio was 2.6 (2.3 to 3.0) at 2 hPa and 9.9 (6.5 to 15.1) at 5 hPa. This version includes about 18,000 business-jet landings that had no consensus reference.

This resolves the "reference was not validated against weather reports" item above for the first sample. The paper (v0.3) now reports it.

## Added 11 November 2026: replication on a second sample (v0.3)

Pre-registered in `PREREGISTRATION_REPLICATION.md` (commit 7306d3b, 14:39 UTC) before any of the second sample was downloaded. Code hashes in `code/HASHES_REPLICATION.txt` were verified immediately before the single analysis run. Results are in `results/replication.json`.

- **Days.** 29 of the 30 drawn days processed. 27 March 2026 failed at the extraction step (25-minute limit) and was replaced by the first reserve day, 25 March, as the plan provided. Download sizes for all 30 main days matched the published sizes. The reserve day's download overlapped a restart of the driver, so it was re-extracted from the complete download and the result was identical to the stored one (8,465,150 rows).
- **Blinding.** No outcome was computed on any second-sample day until all 30 were processed. The analysis script was run once.
- **Result.** R1 odds ratio 4.02 (3.47 to 4.65), inside the pre-set replication range of 2 to 6. R2 13.9 (8.9 to 21.8). R3 2.60 (2.11 to 3.20). R4 35 (16 to 78). All supported after Holm correction.
- **Weather-report check.** Consensus within 1.0 hPa of the latest report for 97.5% of 724,718 landings. With the report as reference: 2.77 (2.46 to 3.12) at 2 hPa, 9.4 (6.6 to 13.4) at 5 hPa.
- **Defect found in the frozen script.** In `us_vs_europe_err5` the keys `rate_eu_per1000`/`rate_us_per1000`, `ev_*` and `n_*` are transposed (the "eu" values are the US ones). The ratio is US over Europe (1.34, p = .22). The script was left unchanged; the paper takes the rates from `rates_region`.
- **Limit of the replication.** 99% of second-sample landings were by aircraft also present in the first sample, at the same 119 airports. The replication tests stability over new days and guards against post hoc choices; it is not an independent population.
- **Not re-reviewed.** The v0.3 additions (replication section and weather check) have not been through independent review.

Items above now resolved: reference validated against weather reports; corrected measure confirmed on a second sample. Still open: source of the second data stream; which altimeter the broadcast reflects; military and government callsigns in the airline class; EUROCONTROL paper not read in full (requested from an author).

## Third independent review (AI), 11 November 2026, and changes in v0.4

A third AI reviewer, which had not seen the work, reproduced every number in the replication section from the data, reproduced the random day draw, verified the code hashes, and re-derived R1 with its own code (4.02; conditional estimate 4.09). Its findings and the response:

| Finding | Response in v0.4 |
| --- | --- |
| Corrupt weather reports in the archive (e.g. 40.00 inHg at EGLL) inflate airline "errors" against the weather-report reference | Reports outside 940 to 1060 hPa and isolated spikes removed (25 reports). Weather-referenced 5 hPa odds ratio restated as 13.1 (frozen-script figure 9.4 shown and explained) |
| The weather-referenced "2.6 to 2.8" was a threshold artefact of the 0.8 hPa broadcast step; "more conservative" was not a fair description | Removed from the abstract and discussion. Matched-threshold (2.4 hPa) figure 4.0 reported. Weather check presented as a validity check |
| Landings whose value is off the 0.8 hPa grid (second source only) are 0.2% of European landings but about half of European errors of 5 hPa or more; a few old aircraft show 1013 on most landings | New Section 7 and Table 6 report rates with and without them. US against Europe conclusion changed: 2.8 times (sample 2) and 2.2 times (sample 1) on grid values. R1 to R3 unchanged; R4 reported both ways |
| Overclaims: "nearly all" 10 hPa errors from rarely seen aircraft; the "not renewed" explanation of small US discrepancies; 1013 "absent in types with integrated flight decks"; unhedged novelty claims | Each rewritten with second-sample figures (15 of 21; 24% and 11% matching a recent destination setting; 22 types). Novelty statements hedged in abstract and introduction |
| Missing registered reporting for sample 2: exclusions, airport-resampling intervals, four-plus sensitivity, 33 UTC dates, one unreadable trace file | Added |
| "This section is confirmatory" covered descriptive material | Scope narrowed to the four tests |
| Intervals too narrow given clustering by operator; two fractional operators are 26% of business-jet landings | Operator-level bootstrap intervals added to Table 5 and the abstract (R1 2.7 to 5.4) |
| Implausible large business-jet values | Sensitivity excluding non-standard values 30 hPa or more from reference added (R2 13.0) |
| Body text did not say the reviewers were AI | Stated in the abstract, date line, Section 3, limitations and acknowledgement |
| README stale | Rewritten |

Re-derived by the analysis author (`code/posthoc_after_review3.py`): cleaned weather results, grid/off-grid rates and tests, operator, airport and aircraft bootstrap intervals, exclusion counts, the 10 hPa counts, aircraft overlap between samples, the share of small US discrepancies matching a recent destination report, and 1013-at-landing by type. The author's weather cleaning found 25 bad reports against the reviewer's 80; the resulting odds ratios agree (13.1).

Quoted from the reviewer and NOT re-derived: the identification of the off-grid aircraft types (A300-600, 737 Classic); the trace inspection of the 35 business-jet 1013 events and of the implausible large values; the higher second-sample rate among business jets with a first-sample error (14.3 against 8.5 per 1,000).

## Still open after v0.4

- No human peer review. All review has been by AI.
- EUROCONTROL paper (Mourousias et al.) not read in full; a copy has been requested from an author. The reviewer recalled, without verifying, UK NATS/CAA monitoring of barometric pressure settings; not searched.
- Which altimeter the broadcast reflects on each business-jet type: needs human avionics input.
- The second source is identified only by an approximate grid test, not by decoding message types.
- Military and government callsigns remain in the airline class.
- No mixed-effects model; clustering handled by bootstrap only.
- What the 2 to 5 hPa discrepancies are (other-station settings were not tested).
- Timestamps are git commit times; no external registry (OSF or Zenodo) yet.
