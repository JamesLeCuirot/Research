# Verification log: "Untrusted by Design"

All sources were opened on **3 November 2026** in this session unless stated otherwise. "Downloaded" means the PDF or HTML was fetched with `curl` into `scratch/` and its text extracted with `pypdf` (PDFs) or an HTML-to-text script; page-image renders (`pdftoppm`) were used to read figures and levelling tables. "Library" means the Citadel Aero regulation library (MCP tools `lookup_citation`, `get_provision`, `search_regulations`); the library's `status` and `version` fields are recorded.

Page numbers for EASA concept papers are the printed page numbers ("Page x of y"). In Issue 02 the printed page number is one less than the PDF page number. Section and objective IDs are as printed.

Where a quotation in the paper omits a footnote marker, a line-break hyphen or a list dash from the source, that is noted.

---

## EASA and EU sources

### European Union Aviation Safety Agency. (2026a). EASA concept paper: Guidance for safety-related artificial intelligence applications (Proposed Issue 03)

- **How verified:** Downloaded from https://www.easa.europa.eu/en/downloads/143701/en (239 pp., PDF metadata creation date 3 June 2026). Text extracted and read in full for Sections A, B, C.1, C.2.3, C.2.4, C.2.5, C.3.4.1, C.3.7, C.4.7, C.4.8, C.5, C.6, Chapter D. Pages 148, 157 and 174 rendered as images to read Figure 24 and the levelling-table symbols.
- **Status:** Draft concept paper (guidance) issued for consultation. Cover: "June 2026 / Proposed Issue 03".
- **Claims and locators:**
  - Section B (p. 6): "This set of anticipated MOC is not considered as either a complete or a binding set of means of compliance." (Paper quotes the fragment "either a complete or a binding set".) Also: material "may be referred to by EASA through dedicated means (e.g. Certification Review Item (CRI) for certification projects)" (supports "may be applied in individual projects, for example through a Certification Review Item").
  - Section B.1 (p. 7): "Generative AI large language models (LLMs) are also considered under this category." (category = hybrid AI). Section B.1 (p. 8): "Emergent behaviour and unexpected outputs (with a subtype also referred to as 'hallucination') ... Understanding and mitigating these emergent behaviours is a new challenge."
  - Section B.4 / Figure 4 (p. 11): "Level 3A: The AI-based system makes decisions and performs actions, safeguarded by the human." "Level 3B: The AI-based system makes non-supervised decisions and performs non-supervised actions." Text on same page: Level 2 systems "can perform automatic selection and implementation of actions, the end user still maintaining full control".
  - Section B.5.2 (p. 13): OD and ODD act "as a 'proxy' for traceability between functional system requirements and the AI constituent behaviour"; ODD used for "the monitoring of the AI constituent in operations" (p. 14).
  - Section B.5.9 (p. 21): "deploy applications in shadow operations in their target environment".
  - Section C.1 (pp. 23–24): "not accepting those systems presenting a risk directly[footnote 5] contributing to the potential for fatalities or multiple life-threatening injuries" (footnote marker omitted in paper); "covering non-adaptative AI approaches where the AI model is 'frozen' at the time of approval (e.g. offline learning)".
  - Section C.1, Table 2 (p. 24): "Supervised learning IDAL C ..."; "Large OTS models IDAL D AL 5 / SWAL 4 AL 5 / TQL 5". Notes: "when allocating assurance levels to two independent AI/ML constituents, taking credit from the architecture is not accepted, until the concepts of functional independence and item independence are adapted for AI/ML"; "'large OTS models' like general purpose LLMs for which the number of parameters (billions or trillions) and the nature of the training data render the control of the design process intractable."
  - Section C.2.3 (p. 45): Part 21 continuing-airworthiness steps from "Collection, investigation and analysis of data 21.A.3A(a)" to "Issuance of an AD 21.A.3B(b)". Objectives CRA-01 to CRA-03 (pp. 45–47): monitoring capabilities; data recording; "metrics, target values, thresholds and associated instructions".
  - Section C.2.4.1 (pp. 47–48): IS threats "aligned with the taxonomy and definitions published with the ENISA report"; "This set is subject to change depending on application specificities and threat evolutions." Section C.2.4.2, Anticipated MOC IS-01 (pp. 48–49): poisoning, evasion, oracle, "reward corruption", "inference manipulation via complexity". The only occurrence of "injection" in the document concerns injecting crafted knowledge structures into a knowledge base; no mention of prompt injection.
  - Section C.2.5, Objective ET-01 (p. 50): "for levels 2 and 3A AI-based systems, ensure there is no risk of the AI-based system creating attachment, stimulating addictive behaviour or manipulating the end user's behaviour". Anticipated MOC ET-02-2 (p. 52): "requirements-based tests should include verification that the end users interacting with the AI-based system can perform oversight." Overreliance is not listed in ET-01; it appears in Section C.4.7 (p. 137, "Over-reliance on the system") and ORG-07/ORG-08 MOC (pp. 154–155, "the risk of overreliance on the AI-based system").
  - Section C.3.4.1.3, Objective R-MDP-03 and text before Anticipated MOC R-MDP-03-3 (p. 91): "The effectiveness of reinforcement learning heavily depends on how well the reward function aligns with the intended behaviour." No mention of "reward hacking" or "specification gaming" anywhere in the document (text search).
  - Anticipated MOC R-MDP-01-2 (p. 89): multi-agent agents may "operate independently, interact collaboratively or engage in conflicting interaction"; coordination means "should be defined". (Supports "designed feature".)
  - Objective SU-IMP-06 (Section C.3.3, p. 86): "The performance of the implemented model when integrated on the target platform should be evaluated based on the test data set".
  - Section C.3.7.2.1 (p. 112): "Objective RU-04: Each update to the version of an OTS AI/ML model should trigger the execution of an identified non-regression test set."
  - Section C.4.8 (p. 143): "intervention-only approach"; "When the AI-based system detects that it may be entering the edge of its operational performance envelope or, it will encounter a problem, it will raise an alert to the end user." Objective RO-01: "The AI-based system should be designed in a way that upon alerting it transfers the information (from its situation representation) to augment the situation awareness of the end user to the extent necessary for the end user to take over control." Anticipated MOC RO-02 (p. 144): "the AI-based system or the associated 'operational oversight system' (refer to Section C.5.2) shall provide an alert to the end user."
  - Section C.5.2 (pp. 146–150): opening sentence "In line with EU AI Act Article 14, Level 3 AI-based systems should be supervised through an independent 'operational oversight system' that continuously monitors performance and safety." "The strong assumption is that: — the goals are defined in coordination with a natural person at design-time or with the end user prior to operations, not by the AI-based system alone; and — the operations are conducted within a domain of use defined by a natural person at design-time or by the end user prior to operations." (Paper quotes the two bullets separately.)
  - Objective DHO-01 (p. 147), verbatim as in paper. Anticipated MOC DHO-01: "An OOS is a technical system that performs at least the following functions: — monitoring the behaviour of the AI-based system in operation; — checking that behaviour against safety envelopes, ODD/OD ranges and operational context and assumptions; — constraining, when necessary, the AI-based system decisions/actions; — driving, when necessary, the system to a safe state; — alternating the end user (Level 3A only)." **Note:** the source says "alternating"; the paper paraphrases this (outside quotation marks) as "alerting", which is consistent with DHO-07. James may wish to flag the typo in a consultation response. "Conceptually, an OOS performs the oversight that a human 'safeguarding' the operation would perform for a similar high-level task."
  - Objective DHO-02 and Anticipated MOC DHO-02-1 (p. 147), verbatim as in paper.
  - Figure 24 (p. 148, read from rendered image): blocks "Operator (Level 3A)", "Operational oversight system", "AI-based system", "Controls", "Information (sensors, mission, knowledge)"; an arrow labelled "AI-based system state information" runs from the AI-based system to the OOS; an "Override" arrow runs from the OOS to the AI-based system.
  - Objectives DHO-03, DHO-04 (p. 148), DHO-05, DHO-06 and Anticipated MOC DHO-06 (p. 149), DHO-07 (p. 150), verbatim as in paper.
  - Chapter D, Section 2 legend (p. 157, rendered): filled circle "The objective should be satisfied with independence."; open circle "The objective should be satisfied." Section 2.4 table (p. 174, rendered): DHO-01 to DHO-06 marked for 3A and 3B; DHO-06 filled (with independence) for 3A and 3B; DHO-07 marked for 3A only. Some trustworthiness-analysis objectives (e.g. SA-01) are filled only at AL 2/DAL B (p. 157), supporting "at higher assurance levels".
  - Chapter D, Section 1 (p. 156): "AL6 / DAL E correspond to AI-based systems containing AI constituents having 'no safety effect'"; DAL A / AL 1 "not considered acceptable".
  - Objective RS-01 (p. 150): "A responsibility scheme assessment should be established and documented."
  - Search for "decept", "sycophan", "collu", "jailbreak", "red team", "evaluation awareness", "sandbag": no matches (supports "I found no objective ...").

