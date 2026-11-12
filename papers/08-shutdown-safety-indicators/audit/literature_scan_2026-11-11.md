<!-- Research scan run on 11 November 2026, before preregistration. Kept as produced; later checks are in sources.md. -->

# The 2025 US Shutdown and Airport Safety Indicators: Novelty Check, Verified Timeline, and Staffing-Exposure Data (scan as of 11 November 2026)

As of November 2026, this scan found no study, preprint, government report or data-journalism piece that used flight-track data (ADS-B or FAA surveillance data) or occurrence-report counts to measure go-around rates, TCAS resolution advisories, losses of separation or runway incursions during the 1 October – 12 November 2025 shutdown. The planned study therefore appears novel. The closest work measures delays: the Richmond Fed brief, A4A analyses and the CRS report. The FAA's own safety data was described only qualitatively and was never released.

## TL;DR

- **Novelty:** No published flight-data or occurrence-data measurement of shutdown-period safety indicators was found. The FAA's emergency orders cited "voluntary safety reports" and "increased stress on the NAS in aviation safety data" but gave no numbers. Secretary Duffy said on 11 November 2025: "I'm not going to give the exact numbers." The Richmond Fed brief EB 25-45 (Russell Wong, 19 December 2025) is the nearest design template: difference-in-differences on BTS delays at 82 ASPM airports. It is a delay study, not a safety study.
- **Timeline:** These dates are verified against primary sources:
  - The lapse ran from 1 October 2025 to the signing of P.L. 119-37 on the evening of 12 November 2025, about 10:20–10:25 p.m. EST. That is 43 days.
  - The flight-reduction order was issued and took effect on 7 November (FR 2025-19850, 90 FR 50884). It was replaced by a 6% order effective 6:00 a.m. on 13 November (FR 2025-19986, 90 FR 51426), cut to 3% by an addendum effective 15 November, and cancelled effective 6:00 a.m. EST on 17 November (FR 2025-20308, 90 FR 52132, published 19 November). CRS's "canceled on November 19" is the Federal Register publication date, not the effective date.
- **Staffing exposure:** No compiled facility-by-date dataset of staffing triggers exists publicly. One can probably be rebuilt. The ATCSCC per-date advisory list endpoint on fly.faa.gov still served a September 2025 page on 11 November 2026, and each "OPERATIONS PLAN" advisory contains a "STAFFING TRIGGER(S):" section. Retrieval of October–November 2025 and 2024 pages was not directly confirmed. Published daily counts exist only for scattered days.

## Key Findings

1. **No prior safety measurement with flight data was found.** The searches covered arXiv, the OpenSky literature, CRS, GAO-adjacent sources, Senate testimony, A4A, news analyses and aviation blogs. Every quantitative shutdown study identified measures delays, cancellations, passengers disrupted, or staffing-trigger counts.
2. **Official safety claims are qualitative and unpublished.** The 7 November order states: "the FAA assessed voluntary safety reports submitted for the month of October. The reports indicated users of the system had concerns about its performance... The FAA has also observed evidence of increased stress on the NAS in aviation safety data, particularly at 40 high traffic airports." The 16 November cancellation order adds that "This data indicated a correlation between ATO staffing and stress on the NAS." No counts of losses of separation, runway incursions or reports were published in the orders, press releases or the CRS report.
3. **The "dose" variable is partly observable.** Daily national counts of staffing triggers exist for some dates; for example the FAA reported a record 81 on 8 November and 1 on 16 November. Facility names are reported only anecdotally. A facility-by-date panel must be rebuilt from the ATCSCC operations-plan archive.
4. **The orders themselves changed operations in ways that can move go-around and RA rates.** They did more than cut scheduled flights:
   - general aviation was banned at 12 hubs;
   - GA could be cut by up to 10% at the high-impact airports;
   - when staffing was inadequate, ATC could withhold VFR radar services, traffic pattern operations and practice approaches.

   This confounds a pure "controller strain" interpretation from 7 to 17 November.

## Part A — Has anyone already measured this with flight data?

### A1. Safety-indicator studies (the novelty question)

**Result: none found.** The searches looked for shutdown-period go-around, TCAS RA, loss-of-separation, runway-incursion or similar safety metrics built from ADS-B/OpenSky/FAA data or ASRS/ATSAP counts. Nothing matched in arXiv, the OpenSky Network literature, congress.gov/CRS, Senate Commerce hearing materials, A4A, the Richmond Fed, or news and blog coverage. The documents examined include:

- **CRS R49491, "Federal Government Shutdowns and the Impact on Civil Aviation"** (Bart Elias and Rachel Y. Tang, 22 October 2026).
  - It is the most comprehensive official review. It covers 2018–19, October–November 2025, 31 January – 3 February 2026, and the DHS lapse of 14 February – 30 April 2026.
  - Its 2025 aviation evidence is descriptive: the Burbank tower going unstaffed on 6 October, A4A delay and cancellation figures, and the flight-reduction orders.
  - It uses no safety-event data. It notes that FAA overtime use reached 7.3% in FY2025 and quotes the FAA's *Air Traffic Controller Workforce Plan 2026–2028*: "[c]hronic use of overtime leads to fatigue, controller burnout and ultimately loss of retention."
- **Senate Commerce Aviation Subcommittee hearing, "Flying on Empty: How Shutdowns Threaten Air Safety, Travel, and the Economy"** (19 November 2025; S. Hrg. 119-318). Witnesses were Nick Daniels (NATCA), Chris Sununu (A4A), and statements from NBAA and ASTA. The testimony found gives delay, cancellation and economic figures. No FAA safety-event numbers were located in it. Chairman Moran's announcement said the safety data "was blinking red" but gave no figures.
- **FAA/DOT press releases** of 6, 12, 14 and 16 November 2025 report staffing-trigger counts only.

**Caveat on exhaustiveness:** I could not run the full search list. Google Scholar, SSRN, ResearchGate full-text, TRB/TRR, AIAA SciTech/Aviation 2026, ATM Seminar, SESAR Innovation Days, the OpenSky Symposium 2026, MITRE/RAND, DOT OIG, GAO and Substack were not each searched individually. A preprint indexed only in those venues cannot be ruled out. Before preregistration, run a final check of these venues for "shutdown" combined with "go-around", "TCAS", "ADS-B" and "loss of separation".

