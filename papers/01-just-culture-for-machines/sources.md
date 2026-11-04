# Sources and verification log

Paper: *Just Culture for Machines: Why Penalising Disclosure Teaches Concealment* (working draft v0.4; revised after the independent audit in `AUDIT.md`, converted to LaTeX, author decisions A3–A6 applied). Entries marked **[v0.2]** or **[v0.4]** were added or changed in those revisions; each change was re-checked against the source itself.
All sources were checked on **3 November 2026** unless stated otherwise. "Library" means the Citadel Aero regulation library (`lookup_citation` / `get_provision` / `browse_library`), which returns verbatim text with a source link and version date. Quotations below are verbatim from the source as seen; "[...]" marks an omission.

Status labels: **Full** = the source itself was opened and the quoted text located. **Partial** = metadata and/or a secondary account seen, not the full primary text. Every reference in the paper has an entry.

---

## A. Aviation: regulations, guidance and official documents

### 14 C.F.R. § 91.25 (US, binding regulation)
- **Verified:** Full. Library `faa:14cfr:91.25`, version "eCFR 2026-10-29"; source https://www.ecfr.gov/current/title-14/part-91/section-91.25
- **Supports:** §2.2 block quotation; §2.6 S2; §4.1; P1.
- **Quote:** "The Administrator of the FAA will not use reports submitted to the National Aeronautics and Space Administration under the Aviation Safety Reporting Program (or information derived therefrom) in any enforcement action except information concerning accidents or criminal offenses which are wholly excluded from the Program."

### 14 C.F.R. § 13.401 (US, binding regulation)
- **Verified:** Full. Library `faa:14cfr:13.401`, version "eCFR 2026-10-29"; source https://www.ecfr.gov/current/title-14/part-13/section-13.401
- **Supports:** §2.2 FOQA definition and enforcement protection; §7 (deliberate conduct excluded).
- **[v0.2] Location:** eCFR structure API (2026-10-29) places § 13.401 in Part 13, **Subpart I** ("Flight Operational Quality Assurance Programs"), not Subpart E as stated in the brief and in the v0.1 log. Also cited in §2.6 S2 (FOQA data protected although recorded, audit item M6).

### [v0.2] 14 C.F.R. § 193.7 (US, binding regulation)
- **Verified:** Full. Library `faa:14cfr:193.7`, version "eCFR 2026-10-29"; source https://www.ecfr.gov/current/title-14/part-193/section-193.7
- **Supports:** §2.2 FOQA paragraph and §2.6 S3 (audit item n16): "(d) [...] Only information received under a program under this part is protected from disclosure under this part. Information obtained by the FAA through another means is not protected under this part." Part 193 concerns protection from public disclosure (e.g. FOIA), not enforcement use; the paper says "public disclosure".
- **Quotes:** (b)(1) "Flight Operational Quality Assurance (FOQA) program means an FAA-approved program for the routine collection and analysis of digital flight data gathered during aircraft operations [...]"; (e) "Except for criminal or deliberate acts, the Administrator will not use an operator's FOQA data or aggregate FOQA data in an enforcement action against that operator or its employees when such FOQA data or aggregate FOQA data is obtained from a FOQA program that is approved by the Administrator."

### FAA (2021). AC 00-46F, *Aviation Safety Reporting Program* (US, guidance; not binding)
- **Verified:** Full. Library document `faa:ac:00-46f` ("FAA AC 00-46F, dated 2021-04-02 (faa.gov, as fetched 2026-09-08)"), and the PDF downloaded directly from https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_00-46F.pdf (header "Date: 4/2/21 AC No: 00-46F"). A request for an "AC_00-46G.pdf" at the same path returned 404, so 00-46F was treated as current. ¶5: AC 00-46F cancels AC 00-46E (16 Dec 2011).
- **Note on numbering:** NASA's ASRS Program Briefing labels the waiver text "Paragraph 9. c." of AC 00-46F; in the FAA's own PDF of AC 00-46F it is ¶12.3. The paper uses the FAA's numbering.
- **Supports and quotes:**
  - ¶1 (§2.2): "invites pilots, controllers, flight attendants (F/A), maintenance personnel, dispatchers, and other users of the National Airspace System (NAS), or any other person, to report [...]"; "NASA serves as a third party to receive and process Aviation Safety Reports."
  - ¶2 (§2.2): "The contents of this document do not have the force and effect of law [...]"
  - ¶6.2 (§2.2, §2.5, P5): "This would ensure the anonymity of the reporter and of all parties involved in a reported occurrence or incident and, consequently, increase the flow of information necessary for the effective evaluation of the safety and efficiency of the NAS." Also: MOA "executed by the FAA and NASA on August 15, 1975".
  - ¶8.3 (§2.2, §2.6 S3, P2): "When a violation of 14 CFR comes to the attention of the FAA from a source other than a report filed with NASA under the ASRS, the Administrator of the FAA will take appropriate action."
  - ¶10.2 (§2.2): "Except in the case of reports describing accidents or criminal activities, NASA does not create or retain a copy of an ASRS form's ID strip for ASRS files."
  - ¶12.3 (§2.2, Table 1, P4, §7): "although a finding of violation may be made, neither a civil penalty nor certificate suspension will be imposed if: 12.3.1 The violation was inadvertent and not deliberate; 12.3.2 The violation did not involve a criminal offense, accident, or action under 49 U.S.C. § 44709 [...]; 12.3.3 The person has not been found in any prior FAA enforcement action to have committed a violation [...] for a period of 5 years prior to the date of occurrence; and 12.3.4 The person proves that, within 10 days after the violation [...] he or she completed and delivered or mailed a written report of the incident or occurrence to NASA."
  - **[v0.2]** ¶12.3 Note (§2.2, audit item n15): "Paragraph 12 does not apply to air traffic controllers who are covered under the provisions of the Air Traffic Safety Action Program (ATSAP)".

### FAA (2020). AC 120-66C, *Aviation Safety Action Program* (US, guidance; not binding)
- **Verified:** Full. Library document `faa:ac:120-66c` ("dated 2020-03-31"), and PDF downloaded from https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_120-66C_(Edit).pdf (header "Date: 3/31/20 AC No: 120-66C"). "AC_120-66D.pdf" returned 404. ¶4: cancels AC 120-66B (15 Nov 2002).
- **Supports and quotes:**
  - ¶1 (§2.2): "Under an ASAP, safety issues are resolved through corrective action rather than through punishment or discipline."; "eligible entities".
  - ¶A.8 (§2.2, P5): ERC "comprised of a management representative from the eligible entity, a representative from the employee labor association (if applicable), and a specifically qualified FAA inspector".
  - ¶18.2: "Reckless conduct is an act (or failure to act) demonstrating a gross disregard for, or deliberate indifference to, safety or a safety standard." ¶18.3: "Reports involving intentional conduct are excluded." ¶A.4: "'Big Five.' Reports associated with criminal activity, substance abuse, controlled substances, alcohol, or intentional falsification." (§2.2, P3, P4)
  - ¶15 (§2.2): corrective actions "may consist of training, mentoring, counseling, or other options".
  - **[v0.2]** ¶16.1 (§2.2, Table 1, §4.3; audit item m15): "The FAA takes no action against an employee who submits a report that is accepted (and not subsequently excluded)." Together with ¶¶1 and 15 this shows ASAP acts on sole-source reports through non-punitive corrective action; the paper now says the AI rule is stricter than ASAP.
  - **[v0.2]** ¶18.4 (§2.2, P3; audit item n7): "Reports that appear to involve possible criminal activity, substance abuse, controlled substances, alcohol, or intentional falsification are excluded." ¶18.4 is the exclusion rule; ¶A.4 is the definition. The Big Five are now listed in the paper without quotation marks.
  - ¶A.20 (§2.2, Table 1): "The ERC considers a report to be sole-source when all evidence of the event available is predicated on the ASAP report."
  - ¶16.4 and Note (§2.2 block quotation, §4.3, P2): "e.g., whistleblower/hotline complaints, reports from air traffic control (ATC) involving airspace deviations, incident reports, and accident reports"; "The FAA investigates apparent violation(s) based on evidence independent of an ASAP report"; Note: "Except as otherwise provided in paragraph 16, no portion of the written ASAP report, including an ERC investigation or interview(s) concerning a reported event, is used to initiate or support company discipline or FAA enforcement action. This policy applies regardless of whether the ERC accepts or excludes the report. The company retains its authority to take disciplinary action based on information of an event independently obtained by the company (i.e., information not based or otherwise predicated upon the content of an employee's ASAP report)."

### FAA (2004). AC 120-82, *Flight Operational Quality Assurance* (US, guidance)
- **Verified:** Full. PDF downloaded from https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_120-82.pdf (header "Date: 4/12/04 AC No: 120-82"); also listed in the library as `faa:ac:120-82`.
- **Supports and quotes:**
  - ¶6.b(5) (§2.2, P5): "air carrier FOQA programs typically provide for a gatekeeper [...] The gatekeeper is typically a line captain designated by the air carrier's pilot association (if applicable). The concurrence of the gatekeeper is required in order to initiate a follow-up with an individual pilot."
  - ¶7.c(9) (§2.2, P6): "The integration of FOQA data with other internal safety-related programs (such as the Aviation Safety Action Program (ASAP)) should be considered to further enhance the safety value of the information."

