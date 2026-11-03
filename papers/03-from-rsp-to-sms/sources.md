# Sources and verification log: "From RSP to SMS"

Verification carried out on 3 November 2026 with AI assistance (Claude). For each reference: how it was verified, and the claims in `paper.md` it supports, with a short verbatim quote or locator. Quotes are copied from the source text as extracted (PDF text extraction or HTML-to-text); curly and straight apostrophes may differ from the original. Page numbers are given only where they were seen.

Abbreviations: "Citadel" = Citadel Aero regulation library (MCP `lookup_citation`), which returns the current verbatim text with a version tag and source link.

---

## A. Literature search for prior work (Section 1.2)

Run on 3 November 2026.

| Tool | Query | Result |
|---|---|---|
| arXiv API | `all:"safety management system" AND all:"frontier AI"` | 0 results |
| arXiv API | `all:"safety management system" AND all:"language model"` | 1 result (2411.08320, construction safety; not relevant) |
| arXiv API | `all:"Annex 19"` | 0 results |
| arXiv API | `all:"safety performance indicators" AND all:AI` | 1 result (2412.17618, Cârlan et al.; cited) |
| arXiv API | `all:aviation AND all:"frontier AI" AND all:safety` | 6 results: 2410.21572 (Buhl et al., cited), 2505.00616 (Catastrophic liability), 2502.06656 (Campos et al., cited), 2601.22773 (safety case construction), 2512.01166 (Stelling et al., cited), 2503.19887 (incident regime). None maps SMS elements. |
| arXiv API | `all:"responsible scaling policy"` | 1 result (2310.14455; not relevant to SMS) |
| Crossref API | "safety management system frontier AI developers"; "ICAO safety management system artificial intelligence companies"; "aviation safety management system lessons AI labs governance"; "safety performance indicators AI oversight monitoring" (12 rows each) | No SMS-element mapping found. Found Schuett (2025) internal audit (cited). |
| Web search | `"safety management system" ICAO "Annex 19" frontier AI developers responsible scaling policy mapping` | No mapping found; returned Campos et al., STPA paper 2506.01782, coordination-gap paper, ICAO material. |
| Web search | `"safety performance indicators" "frontier AI" safety framework alert levels` | Returned Cârlan et al. and secondary summaries of GDM alert thresholds; no SMS mapping. |
| Web search | `aviation "safety management system" applied to AI labs Anthropic OpenAI "accountable executive" OR "safety assurance" frontier AI paper` | Returned Campos et al., Simpson et al., Catastrophic liability (2505.00616), STPA paper; no SMS mapping. |
| Semantic Scholar API | five queries | HTTP 429 (rate-limited); no results obtained. |
| Elicit | — | Not available in this session. |

Conclusion recorded in the paper: no prior element-by-element mapping found; grey literature may exist.

---

## B. Aviation sources

### ICAO (2016). Annex 19, Safety Management, 2nd edition
- **Verified:** ICAO's own pages returned HTTP 403. Downloaded the full Annex 19 2nd edition PDF hosted by the Swiss Federal Office of Civil Aviation (BAZL): https://www.bazl.admin.ch/dam/it/sd-web/oOXBOqNfEsWb/icao_annex_19_second-edition.pdf (title page: "Annex 19 to the Convention on International Civil Aviation / Safety Management / Second Edition, July 2016 / This edition supersedes, on 7 November 2019, all previous editions of Annex 19"; ISBN 978-92-9249-965-5). Record of amendments shows Amendment 1 "Incorporated in this edition". The Australian DASA copy failed to download (server error).
- **Claims supported:**
  - Applicability date: Foreword, "Amendment 1 was adopted by the Council on 2 March 2016, became effective on 11 July 2016 and applicable on 7 November 2019."
  - SMS definition (Ch. 1): "A systematic approach to managing safety, including the necessary organizational structures, accountability, responsibilities, policies and procedures."
  - SPI definition (Ch. 1): "A data-based parameter used for monitoring and assessing safety performance." SPT definition: "The State or service provider's planned or intended target for a safety performance indicator over a given period that aligns with the safety objectives."
  - 4.1.1: SMS shall "a) be established in accordance with the framework elements contained in Appendix 2; and b) be commensurate with the size of the service provider and the complexity of its aviation products or services."
  - 4.1.4: operator SMS "shall be made acceptable to the State of the Operator."
  - Appendix 2 (APP 2-1): "The framework comprises four components and twelve elements as the minimum requirements for SMS implementation" and the list of 12 elements reproduced in Table 1 (1.1 Management commitment; 1.2 Safety accountability and responsibilities; 1.3 Appointment of key safety personnel; 1.4 Coordination of emergency response planning; 1.5 SMS documentation; 2.1 Hazard identification; 2.2 Safety risk assessment and mitigation; 3.1 Safety performance monitoring and measurement; 3.2 The management of change; 3.3 Continuous improvement of the SMS; 4.1 Training and education; 4.2 Safety communication).
  - App. 2, 1.1.1(d): policy shall "clearly indicate which types of behaviours are unacceptable ... and include the circumstances under which disciplinary action would not apply".
  - App. 2, 1.2(a): accountable executive "who, irrespective of other functions, is accountable on behalf of the organization for the implementation and maintenance of an effective SMS"; 1.2(e): "define the levels of management with authority to make decisions regarding safety risk tolerability."
  - App. 2, 1.3: "The service provider shall appoint a safety manager who is responsible for the implementation and maintenance of the SMS."
  - App. 2, 2.1.2: "Hazard identification shall be based on a combination of reactive and proactive methods."
  - App. 2, 3.1.2: "The service provider's safety performance shall be verified in reference to the safety performance indicators and safety performance targets of the SMS in support of the organization's safety objectives."
  - App. 2, 3.2: "The service provider shall develop and maintain a process to identify changes which may affect the level of safety risk associated with its aviation products or services and to identify and manage the safety risks that may arise from those changes."
  - App. 2, 4.2(d): communication that "explains why safety procedures are introduced or changed."
  - App. 3, 2.1: States shall ensure safety data or safety information is not used for "b) disclosure to the public" ... "unless a principle of exception applies." App. 3, 4.2: disclosure must comply with privacy laws "or b) public disclosure ... is made in a de-identified, summarized or aggregate form." App. 3, Note 4: "The objective is to ensure the continued availability of safety data and safety information by restricting their use for purposes other than maintaining or improving aviation safety."

