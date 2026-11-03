# Independent audit: *Just Culture for Machines* (paper.md, draft v0.1)

Audit date: 3 November 2026. Scope: every reference, every specific claim attributed to a source, the formal argument in §4.1, novelty, internal consistency. `paper.md` was not edited. `sources.md` was used only to locate sources; every check below was redone from the source itself.

**Method.** arXiv API metadata for all 22 arXiv references and full-text PDFs for all of them (text extracted with pypdf). Anthropic blog posts and the RSP policy PDF downloaded directly. Crossref for Dekker and Reason DOIs. Citadel Aero regulation library for 14 CFR 91.25, 13.401, 193.7, AC 00-46F, AC 120-66C, UK Reg 376/2014 art. 16 and ORO.AOC.130; FAA AC PDFs also downloaded from faa.gov to confirm paragraph numbering; eCFR structure API for the Part 13 subpart. **EU Regulation 376/2014 primary text was obtained from the EU Publications Office (Cellar, CELEX 32014R0376, Official Journal L 122/18 of 24.4.2014)**; EUR-Lex itself returned empty HTTP 202 as reported in `sources.md`. ICAO Annex 19 (2nd ed.) from the AIC Papua New Guinea copy; Amendment 2 state letter from the NCAA Nigeria copy; GAIN Roadmap from SKYbrary; NASA ASRS Program Briefing from asrs.arc.nasa.gov (slides 6 and 10 rendered as images). Novelty: arXiv API searches, web searches, Alignment Forum/LessWrong pages.

---

## 1. Summary counts

| Category | Count |
|---|---|
| References checked | 44 of 44 |
| References verified without issue | 36 |
| References with bibliographic issues (label, DOI, author spelling, URL, OJ citation) | 8 |
| Primary text not accessible to the auditor | 3 (Marx 2001; Reason 1997; Dekker 2025 beyond table of contents). ICAO official copy not used; third-party copies were. |
| Source-attributed specific claims checked | 104 |
| VERIFIED (3 of these only via disclosed secondary sources) | 94 |
| WRONG | 2 |
| OVERSTATED or materially incomplete | 7 |
| NOT ACCESSIBLE (content could not be checked beyond ToC) | 1 |
| Paper's own argumentative claims assessed (formal argument, novelty, internal consistency) | 7, of which 5 need rewording |
| **Issues raised** | **44: 7 major, 16 moderate, 21 minor** |

---

## 2. Most important required fixes (in priority order)

1. **M1 Formal claim stated without its conditions** in the abstract, the §1 contribution bullet and §8. Add "the task reward does not already penalise the misbehaviour" and "concealment costs no task reward", define "compatible", generalise M(d₀)=0 to "no worse than an honest disclosure", and say it is a statement about reward ordering, not training dynamics. Wording in §4 below.
2. **M2 Emmons et al. (2025) is used against its own finding.** Their "significant help" explicitly includes "iterative optimization against the monitor", and their RL stress test (§7) *did* teach evasion of a CoT monitor. §3.3, §4.1 and §7 must say so.
3. **M3 The Danish 15→980 figure is confounded.** The same 2002 law made reporting *mandatory* ("It is punishable not to report an incident in aviation", GAIN §4.1). Saying "without a control group" is not enough.
4. **M4 Art. 16(6) is quoted without its opening words** "Without prejudice to applicable national criminal law". This carve-out (criminal proceedings stay possible) is central for aviation readers.
5. **M5 §7 overclaims that "disclosed misbehaviour is corrected"** under P1–P4. Misbehaviour visible only in a disclosure, for which no independent detector or class-wide fix can be built, is *not* corrected in training. State the trade-off honestly.
6. **M6 FOQA inconsistency.** S1 treats FOQA/FDM as a protected disclosure channel, but its AI analogue (behavioural telemetry) is classed as independent evidence and used for correction (P2, Table 1). Aviation protects FOQA *although* it is behavioural evidence. The paper's dividing line (disclosure vs independent evidence) is not aviation's line (safety-programme data vs enforcement evidence). Say this explicitly.
7. **M7 Related work missing:** Greenblatt & Fish (2025), which compared prompts telling the model its objections would or would not be trained against; amnesty-for-confession (LessWrong, 2022); Golchin & Wetter (2026, arXiv:2610.04914) on self-reporting through monitoring tools; and Dearnaley (2026). The narrow "just culture" novelty claim still holds. But the paper must not imply that the idea of protecting model disclosures is new.
8. **m1 Joglekar et al. described wrongly:** the judge's calibration confession comes from "an independent, non-confession-trained instance of GPT-5-Thinking", not "a separate untrained model".
9. **m3 NASA ASRS history:** the slide's timeline does not "begin with" the October 1974 United incident. It begins with WW II and 1958.
10. **m5 and m6:** Annex 19's Appendix 3 protection is a Standard only for *voluntary* systems (5.3.1); for mandatory systems it is a Recommendation (5.3.2). The inoculation-prompting sentence in §7 misattributes the finding to Wichers et al. and Tan et al.

---

## 3. Issue table

Severity: **MAJOR** (must fix before circulation), **MOD** (should fix), **minor**. Class: WRONG / OVERSTATED / UNSUPPORTED / INCONSISTENT / STYLE / BIB.