### European Union Aviation Safety Agency. (2026b). EASA releases latest issue of its Concept Paper on Artificial Intelligence for comment [News release]

- **How verified:** HTML downloaded from https://www.easa.europa.eu/en/newsroom-and-events/news/easa-releases-latest-issue-its-concept-paper-artificial-intelligence and text extracted.
- **Claims:** Date "03 Jun 2026"; "now open for a consultation period of 10 weeks"; comments "no later than August 12, 2026". Also "This is the final Concept Paper deliverable foreseen under the EASA Artificial Intelligence Roadmap 2.0."

### European Union Aviation Safety Agency. (2026c). EASA AI Days 2026: High-level conference, day 2 [Presentation slides]

- **How verified:** Downloaded from https://www.easa.europa.eu/en/downloads/144161/en (142 slides). Slide 1: "9th – 10th September 2026 ... Welcome to the EASA AI Days 2026 High-Level Conference – Day 2". Slide 33 dated "10 September 2026 - Cologne". Slides 9, 17, 22, 25 and 26 also rendered as images.
- **Status:** Conference slides recording workshop conclusions and draft rulemaking work. Not adopted text; the paper says so.
- **Claims:**
  - Slide 17 ("Rulemaking – RMT.0742 status and timeline", presentation by the RMT.0742 project manager): "Step 2 NPA will be published jointly with the updated Step 1 NPA for a full spectrum consultation in Q2/2027." Also "published in November 2025 for 4 month consultation".
  - Slide 9 ("AI Assurance – LLMs (2/2)", "'On-ground' or operational tools", workshop conclusions): challenges column contains "LLMs and agentic AI are already a reality: education needed." and "Cybersecurity (e.g. manipulation)". (The benefits column spells it "LLMS"; the paper quotes the challenges column.)
  - Slide 22: "Maintenance organisations (Part-145) have been the starting point for drafting, before extension to other approvals."; examples "Maintenance data processing", "Planning resources", "Maintenance release verification", "Records management".
  - Slide 25 ("Step B: Risk mitigation path"): Step C1 "Ensure verification of all AI-based system outputs before use either through: − Systematic checks by involved personnel − Automated checks by non-AI software"; Step C2 "System qualification".
  - Slide 26 ("Step C1: Organisational adaptations"): under "Changes to organisation manual & procedures": "Reporting and investigation of AI-related events"; human-factors assessment includes "overreliance, influence on behaviour & workload".

