# Pre-registration: go-around rates, final-approach spacing and TCAS resolution advisories at US airports during the October–November 2025 federal government shutdown

**Study:** paper 08 (working folder `papers/08-shutdown-safety-indicators`)
**Author:** James Le Cuirot
**Registered:** 11 November 2026, committed to this repository before any study-window data were processed. The git commit timestamp is the registration record. (An OSF registration, if lodged, will be linked here.)
**Status of data at registration:** no archive day inside the study windows (section 4) has been downloaded or processed. The pipeline was built and tested on three days outside the windows (20 August 2025, 14 and 21 August 2024), looking only at pooled outputs (section 9).

Any change after registration is listed in section 11 with its reason, and every result from a changed analysis is labelled as such in the paper.

---

## 1. Background and question

The US federal government was shut down from 1 October 2025 until the evening of 12 November 2025 (43 days). Air traffic controllers worked without pay. Facilities reporting staffing shortfalls ("staffing triggers") rose through October to a record 81 on 8 November. From 7 November the FAA ordered scheduled domestic flight reductions at 40 "High Impact Airports" (4%, then 6% from 11 November, 3% from 15 November, cancelled at 06:00 EST on 17 November), banned most general aviation at 12 of them from 10 November, and allowed understaffed facilities to withhold some services to VFR traffic. The FAA and the Secretary of Transportation said safety data showed more losses of separation, runway incursions and pilot reports of strain. No figures were published.

A literature and news scan on 11 November 2026 found studies of delays and cancellations during the shutdown (notably Richmond Fed Economic Brief 25-45) but no study that measured safety indicators with flight-track data. The scan did not individually search Google Scholar, SSRN, TRB or AIAA proceedings; a final sweep will be run and dated before the paper is written.

**Question.** Did measurable safety indicators at US airports change during the shutdown, relative to the same airports a year earlier and to airports outside the United States?

## 2. Hypotheses

The direction of any effect is uncertain. Controller strain could raise go-arounds through spacing errors; traffic management initiatives and flight cuts lowered traffic density, which could reduce them. All tests are two-sided.

- **H1 (primary).** The go-around rate at US study airports during the shutdown (1 October–12 November 2025) changed relative to the same weekday-aligned dates in 2024 by a different factor than at the non-US control airports.
- **H2 (secondary, spacing).** The share of tightly spaced arrival pairs on final approach at US study airports changed over the same comparison.
- **H3 (secondary, TCAS).** The rate of TCAS resolution advisories near US study airports changed during the shutdown relative to the September baseline, compared with the same contrast in 2024.

**Author's stated expectation, recorded before the data:** H1 will show no change (a flat result); spacing is the indicator most likely to move, toward wider spacing; the TCAS analysis will be the least precise.

A flat result is a legitimate finding and will be reported as such, with the size of change the study could exclude (section 8).

## 3. Data

**Source.** adsb.lol open ADS-B archive (Open Database Licence), daily GitHub releases `adsblol/globe_history_2024` and `globe_history_2025`, tag `vYYYY.MM.DD-planes-readsb-prod-0`. Every day in the study windows is listed in the releases index for both years.

**Download integrity.** Each part is re-requested with `curl -C -` until the server returns HTTP 416; all parts (`.aa`, `.ab`, `.ac`, `.ad` where present) are fetched; the total size must match the published size to within 2 MiB or the day is rejected and re-fetched. A day with fewer than 20,000 trace files is rejected. Compressed trace files over 30 MB, or expanding beyond 150 MB, are skipped and counted.

**Airports (fixed; `code/airports_study.csv`).**
- *US40* (40): the FAA order's Appendix A airports.
- *USOTHER* (15): AUS, BNA, MSY, RDU, SJC, SMF, STL, MCI, CLE, PIT, BUR, SNA, SAT, CMH, JAX.
- *Control* (29): Canada YYZ, YVR, YUL, YYC; Europe LHR, LGW, MAN, STN, AMS, FRA, MUC, BER, DUS, CDG, ORY, MAD, BCN, FCO, MXP, ZRH, GVA, VIE, CPH, ARN, OSL, HEL, DUB, BRU, LIS.

