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