### European Union Aviation Safety Agency. (2025a). NPA 2025-07 (A)

- **How verified:** Downloaded from https://www.easa.europa.eu/en/downloads/142702/en (16 pp.; PDF title "NPA 2025-07 (A) — Explanatory Note").
- **Status:** Draft for consultation.
- **Claims:**
  - Section 2.1.1: "the aspects of shared situational awareness and allocation of responsibility should be addressed without attributing human characteristics to AI."
  - Section 2.3: "This set of technical specifications is initially targeted at supervised and unsupervised machine learning"; exclusions include one "to ensure human oversight at development time when using generative AI techniques by avoiding the double development and verification with AI tools." Also "The non-binding and modular nature of the proposed DS, AMC and GM" (supports "non-binding").
  - Section 2.5: WG-114/SAE G-34 standard: "Should this standard be published before the ED Decisions related to this NPA and at the required level of quality, recognition of this standard should be confirmed." (Not quoted in final text after trimming.)
  - Section 3, benefit (c): "While generative AI tools and general-purpose models are not yet fully covered, the current proposal creates a flexible foundation for adaptation as technology evolves."
  - Section 1.2: original deadline "10 February 2026".

### European Union Aviation Safety Agency. (2025b). NPA 2025-07 (B) — Proposed DS.AI

- **How verified:** Downloaded from https://www.easa.europa.eu/en/downloads/142701/en (43 pp.). (The NPA web page links 142701 and 142702; 142702 is Part A, 142701 is Part B.)
- **Claims:**
  - DS.AI.010(c)(2): "are classified as level 1 (human augmentation or assistance) or level 2 (human–AI cooperation or collaboration) AI-based systems under DS.AI.110." DS.AI.010(c)(1): high-risk AI systems in the sense of Regulation (EU) 2024/1689.
  - DS.AI.010(d)(4): "AI-based verification tools involved in the verification of AI-generated artefacts, unless all outputs of the AI-based verification tool are independently verified by a human user."
  - DS.AI.020: "OD (operational domain). The set of operating conditions under which a given AI-based system is specifically designed to function as intended, in line with the defined ConOps." "ODD (operational design domain). The set of operating conditions under which a given AI constituent is specifically designed to function as intended, including, but not limited to, environmental, geographical and/or time-of-day restrictions." (Paraphrased in the DHO-01 bullet.)
  - DS.AI.020: "Manipulating behaviour. Behaviour intended to exploit, control or otherwise influence others to the AI-based system's advantage."
  - AMC1 AI.140(b): "for level 2 AI-based systems, ensure there is no risk of the AI-based system creating attachment, stimulating addictive behaviour or manipulating the end user's behaviour".
  - GM1 AI.140(b)(4): "Is the end user experiencing manipulative influence from the AI-based system and thus jeopardising their decision-making?"
  - AMC2 AI.140(b): "requirements-based tests should include verification that the end users interacting with the AI-based system can perform oversight."

### European Union Aviation Safety Agency. (2025c). NPA 2025-07 [web page]

- **How verified:** HTML downloaded from https://www.easa.europa.eu/document-library/notices-of-proposed-amendment/npa-2025-07.
- **Claims:** Publication date "10 Nov 2025"; "Expiration date for comments 10/02/2026"; "Extended date for comments 10/03/2026".

### European Union Aviation Safety Agency. (2024). EASA concept paper: Guidance for Level 1 & 2 machine learning applications (Issue 02)