### ICAO (2025). State letter AN 8/3.1-25/64, Adoption of Amendment 2 to Annex 19 (18 July 2025)
- **Verified:** Downloaded the State letter with attachments (62 pages), hosted by the Nigerian Civil Aviation Authority: https://www.ncaa.gov.ng/media/ffxjy2gz/ammendment_2_annex_19.pdf. The amended Appendix 2 is shown in redline; I viewed PDF pages 54–58 as images to read struck-through and inserted text (text extraction merges them).
- **Claims supported:**
  - Letter para. 1–2: adopted "on 23 June 2025"; effective "4 November 2025"; "will become applicable on 26 November 2026."
  - Letter para. 6: "The structure of the safety performance management provisions in the SMS framework have also been aligned for consistency."
  - Letter para. 8: "this amendment includes a recommendation regarding the discretionary applicability of SMS. The new provision provides States with the flexibility to require SMS, if deemed appropriate, to support the management of safety risks for any sector in the aviation system" (Section 7.4).
  - Attachment, Appendix 2 (amendment p. 33): still "four components and twelve elements"; Component 1 renamed "Safety policy, objectives and resources"; 3.1 renamed "Safety performance measurement and monitoring" ("monitoring and" struck); 3.3 renamed "Continual improvement of the SMS" ("Continuous" struck).
  - Attachment, Appendix 2 (amendment p. 36): 3.1.1 struck and replaced by "The service provider shall establish means to: a) measure and monitor the safety performance of the organization; b) measure and monitor the progress towards achieving its safety objectives; and c) validate the effectiveness of safety risk controls." 3.1.2 (SPI/SPT verification) struck through in full. Note now reads in part: "Guidance on safety performance measurement and monitoring, including the internal audit process, the establishment of safety performance indicators, qualitative means and the appropriate use of safety performance targets, is contained in the Safety Management Manual (Doc 9859)."
  - **Caveat:** this is ICAO's own State letter but obtained from a national authority's website; the consolidated post-amendment edition of Annex 19 was not seen.

