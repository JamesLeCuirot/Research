# Sources and verification log: paper 08

Checks made on 11 and 12 November 2026. "Fetched" means the page was retrieved and read through a summarising fetch tool, which returns extracts and not the full text; quotations in the paper are the extracts returned.

| Key | How verified | Claims it supports |
|---|---|---|
| `faa2025order1` | Fetched from govinfo.gov (FR Doc. 2025-19850, 90 FR 50884–50886). | Issued and effective 7 Nov 2025; 40 High Impact Airports; 4% from 7 Nov with steps to 10%; services to VFR aircraft may be withheld; quotations "working without pay since October 3, 2025", "assessed voluntary safety reports submitted for the month of October", "evidence of increased stress on the NAS in aviation safety data". |
| `faa2025order2` | Fetched from govinfo.gov (FR Doc. 2025-19986, 90 FR 51426–51429). | Effective 6:00 a.m. 13 Nov 2025; 6% reduction; general aviation prohibition at the 12 Appendix B airports. |
| `faa2025cancel` | Fetched from govinfo.gov PDF (FR Doc. 2025-20308, 90 FR 52132–52133). | Cancellation effective 6:00 a.m. EST 17 Nov 2025; quotation "indicated a correlation between ATO staffing and stress on the NAS". |
| `crs2026` | Fetched from the everycrsreport.com copy (R49491, 22 Oct 2026). | No safety-event data and no empirical safety study cited; delay and cancellation counts only. The copy shows no author names; an earlier research scan gave Bart Elias and Rachel Y. Tang, not re-verified, so the entry uses the corporate author. |
| `wong2025` | Fetched from richmondfed.org. | Difference-in-differences on delays at 82 airports; six airports with significant effects; no safety outcome. The six airport names come from an earlier research scan of the same brief; the fetch on 12 Nov confirmed Boston, the three New York airports, San Francisco and Washington National by their cost figures. |
| `cruz2025` | Fetched from knowledge.uchicago.edu record 16607. | Student report on cancellations at Orlando; no safety outcome. |
| `proud2020` | Fetched from mdpi.com. | 392 go-arounds in 153,765 landing attempts at Mumbai (about 2.5 per 1,000; the rate is this paper's arithmetic). |
| `kumar2021` | Fetched from mdpi.com. | Quotation "one to three per 1000 commercial flight approaches" (the article attributes it to its reference 2). |
| `figuet2023` | Fetched from journals.open.tudelft.nl. | 1.5 to 6 go-arounds per 1,000 landings across 20 European airports. Page numbers not obtained. |
| `monstein2022` | Fetched from mdpi.com. | Go-around detection from crowd-sourced data is biased towards misses ("the GA rate is generally underestimated"). |
| `schafer2019` | Fetched from the authors' copy at cs.ox.ac.uk; venue from the IEEE Xplore listing title. | TCAS resolution advisories have been studied in crowd-sourced data. |
| `adsblol` | README fetched from raw.githubusercontent.com. | Daily archive of traces; Open Database License. |
| `iem` | Not reachable from the analysis workspace; data downloaded by the author on 11 Nov 2026 from the request URL. | Source of hourly METAR. |
| `ourairports` | airports.csv and runways.csv downloaded from the project's GitHub mirror. | Runway thresholds and airport elevations. |
| `sfo2025bridge` | Fetched. Trade-press page with no publication date. | A revised "Special FMS Bridge Visual 28R" used by United Airlines from November 2024, reported to have reduced TCAS RA events. No numbers given. |
| `faa2025vny` | Fetched from faa.gov. Undated. | FAA planned to lower the Van Nuys traffic pattern by 100 ft then 200 ft, in two 90-day steps, starting summer 2025, to reduce TCAS alerts for Burbank arrivals. Actual start dates not verified. |
| `cp2025pearson` | Fetched from cbc.ca. | Nav Canada attributed delays at Toronto Pearson on 1 Nov 2025 to "resource constraints". |
| `ain2025bos` | Fetched. | A Boston Logan runway closed for a 75-day safety project from about 2 Sep 2025. The extract does not name the runway; the identification with runway 27 rests on this study's data (7,942 approaches in 2024, 436 in 2025). |
| `faa2025ewr` | Fetched from faa.gov. | FAA order limiting hourly operations at Newark, extended on 25 Sep 2025; weekend closures of runway 4L-22R from September 2025. |

Statements in the paper with no cited source: the dates of Hurricanes Helene and Milton, the January 2025 collision at Washington and the UPS accident at Louisville on 4 November 2025 are given from general knowledge and an earlier research scan and were not re-verified.

Novelty searches: an extended research scan on 11 Nov 2026 and keyword web searches on 12 Nov 2026 ("shutdown" with "go-around", "TCAS", "ADS-B", "loss of separation", "difference-in-differences"). No flight-data safety study of the shutdown was found. Google Scholar, SSRN, TRB and AIAA were reached only through general web search.

Every number in the paper comes from `results/results.json`, `results/supplementary.json`, `results/post_review.json` or `results/post_review_ops.json`, except the position-density ratio (from the extraction logs, not in the repository) and figures attributed in the text to the reviewers.
