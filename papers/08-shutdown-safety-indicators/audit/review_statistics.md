# Independent statistical and reproducibility review: Paper 08 (2025 shutdown and go-around rates), draft v0.1

Reviewer scripts: `audit/scripts_statistics/` (`r1_rebuild.py` … `r7_extra.py`, `common.py`). Nothing under `/home/claude/research` was edited; nothing was committed. Line numbers refer to `paper.tex`.

## Verdict

The arithmetic is reproducible: every count in `airport_day.csv` rebuilds exactly from the raw attempt files (all 154 days, 11,592 airport-days), every point estimate in `results.json` and `supplementary.json` reproduces to at least 6 significant figures with independent code, and the "inconclusive" primary verdict follows correctly from the registered rules. The headline go-around conclusion is sound. Three things in the draft are not: (1) the TCAS result (0.73) is largely an artefact of a change in the archive's ACAS logging on 26–27 September 2024, exactly at the 2024 baseline/comparison boundary, and it disappears (1.01) when the baseline is taken after that change; (2) the per-airport statement "14 of 76, about four expected by chance" uses the wrong null, since a no-change calibration on the same data gives about 10 by chance, and the registered Holm adjustment was not applied (only 1 airport survives it); (3) "excludes a rise above about 13%" is stated as something the study shows, yet it depends on a comparison the paper's own placebo rejects and on a bootstrap that ignores day-to-day serial correlation. The weather-adjusted "interval excludes 1" is also fragile: it stops excluding 1 when weather effects are allowed to differ between US and control airports. These need fixing before circulation; none changes the primary verdict.

## Major issues

### 1. The RA (H3) estimate is confounded by an archive logging change at the 2024 baseline boundary

Evidence (`r6_coverage.py`, `r7_extra.py`, from the raw daily ACAS files):

- ACAS messages per day in the archive: about 4,400–7,300 through 25 September 2024, then 11,342 on 26 September and 20,000–26,000 from 27 September 2024 onward. The share of messages carrying a position falls from 1.00 to about 0.28 at the same date. A second jump occurs about 10 November 2024 (about 170,000–237,000 per day, mostly DF18). In 2025 volumes are flat (about 6,000–9,000 per day, position share 0.96–0.97).
- Qualifying events near US study airports step up at that date: weekly means 77.0, 82.6, 78.4, 75.7 per day, then 102.6, 100.9, 92.6, 99.7. This is the "step up in early October 2024" the paper describes at line 190. It is an archive event, dated 26–27 September 2024, and not an operational one.
- US RA rate per 1,000 approaches, 2024: 3.59 (pdates 1–24 Sep), 4.23 (26–30 Sep), 4.24 (shutdown window). 2025: 2.70, 2.16, 2.19. The 2025 fall also happened before 1 October.
- Registered ratio: 0.728 (reproduced). With the baseline restricted to the five days after the 2024 logging change (pdates 26–30 Sep, both years): **1.01 (0.78 to 1.33)**. With the baseline before the change (1–24 Sep): 0.69.
- Negative control: study-type RA events in the contiguous US that are not within 15 NM of a US study airport show the same 2024 step (shutdown/September per-day ratio 1.17 in 2024, 1.01 in 2025).
- Concentration: SFO alone contributes 1,049 of 3,616 events in the 2024 comparison window and 176 of 1,883 in 2025 (its own ratio is 0.46). The top five airports hold 62% of 2024-window events. Excluding SFO gives 0.79 (0.67 to 0.92); excluding SFO, BUR and DCA gives 0.84 (0.72 to 0.98).

Recommended fix: report the registered number, then state that the 2024 September-to-October rise coincides with a logging change in the archive, that the estimate is 1.01 (0.78 to 1.33) with a post-change baseline, and that H3 is therefore not interpretable. Remove "Resolution advisories ... fell relative to 2024 (0.73; 0.63 to 0.85)" as a finding from the abstract (line 13) and summary item 6 (line 24). Remove the "adjusted p<0.001" (line 188) or mark it as void. Delete the VFR-traffic interpretation at line 190, or reduce it to a statement that it cannot be examined. Report the registered "Clear of Conflict" sensitivity (0.72, 0.62 to 0.83), which is in `results.json` but missing from the paper.

