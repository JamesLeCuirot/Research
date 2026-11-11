# Preregistration: How often do crews land with the wrong altimeter setting, and who does?

Author: James Le Cuirot, with analysis by Claude (Anthropic). Frozen 11 November 2026 (UTC), before any altimeter-setting data from the study days was read. The time of the Git commit that adds this file is the registration time.

## 1. Status and what has been looked at

**Data already held.** The study uses 30 days of open ADS-B data that were downloaded and processed on 10 and 11 November 2026 for an earlier, unrelated study of approach stability. That study detected landings and measured flight path. It never read the altimeter-setting field for any analysis, and no altimeter-setting value from those 30 days has been examined.

**Pilot day.** The method was built on one pilot day, 30 December 2025, which is outside the study sample. On that day we looked only at results pooled across all aircraft:

- 97% of 28,327 landings broadcast an altimeter setting in the last two minutes.
- 3.1 per 1,000 landings differed from the reference by 2 hPa or more, and 0.28 per 1,000 by 10 hPa or more.
- Most 2 hPa differences were exactly 2.4 hPa (three steps of the 0.8 hPa broadcast resolution) and bunched at airports where pressure was rising quickly.

The analysis code was run on the pilot day with aircraft class and region labels randomly shuffled (seed 7) to confirm it executes. No result split by true class or true region has been computed on any day.

**Frozen code.** SHA-256 hashes are in `code/HASHES.txt`. Any later change to the frozen files will be reported as a deviation.

## 2. Background and what this adds

Two studies have measured this, both in Europe. The French DSAC/DSNA study (1,694,266 landings at six French airports, 2019 to 2023, Mode S radar) found a difference of 2 hPa or more on about 1.3 per 1,000 landings and 10 hPa or more on about 0.23 per 1,000, with Le Bourget three times CDG and no explanation beyond "very different fleets". A EUROCONTROL study (Mourousias, Robert and De Smedt, ICNS 2025) reportedly found 196 errors above 5 hPa in 747,353 flights at 378 European airports; we could not read its full text. We found no published rate for the United States, no comparison of business aviation with airlines, and no comparison of regions.

## 3. Hypotheses

- **H1 (primary).** Business jets have higher odds than airline jets of landing with the altimeter setting 2 hPa or more from the local setting, compared at the same airport on the same UTC date.
- **H2.** Landing with the standard setting (1013 hPa) still selected is more frequent at European airports than at US airports, among landings where the local setting was at least 3 hPa from standard.

Estimation aim, not a hypothesis: the rate of differences of 2, 5 and 10 hPa or more, overall and by region, for comparison with the two European studies.

## 4. Data and sample

- **Source.** adsb.lol open archive of daily ADS-B traces (ODbL), "planes-readsb-prod-0" releases. Airport data from OurAirports.
- **Days.** The 30 UTC days of the earlier study: 29 of the 30 days drawn at random with seed 20261110 from 1 January to 31 October 2026, plus the first reserve day (24 June) in place of 4 April, which could not be processed. The list is in `code/days.json`. Days are 2026-01-03, 01-12, 01-13, 01-23, 01-24, 01-27, 01-28, 02-04, 02-14, 03-01, 03-05, 03-11, 03-12, 04-11, 04-12, 04-16, 05-12, 06-01, 06-06, 06-24, 06-30, 08-19, 09-04, 10-06, 10-09, 10-11, 10-14, 10-25, 10-26, 10-27.
- **Airports.** The fixed list of 119 US and European airports in `code/candidates.txt`.
- **Aircraft.** 65 business-jet types and 58 airline jet types in `code/actypes.py`. Airline-type aircraft are kept only with an airline-format callsign (three letters then a digit).
- **Landings.** As detected by the earlier study's frozen code (`code/approaches.py`): the last airborne point of a track aligned with a runway, followed by ground movement or no later climb.
- **Stopping rule.** All 30 days are processed before any result split by class or region is computed.
- **Expected size.** About 800,000 landings, roughly 95,000 by business jets. At an airline rate near 3 per 1,000 this detects an odds ratio of about 1.25 or more for H1.

## 5. Measures

