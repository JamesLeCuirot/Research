# Operational validity review: "Did the 2025 US Government Shutdown Change Go-Around Rates?" (paper 08, draft v0.1)

Reviewer role: flight-operations / ATM validity. Nothing under `/home/claude/research` was edited, nothing committed. All numbers below were recomputed from the raw attempt files, ACAS files and METAR files unless stated. Scripts: `audit/scripts_flight_operations/`.

## Verdict

The go-around detector is operationally credible: about 90% of US detections are followed by a landing of the same aircraft at the same airport within 30 minutes (median 13 min), the hour-of-day and operator profile looks like line flying, and the high-rate airports are the ones a pilot would expect. The paper's cautious headline ("no detectable change, inconclusive") survives. But three things in the draft do not hold as written. (1) The TCAS RA result is not a network-wide signal: two airports (SFO and BUR) supply 47% of 2024 events, the SFO events are RAs between paired arrivals on 28L/28R, and both sites had documented procedure changes between the two autumns; without them the "30% lower in September 2025" disappears (ratio 0.96). (2) The spacing measure is dominated by how low the leader was tracked (tight share 13.9% when the leader was seen below 30 ft, 0.2% when last seen at 100 to 300 ft), and the result ranges from 0.67 to 0.97 depending on how coverage is controlled, so "points that way" is too strong. (3) The per-airport list is largely runway-availability and runway-detection artefacts (BOS 9/27 closed in 2025, CVG 18C/36C absent in 2024, BNA and HOU main landing directions undetected in 2024, SAN driven by runway 09 days, SFO driven by RA-linked go-arounds), and should not be presented as rises and falls in the shutdown. The control-side "rise" in go-arounds is entirely go-arounds below 200 ft at European airports whose low-level coverage improved, which moves the primary estimate from 0.93 to about 1.0 when removed.

## Major issues

### 1. The RA finding is carried by SFO and BUR, and is mostly parallel-approach and known-hotspot RAs

Evidence (replicating `ra_events`, 50 kept US airports, before the n>=30 filter):

| | Sep 2024 | Shutdown-equiv 2024 | Sep 2025 | Shutdown 2025 |
|---|---|---|---|---|
| All US events | 2,139 | 3,619 | 1,534 | 1,886 |
| KSFO | 576 | 1,049 | 209 | 176 |
| KBUR | 426 | 634 | 219 | 147 |
| SFO per 1,000 approaches | 34.5 | 43.7 | 12.8 | 7.4 |
| BUR per 1,000 approaches | 126 | 122 | 58 | 25 |