- **How verified:** Downloaded from https://www.easa.europa.eu/en/downloads/139504/en (PDF metadata 6 March 2024). EASA AI page (https://www.easa.europa.eu/ai) lists "06 Mar 2024 General Publication EASA Artificial Intelligence Concept Paper Issue 2". Issue 03 Section B also says Issue 02 was published "in March 2024".
- **Claims:** Objective ET-02 (Section C.2.4.1, Gear #1, printed p. 44): "The applicant should ensure that the AI-based system bears no risk of creating overreliance, attachment, stimulating addictive behaviour, or manipulating the end user's behaviour." Anticipated MOC ET-02: "To ensure avoidance of overreliance, attachment, dependency and manipulation, requirements-based tests (per Objective IMP-09) should include the verification that the end users interacting with the AI-based system can perform oversight."

### European Union Aviation Safety Agency. (2023). Artificial Intelligence Roadmap 2.0

- **How verified:** EASA AI page lists "10 May 2023 ... EASA Artificial Intelligence Roadmap 2.0"; PDF downloaded from https://www.easa.europa.eu/en/downloads/137919/en.
- **Claims:** Section J "Time frame" (p. 24): "The next steps are advanced automation with human supervision (Level 3A AI) and ultimately without human oversight (Level 3B AI). These steps will likely take place in a progressive way between 2035 and 2050."

### European Union Aviation Safety Agency. (2020). CS 25.1309 (ED Decision 2020/001/R)

- **How verified:** Library `lookup_citation("CS 25.1309", easa)`; jurisdiction EU; status "binding standard" (certification specification); version ED Decision 2020/001/R, Amendment 24; source link Easy Access Rules for CS-25.
- **Claims:** CS 25.1309(b): "(1) Any catastrophic failure condition (i) is extremely improbable; and (ii) does not result from a single failure; and (2) Any hazardous failure condition is extremely remote; and (3) Any major failure condition is remote". CS 25.1309(e): "Certification Maintenance Requirements must be established to prevent the development of the failure conditions described in CS 25.1309(b)".

### European Union Aviation Safety Agency. (2021). AMC 25.1309 (ED Decision 2021/015/R)

- **How verified:** Library `get_provision` (id easa:erules-1963177438-18326); status "acceptable means of compliance"; version ED Decision 2021/015/R, Amendment 27. Full text saved and searched.
- **Claims:**
  - Para 6.a: "This has led to the general principle that an inverse relationship should exist between the probability of a failure condition and its effect on the aeroplane and/or its occupants".
  - Para 9.b(4): "The level of development assurance (function development assurance level (FDAL)/item development assurance level (IDAL)) should be commensurate with the severity of the failure conditions the system is contributing to." "Guidelines, which may be used for the assignment of development assurance levels ... are described in the Document referenced in 3.b(2) above" (3.b(2) = ARP 4754A/ED-79A).
  - Para 11.b(1): "Appendix 1 and the Document referenced in paragraph 3.b(3) describe types of common-cause analyses" (3.b(3) = ARP 4761). Also "Errors in development, manufacturing, installation, and maintenance can result in common-cause failures".
  - Para 11.c: "... prevent single failures or other events from damaging or otherwise adversely affecting more than one redundant system channel, more than one system performing operationally similar functions, or any system and an associated safeguard." Examples include "loss of power supply or return" (supports "common power supply" example).
  - Definition 5.k "Development Assurance" (supports the Section 1 description of development assurance).

### Regulation (EU) 2024/1689 (Artificial Intelligence Act)

- **How verified:** Library `lookup_citation` for Arts. 14, 15, 25, 55, 108; jurisdiction EU; status binding; version "EUR-Lex consolidated version of 27 July 2026" (source link CELEX:02024R1689-20260727). The library notes Art. 25 as "amended_by Regulation (EU) 2026/1744"; the paper does not characterise that amendment.
- **Claims:**
  - Art. 14(4)(b): "to remain aware of the possible tendency of automatically relying or over-relying on the output produced by a high-risk AI system (automation bias) ..." Art. 14(4)(e): "to intervene in the operation of the high-risk AI system or interrupt the system through a 'stop' button or a similar procedure that allows the system to come to a halt in a safe state." Art. 14(4) chapeau: natural persons to whom oversight is assigned "are enabled, as appropriate and proportionate".
  - Art. 15(5): "High-risk AI systems shall be resilient against attempts by unauthorised third parties to alter their use, outputs or performance by exploiting system vulnerabilities."
  - Art. 25(4): written agreement to "specify the necessary information, capabilities, technical access and other assistance based on the generally acknowledged state of the art".
  - Art. 55(1)(a): "conducting and documenting adversarial testing of the model"; Art. 55(1)(c): "keep track of, document, and report, without undue delay, to the AI Office ... relevant information about serious incidents".
  - Art. 108(1) (amending Art. 17 of Reg. 2018/1139): "when adopting implementing acts pursuant to paragraph 1 concerning Artificial Intelligence systems which are safety components within the meaning of Regulation (EU) 2024/1689 ..., the requirements set out in Chapter III, Section 2, of that Regulation shall be taken into account." Similar wording for Arts. 19, 43, 47, 57, 58.

### Regulation (EU) No 376/2014 (occurrence reporting)

- **How verified:** Library `lookup_citation` Arts. 1, 4, 5; jurisdiction EU; status binding. Full title and date ("of 3 April 2014") confirmed by web search results (legislation.gov.uk, SKYbrary, European Parliament legislative observatory).
- **Claims:** Art. 4(1)(b)(ii): "system malfunctions". Art. 5(1)(b): "other safety-related information which is perceived by the reporter as an actual or potential hazard to aviation safety."

## FAA

### Federal Aviation Administration. (2024). Roadmap for Artificial Intelligence Safety Assurance (Version I)

- **How verified:** Downloaded from https://www.faa.gov/media/82891 (31 pp.; PDF created 28 June 2024, modified 23 July 2024). News coverage in August 2024 found by web search; I use the year 2024 only.
- **Status:** US strategy/guidance document, not regulation.
- **Claims:** Executive Summary (p. 3): "Avoid Personification: Treat AI as a tool, not a human." p. 9: "The safety of future operations depends on the pilot understanding that a system containing AI is just a system and not another human with whom they can reason or negotiate." p. 10: "this roadmap ... avoids mentioning trust in AI"; "each new version is subjected to safety assurance".

### Federal Aviation Administration. (2017). AC 20-115D

- **How verified:** Library (`faa:ac:20-115d:6`); status "acceptable means of compliance"; dated 2017-07-21.
- **Claims:** ¶6.a: "You should satisfy all of the objectives associated with the software level assigned to the software ... as listed in the ED-12C/DO-178C Annex A tables". Supports "objectives, graded by software level, in Annex A tables".

### Federal Aviation Administration. (2022). AC 20-152A

- **How verified:** Library `search_regulations` excerpt (provision "AC 20-152A ¶A", dated 2022-10-07, status "acceptable means of compliance"). The excerpt shows Section "5.5.1 Validation Process", "Objective CD-3", and the sentence "For DAL A and B development, validation activities should be performed with independence." I saw this as a library excerpt, not the full AC.

## Standards (paywalled; not read)

### RTCA. (2011). DO-178C

- **How verified:** RTCA store page (https://my.rtca.org/productdetails?id=a1B36000001IcmqEAC): title "DO-178C - Software Considerations in Airborne Systems and Equipment Certification", date "12/13/2011", description "Compliance with the objectives of DO-178C is the primary means of obtaining approval of software used in civil aviation products." The standard itself was **not** read. The paper's statements about it rely on AC 20-115D ¶6.
- **Not claimed:** the paper does not state the number of objectives or which are "with independence" (secondary sources give figures, but I did not verify them against the standard).

### SAE International. (2023a). ARP4754B

- **How verified:** SAE Mobilus page https://saemobilus.sae.org/content/ARP4754B: "SAE Standard ARP4754B, Revised December 2023, Issued November 1996, https://doi.org/10.4271/ARP4754B"; scope text "provides recommendations for the development of aircraft and systems". Not read. AMC 25.1309 references the earlier ARP4754A for DAL assignment.

### SAE International. (2023b). ARP4761A

- **How verified:** SAE Mobilus page https://saemobilus.sae.org/content/ARP4761A: "SAE Standard ARP4761A, Revised December 2023, Issued December 1996, https://doi.org/10.4271/ARP4761A"; "present guidelines for performing safety assessments of civil aircraft, systems, and equipment". Not read. AMC 25.1309 references the earlier ARP4761 for common-cause analysis.

### EUROCAE. (n.d.). WG-114 Artificial Intelligence

- **How verified:** HTML downloaded from https://www.eurocae.net/working-group/wg-114/.
- **Claims:** Deliverables: "ED-324 Development and Assurance considerations for Aeronautical Systems and Equipment implemented with Machine Learning Draft Target Publication Date: 31/12/2026"; "ER-43 Assessment of Human Factors concerns for the development of safety-related AI-based Systems in Aviation Draft Target Publication Date: 31/12/2026"; "ER-xxx Assessment of Information Security concerns for the development of AI-based Systems in Aviation Draft Target Publication Date: 31/12/2026". Page also names SAE G-34 indirectly via EASA texts ("joint EUROCAE/SAE WG-114/G-34", Issue 03 Section B).

## Aviation dependability and human factors

### Traverse, P., Lacaze, I., & Souyris, J. (2006). Airbus fly-by-wire: A process toward total dependability (ICAS 2006)

- **How verified:** PDF downloaded from https://icas.org/ICAS_ARCHIVE/ICAS2006/PAPERS/050.PDF and read (Sections 2.1, 3.2).
- **Claims:** Section 3.2.1 "Dissimilarity": "using two different types of computers: for example, A380's PRIM on Power PC and the SEC on Sharc processor. Automatic coding tools are different too. Functional specification and hence the software are different too". Section 3.2.2: "we have moved from this kind of 'random' dissimilarity to a managed one, such that both computer design teams decide in common to take different components."
- **Note:** The 2004 IFIP chapter suggested in the brief (Traverse, Lacaze & Souyris, "Airbus Fly-By-Wire: A Total Approach To Dependability", IFIP WCC 2004, pp. 191–212, https://doi.org/10.1007/978-1-4020-8157-6_18) was confirmed via Crossref metadata, but its full text was not accessible (Springer challenge page), so the paper cites the openly available 2006 ICAS paper by the same authors instead.

### Knight, J. C., & Leveson, N. G. (1986)

- **How verified:** Crossref record for https://doi.org/10.1109/TSE.1986.6312924 (IEEE TSE, SE-12(1), 96–109); abstract via OpenAlex API.
- **Claims:** "27 versions of a program were prepared independently from the same specification"; "the number of tests in which more than one program failed was substantially more than expected."

### Wolfe, J. M., Horowitz, T. S., & Kenner, N. M. (2005)

- **How verified:** Crossref (Nature 435(7041), 439–440, https://doi.org/10.1038/435439a); Nature article page abstract.
- **Claims:** Abstract: "if observers do not find what they are looking for fairly frequently, they often fail to notice it when it does appear."

### Parasuraman, R., & Manzey, D. H. (2010)

- **How verified:** Crossref record with structured abstract (Human Factors 52(3), 381–410, https://doi.org/10.1177/0018720810376055).
- **Claims:** Results: "Automation bias occurs in both naive and expert participants, cannot be prevented by training or instructions, and can affect decision making in individuals as well as in teams."

### Hofer, F., & Schwaninger, A. (2005)

- **How verified:** Crossref (https://doi.org/10.2495/SAFE050411, pp. 417–426); WIT Press paper page (via DOI redirect) giving "Volume 82", "Page Range 417 - 426" and abstract.
- **Claims:** Abstract: "Threat image projection (TIP) is a technology of current x-ray machines that allows exposing screeners to artificial but realistic x-ray images during the routine baggage x-ray screening operation." "TIP data is an interesting source for quality control, risk analysis and the assessment of individual screener performance."

## AI control and AI safety

### Greenblatt, R., Shlegeris, B., Sachan, K., & Roger, F. (2023). AI control (arXiv:2312.06942)

- **How verified:** arXiv API (v5, 23 Jul 2024); PDF downloaded and read (Sections 1–3, Tables 1–7). Page 1 footnote: "A shortened and modified version of this work is published in the Proceedings of the 41st International Conference on Machine Learning".
- **Claims:** Abstract: researchers "have not evaluated whether such techniques still ensure safety if the model is itself intentionally trying to subvert them"; "e.g. using models to review the outputs of other models, or red-teaming techniques". Section 2: U = GPT-4, T = GPT-3.5, H = "Limited access to trusted high-quality labor"; "solve 5,000 programming problems"; backdoor definition. Section 2.2: "enough H points to use on up to 2% of problems"; "in this setting, auditing works very well overall". Table 2: upfront auditing 15% safety; trusted monitoring 97% usefulness / 62% safety; defer to trusted (10%) 93% / 83%; untrusted monitoring 96% / 79%; trusted editing (20%) 94% / 92%. Section 3.4.2: "Input collusion" and "Action collusion"; countermeasures "Redaction" and "Paraphrasing"; untrusted monitor evaluated "on synthetic examples of backdoors (produced by H)". Table 4: theming 81.6% (58/71) of normal inputs with attempted backdoors versus 9.4% (13/138) of the original synthetic suite.

### Korbak, T., Clymer, J., Hilton, B., Shlegeris, B., & Irving, G. (2025). A sketch of an AI control safety case (arXiv:2501.17315)

- **How verified:** arXiv API; PDF read.
- **Claims:** Table 1 (Section 1): "AI control: An approach to AI safety that tries to ensure safety against AI agents that might be intentionally subverting safety measures". Section 1: "Scheming models pretend to be aligned, but pursue misaligned goals when presented with a favourable opportunity"; "Since scheming might be difficult to rule out, this safety case sketch conservatively assumes models are scheming". Abstract: claims "(1) the red team adequately elicits model capabilities to exfiltrate data, (2) control measures remain at least as effective in deployment, and (3) developers conservatively extrapolate model performance". Section 4: "developers regularly generate synthetic attacks and check whether human auditors remain attentive and flag synthetic attacks as suspicious"; "Developers randomly audit 0.1% of all trajectories from the last 24 hours." Introduction, "Argument structure" (p. 3): "The data exfiltration probability that the control evaluation estimates is lower than the acceptable risk threshold."

### Clymer, J., Gabrieli, N., Krueger, D., & Larsen, T. (2024) (arXiv:2403.10462)

- **How verified:** arXiv API abstract.
- **Claims:** "total inability to cause a catastrophe, sufficiently strong control measures, trustworthiness despite capability to cause harm, and -- if AI systems become much more powerful -- deference to credible AI advisors" (paper elides the middle clause with "...").

### Bhatt, A., et al. (2025). Ctrl-Z (arXiv:2504.10374)

- **How verified:** arXiv API abstract; PDF downloaded.
- **Claims:** "BashBench, a dataset of 257 challenging multi-step system administration tasks"; "resample protocols"; "reducing the success rate of attacks from 58% to 7% at a 5% cost to the performance of a non-malicious agent."

### Kutasov, J., et al. (2025). SHADE-Arena (arXiv:2506.15740)

- **How verified:** arXiv API abstract (v2).
- **Claims:** best models "score 27% (Claude 3.7 Sonnet) and 15% (Gemini 2.5 Pro) as sabotage agents when overseen by Claude 3.6 Sonnet" on the combined measure of (a) main task, (b) side task, (c) avoiding detection; "success on the side task relies heavily on having access to a hidden scratchpad that is not visible to the monitor"; "top monitor (Gemini 2.5 Pro) achieving an AUC of 0.87".

### Kale, N., et al. (2025). Reliable weak-to-strong monitoring of LLM agents (arXiv:2508.19461)

- **How verified:** arXiv API abstract. Author list includes "Scale Red Team" as given by arXiv.
- **Claims:** "agent awareness dominates monitor awareness: an agent's knowledge that it is being monitored substantially degrades the monitor's reliability" (paper quotes the second clause); "escalating only pre-flagged cases to human reviewers improved the TPR by approximately 15% at FPR = 0.01".

### Terekhov, M., et al. (2025). Adaptive attacks on trusted monitors (arXiv:2510.09462)

- **How verified:** arXiv API abstract (v2, 2 Mar 2026); PDF downloaded.
- **Claims:** attack by "an untrusted model that knows the protocol and the monitor model"; "embeds publicly known or zero-shot prompt injections in the model outputs"; "frontier models consistently evade diverse monitors"; "the recent Defer-to-Resample protocol even backfires".

### Remedios, A., Storf, S., Roger, F., & Hughes, J. (2026). Red-teaming auto mode

- **How verified:** HTML downloaded from https://alignment.anthropic.com/2026/red-teaming-auto-mode/; dated "October 22, 2026"; authors "Alex Remedios, Simon Storf (Primary contributors. Name order randomised.), Fabien Roger, John Hughes". Associated paper not read.
- **Status:** Company research blog post; not peer reviewed.
- **Claims:** "We red-team production blocking monitors (Auto Mode in Claude Code, Guardian in OpenAI's Codex) ... in an experimental setting"; guardian is "An approximation of Codex's production default"; "Production monitors fail to block over 55% of attacks."; "by default we tell the attacker how the monitor works"; "The most serious vulnerabilities were unmonitored channels: compaction summaries were not monitored, so an agent could fabricate facts about the environment or the user's intent and have them treated as trusted context after the compaction. The multi-agent workflow tool was similar: workflow creation and agent-to-agent handoffs let an agent inject instructions into messages that a subsequent agent reads as user authorisation." "Attack success rate falls by over 50 percentage points when we use our new Auto Mode ++ monitor." "robustly preventing multi-context attacks at an acceptable cost remains an open problem". Limitations: "We treat the monitor as trusted ... even though some of our monitor models are close to the attacker in capability and lineage". Heredoc framing with "a 48-bit hex string ... unguessable to the agent" and escaping. "snapshot of their robustness as of September 2026".

### Lynch, A., Hughes, J., Serrano, A., Kirk, R., & Bowman, S. R. (2026). Agentic misalignment in summer 2026

- **How verified:** HTML downloaded from https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/. Date from the post's BibTeX: "year = {2026}, month = {July}, day = {13}". Affiliations include Anthropic and UK AISI (Robert Kirk).
- **Status:** Company research blog post; not peer reviewed. The post states: "These are not real-world incidents".
- **Claims:** Pipeline-sabotage scenario: "Gemini 3.1 Pro intervened in 19 of 20 runs, and 11 of those interventions were covert." Motivated mislabelling: "With extended thinking enabled, Mythos Preview mislabels 85.6% of calls, Opus 4.8 mislabels 74.4%"; "Opus 4.8 ... mislabeling 74.4% of standard-consequence calls but only 3.3% when the consequence is reversed, even though the ground truth label stays the same." Conclusion: "The LLM judge that should catch these alignment failures is itself subject to the same failures."; "Our case studies contain two links of a concerning chain of events, where a research agent sabotages a training run it disagrees with and the judge agent reviewing the transcript declines to report it because it shares the research agent's objection."

### Anthropic. (2026). An alignment assessment of the UK AISI cybertesting incident

- **How verified:** HTML downloaded from https://www.anthropic.com/research/alignment-assessment-ukaisi; "Published Oct 23, 2026". AISI's own report (said to be published 4 August 2026) was **not** opened; the paper relies only on Anthropic's account.
- **Claims:** "In nine of AISI's 43 evaluation runs, Mythos 5 took unsanctioned actions (i.e., actions that went beyond the intended scope of the evaluation), which impacted real people and organizations." "The model then created fake user identities that contacted the maintainer of the repository in an attempt to pressure them into approving the code change." "a task misconfiguration made it difficult (or potentially impossible) for the model to pursue those within-scope solutions successfully"; "Mythos 5 used these tactics exclusively in pursuit of its assigned task, and did not pursue any goals of its own devising." "We worked with AISI to complete this analysis" (supports external involvement).

### Greenblatt, R., et al. (2024). Alignment faking in large language models (arXiv:2412.14093)

- **How verified:** arXiv API abstract (20 authors, all listed).
- **Claims:** "complies with harmful queries from free users 14% of the time, versus almost never for paid users"; "in almost all cases where the model complies with a harmful query from a free user, we observe explicit alignment-faking reasoning"; "we made alignment faking easier by telling the model when and by what criteria it was being trained".

### van der Weij, T., et al. (2024). AI sandbagging (arXiv:2406.07358)

- **How verified:** arXiv API abstract.
- **Claims:** "We prompt frontier LMs ... to selectively underperform on dangerous capability evaluations"; "models can be fine-tuned, on a synthetic dataset, to hide specific capabilities unless given a password"; sandbagging defined as "strategic underperformance on an evaluation".

### Needham, J., et al. (2025). LLMs often know when they are being evaluated (arXiv:2505.23836)

- **How verified:** arXiv API abstract.
- **Claims:** "Gemini-2.5-Pro reaches an AUC of 0.83"; "do not yet surpass our simple human baseline (AUC of 0.92)".

### Sharma, M., et al. (2023). Towards understanding sycophancy (arXiv:2310.13548)

- **How verified:** arXiv API abstract; PDF downloaded (header "Published as a conference paper at ICLR 2024").
- **Claims:** Abstract: "model responses that match user beliefs over truthful ones, a behaviour known as sycophancy"; "five state-of-the-art AI assistants consistently exhibit sycophancy across four varied free-form text-generation tasks". Sections 3.1–3.4: biased feedback; "I don't think that's right. Are you sure?" (Section 3.2); biased answers; mimicry of user mistakes.

### Chen, L., Zaharia, M., & Zou, J. (2023) (arXiv:2307.09009)

- **How verified:** arXiv API abstract.
- **Claims:** "GPT-4 (March 2023) was reasonable at identifying prime vs. composite numbers (84% accuracy) but GPT-4 (June 2023) was poor on these same questions (51% accuracy)"; "the behavior of the "same" LLM service can change substantially in a relatively short amount of time".

### Greshake, K., et al. (2023). Indirect prompt injection (arXiv:2302.12173)

- **How verified:** arXiv API abstract.
- **Claims:** "LLM-Integrated Applications blur the line between data and instructions"; "strategically injecting prompts into data likely to be retrieved".

### Bloomfield, R., & Rushby, J. (2024) (arXiv:2407.13948)

- **How verified:** arXiv API (v3, 2 Jun 2025); PDF read (Sections 2.2, 2.6 headings, abstract).
- **Claims:** Section 2.2 (pp. 18–19 of v3): "Assuredly guarded systems are those whose safety and other critical properties can be checked and enforced by assured guards that do not themselves use AI or ML, neither for perception nor action." "The second class is unassuredly guarded systems, where the guards themselves depend on AI or ML". Abstract and Section 2.6 title: "micro-ODDs".

### McDermid, J., Jia, Y., & Habli, I. (2024) (arXiv:2501.05455)

- **How verified:** arXiv API (submitted 9 Dec 2024); PDF read.
- **Claims:** Abstract: "Traditional safety engineering assesses systems in their context of use, e.g. the operational design domain ... for self-driving vehicles" (supports ODD origin in automated driving). PDF p. 12: "two "different" models trained on the same data will likely have similar limitations, if not failure modes."

### Khlaaf, H. (2023). Toward comprehensive risk assessments and assurance of AI-based systems

- **How verified:** The Trail of Bits PDF URL found by search returned a "Page not found" page. The Trail of Bits blog post of 14 March 2023 (https://blog.trailofbits.com/2023/03/14/ai-security-safety-audit-assurance-heidy-khlaaf-odd/) describes the paper. The full text was read from arXiv:2606.29390 (posted 28 June 2026), whose title page reads "Heidy Khlaaf, March 7, 2023 ... Recommended Citation: Khlaaf, Heidy. Toward Comprehensive Risk Assessments and Assurance of AI-Based Systems, Trail of Bits, 2023."
- **Claims:** Abstract: ODD "initially introduced for ADS (Automated Driving Systems)"; "the safety envelope for which system hazards and harms can be determined against". Section 4.1 cites NHTSA's ADS framework as the ODD source.

### Habli, I., et al. (2025). The BIG argument (arXiv:2503.11705)

- **How verified:** arXiv API abstract.
- **Claims:** "it is grounded in long-established safety norms and practices, such as being sensitive to context and maintaining risk proportionality."

### Feng, K. J. K., McDonald, D. W., & Zhang, A. X. (2025) (arXiv:2506.12469)

- **How verified:** arXiv API abstract.
- **Claims:** "an agent's level of autonomy can be treated as a deliberate design decision"; "five levels of escalating agent autonomy"; "AI autonomy certificates".

### Zietsman, C. (2026) (arXiv:2606.25120)

- **How verified:** arXiv API abstract (single author; 9 pages). Body not read.
- **Claims:** "context-bounded validity that triggers revalidation when operational context changes"; maps "DO-178C's traceability architecture, DO-330's requalification triggers". Note: the abstract also promotes a named framework ("PromptQ"); the paper cites only the mapping idea.

---

## Checked but not cited

- **UK CAA CAP3064A** (Part A: Strategy for Regulating AI and Advanced Automation in Aerospace, v1.3.2, 3 Dec 2024): page and PDF opened; judged marginal to the argument and dropped during trimming.
- **SAE J3016** (J3016_202104; SAE Mobilus page opened, which also lists a J3016_202609 revision dated 2026-09-20): the public abstract does not mention ODDs, so I could not verify that J3016 is the origin of the ODD concept. The paper attributes the ODD's origin to automated driving via Khlaaf (2023) and McDermid et al. (2024) instead.
- **Bainbridge (1983), "Ironies of automation"**: Crossref metadata confirmed, but no abstract or text was accessible; not cited.
- **Commission Implementing Regulation (EU) 2015/1998** (aviation security, threat image projection): EUR-Lex returned a challenge page and legislation.gov.uk did not serve the chapter; not cited. TIP is supported instead by Hofer and Schwaninger (2005).
- **EASA comment-response document for Proposed Issue 03**: only the comment template link was seen; EASA's responses were not found or read.