**Aircraft (fixed; `code/actypes.py`).** Airline jets and business jets by ICAO type designator. Other types are not processed.

**Reference data.** OurAirports `airports.csv` and `runways.csv` as downloaded on 11 November 2026.

**Weather.** At registration no historical METAR source is reachable from the analysis workspace. See section 7.4.

## 4. Study windows

Dates are UTC archive days. The 2024 comparison dates are the 2025 dates minus 364 days, so weekdays align.

| Window | 2025 | 2024 comparison | Days per year |
|---|---|---|---|
| Baseline | 1–30 September | 2 September–1 October | 30 |
| **Shutdown (primary)** | 1 October–12 November | 2 October–13 November | 43 |
| Phase A: strain, no order | 1 October–6 November | 2 October–7 November | 37 |
| Phase B: order in force | 7–16 November | 8–17 November | 10 |
| Peak strain | 31 October–9 November | 1–10 November | 10 |

Days processed: 1 September–16 November 2025 and 2 September–17 November 2024 (77 days each, 154 in total).

## 5. Measures

All detection code is in `code/approaches.py`. The landing and go-around logic is carried over unchanged from the author's previous study, where it was validated by inspection of individual tracks.

**Approach attempt.** A landing or a go-around by a study aircraft at a study airport.

**Landing.** The last airborne position of a visit, on short final to a runway (within 150 m of the centreline, under 700 ft above the threshold, track within 15° of the runway), after a descent of at least 1,500 ft, followed by a ground position on that runway or by no further airborne data.

**Go-around.** A local altitude minimum below 3,000 ft above the airport, aligned with a runway (within 0.5 NM laterally, between 6 NM before and 1.5 NM past the threshold, track within 30°), preceded by a descent of at least 800 ft and followed by a climb of at least 500 ft, with continuous data and no ground contact.

**O1 (primary): go-around rate** = go-arounds ÷ (landings + go-arounds), reported per 1,000 approaches.

**O2: tight-pair share.** For each landing followed within 400 s by another aircraft landing on the same runway, the follower's distance from the threshold at the moment the leader was last seen airborne, where the follower's track brackets that moment within 30 s. *Tight-pair share* = pairs with follower distance under 2.5 NM ÷ all measured pairs. The median follower distance is reported alongside.

**O3: TCAS RA rate.** RA events are taken from the archive's daily ACAS file (`acas/acas.json.gz`, downlinked resolution advisory messages). An *event* is the first RA message from an aircraft after at least 120 s without one. Events count if the aircraft is in the study type sets, has a position, and is within 15 NM of a US study airport and below 7,000 ft above it. Rate = events ÷ 1,000 detected approaches at that airport-day.

## 6. Exclusions (fixed before the data)

1. **Training, test and flight-inspection flights.** If one aircraft makes three or more go-arounds at one airport on one UTC day, all of its approach attempts at that airport that day are removed. Callsigns beginning `FLC` (FAA flight inspection) are removed. The number removed is reported.
2. **Thin airport-days.** An airport-day with fewer than 30 detected approaches is dropped.
3. **Poorly covered airports.** An airport is excluded from all analyses if, in either year, fewer than 60 of its 77 days pass rule 2. This rule uses approach counts only, not outcomes. Excluded airports are listed.
4. **Failed days.** A day that cannot be downloaded intact after repeated attempts is dropped together with its weekday-aligned partner in the other year.

## 7. Analysis

The unit is the airport-day. Counts are summed to airport-day level after exclusions.

### 7.1 Primary analysis (H1)

Estimand: the ratio of rate ratios

RRR = (rate US 2025 ÷ rate US 2024) ÷ (rate control 2025 ÷ rate control 2024)

over the shutdown window, with US = US40 + USOTHER and control = Canada + Europe.

Estimator: Poisson regression of go-around counts on airport fixed effects, year, and year × US, with log approaches as offset, on airport-days in the shutdown window. The coefficient on year × US is log RRR.

Reported beside it: the four pooled rates per 1,000 approaches, the two year-over-year rate differences, and the difference-in-differences of rates per 1,000.