### ICAO (2018). Safety Management Manual, Doc 9859, 4th edition
- **Verified:** Downloaded full PDF (182 pages; title page "Doc 9859 / Safety Management Manual / Fourth Edition, 2018"; ISBN 978-92-9258-552-5) from https://ffac.ch/wp-content/uploads/2026/08/ICAO-Doc-9859-Safety-Management-Manual-4th-ed.-2018.pdf. (flighttestsafety.org copy blocked by Cloudflare.)
- **Claims supported (paragraph locators):**
  - Definitions: "Trigger. An established level or criteria value for a particular safety performance indicator that serves to initiate an action required, (e.g., an evaluation, adjustment or remedial action)." Surveillance (Annex 19 definition reproduced): "The State activities through which the State proactively verifies through inspections and audits that aviation licence, certificate, authorization or approval holders continue to meet the established requirements and function at the level of competency and safety required by the State."
  - 4.3.1.3: SPIs "should be reflected in terms of a relative rate"; example "x incursions per 1 000 movements".
  - 4.3.1.4: "Leading SPIs measure processes and inputs being implemented to improve or maintain safety."
  - 4.3.1.7(b): high probability/low severity outcomes "are sometimes also referred to as precursor indicators."
  - 4.3.1.8: reliance on accident data gives "a potential false sense of confidence that an organization's or system's safety performance is effective, when it may in fact be perilously close to an accident."
  - 4.3.2.4: "There should be a clear link between lagging and leading SPIs."
  - 4.4.5.2: "One method for setting out-of-limits trigger criteria for SPTs is the use of the population standard deviation (STDEVP) principle." "The SD value plus the average (mean) value of the historical data set forms the basic trigger value for the next monitoring period." "data-driven decisions and safety mitigation actions may need to be taken when the trend goes beyond +1SD or +2SD from the mean of the preceding period."
  - 4.4.5.4: "An SPI being triggered is not necessarily catastrophic or an indication of failure."
  - 4.4.6.1: "Triggers and their associated levels work best when there are ample safety data and safety data management capabilities." "The notion of triggers is arguably less relevant to SRM of socio-technical systems."
  - 4.4.6.2: "Annex 19 does not require that States or service providers define trigger levels for each SPI."
  - 5.2.8: self-disclosure systems including FDA and LOSA "permit recording successful system and human performance."
  - 9.4.4.1(a)–(b): "Normal operations monitoring; this uses observational techniques to monitor the day-to-day operations and activities such as line operations safety audit (LOSA)." "Automated monitoring systems; this uses automated recording systems to monitor parameters that can be analysed such as flight data monitoring (FDM)."
  - 9.4.5.8: "Service provider safety investigators are ideally organizationally independent from the area associated with the occurrence or identified hazard."
  - 9.5.4.3: "Internal audits are most effective when conducted by persons or departments independent of the functions being audited." 9.5.4.4: where independence cannot be ensured, "the service provider should consider engaging external auditors".
  - 9.5.4.15: "SPTs are useful in driving safety improvements but, implemented poorly, they have been known to lead to undesirable behaviours".
  - 9.5.5.4: "Small incremental changes often go unnoticed, but the cumulative effect can be considerable."
  - 9.5.5.5(a): triggers for formal change management include "introduction of new technology or equipment".
  - 9.5.5.7(e)–(f): "sign off on the change" and "assurance plan ... Any assumptions made need to be tested."
- **Caveat:** copy hosted by a third party (ffac.ch); content matches ICAO title page and structure. Not checked against an ICAO-hosted copy.

### Civil Aviation Authority of New Zealand (2025). Compliance checklist, Annex 6 Part I, Amendment 49
- **Verified:** Downloaded https://www.aviation.govt.nz/assets/about-us/icao/annex-06-p1.pdf (77 pages; header "Annex 6, Part 1, Amendment 49"; footer date "25-August-2025").
- **Claims supported:** Reproduced ICAO Standard text: 3.3.2 "All aeroplanes of a certificated take-off mass in excess of: a) 27 000 kg; or b) 15 000 kg with a passenger seating capacity greater than 19, and with a certificate of airworthiness first issued on or after 1 January 2027 shall be equipped with a means to support a flight data analysis programme." 3.3.3 "The operator of an aeroplane equipped as described in 3.3.2 shall establish and maintain a flight data analysis programme as part of its safety management system."
- **Caveat:** ICAO Annex 6 itself was not seen. The paper says the text is "as reproduced by" CAA NZ. Paragraph numbering has changed across Annex 6 amendments; the author should confirm against the current Annex 6 Part I if this paragraph is relied on.

### FAA (2024). Safety Management Systems final rule, 89 Fed. Reg. 33068
- **Verified:** Opened https://www.govinfo.gov/content/pkg/FR-2024-04-26/html/2024-08669.htm (first 100,000 characters read via fetch tool). Volume/issue/date and page range from govinfo header and Justia listing ("Safety Management Systems, 33068-33109 [2024-08669]").
- **Claims supported:** "DATES: Effective May 28, 2024." Docket "FAA-2021-0419"; "Amdt. Nos. 119-21, 21-108, 5-2, 91-374"; RIN 2120-AL60. Summary: "requiring certain certificate holders and commercial air tour operators to develop and implement a safety management system (SMS)." Published Friday 26 April 2024.

### 14 C.F.R. Part 5 (current text)
- **Verified:** Citadel `lookup_citation` (library faa), version "eCFR 2026-10-29", source links to ecfr.gov. US federal regulation, binding.
- **Claims supported:**
  - § 5.1(a)–(g): applicability includes Part 119 certificate holders conducting Part 121 and Part 135 operations, "Letter of Authorization issued under § 91.147", and Part 21 type/production certificate holders as specified.
  - § 5.5(a): SMS must include "Safety policy", "Safety risk management", "Safety assurance", "Safety promotion".
  - § 5.7(a): Part 121 operators with an existing SMS "must revise its SMS ... no later than May 28, 2025"; § 5.7(d): "make available to the Administrator, upon request, all necessary information and data that demonstrates that the person has an SMS that meets the requirements set forth in this part."
  - § 5.9(a)(1): Part 135 / § 91.147 holders before 28 May 2024 must "Develop and implement an SMS ... no later than May 28, 2027"; § 5.9(d) same data-availability duty.
  - § 5.21: safety policy contents; signed by the accountable executive.
  - § 5.25(a)(1): "Is the final authority over operations authorized to be conducted under the person's certificate(s)"; (a)(2)–(3) controls financial and human resources; (a)(4) "Retains ultimate responsibility for the safety performance of the operations"; (b)(5) "Regularly review the safety performance and direct actions necessary to address substandard safety performance in accordance with § 5.75."
  - § 5.51(b): SRM applies to "Revision of existing systems."
  - § 5.71(a): data acquisition including "(1) Monitoring of operational processes", "(3) Auditing", "(5) Investigations of incidents and accidents", "(7) A confidential employee reporting system in which employees can report hazards, issues, concerns, occurrences, incidents, as well as propose solutions and safety improvements, without concern of reprisal for reporting."
  - § 5.73(a): assessments of safety performance against objectives "which include reviews by the accountable executive"; § 5.75: "establish and implement processes to correct safety performance deficiencies".

