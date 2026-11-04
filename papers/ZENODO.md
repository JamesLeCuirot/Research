# Zenodo upload sheet

Everything needed to publish each preprint on Zenodo (zenodo.org), so that each gets a permanent DOI under James's name and ORCID. Prepared 4 November 2026. Zenodo is CERN's free research repository. Its records are indexed by Google Scholar and OpenAIRE, can be added to ResearchGate by DOI, and can be pushed to ORCID automatically.

**Paper 07 is not listed:** it already has a DOI on OSF (10.17605/OSF.IO/DHF38). Add that DOI to ORCID and ResearchGate instead of creating a second record.

## Fields that are the same for every upload

| Field | Value |
|---|---|
| Resource type | Publication → Preprint |
| Creator | Le Cuirot, James · ORCID 0009-0009-6014-1298 · Affiliation: CitadelAero |
| Licence | **Creative Commons Attribution 4.0 International (CC BY 4.0)**, recommended. Every journal on the shortlist allows preprints, and CC BY is the usual licence for them. The alternative is to keep "all rights reserved", which matches the repository's current statement for paper text but limits reuse. |
| Publisher | Zenodo |
| Language | English |
| Related works | "Is supplemented by" → the paper's GitHub folder (URL below), resource type "Software" or "Dataset" as fits |
| Funding | None |

**Before publishing, use "Reserve DOI"** (the button on the upload form). It shows the DOI before the record goes live. Send it to me and I'll add it to the PDF and the README, rebuild, and you upload that PDF. Or publish as it is and the DOI is added in the next version. Both are fine.

**Rename each PDF on upload,** for example `LeCuirot-2026-just-culture-for-machines-v1.0.pdf`, so the file name says what it is.

## 01 Just Culture for Machines: Why Penalising Disclosure Teaches Concealment

| Field | Value |
|---|---|
| File to upload | `papers/01-just-culture-for-machines/paper.pdf` |
| Title | Just Culture for Machines: Why Penalising Disclosure Teaches Concealment |
| Version | Preprint v1.0 |
| Publication date | 2026-11-04 |
| Keywords | just culture; safety reporting; AI safety; reinforcement learning; chain-of-thought monitoring; AI alignment |
| Related work (is supplemented by) | https://github.com/JamesLeCuirot/Research/tree/main/papers/01-just-culture-for-machines |
| Notes | Prepared with AI assistance (Claude, Anthropic) under the author's direction, as stated in the paper. |

**Description** (paste into the description box):

> Aviation learned that when reports of error feed punishment, people stop reporting and the hazards stay hidden. Its protected arrangements, among them NASA’s Aviation Safety Reporting System, the FAA’s Aviation Safety Action Program and flight data programmes, EU Regulation 376/2014 and ICAO Annex 19, keep the data that safety programmes gather, whether reported or recorded, out of blame and enforcement, leave enforcement to independently obtained evidence, and exclude wilful misconduct and gross negligence from protection. This paper argues that AI training faces a similar incentive structure. When a model’s own disclosures (its chain of thought, self-reports or confessions) set the reward or penalty for the behaviour they disclose, optimisation acts on the disclosure as well as on the behaviour. A simple argument makes the conditions explicit: if the task reward does not already penalise a misbehaviour, and the model can pair it, at no cost in task reward, with a disclosure the monitor scores no worse than an honest one, then no penalty computed only from the disclosure can make good behaviour score higher than concealed misbehaviour. The argument concerns the ordering of rewards, not what training will reach, but experiments that trained reasoning models against chain-of-thought monitors observed the predicted concealment. OpenAI’s confession method, which rewards confessions only for honesty, is in effect a just-culture design. The paper proposes six design principles and five falsifiable predictions, and sets out where the analogy fails: models are not moral agents, and the mechanism is optimisation pressure rather than fear.

## 02 Do LLM Monitors Miss Rare Threats? A Pre-registered Test of the Low-Prevalence Effect