Interval: 95% percentile interval from 2,000 bootstrap resamples of weekday-aligned day-pairs (a 2025 day and its 2024 partner are resampled together, with all airports). A second interval from resampling airports (within group) is reported; if the two disagree about whether the interval excludes 1, the wider is used for the conclusion.

Decision rules:
- **Change detected** if the 95% interval for RRR excludes 1.
- **No meaningful change** if the 95% interval lies entirely within 0.80–1.25.
- Otherwise **inconclusive**, reported with the interval.

### 7.2 Validity check and robustness for H1 (reported whatever they show)

- **September placebo.** The same RRR computed on the baseline window. An interval excluding 1 would mean US and control airports were already diverging year-over-year before the shutdown, and the primary result would be flagged accordingly.
- **Baseline-adjusted estimate.** RRR(shutdown) ÷ RRR(baseline), which removes any year-over-year change specific to US airports that was already present in September (for example, differential growth of the receiver network).
- **By phase:** Phase A, Phase B, peak strain.
- **By airport group:** US40 and USOTHER separately against control; and in Phase B, US40 against USOTHER.
- **Airline jets only.**
- **Control group variants:** Europe only; Canada only.
- **Leave-one-airport-out** range of the primary RRR.
- **Without exclusion rule 1.**

### 7.3 Per-airport variation

For each US airport: go-around rate per 1,000 in each year's shutdown window, the rate difference, the rate ratio with an exact conditional interval, shown as a forest plot. Between-airport heterogeneity is summarised with a random-effects variance. Per-airport results are descriptive; no airport is singled out as significant without Holm adjustment across airports.

### 7.4 Weather

Go-around rates depend strongly on weather. The design addresses this through the year-over-year and control-airport comparison and through day-level resampling, not through direct adjustment. If hourly METAR for the study airports can be obtained before the outcome analysis is run, a weather-adjusted model will be added as a secondary analysis with these airport-day covariates, fixed now: share of hours with ceiling under 1,000 ft or visibility under 3 statute miles; maximum reported gust of 25 kt or more (yes/no); thunderstorm reported (yes/no). The primary analysis stays as in 7.1 either way. If METAR cannot be obtained, the paper will say so.

### 7.5 Spacing (H2)

Same model and bootstrap as 7.1 with tight pairs as the count and measured pairs as the offset. The year-over-year difference in median follower distance is reported for US and control. Because unseen aircraft make gaps look wider, and receiver coverage grew between the years, the baseline-adjusted estimate (as in 7.2) is the main spacing result.

### 7.6 TCAS resolution advisories (H3)

A pilot day showed RA events near US study airports but almost none near the European ones, so the control group cannot be used. Estimand, US study airports only:

(RA rate shutdown 2025 ÷ RA rate baseline 2025) ÷ (RA rate shutdown 2024 ÷ RA rate baseline 2024),

with the day-pair bootstrap. Sensitivity: excluding DCA and BUR (known RA-rate changes in 2025); excluding RAs whose first message is "Clear of Conflict". RA capture depends on receiver coverage and on interrogation, so this analysis is descriptive support, not a test on which the paper's conclusion rests.

### 7.7 Multiplicity

There is one primary test (7.1). H2 and H3 main estimates are judged with Holm adjustment across the two. Everything else is labelled secondary or exploratory.

## 8. What the study can detect

Volumes come from the three pilot days (pooled, outside the study windows): about 19,800 detected approaches per day at the US study airports and 8,900 at the control airports, with roughly 70% of landings yielding a spacing measurement. The pooled go-around rate on those August days was 4.9 per 1,000 approaches. Pilot days showed some airports with almost no detected approaches in one year (for example HNL, HOU, IAH, JAX, CDG and ORY in August 2024; CMH, GVA and OSL in August 2025); exclusion rule 3 removes any such airport from both years.

Over the 43-day shutdown window that implies about 850,000 US approaches and 380,000 control approaches per year. At 4 go-arounds per 1,000 approaches that is about 3,400 US and 1,500 control go-arounds per year.

- If counts were purely Poisson, the standard error of log RRR would be about 0.044, and the study would have 80% power (two-sided 5%) to detect a relative change of about 13%.
- Go-arounds cluster on bad-weather days. Assuming day-level clustering inflates the variance threefold (an assumption, not an estimate), the standard error is about 0.075 and the detectable change is about 21–23%, roughly 0.8 go-arounds per 1,000 approaches.

