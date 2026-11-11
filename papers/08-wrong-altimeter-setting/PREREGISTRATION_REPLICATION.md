# Preregistration: replication on a fresh sample, with the corrected measure

Author: James Le Cuirot, with analysis by Claude (Anthropic). Frozen 11 November 2026 (UTC), before any data for the days listed here was downloaded. The time of the Git commit that adds this file is the registration time.

## 1. Why

The first study ([`PREREGISTRATION.md`](PREREGISTRATION.md)) supported its main hypothesis, but independent review found that its measure, the last altimeter setting recorded before landing, picks up a spurious switch to 1013 around touchdown on some aircraft. A corrected measure was chosen after seeing that problem, so every result on it is post hoc. This replication fixes the corrected measure in advance and tests it on days that have not been downloaded or examined. It also adds a check of the reference against weather reports.

## 2. Hypotheses

On the corrected measure, comparing business jets with airline jets at the same airport on the same UTC date:

- **R1 (primary).** Business jets have higher odds of landing with the setting 2 hPa or more from the reference. First sample, post hoc: odds ratio 3.5.
- **R2.** The same for 5 hPa or more. First sample, post hoc: 8.6.
- **R3.** The same as R1 among aircraft with ten or more analysed landings in the sample. First sample, post hoc: 2.6.
- **R4.** Business jets have higher odds of landing with 1013 selected when the reference is at least 5 hPa from standard. First sample, post hoc: 32, very imprecise.

Estimation aims: rates at 2, 5 and 10 hPa by region and class, and the ratio of the US to the European rate at 5 hPa or more.

## 3. Data and sample

- **Source, airports, aircraft types, landing detection:** as in the first study, using the same frozen code (`extract.py`, `approaches.py`, `actypes.py`, `candidates.txt`).
- **Days.** Thirty UTC days drawn at random (NumPy `default_rng`, seed 20261111) from the 263 eligible days between 1 January and 31 October 2026 that were neither used nor held in reserve by the first study. The list and six ordered reserve days are in `code/days_replication.json`. Days: 2026-01-01, 01-02, 01-08, 01-09, 01-17, 01-20, 01-30, 02-09, 02-17, 02-19, 03-08, 03-17, 03-18, 03-19, 03-27, 04-13, 04-20, 04-22, 05-17, 07-04, 07-16, 07-20, 07-22, 08-06, 08-12, 08-14, 08-27, 08-29, 09-06, 10-21. A day that cannot be downloaded or processed is replaced by the next reserve: 2026-03-25, 09-19, 01-29, 06-20, 03-07, 03-06.
- **Stopping rule.** All 30 days are processed before any result is computed. Each download is checked against its published size.

## 4. Measures

- **Setting at landing (corrected).** The most frequent value of the recorded altimeter setting in the 120 seconds before the last airborne point. The landing is excluded if three or more different values were recorded in that window, or if the value is outside 940 to 1060 hPa.
- **Reference, QFE rule, suspect-aircraft rule:** as in the first study.
- **Difference.** Setting minus reference, rounded to 0.1 hPa. Thresholds 2, 5 and 10 hPa.
- **Standard at landing.** Setting within 0.5 hPa of 1013.25 and at least 5 hPa from the reference; eligible landings are those whose reference is at least 5 hPa from standard.

## 5. Analysis

- **R1 to R4.** Mantel-Haenszel common odds ratio across strata of airport × UTC date, Cochran-Mantel-Haenszel test, Robins-Breslow-Greenland 95% interval, and for R1 and R2 an interval from resampling whole airports. Two-sided tests at 0.05 with Holm correction across the four. A hypothesis is supported if its adjusted p is below 0.05 and the odds ratio is above 1. An odds ratio between 0.9 and 1.1 is treated as negligible.
- **Replication criterion.** R1 counts as replicated if it is supported and its odds ratio lies between 2 and 6.
- **Reporting.** Coverage and exclusions by class and region first. Absolute rates beside every ratio. Event counts beside every rate.
- **Sensitivity (not confirmatory):** errors of 2 to 5 hPa only; 10 hPa or more; aircraft with four or more and twenty or more landings; a reference from ten or more aircraft with over 95% agreement; the US and Europe separately; strata including the hour.

## 6. Weather-report check

If hourly weather reports for the 119 airports can be obtained (Iowa State University archive, altimeter setting field), then for each landing the most recent report within 70 minutes is compared with the reference. We report the share of references within 1.0 hPa of the report, by region, and rerun R1 and R2 with the report as the reference in place of the consensus. This is a validity check, not a hypothesis. If the reports cannot be obtained, the paper will say so. The same check will be run on the first sample and labelled post hoc there.

## 7. Limitations known in advance

Those of the first study apply, in particular: which altimeter the recorded value reflects is not defined, so on some aircraft a wrong value may not be the setting the crew flew on; the recorded value mixes two sources; broadcast is optional in the US and a third of business-jet landings cannot be analysed; small differences include settings that were correct when set; approach type, weather and crew are unknown. European weather reports give the setting in whole hectopascals rounded down, and US reports to 0.01 inHg, so agreement within 1 hPa is the most that can be expected.

Frozen code hashes are in `code/HASHES_REPLICATION.txt`.