| Field | Value |
|---|---|
| File to upload | `papers/02-do-llm-monitors-miss-rare-threats/paper.pdf` |
| Title | Do LLM Monitors Miss Rare Threats? A Pre-registered Test of the Low-Prevalence Effect |
| Version | Preprint v1.0 |
| Publication date | 2026-11-04 |
| Keywords | AI control; LLM monitors; low-prevalence effect; signal detection theory; code backdoors; pre-registration |
| Related work (is supplemented by) | https://github.com/JamesLeCuirot/Research/tree/main/papers/02-do-llm-monitors-miss-rare-threats |
| Notes | Prepared with AI assistance (Claude, Anthropic) under the author's direction, as stated in the paper. |

**Description** (paste into the description box):

> AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to send the most suspicious items to a small human audit. Real attacks are expected to be rare. Human screeners miss rare targets far more often than common ones, mainly because they grow reluctant to say “yes”; airport security counters this with Threat Image Projection. A pre-registered experiment tested whether large language model (LLM) monitors show this low-prevalence effect. Two Claude models made 30880 judgements of Python solutions drawn from 379 execution-verified pairs of clean and backdoored code. The prediction failed in the opposite direction. In batches of 40, both monitors caught more backdoors when backdoors were rare: hit rates rose from 0.51 at 50 % prevalence to 0.69 at 2.5 % for Haiku, and from 0.50 to 0.74 for Sonnet (Holm-adjusted p = .0015 and p < .001), with false-alarm rates below 2 %. The decision criterion did not become more conservative. Single-item review caught about as many backdoors as 2.5 % batches, and more than 10 % and 50 % batches in three of four comparisons. Stating that about 1 in 100 submissions contained a backdoor, rather than about half, slightly lowered Sonnet’s single-item hit rate (0.85 to 0.78); Haiku’s change was not significant. A labelled calibration block modelled on Threat Image Projection did not reliably raise hit rates and more than doubled Sonnet’s false alarms. Rarity did not increase misses. Misses were more frequent when several backdoors shared a batch than when one did.

## 03 Applying Aviation Safety Management to Frontier AI: A Gap Analysis of Developer Safety Frameworks

| Field | Value |
|---|---|
| File to upload | `papers/03-from-rsp-to-sms/paper.pdf` |
| Title | Applying Aviation Safety Management to Frontier AI: A Gap Analysis of Developer Safety Frameworks |
| Version | Preprint v1.1 |
| Publication date | 2026-11-04 |
| Keywords | safety management systems; ICAO Annex 19; frontier AI; AI safety frameworks; safety performance indicators; AI governance |
| Related work (is supplemented by) | https://github.com/JamesLeCuirot/Research/tree/main/papers/03-from-rsp-to-sms |
| Notes | Prepared with AI assistance (Claude, Anthropic) under the author's direction, as stated in the paper. |

**Description** (paste into the description box):

> Frontier AI developers publish safety frameworks, such as Anthropic’s Responsible Scaling Policy, OpenAI’s Preparedness Framework and Google DeepMind’s Frontier Safety Framework. In 2026 Anthropic also published risk reports, incident investigations and monitoring statistics. Commercial aviation manages operational safety through the Safety Management System (SMS) defined in ICAO Annex 19: four components and twelve elements, run in practice on safety performance indicators, management of change, occurrence reporting and monitoring of routine operations. This paper maps the three frameworks, OpenAI’s companion compliance framework and Anthropic’s 2026 operational artefacts onto the twelve SMS elements, with the EU General-Purpose AI Code of Practice as a reference point, using documents public on 3 November 2026. The documents contain more SMS-like machinery than a reading of the headline frameworks alone suggests: hazard identification and risk acceptance throughout, incident response plans, security change management and audits, and security detection targets set as goals. The remaining gaps are specific. In the documents assessed, no developer publishes indicators with targets, alert levels and trends for its safety controls, such as monitors and classifiers. None documents a change process aimed at those controls’ settings with hazard assessment. None publishes an occurrence taxonomy or measures detection latency. Training for safety-assurance roles is not described, and independent assurance covers security controls more than safety controls in practice. Anthropic’s oversight metrics (coverage, review latency and escalation rate) are safety performance indicators in all but name. The paper proposes twelve AI safety performance indicators for testing and notes practices aviation could adopt. No prior element-by-element mapping was found.