- SFO+BUR are 47% of events in both 2024 windows, 28% in Sep 2025, 17% in the shutdown.
- Preregistered ratio 0.73 (replicated 0.729). Excluding SFO only: 0.79. Excluding SFO+BUR: 0.83. Excluding SFO+BUR+DCA: 0.84. I did not bootstrap these; with the paper's SE (about 0.08 on the log scale, larger with fewer events) the upper limit is near 1.
- Year-on-year September ratio: 0.71 all airports; 0.96 without SFO+BUR; 1.02 without SFO, BUR, DCA, PHX, TEB, DAL. So paragraph 2 of the RA section ("about 30% lower in 2025 even in September ... something other than the shutdown separates the two years") is two airports, not the network, the receiver network or the decoder.
- SFO: 90% of RA aircraft were arrivals to SFO; 94% of events carry a threat address, and for 84% the threat is another study-type aircraft that landed on the other parallel (28L vs 28R, 1,645 of 1,657 cross-runway) a median 26 s apart. These are RAs between paired aircraft on closely spaced parallel visual approaches. SkyWest alone: 808 events in 2024, 158 in 2025. Location cluster 37.60N 122.28W (about 5 NM final).
- A documented cause exists: United introduced a revised "Special FMS Bridge Visual 28R" with a smaller intercept angle in November 2024, reported to reduce RA events, with the FAA revising the public procedure to match (https://justhelicopters.com/Articles-and-News/Industry-Wide-News/Article/180638/Reducing-Resolution-Alerts-at-SFO; undated page, FAA files in a Jan 2025 path; no numbers given). The later FAA ban on side-by-side landings at SFO is 2026 and outside the window (https://avbrief.com/faa-bans-parallel-landings-at-sfo-sharply-cutting-capacity/).
- BUR: 893 of 1,426 events lie in one 0.04-degree cell over Van Nuys airport (34.20N 118.48W); 39 to 55% are business jets, only 47 to 64% are arrivals to BUR, and the threat is almost never a study-type arrival (0.3 to 1.6%). This is the known BUR ILS 8 / VNY pattern interaction. The FAA lowered the VNY pattern in two 90-day steps beginning about July 2025 (100 ft, then 200 ft), later made permanent (https://www.faa.gov/air_traffic/community_engagement/vny/tcas-faq.pdf; https://www.cbsnews.com/losangeles/news/faa-implements-changes-to-la-area-airport-to-lower-risk-of-midair-collisions/). Exact start dates could not be verified; if the first step began in July the second step would have begun around October 2025, inside the shutdown window. BUR weekly counts in 2025: 51, 61, 44, 51 (September) then 40, 23, 12, 26, 20, 31.
- Other clusters are also satellite-airport interactions, not study-airport approaches: PHX (131 events in a cell over Falcon Field, 112 in 2024 vs 19 in 2025), DAL (over Addison), TEB (83 to 87% business jets). Business jets are 36 to 52% of RA aircraft but 8.5% of approaches.
- RA types: Monitor Vertical Speed 3,459, Level Off 2,080, Climb 1,738, Descend 1,135. Corrective Climb/Descend share fell from 38% to 29 to 30%.
- Not test or ground artefacts: Clear-of-Conflict-only events 0.7%, single-message events 0.2%, events at file start 0.5%, events below airport elevation under 1%.
- Factual error in Method: the paper says RA messages "are only received when the aircraft is interrogated within range of a receiver". 97% of events here are DF17, the ADS-B extended-squitter RA broadcast, which is spontaneous; only 3% are DF16 and none of the kept events are DF20/21 Comm-B replies.
- Denominator: "per 1,000 detected approaches at the nearest study airport" does not match the numerator population (any study-type aircraft within 15 NM below 7,000 ft, including departures, and traffic to VNY, FFZ, ADS, HWD, SQL, OPF). It works as a rough exposure scaler only.

Fix: report the RA analysis with SFO shown separately and excluded (it was not in the preregistered exclusion, so label it exploratory); state that the year-on-year gap is SFO+BUR; replace the three speculative causes with the two documented procedure changes; describe the events as dominated by paired-approach and satellite-airport RAs; correct the interrogation sentence; drop or heavily qualify "less VFR traffic ... during the shutdown" (still possible for the residual 0.83, untestable here).

### 2. RA-linked go-arounds explain the SFO "fall" and shift the US go-around rate

Matching each US go-around to an RA by the same aircraft within 180 s: 146 of 3,141 (Sep 2024), 237 of 4,065 (2024 window), 67 of 2,507 (Sep 2025), 86 of 3,999 (shutdown). At SFO over the 77 days: 255 of 424 go-arounds in 2024 were RA-linked, 71 of 316 in 2025; non-RA-linked SFO go-arounds went up, 169 to 245. SFO's median go-around minimum height fell from 1,075 ft to 621 ft, consistent with fewer RA climb-outs at 4 to 5 NM. Excluding RA-linked go-arounds, the US rate in the shutdown window is 4.49 (2024) vs 4.55 (2025) instead of 4.77 vs 4.64.

Fix: say that the detector counts TCAS RA climb-outs and parallel-approach breakouts as go-arounds (operationally defensible, but it is a different mechanism from runway or spacing go-arounds), and add the RA-excluded rate as an exploratory robustness row. Remove SFO from the list of airports that "fell" or explain it.

### 3. The control-airport rise is a low-level coverage artefact; go-arounds below 200 ft are coverage-dependent

Shutdown window, go-arounds per 1,000 by lowest height reached:

| | Ctl 2024 | Ctl 2025 | US 2024 | US 2025 |
|---|---|---|---|---|
| Minimum below 200 ft | 0.66 (244) | 1.09 (422) | 1.02 | 1.11 |
| Minimum 200 ft or above | 2.78 | 2.58 | 3.75 | 3.53 |

- The whole control rise (3.44 to 3.66) is the under-200 ft class, concentrated at airports whose low-level coverage changed: LSZH 2 to 28, EDDL 6 to 31, LEMD 4 to 25 (ground-confirmed landings 0% to 83%), EGKK 0 to 17 (1% to 31%), LEBL 5 to 17. Same pattern at US airports with coverage steps: BNA 0 to 23, STL 0 to 11, CLT 5 to 23.
- Ratio of rate ratios by definition: all 0.92; minimum >= 200 ft 1.02 (September 0.83); minimum >= 400 ft 1.11 (September 0.83); only go-arounds followed by a landing within 30 min 0.89; both conditions 0.97.
- Coverage did change materially: ground-confirmed landings rose from 47% to 62% (US) and 42% to 55% (controls); the leader's median last-seen height fell from 22 ft to 0 ft (US) and 55 ft to 8 ft (controls). Go-arounds with no detected landing within 60 min fell from 7.0% to 3.5% (US) and 11.6% to 8.9% (controls); they reach 42% at LIMC, 35% at LSGG and LSZH, 27% at SDF, 23% at LGA.

Fix: add the >= 200 ft (or >= 400 ft) estimate as an exploratory coverage-robust row; rewrite the Limitations bullet to say the direction is known (better low-level coverage raises detected low go-arounds, more in the controls); do not describe the control rate as having "risen".

### 4. Per-airport "rises and falls" are mostly runway availability, runway detection or single-configuration effects

| Airport | Paper | What the raw data show |
|---|---|---|
| BOS (1.36) | rise | Runway 27 landings: 7,242 in 2024, 0 in 2025 (all 77 days). 9/27 was closed for safety-area work from early Sep to 18 Nov 2025 (https://backend.ainonline.com/aviation-news/aerospace/2025-09-02/boston-runway-closes-safety-improvement-project; https://rock929rocks.com/2025/11/18/boston-logans-runway-9-27-reopens-following-safety-upgrades/). Landings moved to 04L (764 to 6,207 in the window; 53 go-arounds, 8.5 per 1,000) and 22L. A closure effect, not a shutdown effect. |
| BNA (2.00) | rise | Runway end "20L": 0 landings and 4 go-arounds in 2024, 8,875 approaches in 2025; 13 of 43 days in 2024 had under half the median count. The south-flow landing runway was not detected in 2024. Not comparable; should be excluded, not just caveated. |
| CVG (0.54) | fall | 18C/36C: 0 landings in 2024, 5,551 in 2025. Consistent with a 2024 closure (an RFP titled "24-24 Runway 18C/36C rehabilitation" exists, https://airportscouncil.org/rfp/24-24-runway-18c-36c-rehabilitation-tw-d2-demo-relocation-and-runway-18l-36r-rsa-grading-corrections; dates not verified). ABX Air go-arounds 12 to 2. |
| SAN (0.72) | fall | Runway 27 rate unchanged (7.6 vs 7.9). The fall is runway 09: 1,286 approaches with 84 go-arounds in 2024 (65 per 1,000) vs 591 with 26 in 2025. Runway 09 is the low-ceiling configuration; top days 4, 7, 8, 12 Oct 2024 had low cloud in 62 to 75% of hours (8 Oct: 29 go-arounds in 316 approaches). Weather and configuration. |
| SFO (0.82) | fall | RA-linked go-arounds, see issue 2. |
| JFK (0.66) | fall | 13L: 4,140 approaches (8.0 per 1,000) in 2024 vs 1,589 in 2025; 31R rate 4.8 to 2.4. Half of JFK go-arounds bottom out under 200 ft, the coverage-sensitive class; low go-arounds 59 to 33 while confirmed share rose 73% to 88%. Configuration mix plus unknown. |
| ATL (0.69) | fall | No coverage change (97 to 98% confirmed). West-flow share rose (27L 4,961 to 9,055). Falls on 26R (4.9 to 2.4), 10 (6.7 to 2.6), 28. Looks operational; cause not identified. |
| DAL (0.66) | fall | 13L 1,701 to 6,330 landings, 13R 8,522 to 4,067; confirmed share 38% to 78%. Runway use and coverage both changed. |
| EWR (1.83) | rise | Small numbers (50 to 85). Median minimum height rose 309 to 843 ft (more go-arounds initiated high, typical of ATC-directed ones). Runway 29 use up (1,301 to 2,238); weekend 4R landings halved. EWR operated under FAA arrival limits throughout 2025, extended to October 2026 (https://www.faa.gov/newsroom/faa-extends-order-limiting-operations-newark-liberty-international-airport). Plausibly operational, but confounded with a year of Newark-specific changes. |
| IAD (2.48) | rise | 22 to 58 events, spread over all runways; runway 30 landings 6 to 246 with 6 go-arounds; peaks on 31 Oct and 11 Nov 2025 (7 and 8). No coverage change. Small numbers, windy-day clusters. |
| SJC (3.0) | rise | 5 to 14 events; south-flow (12R) landings 162 to 1,115. Noise. |

Other airports with a runway end at 4% or more of landings in one year and under 0.4% in the other: HOU 04/22 (0 vs 12,862; 93% of 2025 landings), PHNL 04L (0 vs 5,432), DTW 04R (59 vs 3,415), FLL 28L, MCO 18L, BUR 33, CYYC 35L (2,425 vs 0). Whether each is a closure or a detection gap, the airport is not like-for-like across years.

Also: the two hurricanes are handled asymmetrically. TPA has no airport-days from 9 Oct to at least 12 Oct 2024 and MCO none for 10 Oct (n<30 rule), while MCO on 11 Oct 2024 contributes 20 go-arounds in 402 approaches and 15 on 27 Sep (Helene).

Fix: replace the "rises include / falls include" sentences (Summary item 5 and the Variation section) with a statement that most of the large single-airport changes trace to runway closures, configuration mix or detection breaks, and give the table. Add a runway-availability screen (runway-end share shift) as an exploratory exclusion. With 16 such airports removed I get 0.88 (all go-arounds) and 0.96 (>= 200 ft, matched), so the pooled estimate is not sensitive, which is worth reporting. Drop "Delay during the shutdown was not a guide to the go-around rate": the airport-level go-around changes are not shutdown measurements.

### 5. Spacing: the measure tracks coverage first, and the "wider spacing" reading is too strong

- What it measures: the follower's distance to the threshold at the leader's last airborne fix. With good coverage that fix is at the flare, so true in-trail distance is roughly the value plus 0.2 to 0.3 NM. Under FAA rules 2.5 NM on final is a permitted radar minimum inside 10 NM at many airports, and visual separation allows less (JO 7110.65 section 5-5-4, from the reviewer's knowledge, not re-verified here). "Tight" is therefore not a loss of separation and mostly counts normal high-rate visual-separation operations. Tight pairs have a median time gap of 72 s. Only 0.4 to 0.6% of US pairs are under 1.5 NM.
- Coverage dependence: tight share by leader's last-seen height, US: below 30 ft 13.9% (2024) and 13.9% (2025); 30 to 100 ft 3.4% and 4.7%; 100 to 300 ft 0.2%; above 300 ft 0.0%. The share of pairs with the leader seen below 30 ft rose from 54% to 66% (US) and 46% to 59% (controls). The year-on-year rise in both groups is this mix shift.
- The estimate is not stable to coverage control (my replication of pooled all-pairs: September 1.06, shutdown 0.84, adjusted 0.79):
  - leader last seen below 30 ft: September 0.94, shutdown 0.91, adjusted 0.97;
  - leader ground-confirmed within 10 s: 0.95, 0.71, 0.75;
  - 18 airports with over 90% of leaders seen below 30 ft in both years: 1.23, 0.82, 0.67.
- The September-to-shutdown drop in 2025 is carried by ATL, JFK, LGA and BOS (BOS lost a runway; JFK and LGA changed configuration mix).
- Seasonal weather matters: within VFR hours the US share went 11.3% to 9.6% in 2025 and 8.8% to 8.2% in 2024, so some of the 2025 drop is beyond weather, but less visual separation in autumn is the default explanation and is not discussed.
- The median follower distance fell (4.32 to 4.21 NM), the opposite direction to "wider spacing"; the paper reports this without comment.
- Runway identification is not a problem (150 m half-width; closest parallels are 229 m apart). Missing turboprops and unseen departures only remove pairs.

Fix: explain what the measure is and is not; present the stratified table; change "consistent with slightly wider spacing on final" to "direction negative but dependent on how coverage is handled (0.67 to 0.97)"; delete "the spacing result, for what it is worth, points that way" from the closing section; mention the median moved the other way.

### 6. The failed September placebo: partly explained, and the explanations are operational

- September plus the first week of October 2024 has about 810 more US go-arounds than 2025 rates would give, spread across 36 of 50 airports. Largest: SAN +70, SFO +68, ORD +67, LAX +61, LGA +47, BUR +46, CVG +43, DFW +42, SEA +40, RDU +40. PHX goes the other way (-51).
- Weather explains part, but the daily-share covariate is too blunt. Matching each approach to its METAR hour: US approaches in IFR or worse were 5.2% of September 2024 vs 2.3% of September 2025. Southern California stratus is visible (SAN low-cloud share 0.23 vs 0.06; LAX 0.30 vs 0.12; LAX 7 Oct 2024 92% of hours, 18 go-arounds). Reweighting 2025 hourly-category rates to the 2024 weather mix only moves 4.27 to 4.34, against 5.42 observed.
- The gap is mostly in good weather: VFR-hour US rate 4.62 (Sep 2024) vs 3.75 (Sep 2025), about 400 excess go-arounds, at LAS, ORD, SFO, LGA, FLL, BUR, DFW, SLC, DEN, JFK. It persists across wind-speed bands and across every detection restriction I tried (0.79 to 0.85).
- Identified pieces: SFO and BUR RA-linked go-arounds (146 RA-linked in Sep 2024 vs 67 in Sep 2025). LAS runway 19L: 717 approaches with 52 go-arounds in Sep 2024 (72 per 1,000) vs 470 with 12 in 2025; on 14 and 19 Sep 2024 LAS ran a 19L/08R configuration with go-around clusters at 600 to 800 ft in clear, light-wind conditions (23 and 20 go-arounds on those two days). Helene: 27 Sep 2024 was the highest US day in the September series (171 go-arounds, 8.4 per 1,000); MIA had 18 on 26 Sep, CVG 16 and MCO 15 on 27 Sep.
- The residual VFR-hour excess at ORD, LGA, DFW, FLL, SLC, DEN, JFK is unexplained. A real change in practice between years (for example less use of visual approaches and visual separation after January 2025, or schedule de-peaking) is possible and cannot be tested here.

Fix: replace "The cause was not identified" with what is identified (stratus at the California airports with airport-specific sensitivity, SFO/BUR RA events, one LAS configuration, Helene days) and what is not (a broad VFR-hour excess). Note that a common weather coefficient cannot capture SAN-type sensitivity (runway 09 days run at 44 to 65 per 1,000). This strengthens the paper's statement that the primary and baseline-adjusted estimates bracket the answer.

### 7. Controls and unexamined differences between the two autumns

- Canada was not an undisturbed control: Nav Canada attributed Toronto Pearson delays on 1 Nov 2025 to "resource constraints" and used a traffic management initiative (https://www.cbc.ca/lite/story/9.6963586), and staff shortages were periodically closing two Canadian towers in October 2025 (https://www.bnnbloomberg.ca/business/company-news/2025/10/24/staff-shortages-shutting-two-canadian-airport-control-towers-periodically-memo-says/). YYZ go-arounds rose 104 to 160 over the 77 days. Calgary lost a runway (35L: 2,425 landings in 2024, 0 in 2025).
- Europe: a Belgian national strike on 14 Oct 2025 cancelled all Brussels departures (https://www.belganewsagency.eu/brussels-airport-cancels-all-departing-flights-on-14-october); a French ATC strike planned for early October 2025 was called off (https://newswav.com/article/french-air-traffic-controllers-call-off-three-day-strike-will-there-be-more-A2510_Iwo4Dj). Neither is large for this design, but the Limitations bullet "was not checked" can now be replaced.
- Procedures differ in ways that matter for go-arounds: the US uses visual approaches and pilot-applied visual separation routinely, lands on intersecting and closely spaced runways, and allows "anticipated separation" landing clearances; Europe generally keeps radar or time-based separation to touchdown. The US rate is therefore more sensitive to weather (VMC to IMC switches capacity mode) and to runway closures. US IFR-hour go-around rates are 2 to 3 times the control rates (9.5 to 12.3 vs 4.0 to 6.0 per 1,000). Controls remove network-wide data effects, not US operational seasonality.
- Control weather moved the other way: control approaches in IFR or worse fell from 16.7% to 9.2% between the windows, the reason the weather-adjusted estimate drops to 0.81. That estimate inherits issue 3 (the control rise is a coverage artefact), so it should not be read as a fall.
- US-side differences the paper under-weights: runway closures (issue 4), the SFO and BUR/VNY procedure changes, Newark limits, the hurricanes' asymmetric exclusion, and a windy late-October 2025 (26 to 31 Oct 2025 daily US rates 5.9, 5.5, 3.9, 4.7, 5.4, 6.4 against 4.0, 3.3, 4.6, 3.9, 4.0, 4.0 a year earlier; BOS 17 go-arounds on 1 Nov). I did not verify the weather system behind that week.
- The Louisville UPS accident (4 Nov 2025) is mentioned; SDF also had a coverage step (approaches +52%).

### 8. Mechanism section and wording

- The Background gives two mechanisms (less accurate spacing; reduced arrival rates). Missing: short staffing is managed mainly upstream (miles-in-trail, ground delay programs, ground stops, reduced acceptance rates), which lowers pressure on final; towers combine positions, which can raise runway-occupancy go-arounds; services to VFR traffic are withheld, which lowers RA exposure near satellite airports; and most go-arounds are crew-initiated or weather-driven and insensitive to staffing. A priori: go-arounds flat or slightly down, tight pairs down, RAs down. The paper's "flat was the most likely outcome" is right; say why.
- "Controllers worked without pay from 1 October" (abstract) vs the quoted order "since October 3". Reconcile.
- "the rate at which jets abandoned approaches" and "how often an approach could not be completed": use "discontinued". A go-around is often the conservative choice, and a lower rate is not safer (pressing on with an unstable approach also lowers it). The paper says a go-around is "a normal, safe manoeuvre" once; the closing section should repeat that a change in either direction is not a safety verdict.
- "protecting its margins by slowing down ... the spacing result points that way": not supported (issue 5).
- "A landing is the last airborne position of a flight on short final": this includes aircraft lost from coverage below 700 ft with no later climb seen, so it is "landing or presumed landing"; only 47 to 62% are ground-confirmed.
- "Go-around ... local altitude minimum below 3,000 ft": state that it includes missed approaches, breakouts and RA climb-outs initiated well above the runway (10% of US events bottom out above 1,500 ft) and excludes rejected landings after touchdown and any event with a ground-flagged fix within 120 s.
- "Pilot days showed almost no RA messages near the European airports": confirmed (102 control events in 154 days). Note that this is reception, not absence of RAs.
- "TCAS RA" within 15 NM and 7,000 ft is not "near runways"; the abstract's "what aircraft did near runways" overstates for that measure.

## Minor issues

- Absolute rate: 4.7 per 1,000 is at the upper end of published airline figures (1 to 3 per 1,000 from operator data; the paper cites 1.5 to 6 from ADS-B). It is plausible given that RA climb-outs and high breakouts are counted, business jets are included (3.0 per 1,000), and denominators miss landings where low coverage is poor. High-rate airports are operationally sensible: SFO (paired visuals, RAs, crossing departures), SAN (single runway, mixed mode, runway 09 days), BUR (short intersecting runways, VNY), DCA (short intersecting runways, river visual; 24% of DCA go-arounds bottom out over 150 m off the centreline), DEN (wind shear, mountain wave), PHL, LGA.
- By type the pattern is sensible: B748 10.8, E145 7.4, B744 6.8, B738 5.8 per 1,000; B712 2.4; business jets 2 to 3.
- Training screen: adequate. 351 aircraft-days with exactly two go-arounds are 91% airline (UAL, AAL, SWA, SKW, DAL), concentrated at SAN, DEN, SFO, i.e. real second attempts. Only residue found: Boeing test callsigns (BOE, 11 approaches, 1 go-around) and Convoy (CNV, 40 and 2). No duplicate go-arounds across neighbouring airports (0 of 19,457). One case of a go-around within 15 min after a landing by the same aircraft.
- The detector misses: go-arounds that climb less than 500 ft within 3 min (low missed-approach altitudes, "maintain 2,000" from 1,600 ft); events with a 60 s data gap around the minimum; rejected landings. It could misattribute a go-around at a non-study airport lying within 0.5 NM of a study runway's extended centreline inside 6 NM and within 30 degrees of its course (Boeing Field under the SEA finals is the obvious candidate; I found only 6 off-centreline SEA events, so the effect is negligible).
- Hour-of-day profile (approximate solar time): US 2.8 to 3.7 per 1,000 overnight, 4.3 to 5.5 by day with an afternoon and evening maximum; nothing suggests circuit training.
- The 364-day pairing aligns weekdays and both daylight-saving changes; Veterans Day (11 Nov) is offset by one day. Trivial.
- UTC days split the US evening bank across two "days"; harmless for rates, worth a sentence.
- Summary item 6 and the Limitations say coverage "changed"; the direction is known for all three measures and should be stated.

## What appears sound

- Specificity of the go-around detector: 90.5% of US events and 85.7% of control events followed by a landing at the same airport within 30 min; another 1% land at a different study airport; the unmatched share tracks low-coverage airports.
- Robustness of the pooled primary estimate: 0.88 to 1.02 under every restriction I tried (matched only, >= 200 ft, RA-linked removed, 16 non-comparable airports removed). None suggests a clear rise; the paper's central statement stands.
- The September placebo failure is real and robust (0.79 to 0.85 under all restrictions); the paper is right to give it weight.
- The training exclusion, the type lists (no helicopters or military types), runway attribution, and the absence of double counting.
- RA events are genuine airborne RAs, not test or ground transmissions.
- The paper's general caution, and its statement that the study does not measure losses of separation, incursions or workload.

## What cannot be resolved with these data

- Why US good-weather go-around rates were about 20% higher in September 2024 than September 2025 at ORD, LGA, DFW, FLL, SLC, DEN and JFK. The point files (`data/pts`) are no longer on disk, so individual tracks could not be inspected.
- Who initiated each go-around (crew or ATC) and why; the height at initiation is the only proxy.
- Whether runway ends absent in one year (HOU 04/22, PHNL 04L, DTW 04R, BNA south flow, CVG 18C/36C, CYYC 35L) were closed or simply not received. BOS 9/27 is confirmed closed; CVG is only supported by an RFP title.
- The exact dates of the VNY pattern-altitude steps and of the FAA's adoption of the revised SFO Bridge Visual, hence how much of the within-2025 RA decline at BUR and SFO falls inside the shutdown for unrelated reasons.
- Whether less VFR traffic or withheld VFR services lowered RAs during the shutdown: no VFR traffic counts here. The residual ratio without SFO/BUR/DCA (0.84) is the only evidence, without an interval.
- The LAS September 2024 19L/08R configuration, the windy last week of October 2025, and the hurricane dates were not checked against external records.
- True separation at the threshold: last-seen height varies by airport and year, so the tight-pair share cannot be made comparable without restricting to ground-confirmed leaders, and that restriction changes the answer.

## Sources

- [Reducing Resolution Alerts at SFO](https://justhelicopters.com/Articles-and-News/Industry-Wide-News/Article/180638/Reducing-Resolution-Alerts-at-SFO)
- [FAA Bans Parallel Landings at SFO (2026)](https://avbrief.com/faa-bans-parallel-landings-at-sfo-sharply-cutting-capacity/)
- [FAA VNY TCAS FAQ](https://www.faa.gov/air_traffic/community_engagement/vny/tcas-faq.pdf)
- [CBS LA: FAA changes at Van Nuys](https://www.cbsnews.com/losangeles/news/faa-implements-changes-to-la-area-airport-to-lower-risk-of-midair-collisions/)
- [AIN: Boston runway closes for safety project](https://backend.ainonline.com/aviation-news/aerospace/2025-09-02/boston-runway-closes-safety-improvement-project)
- [Boston 9/27 reopens (18 Nov 2025)](https://rock929rocks.com/2025/11/18/boston-logans-runway-9-27-reopens-following-safety-upgrades/)
- [CVG 18C/36C rehabilitation RFP](https://airportscouncil.org/rfp/24-24-runway-18c-36c-rehabilitation-tw-d2-demo-relocation-and-runway-18l-36r-rsa-grading-corrections)
- [FAA extends Newark order](https://www.faa.gov/newsroom/faa-extends-order-limiting-operations-newark-liberty-international-airport)
- [CBC: Nav Canada resource constraints at Pearson](https://www.cbc.ca/lite/story/9.6963586)
- [BNN Bloomberg: Canadian tower closures](https://www.bnnbloomberg.ca/business/company-news/2025/10/24/staff-shortages-shutting-two-canadian-airport-control-towers-periodically-memo-says/)
- [Belga: Brussels Airport 14 Oct 2025](https://www.belganewsagency.eu/brussels-airport-cancels-all-departing-flights-on-14-october)
- [French ATC strike called off](https://newswav.com/article/french-air-traffic-controllers-call-off-three-day-strike-will-there-be-more-A2510_Iwo4Dj)

Verification level: the SFO, VNY FAQ, CBS, AIN and CBC pages were read through a summarising fetch, not in full. The Boston reopening date, the Newark extension, the SFO 2026 ban, the Canadian tower closures, the Brussels strike and the French strike cancellation rest on search-result headlines only and were not opened. The SFO and VNY pages give no dates precise enough to pin to the study windows. The AIN page did not name the Boston runway; the identification of 9/27 comes from the reopening headline and from the zero runway-27 landings in the 2025 data.