### A2. Delay and economic studies (not safety studies)

| Study | Data | Identification | Main result |
|---|---|---|---|
| Richmond Fed Economic Brief EB 25-45, Russell Wong, "The Value of Government Services: Evidence From Flight Delays During the 2025 Shutdown" (19 Dec 2025) | 76 million BTS flight operations since 2022 at 82 ASPM airports; FAA-initiated delays; daily NOAA airport weather; BLS metro-area wages | Difference-in-differences comparing the same airports in and out of the shutdown window, with weather controls and airport-specific seasonality. Only effects significant at 1% are reported. | Six airports significant: BOS, DCA, EWR, JFK, LGA, SFO. About 1.0 million extra work-hours of delay, about $66 million. Delay increases: BOS +527%, DCA +547%, EWR +438%, JFK +410%, LGA +536%, SFO +210%. |
| A4A news updates (9–10 Nov 2025) and Sununu Senate testimony (19 Nov 2025) | FAA NAS delay data, A4A member airlines | Descriptive | Staffing's share of NAS delay minutes: 5% Jan–Sep 2025, 16% October, 47% for 1–6 Nov, 61% for 7–9 Nov, 71% on 8 Nov (more than 184,000 staffing delay minutes, the shutdown high), 62% for November. 7–12 Nov: more than 15,600 staffing-related delays, more than 7,100 staffing-related cancellations, 2.3 million passengers disrupted. |
| Cirium estimate (reported by AP, 5–6 Nov 2025) | Schedules | Projection | A 10% cut could be up to 1,800 flights and 268,000 seats; ORD could lose 121 of 1,212 Friday flights. This is a forecast, not an outcome. |

These are **delay studies, not safety studies.** The Richmond Fed design suits a go-around study: the same airport in and out of the window, airport seasonality, and weather controls. It has two weaknesses for this purpose.

- It uses a single national shutdown window and no facility-level exposure.
- Its strict 1% threshold leaves only six "treated" airports.

A staffing-trigger dose variable would strengthen identification beyond this design.

### A3. Earlier and later shutdowns

- **2018–19 (22 Dec 2018 – 25 Jan 2019, 34–35 days).**
  - CRS reports that most aviation safety inspectors were initially furloughed, with 2,148 recalled by the final week.
  - Callouts on 25 January 2019 at the Washington and Jacksonville centers caused delays at LGA, EWR and PHL; the shutdown ended that day.
  - The 2019 House T&I hearing "Putting U.S. Aviation at Risk" (13 Feb 2019) heard that ATSAP and ASAP processing was curtailed.
  - The Partnership for Public Service report "Shutdown Letdown" (Sept 2019) documents the FAA cutting its FY2019 controller hiring target by 524.
  - **The often-cited figure that FAA voluntary safety reports fell about 14% could not be verified in this scan; treat it as unsourced.** No ASRS-based empirical analysis of the 2019 shutdown was found.
- **31 January – 3 February 2026.** A three-day lapse that affected FAA and TSA, ended by P.L. 119-75. CRS gives no operational safety data.
- **DHS lapse, 14 February – 30 April 2026 (75 days; P.L. 119-86).** It affected TSA, not FAA air traffic control.
  - TSA callouts rose from about 4% to 11% on average.
  - Callouts were 36–43% at MSY, JFK, ATL, HOU and IAH on 24 March 2026.
  - About 460 screeners resigned in the first five weeks.
  - No ATC safety studies were found. Because FAA controllers were paid, this lapse is a possible placebo period for ATC-specific effects. It is not a clean control for airport operations, since screening queues changed.

### A4. What officials said the FAA's data showed

- **Duffy, 11 November 2025** (Mosinee, WI, and Fox News):
  - "We have seen incursions on runways. We have seen loss of separation in the airspace, and we have seen heightened complaints by pilots of the communication they are having with air traffic controllers."
  - Also: "I'm not going to give the exact numbers."
- **Emergency order texts** (7, 12 and 16 Nov): only the qualitative language quoted above.
- **12 November DOT release:** "Low staffing triggers are a leading indicator for key safety trends." No safety metric was given.
- **Bedford:** statements found concern staffing-trigger declines. No safety-event numbers were found.
- **Follow-ups:**
  - On 1 December 2025 the FAA said it was investigating whether airlines with more than 10 daily operations at any high-impact airport complied with the order, with fines of up to $75,000 per excess flight.
  - No FOIA release, DOT OIG report or GAO report quantifying shutdown-period losses of separation, incursions or voluntary reports was found.
  - **Conclusion: the underlying FAA safety numbers have not been published as far as this scan could determine.**

### A5. Specific incidents during the shutdown

| Date | Event | Status |
|---|---|---|
| 6 Oct 2025 | Hollywood Burbank (BUR) tower unstaffed in the afternoon and evening ("ATC Zero"). ATCSCC advisory 070 BUR/ZLA set a ground delay program; aircraft self-separated on the CTAF. | Confirmed: CRS R49491 citing the LA Times; ATCSCC advisory |
| 25–26 Oct 2025 | 22 staffing triggers on Saturday 25 Oct. On Sunday 26 Oct a SoCal TRACON shortage briefly halted LAX flights and DCA had a staffing ground delay. | CNN, 27 Oct 2025 |
| 29 Oct 2025 | Southwest WN1333 (B737-700 N280WN, BWI–CLE) on final for CLE runway 6L about 4 nm out, versus a Metro Aviation Airbus H145 air ambulance. Same altitude, about 2,075 ft; Flightradar24 shows about 0.56 nm lateral. TCAS RA, then go-around. NTSB opened an investigation on 1 Nov 2025 ("loss of separation event"). | Confirmed NTSB investigation. **No NTSB finding links it to staffing**; ATC had issued traffic and visual-separation instructions. |
| 30 Oct 2025 (Thu) | Boston: Delta arrival from Paris went around within about half a mile of a departing Cape Air Cessna 402C. | Reported secondhand (Jalopnik via Yahoo); not verified against FAA or NTSB |
| 9 Nov 2025 | Duffy: "Eighteen of 22 air traffic controllers at Atlanta... did not show up to work on Sunday." | Secondhand (CBS live blog) |
| 4 Nov 2025 | UPS crash after takeoff at Louisville (SDF, one of the 40 airports), referenced in NATCA testimony | Not attributed to ATC staffing; relevant as an SDF disruption confounder |