## 04 Observing AI Systems in Normal Operations: What Aviation's Line Operations Safety Audit and Evidence-Based Training Offer AI Evaluation

| Field | Value |
|---|---|
| File to upload | `papers/04-checkride-or-jump-seat/paper.pdf` |
| Title | Observing AI Systems in Normal Operations: What Aviation's Line Operations Safety Audit and Evidence-Based Training Offer AI Evaluation |
| Version | Preprint v1.1 |
| Publication date | 2026-11-04 |
| Keywords | LOSA; evidence-based training; AI evaluation; evaluation awareness; competency-based assessment; AI safety |
| Related work (is supplemented by) | https://github.com/JamesLeCuirot/Research/tree/main/papers/04-checkride-or-jump-seat |
| Notes | Prepared with AI assistance (Claude, Anthropic) under the author's direction, as stated in the paper. |

**Description** (paste into the description box):

> *A conceptual mapping, two proposals and a feasibility pilot of competency-based grading.* Frontier language models can often tell when they are being evaluated, and in some studies they behave better when they say they are being tested. This threatens the validity of pre-deployment safety evaluations. Airline training faced a similar problem: a checkride shows what a crew does while being assessed. It developed two complementary answers. Line Operations Safety Audits (LOSA) put trained observers in the flight-deck jump seat on normal flights under confidential, non-jeopardy conditions, explicitly not as checks, and code threats, errors and undesired aircraft states. Evidence-based training (EBT) assesses competencies through observable behaviours across varied scenarios rather than a fixed list of manoeuvres, and requires assured instructor concordance. This paper maps their design principles onto alignment evaluation, records how far current AI practice already follows them, and states where the analogy fails. It proposes a “jump-seat” layer of privacy-preserving, non-jeopardy observation of deployed models and a competency-based alignment assessment, and shows how the two feed each other. A small feasibility pilot graded 48 model transcripts from six airline-workplace scenarios with an EBT-style rubric and with a single holistic score, by two LLM graders, twice each. Each grader’s two runs agreed at Krippendorff’s alpha 0.56–0.89, but every inter-grader alpha for the grades fell below 0.667, Krippendorff’s minimum for tentative conclusions, and the rubric showed no consistent advantage over the holistic score. Grades separated scenarios. Premature claims that actions had been taken lowered rubric communication grades but not holistic grades. Trained human instructors are the next test.

## 05 AI Control for Aviation: A Gap Analysis of EASA's Operational Oversight Objectives for Advanced AI

| Field | Value |
|---|---|
| File to upload | `papers/05-untrusted-by-design/paper.pdf` |
| Title | AI Control for Aviation: A Gap Analysis of EASA's Operational Oversight Objectives for Advanced AI |
| Version | Preprint v1.1 |
| Publication date | 2026-11-04 |
| Keywords | EASA; AI control; aviation regulation; runtime monitoring; AI assurance; certification |
| Related work (is supplemented by) | https://github.com/JamesLeCuirot/Research/tree/main/papers/05-untrusted-by-design |
| Notes | Prepared with AI assistance (Claude, Anthropic) under the author's direction, as stated in the paper. |

**Description** (paste into the description box):