The realised standard error from the bootstrap will be reported, with the detectable change computed as 2.8 times that standard error. If the realised 95% interval is wider than 0.80–1.25, the study cannot support a "no meaningful change" conclusion and the paper will say so.

The spacing analysis has far more events (roughly 8% of about 590,000 measured US pairs per year are tight) and can detect changes of a few percent, but is more exposed to coverage artefacts. The TCAS analysis has roughly 40–80 qualifying events per day near US study airports on the pilot days, about 2,000–3,500 per shutdown window, and no usable control group.

## 9. Blinding

- The pipeline was built and tested on 20 August 2025 and on 14 and 21 August 2024 only. Pooled detection counts, spacing quantiles and ACAS event counts from those days were inspected.
- During processing of the study windows, logs record only file counts, sizes and the number of attempts per day. No go-around count, spacing statistic or RA count for any study day will be computed or viewed until all 154 days are processed.
- The analysis script will be committed to the repository before it is first run on study data.

## 10. Reporting

Absolute rates and rate differences are reported beside every ratio. Per-airport variation is shown. Intervals come from resampling days and airports. The paper leads with the results and states plainly what the study does and does not show. Code, the airport-day table and the analysis outputs will be published in this folder; raw archive files are not redistributed.

## 11. Changes after registration

None at registration.

### 11.1 Addendum, 11 November 2026 (before any outcome was computed; 27 of 154 days processed)

Hourly METAR was obtained for all 84 study airports from the Iowa Environmental Mesonet (routine and special reports, 31 August–17 November 2025 and 1 September–18 November 2024), downloaded by the author because the analysis workspace cannot reach that site. The weather-adjusted secondary analysis of section 7.4 will therefore be run. Details fixed here, before unblinding:

- Covariates are computed per airport and UTC day by `code/weather.py`; the output is `data/weather_airport_day.csv`. A clock hour counts as low if any report in it shows a ceiling (lowest broken, overcast or vertical-visibility layer) under 1,000 ft or visibility under 3 statute miles; the covariate is the share of reporting hours that are low. Gust is 1 if any report that day has a gust of 25 kt or more. Thunderstorm is 1 if any report that day carries a thunderstorm code, including thunderstorm in the vicinity.
- Model: Poisson regression on airport-days in the primary shutdown window, with airport fixed effects, year, year × US, the three covariates and offset log(approaches). The coefficient on year × US is the weather-adjusted ratio of rate ratios. Interval: day-pair bootstrap, 2,000 resamples. The same model without covariates on the same airport-days is reported beside it.
- This analysis is secondary. The primary analysis and decision rules of section 7.1 are unchanged.

SHA-256 of the two source files as received: 2025 `2dcca1c37bf86d1b35683121eb115bb0f418aca77dc2b429cccdddca2bc76f01`; 2024 `473cae8f66a4e6638aab080c322ea287383449beba4448135edf698f15b4b9b8`.

### 11.2 Departures recorded after the analysis, 12 November 2026

1. `code/analysis.py` omitted three registered items: the median follower distance (7.5), the airport-resampled interval for the baseline-adjusted spacing estimate (7.5), and the Holm adjustment across airports (7.3). They were computed after unblinding by `code/supplementary.py` and `code/post_review.py` using the registered definitions.
2. RA events were assigned to the nearest of the 84 registered airports and dropped if that airport was later excluded by rule 3, which departs slightly from "within 15 NM of a US study airport" (5).
3. The airport bootstrap resamples within two strata (US, control), not within the four registered groups.
4. The realised detectable change was 33%, against the 21–23% expected in section 8.
5. Six 2025 days failed during processing (out of memory) and completed on retry; rule 4 was not invoked.
6. `code/run_day.sh` was changed during processing so that the two memory-heavy steps take turns; this affects scheduling only.
7. All analyses in `code/supplementary.py` part 2, `code/post_review.py` and `code/post_review_ops.py` are exploratory and were chosen after the results, and after independent review, were known.
8. This document was not lodged with a registry. Its time-stamp is the repository commit.