### A6. Verdict on novelty

**As of November 2026, a flight-data measurement of go-around rates or TCAS RAs during the 2025 shutdown appears to be novel.** The closest prior work, and how it differs:

1. Richmond Fed EB 25-45: delays, BTS data, airport-level difference-in-differences, no safety outcome.
2. CRS R49491: descriptive policy review, no safety-event data.
3. A4A and CNN/AP analyses: delay shares and staffing-trigger counts.
4. FAA internal safety analyses: they exist but are unpublished and gave no numbers.
5. Generic ADS-B go-around and TCAS methods papers (Part D): none applied to this period.

## Part B — Verified timeline

### B1. Lapse in appropriations

- **Start:** 12:01 a.m. EDT, 1 October 2025, the start of FY2026, when none of the 12 bills or any CR had been enacted (CRS R49491).
- **End:** P.L. 119-37 (Continuing Appropriations, Agriculture, Legislative Branch, Military Construction and Veterans Affairs, and Extensions Act, 2026), signed 12 November 2025.
  - The House passed it 222–209 on the evening of 12 November.
  - CBS's live blog timestamped "Trump signs legislation" at 10:24 p.m.; The Hill's report is time-stamped 10:25 p.m. ET. Signing was therefore about 10:20 p.m. EST.
  - It funded DOT and FAA by CR through 30 January 2026.
- **Length:** 43 days (CRS). Some outlets, such as Federal News Network, say "44-day," which counts both end days; use 43.
- **Note for study windows:** the emergency order text says "air traffic controllers have been working without pay since October 3, 2025." This reflects pay-period accounting, not the lapse start.

### B2. Controller pay timeline

| Date | Event | Source |
|---|---|---|
| 14 Oct 2025 | Partial paycheck (some reports say 15 Oct) | NATCA, 24 Oct 2025; CNBC, 14 Oct |
| 28 Oct 2025 | First $0 paycheck | NATCA; Skift; Larsen/Carson statement, 28 Oct |
| Tue 11 Nov 2025 | Second missed paycheck (pay period ending 1 Nov). AP, via Fortune on 10 Nov 2025: "Tuesday will be the second missed payday for controllers and other FAA employees." NATCA held a press conference on 10 Nov to mark "the second consecutive zero-dollar paycheck." | AP via Fortune, 10 Nov 2025; NATCA |
| Fri 14 Nov 2025 | Partial back pay arrived. CNBC (15 Nov 2025): controllers "were paid in part on Friday, according to people familiar with the matter." Duffy had pledged on 11 Nov that 70% of back pay would arrive within 48 hours of reopening. **The date full back pay was completed is not verified.** NATCA noted that in 2019 it took over two months. | CNBC, 15 Nov 2025 |
| 20 Nov 2025 (Thu), reported 21 Nov | $10,000 bonus for "perfect attendance" to 776 controllers and technicians; payment "no later than Dec. 9" | FAA/DOT via CNBC, The Hill, Washington Times |

The reported split of the bonus recipients, 311 NATCA-represented controllers and 423 technicians (AP via The Hill), sums to 734, not 776. The discrepancy is unresolved.

### B3. The emergency orders

**Order 1: "Emergency Order Establishing Operating Limitations on the Use of Navigable Airspace"**
- Announced Wednesday 5 November 2025 (AP); FAA press release dated 6 November.
- Issued and effective 7 November 2025.
- Published at 90 FR 50884–50886, FR Doc. 2025-19850, on 12 November 2025 (filed 11-7-25, 12:30 p.m.).

What it required:
- **Operators and scope:** every 14 CFR Part 121 and commuter or scheduled Part 135 carrier at the 40 high-impact airports must cut "total daily scheduled domestic operations between 6:00 a.m. and 10:00 p.m. local." International flights were not covered.
- **Phasing:** at least 4% by 6:00 a.m. EST on 7 Nov, 6% by 11 Nov, 8% by 13 Nov, and 10% by 14 Nov.
- **Calculation:** by marketing code, with no more than 15% per operating certificate. The baseline was "currently scheduled operations." Cuts were set seven days ahead on a rolling basis.
- **Penalties:** $75,000 per excess flight, or $16,630 for small businesses.

**Order 2: replacement order**
- Issued 12 November and effective 6:00 a.m. on 13 November 2025.
- Published at 90 FR 51426–51429, FR Doc. 2025-19986, on 17 November 2025.
- It froze the cut at 6%, with cuts set four days ahead on a rolling basis.
- International cuts were voluntary but could be credited toward the domestic requirement.
- It added the Appendix B general aviation prohibition (see B5).
- DOT's 12 November release cited the trigger decline: "only eleven staffing triggers on Tuesday, November 11 and four staffing triggers today from a high of 81 on November 8."

**14 November addendum**
- Cut the requirement to 3%, effective 6:00 a.m. on 15 November (FAA release of 14 November; Newsweek).

**Cancellation**
- Issued 16 November and effective at 6:00 a.m. EST on 17 November 2025.
- FR Doc. 2025-20308, 90 FR 52132–52133, published 19 November 2025.

**Reconciling 17 vs 19 November:** the cancellation took effect on 17 November. CRS's "measures were canceled on November 19" cites the Federal Register publication (footnote 56). CRS's own later section correctly says the orders "were lifted on November 17." Use 6:00 a.m. EST, 17 November 2025.

### B4. The 40 high-impact airports (Appendix A, verbatim names as printed in both orders)

ICAO codes are added by me; they are not in the order.

