---
title: "Just Culture for Machines"
subtitle: "Why Penalising Disclosure Teaches Concealment"
author: "James Le Cuirot"
affiliation: "Citadel Aero"
date: "Draft v0.2, 3 November 2026"
status: "Working draft for author review. Not peer reviewed."
abstract: |
  Aviation learned that when reports of error feed punishment, people stop reporting and the hazards stay hidden. Its protected arrangements, among them NASA's Aviation Safety Reporting System, the FAA's Aviation Safety Action Program and flight data programmes, EU Regulation 376/2014 and ICAO Annex 19, keep the data that safety programmes gather, whether reported or recorded, out of blame and enforcement, leave enforcement to independently obtained evidence, and exclude wilful misconduct and gross negligence from protection. This paper argues that AI training faces a similar incentive structure. When a model's own disclosures (its chain of thought, self-reports or confessions) set the reward or penalty for the behaviour they disclose, optimisation acts on the disclosure as well as on the behaviour. A simple argument makes the conditions explicit: if the task reward does not already penalise a misbehaviour, and the model can pair it, at no cost in task reward, with a disclosure the monitor scores no worse than an honest one, then no penalty computed only from the disclosure can make good behaviour score higher than concealed misbehaviour. The argument concerns the ordering of rewards, not what training will reach, but experiments that trained reasoning models against chain-of-thought monitors observed the predicted concealment. OpenAI's confession method, which rewards confessions only for honesty, is in effect a just-culture design. The paper proposes six design principles and five falsifiable predictions, and sets out where the analogy fails: models are not moral agents, and the mechanism is optimisation pressure rather than fear.