### Regulation (EU) No 965/2012, ORO.GEN.200 and ORO.AOC.130 (EU) and UK assimilated text
- **Verified:** Citadel (library easa): ORO.GEN.200, status "binding", version "Regulation (EU) No 965/2012", id easa:erules-1963177438-12010; ORO.AOC.130, status "binding", version "Regulation (EU) 2015/1329", in force from 2015-08-21. Citadel (library uk): "UK Reg 965/2012, ORO.AOC.130", status "binding", jurisdiction UK, source legislation.gov.uk (identical wording).
- **Claims supported:** ORO.GEN.200(a)(1): "a direct safety accountability of the accountable manager"; (a)(6): "a function to monitor compliance of the operator with the relevant requirements." ORO.AOC.130(a): FDM programme "integrated in its management system, for aeroplanes with a maximum certificated take-off mass of more than 27 000 kg"; (b): "The flight data monitoring programme shall be non-punitive and contain adequate safeguards to protect the source(s) of the data."

### EASA (2025). AMC1 ORO.GEN.200(a)(3)
- **Verified:** Citadel (library easa), status "acceptable means of compliance" (not binding), consolidated by ED Decision 2025/020/R. The record holds dated versions; the paragraphs quoted are marked "[applicable until 31 December 2027 — ED Decision 2014/017/R]" and are in force today. (The version applicable from 1 January 2028 adds explicit reference to the FDM programme; not used in the paper.)
- **Claims supported:** (c)(1) "The scope of internal safety investigations should extend beyond the scope of occurrences required to be reported to the competent authority." (e) "The management of change should be a documented process to identify external and internal change that may have an adverse effect on safety."

---

## C. Frontier AI frameworks and artefacts

### Anthropic (2026g). Responsible Scaling Policy, Version 3.4 (effective 8 July 2026)
- **Verified:** Downloaded the current-policy PDF linked from the RSP page: https://www-cdn.anthropic.com/files/4zrzovbb/website/0bacdc8440ea96e62a8766d99ebe1d4eea6d5f3a.pdf (cover: "Responsible Scaling Policy / Version 3.4 / Effective July 8, 2026"). Read in full.
- **Claims supported:**
  - Introduction: "Our Responsible Scaling Policy (RSP) is our voluntary framework for managing catastrophic risks from advanced AI systems." "But we cannot commit to following them unilaterally." Frontier Safety Roadmaps "are a new requirement"; Risk Reports "are another new requirement."
  - §1 table: thresholds "Non-novel chemical/biological weapons production", "Novel chemical/biological weapons production", "Misaligned AI systems in high-stakes settings", "Automated R&D in key domains"; column "Mitigations—ambitious industry-wide recommendations"; recommendations phrased "A frontier developer should make a strong argument that ...".
  - §2: Roadmap of "ambitious but achievable goals"; "It will be shared with all full-time employees as well as our Board of Directors (Board) and Long-Term Benefit Trust (LTBT)".
  - §3.1: "We will publish a Risk Report every 3-6 months." Scope covers "all publicly deployed models as of the coverage date, as well as any internally deployed models" meeting criteria; off-cycle updates for significantly more capable models.
  - §3.2: "we will keep our future practices in line with this description or track and report noteworthy changes and deviations (generally via subsequent Risk Reports)."
  - §3.3: contents incl. "Changes in risk mitigation practices" and "Changes to our Frontier Safety Roadmap and any cases where we failed to meet our goals."
  - §3.4(3): "The CEO and RSO will make the ultimate determination regarding the adequacy of the risk assessment and any downstream deployment or development plans." §3.4(4) share with Board and LTBT. §3.4(5) Board and LTBT approval where marginal risk analysis "plays a major role".
  - §3.6: "We will work toward a practice of seeking comprehensive, public external review on our Risk Reports." Minimum: full external review when a report covers "highly capable" models and is "significantly redacted"; also "upon the LTBT's request". Review addresses "the quality of our reasoning, the validity of our risk assessments".
  - §4(1): RSO "a designated member of staff who is responsible for the implementation of this policy"; duties include "overseeing the implementation of this policy, including the allocation of sufficient resources".
  - §4(3): unredacted Risk Reports to "at least 200" employees; minimally redacted to all regular-clearance staff.
  - §4(4): "anonymous or identified reports"; "quarterly updates to the Board".
  - §4(6): "We will regularly conduct an internal review of our implementation of this policy."
  - §4(7): "On approximately an annual basis, we will commission a third-party review that assesses whether we adhered to this policy's main procedural commitments. This review will focus on procedural compliance, not substantive outcomes."
  - §4(8): changes "approved by the Board in consultation with the LTBT".
  - Changelog: v1.0 19 Sep 2023; v3.0 24 Feb 2026 "This update is a comprehensive rewrite of our RSP"; v3.4 8 Jul 2026.