| FAA | ICAO | Name as printed in Appendix A |
|---|---|---|
| ANC | PANC | Ted Stevens Anchorage International Airport |
| ATL | KATL | Hartsfield-Jackson Atlanta International |
| BOS | KBOS | Boston Logan International |
| BWI | KBWI | Baltimore/Washington International |
| CLT | KCLT | Charlotte Douglas International |
| CVG | KCVG | Cincinnati/Northern Kentucky International |
| DAL | KDAL | Dallas Love Field |
| DCA | KDCA | Ronald Reagan Washington National |
| DEN | KDEN | Denver International |
| DFW | KDFW | Dallas/Fort Worth International |
| DTW | KDTW | Detroit Metropolitan Wayne County |
| EWR | KEWR | Newark Liberty International |
| FLL | KFLL | Fort Lauderdale/Hollywood International |
| HNL | PHNL | Honolulu International |
| HOU | KHOU | William P. Hobby Airport |
| IAD | KIAD | Washington Dulles International |
| IAH | KIAH | George Bush Houston Intercontinental |
| IND | KIND | Indianapolis International |
| JFK | KJFK | New York John F. Kennedy International |
| LAS | KLAS | Las Vegas McCarran International |
| LAX | KLAX | Los Angeles International |
| LGA | KLGA | New York LaGuardia |
| MCO | KMCO | Orlando International |
| MDW | KMDW | Chicago Midway |
| MEM | KMEM | Memphis International |
| MIA | KMIA | Miami International |
| MSP | KMSP | Minneapolis/St. Paul International |
| OAK | KOAK | Oakland International |
| ONT | KONT | Ontario International |
| ORD | KORD | Chicago O'Hare International |
| PDX | KPDX | Portland International |
| PHL | KPHL | Philadelphia International |
| PHX | KPHX | Phoenix Sky Harbor International |
| SAN | KSAN | San Diego International |
| SDF | KSDF | Louisville International |
| SEA | KSEA | Seattle/Tacoma International |
| SFO | KSFO | San Francisco International |
| SLC | KSLC | Salt Lake City International |
| TEB | KTEB | Teterboro |
| TPA | KTPA | Tampa International |

The order uses outdated names for LAS (now Harry Reid) and HNL (now Daniel K. Inouye). The list includes cargo hubs (MEM, SDF, ANC, CVG) and a business-aviation airport (TEB). Notable large or medium airports not on the list, possibly useful as within-US comparisons, include AUS, BNA, MSY, RDU, SJC, SMF, STL, MCI, CLE, PIT and BUR. Several of these had staffing triggers themselves (AUS, BNA, BUR, MSY towers), so absence from the list does not mean they were unexposed.

### B5. Other restrictions that can mechanically affect go-around and RA rates

- **GA cuts and dual Airspace Flow Programs:** both orders allow a "dual Airspace Flow Program strategy" for GA and commercial traffic when triggers occur. GA "may also be reduced by up to 10 percent at High Impact Airports, including TEB, HOU, and DAL."
- **GA prohibition at 12 airports (Appendix B of the 12 November order):** ATL, BOS, DCA, DEN, DFW, EWR, IAH, JFK, LAX, ORD, PHX, SEA.
  - It covered Part 91, non-scheduled Part 135 and Part 380 public charter.
  - Exceptions: helicopters, based aircraft, emergency/medical/law-enforcement/firefighting/military flights, and ATCSCC-authorised aircraft.
  - Before the 12 November order, the same restriction was imposed through 12 airport-specific NOTAMs the FAA issued on 9 November 2025. Vertical Aviation International: "Closures are effective Nov. 10, 2025, (UTC-5), through Dec. 31, 2025, unless canceled earlier." NATA said the restrictions were "published as individual NOTAMs for each affected facility." NBAA put the start at midnight Monday (The Hill, 10 Nov 2025).
- **ATC services that could be withheld** at understaffed FAA facilities:
  - Radar Traffic Information Service;
  - radar assistance and terminal radar services to VFR aircraft;
  - VFR traffic pattern operations;
  - practice approaches;
  - flight checks;
  - services to parachute operations;
  - "certain special or unusual operations";
  - non-activation of ATCAAs and MOAs.

  DOT and FAA releases summarised these as limits on "some visual flight rule approaches at facilities with staffing triggers" and on "parachute operations and photo missions."
- **Commercial space:** launches and reentries allowed only between 10 p.m. and 6 a.m. local, from 6:00 a.m. EST on 10 November (13 November under the replacement order).
- **Visual approaches and visual separation:** **no restriction on IFR visual approaches or controller-applied visual separation was found in either order's text.** The "VFR approaches" language concerns VFR aircraft services.

### B6. Compliance and actual cancellations

- A4A: of 861 staffing-related cancellations on 12 November, 99.8% were attributable to the mandate.
- A4A put the 6% directive at about 875 cancellations and 60,000 disrupted passengers per day at the 40 airports, "more than 13 times the normal rate."
- A4A members cancelled only 11 flights for controller staffing in the first 29 days of the shutdown. They cancelled 1,271 over the next nine days.
- CNN reported more than 2,700 daily US cancellations on 9 November, combining mandate, staffing and weather.
- The FAA opened compliance investigations on 1 December 2025.
- **No per-airport realised-reduction dataset was found.** Measure realised cuts directly from ADS-B or BTS counts rather than assuming the ordered 4/6/3%.

## Part C — Staffing shortfalls by facility and date

### C1. What a staffing trigger is and where it is published

A staffing trigger is a notice in an ATCSCC "OPERATIONS PLAN" advisory that a facility (tower, TRACON or area, or ARTCC) has staffing below what it needs to run its planned configuration. It may lead to traffic management initiatives such as ground stops, GDPs or miles-in-trail. Plans list entries under "STAFFING TRIGGER(S):", for example "UNTIL 0300 -PHL AREA C / UNTIL 0800 -L30 TRACON". Several plans are issued per day, so one facility can appear repeatedly. Counts of "reports" (CNN) and "facilities" (AP, FAA) therefore differ.

### C2. Archive availability (checked 11 November 2026)

- **Official form:** fly.faa.gov/adv/advAdvisoryForm, which offers only the last 15 days.
- **Per-date list endpoint:** this pattern still worked:
  `https://www.fly.faa.gov/adv/adv_list?whichAdvisories=ATCSCC&advisoryCategory=All&date=YYYY-MM-DD&...`
  - It returned the full ATCSCC index for 2025-09-24, with links of the form `adv_otherdis?adv_date=MMDDYYYY&advn=NNN`.
  - A GitHub issue on the cyanheads/faa-traffic-delays-mcp-server repository reports the endpoint returning pages back to 2004.
  - **Retrieval for dates between 1 October and 30 November 2025, and for 2024, was not directly confirmed** (one test returned a cached September page). Check this first.
- **Wayback Machine:** not checked.
- **Compiled datasets:** none found on GitHub, Kaggle, Zenodo or Dataverse, and none from AP, CNN, Reuters, the Washington Post, NYT, Bloomberg or USA Today. CNN and AP described analyses of the operations plans but released no files. The Richmond Fed brief has an appendix PDF but no replication data was found.