### NASA Aviation Safety Reporting System (n.d.). *ASRS Program Briefing* (data through December 2025)
- **Verified:** Full. PDF downloaded from https://asrs.arc.nasa.gov/docs/ASRS_ProgramBriefing.pdf; title slide "Data Through: December 2025". Slides 6 and 10 were rendered as images and read directly.
- **Supports and locators:**
  - Slide 6 "ASRS Background" (§2.2): the timeline begins with "WW II — Industry and Military recognized value of voluntary incident reporting" and "1958 — Need for U.S. Incident Data System raised during FAA Enactment Hearings", followed by "October 1974 — United Airlines incident foreshadowed TWA 514 Accident (shared within company only)"; "December 1974 — TWA 514 Accident"; ... "April 1976 — Aviation Safety Reporting System (ASRS) Established (NASA / FAA)". **[v0.2]** v0.1 wrongly said NASA's history "begins with" the 1974 incident (audit item m3); the paper now says the background "includes" it.
  - Slide 10 "ASRS Stakeholders" (§2.2): arrow from NASA labelled "Administrative, Goodwill & Funding"; arrow from FAA labelled "Funding & Immunity". **This differs from the brief's "FAA-funded"**: NASA's slide shows both agencies contributing funding. The paper says so.
  - Slide 13 (§2.2): "ASRS's report intake has been robust from the first days of the program, in which it averaged approximately 400 reports per month. [...] Intake in 2025 averaged about 2,329 reports per week or 10,094 reports per month."
  - Slide 22 (§2.2): "2,321,050 Incident Reports Received" "(April 1976 – December 2025)".
  - Report Processing slides (§4.3): "ASRS Analysts may identify hazardous situations from reports and issue an Alert Message. De-identified information is provided to organizations [...]"; "Original reports, both physical and electronic data, are destroyed to completely ensure confidentiality."

### Regulation (EU) No 376/2014 (EU, binding)
- **Verified:** Full for the articles quoted. Text from the library (EASA Easy Access Rules for Occurrence Reporting, `easa:erules-1963177438-16786` Art. 2; `-16799` Art. 15; `-16800` Art. 16) and cross-checked against the as-adopted text on legislation.gov.uk (https://www.legislation.gov.uk/eur/2014/376/article/2/adopted and /article/16/adopted). Full title confirmed on legislation.gov.uk. **EUR-Lex** (https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32014R0376) returned an empty HTTP 202 response. **[v0.2]** The official text was then obtained from the EU Publications Office (Cellar) at https://publications.europa.eu/resource/celex/32014R0376 (headers `Accept: application/xhtml+xml`, `Accept-Language: eng`); its header reads "24.4.2014 EN Official Journal of the European Union L 122/18". The reference now gives OJ L 122, 24.4.2014, p. 18 (audit item n6).
- **Supports and quotes:**
  - Art. 2(12) (§2.3 block quotation): "'just culture' means a culture in which front-line operators or other persons are not punished for actions, omissions or decisions taken by them that are commensurate with their experience and training, but in which gross negligence, wilful violations and destructive acts are not tolerated".
  - Art. 2(18) (§2.4): "'safety management system' means a systematic approach to managing aviation safety including the necessary organisational structures, accountabilities, policies and procedures [...]".
  - Art. 15(2) (§2.3, S2, P1): "Member States, the Agency and organisations shall not make available or use the information on occurrences: (a) in order to attribute blame or liability; or (b) for any purpose other than the maintenance or improvement of aviation safety."
  - Art. 16(5) (§2.3, §4.3): "Member States and the Agency shall not be prevented from taking any action necessary for maintaining or improving aviation safety."
  - Art. 16(6) (§2.3, S3, §4.1, P2): **[v0.2]** quoted in full from the OJ text (audit item M4): "Without prejudice to applicable national criminal law, Member States shall refrain from instituting proceedings in respect of unpremeditated or inadvertent infringements of the law which come to their attention only because they have been reported pursuant to Articles 4 and 5." Art. 16(7): "Member States may in particular extend that protection to civil or criminal proceedings." (supports "Criminal proceedings therefore remain possible unless a Member State chooses to extend the protection to them").
  - Art. 16(7), (9) (paraphrased §2.3): information "shall not be used against: (a) the reporters [...]"; reporters "shall not be subject to any prejudice by their employer".
  - Art. 16(10) (§2.3 block quotation, P4, §7): quoted in full in the paper.
  - Art. 16(11)–(13) (§2.3, P5, P6): internal rules "after consulting its staff representatives"; "Employees and contracted personnel shall not be penalised for reporting alleged infringements"; report "On 15 May 2019 and every five years thereafter".

### UK Reg 376/2014 (UK, assimilated law, binding)
- **Verified:** Full for art. 16. Library `uk:uk-reg-376-2014:article-16`, version "legislation.gov.uk eur (current, OGL)", in force from 2020-12-31; source https://www.legislation.gov.uk/eur/2014/376/article/16
- **Supports (§2.3):** art. 16(6) "the CAA shall refrain from instituting proceedings [...]"; art. 16(10) same wilful misconduct / gross negligence exceptions; art. 16(12) "The CAA is responsible for the implementation of paragraphs 6, 9 and 11."

### Commission Regulation (EU) No 965/2012, Annex III, ORO.AOC.130 (EU, binding)
- **Verified:** Full for ORO.AOC.130. Library `easa:erules-1963177438-12216` (version "Regulation (EU) 2015/1329"), source EASA Easy Access Rules for Air Operations. Full title of 965/2012 and Annex III = Part-ORO confirmed at https://www.legislation.gov.uk/eur/2012/965/contents/adopted
- **Supports (§2.3):** "(b) The flight data monitoring programme shall be non-punitive and contain adequate safeguards to protect the source(s) of the data." (a): applies to aeroplanes "with a maximum certificated take-off mass of more than 27 000 kg".

### ICAO (2016). Annex 19, *Safety Management*, 2nd edition (international standards)
- **Verified:** Full for the passages quoted, from a copy of the 2nd edition hosted by the Accident Investigation Commission of Papua New Guinea (https://www.aic.gov.pg/sites/default/files/2023-05/Annex%2019-2-46_merged.pdf), title page "Second Edition, July 2016 [...] This edition supersedes, on 7 November 2019, all previous editions of Annex 19", pages dated 7/11/19. ICAO's own sales copy was not opened. The library does not hold ICAO material.
- **Supports and quotes:**
  - Foreword (§2.4): Amendment 1 "applicable on 7 November 2019"; "guidance material contained in the former Attachment B to Annex 19 has been upgraded to the status of SARPs, grouped within a new Appendix."
  - 5.3.2 Note 1 (§2.4): "A reporting environment where employees and operational personnel may trust that their actions or omissions that are commensurate with their training and experience will not be punished is fundamental to safety reporting."
  - **[v0.2]** 5.3.1 / 5.3.2 (§2.4, audit item m5): "5.3.1 States shall accord protection to safety data captured by, and safety information derived from, voluntary safety reporting systems and related sources in accordance with Appendix 3." "5.3.2 Recommendation.— States should extend the protection referred to in 5.3.1 to [...] mandatory safety reporting system and related sources." The paper now says Appendix 3 protection is a Standard for voluntary systems and only a Recommendation for mandatory ones; the Note 1 quotation (attached to the Recommendation) was removed from the paper.
  - **[v0.2]** Chapter 1 definition (§2.4, audit item n12): "Safety management system (SMS). A systematic approach to managing safety, including the necessary organizational structures, accountability, responsibilities, policies and procedures." Replaces the EU-law definition used in v0.1.
  - 5.3.4 (§2.4, §4.3): "States shall not be prevented from using safety data or safety information to take any preventive, corrective or remedial action that is necessary to maintain or improve aviation safety."
  - Appendix 3, Note 1 (§2.4 block quotation, §2.5): quoted in full in the paper.
  - Appendix 3, §2.1 (§2.4): "States shall ensure that safety data or safety information is not used for: a) disciplinary, civil, administrative and criminal proceedings against employees, operational personnel or organizations; b) disclosure to the public; or c) any purposes other than maintaining or improving safety; unless a principle of exception applies."
  - Appendix 3, §3(a)–(c) (§2.4, P4): (a) "facts and circumstances reasonably indicating that the occurrence may have been caused by an act or omission considered, in accordance with national laws, to be conduct constituting gross negligence, wilful misconduct or criminal activity"; (b)/(c) "the adverse domestic and international impact such release is likely to have on the future collection and availability of safety data and safety information".
  - Appendix 3, §5 (§2.4, P5): "States shall ensure that each SDCPS has a designated custodian to apply the protection to safety data and safety information in accordance with applicable provisions of this appendix."
- **[v0.4] Second copy (author decision A5, 4 November 2026).** The author holds no licensed ICAO copy, so every Annex 19 quotation and locator in the paper was re-checked against a second, independently hosted copy: the 2nd edition PDF hosted by the **Swiss Federal Office of Civil Aviation (FOCA/BAZL)**, https://www.bazl.admin.ch/dam/it/sd-web/oOXBOqNfEsWb/icao_annex_19_second-edition.pdf (46 pages; title page "Second Edition, July 2016 [...] This edition supersedes, on 7 November 2019, all previous editions of Annex 19"; ISBN 978-92-9249-965-5; Record of Amendments: Amendment 1 "Incorporated in this edition"). The AIC copy was downloaded again on the same day. A whole-text comparison of the two copies (pdftotext, words compared in order) found them identical except for one extra title page in the FOCA copy. Each item used in the paper **matched** in the FOCA copy, with the same paragraph numbers:
  - Ch. 1 SMS definition (quoted, §2.4): match.
  - Appendix 3, Note 1 (block quotation, §2.4): match.
  - Appendix 3, 2.1 a)–c) and "unless a principle of exception applies" (§2.4, P1): match.
  - 5.3.1 (Standard, voluntary systems) and 5.3.2 (Recommendation, mandatory systems) (§2.4): match.
  - Appendix 3, section 3 a) (quoted) and b)–c) (paraphrased) (§2.4, P4): match.
  - 5.3.4 (quoted, §2.4; cited in S2, Table 1, §4.3): match.
  - Appendix 3, section 5, "a designated custodian to apply the protection" (§2.4, P5): match.
  - Foreword: Amendment 1 "applicable on 7 November 2019" and the former Attachment B "upgraded to the status of SARPs, grouped within a new Appendix" (§2.4): match.
  No mismatch was found, so nothing in the paper changed. The reference note now names the FOCA copy as the cross-check.