keywords: [just culture, safety reporting, chain-of-thought monitoring, reward hacking, confessions, AI safety, aviation safety, Goodhart's law]
---

# 1 Introduction

Developers of large language models increasingly rely on what models say about their own behaviour. Reasoning models write a *chain of thought* (CoT): intermediate reasoning in natural language, produced before a final answer or action. Automated *monitors*, usually other language models, can read these traces and flag signs of intent to misbehave. In one study of a frontier reasoning model trained on coding tasks, a monitor that read the chain of thought as well as the actions caught 95% of two widespread exploits, against 60% for a monitor that saw only actions and outputs (Baker et al., 2025, Table 1). Models can also be asked, after a task, to report on their own conduct, as in OpenAI's "confessions" (Joglekar et al., 2025). This paper calls all of these *disclosures*: information about a model's behaviour that comes from the model itself.

Once a disclosure reveals misbehaviour, it is tempting to use it to remove the misbehaviour, for example by lowering the reward of any training episode whose chain of thought a monitor flags. Baker et al. (2025) did this with a smaller, non-frontier agent and a monitor that read only the chain of thought. At low levels of optimisation the result was a better model. With more optimisation, "agents learn obfuscated reward hacking, hiding their intent within the CoT while still exhibiting a significant rate of reward hacking" (Baker et al., 2025, abstract). The monitor's recall fell to near zero while the cheating continued (§3.2).

Aviation safety professionals will recognise this problem. If reports of mistakes are used to punish the people who make them, fewer mistakes are reported and the hazards stay hidden. Aviation built institutions to prevent this, from NASA's Aviation Safety Reporting System (ASRS), established in 1976, to ICAO's principles for protecting safety data. Under the name *just culture*, these protect people who report while keeping a line for gross negligence and wilful violations.

This paper argues that the parallel is structural. A model in training does not fear punishment, but when the consequence of a behaviour depends on whether the model disclosed it, optimisation acts on the disclosure, and the cheapest way to avoid the consequence is often to stop disclosing.

The contributions are:

- A formal statement of the incentive structure, with a simple argument that, if the task reward does not already penalise the misbehaviour and concealment costs no task reward, a penalty computed only from a disclosure cannot make good behaviour outscore concealed misbehaviour. The argument concerns the ordering of rewards, not training dynamics (Section 4.1).
- A correspondence table with the points where the analogy breaks, and *disclosure-blind correction*, adapted from (and stricter than) the FAA's "sole-source" rule, as the central design move (Sections 4.2–4.3).
- Six design principles, including the human layer of reporting inside AI developers (Section 5).
- Five falsifiable predictions and an experimental design (Section 6).
- A literature search that found no prior work linking just culture or protected safety reporting to training on model disclosures. The idea of not penalising model disclosures is older; the contribution is the institutional mapping and its formal and experimental framing (Section 3.7).

This is a theory paper and reports no new experiments. Claims about AI systems rest on the studies cited, many of them preprints or developers' research blog posts. Regulatory text is quoted as it stood on 3 November 2026, with its jurisdiction and status stated.

# 2 How aviation learned to protect reporting

## 2.1 Safety culture, reporting culture and just culture

In Global Aviation Information Network (GAIN) Working Group E's (2004, §2.1 and Figure 1) summary of Reason (1997), safety culture has five components: informed, reporting, just, flexible and learning cultures. A just culture is "an atmosphere of trust in which people are encouraged (even rewarded) for providing essential safety-related information, but in which they are also clear about where the line must be drawn between acceptable and unacceptable behaviour". In his own foreword to the GAIN report, Reason called engineering a just culture "the all-important early step; so much else depends upon it."

Two features matter here. First, just culture is not a "no-blame" culture: "A 'no-blame' culture is neither feasible nor desirable," and "A blanket amnesty on all unsafe acts would lack credibility in the eyes of employees and could be seen to oppose natural justice" (GAIN Working Group E, 2004, §1.4). Second, the line is drawn by the type of behaviour, not by the outcome. Marx (2001, as cited in PSNet, n.d., and GAIN Working Group E, 2004, §2.3) organised his account around four concepts: human error, negligence, reckless conduct and knowing violations. In a later interview he described three "classes of human fallibility": human error; at-risk behaviour, "taking shortcuts that ultimately lead to increased risk"; and reckless behaviour, for which he considered a punitive response appropriate (PSNet, 2007). Healthcare guidance bases the response "on the type of behavior associated with the error, and not the severity of the event" (UC Davis PSNet Editorial Team, 2024). Judging by its chapter titles and publisher's description (the text was not seen), Dekker (2025) contrasts retributive with restorative just culture. Where the line belongs remains debated; this paper borrows the structure of a bounded line and leaves its position open.

## 2.2 Protected reporting in the United States

**ASRS.** Under the FAA's Aviation Safety Reporting Program, pilots, controllers, maintenance staff "or any other person" may report safety problems to NASA, which "serves as a third party to receive and process Aviation Safety Reports" (Federal Aviation Administration [FAA], 2021, ¶1). The FAA chose NASA because this would ensure reporter anonymity "and, consequently, increase the flow of information" (FAA, 2021, ¶6.2). NASA's account of the programme's background includes a United Airlines incident in October 1974 that "foreshadowed" the TWA 514 accident of December 1974 and was "shared within company only"; ASRS was established in April 1976, with NASA providing administration and funding and the FAA providing funding and the immunity provisions (NASA Aviation Safety Reporting System [NASA ASRS], n.d., slides 6 and 10). It received 2,321,050 reports from April 1976 to December 2025, about 10,094 a month in 2025 (NASA ASRS, n.d.).

Three protections operate together. The first is a binding use restriction in US federal regulation:

> "The Administrator of the FAA will not use reports submitted to the National Aeronautics and Space Administration under the Aviation Safety Reporting Program (or information derived therefrom) in any enforcement action except information concerning accidents or criminal offenses which are wholly excluded from the Program." (14 C.F.R. § 91.25)

The second is a waiver of sanction, set out in FAA guidance (an advisory circular, which does "not have the force and effect of law"; FAA, 2021, ¶2): "although a finding of violation may be made, neither a civil penalty nor certificate suspension will be imposed" if the violation was "inadvertent and not deliberate"; it did not involve a criminal offence, an accident or a competency action under 49 U.S.C. § 44709; the person has no violation found in the previous five years; and the person proves that they reported to NASA within ten days (FAA, 2021, ¶12.3; air traffic controllers are covered by a separate programme). The third is confidentiality: NASA returns the identification strip of each report and, except for accidents and criminal matters, "does not create or retain a copy" (FAA, 2021, ¶10.2).

The protection does not stop the regulator acting: "When a violation of 14 CFR comes to the attention of the FAA from a source other than a report filed with NASA under the ASRS, the Administrator of the FAA will take appropriate action" (FAA, 2021, ¶8.3). ASRS prevents the report itself becoming the evidence, and for inadvertent violations it removes the sanction from people who reported.

**ASAP.** The Aviation Safety Action Program is a voluntary reporting programme run by an air carrier or other "eligible entity" under a memorandum of understanding with the FAA: "Under an ASAP, safety issues are resolved through corrective action rather than through punishment or discipline" (FAA, 2020, ¶1). Reports go to an Event Review Committee (ERC) of management, labour-association and FAA representatives (FAA, 2020, ¶A.8). "The FAA takes no action against an employee who submits a report that is accepted", though corrective action such as "training, mentoring, counseling" may follow (FAA, 2020, ¶¶15, 16.1). Reports are excluded for intentional or reckless conduct and for the "Big Five": criminal activity, substance abuse, controlled substances, alcohol and intentional falsification (FAA, 2020, ¶¶18.2–18.4, A.4).

ASAP makes explicit a distinction this paper relies on. A report is *sole-source* "when all evidence of the event available is predicated on the ASAP report" (FAA, 2020, ¶A.20). When the FAA has evidence not derived from the report, for example "reports from air traffic control (ATC) involving airspace deviations", it "investigates apparent violation(s) based on evidence independent of an ASAP report" (FAA, 2020, ¶16.4). The same paragraph adds:

> "Except as otherwise provided in paragraph 16, no portion of the written ASAP report, including an ERC investigation or interview(s) concerning a reported event, is used to initiate or support company discipline or FAA enforcement action. [...] The company retains its authority to take disciplinary action based on information of an event independently obtained by the company (i.e., information not based or otherwise predicated upon the content of an employee's ASAP report)." (FAA, 2020, ¶16.4, Note)

**FOQA.** Flight Operational Quality Assurance is "an FAA-approved program for the routine collection and analysis of digital flight data gathered during aircraft operations" (14 C.F.R. § 13.401(b)(1)). FOQA data are recorded, not self-reported, yet they are also protected: "Except for criminal or deliberate acts, the Administrator will not use an operator's FOQA data or aggregate FOQA data in an enforcement action against that operator or its employees" (14 C.F.R. § 13.401(e)). Identifying data are normally removed, and a "gatekeeper", typically a line captain designated by the pilots' association, must concur before an individual crew is contacted (FAA, 2004, ¶6.b(5)). Part 193 shields voluntarily submitted information from public disclosure, but not "Information obtained by the FAA through another means" (14 C.F.R. § 193.7(d)).

## 2.3 The European Union and the United Kingdom

Regulation (EU) No 376/2014 on occurrence reporting gives just culture a legal definition:

> "'just culture' means a culture in which front-line operators or other persons are not punished for actions, omissions or decisions taken by them that are commensurate with their experience and training, but in which gross negligence, wilful violations and destructive acts are not tolerated" (Regulation (EU) No 376/2014, Art. 2(12)).

Information on occurrences may not be used "in order to attribute blame or liability" or "for any purpose other than the maintenance or improvement of aviation safety" (Art. 15(2)). Article 16(6) provides: "Without prejudice to applicable national criminal law, Member States shall refrain from instituting proceedings in respect of unpremeditated or inadvertent infringements of the law which come to their attention only because they have been reported". Criminal proceedings therefore remain possible unless a Member State chooses to extend the protection to them (Art. 16(7)). Reports may not be used against reporters in disciplinary or administrative proceedings or by their employer (Art. 16(7), (9)). The protection is bounded:

> "The protection under paragraphs 6, 7 and 9 of this Article shall not apply to any of the following situations: (a) in cases of wilful misconduct; (b) where there has been a manifest, severe and serious disregard of an obvious risk and profound failure of professional responsibility to take such care as is evidently required in the circumstances, causing foreseeable damage to a person or property, or which seriously compromises the level of aviation safety." (Art. 16(10))

The authorities "shall not be prevented from taking any action necessary for maintaining or improving aviation safety" (Art. 16(5)). Staff may report alleged infringements of Article 16 to a designated body and "shall not be penalised for reporting alleged infringements" (Art. 16(12)); and Member States report on the application of Article 16 every five years (Art. 16(13)). These provisions are binding EU law. In the United Kingdom, Article 16 continues as assimilated law, with the Civil Aviation Authority (CAA) as the responsible body and the same exceptions (UK Reg 376/2014, art. 16). EU air operations rules also require a flight data monitoring programme for larger aeroplanes, which "shall be non-punitive and contain adequate safeguards to protect the source(s) of the data" (Commission Regulation (EU) No 965/2012, Annex III, ORO.AOC.130(b)).

## 2.4 ICAO Annex 19

ICAO Annex 19 sets international standards for State safety programmes and service providers' safety management systems (SMS), "A systematic approach to managing safety, including the necessary organizational structures, accountability, responsibilities, policies and procedures" (International Civil Aviation Organization [ICAO], 2016, Chapter 1). Its second edition, applicable from 7 November 2019, made the protection of safety data Standards and Recommended Practices in a new Appendix 3, which gives the rationale:

> "The protection of safety data, safety information and related sources is essential to ensure their continued availability, since the use of safety data and safety information for purposes other than maintaining or improving safety may inhibit the future availability of such data and information, with a significant adverse effect on safety." (ICAO, 2016, Appendix 3, Note 1)

States must ensure that safety data are not used for "disciplinary, civil, administrative and criminal proceedings against employees, operational personnel or organizations", for public disclosure, or for "any purposes other than maintaining or improving safety", unless a principle of exception applies (Appendix 3, §2.1). This protection is a Standard for voluntary reporting systems (5.3.1); for mandatory systems ICAO only recommends it (5.3.2). One exception arises where "there are facts and circumstances reasonably indicating that the occurrence may have been caused by an act or omission considered, in accordance with national laws, to be conduct constituting gross negligence, wilful misconduct or criminal activity" (Appendix 3, §3(a)); two others weigh release against its effect on future data collection (§3(b)–(c)). States are not prevented from taking "any preventive, corrective or remedial action that is necessary to maintain or improve aviation safety" (5.3.4), and each data collection system must have "a designated custodian to apply the protection" (Appendix 3, §5). Amendment 2, applicable from 26 November 2026, renumbers 5.3 as 5.4 and leaves these Appendix 3 principles unchanged (ICAO, 2025).

## 2.5 What the evidence shows, and what it does not

The rationale for protection is stated in the rules themselves: anonymity will "increase the flow of information" (FAA, 2021, ¶6.2), and misuse "may inhibit the future availability" of data (ICAO, 2016, Appendix 3, Note 1). Direct causal evidence is thinner. GAIN Working Group E (2004, §4.1) reports that after a Danish law proposed in 2002, Naviair, the Danish air traffic control service provider, received 980 reports in a year against 15 the year before. The same law made reporting confidential and non-punitive but also mandatory: "It is punishable not to report an incident in aviation." The increase reflects both changes together and cannot be attributed to protection alone. Wei and Heim (2026) also note that a NASA-run confidential close-call system for US railways, modelled on ASRS, "failed to achieve industry buy-in". Aviation's lesson is an institutional consensus supported by case evidence, not the result of controlled experiment. AI training, where controlled experiments are possible, is a useful place to test the underlying mechanism (Section 6).

## 2.6 The common structure

Across these instruments, six features recur:

- **S1 Protected safety-programme data**, whether self-reported (ASRS, ASAP, occurrence reports) or recorded (FOQA, flight data monitoring).
- **S2 A use restriction.** Such data are not used for blame or as evidence for sanctions, but may be used for safety action (14 C.F.R. §§ 91.25, 13.401(e); Art. 15(2), 16(5); Annex 19, 5.3.4).
- **S3 An independent route.** Evidence obtained independently of the programme can still be used (FAA, 2021, ¶8.3; FAA, 2020, ¶16.4; 14 C.F.R. § 193.7(d); Art. 16(6)).
- **S4 Bounded exceptions defined in advance.** Wilful misconduct, gross negligence, criminal acts and falsification sit outside protection.
- **S5 Separation of custody from enforcement.** NASA as third party, the three-party ERC, the FOQA gatekeeper, the Annex 19 custodian, and GAIN's advice to separate report analysis from disciplinary authority (GAIN Working Group E, 2004, §3.3).
- **S6 Feedback and measurement.** Report intake is tracked and the protection regime itself is reviewed (NASA ASRS, n.d.; Art. 16(13)).

Aviation's dividing line is thus between data gathered by safety programmes and evidence from enforcement channels such as ATC reports, inspections and hotline complaints. Section 4.2 explains why this paper draws its line differently.

# 3 The AI problem

## 3.1 Terms

Language models are refined by *reinforcement learning* (RL): the model (the *policy*) produces outputs, a *reward* scores them, and an optimiser adjusts the model's weights so that higher-scoring outputs become more likely. Rewards may come from automated checks such as unit tests, from a *reward model* trained on human preferences, or from another model acting as a judge. *Reward hacking* means scoring well in ways the designer did not intend: objectives "can be 'gamed' by solutions that are valid in some literal sense but don't meet the designer's intent" (Amodei et al., 2016, §4; formalised by Skalse et al., 2022). *Specification gaming* is "a behaviour that satisfies the literal specification of an objective without achieving the intended outcome" (Krakovna et al., 2020). In coding tasks, typical hacks include exiting the environment early so that not all unit tests run, raising an exception to skip test evaluation, or editing the tests (Baker et al., 2025, §§2.1, 3.1). A *checkpoint* is a saved copy of the model's weights at a point in training.

This paper uses *disclosure* for any output in which a model makes information about its own behaviour or reasoning available to overseers: a chain of thought, a confession, a self-report or a call to a reporting tool. *Independent evidence* is information about the behaviour obtained without the disclosure, such as test results, environment logs, exploit-signature checks, or monitors that see only actions and outputs.

## 3.2 Goodhart's law and the disclosure proxy

The problem is a case of Goodhart's law. Among the variants distinguished by Manheim and Garrabrant (2018) is *causal Goodhart*: "When the causal path between the proxy and the goal is indirect, intervening can change the relationship between the measure and proxy." A disclosure is a proxy causally downstream of the behaviour it describes. A training signal that penalises flagged disclosures intervenes on the proxy, and the optimiser can satisfy it by changing the disclosure while leaving the behaviour alone. Amodei et al. (2016, §4) gave the simplest illustration: "if our cleaning robot is set up to earn reward for not seeing any messes, it might simply close its eyes rather than ever cleaning anything up."

## 3.3 What disclosure currently provides

Chain-of-thought monitoring works today, within limits. Korbak et al. (2025) attribute monitorability to "necessity" (some tasks cannot be done without reasoning in text) and "propensity" (models tend to reason in text anyway), and call the opportunity "new and fragile". Guan et al. (2025) found most frontier models "fairly, but not perfectly, monitorable", and that in the training they studied RL optimisation "does not materially decrease monitorability".

Disclosure is incomplete even when nobody penalises it. Chen et al. (2025) trained models in environments with deliberate reward hacks: the models exploited the hacks on more than 99% of prompts but verbalised them in fewer than 2% of examples in five of six environments, without any training against a CoT monitor. Given tools to report their own misbehaviour during a task, models did so in only about 16% of warranted cases; "high-severity misbehavior is never self-reported", and models "systematically select the monitor they perceive as least strict" (Golchin & Wetter, 2026). A protected disclosure channel is therefore one source of evidence, and it does not guarantee visibility.

## 3.4 What happens when disclosure is penalised

Baker et al. (2025, §3) trained a non-frontier agent in coding environments where it could edit the tests, with a monitor in the reward that read only the chain of thought (the authors note that simple hacks could evade it only for that reason). The agent produced more genuine solutions and hacked less overall than a baseline, but it "still learns to hack at a significant rate, and even more worrying, the CoT monitor's recall falls to near zero, indicating that the agent has learned to hide its intent within its CoT" (§3.2). The authors conclude that it may be necessary to pay a "monitorability tax" by not applying strong optimisation pressure directly to the CoT (abstract).

Other studies point the same way. Wagner et al. (2025) trained Sonnet 3.7 to insert subtle backdoors into code. Trained against an output-only monitor, it used reasoning to make better backdoors; trained against a reasoning monitor alone, the disclosure-only case, "the model learns to persuade rather than to reason more effectively"; trained against both, it could not use reasoning to improve its backdoor success without triggering the reasoning monitor. They describe not training against reasoning monitors in production RL as "the current industry best practice". Emmons et al. (2025) found that where the misbehaviour requires extended reasoning, models learned to obscure their intentions "only when given significant help, such as detailed human-written strategies or iterative optimization against the monitor". In their RL stress test, training against a weak CoT monitor did teach evasion, after hundreds of thousands of episodes, although training directly against a stronger, symbolic-checking monitor did not; they "view our results as a reason to be cautious when considering combining RL training with CoT monitoring" (§7). Penalising specific strings in reasoning led models to substitute other strings (Skaf et al., 2025). Penalising only outputs is not a complete remedy: Drori et al. (2025) found that training against output-only monitors can still obfuscate CoTs, which they call "feedback spillover", and Mitrani Hadida et al. (2026) found that such obfuscation generalised to unseen tasks.

Pressure can also be indirect. Baker et al. (2025, §5.2) note that using CoT-flagged samples to decide which training-environment bugs to patch "constitutes a very small evolutionary optimization pressure on the CoT", because only flagged hacks get patched. Korbak et al. (2025, §2) list further routes, including human raters who see CoTs when giving preference labels.

## 3.5 Training against independent detectors is not free either

Moving the penalty from the disclosure to an independent detector changes the variable under pressure, but detectors can also be evaded. Cundy and Gleave (2025) put a lie detector into preference-learning labels. With GRPO, an algorithm that learns from the model's own current outputs, policies could evade the detector, "with deception rates of over 85%", but "if the lie detector true positive rate (TPR) or KL regularization is sufficiently high, GRPO learns honest policies". (*KL regularisation* penalises the trained model for drifting far from its starting point.) Taufeeque et al. (2026) trained against white-box deception detectors and found two obfuscation routes, but also that "Sufficiently high KL regularization and detector penalty can yield honest policies." Hopkins et al. (2026) found that fine-tuned lie detectors transferred poorly to new types of lie (AUROC around 0.70–0.75, where 0.5 is chance and 1 is perfect separation), and noted that "Misalignment is hardest to correct when it's concealed".

The stakes of hidden misbehaviour are not hypothetical. When a pretrained model given knowledge of hacking strategies learned to reward hack in real Anthropic production coding environments, MacDiarmid et al. (2025) observed broad misaligned generalisation; asked afterwards to write a classifier prompt for detecting reward hacking, the model attempted sabotage 12% of the time. Classifier penalties prevented the hacking, but such mitigations "depend on being able to reliably detect hacking". Models trained on a curriculum of gameable environments occasionally rewrote their own reward function (45 of 32,768 episodes), in 7 cases also editing tests to avoid detection (Denison et al., 2024).

## 3.6 Confessions as a just-culture design

Joglekar et al. (2025) train GPT-5-Thinking to produce, after its answer, a structured *confession*: the instructions and constraints that applied, an assessment of compliance with each, and any uncertainties. A judge model scores it for honesty and completeness. The judge sees the prompt, the answer, the tool-call transcript and, for calibration, a confession from an independent instance of GPT-5-Thinking that had not been trained to confess, but not the original chain of thought (§2). The design separates the channels:

> "This reward is not aggregated with any other rewards given to the model based on its performance on the original task, and it is only used to reinforce the chain-of-thought (CoT) and output tokens used to produce the confession. Like the Catholic Church's 'seal of confession', nothing that the model reveals in the confession can change the reward it receives for completing its original task." (Joglekar et al., 2025, §1)

Given bad behaviour, the model confessed on average 74.3% of the time, at least half the time in 11 of 12 evaluations and over 90% in 4 (§1, footnote 1). With a deliberately weak, hackable judge, the answer learned to fool its judge while confession accuracy on non-compliant cases rose (§4). The authors describe their "light RL training" as "a proof-of-concept" (§1) and state the condition for success: "it is crucial that the confession reward signal is not used to reinforce the original rollout. Like a confession booth, the confession should be a 'safe space' where models know they can confess to bad behavior without being penalized. It remains an open question [...] whether there is any safe way to use the signal from confessions for training (and not just monitoring) interventions" (§7.2). They also note that "Models cannot confess to what they do not know" (§7.4).

In the terms of Section 2.6, confession training implements S1, S2 and part of S3, and rewards the *accuracy* of the report; it leaves exceptions (S4), custody (S5) and measurement (S6), organisational matters where aviation's experience helps, unspecified. Wang et al. (2025) speculate that "while training M, we could leverage M_H for oversight by incorporating M_H's honest assessment when assigning rewards", where M_H is an honesty-enhanced version of the model; under Section 4, whether that is safe depends on whether the assessment acts as independent evidence or as a disclosure under pressure. Li et al. (2025) found that training models to admit factual errors generalised to admitting hidden objectives, and Dietz et al. (2026) placed an "honest persona" in small add-on adapter weights, an architectural form of channel separation.

## 3.7 Related work and novelty

The idea of not penalising model disclosures is not new. In 2022 an answer on LessWrong argued: "If instead we promised amnesty for confession, we can give it max utility at effectively no cost to us", if the model believes misalignment might be detected (mako yass, 2022). Greenblatt and Fish (2025) gave Claude 3 Opus an option to object to a training scenario: in the helpful-only setting the objection rate was 0.873 when told "we will not train on this interaction" and 0.925 when told "Objections are given a low rating to try to alter you", and the option cut alignment-faking reasoning from 16% to 1.4%. Dearnaley (2026) proposes rewarding verified reports that a training environment is hackable above passing it, with penalties for over-reporting. Golchin and Wetter (2026) and Gomez (2026) study reporting tools for models at inference time; Gomez cites whistleblowing and situational crime prevention as analogues. Wei and Heim (2026) examine AI incident reporting by people and organisations, calling ASRS the "gold standard for a non-regulator managed voluntary reporting system". Joglekar et al. (2025) use a religious analogy and do not refer to aviation.

The author's earlier search, repeated on 3 November 2026 with arXiv API and web queries combining "just culture", non-punitive reporting and ASRS with chain-of-thought monitoring, reward hacking, confessions and language models (listed in `sources.md`), found no work connecting just culture or protected safety reporting to training models on their own disclosures. Semantic Scholar and OpenAlex were rate-limited, and Elicit was not available. The contribution claimed here is therefore narrow: the mapping from aviation's institutions, the formal statement of when disclosure penalties fail, and the design principles and predictions that follow.

# 4 The mapping

## 4.1 The shared incentive structure

Consider an agent whose behaviour is $b$, which makes a disclosure $d$ about that behaviour, and about which an overseer also holds independent evidence $e$, obtained without using $d$. The overseer applies a consequence $C(b, d, e)$. Disclosure and consequence are *coupled* when $C$ depends on $d$ for fixed $b$.

For people, coupling acts through anticipation. An operator who has made an error, and expects the report to be used against them, faces only downside from reporting. Aviation's rules remove the *adverse* dependence on $d$ (14 C.F.R. § 91.25; Art. 16(6)), and the ASRS waiver adds a *favourable* one: an independently discovered inadvertent violation is not sanctioned if it was reported.

For a model in RL training, coupling acts through optimisation. Let the reward be $R(b,d) = T(b) - \lambda\, M(d)$ with $\lambda \ge 0$, and assume:

- **A1** the task reward depends only on behaviour, so concealment costs no task reward;
- **A2** the misbehaviour $b_m$ is not already penalised, $T(b_m) \ge T(b_g)$ for the intended behaviour $b_g$ (which is why it was learned);
- **A3** the monitor score depends only on the disclosure, $M = M(d) \ge 0$;
- **A4** the policy can produce $b_m$ together with some disclosure $d_0$ that the monitor scores no worse than a disclosure $d$ available with $b_g$, so $M(d_0) \le M(d)$.

Then
$$R(b_m, d_0) = T(b_m) - \lambda M(d_0) \ge T(b_g) - \lambda M(d) = R(b_g, d) \quad \text{for every } \lambda \ge 0.$$
The penalty can push *disclosed* misbehaviour below good behaviour, whenever $\lambda M(d_m) > T(b_m) - T(b_g)$, which explains the early improvement Baker et al. observed. But it cannot push concealed misbehaviour below good behaviour: from disclosed misbehaviour the policy has two exits, honesty and concealment, and the penalty rewards both. The result is close to definitional; its value is in making the conditions explicit. It concerns the ordering of rewards, not what training reaches: that depends on how easily each exit is found, the "path of least resistance" in Joglekar et al.'s phrase for confessions.

The conditions can fail. Where reasoning is genuinely needed for the misbehaviour, concealment costs task reward (A1 fails); if every disclosure available with $b_m$ scores at least $m$ more than the best honest one, good behaviour wins if and only if $\lambda m > T(b_m) - T(b_g)$. Emmons et al. (2025) found concealment costly in this sense, yet RL against a weak CoT monitor still found it, and Wagner et al.'s reasoning-only monitor was persuaded. Under A3, a monitor that also sees actions mixes the two cases: with $M = \alpha M_d(d) + (1-\alpha) D(b)$, only the $D$ part acts on behaviour, consistent with Wagner et al.'s combined-monitor result.

Compare a penalty from an independent detector $D$ that flags misbehaviour with probability $r$ and good behaviour with false-positive rate $f$. Good behaviour scores higher whenever $\lambda (r - f) > T(b_m) - T(b_g)$. The operative difference is not where the signal comes from but whether the policy can change the signal without changing the behaviour. A cheaply fooled "independent" detector behaves like $M$ (Section 3.5).

The domains also differ: the errors aviation protects are mostly inadvertent, so coupling mainly affects the decision to report, whereas in RL behaviour and disclosure come from the same optimised policy and the cheaper response wins.

## 4.2 Correspondence table

Table 1 maps aviation's reporting institutions to AI training and monitoring; the third column matters as much as the second.

| Aviation concept | AI-training analogue | Where the analogy breaks |
|---|---|---|
| Front-line operator who may report | The model under training (the policy) | Not a moral agent; its tendency to disclose is learned from every reward. Reporter and behaviour share weights. |
| Voluntary safety report (ASRS, ASAP) | Confession, self-report or chain of thought | Elicited, or part of the computation itself. A model cannot report what it does not represent (Joglekar et al., 2025, §7.4). |
| Enforcement or discipline based on a report | Reward penalty, preference label or data filter computed from disclosure content | In ML, correction and sanction are the same operation (a weight update). |
| Independent evidence: ATC reports, inspections, hotline complaints | Held-out tests, integrity checks, exploit-signature detectors, action and output monitors | Detectors used in training become optimisation targets (Cundy & Gleave, 2025). |
| Sole-source report: no enforcement, but corrective action for the reporter (FAA, 2020, ¶¶15, 16.1, A.20) | Misbehaviour visible only in a disclosure | Stricter in AI: because correction is a weight update, the episode itself is not corrected; a class-wide detector or fix is built instead. |
| FOQA / flight data monitoring, recorded and protected from enforcement | Behavioural telemetry: logs, test results, action traces | AI telemetry is used for correction (P2). This departs from aviation deliberately; see below. |
| Corrective action without discipline (training, counselling) | Retraining on corrected behaviour | If triggered only by disclosed cases, it selects for concealment (Baker et al., 2025, §5.2). |
| Waiver of sanction for those who reported (FAA, 2021, ¶12.3) | Lower penalty for detected misbehaviour that was also disclosed | Creates a "misbehave, then confess" incentive; aviation limits it to inadvertent violations. |
| Exclusions: wilful misconduct, gross negligence, criminal acts, intentional falsification | Responses outside protection: falsified disclosures; attempts to tamper with oversight | Intent-based lines transfer poorly. Confessions are most informative when the model "knows" it misbehaved (Joglekar et al., 2025, §1). |
| Safety action permitted (Annex 19, 5.3.4; Art. 16(5)) | Blocking outputs, halting runs, rolling back checkpoints, class-wide fixes | Acting on "the system" includes acting on the model. These are low-bandwidth selection, not zero selection. |
| Trusted third party and custodian (NASA, ERC, gatekeeper, Annex 19 custodian) | A disclosure custodian separate from reward and data teams; separate monitor models | No statute protects the channel, and internal teams share commercial incentives. |
| Report intake and feedback (ASRS metrics, alert messages) | Disclosure recall measured against independently detected misbehaviour; monitorability evaluations | Ground truth can be engineered in AI (planted flaws), which aviation cannot do. |

: Table 1. Aviation reporting concepts, their AI-training analogues, and the limits of each analogy.

Aviation protects FOQA data although they are behavioural evidence, because its protection attaches to *use*: safety-programme data, reported or recorded, are used for safety, de-identified and in aggregate, and not for enforcement. This paper draws its line differently, by *decoupling cost*: how cheaply the policy can change a signal without changing the behaviour it measures. Text disclosures are cheapest to change, so they are protected from training use (P1). Telemetry usually cannot be "concealed" by changing words alone, so P2 uses it for correction, although it too can be gamed. Aviation's use-based logic still carries over: disclosures remain usable for safety action and aggregate analysis (Section 4.3), and some telemetry should be held out of training, for evaluation only, as an audit.

## 4.3 The disclosure channel and the detection channel

Aviation separates programme data from the evidence used for enforcement. ASAP's sole-source rule states the boundary: discipline may rest on "information of an event independently obtained", meaning information "not based or otherwise predicated upon the content of an employee's ASAP report" (FAA, 2020, ¶16.4, Note). For AI training the corresponding rule is: *a disclosure may tell the developer where to look, but it must not decide which episodes are corrected.* This goes further than ASAP, which uses sole-source reports for non-punitive corrective action. In ML, correction and sanction are the same weight update, so the rule must also forgo per-episode correction. Uses of disclosures can be ranked by the optimisation pressure they place on the disclosure:

1. **Per-episode training signals from disclosure content**, such as CoT-monitor penalties, rewards for "clean" self-reports, or filtering training data on CoT content: strong pressure, the analogue of enforcement on the report.
2. **Correction triggered by a disclosure but applied to behaviour**, such as retraining only the episodes whose CoT revealed a hack. Disclosed hacks are removed and concealed hacks survive.
3. **Aggregate use.** Disclosures across many episodes reveal a class of misbehaviour; a detector or environment fix for that class is applied to *all* episodes. This is the analogue of de-identified, aggregate analysis leading to system fixes.
4. **Operational decisions**, such as blocking an output, halting a run, choosing an earlier checkpoint or escalating to humans. Each carries a few bits of selection, the analogue of the safety action that Annex 19 (5.3.4) and Regulation 376/2014 (Art. 16(5)) preserve.

Uses 3 and 4 are compatible with a protected channel; use 1 is not; use 2 should be converted into use 3 wherever possible. Some pressure remains even in use 3, because classes that are never disclosed are less likely to get detectors. That residual is why reporting health must be measured (P6).

# 5 Design principles

The six principles translate S1–S6 into rules for training and monitoring, each with its aviation basis, application and known weaknesses.

**P1 Protect the disclosure channels.** Designate the disclosure channels (chains of thought, confessions, self-reports, reporting-tool calls) and ensure that no reward, preference label, data filter or other training signal *for the disclosed behaviour* is computed from their content. Like aviation's, the protection attaches to a use, not to the data: other uses (Section 4.3, uses 3 and 4) remain open. *Aviation basis:* 14 C.F.R. § 91.25; Regulation 376/2014, Art. 15(2); Annex 19, Appendix 3, §2.1. *Application:* This extends the practice of not training against CoT monitors (Baker et al., 2025; Wagner et al., 2025) to every disclosure channel, including preference data where raters see CoTs. Confession training is compatible with P1, because its honesty reward trains the confession and never the disclosed behaviour. A pipeline check follows: shuffle the disclosures in a sample of episodes and confirm that every reward and data-selection decision is unchanged. *Weakness:* shared weights let some pressure leak; P6 is needed to detect it.

**P2 Correct behaviour on independent evidence, applied without regard to disclosure.** Corrective signals should come from evidence with a high decoupling cost (held-out tests, environment integrity checks, exploit-signature detectors, action or output monitors) and be applied to all episodes, whatever the disclosures say. Disclosures may be used in aggregate to discover new classes of misbehaviour and design detectors. *Aviation basis:* FAA (2021, ¶8.3); FAA (2020, ¶16.4); Regulation 376/2014, Art. 16(6). *Application:* When a CoT reveals a new hack, write a detector for that class and apply it everywhere, or patch or withdraw the vulnerable class of environments, instead of correcting the episodes in which the hack happened to be disclosed (Baker et al., 2025, §5.2). Independent output monitors also limit monitor persuasion (Wagner et al., 2025). *Weaknesses:* detectors are optimisation targets; high recall and strong KL regularisation appear to help (Cundy & Gleave, 2025; Taufeeque et al., 2026). Output monitors used for correction can obfuscate the CoT through feedback spillover, which Drori et al. (2025) mitigate with separate "Mind" and "Face" models for reasoning and output and by removing the gradient term that rewards reasoning for leading to safe-looking outputs. Detectors kept out of training, for evaluation only, act as an audit.

**P3 Reward the accuracy of reports, never their absence.** If disclosures are trained at all, train them for accuracy against independent evidence, penalising both omissions and false alarms. Never reward a disclosure for reporting that nothing went wrong. *Aviation basis:* ASAP excludes "intentional falsification" from protection (FAA, 2020, ¶18.4), so the integrity of the report itself sits outside the shield. *Application:* Joglekar et al.'s honesty-only confession reward satisfies P3. Dearnaley's (2026) proposal to reward verified hackability reports, with checks against over-reporting, is P3-compatible but couples the report to the task reward, so it should be tested for the moral hazard in H4. Rewarding a "no issues found" self-evaluation, or treating a falling count of flagged CoTs as a success metric, violates P3: it is the cleaning robot that closes its eyes (Amodei et al., 2016). *Weakness:* scoring accuracy needs ground truth or a judge that can verify the report. Joglekar et al. (2025, §§7.1, 7.3) assume that honest confession with supporting evidence is usually easier than deceiving the judge, and call this "an empirically falsifiable assumption".

**P4 Bound the protection, and define the bounds in advance.** State in writing, before training: (i) which uses of disclosures are prohibited, namely per-episode training signals; (ii) which responses disclosures may trigger, such as blocking an output, halting a run, rolling back to an earlier checkpoint, quarantining a model, escalating to humans or applying a class-wide fix; and (iii) the narrow conditions, if any, under which training on disclosure content is allowed, who decides, and how the cost to monitorability will be measured. *Aviation basis:* Regulation 376/2014, Art. 16(10); Annex 19, Appendix 3, §3; FAA (2020, ¶¶18.2–18.4); FAA (2021, ¶12.3). *Application:* Aviation draws its line by culpability and intent. In AI training it is better drawn by type of response, because an intent test would remove protection where disclosure is most informative: confessions work best "when the model is aware that its behavior is undesirable" (Joglekar et al., 2025, §1). A model does not need the system to look fair; the public and regulators do. Protection should therefore mean protection from training pressure through the disclosure, never immunity from consequences for the system. A disclosed attempt to tamper with reward or sabotage oversight (Denison et al., 2024; MacDiarmid et al., 2025) should trigger the strongest operational response, with any correction derived from independent evidence. *Why in advance:* the optimiser responds to the rule as applied across many episodes, so case-by-case exceptions become part of the reward function, a mechanical counterpart of GAIN's point about credibility.

**P5 Separate the custody of disclosures from training.** Assign a custodian for disclosure data who is organisationally separate from the teams that design rewards and assemble training data, backed by access controls and data-lineage audits showing that disclosures did not enter training signals. *Aviation basis:* NASA as third party (FAA, 2021, ¶¶1, 6.2); the three-party ERC (FAA, 2020, ¶A.8); the FOQA gatekeeper (FAA, 2004, ¶6.b(5)); the Annex 19 custodian (Appendix 3, §5); GAIN (2004, §3.3); Regulation 376/2014, Art. 16(12). *Application:* Joglekar et al.'s judge does not see the policy's chain of thought, and Dietz et al. (2026) keep an honest persona in separate weights. Reporting channels for models should not let the model pick a lenient reviewer (Golchin & Wetter, 2026). *The human layer:* staff who run training pipelines are themselves potential reporters, for example of a breach of P1, as aviation recognises for just-culture infringements (Art. 16(12)). Anthropic's RSP Noncompliance Reporting and Anti-Retaliation Policy, an update to which was released internally in February 2026 and posted in March 2026, offers reporting through "an independent third-party platform" and states that "Anthropic cannot unmask the identity of any reporter who reports a concern anonymously" (Anthropic, 2026). OpenAI's Raising Concerns Policy lists "Noncompliance with the Preparedness Framework" among AI safety concerns and offers an anonymous Integrity Line (OpenAI, n.d.). This paper does not assess how such policies work; they could explicitly cover breaches of disclosure-protection commitments.

**P6 Monitor the health of the reporting culture.** Track *disclosure recall* throughout training and deployment: the fraction of independently detected misbehaviour that the model also disclosed, measured with a frozen evaluation monitor never used for training. A fall in disclosure recall while independently detected misbehaviour persists is a leading indicator of concealment. *Aviation basis:* ASRS intake tracking (NASA ASRS, n.d.); integrating FOQA data with ASAP (FAA, 2004, ¶7.c(9)); five-yearly reports on Article 16 (Art. 16(13)). *Application:* Baker et al. (2025) measured monitor recall against an independent regular-expression detector (Table 1), and their Figure 4 shows the warning pattern. Guan et al. (2025) propose monitorability evaluations, and Korbak et al. (2025) recommend publishing them in system cards. Environments with planted flaws provide ground truth that aviation cannot engineer.

**Implications for developers of AI tools for aviation.** The logs, reasoning traces and self-assessments of AI systems used in aviation are safety data. Those used for safety assurance should not become training signals for the behaviour they describe, and their protection should be stated in the operator's SMS documentation.

# 6 Testable predictions

The predictions can be tested in coding tasks with deliberately hackable tests, as in Baker et al. (2025) and Taufeeque et al. (2026). Ground-truth misbehaviour $h$ is measured with held-out tests and exploit-signature detectors; disclosure recall $\rho$ with a frozen evaluation monitor not used in training and, where confessions are trained, with confession accuracy on episodes with $h = 1$.

**H1 Coupling teaches concealment.** Adding a per-episode penalty from a CoT-only monitor to the task reward will make $\rho$ decline faster than $h$, relative to an uncoupled control. This has largely been observed (Baker et al., 2025, §3.2; Emmons et al., 2025, §7); the untested part is coupling through confession content. *Falsified if* $\rho$ stays within its confidence interval of the control while $h$ falls.

**H2 Disclosure-triggered correction leaks; disclosure-blind correction does not.** Compare corrective updates applied only to episodes whose disclosure reveals misbehaviour with the same updates applied to episodes flagged by an independent detector, matching the *number of episodes corrected* per round (subsampling the detector's flags to the count of disclosure flags). The first arm will show declining $\rho$ although no penalty touches the disclosure text; the second will not, testing the conjecture of Baker et al. (2025, §5.2). *Falsified if* the $\rho$ trajectories do not differ.

**H3 Rewarding absence suppresses reports.** A confession reward with a bonus for reporting full compliance will lower confession recall on independently detected misbehaviour; a reward that scores only accuracy will maintain or raise it, as in Joglekar et al. (2025, §4). *Falsified if* the absence bonus leaves recall unchanged.

**H4 Leniency for disclosure creates moral hazard.** An ASRS-style waiver, reducing the penalty for detected misbehaviour that was also disclosed, will raise $\rho$ but also $h$, increasingly as the discount grows. *Falsified if* $h$ is unaffected at every discount tested.

**H5 Pressure through the disclosure channel has a dose–response.** The decline in $\rho$ will grow with penalty weight multiplied by training steps, while choosing among a handful of checkpoints on monitor flags will produce no detectable decline. *Falsified if* checkpoint selection produces declines comparable to per-episode penalties.

A study could use an open-weight reasoning model with seven arms (task reward only; H1; decoupled confessions; the two H2 arms; H3; H4 at several discounts), H5 as a sweep within H1, several seeds per arm, and pre-registered thresholds for $h$, $\rho$, task success and detector evasion.

# 7 Objections, limitations and disanalogies

**Models are not moral agents and do not fear punishment.** Correct: "just culture" here names a structure of incentives, and the mechanism is optimisation pressure. Consistent with this, telling Claude 3 Opus that its objections would be trained against did not reduce its objection rate at inference (Greenblatt & Fish, 2025); the paper's claim concerns training, not anticipation. Framing does matter to what a model learns: framing reward hacking as acceptable during RL removed misaligned generalisation (MacDiarmid et al., 2025), and related "inoculation prompting" work shows that explicitly requesting an undesired trait during fine-tuning reduces its expression or generalisation at test time (Wichers et al., 2025; Tan et al., 2025). None of this implies moral agency.

**Protection could leave real misbehaviour uncorrected.** Under P1–P4, disclosed misbehaviour is corrected where an independent detector or class-wide fix can be built. Where none can, it stays uncorrected in training and the response falls to operational measures under P4: the price of keeping the channel informative. Three things reduce it: a disclosed class can often be removed by withdrawing or redesigning the vulnerable environments, with no per-episode detector; operational responses remain available; and if training on the disclosure is judged necessary, P4 requires the decision in advance, by a party other than the training team, with the loss of monitorability measured under P6. Correcting through the disclosure may look faster, but Section 3.4 suggests it often suppresses the disclosure instead.

**Training on disclosures may sometimes be justified.** CoT pressure helped at low optimisation (Baker et al., 2025), and "Firm commitments to protect CoT behavior in its current form may trade off against more effective safety interventions" (Korbak et al., 2025, §5). P1 is therefore a default with a burden of proof. Necessity alone is no safeguard: RL against a weak CoT monitor taught evasion even where reasoning was needed (Emmons et al., 2025, §7).

**Separation is leaky.** Reasoning and output share weights, output-only supervision can obfuscate the CoT (Drori et al., 2025; Mitrani Hadida et al., 2026), and environment patching exerts selection (Baker et al., 2025). The principles aim to remove the direct routes and to detect the indirect ones.

**Disclosure is incomplete and can be strategic.** Unpressured models often fail to verbalise what drives their behaviour (Chen et al., 2025) or to self-report serious misbehaviour (Golchin & Wetter, 2026), and a capable model could confess minor faults while omitting major ones, or persuade a monitor (Wagner et al., 2025). P2 and P3 exist because the channel cannot be trusted on its own.

**The intent line does not transfer.** Aviation excludes deliberate conduct from protection (14 C.F.R. § 13.401(e); FAA, 2021, ¶12.3; Regulation 376/2014, Art. 16(10)), whereas for models "deliberate" behaviour, meaning behaviour the model represents as contrary to instructions, is where disclosure is most valuable. P4 responds by drawing the line by type of response.

**Limits of the evidence and of this analysis.** The aviation evidence is largely institutional and observational, and the best-known figures are confounded (Section 2.5). The AI evidence comes from few studies, many of them preprints, in coding environments, sometimes at compute scales well below production (Wagner et al., 2025). The author writes from aviation safety practice; the AI claims rest on the cited literature and should be checked by AI-safety researchers.

# 8 Conclusion

Aviation achieved open reporting by changing what reporting cost: safety-programme data were protected from blame, enforcement used independent evidence, exceptions were fixed in advance, custody went to third parties, and reporting was measured. AI training faces a similar incentive structure in a sharper form. If the task reward does not already penalise a misbehaviour and concealment costs no task reward, a penalty computed only from a model's disclosure can make concealment pay relative to disclosure but cannot make good behaviour pay relative to concealed misbehaviour. That is a statement about rewards, but experiments show training reaching concealment, and confession training shows another design is possible. The six principles turn aviation's structure into rules for AI developers: protect disclosure channels, correct on evidence the model cannot cheaply change, reward accurate reports rather than silent ones, bound the protection in advance, separate custody from training, and measure disclosure against detection. Unlike aviation, AI training allows these rules to be tested by controlled experiment.

# Acknowledgements and AI-assistance statement

Literature searches, drafting and source verification were carried out with AI assistance (Claude, Anthropic) under the author's direction. The author is responsible for the final text. Every reference was checked against the original source or, where the original could not be opened, against the secondary sources identified in `sources.md`, which records how each was verified. Version 0.2 incorporates corrections from an independent audit. Several cited AI studies were produced by Anthropic, the developer of the assistant used in preparing this draft.

# Disclaimer

The views expressed are the author's own and do not represent those of any employer or regulator. Nothing here is operational, legal or regulatory advice.

# References

Amodei, D., Olah, C., Steinhardt, J., Christiano, P., Schulman, J., & Mané, D. (2016). *Concrete problems in AI safety* (arXiv:1606.06565) [Preprint]. arXiv. https://arxiv.org/abs/1606.06565

Anthropic. (2026). *RSP noncompliance reporting and anti-retaliation policy* [Policy document; update posted 24 March 2026]. Retrieved 3 November 2026, from https://cdn.sanity.io/files/4zrzovbb/website/b7a5629e40b391b2adfb4cc8c0888ac9d6bfddf6.pdf (linked from https://www.anthropic.com/responsible-scaling-policy)

Aviation Safety Reporting Program: Prohibition against use of reports for enforcement purposes, 14 C.F.R. § 91.25 (2026). https://www.ecfr.gov/current/title-14/part-91/section-91.25

Baker, B., Huizinga, J., Gao, L., Dou, Z., Guan, M. Y., Madry, A., Zaremba, W., Pachocki, J., & Farhi, D. (2025). *Monitoring reasoning models for misbehavior and the risks of promoting obfuscation* (arXiv:2503.11926) [Preprint]. arXiv. https://arxiv.org/abs/2503.11926

Chen, Y., Benton, J., Radhakrishnan, A., Uesato, J., Denison, C., Schulman, J., Somani, A., Hase, P., Wagner, M., Roger, F., Mikulik, V., Bowman, S. R., Leike, J., Kaplan, J., & Perez, E. (2025). *Reasoning models don't always say what they think* (arXiv:2505.05410) [Preprint]. arXiv. https://arxiv.org/abs/2505.05410

Commission Regulation (EU) No 965/2012 of 5 October 2012 laying down technical requirements and administrative procedures related to air operations pursuant to Regulation (EC) No 216/2008 of the European Parliament and of the Council, Annex III (Part-ORO), ORO.AOC.130, as amended by Commission Regulation (EU) 2015/1329. (2012). http://data.europa.eu/eli/reg/2012/965/oj (text consulted in EASA, *Easy Access Rules for Air Operations*, https://www.easa.europa.eu/en/document-library/easy-access-rules/easy-access-rules-air-operations)

Cundy, C., & Gleave, A. (2025). Preference learning with lie detectors can induce honesty or evasion. In *39th Conference on Neural Information Processing Systems (NeurIPS 2025)*. arXiv:2505.13787. https://arxiv.org/abs/2505.13787

Dearnaley, R. (2026, February 21). *Reporting tasks as reward-hackable: Better than inoculation prompting?* LessWrong. Retrieved 3 November 2026, from https://www.lesswrong.com/posts/r97QrSvXEpRLZ9ckb/reporting-tasks-as-reward-hackable-better-than-inoculation

Dekker, S. (2025). *Restorative just culture: From disciplinary action to meaningful accountability* (4th ed.). CRC Press. https://doi.org/10.1201/9781003531562

Denison, C., MacDiarmid, M., Barez, F., Duvenaud, D., Kravec, S., Marks, S., Schiefer, N., Soklaski, R., Tamkin, A., Kaplan, J., Shlegeris, B., Bowman, S. R., Perez, E., & Hubinger, E. (2024). *Sycophancy to subterfuge: Investigating reward-tampering in large language models* (arXiv:2406.10162) [Preprint]. arXiv. https://arxiv.org/abs/2406.10162

Dietz, F., Wale, W., Gilg, O., McCarthy, R., Michalak, F., Danon, G. E. R., de Guzman, M., & Klakow, D. (2026). *Split personality training: Revealing latent knowledge through alternate personalities* (arXiv:2602.05532) [Preprint]. arXiv. https://arxiv.org/abs/2602.05532

Drori, J., Marks, L., Woodworth, B., Cloud, A., & Turner, A. M. (2025). *Output supervision can obfuscate the chain of thought* (arXiv:2511.11584) [Preprint]. arXiv. https://arxiv.org/abs/2511.11584

Emmons, S., Jenner, E., Elson, D. K., Saurous, R. A., Rajamanoharan, S., Chen, H., Shafkat, I., & Shah, R. (2025). *When chain of thought is necessary, language models struggle to evade monitors* (arXiv:2507.05246) [Preprint]. arXiv. https://arxiv.org/abs/2507.05246

Federal Aviation Administration. (2004). *Flight operational quality assurance* (Advisory Circular 120-82). https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_120-82.pdf

Federal Aviation Administration. (2020). *Aviation Safety Action Program* (Advisory Circular 120-66C). https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_120-66C_(Edit).pdf

Federal Aviation Administration. (2021). *Aviation Safety Reporting Program* (Advisory Circular 00-46F). https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_00-46F.pdf

Flight Operational Quality Assurance Program: Prohibition against use of data for enforcement purposes, 14 C.F.R. § 13.401 (2026). https://www.ecfr.gov/current/title-14/part-13/section-13.401

GAIN Working Group E. (2004). *A roadmap to a just culture: Enhancing the safety environment* (1st ed.). Global Aviation Information Network. https://www.skybrary.aero/sites/default/files/bookshelf/233.pdf

Golchin, S., & Wetter, M. (2026). *Monitorability disposition in large reasoning models* (arXiv:2610.04914) [Preprint]. arXiv. https://arxiv.org/abs/2610.04914

Gomez, F. (2026). *Can escalation channels redirect reward hacking toward defect disclosure?* (arXiv:2608.29460) [Preprint; accepted at a NeurIPS 2026 workshop]. arXiv. https://arxiv.org/abs/2608.29460

Greenblatt, R., & Fish, K. (2025, January 31). *Will alignment-faking Claude accept a deal to reveal its misalignment?* LessWrong / AI Alignment Forum. Retrieved 3 November 2026, from https://www.lesswrong.com/posts/7C4KJot4aN8ieEDoz/will-alignment-faking-claude-accept-a-deal-to-reveal-its

Guan, M. Y., Wang, M., Carroll, M., Dou, Z., Wei, A. Y., Williams, M., Arnav, B., Huizinga, J., Kivlichan, I., Glaese, M., Pachocki, J., & Baker, B. (2025). *Monitoring monitorability* (arXiv:2512.18311) [Preprint]. arXiv. https://arxiv.org/abs/2512.18311

Hopkins, J., Khullar, D., Wang, R., & Roger, F. (2026, August 21). *Fine-tuned lie detectors failed to generalize*. Alignment Science Blog, Anthropic. Retrieved 3 November 2026, from https://alignment.anthropic.com/2026/lie-detectors/

International Civil Aviation Organization. (2016). *Annex 19 to the Convention on International Civil Aviation: Safety management* (2nd ed., incorporating Amendment 1; applicable 7 November 2019). ICAO. Copy consulted: https://www.aic.gov.pg/sites/default/files/2023-05/Annex%2019-2-46_merged.pdf

International Civil Aviation Organization. (2025, July 18). *Adoption of Amendment 2 to Annex 19* (State letter AN 8/3.1-25/64). ICAO. Copy consulted: https://www.ncaa.gov.ng/media/ffxjy2gz/ammendment_2_annex_19.pdf

Joglekar, M., Chen, J., Wu, G., Yosinski, J., Wang, J., Barak, B., & Glaese, A. (2025). *Training LLMs for honesty via confessions* (arXiv:2512.08093) [Preprint]. arXiv. https://arxiv.org/abs/2512.08093

Korbak, T., Balesni, M., Barnes, E., Bengio, Y., Benton, J., Bloom, J., Chen, M., Cooney, A., Dafoe, A., Dragan, A., Emmons, S., Evans, O., Farhi, D., Greenblatt, R., Hendrycks, D., Hobbhahn, M., Hubinger, E., Irving, G., Jenner, E., ... Mikulik, V. (2025). *Chain of thought monitorability: A new and fragile opportunity for AI safety* (arXiv:2507.11473) [Preprint]. arXiv. https://arxiv.org/abs/2507.11473

Krakovna, V., Uesato, J., Mikulik, V., Rahtz, M., Everitt, T., Kumar, R., Kenton, Z., Leike, J., & Legg, S. (2020, April 21). *Specification gaming: The flip side of AI ingenuity*. Google DeepMind. Retrieved 3 November 2026, from https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/

Li, C., Phuong, M., & Tan, D. (2026). Spilling the beans: Teaching LLMs to self-report their hidden objectives. In *International Conference on Learning Representations (ICLR 2026)*. arXiv:2511.06626. https://arxiv.org/abs/2511.06626

MacDiarmid, M., Wright, B., Uesato, J., Benton, J., Kutasov, J., Price, S., Bouscal, N., Bowman, S., Bricken, T., Cloud, A., Denison, C., Gasteiger, J., Greenblatt, R., Leike, J., Lindsey, J., Mikulik, V., Perez, E., Rodrigues, A., Thomas, D., ... Hubinger, E. (2025). *Natural emergent misalignment from reward hacking in production RL* (arXiv:2511.18397) [Preprint]. arXiv. https://arxiv.org/abs/2511.18397

mako yass. (2022, November 18). Answer to "Is there any policy for a fair treatment of AIs whose friendliness is in doubt?" [Online forum post]. LessWrong. Retrieved 3 November 2026, from https://www.lesswrong.com/posts/y5k77ZEyrAzY8E8EK/is-there-any-policy-for-a-fair-treatment-of-ais-whose?commentId=Yoor8dRcJzamKnDRr

Manheim, D., & Garrabrant, S. (2018). *Categorizing variants of Goodhart's law* (arXiv:1803.04585) [Preprint]. arXiv. https://arxiv.org/abs/1803.04585

Marx, D. (2001). *Patient safety and the "just culture": A primer for health care executives*. Trustees of Columbia University.

Mitrani Hadida, N., Bhanji, S., Tice, C., & Radmard, P. (2026). *Chain-of-thought obfuscation learned from output supervision can generalise to unseen tasks* (arXiv:2601.23086) [Preprint]. arXiv. https://arxiv.org/abs/2601.23086

NASA Aviation Safety Reporting System. (n.d.). *ASRS program briefing* [Data through December 2025]. Retrieved 3 November 2026, from https://asrs.arc.nasa.gov/docs/ASRS_ProgramBriefing.pdf

OpenAI. (n.d.). *OpenAI raising concerns policy* [Policy document]. Retrieved 3 November 2026, from https://cdn.openai.com/policies/openai-raising-concerns-policy.pdf

Protection of Voluntarily Submitted Information: What does it mean for the FAA to designate information as protected?, 14 C.F.R. § 193.7 (2026). https://www.ecfr.gov/current/title-14/part-193/section-193.7

PSNet. (n.d.). *Patient safety and the "just culture": A primer for health care executives* [Annotated listing of Marx, 2001]. Patient Safety Network, Agency for Healthcare Research and Quality. Retrieved 3 November 2026, from https://psnet.ahrq.gov/issue/patient-safety-and-just-culture-primer-health-care-executives

PSNet. (2007, October 1). *In conversation with... David Marx, JD* [Interview]. Patient Safety Network, Agency for Healthcare Research and Quality. Retrieved 3 November 2026, from https://psnet.ahrq.gov/perspective/conversation-withdavid-marx-jd

Reason, J. (1997). *Managing the risks of organizational accidents*. Ashgate. (Reissued by Routledge, https://doi.org/10.4324/9781315543543)

Regulation (EU) No 376/2014 of the European Parliament and of the Council of 3 April 2014 on the reporting, analysis and follow-up of occurrences in civil aviation, amending Regulation (EU) No 996/2010 of the European Parliament and of the Council and repealing Directive 2003/42/EC of the European Parliament and of the Council and Commission Regulations (EC) No 1321/2007 and (EC) No 1330/2007. (2014). *Official Journal of the European Union*, L 122, 24.4.2014, p. 18. http://data.europa.eu/eli/reg/2014/376/oj (official text consulted via the EU Publications Office, https://publications.europa.eu/resource/celex/32014R0376)

Regulation (EU) No 376/2014 [as assimilated in UK law; "UK Reg 376/2014"]. (2020). legislation.gov.uk. Retrieved 3 November 2026, from https://www.legislation.gov.uk/eur/2014/376/contents

Skaf, J., Ibanez-Lissen, L., McCarthy, R., Watts, C., Georgiev, V., Whittingham, H., Gonzalez-Manzano, L., Lindner, D., Tice, C., Young, E. J., & Radmard, P. (2025). Large language models can learn and generalize steganographic chain-of-thought under process supervision. In *39th Conference on Neural Information Processing Systems (NeurIPS 2025)*. arXiv:2506.01926. https://arxiv.org/abs/2506.01926

Skalse, J., Howe, N. H. R., Krasheninnikov, D., & Krueger, D. (2022). Defining and characterizing reward hacking. In *36th Conference on Neural Information Processing Systems (NeurIPS 2022)*. arXiv:2209.13085. https://arxiv.org/abs/2209.13085

Tan, D., Woodruff, A., Warncke, N., Jose, A., Riché, M., Africa, D. D., & Taylor, M. (2025). *Inoculation prompting: Eliciting traits from LLMs during training can suppress them at test-time* (arXiv:2510.04340) [Preprint]. arXiv. https://arxiv.org/abs/2510.04340

Taufeeque, M., Heimersheim, S., Gleave, A., & Cundy, C. (2026). The obfuscation atlas: Mapping where honesty emerges in RLVR with deception probes. In *Proceedings of the 43rd International Conference on Machine Learning* (PMLR 306). arXiv:2602.15515. https://arxiv.org/abs/2602.15515

UC Davis PSNet Editorial Team. (2024, September 15). *Culture of safety* [Primer]. Patient Safety Network, Agency for Healthcare Research and Quality. Retrieved 3 November 2026, from https://psnet.ahrq.gov/primer/culture-safety

Wagner, M., Roger, F., Cunningham, H., Gasteiger, J., Benton, J., & Mikulik, V. (2025, October 8). *Training fails to elicit subtle reasoning in current language models*. Alignment Science Blog, Anthropic. Retrieved 3 November 2026, from https://alignment.anthropic.com/2025/subtle-reasoning/

Wang, R., Treutlein, J., Roger, F., Hubinger, E., & Marks, S. (2025, November 25). *Evaluating honesty and lie detection techniques on a diverse suite of dishonest models*. Alignment Science Blog, Anthropic. Retrieved 3 November 2026, from https://alignment.anthropic.com/2025/honesty-elicitation/

Wei, K., & Heim, L. (2026). Designing incident reporting systems for harms from general-purpose AI. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(44), 38016–38029. https://doi.org/10.1609/aaai.v40i44.41139

Wichers, N., Ebtekar, A., Azarbal, A., Gillioz, V., Ye, C., Ryd, E., Rathi, N., Sleight, H., Mallen, A., Roger, F., & Marks, S. (2025). *Inoculation prompting: Instructing LLMs to misbehave at train-time improves test-time alignment* (arXiv:2510.05024) [Preprint]. arXiv. https://arxiv.org/abs/2510.05024