### C3. Day-by-day published counts, 1 October – 17 November 2025

| Date | Count | Unit / note | Source |
|---|---|---|---|
| 1–24 Oct | not published daily | CNN: "at least 264 instances" 1–26 Oct vs 60 on the same dates in 2024 | CNN, 27 Oct |
| Sat 4, 11, 18 Oct | ≤12 each | "each of the three prior Saturdays saw a maximum of a dozen" | Forbes, 28 Oct |
| 6 Oct | BUR tower ATC Zero | facility event | ATCSCC advisory; CRS |
| Fri 24 – Sun 26 Oct | >50 | reports | CNN, 27 Oct |
| Sat 25 Oct | 22 | facilities ("staffing triggers") | Duffy on Fox, 26 Oct; Forbes |
| Tue 28 Oct | 7 | facilities in one 5:28 p.m. EDT plan (incl. Dallas, Denver, Newark) | Forbes, 28 Oct |
| 31 Oct (Fri) | 46 | facilities | CNN, 3 Nov |
| 1 Nov (Sat) | 34 | facilities | CNN, 3 Nov |
| 2 Nov (Sun) | 18 | facilities | CNN, 3 Nov |
| 31 Oct – 2 Nov | 98 reports; AP: "at least 39" facilities | AP likely counts unique facilities | CNN; AP via PBS |
| 1 Oct – 2 Nov | 393 | cumulative reports, about 4x 2024 | CNN, 3 Nov |
| Weekend averages | 8.3 (Jan 1–Sep 30) vs 26.2 (five shutdown weekends) | facilities per weekend | AP, 5 Nov |
| ~6 Nov | 17 | "airports" | NBC live blog |
| 7 Nov (Fri) | 32 | reports ("short-staffed 32 times"); cumulative 482 | CNN live blog, 7 Nov |
| 8 Nov (Sat) | 81 | record; mid-day reports said about 36–42 | FAA/DOT, 12/14/16 Nov |
| 9 Nov (Sun) | not published | ATL: 18 of 22 controllers absent (Duffy) | CBS |
| 10 Nov | not published | — | — |
| 11 Nov | 11 | Duffy said "four" by late afternoon | DOT, 12 Nov |
| 12 Nov | 13 (final); 4 (same-day) | **conflict:** later release revises | DOT, 14 Nov vs 12 Nov |
| 13 Nov | 4 | — | DOT, 14 Nov |
| 14 Nov | 6 (final); 3 (same-day) | **conflict** | FAA, 16 Nov vs 14 Nov |
| 15 Nov | 8 | — | FAA, 16 Nov |
| 16 Nov | 1 | "aligns with staffing conditions before the shutdown" | FAA, 16 Nov |
| 17 Nov | — | order cancelled 06:00 EST | FR 2025-20308 |

When an earlier same-day count conflicts with a later full-day count, use the later full-day figures.

### C4. Most- and least-affected facilities

**Most affected, from named reports:**
- The Newark operation (N90/EWR) had the most triggers over 31 Oct – 2 Nov (CNN). The FAA said on 31 Oct that nearly 80% of controllers were absent at New York-area facilities; Fortune quoted "nearly 90 percent."
- The FAA said on 31 Oct that "nearly 50 percent of major air traffic control facilities" were short. This is the "half of the Core 30" claim.
- Towers named: Austin, Boston, Burbank, Dallas, Denver, DCA, Nashville, New Orleans, Ontario, Phoenix, San Francisco, Tampa.
- TRACONs named on 7 Nov: Atlanta (A80), Chicago (C90), Houston (I90, twice), Las Vegas, Newark (twice), Orlando, Phoenix, SoCal (SCT, three areas).
- Richmond Fed delay effects concentrated at BOS, DCA, EWR, JFK, LGA and SFO.

**Least affected:** no published source lists large airports with zero triggers. Richmond Fed found no statistically significant effect at 76 of 82 airports at the 1% level; this is suggestive but is not a staffing measure. Facility-level zero-exposure units must come from the rebuilt archive. No specific en-route center (ZDC, ZJX, ZNY) or PCT/D10/D01/NCT/I90 trigger was confirmed by date beyond the 7 Nov list.

### C5. Alternative exposure: OPSNET/ASPM

The Richmond Fed relied on FAA system-impact delay data for the 82 ASPM airports. OPSNET records delays by cause (including staffing, labelled e.g. "STAFFING:TERMINAL" and "STAFFING:CENTER" in advisories). Its suitability as a public daily airport-level exposure measure, and whether ASPM modules can be downloaded without an account, **were not verified in this scan.** My understanding is that OPSNET is publicly queryable and parts of ASPM require registration; confirm both on aspm.faa.gov.

## Part D — Methods and practical inputs

### D1. Detecting go-arounds from ADS-B, and baseline rates

| Work | Setting | Rate / method |
|---|---|---|
| Proud (2020), "Go-Around Detection Using Crowd-Sourced ADS-B Position Data" | Mumbai (VABB), Aug 2018 – Aug 2019; OpenSky | 392 go-arounds in 153,765 landing attempts, about 2.5 per 1,000; compares five detection methods against manual labels |
| Kumar, Corrado, Puranik, Mavris, *Aerospace* 8(10):291 (2021) | SFO 2019; OpenSky | 890 single go-arounds; 61 features; HDBSCAN clusters into nominal, anomalous and late go-arounds; cites 1–3 per 1,000 approaches as typical |
| Figuet et al., "Predicting Airplane Go-Arounds Using Machine Learning and Open-Source Data" | Zurich runway 14 | 715 go-arounds, about 3 per 1,000; macroscopic (next-hour) and microscopic models |
| Monstein, Figuet, Waltert et al., "Large Landing Trajectory Dataset for Go-Around Analysis," *Eng. Proc.* 28:2 (2022) | Global, OpenSky, incl. US operators | Quasi-binomial GLM per airport–runway; operator-level rates at US airports |
| "Analysing the Impact of Go-Around Occurrences at Large European Airports" | 20 European airports, Jan 2019 – Jul 2023 | Mean 3.1 per 1,000; airport range 1.5–6; type range 1–4.5 |