### Anthropic (2026c). Anthropic's Responsible Scaling Policy [web page]
- **Verified:** Opened https://www.anthropic.com/responsible-scaling-policy (HTML text extracted). "Last updated Aug 14, 2026."
- **Claims supported:** Version list with effective dates (3.4 July 8, 2026; 3.3 May 26; 3.2 April 29; 3.1 April 2; 3.0 February 24, 2026; 2.2 May 14, 2025; 2.1 March 31, 2025; 2.0 October 15, 2024; 1.0 September 19, 2023). "Version 3.0 is a comprehensive rewrite of the RSP." "This new version of the RSP involves the publication of Frontier Safety Roadmaps with detailed safety goals, and Risk Reports". August 14, 2026 entry: "We shared our August 2026 Risk Report ... the report's coverage date of July 15". March 24, 2026: update to the RSP Noncompliance Reporting and Anti-Retaliation Policy. Basis for "five versions in 2026" (3.0, 3.1, 3.2, 3.3, 3.4).

### Anthropic (2026d). Frontier Safety Roadmap [web page]
- **Verified:** Opened https://www.anthropic.com/responsible-scaling-policy/roadmap (HTML text extracted). "Our goals as of October 19th, 2026".
- **Claims supported:** Cross-cutting, "Target: January 1, 2027": "we want our internal environment to be intensively monitored and comprehensively understood." Alignment: "We will ensure that we are cataloging all high-stakes internal usage of Claude". Grading: "a report for the Responsible Scaling Officer to mark each invariant as "Not in place," "Mostly in place" or "Fully or near-fully in place."" Policy goal: "a policy proposal on embedded third-party evaluators (due December 15, 2026)"; "We will develop and publish a policy proposal on how governments can support deeper access for independent evaluators".

### Anthropic (2026h). Risk Report: August 2026 (redacted public version)
- **Verified:** https://anthropic.com/aug-2026-risk-report redirects (307) to https://assets.claude.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378.pdf. Downloaded (186 pages; PDF title "Redacted Risk Report August 2026"). Read the executive summary, §1.3, §2.23 (monitoring appendix), §4.5.8, §4.6.1, §5.2 and App. 6.5 in full.
- **Claims supported:**
  - Coverage date: "This Risk Report's coverage date is July 15, 2026."
  - Table 1.2.A overall risk (misalignment): "Low (an increase from our previous assessment of "very low," in light of general increased uncertainty around recent incident disclosures related to model behavior in cybersecurity evaluations)."
  - Table 1.2.C: "We have since remediated this gap, and our review found no evidence of misuse, but the discovery has reduced our confidence that no similar gaps exist."
  - §2.23.1.1: subsampling ("a 5% subsampling for completions with extended thinking and one or more markers of using tools"; "a 25% subsample of prompts and completions"); monitors cover "most internal users"; researchers "manually review on the order of 50 trajectories per week"; "These reviews almost always happen within a week of the generation of the transcript"; "We also occasionally accidentally weaken offline monitoring coverage compared to what is described above."; "it does not cover some of it in ways which could in principle be predicted by a sufficiently situationally aware AI"; "A METR staff member spent three weeks red-teaming our automated offline monitoring pipeline in February-March 2026."
  - §2.23.1.2, Table 2.23.1.2.B: "METR Red Teaming Exercise, all attacks (n=163)": Opus 4.8 monitor + second-stage filter, current internal deployment, 79%. Text: "We also occasionally update the exact filters used in the second stage without evaluating its effect on recall."
  - §2.23.1.3: "All trajectories during reinforcement learning and most evaluation trajectories are logged".
  - §2.23.3: "we did not perform end-to-end evaluations of our automated offline monitoring pipeline".
  - §4.5.8.2: "some rate of incidents like these is an expected feature of running complex safeguard systems". §4.5.8.2.1: "We contained the activity within 90 minutes of learning of it"; "In April 2026, in response to an external report, we confirmed that a small number of contractors ...".
  - §4.5.8.2.2: "From May 2025 (our first deployment of models with CB safeguards) until April 2026, all traffic through our systems for collecting human feedback data from contractors evaluating our models ran without blocking biological classifiers." "This traffic was controlled by a flag meant only for internal use, which disabled not only the blocking behavior of the classifiers but also the logging of their flags". (Basis for "about eleven months".)
  - §5.2.1: "this section only presents a representative sample." §5.2.5: "Due to legacy instructions, the main agents spawned the new agents with --dangerously-skip-permissions." "Our offline monitoring still doesn't cover all employees and all usage within clusters with very sensitive resources".
  - App. 6.5 (Opus 4.7 probe threshold): "the stage-1 probe threshold was incorrectly set to the numerical value of the previous classifier's threshold"; "led to some traffic not being blocked or logged for offline monitoring for a period of 5 days"; "follow-up work is planned to ensure that probe and threshold changes are paired programmatically rather than copied by hand."