- **Setting at landing.** The last altimeter setting broadcast by the aircraft (ADS-B target state, field `nav_qnh`, resolution 0.8 hPa) in the 120 seconds before its last airborne point. Values outside 940 to 1060 hPa are treated as implausible and dropped.
- **Reference setting.** The median setting at landing of other aircraft landing at the same airport within 30 minutes either side. It needs at least five other aircraft, with at least 60% of them within 1.0 hPa of their median; otherwise the landing has no reference and is excluded.
- **Difference.** Setting at landing minus reference.
- **Error thresholds.** 2 hPa or more (primary), 5 hPa or more, 10 hPa or more. Because of the 0.8 hPa resolution, 2 hPa in practice means three steps (2.4 hPa).
- **Standard left set.** Setting within 0.5 hPa of 1013.25 while differing from the reference by 2 hPa or more.
- **QFE-like.** At airports 300 ft or more above sea level, a setting within 1.5 hPa of station pressure. These landings are excluded and counted.
- **Suspect avionics.** An aircraft with four or more landings of which at least half differ by 2 hPa or more is assumed to broadcast an unreliable value. All its landings are excluded from the main analysis and counted. This rule is applied without regard to class.

## 6. Analysis

**Confirmatory**

- **H1.** Mantel-Haenszel common odds ratio of an error of 2 hPa or more, business jet against airline jet, across strata of airport × UTC date. Cochran-Mantel-Haenszel test. Robins-Breslow-Greenland 95% interval, plus a percentile interval from resampling whole airports (2,000 replicates, seed 1).
- **H2.** Ratio of the rate of "standard left set" at European airports to the rate at US airports, among eligible landings. Two-sided p-value from permuting the region label across airports (10,000 permutations, seed 1); 95% interval from resampling airports within region.
- **Decision rule.** Two-sided tests at 0.05 with Holm correction across H1 and H2. A hypothesis is supported if its adjusted p is below 0.05 and the effect is in the predicted direction. A significant effect in the opposite direction is reported as evidence against it. An H1 odds ratio between 0.9 and 1.1 is treated as negligible whatever its p-value.
- **Reporting.** Absolute rates per 1,000 landings are given beside every ratio. Coverage (share of landings broadcasting a setting, share with a reference) and every exclusion are reported by class and region before the results.

**Sensitivity (H1)**: thresholds of 3, 5 and 10 hPa; excluding periods when the reference changed by 1.5 hPa or more in an hour; a 15-minute reference window; including suspect aircraft; aircraft with three or more landings only; US and Europe separately; strata of airport × date × hour and of airport only; ground-confirmed landings only; leaving out each airport in turn. For H2: each class separately, and eligibility at 5 hPa from standard.

**Exploratory**: direction of error (set too high puts the aircraft lower than indicated); the distribution of error sizes by region, including slips of 10 hPa and of one inch of mercury; standard left set by class; day against night; pressure far from standard; rising or falling pressure; whether the setting was already wrong five minutes before landing; within business jets, light against large types and registration against company callsigns; aircraft type; individual airports, including Le Bourget against CDG and Orly; the European rate above 5 hPa for comparison with EUROCONTROL.

All of these are implemented in `code/qnh_secondary.py`, frozen with this document. Anything else will be labelled post hoc.

## 7. Known limitations, stated in advance

- **The reference is inferred.** It is the consensus of other aircraft, not the value ATC issued. If ATC or the ATIS gave a wrong value to everyone, the study cannot see it. Weather reports are not used.
- **Lag is counted as error.** When pressure changes quickly, a crew holding a correct but older value is counted. The sensitivity analysis on changing pressure addresses this.
- **Resolution.** At 0.8 hPa per step, a 2 hPa threshold cannot be applied exactly.
- **Broadcast is optional in the US.** Aircraft that do not broadcast a setting are missing, and coverage may differ by class and age of avionics.
- **What the field represents.** It is the setting selected on one altimeter or flight guidance side; which side is not defined. Some avionics may broadcast stale values. The suspect-avionics rule catches only aircraft with four or more landings, which favours airline aircraft.
- **Small airports are excluded** where fewer than five other aircraft land within the hour.
- **No approach type, minima or consequence.** The study measures the setting, not terrain clearance.
- **Operator type is inferred** from aircraft type and callsign.
- **Sample.** Thirty days in 2026, none in July; 119 airports chosen by judgement and weighted to the US.
