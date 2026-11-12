# Audit record: paper 08, shutdown and go-around rates

Two independent AI reviewers examined draft v0.1 on 12 November 2026. Neither saw the paper being written, and neither could edit the repository. Their full reports are in `audit/review_statistics.md` and `audit/review_flight_operations.md`; the scripts they wrote are in `audit/scripts_statistics/` and `audit/scripts_flight_operations/` (kept as written; they use absolute paths from the review workspace). Draft v0.2 is the revision. The findings the paper relies on were re-computed with this repository's own code (`code/post_review.py`, `code/post_review_ops.py`).

## What the reviewers confirmed

- All 11,592 airport-day rows in `results/airport_day.csv` rebuild exactly from the raw per-day files with independent code, including the exclusion rules and the weekday alignment.
- Every point estimate in `results/results.json` and `results/supplementary.json` reproduces with independent code; intervals agree within 0.02.
- The weather covariates rebuild exactly from the raw METAR files (13,271 of 13,271 airport-days).
- The preregistered decision logic is implemented as registered and the primary verdict, "inconclusive", is correct.
- About 90% of detected US go-arounds are followed by a landing by the same aircraft at the same airport within 30 minutes; the hour-of-day, operator and aircraft-type patterns look like line flying; the training-flight screen is adequate.
- The pooled primary estimate stays between about 0.88 and 1.08 under every restriction either reviewer tried.

## Findings and what was done

| # | Finding | Reviewer | Action in v0.2 |
|---|---|---|---|
| 1 | The TCAS RA result (0.73) is driven by a change in the archive's logging of RA messages on 26–27 September 2024, at the boundary of the 2024 baseline. With a post-change baseline the ratio is 1.01. | Statistics | Reproduced. RA result reported as an artefact; removed as a finding from the abstract and summary. |
| 2 | San Francisco and Burbank supply 47% of 2024-window RA events; both had procedure changes between the two autumns. | Operations | Reproduced the shares and rates. Section rewritten; procedure changes cited to a trade report (SFO) and an FAA document (Van Nuys). |
| 3 | "14 of 76 airports, about four expected by chance" used the wrong benchmark; the registered Holm correction was not applied. | Statistics | Reproduced: 17 at 5% on the exact test, 10–11 expected under no change, one airport (IAD) after Holm. Text replaced. |
| 4 | Most large single-airport changes are runway closures, runway-detection gaps, configuration or RA-linked go-arounds (BOS, BNA, CVG, SAN, SFO and others). | Operations | Reproduced the runway-end screen (10 airports), Boston and San Diego runway counts, SFO RA-linked counts. Airport list replaced by explanations; exclusion added as a robustness row. |
| 5 | "Excludes a rise above about 13%" was overstated: it assumes a comparison the placebo rejects, and neighbouring days are correlated. | Statistics | Removed from "It shows"; stated as conditional. Block-bootstrap interval added. |
| 6 | The placebo failure runs through 1–14 October (0.67) and is absent afterwards (1.09). "The two bracket the answer" was unsupported. | Statistics | Reproduced; added; bracket sentence removed. |
| 7 | The control airports' apparent rise is entirely go-arounds below 200 ft, at airports where low-level coverage improved. | Operations | Reproduced. Added as a results paragraph and a robustness row (1.03; 0.87–1.22). |
| 8 | The detector counts RA climb-outs as go-arounds; these fell sharply at SFO. | Operations | Reproduced (237 vs 86 in the window). Added as a robustness row and to the method description. |
| 9 | The weather-adjusted estimate (0.81) depends on equal weather effects in both groups, which the data reject. | Statistics | Reproduced (0.87; 0.74–1.04 with separate effects). Now given as the reason for not reading 0.81 as a fall. |
| 10 | Coverage changed more than the paper said (about 1.8 times the positions per aircraft; confirmed landings 47% to 62%). | Both | Reproduced from the extraction logs and raw files; stated with direction. |
| 11 | The spacing measure tracks how low the leader was seen; "points that way" was too strong; the median moved the other way. The registered airport-resampled interval for the main spacing estimate had not been run. | Both | Reproduced. Section rewritten; closing sentence deleted; airport-resampled interval added (0.65–0.91). |
| 12 | Background lacked the upstream mechanisms; wording treated a lower go-around rate as better; "abandoned" approaches. | Operations | Rewritten. |
| 13 | Number and wording slips: 4.5 vs 4.4 million approaches; SE 0.044 vs 0.045; median 4.22 vs 4.21; hurricane placement; flight-cut percentages; RA reception sentence. | Both | Corrected. |
| 14 | Registered items missing from the paper: "Clear of Conflict" RA sensitivity; oversize-file count; nearest-airport RA assignment departs from the registered wording. | Statistics | Added; departure listed. |

## Unresolved

1. **Which autumn was unusual.** US go-around rates were higher in September and early October 2024 than in 2025 at 40 of 50 airports, including in good weather. The cause is only partly identified. A third year is needed.
2. **Coverage.** The 2025 archive has about 1.8 times the positions per aircraft near the study airports. The restriction to go-arounds at or above 200 ft is a partial remedy. A clean fix needs the 2025 traces thinned to the 2024 density and reprocessed; the raw point files were deleted after processing to save disk, so this means downloading the days again.
3. **A valid RA estimate.** Only five baseline days follow the 2024 logging change. The cause of that change was not established with the archive's maintainers.
4. **Runway availability.** Ten airports have a runway present in one year only. Whether each was closed or not received was checked against an outside source only for Boston, and that source does not name the runway.
5. **Operational facts from the review that were not checked against primary records:** the dates of the Van Nuys pattern changes and of the revised San Francisco procedure; the Cincinnati runway closure; a Las Vegas runway configuration in September 2024; the weather in the last week of October 2025; European and Canadian disruptions other than the one cited. Several rest on search-result headlines only.
6. **Reviewer analyses not re-computed here:** hour-by-hour weather matching (IFR share of approaches), the good-weather excess by airport, threat-aircraft pairing at San Francisco, RA message types, and the 30-minute landing follow-up. These appear in the paper only as attributed statements or not at all.
7. **Serial correlation.** The registered bootstrap resamples single days. Block resampling widens the primary interval to 0.74–1.18; the registered interval is still the one the verdict uses.
8. **Go-around detection has no ground-truth validation** at these airports, and the reason for each go-around is unknown.
9. **Reference checks.** `papers/_build/check_bib.py` was not run (it needs network access this workspace lacks), and the PDF was built with the `IEEEtranM` style because `IEEEtran.bst` could not be installed. Rebuild with `papers/_build/build.sh`.
10. **The author has not yet read the raw tracks** behind any result, and the preregistration is time-stamped only by the repository commit.