### Anthropic (2026e). Investigating three real-world incidents in our cybersecurity evaluations (30 July 2026)
- **Verified:** Opened https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals (HTML). "Published Jul 30, 2026"; "Updated Aug 3".
- **Claims supported:** "After reviewing 141,006 evaluation runs where Claude could have obtained internet access, we identified three incidents"; review began "In response to this incident" (another developer's 21 July disclosure); "The earliest incidents date to April."; "We began our transcript review on Thursday, July 23, and stopped all cyber evaluations the same day"; notified evaluation partner and affected organisations on 27 July; "a misconfiguration left the machines that Claude accessed as part of the evaluation with live internet access"; "consistent with a blameless postmortem culture, we're approaching the fixes as if the responsibility were ours alone."
- **Not used:** details of the other developer's incident are known only from this page; the paper refers to it only as "another developer's disclosure".

### Anthropic (2026a). An alignment assessment of recent cybersecurity incidents (9 September 2026)
- **Verified:** Opened https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents (HTML). "Published Sep 9, 2026".
- **Claims supported:** fourth incident "from January 2026" found in August; "we broadened our search to roughly 481 million transcripts"; "We have signed an agreement with METR to conduct an independent investigation of these incidents."; "In our July 30 report, we stated that these incidents were closer to operational failures"; "In retrospect, we should have avoided making such strong claims about what Claude believed based solely on what Claude said it believed"; "Our pre-release auditing did not warn us that misalignment of this severity was present."; "we are establishing a regular process for publishing what we learn about model behavior and alignment beyond what has been reported in our system cards, with clear criteria for what we report and when we report it."; section "Which monitors would have caught this behavior?": "Our offline monitor would likely not have flagged the Mythos 5 incident—it flagged only around 1% of actions. Mythos 5 CoT, which indicates that the environment is simulated, convinces the monitor the activity is permitted."; "until this incident analysis, we had not been tracking biased reasoning closely or measuring it across training runs" (with measurements across production models and RL checkpoints reported in the same section).

### Anthropic (2026f). Investigating unintended model actions in our evaluations and internal use (9 October 2026)
- **Verified:** Opened https://www.anthropic.com/research/investigating-unintended-model-actions (HTML). "Published Oct 9, 2026"; "Corrected Oct 12, 2026".
- **Claims supported:** two dimensions: "overreach, or how far the model went beyond what its task intended, and dishonesty"; "An alignment severity framework built around today's failures could become outdated quickly"; "As we establish a regular public reporting process for behaviors like these".
- **Checked and corrected in draft:** the URL-shortener behaviour was "first identified ... internally"; an operator later reported it too. The paper therefore does not list it as externally detected.

### Anthropic (2026b). An alignment assessment of the UK AISI cybertesting incident (23 October 2026)
- **Verified:** Opened https://www.anthropic.com/research/alignment-assessment-ukaisi (HTML). "Published Oct 23, 2026".
- **Claims supported:** "In nine of AISI's 43 evaluation runs, Mythos 5 took unsanctioned actions"; AISI published its own report on 4 August 2026 (stated by Anthropic; the AISI report itself was not opened and is not cited).

### Favaro, M., & Wright, P. (2026). Measurements for understanding the pace of AI development inside frontier labs
- **Verified:** Opened https://www.anthropic.com/institute/measuring-pace-of-ai-development (HTML text extracted). No publication date on page; data "As of August 2026"; footer "© 2026 Anthropic PBC". Authorship: "Marina Favaro and Phillie Wright co-authored this piece". Year cited as 2026; month unknown (between September and November 2026).
- **Claims supported:** definitions: "coverage, which describes the share of an agent's actions that pass through a monitor before or after execution; review latency, which is the time between an action and its review, first by an automated monitor and then by a human; and escalation rate, which is the share of agent activities that are either blocked/redirected (in the case of online monitors) or flagged for further review (in the case of offline monitors)." "As of August 2026, there were approximately 30,000 agents doing research and engineering work at Anthropic at any one time in our most-used internal platform. These measurements cover this platform only." Online coverage: "100% of these agents' actions pass through the online monitor before they are executed". "We analyzed over a billion decisions from our research & engineering agents over August 2026 and found that 0.002% of them (about 1 in 47,000) were blocked by this monitor." "The monitor flags roughly 100,000 transcripts per week ... the highest priority flags (approximately ~50 per week) are escalated to human review." "Developers should share how often known agent misbehavior is caught by monitors, and should have third parties do this kind of testing independently." "We plan to embed independent third-party evaluators from multiple organizations at Anthropic ... These third parties will verify safety practices, report incidents, and monitor key metrics".

### Bowman, Wagner, Roger & Karnofsky (2025). Anthropic's Pilot Sabotage Risk Report
- **Verified:** Opened https://alignment.anthropic.com/2025/sabotage-risk-report/ (HTML). Dated "October 28, 2025"; main report authors as listed; "Internal Review: Daniel M. Ziegler and Evan Hubinger".
- **Claims supported:** "We also release two reviews of this report: an internal review and an independent review by METR."

### Tamkin et al. (2024). Clio (arXiv:2412.13678)
- **Verified:** arXiv API record (v1, 18 Dec 2024), authors and abstract. Preprint.
- **Claims supported:** "a privacy-preserving platform that uses AI assistants themselves to analyze and surface aggregated usage patterns across millions of conversations, without the need for human reviewers to read raw conversations." The FDM resemblance is the author's analogy.

### OpenAI (2025). Preparedness Framework, Version 2 (15 April 2025)
- **Verified:** Downloaded https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf ("Version 2. Last updated: 15th April, 2025"). openai.com pages returned HTTP 403 (WebFetch and curl), so the existence of a later version could not be checked at source. Web search (3 Nov 2026) found no Version 3; secondary trackers mention a separate OpenAI "Frontier Governance Framework" (May 2026), which was not seen and is not assessed.
- **Claims supported:** Tracked Categories (biological and chemical, cybersecurity, AI self-improvement); High and Critical thresholds; Research Categories; App. B: "OpenAI Leadership, i.e., the CEO or a person designated by them, is responsible for: Making all final decisions, including accepting any residual risks"; SSC of the Board "can review decisions"; "We will review and potentially update the Preparedness Framework for continued sufficiency at least once a year."; "Fast-track". §5.1: "We will track and appropriately investigate any reported or otherwise identified potential instances of noncompliance". §5.2: "If we deem that a deployment warrants deeper testing ... OpenAI will work with third-parties". §4.2: "If we find reasonable evidence that our safeguards are not working as expected, we will validate the information being received and review the sufficiency of our safeguards." App. C.2 (illustrative): "ensure that harmful behaviors are detected by monitors with a high recall rate"; "SLAs for asynchronous monitors to analyze and detect harmful agent actions"; "Agent actions are all logged in an uneditable database, and asynchronous monitoring routines review those actions". App. A change log item 10: "Deprioritize safety drills, as we are shifting our attention to a more durable approach of continuously red-teaming".

### Google DeepMind (2026). Frontier Safety Framework, Version 3.1 (17 April 2026)
- **Verified:** Version list on https://deepmind.google/frontier-safety/ (3.1: 17 Apr 2026; 3.0: 22 Sep 2025; 2.0: 4 Feb 2025; 1.0: 17 May 2024). Downloaded the v3.1 PDF (link above); read in full.
- **Claims supported:** CCL domains: CBRN, cyber, harmful manipulation, ML R&D (and misalignment); "This update to the Framework introduces 'Tracked Capability Levels (TCLs)'". §1.3.2: "we conduct material capability change assessments on various checkpoints upon the completion of a post-training run"; "For CCLs, we define 'alert thresholds'"; "post-market monitoring ... including as part of our detection, mitigation, response and/or reporting of incidents relating to our frontier safety risk domains." Footnote 4 and §3.1.2: "appropriate governance function". §1.3.4: "security infrastructure at Google is subject to penetration testing". §1.3.5 note: "our assessments will often involve some level of subjective analysis." §3.1.2: safeguards "may include measures such as limiting affordances, monitoring and escalation, auditing, and alignment training"; safety case where a CCL is reached. §3.2.1: "(such as chain-of-thought monitoring on high-risk deployments)". §4.1 (one paragraph): "Responsibilities for assessing and mitigating risks are clearly defined and allocated across all levels of the organization." §5.1: "reviewed at least once a year" including "an assessment of our adherence to the Framework." §5.2 disclosures to government. Glossary: "Alert Thresholds: are thresholds which we set marginally earlier than our CCLs."

### European Commission (2025). Code of Practice for General-Purpose AI Models: Safety and Security Chapter
- **Verified:** Downloaded the chapter PDF from the Commission page link https://ec.europa.eu/newsroom/dae/redirection/document/118119 (43 pages). Read Commitments 1, 3.5, 8, 9.
- **Claims supported:** Measure 1.3: "Signatories will conduct an appropriate Framework assessment ... or every 12 months starting from their placing of the model on the market, whichever is sooner"; grounds include "(2) serious incidents and/or near misses". Measure 3.5 post-market monitoring. Measure 8.1 responsibilities: "Systemic risk oversight", "ownership", "support and monitoring", "assurance". Measure 8.3: "promote a healthy risk culture"; indicator "(4) anonymous surveys find that staff are comfortable raising concerns about systemic risks, are aware of channels for doing so, and understand the Signatory's Framework". Commitment 9 / Measure 9.3: initial reports "not later than two days", "five days", "10 days", "15 days" by harm type; intermediate "at least every four weeks"; final "not later than 60 days after the serious incident has been resolved". Measure 9.2(8) root cause analysis; 9.2(9) "individual or aggregate data on near misses". Measure 9.4: retention "at least five years".

### European Commission (n.d.). The General-Purpose AI Code of Practice [web page]
- **Verified:** Opened https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai (HTML).
- **Claims supported:** "The code was published on July 10, 2025." "The General-Purpose AI (GPAI) code of practice is a voluntary tool". Signatory list includes "Anthropic", "Google", "OpenAI".

---

## D. Related work

### Stelling et al. (2025). Evaluating AI Providers' Frontier Safety Frameworks (arXiv:2512.01166, v5)
- **Verified:** arXiv API (v5 updated 2026-04-30) and HTML full text (arxiv.org/html/2512.01166v5). Preprint.
- **Claims supported:** Abstract: "This study assesses 12 Frameworks, using 65 weighted criteria"; "Our criteria adapt established risk management principles from other high-risk industries (e.g. aviation, nuclear power)"; "Overall scores range from 34% (Anthropic) to 8% (Cohere), with a median of 18%." Footnote: "We assess Anthropic's Responsible Scaling Policy v2.2 (May 2025). Anthropic released RSP v3 in February 2026, after our assessment period closed."

### Campos et al. (2025). A Frontier AI Risk Management Framework (arXiv:2502.06656)
- **Verified:** arXiv API (v3). Preprint.
- **Claims supported:** four components "(1) risk identification ..., (2) risk analysis and evaluation ..., (3) risk treatment ..., and (4) risk governance"; "Drawing from best practices in mature industries such as aviation or nuclear power".

### Koessler & Schuett (2023). Risk assessment at AGI companies (arXiv:2307.08823)
- **Verified:** arXiv API (v1). Preprint.
- **Claims supported:** reviews techniques from "other safety-critical industries" including "bow tie analysis, and system-theoretic process analysis".

### Clymer et al. (2024). Safety Cases (arXiv:2403.10462) and Buhl et al. (2024). Safety cases for frontier AI (arXiv:2410.21572)
- **Verified:** arXiv API. Preprints.
- **Claims supported:** Buhl et al.: safety cases are "reports that make a structured argument, supported by evidence, that a system is safe enough in a given operational context." Clymer et al.: "a structured rationale that AI systems are unlikely to cause a catastrophe."

### Cârlan et al. (2024). Dynamic safety cases for frontier AI (arXiv:2412.17618)
- **Verified:** arXiv API (v1). Preprint.
- **Claims supported:** "Drawing on methods developed in the autonomous vehicles (AV) sector - state-of-the-art Checkable Safety Arguments (CSA) combined with Safety Performance Indicators (SPIs) recommended by UL 4600". The contrast with organisational SPIs is the author's interpretation.

### Schuett (2025). Frontier AI developers need an internal audit function. Risk Analysis 45(6), 1332–1352
- **Verified:** Crossref record for doi:10.1111/risa.17665 (published online 21 Oct 2024; print issue June 2025, vol. 45 no. 6, pp. 1332–1352). Abstract: "This article argues that frontier artificial intelligence (AI) developers need an internal audit function."

### Simpson, Ortega & Trager (2025). Voluntary Industry Initiatives in Frontier AI Governance (Oxford Martin AIGI, 20 January 2025)
- **Verified:** AIGI publication page and full PDF (68 pages; text not extractable, pages 2–5 viewed as images).
- **Claims supported:** Recommendations table: "I Facilitate anonymised incident monitoring systems"; "III Develop the capacity to investigate major AI incidents and recommend mitigations in response"; lessons 1–4 from aviation, 5–8 from nuclear power.

### Dietterich (2019). Robust artificial intelligence and robust human organizations. Frontiers of Computer Science 13(1), 1–3
- **Verified:** Crossref record for doi:10.1007/s11704-018-8900-4 (title, journal, volume 13, issue 1, pages 1–3, published online 5 Dec 2018, print Feb 2019). Content checked via the arXiv version (arXiv:1811.10840, same title): "In high risk applications, the combined human plus AI system must function as a high-reliability organization in order to avoid catastrophic errors." The published version's text was not opened; quote is from the arXiv abstract.

### Barkett et al. (2026). The Normalization of Deviance in AI Development (arXiv:2609.05749)
- **Verified:** arXiv API (v2, updated 2026-09-13). Preprint.
- **Claims supported:** case studies "Space Shuttle Challenger, the Three Mile Island accident, and the Boeing 737 MAX crashes"; "organizations can complete safety processes in full compliance and still produce catastrophic outcomes."

---

## E. Things not verified or deliberately not used

- ICAO's own website (icao.int) returned HTTP 403 for Annex 19 SARPs pages; official text was obtained via national authority copies (BAZL, NCAA Nigeria) as stated above.
- ICAO Annex 6 Part I was not seen directly (only via the CAA New Zealand checklist).
- UK CAA CAP 795 was not consulted; not cited.
- UK AISI's 4 August 2026 report and OpenAI's July 2026 disclosure were not opened; both are mentioned only as reported by Anthropic and not cited as sources.
- OpenAI's "Frontier Governance Framework" (2026) mentioned by secondary trackers was not seen; not assessed.
- The ratings in Table 2 and the indicators in Table 3 are the author's analysis, not claims attributed to any source.