**Sample-size implication:** at about 3 per 1,000, a hub with about 600 daily arrivals produces about 1.8 go-arounds per day. Day-level counts are highly overdispersed because weather drives clusters. Plan for airport-week or pooled models with negative-binomial or quasi-binomial errors. This scan did not retrieve published day-to-day variance figures or FAA/Eurocontrol/DGAC/FSF national rates.

### D2. TCAS RAs from open receiver data

- **Schäfer, Olive, Strohmeier, Smith, Martinovic, Lenders, "OpenSky Report 2019: Analysing TCAS in the Real World using Big Data," DASC 2019.**
  - Data: 250 billion Mode S replies from 126,700 aircraft, 10–23 May 2019.
  - RAs are detected from Comm-B BDS 3,0 (active RA) replies. BDS 1,0 gives equipage information.
  - About 89.5% of ADS-B-equipped aircraft had operational TCAS.
  - Key limitation: BDS 3,0 is only seen when a ground or airborne interrogator elicits it within a receiver's range. Capture is therefore partial and coverage-dependent.
- **Known artefacts:**
  - The 1 March 2025 DCA false alerts: the FAA said "Some of the crews executed go-arounds as a result of the alerts" and was investigating.
  - Helicopter and VFR conflicts: DCA had 15,200 losses of separation between airliners and helicopters since 2021 (NTSB, March 2025).
  - At BUR, during an evaluation in 2025, the FAA lowered the Van Nuys traffic pattern by 200 ft. This reduced TCAS alerts for Burbank arrivals and was made permanent on 5 January 2026. **This is a direct RA-rate confounder at BUR within the comparison window.** The FAA's VNY community-engagement page describes a 180-day evaluation, "100 feet lower than usual for 90 days, then 200 feet lower for the next 90 days," and says "BUR experiences a high number of TCAS alerts, with a rate far exceeding the NAS average." The calendar dates of the evaluation remain unconfirmed.
- **Not covered by this scan:** published US terminal RA baselines per 100,000 flight hours (FAA TOPA, MIT Lincoln Laboratory, Eurocontrol), the format of readsb/adsb.lol ACAS output, and quantified capture fractions. These need direct literature retrieval.

### D3. Mechanism evidence

The scan retrieved only secondary material:
- The FAA workforce plan, via CRS, links chronic overtime to fatigue. Overtime reached 7.3% in FY2025, versus about 2.1% in 2008–2011. Time on position fell from 4.68 hours to 4.01 hours per shift between 2008 and 2025.
- Many controllers work six 10-hour days a week (AP, Nov 2025).

**Not retrieved:** CAMI fatigue studies, the National Academies controller-staffing reports, NTSB fatigue recommendations, DOT OIG reports, and any study of go-around rates responding to traffic density or reduced arrival rates.

The direction of effect is a priori ambiguous. Strain could increase spacing errors. Traffic management initiatives and the orders lowered traffic density, and that could reduce go-arounds. The design should model traffic volume explicitly.

### D4. Confounders for an autumn 2025 vs 2024 comparison

Partly verified:
- **DCA:** visual separation between helicopters and fixed-wing aircraft eliminated in February 2025 and within 5 nm from March 2025, after the 29 January 2025 collision. On 18 March 2026 the FAA and DOT issued a GENOT suspending visual separation between airplanes and helicopters in Class B, Class C and TRSA airspace nationally, stating: "The FAA's data analysis revealed for high-traffic areas, visual separation was not enough of a safety mitigation tool." This falls after the study window but matters for any later comparison period.
- **BUR / Van Nuys:** pattern change in 2025 (above).
- **SDF:** UPS accident on 4 November 2025.
- **TCAS alert episodes:** the DCA false alerts of 1 March 2025.

From background knowledge, not re-verified here:
- Hurricanes Helene (late September 2024) and Milton (9–10 October 2024, with TPA and MCO closures).
- Newark disruptions in 2025: the Philadelphia TRACON outages from 28 April, runway 4L/22R works, and FAA flight caps at EWR running into late October 2025.

Not researched:
- weather events in October–November 2025;
- JFK, ORD, SFO and DEN construction;
- growth of the adsb.lol receiver network between 2024 and 2025.

### D5. METAR sources (not re-verified in this scan)

- Iowa Environmental Mesonet ASOS/AWOS archive: bulk CSV through its request interface. It is the standard choice for US and many international stations.
- NOAA NCEI Integrated Surface Database / Global Hourly.
- Ogimet for international METARs.
- aviationweather.gov keeps only recent data, so it is unsuitable for 2024–2025 history.

Confirm URL patterns and licences before preregistration. The Richmond Fed used daily NOAA airport weather.

### D6. Canada and Europe as controls

**Not verified in this scan.** No source was retrieved on Nav Canada staffing in October–November 2025, French ATC strikes or European outages in that window. Check these, along with whether US reductions touched transborder flights. The US orders covered only domestic operations, but staffing ground stops at US destinations affected all inbound traffic.

## Recommendations

1. **Run a final novelty sweep** of Google Scholar, SSRN, TRB, AIAA 2026, the OpenSky Symposium 2026 and the ATM Seminar before preregistration, and record the search date.
2. **Rebuild the exposure panel** from the fly.faa.gov per-date advisory lists for 1 September – 30 November in 2024 and 2025.
   - Parse "STAFFING TRIGGER(S)" by facility and hour.
   - Validate the totals against the FAA's published figures (81 on 8 Nov; 11, 13, 4, 6, 8 and 1 on 11–16 Nov) and CNN's cumulative counts (264, 393, 482).
   - Archive the raw HTML.
3. **Split the treatment window** into three phases, because the orders changed traffic mix and VFR services at the same time as staffing improved:
   - 1 Oct – 6 Nov: strain only;
   - 7 – 16 Nov: strain plus mandated cuts and GA bans;
   - 17 Nov onward: recovery.
4. **Borrow the Richmond Fed identification** (same airport in and out of the window, airport seasonality, weather controls). Add facility-day trigger exposure and realised traffic volume as covariates.
5. **Treat TCAS RA counts as a secondary, coverage-limited outcome.** Report receiver coverage by airport-year, and exclude or flag DCA and BUR.

## Caveats and unresolved or conflicting facts