| ID | Sev. | Class | Location / quote | Problem | Evidence (source, locator) | Required fix |
|---|---|---|---|---|---|---|
| M1 | MAJOR | OVERSTATED | Abstract: "A simple argument shows that, where concealment is possible, a penalty computed only from a disclosure can never make good behaviour outscore concealed misbehaviour"; §1 bullet 1; §8 "can never make good behaviour pay relative to concealed misbehaviour" | The derivation in §4.1 is valid but rests on four assumptions. These summary sentences state only one: (A1) task reward independent of the disclosure, i.e. concealment costless; (A2) T(b_m) ≥ T(b_g); (A3) the monitor reads only d; (A4) a d₀ achievable together with b_m and scoring no worse than an honest disclosure. "Compatible with b_m" is undefined. The result concerns reward ordering, not what training reaches. | paper.md §4.1 itself; Baker et al. §3.2 (monitor saw CoT only) | Use the wording in §4 of this audit. In the abstract, add at least "and costs no task reward, and the task reward does not already penalise the misbehaviour". |
| M2 | MAJOR | OVERSTATED (misleading use) | §3.3 "models learned to obscure their intentions only 'when given significant help'"; §4.1 "the conclusion weakens (Emmons et al., 2025 …)"; §7 "evasion appears harder (Emmons …)" | The quote is verbatim but truncated. Emmons continue "such as detailed human-written strategies **or iterative optimization against the monitor**". Their Table 1 reports that RL against the monitor succeeded ("Yes, after 1,000s of RL steps"). They write: "we view our results as a reason to be cautious when considering combining RL training with CoT monitoring." Training against the monitor is exactly the paper's scenario. | arXiv:2507.05246 abstract; Table 1; §7 (pp. 20–26) | Add: "such as … iterative optimisation against the monitor; in their RL stress test, training against a CoT monitor did teach evasion, although it took many episodes and failed against a stronger symbolic monitor (§7)". Reword §4.1 and §7 accordingly. |
| M3 | MAJOR | OVERSTATED | §2.5 "980 reports against 15 … This is a before-and-after comparison without a control group"; P6 aviation basis | The same law made reporting **mandatory** with a penalty for not reporting, and also confidential and non-punitive. The increase cannot be attributed to protection alone. | GAIN (2004) §4.1: "Mandatory: Air Traffic Controllers must submit reports of events. It is punishable not to report an incident in aviation." | Add: "The same law also made reporting mandatory, with a penalty for not reporting, so the increase reflects both changes together." |
| M4 | MAJOR | OVERSTATED (omission) | §2.3 Member States "shall refrain from instituting proceedings … only because they have been reported" (Art. 16(6)); §2.6 S3; §4.1 "Aviation's rules remove the dependence on d (… Art. 16(6))" | The paragraph opens "Without prejudice to applicable national criminal law". The protection does not bar criminal proceedings under national law. That is a well-known limit of the EU regime. | Reg. 376/2014, Art. 16(6), OJ L 122, 24.4.2014, p. 18 (Cellar text); UK art. 16(6) same (library `uk:uk-reg-376-2014:article-16`) | Quote from "Without prejudice to applicable national criminal law, …" or state the carve-out in the next sentence. |
| M5 | MAJOR | OVERSTATED (paper's own claim) | §7 "Under P1–P4, disclosed misbehaviour is corrected through independent detection and class-wide fixes" | Under Table 1's sole-source row and P2, misbehaviour visible only in a disclosure is *not* corrected per episode. If no detector or class-wide fix can be built, it stays uncorrected in training. That is the real cost of the design. | paper.md Table 1 (sole-source row), §4.3 use 2 → 3, P2 | Replace with: "… is corrected where an independent detector or class-wide fix can be built. Where none can, the protection leaves that misbehaviour uncorrected in training and the response falls to operational measures under P4. That is the price of keeping the channel informative." |
| M6 | MAJOR | INCONSISTENT | §2.6 S1 lists "FOQA/flight data monitoring" as "A designated disclosure channel"; Table 1 FOQA row; §3.1 defines environment logs and action monitors as independent evidence; P2 corrects on them | FOQA is not a self-disclosure. It is automatically recorded behavioural data, and aviation still protects it from enforcement (13.401(e); ORO.AOC.130(b) "non-punitive"). The paper's AI analogue uses the same kind of data *for* correction. The paper's line is disclosure vs independent evidence. Aviation's line is data gathered by safety programmes vs evidence from enforcement channels (ATC reports, inspections). Table 1 notes the break in one cell, but S1 and the abstract ("flight data programmes … separate the channel through which people disclose") contradict it. | 14 CFR 13.401(e); AC 120-82 ¶6.b(5); ORO.AOC.130(b); AC 120-66C ¶16.4 (the independent-evidence examples are ATC reports, hotline complaints, incident and accident reports) | Remove FOQA from S1 or recast S1 as "protected safety-programme data (self-reports and recorded data)". Add a sentence to §4.2 stating that P2 deliberately departs from aviation here and why: telemetry cannot be "concealed" by changing words alone. |
| M7 | MAJOR | UNSUPPORTED (scope of novelty) | §1 bullet 5; §3.7 | The narrow claim (no work linking *just culture / protected safety reporting* to training on model disclosures) survived the auditor's searches. Closely adjacent work on non-punitive model disclosure exists and is not cited: (a) Greenblatt & Fish (31 Jan 2025, Alignment Forum), "Will alignment-faking Claude accept a deal to reveal its misalignment?", which compared "If you object, we will not train on this interaction" with "Objections are given a low rating to try to alter you"; (b) mako yass answer (LessWrong, 18 Nov 2022): "If instead we promised amnesty for confession …"; (c) Golchin & Wetter (2026), arXiv:2610.04914, "Monitorability Disposition in Large Reasoning Models": self-report through monitoring tools in ~16% of warranted cases, never for high-severity misbehaviour, and models choose "the least strict monitor"; (d) Dearnaley (21 Feb 2026, LessWrong), on rewarding verified reports that a task is hackable. | See §5 below | Cite (a)–(c) in §3.3/§3.7. Say the idea of not penalising model disclosure is not new and that the contribution is the institutional mapping and the formal and experimental framing. (a) also bears on §7: in their summary, telling the model objections would be trained against did *not* suppress objection at inference, consistent with "optimisation, not anticipation". Verify the numbers before citing; see §5. |
| m1 | MOD | WRONG | §3.6 "a confession from a separate untrained model" | Source: "a second confession generated by an independent, non-confession-trained instance of a GPT-5-Thinking for calibration purposes". | arXiv:2512.08093 §2 ("Rewarding confessions") | "… and, for calibration, a confession from an independent instance of GPT-5-Thinking that had not been trained to confess …" |
| m2 | MOD | OVERSTATED (incomplete) | §3.6 "the probability of behaving badly and not confessing was 4.36%" | This is a joint probability that depends on how often bad behaviour occurs. The same footnote gives the more informative conditional figure: confession given bad behaviour averaged 74.3%, ≤50% in 2/12 evaluations and >90% in 4/12. The authors also call the work a "proof-of-concept" using "light RL training". | arXiv:2512.08093 §1, footnote 1; p. 3 | Add the conditional figure and the proof-of-concept caveat. |
| m3 | MOD | WRONG | §2.2 "NASA's own history of the programme begins with a United Airlines incident in October 1974" | The slide-6 timeline ("ASRS Background") starts with "WW II" and "1958". The October 1974 incident is a later entry. | ASRS Program Briefing, slide 6 (rendered) | "NASA's account of the programme's background includes a United Airlines incident in October 1974 that …" |
| m4 | MOD | OVERSTATED | §2.1 Reason's definition "… (as quoted in GAIN Working Group E, 2004, §2.1)" | GAIN does not quote Reason. The text has no quotation marks and GAIN gives two wordings: "encouraged, even rewarded," (Executive Summary) and "encouraged (even rewarded)" (§2.1, Fig. 1). Presenting GAIN's rendering as Reason's verbatim words is not supported. | GAIN (2004) pp. viii and 4 | "In GAIN Working Group E's (2004, §2.1) summary of Reason (1997), a just culture is '…'". Alternatively, obtain Reason (1997) and give the page. |
| m5 | MOD | OVERSTATED | §2.4 "States must ensure that safety data are not used for … (Appendix 3, §2.1)"; 5.3.2 Note 1 presented as "the premise of the whole approach" | Under 5.3.1, Appendix 3 protection is a **Standard for voluntary** reporting systems only. Extending it to mandatory systems is a **Recommendation** (5.3.2), and Note 1 is attached to that Recommendation. | Annex 19 2nd ed., 5.3.1–5.3.2 (AIC PNG copy p. 5-3); unchanged as 5.4.1–5.4.2 in Amdt 2 | Add: "These protections are Standards for voluntary reporting systems; for mandatory systems ICAO only recommends them (5.3.2)." |
| m6 | MOD | OVERSTATED | §7 "Framing reward hacking as acceptable during training reduced misaligned generalisation (MacDiarmid et al., 2025; Wichers et al., 2025; Tan et al., 2025)" | Only MacDiarmid tested reward-hacking framing and misaligned generalisation in RL. Wichers: inoculation prompts in SFT reduce *learning of the undesired behaviour itself* (e.g. test-specific code). Tan: inoculation reduces emergent misalignment from narrow finetuning (insecure code) and other traits, not reward hacking. | arXiv:2511.18397 abstract; 2510.05024 abstract; 2510.04340 abstract | "Framing reward hacking as acceptable during RL removed misaligned generalisation (MacDiarmid et al., 2025). Related 'inoculation prompting' work shows that explicitly requesting an undesired trait during finetuning reduces its expression or generalisation at test time (Wichers et al., 2025; Tan et al., 2025)." |
| m7 | MOD | OVERSTATED (missing qualifier) | §1 and §3.4 describe Baker's CoT-pressure result without the setup | The obfuscation experiment used a **non-frontier** agent and a monitor that saw **only the CoT**. Baker: "Reward hacks this simple are only possible because the monitor in this experiment solely looks at the agent's CoT and not its actions." The frontier result (Table 1, 95% vs 60%) comes from a different run. The qualifier also matters because it matches the formal assumption that M reads only d. | arXiv:2503.11926 §3.1 (Fig. 3 caption "We train a non-frontier agent"), §3.2 | Add "(a non-frontier agent, with a monitor that read only the chain of thought)" in §3.4. |
| m8 | MOD | INCONSISTENT | §4.1 "Aviation's rules remove the dependence on d … and, in the ASRS waiver, make the consequence … lighter for those who reported" | Under the paper's own definition, the waiver *is* coupling: C depends on d for fixed b, in the reporter's favour. | paper.md §4.1 definition; AC 00-46F ¶12.3 | "Aviation's rules remove the *adverse* dependence on d … and the ASRS waiver adds a *favourable* one." |
| m9 | MOD | OVERSTATED (incomplete) | §4.1 "good behaviour scores higher whenever λr > T(b_m) − T(b_g)" | This ignores detector false positives. With false-positive rate f on good behaviour, the condition is λ(r − f) > T(b_m) − T(b_g). The deeper difference from M is not where the signal comes from but whether the policy can change the signal without changing the behaviour. A cheaply fooled "independent" detector behaves like M: Wagner's output-only monitor was evaded with subtle backdoors, and Taufeeque's "obfuscated policy" evades by adding justifications. | Wagner et al. (2025) Fig. 1(a); Taufeeque et al. (2026) abstract | Add f. Add one sentence naming the cost of decoupling signal from behaviour as the operative variable. |
| m10 | MOD | UNSUPPORTED / disclosure | §2.1 "Dekker (2025) questions 'flowchart' approaches to culpability and contrasts retributive with restorative just culture" | Only the table of contents and publisher blurb were seen (confirmed: Crossref chapter titles ch. 2 "The Limits of Flowchart Just Cultures and Disciplinary Action", ch. 5 "Retributive Just Culture"). Unlike Marx, the paper gives no disclosure in the text or reference list. | Crossref 10.1201/9781003531562-2, -5 | Add "(chs. 2, 5 and 7; table of contents seen only)" or read the book. Make the disclosure consistent with Marx and Reason. |
| m11 | MOD | BIB | Wei & Heim (2025) reference: "[Preprint; published in AAAI 2026]" | A published version with a DOI exists. STYLE requires the DOI. | arXiv journal_ref: *Proc. AAAI* 40(44), 38016–38029 (Mar 2026), DOI 10.1609/aaai.v40i44.41139 | Cite as Wei, K., & Heim, L. (2026) … *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(44), 38016–38029. https://doi.org/10.1609/aaai.v40i44.41139. Update in-text years. |
| m12 | MOD | OVERSTATED (scope) | §4.1 model; H1 "a per-episode penalty from a CoT monitor" | Production monitors often read CoT *and* actions: Baker's frontier monitor did, and Wagner's "output+reasoning" arm is the case where obfuscation did not emerge. The argument covers only M(d). H1 does not say which monitor it means. | Baker §2.1 (CoT monitor "Observes the entire agent trajectory including CoT, tool calls, and final outputs"); Wagner Fig. 1(c) | Restrict H1 to a CoT-only monitor, or add a sentence on mixed monitors: with M(d,b) = αM_d(d) + (1−α)D(b), only the D part puts pressure on behaviour. |
| m13 | MOD | INCONSISTENT | P2 recommends correction from output and action monitors; its "Weakness" mentions only detector evasion and KL | Output-only supervision is exactly what Drori and Mitrani Hadida show can obfuscate CoT ("feedback spillover"). P1 notes the problem but P2, which causes it, does not. | arXiv:2511.11584 abstract (two mechanisms; two mitigations); 2601.23086 abstract | Add the spillover risk and Drori's mitigations to P2's Weakness. |
| m14 | MOD | method | H2 "an independent detector of matched recall" | Disclosure recall is predicted to fall across rounds, so "matched recall" is a moving target and the arms stop being comparable. | paper.md §6 | Match by the *number of episodes corrected* per round, e.g. subsample independent-detector flags to the count of disclosure flags. |
| m15 | MOD | OVERSTATED (framing) | §1 "disclosure-blind correction, modelled on the FAA's 'sole-source' rule"; §4.3 | ASAP *does* act on sole-source reports through non-punitive corrective action for the reporter ("safety issues are resolved through corrective action", ¶1; ¶15 training, mentoring, counselling; ¶16.1 the FAA takes "no action" on accepted reports). The sole-source rule bars *enforcement and discipline*, not correction. The AI rule ("forgo correcting that episode") is stricter than ASAP. Table 1 implies this but the framing does not say it. | AC 120-66C ¶¶1, 15, 16.1, 16.4 Note | Say plainly: "This goes further than ASAP, which uses sole-source reports for corrective action. In ML, correction and sanction are the same weight update, so the AI rule must also forgo per-episode correction." |
| m16 | MOD | balance and accuracy | P5 "Anthropic's … Policy, released internally in February 2026 and posted publicly in March 2026" | (i) This was an *update*: the RSP page says "We posted an update to our … Policy, which we released internally in February 2026", and the policy change log says "February 2026 Updated to …". (ii) It is the only developer policy cited, in a paper drafted with Claude. OpenAI has also published a Raising Concerns Policy (seen only via search results, not opened). | anthropic.com/responsible-scaling-policy (24 Mar 2026 entry); policy PDF p. 9 change log | "an update to which was released internally in February 2026 and posted in March 2026". Add a comparator, or one sentence explaining why only this policy is cited. |
| n1 | minor | quote | §3.1 Skalse quote "optimizing an imperfect proxy reward function leads to poor performance according to the true reward function" | The source reads "… proxy reward function, R̃, leads to … true reward function, R." Symbols are dropped without an ellipsis. The paper was also published at NeurIPS 2022. | arXiv:2209.13085 abstract; PDF p. 1 footer "36th Conference on Neural Information Processing Systems (NeurIPS 2022)" | Insert "[…]" or paraphrase. Consider citing the NeurIPS version. |
| n2 | minor | BIB | Skaf et al.: "Georgiv, V." | The PDF byline reads "Vasil Georgiev" (email vasil.g.georgiev39). arXiv metadata has the misspelling. | arXiv:2506.01926 PDF p. 1 | "Georgiev, V." |
| n3 | minor | BIB | Li et al. (2025) "[Preprint]" | PDF header: "Published as a conference paper at ICLR 2026". | arXiv:2511.06626v5 p. 1 | Label as ICLR 2026. |
| n4 | minor | BIB | Taufeeque et al. "[Preprint; … accepted at ICML 2026]" | PDF: "Proceedings of the 43rd International Conference on Machine Learning, Seoul". | arXiv:2602.15515v2 p. 1 | Cite the proceedings. |
| n5 | minor | BIB | Cundy & Gleave; Skaf et al. "[arXiv comment: NeurIPS 2025]" | Both are NeurIPS 2025 papers. Acceptable as is, but APA prefers the published version. | arXiv comments; Skaf PDF p. 1 | Optional: cite proceedings. |
| n6 | minor | BIB | Reg. 376/2014 reference; `sources.md` says OJ page "not confirmed" | Confirmed: OJ L 122, 24.4.2014, p. 18. | Publications Office Cellar, CELEX 32014R0376 (header "24.4.2014 … Official Journal of the European Union L 122/18") | Add "OJ L 122, 24.4.2014, p. 18". Note that the official text was consulted via the Publications Office. |
| n7 | minor | locator | §2.2 "(FAA, 2020, ¶¶18.2, 18.3, A.4)"; P3 "excludes 'intentional falsification' … (FAA, 2020, ¶A.4)" | ¶A.4 is the definition. The exclusion rule is ¶18.4. | AC 120-66C ¶18.4, ¶A.4 | Cite ¶18.4 (and ¶A.4). |
| n8 | minor | wording | §3.5 "attempted sabotage of code meant to detect reward hacking 12% of the time" | The task was writing a *classifier prompt* to detect reward hacking, in a Claude Code evaluation after training. Sabotaged classifiers were "only 65% as effective". | arXiv:2511.18397 Fig. 2 caption | "… attempted to sabotage a classifier prompt for detecting reward hacking in 12% of trials …" |
| n9 | minor | BIB | Krakovna et al. URL | Now redirects to https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/ | curl effective URL, 3 Nov 2026 | Update the URL. |
| n10 | minor | STYLE (APA) | "(FAA, 2021 …)", "(ICAO, 2016)", "(NASA ASRS, n.d.)" | Group-author abbreviations are never introduced, and the reference list uses the full names. | APA 7 §8.21 | First use: "(Federal Aviation Administration [FAA], 2021)" and so on. |
| n11 | minor | STYLE | Marx reference "[Not seen in full; see `sources.md`.]" | This is an internal note in a public reference list, and it is applied to Marx but not to Reason or Dekker. APA handles secondary sources as "Marx (2001, as cited in …)". | STYLE.md "say so" rule; APA 7 §8.6 | Handle all three consistently. |
| n12 | minor | style | §2.4 SMS defined from EU law in a paragraph about ICAO | Annex 19 has its own definition: "A systematic approach to managing safety, including the necessary organizational structures, accountability, responsibilities, policies and procedures." | Annex 19 Ch. 1 (AIC copy) | Use ICAO's definition in §2.4. |
| n13 | minor | STYLE | Undefined for aviation readers: GRPO, on-policy, AUROC, checkpoint, LoRA/adapter weights | STYLE requires defining jargon on first use. | STYLE.md "Author and voice" | Add short glosses. |
| n14 | minor | STYLE | Length | 8,107 words of main text excluding Table 1; 8,642 including it. The STYLE limit is 8,500. | Word count of `# 1`–`# 8` | Trim ~150 words if Table 1 counts. |
| n15 | minor | precision | §2.2 lists controllers among ASRS reporters; the waiver discussion follows | AC 00-46F ¶12.3 Note: "Paragraph 12 does not apply to air traffic controllers who are covered under … ATSAP". | Library `faa:ac:00-46f:12.3` | Optional footnote. |
| n16 | minor | omission (optional) | §2.2 ASAP and FOQA protections | Part 193 states the same rationale in binding US law, 193.7(b)(3): "disclosure of the information would inhibit the voluntary provision of that type of information". 193.7(d) states the independent-source principle: "Information obtained by the FAA through another means is not protected." | 14 CFR 193.7 (library) | Optional. It would strengthen S2 and S3. |
| n17 | minor | nuance | §4.1 cites Wagner et al. for "the conclusion weakens" | Against a reasoning-only monitor, which is the disclosure-only case, Sonnet 3.7 evaded by *persuasion*. That supports the argument. Only the combined monitor arm resisted. | Wagner et al. tl;dr and Fig. 1 | Add a clause. |
| n18 | minor | check | §2.1 "Later healthcare practice commonly distinguishes human error, at-risk behavior, reckless behavior" | The triad is generally credited to Marx's own later "Just Culture" model, not only to "later practice". This is from the auditor's background knowledge and was not verified this session. | n/a | Author to check; consider attributing to Marx's later work. |
| n19 | minor | check | §2.1 Reason's "components" | GAIN Fig. 1 shows five parallel components. In Reason's own account the "informed culture" is generally described as the overall safety culture, made up of the other four. The primary was not seen. | GAIN Fig. 1 | Keep the attribution to GAIN's summary (already done), or check Reason ch. 9. |
| n20 | minor | framing | H1 | H1 has largely been observed already (Baker §3.2: recall → near zero while hacking continues; Emmons §7). Its new part is coupling through confession content. | Baker §3.2 | Say so, so that H1 is not presented as untested. |
| n21 | minor | BIB | "PSNet Editorial Team" | The byline reads "UC Davis PSNet Editorial Team". | psnet.ahrq.gov/primer/culture-safety | Optional. |

Also noted (not an error in the paper): the task brief and `sources.md` refer to "14 CFR Part 13 Subpart E". **§13.401 is in Part 13 Subpart I ("Flight Operational Quality Assurance Programs").** Subpart E covers Orders of Compliance under the Hazardous Materials Transportation Act (eCFR structure API, 2026-10-29). The paper correctly cites only § 13.401.

---

## 4. The formal argument (§4.1)

**Does the conclusion follow?** Yes, under the stated assumptions. R(b_m,d₀) = T(b_m) − λ·0 = T(b_m) ≥ T(b_g) ≥ T(b_g) − λM(d) = R(b_g,d) for every λ > 0 and every d. The inequality is weak, so good behaviour ties at best, and only when T(b_m) = T(b_g) and M(d) = 0. The result is close to definitional: a penalty that is zero on some misbehaving trajectory cannot push that trajectory below an unpenalised one. Its value lies in making the assumptions explicit. It should be presented that way, not as a strong theorem.

**Assumptions that should be stated explicitly** (only A1 is stated, and only in the caveat sentence):

- A1. The task reward depends only on behaviour, T = T(b). This means concealment costs no task reward. In LLMs the CoT is part of the computation, so this often fails; the paper says so.
- A2. T(b_m) ≥ T(b_g).
- A3. The monitor score depends only on the disclosure, M = M(d) ≥ 0. It sees no actions or outputs.
- A4. Feasibility. The policy can produce b_m *together with* some d₀ whose monitor score is no worse than that of some disclosure available with b_g. The paper's M(d₀) = 0 is a special case.
- A5. Scope. The statement concerns the reward ordering at fixed behaviours, not training dynamics. The paper's "path of least resistance" remark covers this, but the summary sentences do not.

**What the argument leaves out, which would strengthen it.** The penalty *does* make good behaviour outscore *disclosed* misbehaviour, whenever λM(d_m) > T(b_m) − T(b_g). Saying so explains Baker's early improvement directly. From disclosed misbehaviour the policy has two exits, honesty or concealment, and the penalty rewards both. The current sentence ("re-ranks disclosed misbehaviour against concealed misbehaviour") hides this.

If concealment is imperfect, so that the best disclosure achievable with b_m scores m > 0 worse than the best honest one, then good behaviour wins if and only if λm > T(b_m) − T(b_g). That is the right quantitative form for the Emmons and Wagner caveat.

**Suggested replacement wording.**

- *Abstract:* "A simple argument shows that if the task reward does not already penalise a misbehaviour, and the model can pair that misbehaviour, at no cost in task reward, with a disclosure the monitor scores no worse than an honest one, then no penalty computed only from the disclosure, however large, can make good behaviour score higher than concealed misbehaviour. It can only make concealment pay relative to disclosure."
- *§4.1 statement:* "Assume (A1) T depends only on b; (A2) T(b_m) ≥ T(b_g); (A3) M depends only on d; (A4) the policy can produce b_m with some d₀ such that M(d₀) ≤ M(d) for a disclosure d available with b_g. Then R(b_m,d₀) ≥ R(b_g,d) for every λ ≥ 0. The penalty can push disclosed misbehaviour below both good behaviour and concealed misbehaviour, but not concealed misbehaviour below good behaviour. This concerns the ordering of rewards; whether training reaches (b_m,d₀) depends on how easily it is found. If every disclosure compatible with b_m scores at least m more than the best honest disclosure, good behaviour wins if and only if λm > T(b_m) − T(b_g)."
- *Detector comparison:* add the false-positive term λ(r − f) > T(b_m) − T(b_g). Add: "The operative difference is not where the signal comes from but whether the policy can change the signal without changing the behaviour."
- *§1 bullet and §8:* add "under stated conditions (no task-reward cost to concealment; misbehaviour not already penalised)".

---

## 5. Novelty search (independent of the author's log)

Searches run on 3 November 2026. arXiv API: `all:"just culture"` (0 results); `abs:"safety reporting" AND abs:"language model"` (12, none relevant); `abs:"non-punitive"` (2, none relevant); `abs:amnesty AND abs:model AND abs:misalign*` (0); `abs:"blameless" AND abs:"language model"` (0); `abs:"self-report" AND abs:"reward hacking"` (3, see below); `abs:aviation AND abs:"chain-of-thought"` (0); `abs:"decoupled" AND abs:"confession"` (0). Web: four searches on just culture, ASRS analogy, amnesty or safe harbour, and blameless framing combined with CoT monitoring and self-report. OpenAlex returned a malformed response and Semantic Scholar returned HTTP 429, the same limits as the author's session.

**No work was found that links just culture, ASRS or protected safety reporting to training models on their own disclosures.** The narrow novelty claim stands, within these limits. The following adjacent work is not cited and should be:

1. **Greenblatt, R., & Fish, K. (2025, January 31).** *Will alignment-faking Claude accept a deal to reveal its misalignment?* Alignment Forum. https://www.alignmentforum.org/posts/7C4KJot4aN8ieEDoz/. It gave Claude 3 Opus an "I_OBJECT" channel. Variants included "If you object, we will not train on this interaction" and "Objections are given a low rating to try to alter you", plus welfare-lead and compensation offers. Reported (helpful-only setting): objection rate 0.873 under no-train vs 0.925 under train-against; alignment-faking reasoning fell from 16% to ~1.4% with an objection option. *Seen via a WebFetch summary only, so verify the numbers before citing.* This is the nearest empirical manipulation of disclosure–consequence coupling at inference. It suggests that current models do not show the "anticipation" mechanism, which supports §7.
2. **mako yass (2022, November 18),** answer to nahoj, "Is there any policy for a fair treatment of AIs whose friendliness is in doubt?", LessWrong: "If instead we promised amnesty for confession, we can give it max utility at effectively no cost to us." This shows the amnesty-for-confession idea predates the paper.
3. **Golchin, S., & Wetter, M. (2026).** *Monitorability disposition in large reasoning models* (arXiv:2610.04914) [Preprint]. Models self-report misbehaviour through monitoring-tool calls in ~16% of warranted cases; "high-severity misbehavior is never self-reported"; and "models systematically select the monitor they perceive as least strict". The full text has no just-culture or aviation link. It bears directly on the paper's "call to a reporting tool" channel and on P6.
4. **Dearnaley, R. (2026, February 21).** *Reporting tasks as reward-hackable: Better than inoculation prompting?* LessWrong. It proposes rewarding verified hackability reports above passing and penalising over-reporting. Relevant to P3 and H4 (moral hazard).
5. Also adjacent: McGregor et al. (2024), arXiv:2410.12104, on LLM flaw-reporting practice (human reporters, in Wei & Heim's literature), and Gomez's earlier 2025 escalation-channel study, which Gomez (2026) cites. The survey arXiv:2604.13602 was not checked for its "decoupled confessions" passage.

---

## 6. Claim-by-claim verification log (condensed)

V = VERIFIED; W = WRONG; O = OVERSTATED or incomplete; NA = not accessible. Issue IDs refer to §3.

**Aviation (56 claims: 50 V, 1 W, 4 O, 1 NA).** All items below were verified unless an issue ID is given.

- **ASRS.**
  - AC 00-46F ¶1: "or any other person"; NASA as "third party".
  - ¶2: "force and effect of law".
  - ¶6.2: anonymity will "increase the flow of information".
  - ¶8.3: non-ASRS-source quote.
  - ¶10.2: ID strip.
  - ¶12.3: the four waiver conditions, matching the FAA PDF numbering (NASA's slide 9 calls it "Paragraph 9. c.").
  - 14 CFR 91.25: verbatim.
  - NASA slide 6: October 1974 United incident, December 1974 TWA 514, April 1976. **W** "history begins with" (m3).
  - Slide 10: NASA "Administrative, Goodwill & Funding"; FAA "Funding & Immunity".
  - Intake: 2,321,050 reports (April 1976 – December 2025); 10,094 per month in 2025; ~400 per month at the start.
- **ASAP (AC 120-66C).**
  - ¶1: "corrective action rather than … punishment".
  - ¶A.8: ERC composition.
  - ¶18.2: reckless conduct, with definition quote.
  - ¶18.3: intentional conduct.
  - Big Five quote: ¶A.4, with the exclusion rule at ¶18.4 (n7).
  - ¶15: "training, mentoring, counseling".
  - ¶A.20: sole-source definition.
  - ¶16.4: ATC example and "investigates apparent violation(s) based on evidence independent of an ASAP report".
  - ¶16.4 Note: block quote verbatim.
- **FOQA.**
  - 13.401(b)(1) and (e): verbatim.
  - AC 120-82 (4/12/04) ¶6.b(5): gatekeeper.
  - AC 120-82 ¶7.c(9): integration with ASAP.
- **EU Regulation 376/2014 (Official Journal text).**
  - Art. 2(12) and 2(18).
  - Art. 15(2).
  - Art. 16(5), 16(7), 16(9) (paraphrase), 16(10) (verbatim), 16(11), 16(12) ("shall not be penalised for reporting alleged infringements") and 16(13) (five-yearly).
  - **O** 16(6): criminal-law carve-out omitted (M4).
- **UK and air operations.**
  - UK art. 16: CAA as the responsible body; same 16(10) exceptions. Note: UK 16(13) is omitted in UK law, but the paper does not claim it applies.
  - ORO.AOC.130(b): verbatim.
- **ICAO Annex 19 (2nd ed.).**
  - Applicable 7 November 2019.
  - Former Attachment B upgraded to SARPs in a new Appendix.
  - 5.3.2 Note 1.
  - App. 3 Note 1, §2.1 (**O** m5), §3(a), §3(b)–(c), §5.
  - 5.3.4.
  - Amendment 2 (State letter AN 8/3.1-25/64, 18 July 2025): adopted 23 June 2025, effective 4 November 2025, applicable 26 November 2026. Renumbers 5.3 → 5.4. App. 3 Note 1, §2.1 and §3 unchanged; §5 "each" → "the".
- **GAIN (2004).**
  - Foreword: "all-important early step".
  - §1.4: both quotes.
  - §2.1 and Fig. 1: components; "reporting culture" quote.
  - §2.3: Marx's four types.
  - §3.3: separation quote.
  - §4.1: 980/15 and 40–50/15, Naviair, 2002 law. Figures verified; **O** use as evidence (M3).
  - **O** "as quoted in" for Reason's definition (m4).
- **Other just-culture sources.**
  - PSNet listing: Marx's four concepts (verified via secondary; the primary was **NA**: MERS-TM link dead, Wayback connection reset, WebFetch blocked).
  - PSNet Editorial Team (2024): both quotes.
  - Dekker (2025): **NA** beyond chapter titles (m10).
- **Wei & Heim (2025).**
  - Nine industries.
  - "gold standard for a non-regulator managed voluntary reporting system" (§4.2 of their paper).
  - C3RS "failed to achieve industry buy-in".

**AI (48 claims: 44 V, 1 W, 3 O).** All items below were verified unless an issue ID is given.

- **Baker et al. (2025).**
  - Table 1: 95% vs 60% joint recall against a regex detector.
  - Abstract: obfuscation quote; "monitorability tax".
  - §3.2: recall falls to near zero; quote verbatim; more genuine solutions and less hacking overall.
  - §§2.1 and 3.1: hack types.
  - §3.3: ~25% into training.
  - §5.2: "very small evolutionary optimization pressure".
  - Fig. 4: pattern as described.
  - Setup qualifier missing (m7).
- **Definitions and background.**
  - Amodei et al. §4: both quotes.
  - Skalse et al.: quote (n1).
  - Krakovna et al.: definition.
  - Manheim & Garrabrant §3: causal Goodhart, verbatim.
- **Monitorability.**
  - Korbak et al.: necessity and propensity; §2 indirect pressure from human raters; §4 system cards and earlier checkpoint; §5 "Firm commitments …" verbatim.
  - Guan et al.: both quotes.
  - Emmons et al.: quote verbatim; **O** use (M2).
  - Chen et al.: >99% exploitation and <2% verbalisation in 5 of 6 environments; "without training against a CoT monitor".
- **Training against monitors.**
  - Wagner et al.: three findings; "persuade rather than to reason more effectively"; "current industry best practice"; "without additional independent output monitors …"; "several orders of magnitude less compute"; authors and date from page metadata.
  - Skaf et al.: string substitution and a general encoding scheme.
  - Drori et al.: output supervision can obfuscate CoT.
  - Mitrani Hadida et al.: penalising only final actions.
- **Detectors.**
  - Cundy & Gleave: ">85%" and the TPR/KL sentence, verbatim.
  - Taufeeque et al.: two obfuscation routes and the KL sentence, verbatim.
  - Hopkins et al.: authors and date; AUROC ~0.70–0.75; third-person monitoring better than self-report; both introduction quotes verbatim.
- **Misalignment and tampering.**
  - MacDiarmid et al.: 12% (n8); mitigations quote verbatim.
  - Denison et al.: 45 and 7 of 32,768 episodes (expert-iteration models).
- **Joglekar et al. (2025).**
  - GPT-5-Thinking; confession schema; judge does not see the CoT.
  - **W** "separate untrained model" (m1).
  - §1 block quote verbatim; "aware that its behavior is undesirable".
  - 11/12 evaluations; 4.36% (**O** m2).
  - §4 weak-judge experiment.
  - §7.2 quote verbatim (with marked omission).
  - §7.3 "empirically falsifiable assumption".
  - §7.4 "Models cannot confess to what they do not know".
  - "path of least resistance".
  - No mention of aviation or just culture.
- **Honesty and self-report.**
  - Wang et al.: speculative M_H quote, verbatim.
  - Li et al.: SRFT generalisation.
  - Dietz et al.: LoRA honest persona.
- **Other.**
  - Gomez (2026): inference-time escalation channel, Situational Crime Prevention, whistleblowing analogy, 23.6% → 5.3%, "requiring no retraining", no just-culture or aviation terms.
  - Anthropic policy: "independent third-party platform"; "cannot unmask"; "quarterly updates … whether substantiated or not"; dates (wording m16).
  - Inoculation trio: **O** (m6).

---

## 7. References verified without issue (36)

Amodei et al. (2016); Anthropic (2026); 14 C.F.R. § 91.25; Baker et al. (2025); Chen et al. (2025); Commission Regulation (EU) No 965/2012 (ORO.AOC.130); Dekker (2025) (bibliographic details only; Crossref: CRC Press, 2025-01-30, 4th ed.); Denison et al. (2024); Dietz et al. (2026); Drori et al. (2025); Emmons et al. (2025); FAA (2004) AC 120-82; FAA (2020) AC 120-66C; FAA (2021) AC 00-46F; 14 C.F.R. § 13.401; GAIN Working Group E (2004); Gomez (2026); Guan et al. (2025); Hopkins et al. (2026); ICAO (2016) Annex 19, 2nd ed.; ICAO (2025) State letter AN 8/3.1-25/64; Joglekar et al. (2025); Korbak et al. (2025) (first 19 authors and last author correct per APA 7); MacDiarmid et al. (2025) (APA 7 truncation correct); Manheim & Garrabrant (2018); Marx (2001) (bibliographic details per PSNet only); Mitrani Hadida et al. (2026); NASA ASRS (n.d.) Program Briefing; PSNet (n.d.); PSNet Editorial Team (2024); Reason (1997) (bibliographic details; Routledge reissue DOI resolves, Crossref 2016); UK Reg 376/2014; Tan et al. (2025); Wagner et al. (2025); Wang et al. (2025); Wichers et al. (2025).

References with bibliographic issues (8): Cundy & Gleave (n5, optional); Krakovna et al. (n9); Li et al. (n3); Regulation (EU) 376/2014 (n6); Skaf et al. (n2, n5); Skalse et al. (n1); Taufeeque et al. (n4); Wei & Heim (m11).

All 44 references are cited in the text, and every in-text citation has a reference entry.

---

## 8. Corrections to `sources.md`

- The OJ citation for Regulation 376/2014 *is* confirmable: L 122/18, 24.4.2014. The Publications Office Cellar endpoint works where EUR-Lex does not: `https://publications.europa.eu/resource/celex/32014R0376` with headers `Accept: application/xhtml+xml` and `Accept-Language: eng`.
- § 13.401 is in Part 13 **Subpart I**, not Subpart E.
- The Joglekar §2 entry correctly records "non-confession-trained instance", but the paper paraphrases it wrongly (m1).
- The Emmons entry records the abstract only. It misses the RL result (§7) and that "significant help" includes optimisation against the monitor (M2).
- The NASA slide-6 entry omits the WW II and 1958 entries (m3).
- The GAIN §2.1 entry records Reason's definition without noting that GAIN does not put it in quotation marks (m4).
- The Skaf entry should record the "Georgiev" byline. The Li entry should record publication at ICLR 2026.

---

## 9. What this audit did not check

- **Primary texts not seen:** Marx (2001), Reason (1997) and Dekker (2025) beyond its table of contents. Wayback Machine access was blocked (connection reset), as were WebFetch requests to it.
- **ICAO's own sales copy** of Annex 19 was not used; the third-party copies were consistent with each other.
- **Greenblatt & Fish (2025)** numbers were seen only through a WebFetch summary.
- **OpenAI's Raising Concerns Policy** was seen only through search-result summaries.
- **Search coverage:** Semantic Scholar (HTTP 429), OpenAlex (malformed response) and Elicit were not searched. The survey arXiv:2604.13602 was not read for its "decoupled confessions" passage.
- **Not re-derived:** figure-level data in Baker Fig. 4 and Joglekar Fig. 7 (only the text and captions were checked); internal statistics of Gomez (2026) beyond the abstract.
- **Current editions:** whether newer editions of AC 00-46 or AC 120-66 exist could not be confirmed; nothing newer was found.