> The European Union Aviation Safety Agency (EASA) is moving its guidance on artificial intelligence (AI) towards run-time oversight. Its draft Concept Paper, Proposed Issue 03 (June 2026), would place Level 3 (“advanced automation”) systems under an independent “operational oversight system” that monitors the AI, overrides it and drives it to a safe state (Objectives DHO-01 to DHO-07). In AI-safety terms this is a run-time monitor. Research on “AI control” has studied such monitors under a stricter assumption than aviation’s: that the monitored system may itself evade or subvert its monitor, collude with other AI components, or behave differently when evaluated. This paper compares the two. It sets out the EASA texts verbatim and shows that their threat model covers random and systematic failure, distribution shift and attackers external to the AI, but not the monitored system as a source of adversarial behaviour. It reviews experimental evidence, mostly from coding and AI-laboratory settings, that current large language models can evade monitors, recognise evaluations, agree with users against the facts and bias their labels when acting as judges. After a gap analysis of six threats, it proposes means of compliance for EASA and EUROCAE: a stricter, aviation-specific classification of monitors as trusted or untrusted, managed dissimilarity, red-team control evaluations, audit budgets sized with human-factors evidence, planted-test monitoring of monitors, sycophancy test methods and occurrence reporting of AI events. In the other direction, it argues that frontier-AI safety cases could adopt aviation’s severity-graded assurance, operational design domains, independent verification and continued airworthiness.

## 06 Extending AI-Agent Incident Analysis to Multi-Agent Systems: AFACS, an HFACS-Based Framework, and an Audit of Public Traces

| Field | Value |
|---|---|
| File to upload | `papers/06-afacs/paper.pdf` |
| Title | Extending AI-Agent Incident Analysis to Multi-Agent Systems: AFACS, an HFACS-Based Framework, and an Audit of Public Traces |
| Version | Preprint v1.1 |
| Publication date | 2026-11-04 |
| Keywords | HFACS; incident analysis; multi-agent systems; LLM agents; human factors; AI safety |
| Related work (is supplemented by) | https://github.com/JamesLeCuirot/Research/tree/main/papers/06-afacs |
| Notes | Prepared with AI assistance (Claude, Anthropic) under the author's direction, as stated in the paper. |

**Description** (paste into the description box):

> Ezell, Roberts-Gaal and Chan (2025) proposed a framework for analysing incidents involving AI agents. It treats single agents, does not distinguish deliberate departures from known requirements from errors, and has been illustrated on a public incident report but, as far as this study found, not used to code agent traces. This paper extends it to multi-agent systems using the structure of the Human Factors Analysis and Classification System (HFACS) from aviation. The extension, AFACS, adds a supervision tier, a coordination category and violations coded from behaviour with a graded statement of the evidence, and it states what evidence each layer needs. It is tested on the public MAST dataset of multi-agent traces. An audit finds duplicate and corrupt rows, an LLM judge that agrees with itself at a mean Cohen's κ of 0.43, and logs that record what the agents did but none of the system documentation needed to reconstruct a failure. In an AI pilot, Claude coded 250 failed traces three times. On the traces that both coders judged failed, layer presence agreed at κ 0.49–0.68 between two models and 0.64–0.70 between two runs of one model (individual codes 0.49 and 0.57), with supervision the least consistent layer. In the AI coding, supervision failures appear in about two-thirds of failures, coordination breakdowns in two-fifths and violations in 9–13%, rarely resting on the agent's own stated reasoning; MAST's "Disobey Task Specification" label mixes errors with violations. Checked against the frameworks' documentation and code, the annotator's design-level claims usually identified a real weakness but overstated it as an absence (7 of 24 confirmed in full, 2 contradicted): design causes need design evidence. Validation with human coders is planned.

## After uploading

1. **ORCID:** connect Zenodo to ORCID (Zenodo → Settings → Linked accounts → ORCID), or add each DOI in ORCID under Works → Add → Search & link → DataCite. Add the OSF DOI for paper 07 the same way.
2. **Google Scholar:** create a profile (scholar.google.com → My profile) and add the papers when they appear (usually days to a few weeks after publication).
3. **ResearchGate:** create an account as an independent researcher, then add each paper by its DOI, or upload the PDF.
4. **Tell me the DOIs.** I'll add them to each paper's README, `CITATION.cff` and the website.