- **Staffing-trigger counts:** 12 Nov is 4 (same-day) vs 13 (later); 14 Nov is 3 vs 6. CNN counts reports while AP and the FAA count facilities (98 vs "at least 39" for 31 Oct – 2 Nov).
- **New York absences:** "nearly 80%" (CNN) vs "nearly 90 percent" (Fortune quoting the FAA, 31 Oct).
- **Cancellation date:** CRS says 19 Nov (publication date); the effective date is 17 Nov, 06:00 EST.
- **Shutdown length:** 43 days (CRS) vs "44-day" (some outlets).
- **Bonus recipients:** 776 total vs a 311 + 423 = 734 breakdown.
- **Unverified items:**
  - the about 14% fall in FAA voluntary reports in 2019;
  - the date full back pay was completed (partial back pay arrived 14 Nov per CNBC);
  - the calendar dates of the Van Nuys pattern evaluation;
  - archive retrieval for October–November 2025 and 2024;
  - OPSNET/ASPM access terms;
  - Nav Canada and European disruptions;
  - RA baseline rates;
  - adsb.lol receiver growth.
- **FAA safety data:** described qualitatively only. No loss-of-separation, incursion or voluntary-report counts for the shutdown were found in any public release, hearing record or report.

## Sources consulted

- [tradingeconomics](https://tradingeconomics.com/united-states/government-debt/news/500793)
- [govinfo](https://www.govinfo.gov/content/pkg/FR-2025-11-12/html/2025-19850.htm)
- [federalregister](https://public-inspection.federalregister.gov/2025-20308.pdf)
- [faa](https://www.faa.gov/newsroom/dot-faa-announce-termination-faa-emergency-order-return-normal-operations)
- [govinfo](https://www.govinfo.gov/content/pkg/FR-2025-11-17/html/2025-19986.htm)
- [Substack](https://crsreports.substack.com/p/paperwork-came-through)
- [everycrsreport](https://www.everycrsreport.com/reports/R49491.html)
- [senate](https://www.moran.senate.gov/public/index.cfm/news-releases?ID=46FDC50A-C743-4B1B-B03E-A14663A1FE7E)
- [govinfo](https://www.govinfo.gov/app/details/CHRG-119shrg62988/CHRG-119shrg62988)
- [senate](https://commerce.senate.gov/2025/11/flying-on-empty-how-shutdowns-threaten-air-safety-travel-and-the-economy)
- [richmondfed](https://www.richmondfed.org/publications/research/economic_brief/2025/eb_25-45)
- [legis1](https://legis1.com/news/tsa-staffing-shortage-government-shutdowns)
- [airlines](https://www.airlines.org/news-update/latest-data-shows-huge-impact-of-the-government-shutdown-on-airlines-and-our-customers/)
- [NBC News](https://www.nbcnews.com/news/us-news/live-blog/flight-cancellations-airlines-government-shutdown-live-updates-rcna242812)
- [airlines](https://www.airlines.org/news-update/new-data-shows-huge-impact-of-the-government-shutdown-on-airlines-and-our-customers/)
- [airlines](https://www.airlines.org/news/flying-on-empty-how-shutdowns-threaten-air-safety-travel-and-the-economy/)
- [aol](https://www.aol.com/articles/airlines-warn-flight-reductions-could-220700214.html)
- [yahoo](https://www.yahoo.com/news/articles/faa-reducing-air-traffic-10-213047412.html)
- [congress](https://www.congress.gov/crs-product/R49491)
- [airlines](https://www.airlines.org/wp-content/uploads/2019/02/A4A-Written-Testimony.pdf)
- [congress](https://www.congress.gov/116/chrg/CHRG-116hhrg35067/CHRG-116hhrg35067.pdf)
- [faa](https://www.faa.gov/NAS_safety_review_team_report.pdf)
- [ourpublicservice](https://ourpublicservice.org/wp-content/uploads/2019/09/Shutdown-Letdown.pdf)
- [kugn](https://www.kugn.com/2025/11/11/duffy-flight-cuts-end-only-when-data-says-they-should/)
- [redstate](https://redstate.com/katie-jerkovich/2025/11/11/democrats-endangering-american-lives-with-schumer-shutdown-faa-data-shows-n2196091)
- [transportation](https://www.transportation.gov/briefing-room/us-transportation-secretary-sean-p-duffy-faa-administrator-bryan-bedford-freeze)
- [faa](https://www.faa.gov/newsroom/statements/general-statements)
- [Wikipedia](https://en.wikipedia.org/wiki/ATC_Zero)
- [CNN](https://www.cnn.com/2025/10/27/us/air-traffic-control-government-shutdown)
- [simpleflying](https://simpleflying.com/another-close-call-southwest-boeing-737-helicopter-cleveland/)
- [avweb](https://avweb.com/flight-safety/accidents-ntsb/ntsb-launches-investigation-into-close-call-involving-southwest-flight/)
- [avherald](https://avherald.com/h?article=52f2ce96)
- [yahoo](https://www.yahoo.com/news/articles/air-traffic-control-struggling-federal-210500833.html)
- [CBS News](https://www.cbsnews.com/live-updates/canceled-flights-government-shutdown-airlines-scramble/)
- [senate](https://www.commerce.senate.gov/services/files/CA99E1E6-8EFC-4EEB-AEB8-DCBEFC1F866C)
- [NPR](https://www.npr.org/2025/11/12/g-s1-97607/house-vote-shutdown-end)
- [CBS News](https://www.cbsnews.com/live-updates/government-shutdown-latest-house-vote-senate-deal-trump/)
- [The Hill](https://thehill.com/homenews/administration/5602790-trump-signs-funding-bill/)
- [federalnewsnetwork](https://federalnewsnetwork.com/federal-newscast/2025/11/776-air-traffic-controllers-and-technicians-to-get-10000-shutdown-bonuses/)
- [natca](https://natca.org/2025/10/24/americas-air-traffic-controllers-to-receive-first-0-paycheck-on-oct-28-2/)
- [CNBC](https://www.cnbc.com/2025/10/14/government-shutdown-air-traffic-controllers.html)
- [Forbes](https://www.forbes.com/sites/suzannerowankelleher/2025/10/07/unpaid-air-traffic-controllers-end-shutdown/)
- [Forbes](https://www.forbes.com/sites/suzannerowankelleher/2025/10/28/tuesday-air-traffic-staffing-issues-flight-delays/)
- [skift](https://skift.com/2025/10/28/air-traffic-controllers-miss-first-paychecks-during-government-shutdown/)
- [yahoo](https://www.yahoo.com/news/articles/transportation-secretary-says-air-traffic-065350613.html)
- [wsws](https://www.wsws.org/en/articles/2025/11/04/sxvo-n04.html)
- [house](https://carson.house.gov/media/press-releases/ranking-member-larsen-and-rep-carson-statements-air-traffic-controllers)
- [CNBC](https://www.cnbc.com/2025/11/21/air-traffic-controllers-government-shutdown-bonus.html)
- [The Hill](https://thehill.com/policy/transportation/5618009-faa-shutdown-10k-bonus/)
- [boston](https://www.boston.com/travel/flights/2025/11/06/faa-reducing-air-traffic-government-shutdown/)
- [senate](https://www.commerce.senate.gov/services/files/CE71F209-761D-42AC-95FB-67E4A6174F1F)
- [aol](https://www.aol.com/articles/domestic-flights-still-curtailed-faa-115759396.html)
- [faa](https://www.faa.gov/newsroom/dot-faa-announce-reduction-required-flight-cuts-3-percent)
- [hstoday](https://www.hstoday.us/subject-matter-areas/transportation/dot-faa-announce-termination-of-faa-emergency-order-and-return-to-normal-operations/)
- [wtap](https://www.wtap.com/2025/11/09/us-airlines-daily-cancellations-top-2000-first-time-since-shutdown-cuts-began/)
- [simpleflying](https://simpleflying.com/back-to-normal-faa-ends-flight-reductions-as-atc-numbers-stabilize/)
- [yahoo](https://ca.news.yahoo.com/faa-lowers-required-flight-cuts-013016033.html)
- [faa](https://www.fly.faa.gov/adv/adv_spt)
- [github](https://github.com/cyanheads/faa-traffic-delays-mcp-server/issues/31)
- [faa](https://www.fly.faa.gov/adv/advADB)
- [faa](https://www.fly.faa.gov/adv/adv_list?whichAdvisories=ATCSCC&advisoryCategory=All&date=2025-09-24&airflow=true&_airflow=on&ctop=true&_ctop=on&gStop=true&_gStop=on&gDelay=true&_gDelay=on&route=true&_route=on&other=true&_other=on)
- [github](https://github.com/cyanheads/faa-traffic-delays-mcp-server/issues/8)
- [yahoo](https://www.yahoo.com/news/articles/air-traffic-controllers-wearing-thin-203415812.html)
- [CNN](https://www.cnn.com/2025/11/03/us/worst-weekend-air-traffic-control-staff-hnk)
- [PBS](https://www.pbs.org/newshour/nation/what-to-know-about-the-10-reduction-in-flights-caused-by-the-government-shutdown)
- [PBS](https://www.pbs.org/newshour/nation/faa-plans-to-reduce-air-traffic-by-10-at-dozens-of-busy-airports-during-shutdown)
- [CNN](https://www.cnn.com/politics/live-news/trump-government-shutdown-flight-cancellations-delays-11-07-25)
- [thepointsguy](https://thepointsguy.com/news/government-shutdown-real-disruption-trump-administration/?utm_section=lat)
- [transportation](https://www.transportation.gov/briefing-room/dot-faa-announce-reduction-required-flight-cuts-3-percent)
- [Fortune](https://www.fortune.com/2025/11/01/faa-air-traffic-control-facilities-staffing-shortages-government-shutdown-flight-delays)
- [cbs58](https://www.cbs58.com/news/worst-weekend-for-air-traffic-controller-staffing-since-start-of-shutdown)
- [accuweather](https://www.accuweather.com/en/travel/worst-weekend-for-air-traffic-controller-staffing-since-start-of-shutdown/1832100)
- [researchgate](https://www.researchgate.net/publication/339422287_Go-Around_Detection_Using_Crowd-Sourced_ADS-B_Position_Data)
- [doi](https://doi.org/10.3390/aerospace8100291)
- [mdpi-res](https://mdpi-res.com/d_attachment/aerospace/aerospace-08-00291/article_deploy/aerospace-08-00291-v2.pdf?version=1634285594)
- [researchgate](https://www.researchgate.net/publication/355205681_Classification_and_Analysis_of_Go-Arounds_in_Commercial_Aviation_Using_ADS-B_Data)
- [researchgate](https://www.researchgate.net/publication/347303686_Predicting_Airplane_Go-Arounds_Using_Machine_Learning_and_Open-Source_Data/fulltext/5fecac2392851c13fed7bd5e/Predicting-Airplane-Go-Arounds-Using-Machine-Learning-and-Open-Source-Data.pdf)
- [researchgate](https://www.researchgate.net/publication/366289916_Large_Landing_Trajectory_Dataset_for_Go-Around_Analysis)
- [doi](https://doi.org/10.3390/engproc2022028002)
- [researchgate](https://www.researchgate.net/figure/GA-rates-per-1000-landings-of-the-top-three-operators-at-selected-US-airports_fig3_366289916)
- [researchgate](https://www.researchgate.net/publication/376572930_Analysing_the_Impact_of_Go-Around_Occurrences_at_Large_European_Airports)
- [researchgate](https://www.researchgate.net/publication/335570864_OpenSky_Report_2019_Analysing_TCAS_in_the_Real_World_using_Big_Data)
- [semanticscholar](https://www.semanticscholar.org/paper/OpenSky-Report-2019:-Analysing-TCAS-in-the-Real-Big-Sch%C3%A4fer-Olive/30d0d4954a5ef56158f0369c4f01d9e522e7edd7/figure/4)
- [admin](https://www.ncsc.admin.ch/dam/ncsc/de/dokumente/dokumentation/lageberichte/2019-2_Technischen_Beilage_I.pdf.download.pdf/Technische%20Beilage%20I.pdf)
- [staradvertiser](https://www.staradvertiser.com/2025/11/02/breaking-news/u-s-probes-near-miss-between-southwest-airlines-jet-and-helicopter/)
- [faa](https://www.faa.gov/newsroom/faa-statements-midair-collision-reagan-washington-national-airport)
- [yahoo](https://www.yahoo.com/news/articles/faa-bonuses-air-traffic-controllers-233603500.html)