### 2. Per-airport claims: wrong chance benchmark, no Holm adjustment, intervals too narrow

Evidence (`r4_robust.py`):

- The 14 intervals excluding 1 reproduce exactly. But they are Poisson-exact intervals, and the paper itself shows go-arounds cluster by day (pooled SE 0.102 vs 0.045 Poisson; Pearson dispersion of the airport-day model 2.29).
- Null calibration: randomly splitting the 43 shutdown days of a single year into two halves (no true change by construction) and applying the same exact test gives a mean of **9.5 (2024) and 10.3 (2025)** of 76 airports "significant" at 5% (95% range 4 to 16). So 14 is within the chance range, not 3.5 times it.
- Holm adjustment (registered in section 7.3: "no airport is singled out as significant without Holm adjustment"): across 76 airports only **IAD** survives; across the 50 US airports IAD, EWR and BNA (and BNA's detected approaches rose 60%). The paper names 14 airports on unadjusted intervals. This is an undisclosed departure.
- Day-resampled per-airport intervals give 11 excluding 1, but a different set (BOS, SAN, DAL, MAN, AMS, BCN drop out; YUL, HEL, FCO enter), which shows how unstable the list is.
- Heterogeneity: the registered DerSimonian–Laird tau (0.196 US, 0.175 control) uses Poisson variances. With day-clustered variances tau is 0.16 for US (Q p = 0.006) and 0.10 for control (Q p = 0.28). "Airports differed from one another by more than chance" holds for the US group and is not shown for the control group.

Recommended fix: delete "where about four would be expected by chance" (line 23) or replace with the calibrated figure (about 10). State the Holm result. Present the airport list as descriptive only. Soften "large differences between airports ... unrelated to where delays were worst" (line 209) and "Delay during the shutdown was not a guide to the go-around rate" (line 166): a six-airport comparison with unadjusted intervals cannot support it.

### 3. "Excludes a relative rise above about 13%" is overstated

- The figure is the upper limit 1.128 of the day-pair interval (my replication: 1.125). It is correct "on this estimator".
- Daily series are serially correlated: lag-1 autocorrelation of the daily log ratio-of-ratios is 0.29 in the shutdown window; of the US daily log rate 0.45 (2024) and 0.29 (2025). A circular block bootstrap gives **0.74 to 1.19 (3-day blocks, SE 0.120)** and 0.76 to 1.16 (7-day blocks, SE 0.111). The upper bound is then 16–19%, and the realised detectable change is 36–40%, not 33%.
- The bound assumes parallel year-on-year trends, which the September placebo rejects. The baseline-adjusted upper limit is 53%.
- The closing section puts "The primary estimate excludes a rise of more than about 13%" under "It shows" (line 209) and then says under "It does not show" that a moderate rise cannot be excluded (line 211). These contradict each other.

Recommended fix: remove the 13% statement from "It shows"; in the abstract and summary item 2 attach the condition ("if the control airports are a valid comparison, which the September check calls into question") and report the block-bootstrap interval as a sensitivity check. The verdict stays "inconclusive" under every variant.

### 4. The placebo failure is not confined to September; the primary window contains it

Weekly fixed-effects ratio of rate ratios (`r4_robust.py`): 0.87, 0.80, 0.70, 0.68 (September); **0.60, 0.73** (29 Sep–12 Oct); then 1.17, 0.82, 1.52, 1.03, 0.77. Split of the primary window (exploratory): 1–14 October **0.67 (0.51 to 0.90)**; 15 October–12 November 1.09 (0.86 to 1.34).

So the primary estimate of 0.93 averages two weeks that look like the failed placebo with four weeks slightly above 1. The paper notes high US 2024 rates "in September and early October" (line 146) but does not draw the consequence. "The two bracket the answer" (line 148) is unsupported: nothing guarantees the truth lies between 0.93 and 1.19, and the registered weather-adjusted estimate (0.81) lies outside the bracket.

Other placebo diagnostics: 40 of 50 US airports had a lower September rate in 2025 than 2024 (controls 15 of 26), so it is broad, not one airport or storm. Leave-one-airport-out placebo range is 0.76 to 0.81. Dropping the Hurricane Helene days (pdates 24–28 Sep) gives 0.81 (0.67 to 0.98); dropping ten south-eastern US airports gives 0.77 (0.64 to 0.89). The largest absolute 2024 excesses are at ORD, SFO, LAS, LGA, SEA, SLC. Line 201 places both hurricanes "in the 2024 comparison period"; Helene (26–27 Sep 2024) falls in the September baseline, Milton (9–10 Oct) in the comparison window.

Recommended fix: add the weekly table or the two-part split, labelled exploratory; delete "bracket the answer"; correct the hurricane sentence and report the Helene sensitivity.

### 5. The weather-adjusted estimate depends on an assumption the data reject

Reproduced: 0.809 (my interval 0.67 to 0.96; paper 0.68 to 0.95). The registered model forces one set of weather coefficients on both groups. Fitted separately (`r3_weather.py`, `r7_extra.py`): low-cloud/visibility rate ratio 2.73 at control airports vs 4.63 at US airports; gust 1.79 vs 1.30. With weather × US interactions the estimate is **0.87 (0.74 to 1.03)**; adding weather × year, 0.88 (0.73 to 1.05). The interval no longer excludes 1.

The paper's handling (not treating 0.81 as a finding) is the right call, but two of its three stated reasons are post-hoc analyses. The interaction result is a better reason. Also: European stations report half-hourly (median 48 reports per day vs 24 in the US), so "any report in the hour is low" is a slightly more sensitive test in Europe.

Recommended fix: add the interaction model as an exploratory row and cite it as the reason for caution.

### 6. Coverage between years changed more than the paper says

- Extraction logs: positions kept near study airports were **1.81 times** higher in 2025 for 1.02 times as many aircraft (about 330 vs 595 points per aircraft; stable across weeks within each year). The paper mentions only "archive about 45% larger" (line 197; verified as 1.47).
- Landing "confirmed by ground position" share rose from 0.42 to 0.55 (control) and 0.48 to 0.62 (US); 500 ft gate success from 0.89 to 0.93 (control) and 0.94 to 0.98 (US).
- Airports with large changes in detected approaches in the shutdown window: ZRH ×2.38, BNA ×1.60, BCN ×1.42, GVA ×1.36, SDF ×1.32; also DTW, STL, TPA about ×1.2. Line 197 says counts were "stable at most airports", which is true, but BCN (one of the 14 "significant" airports, and the leave-one-out minimum) is not flagged.
- Sensitivity (exploratory): restricting to airports with count ratio within 0.80–1.25 gives primary 0.90 (0.74 to 1.09), placebo 0.77; within 0.90–1.11 (61 airports) primary 0.87 (0.72 to 1.06), placebo 0.77. Balanced airport-day pairs only: 0.930. Conclusion unchanged.

Recommended fix: report the point-density change and the sensitivity rows; flag BCN alongside BNA and ZRH.

### 7. Spacing: the caveat quoted is for the wrong estimate, and the result is more robust than stated on one axis

The paper cites the airport-resampled interval 0.55 to 1.22 (shutdown-only estimate) as a reason for doubt about the baseline-adjusted main result (lines 176–178). Section 7.5 says "same model and bootstrap as 7.1", but the script never ran the airport bootstrap for the baseline-adjusted estimate. I ran it: **0.64 to 0.91** (day bootstrap 0.68 to 0.90). Both exclude 1; leave-one-airport-out range 0.75 to 0.81. So the registered main spacing estimate holds under airport resampling.

It remains hard to interpret: the tight-pair share rose year on year in every cell (US 7.9 to 9.2%, control 3.7 to 5.1%), consistent with the density change in issue 6; the top five US airports hold 62% of US tight pairs (ATL alone 25%); and the "median US airport ratio 0.99" (line 178) is the median of only the 32 US airports with more than 20 tight pairs in both years, a filter the text omits. The abstract's "fell at US airports" should read "rose less at US airports than at control airports".

## Minor issues

1. **Registered outputs missing from the paper.** RA sensitivity excluding "Clear of Conflict" (section 7.6); Holm across airports (7.3); count of oversize-skipped trace files (section 3: one file on 2024-11-10; one parse error on 2025-10-15). Section 10 says absolute rates accompany every ratio; Table 2 has none.
2. **Nearest-airport assignment for RAs.** The code assigns each RA to the nearest of all 84 airports, including the 8 excluded ones, then drops events at excluded airports. An RA within 15 NM of HOU but nearer IAH is lost. The registered wording is "within 15 NM of a US study airport". Small, but a departure.
3. **RA events use the first message's position.** 18% of events in my sample had no position on the first message and were dropped, even if later messages had one.
4. **Detectable change is asymmetric.** exp(2.8 × SE) − 1 = 33% upward corresponds to a 25% fall. Computed as registered.
5. **Monte Carlo precision.** With 2,000 resamples the interval limits move by 0.01–0.02 between seeds (primary lower limit 0.759 in the paper, 0.749 and 0.755 in my two runs; baseline-adjusted upper limit 1.53 in `results.json`, 1.57 in `supplementary.json` for the identical estimand, 1.55 mine). Quote one decimal fewer or raise the resample count.
6. **Bootstrap pairing.** Pairing 2024 and 2025 days has no physical basis, but it is harmless: resampling the years independently gives 0.76 to 1.13.
7. **Airport bootstrap strata** are US vs control, not the four registered groups. Acceptable reading of "within group"; say so.
8. **Borderline coverage inclusions.** HOU and CDG pass rule 3 with exactly 60 days in 2024; GVA with 62 in 2025. PIT fails at 59/60. Worth one sentence.
9. **Weather means quoted (20% and 12%, line 150)** are unweighted airport-day means; approach-weighted they are 17.8% and 10.3%.
10. **Line 31 vs preregistration section 1.** The paper says cuts were "4% ... rising to 10% by 14 November" then held at 6%; the preregistration says 6% from 11 November and 3% from 15 November. Reconcile.
11. **Line 43** says the preregistration was committed "before any study-window data had been downloaded". Timestamps support this: preregistration commit 13:44:36 on 11 Nov; working data directory last restructured 13:44:47; analysis script committed 13:47; first processed attempt file written 13:51; weather addendum 15:52; results 12 Nov. The README still says "No results exist".
12. **Six retried days are all 2025 days.** Their counts are in line with the same weekday one week either side; no sign of truncation.
13. **Holm across H2/H3** is computed correctly but from normal-approximation p-values on bootstrap SEs, and H3 is described as "descriptive, not a test" while being given a p-value.

## Number-audit table (mismatches and unsupported numbers only)

| Line | Paper says | Source value | Comment |
|---|---|---|---|
| 13 | "about 4.5 million approaches" at the 76 airports | 4,403,289 in `airport_day.csv`; 4,548,375 is all attempts at all 84 airports before exclusions | Should be about 4.4 million |
| 23 | "about four would be expected by chance" | Nominal 3.8; calibrated on these data about 10 | Unsupported (Major 2) |
| 164 | control between-airport SD "0.18" | 0.1747 | Rounds to 0.17 |
| 176 | US median follower distance "4.22 NM" (shutdown 2025) | 4.2146 | Rounds to 4.21 |
| 154, 22 | SE "0.044 if go-arounds were independent" | Realised model-based SE 0.0447; 0.044 is the planning figure | Say 0.045 or "planned 0.044" |
| 178 | "the median US airport ... ratio 0.99" | Median of 32 of 50 US airports (filter: >20 tight pairs both years) | State the filter |
| 13, 20, 209 | "about 13%" | 12.8% (paper's run), 12.5% (mine); 16–19% with block bootstrap | Conditional claim (Major 3) |
| 201 | two hurricanes "in the 2024 comparison period" | Helene is in the September baseline | Wording |
| 197 | "about 45% larger" | 1.47 (verified from release index); not in results files; point density near airports is 1.81× | Add the 1.81 |
| 188, 24, 13 | RA 0.73 (0.63 to 0.85), p<0.001 | Reproduces, but artefactual (Major 1) | Reframe |

Every other number in the abstract, summary, Tables 1 and 2 and the results text matches `results.json` / `supplementary.json` at the stated rounding (checked item by item, including all 15 rows of Table 2, the airport list at line 164, DCA 1.21, LGA 0.88, BNA +60%, ZRH ×2.38, approach changes +0.5% and −3.7%, RA counts and rates, spacing shares, weather rate ratios 3.6/1.4/1.4, exclusion counts 216/177/64, the 8 excluded airports and the 39/11/3/23 split).

## What I verified as correct

- **Raw rebuild.** All 154 attempt files, rules 1–3 applied with my own code: 11,592 of 11,592 airport-day rows match on n, ga, pairs, tight. Rule 1 removals 216/177/64 match. Excluded airports match. Weekday alignment: pdate = date + 364 days for every 2024 row, zero weekday mismatches; windows have 30/43/37/10/10 days.
- **RA rebuild.** Eight random days from raw ACAS files with my own event logic and haversine distance: 466 of 466 events match, zero mismatching airport-day cells. Files are time-sorted.
- **Table 1.** All eight count pairs and rates exact.
- **Primary.** 0.92954 (own conditional-binomial Newton, and separately an airport-day Poisson with 76 dummies in statsmodels: identical to 12 digits, confirming the equivalence claim). Day-pair interval mine 0.749 to 1.125, SE 0.105; paper 0.759 to 1.128, SE 0.102. Airport bootstrap mine 0.824 to 1.054; paper 0.822 to 1.047. Cluster-robust SEs agree with both bootstraps (0.103 by day, 0.061 by airport).
- **Placebo** 0.7788 (0.653 to 0.916 mine). **Baseline-adjusted** 1.1935 (0.903 to 1.549 mine; airport bootstrap, not in paper, 0.95 to 1.47).
- Phases, groups, control variants, phase B US40 vs USOTHER, airline-only and without-rule-1 (both rebuilt from raw), leave-one-out: all point estimates exact, intervals within 0.02.
- Spacing and RA estimates, medians of follower distance (from raw), Holm arithmetic, exact per-airport intervals (to 1e-15), DL statistic as coded.
- **Weather.** Covariates recomputed from raw METAR with my own code: 13,271 of 13,271 airport-days match (`weather.py` follows the addendum). Weather-adjusted 0.80890 with own IRLS and statsmodels.
- **`supplementary.py` Newton fit** matches statsmodels to 13 digits on the real data, unweighted and for a weighted bootstrap draw (12–13 iterations, converged).
- **Decision logic and verdict.** `verdict()` and the wider-interval rule implement section 7.1; "inconclusive" is correct. The airport interval alone (0.82 to 1.05) would satisfy "no meaningful change"; using the day interval is the registered and conservative choice. Detectable change 33.1% is computed as registered.
- Exploratory analyses are labelled as such in Table 2 and the text.

## Unresolvable limitations (present data)

1. Whether autumn 2024 or autumn 2025 was the unusual US season. Needs a third year (2023 archive coverage is thinner still).
2. Whether the 1.81× change in position density altered go-around or landing detection differently at US and control airports. Needs a density-matched reprocessing (thinning 2025 traces to 2024 density) or a validated reference set.
3. A valid H3 estimate. The 2024 ACAS logging change leaves only five post-change baseline days; the archive's ACAS decoding history would have to be established from the adsb.lol maintainers.
4. The cause of the September/early-October 2024 US excess (broad across 40 of 50 airports; not explained by the three weather covariates or by Helene).
5. Whether European or Canadian operations had their own disturbances in the window.
6. Go-around detection sensitivity and specificity at these airports; cause of each go-around.