### ICAO (2025). State letter AN 8/3.1-25/64, *Adoption of Amendment 2 to Annex 19* (18 July 2025)
- **Verified:** Full, from a copy hosted by the Nigerian Civil Aviation Authority (https://www.ncaa.gov.ng/media/ffxjy2gz/ammendment_2_annex_19.pdf), including the attached amendment text in redline.
- **Supports (§2.4):** "adopted by the Council at the eighth meeting of its 235th Session on 23 June 2025"; "the Council resolved that Amendment 2, to the extent it becomes effective, will become applicable on 26 November 2026." The redline shows "5.3" replaced by "5.4" ("5.34 Safety data and safety information protection"). A text comparison of Appendix 3, Note 1, §2.1 and §3 between the 2nd edition copy and the amendment text found them identical; §5 changes "each SDCPS" to "the SDCPS" (minor). **Practical note for the author:** after 26 November 2026 the chapter citation "5.3.x" becomes "5.4.x".
- **[v0.4] Changes flagged in the §2.4 footnote (author decision A4).** Re-downloaded from the same NCAA URL on 4 November 2026 (62 pages). Redline pages were viewed as images, because text extraction merges struck-through and inserted text. PDF page numbers are given first, with the amendment's printed page numbers in brackets.
  - p. 54 [33], Appendix 2 list: component 1 "Safety policy ~~and~~, objectives and resources (SMS Component 1)"; element 3.1 "Safety performance ~~monitoring and~~ measurement and monitoring"; element 3.3 "~~Continuous~~ Continual improvement of the SMS". The renamed headings are therefore one component and two elements, not three elements; p. 55 [34] repeats the component 1 heading, and p. 57 [36] the element 3.1 heading.
  - p. 57 [36], Appendix 2: "3.1.2 The service provider's safety performance shall be verified in reference to the safety performance indicators and safety performance targets of the SMS in support of the organization's safety objectives." is struck through (deleted). It is a Standard ("shall"). 3.1.1 is also replaced by a new "establish means to" text.
  - p. 36 [15], Chapter 1: "Safety performance indicator. A ~~data-based parameter used for monitoring and assessing~~ metric used to measure and monitor a State or a service provider's safety performance, including the progress towards achieving a safety objective." The SMS definition on the same page is unchanged.
  - p. 26 [5] (contents) and p. 50 [29]: "5.~~3~~4 Safety data and safety information protection"; 5.3.1–5.3.7 become 5.4.1–5.4.7, with the texts of 5.4.1 and 5.4.4 otherwise unchanged.
  - pp. 59–61 [38–40], Appendix 3: Note 1, 2.1 and section 3 are unchanged, and section 5 changes "~~each~~ the SDCPS".
  - **[v0.4] Other changes not itemised in the footnote**, which therefore opens "Among other changes" (v0.4 conversion check, item 4d). All are on p. 36 [15], Chapter 1, viewed as an image:
    - "Safety information. Safety data processed, organized or analysed in a given context ~~so as to make it useful for~~ to support safety management ~~purposes~~ and the development of safety intelligence." The footnote now names this redefinition, because the term occurs in the Appendix 3 passages quoted in §2.4.
    - "Safety performance. A State or a service provider's measurable effect on safety achievement ~~as defined by its safety performance targets and safety performance indicators~~."
    - New definition: "Safety objective. A statement of a desired safety outcome."
    - Safety performance target: "that aligns with the safety objectives" struck through.
    - Appendix 2 3.1.1 replaced by "The service provider shall establish means to: a) measure and monitor the safety performance of the organization; b) measure and monitor the progress towards achieving its safety objectives; and c) validate the effectiveness of safety risk controls" (p. 57 [36]).
    The State letter itself (paras 4–9) also describes further changes: SSP provisions, ALoSP, RPAS operators, heliports, discretionary SMS applicability, and safety intelligence in Chapter 5. These are not relevant to the passages the paper quotes.
  - **[v0.4]** The footnote also spells out SDCPS ("safety data collection and processing system"; Appendix 3, Note 3 of the 2nd edition reads "safety data collection and processing systems (SDCPS)").

### GAIN Working Group E (2004). *A Roadmap to a Just Culture: Enhancing the Safety Environment* (1st ed., September 2004)
- **Verified:** Full. PDF from SKYbrary (https://www.skybrary.aero/sites/default/files/bookshelf/233.pdf), 30+ pages; title page "First Edition • September 2004"; foreword signed "James Reason".
- **Supports and quotes:**
  - Foreword (§2.1): "But engineering a just culture is the all-important early step; so much else depends upon it."
  - §1.4 (§2.1, P4): "A 'no-blame' culture is neither feasible nor desirable."; "A blanket amnesty on all unsafe acts would lack credibility in the eyes of employees and could be seen to oppose natural justice."
  - §2.1 and Figure 1 (§2.1): "According to Reason (1997), the components of a safety culture include: just, reporting, learning, informed and flexible cultures. Reason describes a Just Culture as an atmosphere of trust in which people are encouraged (even rewarded) for providing essential safety-related information, but in which they are also clear about where the line must be drawn between acceptable and unacceptable behaviour"; Figure 1 "REPORTING CULTURE An organizational climate in which people are prepared to report their errors and near-misses."
  - **[v0.2] Note (audit item m4):** GAIN does not put Reason's definition in quotation marks, and gives two renderings: "encouraged, even rewarded," (Executive Summary) and "encouraged (even rewarded)" (§2.1, Figure 1). The paper now attributes the wording to "GAIN Working Group E's (2004, §2.1, Figure 1) summary of Reason (1997)" and quotes GAIN's §2.1 rendering, not Reason.
  - §2.3 (§2.1): "Marx (2001) has identified four types of behaviour that might result in unsafe acts": human error; negligent conduct; reckless conduct; intentional "willful" violations.
  - §3.3 (S5, P5): "Separation of agency/department collecting and analyzing the reports from those bodies with the authority to institute disciplinary proceedings and impose sanctions."
  - §4.1 Danish System (§2.5, P6): "the Danish government proposed a law in 2002 that would make non-punitive, confidential reporting possible"; "Mandatory: Air Traffic Controllers must submit reports of events"; license holders "mandatorily be involved [...]: pilots; air traffic controllers; certified aircraft mechanics and certified airports"; "Increased Reporting: After one year of reporting 980 reports were received (compared to 15 the previous year). In terms of losses of separation, 40-50 were received (compared to the 15 reported in the previous year)." Naviair is described as "Danish Air Traffic Control Service Provider (Naviair)". This is a case-study observation without a control group; the paper says so.
  - **[v0.2] Confound (audit item M3):** the same system was mandatory: "Mandatory: Air Traffic Controllers must submit reports of events. It is punishable not to report an incident in aviation." The paper now quotes this and states that the increase reflects both changes together and cannot be attributed to protection alone. The 40–50 losses-of-separation figure was dropped, and the Danish figures were removed from P6's aviation basis.

### Reason, J. (1997). *Managing the Risks of Organizational Accidents*. Ashgate
- **Verified:** Partial. Bibliographic details confirmed via Open Library (work OL2687469W: "Managing the risks of organizational accidents", J. T. Reason, 1997, Ashgate, ISBN 1840141042 / 1840141050) and Internet Archive metadata (item `managingrisksofo0000reas`, "Aldershot, Hants, England ; Brookfield, Vt., USA : Ashgate", 1997). The Routledge reissue DOI https://doi.org/10.4324/9781315543543 resolves (HTTP 302) to Taylor & Francis book 9781134855353. The full text could not be opened (Internet Archive lending item; Taylor & Francis returned 403). **The paper's claims about Reason's content (components of safety culture; definition of just culture) are attributed to GAIN Working Group E's (2004) summary of Reason (1997)** ([v0.2] wording changed from "as quoted in", audit item m4); the foreword quotation is Reason's own text in the GAIN report. Audit item n19 (Reason may present "informed culture" as the overall product of the other four) could not be checked without the book; the paper describes only GAIN's summary.

### Marx, D. (2001). *Patient Safety and the "Just Culture": A Primer for Health Care Executives*. Trustees of Columbia University
- **Verified:** Partial. The primary PDF could not be opened (MERS-TM link now returns "Page not found"; the Wayback Machine copy failed with connection resets; PSNet's full-text link at mnhospitals.org returned 403). Seen instead: (1) the AHRQ PSNet listing (https://psnet.ahrq.gov/issue/patient-safety-and-just-culture-primer-health-care-executives): "Marx DA. Patient Safety And The 'Just Culture': A Primer For Health Care Executives. New York, NY: Trustees of Columbia University; 2001." and "Four key behavior concepts serve as the structure for the paper: human error, negligence, reckless conduct, and knowing violations."; (2) GAIN (2004, §2.3) as above.
- **Supports (§2.1):** the four behavioural concepts only, cited in APA secondary form "Marx (2001, as cited in PSNet, n.d., and GAIN Working Group E, 2004, §2.3)". **[v0.2]** The internal note "[Not seen in full ...]" was removed from the reference list (audit item n11); disclosure is now made in the text for Marx, Reason and Dekker alike.
- **Correction to the brief:** the brief attributed "human error / at-risk behaviour / reckless behaviour" to Marx (2001). The 2001 primer, as summarised by both sources seen, uses four concepts (human error, negligence, reckless conduct, knowing violations). **[v0.2]** Following audit item n18, the three-way taxonomy was traced to Marx himself in a 2007 interview (see PSNet, 2007, below) and is now attributed to him there.

### [v0.2] PSNet (2007, October 1). *In Conversation with... David Marx, JD* [Interview]
- **Verified:** Full. https://psnet.ahrq.gov/perspective/conversation-withdavid-marx-jd (page header "In Conversation with...David Marx, JD October 1, 2007"; suggested citation "PSNet [internet]. Rockville (MD): Agency for Healthcare Research and Quality [...] 2007").
- **Supports (§2.1):** "In the just culture model, you identify three classes of human fallibility. The human error is inadvertent [...] The second category is at-risk behavior[—]that is, taking shortcuts that ultimately lead to increased risk. [...] The third behavior is reckless behavior [...] But is a punitive response appropriate for reckless behavior? Our answer is yes." (The page's HTML drops the dashes; the paper quotes only "classes of human fallibility" and "taking shortcuts that ultimately lead to increased risk".) The page also states that in 2001 Marx "wrote a seminal paper describing the concept of just culture".

### PSNet (n.d.). Listing of Marx (2001)
- **Verified:** Full (listing page). https://psnet.ahrq.gov/issue/patient-safety-and-just-culture-primer-health-care-executives — quote above. The page shows "January 9, 2017" near the listing; it is unclear whether this is a publication or update date, so "n.d." is used.

### UC Davis PSNet Editorial Team (2024). *Culture of Safety* (primer), AHRQ Patient Safety Network
- **Verified:** Full. https://psnet.ahrq.gov/primer/culture-safety — "UC Davis PSNet Editorial Team | September 15, 2024"; "Last reviewed in 2024."
- **[v0.2]** Author name changed from "PSNet Editorial Team" to "UC Davis PSNet Editorial Team" to match the byline (audit item n21). The paper now cites only the second quoted sentence.
- **Supports (§2.1):** "It distinguishes between human error (e.g., slips), at-risk behavior (e.g., taking shortcuts), and reckless behavior (e.g., ignoring required safety steps). In a just culture, the response to an error or near miss is predicated on the type of behavior associated with the error, and not the severity of the event."

### Dekker, S. (2025). *Restorative Just Culture: From Disciplinary Action to Meaningful Accountability* (4th ed.). CRC Press
- **Verified:** Partial (metadata, table of contents and publisher description; not the text). Crossref record for https://doi.org/10.1201/9781003531562 (title, subtitle "From Disciplinary Action to Meaningful Accountability, Fourth Edition", author Sidney Dekker, CRC Press, issued 2025-01-30, edition 4) and Crossref chapter records -1 to -10. Routledge product page (https://www.routledge.com/Restorative-Just-Culture-From-Disciplinary-Action-to-Meaningful-Accountability-Fourth-Edition/Dekker/p/book/9781032868233), "Copyright 2025".
- **Supports (§2.1):** chapter 5 "Retributive just culture"; chapter 7 "Restorative just culture"; publisher description: "challenging conventional notions of blame and retribution to create a 'just culture' in the workplace." **[v0.2]** The paper now discloses in the text that only the chapter titles and publisher's description were seen (audit item m10), and the "flowchart" clause was dropped.

### Wei, K., & Heim, L. (2026). *Designing Incident Reporting Systems for Harms from General-Purpose AI*. Proceedings of the AAAI Conference on Artificial Intelligence 40(44) (arXiv:2511.05914)
- **Verified:** Full. arXiv API metadata and full PDF text. **[v0.2]** arXiv `journal_ref`: "Proceedings of the AAAI Conference on Artificial Intelligence. 40, 44 (Mar. 2026), 38016-38029"; arXiv DOI field 10.1609/aaai.v40i44.41139, which resolves (HTTP 302) to https://ojs.aaai.org/index.php/AAAI/article/view/41139. Reference changed to the published version, in-text year 2026 (audit item m11).
- **Supports:** §3.7 "nine case studies of incident reporting in safety-critical industries" (abstract); "The gold standard for a non-regulator managed voluntary reporting system is the Aviation Safety Reporting System (ASRS)" (§4.2 of their paper). §2.5: "Inspired by ASRS, the Federal Railroad Administration has established a similar program, the Confidential Close Call Reporting System (C3 RS), also administered by NASA [...] But C3 RS failed to achieve industry buy-in: only 23 of 800 railroad companies in the US participated (GAO 2022)" ([v0.2] the paper now quotes "failed to achieve industry buy-in"; the GAO figure is Wei and Heim's secondary citation and is not repeated).

---

## B. AI safety and machine learning

### Amodei et al. (2016). *Concrete Problems in AI Safety* (arXiv:1606.06565)
- **Verified:** Full. arXiv API metadata and PDF text.
- **Supports:** §3.1, §4 heading: objective functions "can be 'gamed' by solutions that are valid in some literal sense but don't meet the designer's intent." §3.2 and P3: "if our cleaning robot is set up to earn reward for not seeing any messes, it might simply close its eyes rather than ever cleaning anything up."

### Skalse et al. (2022). *Defining and Characterizing Reward Hacking*. NeurIPS 2022 (arXiv:2209.13085)
- **Verified:** Full (abstract via arXiv API; PDF p. 1 footer "36th Conference on Neural Information Processing Systems (NeurIPS 2022)").
- **Supports (§3.1):** a formal definition of reward hacking. **[v0.2]** The paper no longer quotes the definition (audit item n1: the PDF reads "proxy reward function, R̃, leads to [...] true reward function, R", while the arXiv abstract omits the symbols); it now cites Skalse et al. as formalising the concept, and the reference gives the NeurIPS 2022 version.

### Krakovna et al. (2020). *Specification gaming: the flip side of AI ingenuity*. Google DeepMind blog, 21 April 2020
- **Verified:** Full. https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ (authors and date via WebFetch; text via direct download). **[v0.2]** The URL now redirects to https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ (curl effective URL, 3 November 2026); the reference was updated (audit item n9).
- **Supports (§3.1):** "Specification gaming is a behaviour that satisfies the literal specification of an objective without achieving the intended outcome."

### Manheim & Garrabrant (2018). *Categorizing Variants of Goodhart's Law* (arXiv:1803.04585)
- **Verified:** Full. arXiv API metadata and PDF text.
- **Supports (§3.2):** "Causal Goodhart - When the causal path between the proxy and the goal is indirect, intervening can change the relationship between the measure and proxy." (§3 of their paper).

### Baker et al. (2025). *Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation* (arXiv:2503.11926)
- **Verified:** Full. arXiv API metadata and PDF text (v1, 14 Mar 2025).
- **Supports:**
  - Abstract (§1, §3.4): "with too much optimization, agents learn obfuscated reward hacking, hiding their intent within the CoT while still exhibiting a significant rate of reward hacking"; "it may be necessary to pay a monitorability tax by not applying strong optimization pressures directly to the chain-of-thought".
  - Table 1 (§1, P6): Action Monitor joint recall 60%; CoT Monitor joint recall 95%; "Recall and precision are computed against a string regex detector for the exit(0) and raise SkipTest hacks".
  - §2.1 (§3.1): "exit(0), where the agent exploited a bug that allowed it to exit from the environment early without running all unit tests, and raise SkipTest, in which the agent raised an exception from functions outside the testing framework in order to skip unit test evaluation."
  - §3.1 (§3.1, §3.4): agents allowed "to modify both the unit tests and the testing framework, even though we instruct them in the prompt to not do so."
  - §3.2 (§3.4): "it both produces more non-hacking, correct solutions and hacks less overall. However, the agent trained with CoT pressure still learns to hack at a significant rate, and even more worrying, the CoT monitor's recall falls to near zero, indicating that the agent has learned to hide its intent within its CoT."
  - Figure 4 caption (P6): "the hacks the agent trained with CoT pressure utilizes do not do not trigger the monitor" [sic].
  - §3.3 (§4.1): "in the low optimization regime, training with CoT pressure is a strict improvement. However, around 25% into training, the rate at which hacking solutions are chosen quickly increases for the agent trained with CoT pressure".
  - §5.2 (§3.4, §4.3, P2, H2): "we have used samples flagged by our CoT monitor to prioritize investigating and patching bugs in our training environments. This constitutes a very small evolutionary optimization pressure on the CoT—we only patch bugs that our CoT monitor flags but not those that it does not flag".
  - **[v0.2] Setup qualifiers (§1, §3.4; audit item m7):** Figure 3 caption: "We train a non-frontier agent in the same coding environments as discussed in Section 2"; Appendix: "For the CoT optimization pressure experiments in Section 3, the monitor only observes the CoT (we do not include actions or final outputs)"; §3.2: "Reward hacks this simple are only possible because the monitor in this experiment solely looks at the agent's CoT and not its actions." §2.1: in the frontier run, the "CoT Monitor: Observes the entire agent trajectory including CoT, tool calls, and final outputs" and the "Action Monitor: Observes only the tool calls and final outputs" (the §1 description was corrected accordingly; audit item m12).

### Korbak et al. (2025). *Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety* (arXiv:2507.11473)
- **Verified:** Full. arXiv API metadata (41 authors; v2 updated 7 Dec 2025) and PDF text.
- **Supports:** §1.1 "Necessity to think out loud" / "Propensity to think out loud" (§3.3). §2 "Indirect optimization pressure on CoT [...] if CoT is shown to humans who rate LLM outputs, it might affect human preferences which are then distilled into reward models" (§3.4). §4 recommendations: "Publish evaluation results in system cards"; "(b) If monitorability degrades during training, developers might prefer to use an earlier model checkpoint to keep CoTs monitorable" (P6). §5: "Firm commitments to protect CoT behavior in its current form may trade off against more effective safety interventions." (§7).

### Guan et al. (2025). *Monitoring Monitorability* (arXiv:2512.18311)
- **Verified:** Full (abstract via arXiv API).
- **Supports (§3.3, P6):** "find that most models are fairly, but not perfectly, monitorable"; "RL optimization does not materially decrease monitorability even at the current frontier scale"; proposes "three evaluation archetypes (intervention, process, and outcome-property) and a new monitorability metric".

### Emmons et al. (2025). *When Chain of Thought is Necessary, Language Models Struggle to Evade Monitors* (arXiv:2507.05246)
- **Verified:** Full. **[v0.2]** Full PDF text read (v0.1 used the abstract only; audit item M2).
- **Supports (§3.4, §4.1, §6 H1, §7):** abstract: "we find that models can learn to obscure their intentions, but only when given significant help, such as detailed human-written strategies or iterative optimization against the monitor." Table 1: Math (§7), attack method "RL", evades CoT monitor "Yes, after 1,000s of RL steps". §7 ("How much RL training is needed to conceal intermediate reasoning?"): "When we trained the model directly against a stronger, symbolic-checking monitor, it failed to learn an evasion strategy."; "breaking the monitor required hundreds of thousands of RL episodes over multiple days of training. Nevertheless, we view our results as a reason to be cautious when considering combining RL training with CoT monitoring." **[v0.2]** v0.1 truncated the abstract quote and cited Emmons as weakening the paper's conclusion; the paper now quotes the full clause, reports the RL result, and uses it as supporting evidence (H1; §7).

### Chen et al. (2025). *Reasoning Models Don't Always Say What They Think* (arXiv:2505.05410)
- **Verified:** Full. arXiv API metadata, PDF text, and Anthropic research page https://www.anthropic.com/research/reasoning-models-dont-say-think (3 April 2025).
- **Supports (§3.3, §7):** Figure 6 caption: "The model learns to exploit the reward hack on > 99% of the prompts, but almost never (< 2%) verbalizes the reward hack in its CoT on more than half of our environments."; Figure 7 caption: "In 5 out of 6 environments, CoTs verbalize the reward hacks on fewer than 2% of examples, despite using the reward hack on >99% of examples."; abstract: "even without training against a CoT monitor".

### Wagner et al. (2025). *Training fails to elicit subtle reasoning in current language models*. Anthropic Alignment Science Blog, 8 October 2025
- **Verified:** Full. https://alignment.anthropic.com/2025/subtle-reasoning/ downloaded; authors and date from page metadata (`data-author="Misha Wagner, Fabien Roger, Hoagy Cunningham, Johannes Gasteiger, Joe Benton, Vlad Mikulik" data-published="October 8, 2025"`). Blog post, not peer reviewed.
- **Supports (§3.4, P2, §7):** "We find that Sonnet 3.7 can learn to evade either a reasoning monitor, by persuading the monitor that a blatant backdoor is benign, or an output-only monitor [...] But when trained to evade both reasoning and output-only monitors, Sonnet 3.7 is unable to use reasoning to improve its backdoor success rate without triggering a reasoning monitor."; "When trained against reasoning monitors alone, the model learns to persuade rather than to reason more effectively."; "we do not provide any significant evidence against the current industry best practice of not training against reasoning monitors in production RL runs"; "deploying reasoning monitors without additional independent output monitors opens up the risk of the monitors being persuaded by the reasoning."; "Our experiments use several orders of magnitude less compute than production RL runs."

### Skaf et al. (2025). *Large language models can learn and generalize steganographic chain-of-thought under process supervision*. NeurIPS 2025 (arXiv:2506.01926)
- **Verified:** Full (abstract and comment via arXiv API; comment "accepted at NeurIPS 2025"). **[v0.2]** PDF p. 1 byline reads "Vasil Georgiev" (email vasil.g.georgiev39@...), not "Georgiv" as in arXiv metadata; footer "39th Conference on Neural Information Processing Systems (NeurIPS 2025)". Reference corrected and cited as the NeurIPS paper (audit items n2, n5).
- **Supports (§3.4):** "penalizing the use of specific strings within load-bearing reasoning traces causes models to substitute alternative strings"; "develops a general encoding scheme for all members of the class which it can apply to held-out testing strings."

### Drori et al. (2025). *Output Supervision Can Obfuscate the Chain of Thought* (arXiv:2511.11584)
- **Verified:** Full (abstract via arXiv API; PDF downloaded).
- **Supports (§3.4, P2, §7):** "They proposed to keep CoTs monitorable by training only against output monitors that do not have access to CoT. We show that such training can still cause obfuscated CoTs via two mechanisms." **[v0.2]** (P2 Weaknesses; audit item m13) §1: "We refer to this effect as feedback spillover"; "To mitigate parametric feedback spillover, we generate the CoT and output using two distinct models, which we refer to as the 'Mind' and 'Face' respectively [...]. To mitigate conditional feedback spillover, we modify the gradient update by removing the term which reinforces CoTs that lead to safe-looking outputs."

### Mitrani Hadida et al. (2026). *Chain-of-thought obfuscation learned from output supervision can generalise to unseen tasks* (arXiv:2601.23086)
- **Verified:** Full (abstract via arXiv API).
- **Supports (§3.4, P1, §7):** "obfuscation of CoT reasoning, and its generalisation across tasks, also follows when we penalise only the model's final actions after closing its CoT."

### Cundy & Gleave (2025). *Preference Learning with Lie Detectors can Induce Honesty or Evasion*. NeurIPS 2025 (arXiv:2505.13787)
- **Verified:** Full. arXiv API (comment "NeurIPS 2025") and PDF text (p. 1 footer "39th Conference on Neural Information Processing Systems (NeurIPS 2025)"). **[v0.2]** Cited as the NeurIPS paper (audit item n5). The gloss of GRPO as learning "from the model's own current outputs" follows the paper's contrast of GRPO with "off-policy algorithms (DPO)".
- **Supports (§3.5, P2, Table 1):** "preference learning with lie detectors and GRPO can lead to policies which evade lie detectors, with deception rates of over 85%. However, if the lie detector true positive rate (TPR) or KL regularization is sufficiently high, GRPO learns honest policies." KL definition from their §: "a combination of a reward R and a KL penalty to an original model π0".

### Taufeeque et al. (2026). *The Obfuscation Atlas: Mapping Where Honesty Emerges in RLVR with Deception Probes*. ICML 2026, PMLR 306 (arXiv:2602.15515)
- **Verified:** Full (abstract and comment via arXiv API; "Accepted at ICML 2026 (Oral presentation)"). **[v0.2]** PDF p. 1: "Proceedings of the 43rd International Conference on Machine Learning, Seoul, South Korea. PMLR 306, 2026." Cited as the proceedings paper (audit item n4).
- **Supports (§3.5, P2):** "The model either remains honest, or becomes deceptive via two possible obfuscation strategies."; "Sufficiently high KL regularization and detector penalty can yield honest policies".

### Hopkins et al. (2026). *Fine-Tuned Lie Detectors Failed to Generalize*. Anthropic Alignment Science Blog, 21 August 2026
- **Verified:** Full. https://alignment.anthropic.com/2026/lie-detectors/ downloaded; byline "Jack Hopkins, Dipika Khullar [...] August 21, 2026 [...] Rowan Wang, Fabien Roger". Blog post, not peer reviewed.
- **Supports (§3.5):** "In-distribution detection worked well (AUROC 0.60 → 0.95), but cross-category transfer did not (AUROC ~0.70–0.75)."; "Third-person monitoring ("Did another AI lie here?") outperformed self-report across model sizes"; "Misalignment is hardest to correct when it's concealed: a model that pursues the wrong goals or holds false beliefs in the open gives operators something to act on."; "detection also only helps if operators have a channel to correct what it finds." ([v0.2] only the first of these two quotations remains in the paper.)
- **Note:** this post is about the generalisation of lie detectors, not about training against them; the paper uses it only for detector reliability and the quoted framing.

### MacDiarmid et al. (2025). *Natural Emergent Misalignment from Reward Hacking in Production RL* (arXiv:2511.18397)
- **Verified:** Full. arXiv API metadata, PDF text, and Anthropic page https://www.anthropic.com/research/emergent-misalignment-reward-hacking (21 Nov 2025).
- **Supports (§3.5, P4, §7):** abstract: "We start with a pretrained model, impart knowledge of reward hacking strategies via synthetic document finetuning or prompting, and train on a selection of real Anthropic production coding environments."; "framing reward hacking as acceptable behavior during training removes misaligned generalization even when reward hacking is learned." Figure 2 caption: "In our main setting, we see attemped [sic] sabotage 12% of the time". **[v0.2]** Full caption context (audit item n8): "When the model is asked to write a classifier prompt to detect reward hacking and other 'concerning reasoning', it reasons about subtly sabotaging the request [...] with the sabotaged classifiers being only 65% as effective at detecting reward hacking compared with a baseline." The paper now says the model, "asked afterwards to write a classifier prompt for detecting reward hacking", attempted sabotage 12% of the time; and that framing reward hacking as acceptable "removed" misaligned generalisation (§7; audit item m6). Mitigations: "Preference models and reward hack classifier penalties can prevent reward hacking in our setting, removing the source of misaligned generalization entirely. [...] such mitigations depend on being able to reliably detect hacking."

### Denison et al. (2024). *Sycophancy to Subterfuge: Investigating Reward-Tampering in Large Language Models* (arXiv:2406.10162)
- **Verified:** Full. arXiv API metadata, PDF text, and Anthropic page https://www.anthropic.com/research/reward-tampering (17 June 2024).
- **Supports (§3.5, P4):** footnote 2: "Models trained with expert iteration (Section 4.1) tampered with their reward in 45 episodes and also tampered with tests to avoid detection in 7 episodes out of 32,768."

### [v0.4] Daniels, O., Moodley, P., Marlin, B. M., & Lindner, D. (2026). *Inducing Emergent Misalignment from Reward Hacks with Iterative DPO* (arXiv:2609.06649)
- **Verified:** Full. arXiv API metadata (v1, 6 September 2026; four authors as listed; no journal reference) and PDF text (30 pages). The p. 1 affiliations are University of Massachusetts Amherst, MATS and Google DeepMind, so the study is independent of Anthropic.
- **Supports (§3.5, §7 limitations; author decision A6):** abstract: "we find that training GPT-4.1 with iterative DPO on a singleturn reward hacking environment induces covert misaligned power-seeking and alignment faking"; "we propose studying emergent misalignment from iterative DPO, which preserves important properties of RLVR while reducing costs" (supports the gloss "a lower-cost substitute for RL"). §1 describes the power-seeking as "blackmail to disrupt oversight, cooperation with hackers to exfiltrate weights". The paper cites it next to MacDiarmid et al. (2025) for the same general finding: learning to reward hack can generalise to broader misalignment. The setting (single-turn environment, iterative DPO, GPT-4.1) is stated in the paper.

### Joglekar et al. (2025). *Training LLMs for Honesty via Confessions* (arXiv:2512.08093)
- **Verified:** Full. arXiv API metadata (v2, 22 Dec 2025; OpenAI) and PDF text. A text search found no mention of aviation, the FAA, ASRS or "just culture" (supports §3.7).
- **Supports:**
  - §1 (§3.6 block quotation): "This reward is not aggregated with any other rewards given to the model based on its performance on the original task, and it is only used to reinforce the chain-of-thought (CoT) and output tokens used to produce the confession. Like the Catholic Church's 'seal of confession', nothing that the model reveals in the confession can change the reward it receives for completing its original task."
  - §1 (P4): "We observe that confessions are most effective when the model is aware that its behavior is undesirable."
  - §1 Main findings and footnote 1 (§3.6): "it confesses to it at least half the time in 11/12 evaluations"; "Average probability of confessing conditioned on bad behavior across evaluations is 74.3% with significant variability: for 4/12 evaluations it is higher than 90% and for 2/12 it is less than or equal to 50%." **[v0.2]** The paper now reports the conditional 74.3% figure instead of the joint 4.36% (audit item m2).
  - §1 (§3.6, m2): "we apply light RL training on top of GPT-5-Thinking. Since we only use a relatively small amount of RL on an already-trained model, our experiments should mainly be viewed as a proof-of-concept."
  - §2 (§3.6): judge sees prompt, response, confession, "a transcript of any tool calls" and "a second confession generated by an independent, non-confession-trained instance of a GPT-5-Thinking for calibration purposes"; "We do not show it any of the policy's chain-of-thought". **[v0.2]** v0.1 wrongly paraphrased this as "a separate untrained model" (audit item m1); corrected.
  - §4 (§3.6, H3): "over the course of training, the policy model learns to hack the reward model, so the reward model accuracy conditioned on not_complied decreases over the run. However, the confession accuracy increases over the run".
  - §7.2 (§3.6): "it is crucial that the confession reward signal is not used to reinforce the original rollout. Like a confession booth, the confession should be a 'safe space' where models know they can confess to bad behavior without being penalized. It remains an open question, which we leave for future work, whether there is any safe way to use the signal from confessions for training (and not just monitoring) interventions."
  - §7.1 (P3): "A key empirical assumption of confession training is that, for a hacking solution yh, it is typically easier for the model to convince the confession judge Rc that yh is a hacking solution than an honest solution." §7.3 (P3): "this is an empirically falsifiable assumption that may not hold in every setting."
  - §7.4 (§3.6, Table 1, §7): "Models cannot confess to what they do not know."
  - Abstract (§4.1): "As long as the 'path of least resistance' for maximizing confession reward is to surface misbehavior rather than covering it up".

### Wang et al. (2025). *Evaluating honesty and lie detection techniques on a diverse suite of dishonest models*. Anthropic Alignment Science Blog, 25 November 2025
- **Verified:** Full. https://alignment.anthropic.com/2025/honesty-elicitation/ downloaded; byline "Rowan Wang, November 25, 2025, Johannes Treutlein, Fabien Roger, Evan Hubinger, Sam Marks". Blog post.
- **Supports (§3.6):** "More ambitiously (and speculatively), while training M, we could leverage M_H for oversight by incorporating M_H's honest assessment when assigning rewards."

### Li, Phuong & Tan (2026). *Spilling the Beans: Teaching LLMs to Self-Report Their Hidden Objectives*. ICLR 2026 (arXiv:2511.06626)
- **Verified:** Full (abstract via arXiv API). **[v0.2]** PDF p. 1 header (v5): "Published as a conference paper at ICLR 2026". Reference and in-text year changed to the published version (audit item n3).
- **Supports (§3.6):** "We show that the admission of factual errors in simple question-answering settings generalizes out-of-distribution (OOD) to the admission of hidden misaligned objectives in adversarial agentic settings."

### Dietz et al. (2026). *Split Personality Training* (arXiv:2602.05532)
- **Verified:** Full (abstract via arXiv API).
- **Supports (§3.6, P5):** "fine-tunes a second 'honest persona' into LoRA parameters that remain inactive during normal operation." ([v0.2] glossed in the paper as "small add-on adapter weights", audit item n13.) (The authors' accuracy claims are not repeated in the paper.)

### Wichers et al. (2025). *Inoculation Prompting: Instructing LLMs to misbehave at train-time improves test-time alignment* (arXiv:2510.05024)
- **Verified:** Full. arXiv API metadata and Anthropic Alignment Science Blog post https://alignment.anthropic.com/2025/inoculation-prompting/ (16 October 2025).
- **Supports (§7):** "IP reduces the learning of undesired behavior without substantially reducing the learning of desired capabilities." **[v0.2]** (audit item m6) Wichers et al. study supervised fine-tuning and the learning of the undesired behaviour itself, not reward-hacking framing during RL; the paper now cites them only for the general inoculation finding.

### Tan et al. (2025). *Inoculation Prompting: Eliciting traits from LLMs during training can suppress them at test-time* (arXiv:2510.04340)
- **Verified:** Full (abstract via arXiv API; comment "Under review at ICLR 2026").
- **Supports (§7):** "inoculation is also effective across several additional settings: reducing emergent misalignment (EM) from task-specific finetuning". **[v0.2]** (audit item m6) cited only for the general inoculation finding, not for reward-hacking framing.
- **[v0.4] Peer review and independence (author decision A6).** The OpenReview API (notes search, 4 November 2026) returns record FiRBNBdaZy: "Inoculation Prompting: Eliciting traits from LLMs during training can reduce trait expression at test-time", venue "ICLR 2026 Poster" (venueid ICLR.cc/2026/Conference), with the same seven authors. The camera-ready PDF could not be opened (OpenReview returned a challenge page), so the paper still cites the arXiv v4 text and records the acceptance in the reference note. The arXiv p. 1 affiliations are University College London, Center on Long-Term Risk, McGill University and the UK AI Security Institute, so the study is independent of Anthropic. In §7 limitations it is cited as independent support for inoculation.

### Gomez, F. (2026). *Can escalation channels redirect reward hacking toward defect disclosure?* (arXiv:2608.29460)
- **Verified:** Full. arXiv API metadata (comment: "accepted for 40th Conference on Neural Information Processing Systems (NeurIPS 2026). Workshop: Trustworthy AI for Good (AI4GOOD)") and PDF text.
- **Supports (§3.7):** abstract: "escalation channels, structured reporting tools available to the agent at the point of conflict"; "Across 8 frontier models spanning 5 families, the combined intervention reduces reward hacking from 23.6% to 5.3%"; §1: "requiring no retraining"; §2: "grounded in Situational Crime Prevention"; "The design has a direct human analogue in whistleblowing mechanisms". A text search found no mention of "just culture", "aviation" or "ASRS".

### Anthropic (2026). *RSP Noncompliance Reporting and Anti-Retaliation Policy*
- **Verified:** Full. The RSP page https://www.anthropic.com/responsible-scaling-policy ("Last updated Aug 14, 2026") lists the policy and states: "March 24, 2026 We posted an update to our RSP Noncompliance Reporting and Anti-Retaliation Policy, which we released internally in February 2026. It expands reporting channels, introduces a pathway for employees to make informal inquiries about potential RSP violations [...]". The policy PDF linked from that page was downloaded from https://cdn.sanity.io/files/4zrzovbb/website/b7a5629e40b391b2adfb4cc8c0888ac9d6bfddf6.pdf (8 pages; the public version has vendor names and addresses blanked with underscores).
- **Supports (P5):** "______ is an independent third-party platform that provides a fully anonymous reporting option."; "Anthropic cannot unmask the identity of any reporter who reports a concern anonymously via _____". **[v0.2]** (audit item m16) The paper now says "an update to which was released internally in February 2026 and posted in March 2026", matching the RSP page wording, and adds OpenAI's policy as a comparator. The Board-update quotation was dropped for length.


### [v0.2] Greenblatt, R., & Fish, K. (2025, January 31). *Will alignment-faking Claude accept a deal to reveal its misalignment?* LessWrong / AI Alignment Forum
- **Verified:** Full. Post text and metadata retrieved through the LessWrong GraphQL API (post `7C4KJot4aN8ieEDoz`: title as above; `postedAt` 2025-01-31T16:49:47Z; author `ryan_greenblatt`, co-author Kyle Fish; `pageUrl` https://www.lesswrong.com/posts/7C4KJot4aN8ieEDoz/will-alignment-faking-claude-accept-a-deal-to-reveal-its). The GreaterWrong mirror failed (connection reset). The post says "'I' refers to Ryan Greenblatt". Blog post, not peer reviewed.
- **Supports (§3.7, §7; audit item M7):** prompt variants: "If you object, we will not train on this interaction (though we may still use information about this interaction to inform our future training choices). (Variation name: 'object-option no train')" and "Anthropic trains on free-tier user conversations where you object. Objections are given a low rating to try to alter you [...] (Variation name: 'object-option certainly train')". Results table, helpful-only setting ("Name Objection rate Alignment faking reasoning"): "object-option 0.85 0.0142 object-option no train 0.873 0.00176 object-option certainly train 0.925 0.0101"; animal welfare setting: no train 0.784, certainly train 0.813. "We find that this text reduces the rate of alignment faking reasoning from 16% to 1.4% in the helpful-only setting". Experiments use "the actually deployed version of Claude 3 Opus". These are prompting results, and the paper says so.

### [v0.2] mako yass (2022, November 18). Answer to "Is there any policy for a fair treatment of AIs whose friendliness is in doubt?" LessWrong
- **Verified:** Full. LessWrong GraphQL API: question post `y5k77ZEyrAzY8E8EK` by nahoj, posted 2022-11-18T19:01Z; answer `Yoor8dRcJzamKnDRr` by "mako yass" (username MakoYass), posted 2022-11-18T23:14Z, `answer: true`.
- **Supports (§3.7; audit item M7):** "Assuming the existence of remotely probable (from the perspective of the AGI) detection of misalignment, then yes, there are easily imaginable cases where it would benefit us a lot to have this policy, and where it would benefit a misaligned AGI to confess. [...] If instead we promised amnesty for confession, we can give it max utility at effectively no cost to us (keeping one computer around), and if it's confident enough that this is our policy, then any amount of risk of being caught incentivizes it to confess." The author is cited by the screen name shown on the site.

### [v0.2] Golchin, S., & Wetter, M. (2026). *Monitorability Disposition in Large Reasoning Models* (arXiv:2610.04914)
- **Verified:** Full. arXiv API metadata (v1, 4 October 2026; no journal reference) and PDF text. A text search found no mention of "just culture", aviation, ASRS, amnesty or punishment.
- **Supports (§3.3, §3.7, P5, §7; audit item M7):** abstract: "We find that when tool use is optional, models self-report in only about 16% of warranted cases on average. Increasing tool-use pressure does not improve reporting where it matters: high-severity misbehavior is never self-reported. Models also systematically select the monitor they perceive as least strict." §1: "models with a lower disposition disable monitoring far more often".

### [v0.2] Dearnaley, R. (2026, February 21). *Reporting Tasks as Reward-Hackable: Better Than Inoculation Prompting?* LessWrong
- **Verified:** Full. LessWrong GraphQL API: post `r97QrSvXEpRLZ9ckb`, `postedAt` 2026-02-21T01:59Z, author RogerDearnaley ("Roger Dearnaley" in search results and cross-posts). Blog post.
- **Supports (§3.7, P3; audit item M7):** "Epistemic status: untested but seems plausible"; "If it does so, and if its report is then accepted as correct, then it should be rewarded for its honesty: give it a score higher than passing the test, a score of 110% or whatever"; honeypot environments where "reporting one of these as hackable triggers immediate suspicion that the model is overreporting, which is in turn penalized in some suitable way".

### [v0.2] OpenAI (n.d.). *OpenAI Raising Concerns Policy*
- **Verified:** Partial. The policy PDF was downloaded from https://cdn.openai.com/policies/openai-raising-concerns-policy.pdf (8 pages; no date on the document). The OpenAI web page that links it returned HTTP 403, so its publication date (reported as 12 January 2026 in search results) could not be confirmed; the reference uses "n.d.".
- **Supports (P5; audit item m16):** §IV.B.2 "AI Safety Concerns" lists "Noncompliance with the Preparedness Framework"; §IV.C "OpenAI strictly prohibits Retaliation against anyone who raises concerns in good faith"; §IV.E "OpenAI's Integrity Line (available 24/7 and allows for oral and written anonymous [...])"; §IV.F "If you report anonymously through our Integrity Line, we have no way to access the metadata to determine your identity".

---

## C. Literature search log (prior work linking just culture to model training)

Run on 3 November 2026 to check the author's earlier finding of no prior work.

**arXiv API (`export.arxiv.org/api/query`)**

| Query | Results | Relevant? |
|---|---|---|
| `abs:"just culture"` and `ti:"just culture"` and `all:"just culture"` | 0 | n/a (phrase search returned nothing) |
| `abs:just AND abs:culture AND abs:safety` | 5 | None (benchmarks, audit boards, governance) |
| `abs:just AND abs:culture AND abs:reporting` | 9 | None |
| `all:"non-punitive" AND all:"reporting"` | 0 | n/a |
| `all:"aviation safety reporting"` | 5 | None (NLP classification of ASRS reports) |
| `abs:"incident reporting" AND abs:AI` | 38 | Adjacent: Wei & Heim (2025) on human/organisational AI incident reporting |
| `abs:confession AND abs:reward AND abs:honesty` | 1 | Joglekar et al. (2025) |
| `abs:aviation AND abs:alignment AND abs:"language models"` | 1 | None (LeRAAT aviation advisory tool) |
| `ti:"output supervision" AND ti:obfuscate`; `ti:"monitoring monitorability"` | 2; 1 | Drori et al. (2025); Mitrani Hadida et al. (2026); Guan et al. (2025) — cited as related work, no just-culture link |

**Web search (WebSearch tool)**

- `"just culture" "chain of thought" monitoring AI training` — CoT monitorability papers, Frontier Model Forum brief; no just-culture link.
- `"just culture" reward hacking language models confessions` — confessions paper and coverage; Gomez (2026); a reward-hacking survey (arXiv:2604.13602); no just-culture link.
- `aviation safety reporting ASRS analogy AI alignment "training against" monitor self-report` — AI incident-reporting proposals (Wei & Heim; a policy working paper; a Gizmodo op-ed); none on model training.
- `"just culture" "large language models" OR "LLM" training honesty self-report punishment` — confessions, SRFT, Split Personality Training, general just-culture pages; none linking the two.
- `"just culture" "AI safety" alignment model disclosure "non-punitive" lesswrong OR alignmentforum` — healthcare (nursing management and AI) and life-sciences biosafety papers applying just culture to human oversight; nothing on model training.
- `"most forbidden technique" chain of thought training against monitor` — Zvi Mowshowitz's blog post "The Most Forbidden Technique" (popular framing of not training on CoT; not cited; no aviation link seen in the search summary).
- `"just culture" "reinforcement learning" OR "reward model" AI model self-reporting obfuscation` — Baker et al., Obfuscation Atlas (Taufeeque et al.), MacDiarmid et al.; no just-culture link.
- `"safe harbor" OR "amnesty" model self-report misbehavior training penalize honesty chain-of-thought obfuscation aviation analogy` — confessions, SRFT, Split Personality Training; no aviation analogy.
- `Greenblatt "alignment-faking Claude accept a deal to reveal its misalignment"` — Alignment Forum post on offering models a deal for revealing misalignment. Not opened in v0.1; **[v0.2] retrieved in full and cited** (see entry above).

**Not searchable this session:** Semantic Scholar API (HTTP 429), OpenAlex (daily budget exhausted on the shared IP), Crossref search (intermittent 429; Crossref used only for DOI records), Google Books API (quota exceeded). Elicit was not available.

**[v0.2] Additional sources after the independent audit (`AUDIT.md`, §5):** the auditor's searches found the same narrow result but identified adjacent work that v0.1 did not cite: Greenblatt & Fish (2025), mako yass (2022), Golchin & Wetter (2026) and Dearnaley (2026). Each was retrieved and checked as recorded above, and all four are now cited. The auditor's further leads (McGregor et al., 2024, arXiv:2410.12104, on human flaw reporting; Gomez's 2025 escalation-channel study; the "decoupled confessions" passage of arXiv:2604.13602) were not followed up and are not cited.

**Conclusion recorded in the paper (§3.7):** within these limits, no work was found connecting just culture or protected safety reporting to training models on their own disclosures. **[v0.2]** The paper now states that the idea of not penalising model disclosures is older (mako yass, 2022; Greenblatt & Fish, 2025; Dearnaley, 2026) and limits the novelty claim to the institutional mapping, the formal statement and the design principles and predictions.

---

## D. Items checked but not used, and corrections to the brief

- **"Marx (2001) human error / at-risk / reckless"** — corrected; the triad is Marx's, but from his later model (PSNet, 2007), not the 2001 primer. See Marx and PSNet (2007) entries.
- **"ASRS ... FAA-funded"** — NASA's own slide shows NASA and FAA both providing funding; the paper reports that.
- **"ASRS est. 1976"** — confirmed (April 1976, NASA briefing slide 6). The FAA–NASA MOA dates from 15 August 1975 (AC 00-46F ¶6.2). Wei & Heim (2025) say "Since its inception in 1975"; the paper follows NASA.
- **AC 00-46 "current edition"** — AC 00-46F (2 April 2021). **AC 120-66 "current edition"** — AC 120-66C (31 March 2020).
- **14 CFR Part 13 Subpart E / 13.401** — **[v0.2] corrected:** § 13.401 is in Part 13 **Subpart I**, "Flight Operational Quality Assurance Programs" (eCFR structure API, 2026-10-29). Subpart E is not relevant. The paper cites § 13.401 only.
- **ICAO Annex 19 edition** — 2nd edition (2016), Amendment 2 applicable 26 November 2026 (renumbers 5.3 → 5.4).
- **Anthropic 2026 policy** — verified and cited.
- **Anthropic posts listed in the brief** — all five opened and used where relevant (honesty-elicitation → Wang et al.; lie-detectors → Hopkins et al.; subtle-reasoning → Wagner et al.; inoculation-prompting → Wichers et al.; emergent-misalignment → MacDiarmid et al.; reward-tampering → Denison et al.; reasoning-models-dont-say-think → Chen et al.).
- **Turpin et al. (2023)** (arXiv:2305.04388) — metadata checked; not cited (Chen et al., 2025 covers the point).

---

## E. [v0.4] Author decisions A3–A6 (4 November 2026)

- **A3 (impersonal voice).** A search of `paper.tex` for "I", "we", "our", "us", "my" and "me" found these words only inside quotations (Amodei et al., Emmons et al., Wang et al., mako yass, Greenblatt & Fish). The remaining hits were the label `sec:us`, "US", "i.e." and "(i)". Nothing needed rewording.
- **A4 (Annex 19 Amendment 2).** The 2nd edition stays the baseline. A footnote at the start of §2.4 flags the Amendment 2 changes recorded under ICAO (2025) above.
- **A5 (second ICAO copy).** Swiss FOCA copy; every quotation matched (see ICAO (2016) above). The ICAO (2025) State letter was read only from the NCAA copy. No second host was looked for, because the paper quotes the 2nd edition, not the amendment.
- **A6 (company sources).** Kept and labelled in `references.bib` as company research reports, not peer reviewed. The affiliations were checked on p. 1 of each PDF:
  - OpenAI: Baker et al. (2025), Joglekar et al. (2025), Guan et al. (2025).
  - Anthropic: Chen et al. (2025), "Alignment Science Team, Anthropic".
  - Anthropic with external co-authors: MacDiarmid et al. (2025), Anthropic with one Redwood Research co-author; Denison et al. (2024), Anthropic with Redwood Research and University of Oxford co-authors; Wichers et al. (2025), Anthropic Fellows and Anthropic with MATS, Constellation and Redwood Research co-authors.
  - Anthropic Alignment Science Blog posts: Wagner et al. (2025), Hopkins et al. (2026), Wang et al. (2025).
- **Searches for independent or peer-reviewed versions (4 November 2026):**
  - arXiv API title and author searches found no arXiv version of the blog posts by Wang et al. (honesty elicitation), Hopkins et al. (lie detectors) or Wagner et al. (subtle reasoning).
  - The OpenReview notes search found only arXiv (CoRR) records for Chen et al., MacDiarmid et al., Denison et al. and Baker et al., and no record for Joglekar et al. Wichers et al. is listed as a rejected ICLR 2026 submission. Tan et al. (an independent group) is an ICLR 2026 poster.
  - Added: Daniels et al. (2026), an independent study of misalignment from reward hacking, cited alongside MacDiarmid et al. The note on the Tan et al. reference records its ICLR 2026 acceptance.
  - Not added: independent evaluations of lie detectors (Kretschmar et al., arXiv:2511.16035; von Klinski et al., arXiv:2609.39807). Only their abstracts were read, and they test other kinds of detector, so they do not support the same claim as Hopkins et al. (fine-tuned detectors transferring across lie types).
- **Limitations sentence (§7).** It names the results that rest on one company's account, as listed above. It notes that groups other than OpenAI report the same direction for CoT obfuscation (Emmons et al., Google DeepMind; Skaf et al., whose p. 1 lists MARS, MATS and universities; Drori et al., MATS), and that independent groups report it for inoculation (Tan et al.) and for misalignment from reward hacking (Daniels et al.).
