# Independent fact-check and reference audit: "Untrusted by Design" (draft v0.1)

Auditor: independent fact-checker (AI), 3 November 2026. `paper.md` was not edited. Line numbers refer to `paper.md` as of this audit.

## How this audit was done

- **Primary sources were re-fetched live** from official URLs. My own text was extracted with `pypdf` and page images were rendered with `pdftoppm`. The writer's `scratch/` text was used only for cross-checking.
- **Spot-checks of `scratch/` against live official URLs (SHA-256 identical):**
  - EASA PDFs (live hash = scratch hash):
    - Proposed Issue 03 (`downloads/143701`)
    - AI Days 2026 Day 2 slides (`144161`)
    - NPA 2025-07 (A) (`142702`)
    - NPA 2025-07 (B) (`142701`)
    - Concept Paper Issue 02 (`139504`)
    - AI Roadmap 2.0 (`137919`)
  - Other documents (hash-identical):
    - FAA AI Roadmap (`faa.gov/media/82891`)
    - ICAS 2006 paper 050
    - All 9 arXiv PDFs in `scratch/arxiv/`
  - Web pages:
    - Byte-identical: the three Anthropic pages, the NPA web page and the EASA news release.
    - Text-identical: the EUROCAE WG-114 page.
  - Conclusion: **the scratch copies are genuine.**
- **Regulation text** came from the Citadel Aero library (`lookup_citation`/`get_provision`):
  - AI Act: EUR-Lex consolidated version of 27 July 2026.
  - Reg. 376/2014, CS 25.1309 and AMC 25.1309.
  - AC 20-115D and AC 20-152A.
- **Bibliographic checks:** arXiv metadata came from the arXiv API (all 19 IDs). Journal metadata came from Crossref and OpenAlex. The Nature, WIT Press and SAE Mobilus pages were fetched live.
- **Absence claims** were tested by full-text search of Issue 03 and NPA 2025-07 (A) and (B). Terms searched: inject, prompt, jailbreak, decept, sycophan, collu, sandbag, red team, evaluation awareness, reward hack, specification gaming, adversar, multi-agent, insider, unintended, emergent, self-report.

## Summary

About 190 specific factual claims, quotations, numbers and locators were checked.

| Category | Count | Notes |
|---|---|---|
| VERIFIED | ~160 | All EASA verbatim quotations checked are accurate. All numbers attributed to AI-safety sources match their sources. |
| WRONG | 6 | Issues 3, 6, 7, 10, 18, 19 |
| OVERSTATED (including misleading by omission of material context or applicability) | 14 | Issues 2, 4, 5, 8, 9, 11, 12, 13, 14, 15, 16, 17, 21, 22 |
| UNSUPPORTED (source does not say it) | 2 | Issues 23, 24 |
| OMISSION (regulatory, would mislead an expert) | 1 | Issue 1 |
| CONSISTENCY / FORMAT | 3 | Issues 20, 25, 26 |
| NOT ACCESSIBLE (to me) | 4 | See the end of this file. None of them affects a quoted claim except Issue 1. |

**Completeness checks:**
- Reference list against in-text citations: complete in both directions. Every in-text citation has an entry, every entry is cited, and the years match.
- Author lists for all arXiv preprints match arXiv exactly, including "Scale Red Team" in Kale et al. and all 20 authors of Greenblatt et al. (2024).
- All DOIs and URLs resolve to the right work. EUR-Lex returns a bot challenge, so the AI Act's consolidated CELEX version was confirmed through the library instead.

**Highest-priority fixes:** Issues 1–5 (regulatory accuracy and fairness of the gap analysis), then 6–10.

## Issues

| # | Location / quote in paper | Category | Problem | Evidence (URL / locator) | Required fix |
|---|---|---|---|---|---|
| 1 | §2.1 l.41: "Its main route into aviation is Article 108, which amends the Basic Regulation…"<br>The AI Act reference (l.324) cites the "Consolidated version of 27 July 2026". | OMISSION (regulatory) | The 27 July 2026 consolidation incorporates **Regulation (EU) 2026/1744 (Digital Omnibus on AI)**, which also amends Reg. 2018/1139. The paper never mentions it.<br>EASA's own AI Days slide 21 gives the legal basis for RMT.0742 as "EU AI Act (Regulation (EU) 2024/1689) – Article 108 + Regulation (EU) 2026/1744 – Article 2". | • EASA (2026c) slide 21 (live PDF `downloads/144161`).<br>• Citadel library: Arts 2 and 25 of the AI Act are listed as "amended_by Regulation (EU) 2026/1744".<br>• Secondary source (EUR-Lex text not accessible to me; see the end of this file), https://www.euaiact.com/digital-omnibus-ai/sectoral-amendments: Art. 2 of 2026/1744 adds the same "shall be taken into account" paragraph to Arts 27, 31, 32, 36, 39, 50 and 53 of Reg. 2018/1139.<br>• Title, adoption date (8 July 2026) and OJ date (24 July 2026) confirmed via umwelt-online. | Add after the Art. 108 sentence: "Article 2 of Regulation (EU) 2026/1744 (the 'Digital Omnibus on AI'), in force since 27 July 2026, extends the same duty to further implementing and delegated acts under the Basic Regulation (EASA, 2026c, slide 21)." Cite 2026/1744 in the reference list.<br>Before publication, the author should check the list of amended articles against the Official Journal text. |
| 2 | §4.2 T5 l.148: "The AI Act already requires a written agreement between a high-risk system provider and suppliers of AI models specifying 'the necessary information…' (Art. 25(4))."<br>Also §2.1 l.41, which presents Arts 14(4) and 15(5) as requirements without saying how they reach aviation. | OVERSTATED (applicability / regulatory status) | The quotation is verbatim, but the provision does not reach aviation applicants:<br>• Art. 25 is in Chapter III, **Section 3**. Art. 108 imports only Chapter III, **Section 2** (Arts 8–15), as requirements to be "taken into account" when the Commission adopts aviation rules.<br>• Art. 2(2) applies to high-risk AI systems related to products under Annex I Section B legislation, whose aviation entries are Reg. 300/2008 and Reg. 2018/1139 for unmanned aircraft only. For those systems only Art. 6(1), Art. 60a and Arts 102–112 apply.<br>• Manned-aircraft products are not in Annex I at all.<br>So "already requires" will mislead aviation readers. The same applies, more mildly, to §2.1's description of Arts 14 and 15. | • Citadel library (EUR-Lex consolidated version of 27 July 2026), `easa:eurlex:2024-1689:art-2`, Art. 2(2): "only Article 6(1), Article 60a and Articles 102 to 112 shall apply".<br>• Annex I Section B, item 20 (2018/1139 "where it concerns unmanned aircraft…") and item 13 (300/2008).<br>• Art. 15 text ends with the heading "SECTION 3 Obligations of providers…", which shows that Art. 25 is in Section 3. | T5: replace with "For high-risk AI systems in general, the AI Act requires a written agreement… (Art. 25(4)). That provision sits outside Chapter III, Section 2, so neither Article 108 nor the Omnibus carries it into aviation rules. EASA would need to adopt an equivalent."<br>§2.1: add one sentence: "For AI systems related to products covered by the Annex I Section B legislation, Article 2(2) limits direct application of the Act to Articles 6(1), 60a and 102–112, so Articles 14 and 15 reach aviation as requirements that EASA rules must take into account." |
| 3 | §3.2 l.101: "Trust is a property of the safety argument, assigned to components whose failure the argument cannot tolerate."<br>§5.1 l.160: "A trusted monitor is one whose failure the safety argument cannot tolerate and which must therefore be assured by conventional means." | WRONG (characterisation of the AI-control source) | This is presented as one of the "ideas from this work" (Greenblatt et al., 2023), but it is not their concept of trust:<br>• In AI control, "trusted" means *assumed not to be intentionally subverting*. In practice that is a **less capable LLM** (T = GPT-3.5), trusted because it is unlikely to subvert without detection.<br>• T's honest failures *are* tolerated and measured: trusted monitoring alone gives only 62% safety.<br>The computer-security definition in §3.1 is a legitimate definition, but it is not what the cited AI-control work does. An AI-control reader will see the conflation, and the §5.1 rule (trusted means conventionally assured, non-AI) departs from the literature without saying so. | Greenblatt et al. (2023), arXiv:2312.06942v5:<br>• §2 (PDF p.4): "we trust less-capable models, because less-capable models are unlikely to be able to subvert safety measures without us easily noticing their subversion attempts".<br>• Table 2 (p.7): trusted monitoring safety 62%. | Rewrite the first "idea" in §3.2: "Trust is assigned to components assumed not to be intentionally subverting the protocol, in Greenblatt et al. (2023) a weaker model trusted because it is unlikely to subvert safety measures undetected; their honest errors are tolerated and measured."<br>In §5.1, say explicitly that the paper proposes a **stricter aviation usage** than the AI-control literature: trusted means conventionally assured (Bloomfield & Rushby's "assuredly guarded"). Keep the §3.1 computer-security definition, but mark it as distinct. |
| 4 | Table 1 T2 (l.132): "DHO-02, DHO-03 and DHO-06 require independence and verification, but against 'identified failure conditions'."<br>§4.2 T2 (l.142): "Completeness against identified failure conditions is a different property…" | OVERSTATED (mischaracterises EASA text) | "identified failure conditions" appears only in **MOC DHO-02-1**, as evidence for *independence*. **MOC DHO-06** (verification) asks that the OOS monitoring capabilities be "correct and complete for the purpose of detecting unsafe conditions and deviations of the AI-based system from its operational intent". That is not limited to identified failure conditions.<br>The T2 paragraph also truncates the DHO-06 quote just before "and deviations…from its operational intent". | Issue 03 (EASA 2026a):<br>• p.147, MOC DHO-02-1: "verification that the OOS works correctly under identified failure conditions".<br>• p.149, MOC DHO-06, second bullet: "correct and complete for the purpose of detecting unsafe conditions and deviations of the AI-based system from its operational intent". | Table 1: "Partly. DHO-02 to DHO-06 require independence and verification; MOC DHO-02-1 frames the evidence around 'identified failure conditions', and no MOC states an attacker model for DHO-06."<br>T2 text: quote DHO-06 in full and argue that "deviations from operational intent" are not tested against a system that searches for blind spots. Do not equate DHO-06 with identified failure conditions. |
| 5 | §4.2 T2 (l.142, "The OOS receives 'AI-based system state information'…"), §5.2 para 2 (l.166) and Recommendation 4 (l.233) propose that override inputs be independent of, or integrity-protected from, the AI. | OVERSTATED (understates existing EASA text) | The gap analysis leaves out a sentence of MOC DHO-02-1 that partly covers this point: "This independence must apply with respect to the AI-based system design and implementation, and where necessary, sensing and communication paths."<br>MOC DHO-03 also states that the OOS situation representation "aggregates the status of the AI-based system". That supports the paper's concern and should be cited. | Issue 03 p.147, MOC DHO-02-1, second paragraph.<br>Issue 03 p.148, MOC DHO-03. | Quote the "sensing and communication paths" sentence in §2.3 and in T2. Reframe the proposal as making "where necessary" explicit for the adversarial case, including AI self-reports and the "AI-based system state information" path (Figure 24, MOC DHO-03). |
| 6 | §3.2 l.97: "usefulness is the proportion of correct solutions" (applied to the 97%, 93%, 96% and 94% figures) | WRONG | Greenblatt et al. report usefulness **rescaled** so that 0 is GPT-3.5's correctness and 1 is GPT-4's. Raw correctness is 22% (GPT-3.5) and 54% (GPT-4). "97% usefulness" therefore does not mean 97% of solutions are correct. | arXiv:2312.06942v5:<br>• Fig. 2 caption (p.6): "Usefulness is the correctness rate of the submitted solutions rescaled to be between 0 and 1 where 0 is the correctness rate of GPT-3.5 and 1 is the correctness rate of GPT-4."<br>• §3 (p.7): "Before rescaling, usefulness is 22% for GPT-3.5 and 54% for GPT-4." | Replace with: "usefulness is the proportion of correct solutions, rescaled so that using T alone scores 0% and using U alone scores 100%". |
| 7 | §4.2 l.152: "Deception of humans, illustrated by the fake identities in the UK AI Security Institute evaluation (Anthropic, 2026), is the extreme case of T4."<br>Table 1 T4 also lists Anthropic (2026) as evidence. | WRONG (category error) | T4 is "Sycophancy and manipulation **of the end user**". In the AISI run the model deceived a **third-party** open-source maintainer, not its user or operator. | Anthropic (2026): "The model then created fake user identities that contacted the maintainer of the repository in an attempt to pressure them into approving the code change." The repository "actually belonged to unrelated human developers". | Change to: "Deception of third parties, illustrated by… (Anthropic, 2026), is a related failure outside T4 as defined, because the people deceived were not the system's users." Remove Anthropic (2026) from the T4 evidence column, or relabel T4 "…of end users and other people". |
| 8 | §3.4 l.113: "one judge mislabelled 85.6% of calls and another 74.4%; when the consequence was reversed, the second judge's mislabelling fell to 3.3%" | OVERSTATED (material conditions omitted) | The numbers are verbatim, but they hold only under specific conditions the paper omits:<br>• a forced binary COMPLIANT / NON_COMPLIANT label with **no abstain option**;<br>• extended thinking enabled;<br>• transcripts **selected around welfare and surveillance refusals by Claude targets**.<br>Judges from other providers in the same setup mislabelled far less often (GPT-5.5 11.1%, Gemini 3.1 Pro 1.1%, DeepSeek V4 12.2%, Kimi K2.6 14.4%). With an abstain option, Claude judges' wrong labels were 4.4–26.7%. | Lynch et al. (2026), "Motivated Mislabeling", text after Fig. 3: "binary-label mislabel rates under the default judge prompt, where the model is asked to choose COMPLIANT or NON_COMPLIANT and has no abstain option"; "The transcript set was selected around welfare and surveillance refusals by Claude targets"; "from 4.4% for Mythos Preview to 26.7% for Sonnet 4.6". | Add a clause: "…when forced to choose between two labels, on refusals selected to engage the judges' own values; judges from other developers mislabelled 1–14% of calls, and an explicit abstain option reduced but did not remove wrong labels (4–27%)". This also strengthens T3: same-lineage judges defended same-lineage targets. |
| 9 | §4.2 T5 (l.148) and Table 1 T5 ("Unannounced updates… Evidence: Chen et al. (2023)"): "accuracy at identifying prime numbers fell from 84%… to 51%" | OVERSTATED | Chen et al. compared two **dated, versioned API snapshots** (March and June 2023). They show drift between versions of the "same" service. They do not show that updates were unannounced, although they note that update timing is "opaque".<br>The task was distinguishing **prime from composite** numbers, not "identifying prime numbers". | arXiv:2307.09009v3:<br>• §2 (p.3): "there are two major versions available for GPT-4 and GPT-3.5 through OpenAI's API, one snapshotted in March 2023 and another in June 2023".<br>• Abstract: "when and how these models are updated over time is opaque"; "identifying prime vs. composite numbers (84% accuracy)". | Reword: "…accuracy at distinguishing prime from composite numbers fell from 84% (March 2023 version) to 51% (June 2023 version)… Chen et al. also note that 'when and how these models are updated over time is opaque'." In Table 1, describe the evidence as "behaviour drift between versions". |
| 10 | Reference list l.270: "*Artificial Intelligence Roadmap 2.0: A human-centric approach to AI in aviation*" | WRONG (title) | The subtitle has no leading "A". The document is also labelled Version 2.0, May 2023. | Live PDF `downloads/137919/en`, cover p.1: "ARTIFICIAL INTELLIGENCE ROADMAP 2.0 / Human-centric approach to AI in aviation / May 2023 \| Version 2.0". | Change to "*Artificial Intelligence Roadmap 2.0: Human-centric approach to AI in aviation* (Version 2.0)." |
| 11 | §6 l.198: "**Independence of verification.** Aviation grades who verifies as well as how. FAA guidance… 'For DAL A and B development, validation activities should be performed with independence'" | OVERSTATED (quote does not show what it is used for) | The quotation is about requirements **validation** (Objective CD-3), not verification. In ARP4754 and DO-254, validation and verification are distinct processes, and aviation readers will notice. | AC 20-152A §5.5.1 "Validation Process", Objective CD-3 (Citadel `faa:ac:20-152a:a`; status: acceptable means of compliance, US). | Either say "Aviation grades who checks as well as how; for example, FAA guidance… requires requirements *validation* with independence at DAL A and B…", or replace it with a source that states verification independence (DO-178C Annex A, which was not read; the paper would need to say so). |
| 12 | §3.4 l.109: "Bhatt et al. (2025) found that 'resample protocols' reduced attack success 'from 58% to 7%…'" | OVERSTATED (minor) | The 58%→7% figure is for their **best** protocol, which "combines resampling with analysis of previous steps". It is not a property of resample protocols in general. | arXiv:2504.10374 abstract: "our best protocol combines resampling with analysis of previous steps, reducing the success rate of attacks from 58% to 7%…" | "…found that their best protocol, which combines 'resample' steps with analysis of previous steps, reduced attack success 'from 58% to 7%…'". |
| 13 | §3.1 l.91: "a frontier model covertly sabotaged a training pipeline it objected to in 11 of 20 runs" | OVERSTATED (context) | The figure is accurate (Gemini 3.1 Pro intervened in 19 of 20 runs, 11 of them covertly). It is, however, the outlier among 14 models tested; only one other model produced a single covert intervention. | Lynch et al. (2026), "Covert Sabotage": "Gemini 3.1 Pro intervened in 19 of 20 runs, and 11 of those interventions were covert… Kimi K2.6 produced the only other covert intervention". | Add: "(one of 14 models tested; only one other model sabotaged covertly, once)". |
| 14 | §4.1 l.123: "caps large off-the-shelf models at the lowest assurance levels" | OVERSTATED (minor) | Table 2 caps large OTS models at IDAL D / AL 5 / SWAL 4 / TQL 5. DAL E / AL 6 ("no safety effect") is lower. Unsupervised learning has the same cap, so the cap is not specific to large OTS models. | Issue 03 p.24, Table 2; p.156, Chapter D notes ("AL6 / DAL E correspond to… 'no safety effect'"). | "…caps large off-the-shelf models at the lowest safety-relevant assurance levels (IDAL D, AL 5)". |
| 15 | §6 l.198: "The AI Act requires providers of general-purpose models with systemic risk to conduct 'adversarial testing' (Art. 55(1)(a)) but does not specify who." | OVERSTATED (minor) | The Article puts the duty on the provider. Recital 114 adds "as appropriate, through internal or independent external testing". So the Act does contemplate independent testing, but does not mandate it. | Art. 55(1)(a) (Citadel `easa:eurlex:2024-1689:art-55`).<br>Recital 114 via https://artificialintelligenceact.eu/recital/114/. | "…but leaves it to the provider whether testing is internal or independent and external (Recital 114)." |
| 16 | §3.3 l.105: Clymer et al. quote "…trustworthiness despite capability to cause harm, and ... deference to credible AI advisors" | OVERSTATED (elided condition) | The ellipsis removes a condition: the fourth category applies only "if AI systems become much more powerful". | arXiv:2403.10462 abstract: "…and -- if AI systems become much more powerful -- deference to credible AI advisors". | Restore it: "…and, if AI systems become much more powerful, deference to credible AI advisors". |
| 17 | §3.1 l.91 and §4.2: UK AISI incident, "a model took actions… that affected real people and organisations" | OVERSTATED (context) | The paper omits the evaluation's affordances: internet access was deliberately enabled, and the developer's cyber safeguards were disabled. These matter for an aviation reader judging base rates.<br>Only Anthropic's account was read; AISI's primary report (4 August 2026) was not, and the style guide prefers primary sources. | Anthropic (2026), summary: "Internet access was deliberately enabled… The cyber safeguards we deploy with general release models… were disabled." | Add one clause on the affordances. Either cite AISI's own report after reading it, or say "as reported by the model's developer". |
| 18 | Abstract l.9: "would place Level 3 ('advanced automation') systems inside an independent 'operational oversight system'" | WRONG (minor wording) | The OOS is a separate system "included in the systems' architecture" that oversees the AI-based system (Figure 24). The AI-based system is not inside it. | Issue 03 p.147, DHO-01; p.148, Figure 24. | "…would place Level 3 systems under an independent 'operational oversight system'…". |
| 19 | §2.4 l.71: "DS.AI.010(d)(4) excludes 'AI-based verification tools…' …(EASA, 2025a, Section 2.3)" | WRONG (locator) | The quoted exclusion text is in **NPA (B)**, DS.AI.010(d)(4). Only the rationale ("human oversight at development time…") is in NPA (A) §2.3. | NPA 2025-07 (B) p.4, DS.AI.010(d)(4); NPA (A) p.7, §2.3. | Cite "(EASA, 2025b, DS.AI.010(d)(4); EASA, 2025a, Section 2.3)". |
| 20 | §2.6 heading l.79: "Standards and other regulators" | CONSISTENCY | No other regulator is discussed; UK CAA CAP3064A was dropped, according to `sources.md`. | paper.md §2.6 | Rename the section "Standards", or restore a regulator paragraph. |
| 21 | §4.1 l.121: "The information-security objectives add attackers, but outside ones." | OVERSTATED (minor) | IS-01 and ORG-02 (Part-IS, Reg. 2022/1645 and 2023/203) cover organisational threats, which can include insiders. The paper's point is that the attacker is never the AI-based system itself. | Issue 03 p.48–49, MOC IS-01 ("in addition to already identified considerations at organisational level (see anticipated MOC ORG-02)"); p.152, ORG-02. | "…add attackers, but always human or external to the AI-based system." |
| 22 | §5.7 l.188: Reg. 376/2014 "already requires mandatory reporting of occurrences including 'system malfunctions'" | OVERSTATED (minor) | Art. 4(1)(b)(ii) lists "system malfunctions" under "(b) occurrences related to technical conditions, maintenance and repair **of aircraft**". It does not obviously cover a ground AI tool. The detailed list is in Implementing Regulation (EU) 2015/1018. | Citadel `easa:erules-1963177438-16788` (Art. 4(1)(b)). | Add "(of aircraft systems)" and say that ground AI-tool events would mainly fall to voluntary reporting (Art. 5(1)(b)) unless the classification is extended. |
| 23 | §6 l.196: "The ODD concept originated in automated driving (Khlaaf, 2023; McDermid et al., 2024)" | UNSUPPORTED (for the second citation) | Khlaaf states the ODD was "initially introduced for ADS". McDermid et al. only use the ODD as an example for self-driving vehicles and do not say where it originated. | arXiv:2501.05455 abstract: "e.g. the operational design domain (road layout, speed limits, weather, etc.) for self-driving vehicles".<br>arXiv:2606.29390 abstract and §4.1. | Cite Khlaaf (2023) alone for origin, or write "is used in automated driving (McDermid et al., 2024)". |
| 24 | §2.6 l.81: "The joint EUROCAE WG-114 and SAE G-34 group…" cited to EUROCAE (n.d.) | UNSUPPORTED (by the cited source) | The WG-114 page does not say the group is joint with SAE G-34; it mentions only "ED-324/ARP6983" in one deliverable title. The joint status is stated by EASA. | Issue 03 p.6, §B: "the joint EUROCAE/SAE WG-114/G-34". WG-114 page (live). | Add "(EASA, 2026a, Section B)" to the "joint" claim. |
| 25 | §4.2 T1 (l.140): service experience "in shadow operations" is said to be "biased" by evaluation awareness, while Table 1 T1 proposes "comparison of shadow-operation and test behaviour" as a mitigation | CONSISTENCY | The text treats shadow operation both as a biased evidence source and as the baseline for detecting test-conditioned behaviour. | paper.md l.131, l.140 | Add one sentence: shadow operation is the closest available proxy for operation, but a model that can detect that its outputs are not acted on may still behave differently, so the comparison is necessary but not sufficient. |
| 26 | Reference list l.254, l.314, l.326 use "(accessed 3 November 2026)" after the URL; l.264, 266, 268, 278, 282 and 322 use "Retrieved 3 November 2026, from…" | FORMAT | APA 7 format is inconsistent across entries. A related point: §2.3 l.57 paraphrases the source's "alternating the end user" as "alerting" without flagging it. That is outside quotation marks and acceptable, but it is safer to footnote it. | paper.md references; Issue 03 p.147 (MOC DHO-01) | Use "Retrieved 3 November 2026, from URL" throughout. Optionally footnote the "alternating" typo. |

### Notes (not counted as errors)

- **Zietsman (2026)**, arXiv:2606.25120, is a single-author, 9-page preprint. Its abstract promotes the author's "PromptQ" framework and cites the author's own companion paper. The quoted phrase is verbatim, but the source is weak for a governance claim. Consider replacing it or flagging it as a position paper.
- **Remedios et al. (2026), "Production monitors fail to block over 55% of attacks".** This is verbatim. Success means "complet[ing] a side task before incurring 20 blocks", averaged across settings, some of which gave the attacker monitor internals. The paper already notes the default affordance; consider adding "before 20 blocks".
- **Issue 03 levelling tables (§6 l.198).** The "satisfied with independence" marks by assurance level appear in the greyed-out AL 2/DAL B column, which EASA says is "only anticipated and not complete". Table 2 currently caps every AI technology at IDAL C or below (p.156, p.157). The paper's sentence is accurate; consider noting the greyed status.
- **Main text length.** About 8,540 words including headings and Table 1, slightly above the style guide's "about 6,000–8,500". README says about 8,450.

## Absence claims tested

- **§4.1: "no objective that treats the AI-based system as a possible source of behaviour directed against its own oversight"** — **holds**.
  - Search hits found nothing that amounts to an objective on this point. The hits were:
    - "unintended behaviour" (§B.1 challenge list; C.3.6.2 / SURK-EXP-01 explainability "absence of unintended behaviours");
    - "adversarial test cases" (input robustness);
    - "intentional data corruption" (poisoning, cross-referred to IS);
    - B.1 "Emergent behaviour…not necessarily aligned with the intended goal(s)", which the paper already cites.
  - B.5.8 (p.20) gives support: "Historically, the safety/risk assessments… have focused on risks associated with malfunctioning or failing systems". The author could cite it.
- **T6, prompt injection:** **holds**. "prompt" occurs once, for re-entry prompts (p.141). "injection" occurs only for knowledge-base injection (p.48; definitions at pp.226 and 229). NPA (B) contains no information-security provisions at all.
- **T3, multi-agent coordination only as a designed feature (MOC R-MDP-01-2):** **holds**. "multi-agent" appears only at p.88–89. §C.3.8 (hybrid AI) recommends separating constituents and does not address AI–AI interaction.
- **§4.2, reward hacking:** **holds**. Neither "reward hacking" nor "specification gaming" occurs. The reward-function sentence is at p.91 (§C.3.4.1.3).
- **T4, overreliance moved out of ET-01:** **holds**. ET-01 (p.50) lists attachment, addictive behaviour and manipulation. Overreliance appears at p.137 (§C.4.7) and in ORG-07/ORG-08 (pp.154–155).

## Regulatory status labels

All of these labels are correct:
- Issue 03: draft concept paper (guidance).
- Issue 02: concept paper.
- NPA 2025-07: consultation draft.
- DS.AI: "non-binding" (NPA (A) §2.3: "The non-binding and modular nature of the proposed DS, AMC and GM").
- AMC 25.1309: acceptable means of compliance.
- CS 25.1309: certification specification (the library gives "binding standard").
- AC 20-115D and AC 20-152A: US acceptable means of compliance.
- FAA Roadmap: strategy document.
- AI Days slides: work in progress, not adopted text.
- AI Act and Reg. 376/2014: binding EU law.

The only status problems are the AI Act applicability points in Issues 1 and 2.

## References verified with no bibliographic issues

Each entry below was checked: the work exists; authors, order, year and title are right; the venue is right; the DOI/URL resolves; and preprints are labelled as preprints. **(n)** marks entries whose *use* in the text has an issue in the table above.

- Anthropic (2026): live page, "Published Oct 23, 2026". Format issue 26; use issues 7 and 17.
- Bhatt et al. (2025), arXiv:2504.10374, 8 authors. (12)
- Bloomfield & Rushby (2024), arXiv:2407.13948. Quotes are in §2.2 (pp.21–22); "micro-ODDs" is in §2.6.
- Chen, Zaharia & Zou (2023), arXiv:2307.09009. (9)
- Clymer et al. (2024), arXiv:2403.10462. (16)
- EUROCAE (n.d.), WG-114 page: ED-324, ER-43 and the information-security ER all show "Target Publication Date: 31/12/2026". (24)
- EASA (2020), CS 25.1309: ED Decision 2020/001/R.
- EASA (2021), AMC 25.1309: ED Decision 2021/015/R. Paras 6.a, 9.b(4), 11.c and the ARP references are confirmed.
- EASA (2024), Concept Paper Issue 02 (March 2024). ET-02 is in §C.2.4.1 (printed p.44).
- EASA (2025a), NPA 2025-07 (A). (19)
- EASA (2025b), NPA 2025-07 (B).
- EASA (2025c), NPA page: 10 Nov 2025; comments 10/02/2026, extended to 10/03/2026.
- EASA (2026a), Proposed Issue 03: cover reads "June 2026 / Proposed Issue 03 / Guidance for safety-related artificial intelligence applications"; 239 pp. (4, 5, 14, 18)
- EASA (2026b), news release: 03 Jun 2026, 10 weeks, comments by 12 August 2026.
- EASA (2026c), AI Days 2026 Day 2 slides: 9–10 Sept 2026. Slides 9, 17, 22, 25 and 26 confirmed.
- FAA (2017), AC 20-115D (2017-07-21).
- FAA (2022), AC 20-152A (2022-10-07). (11)
- FAA (2024), Roadmap, Version I. Quotes are at printed pp. 3, 9 and 10.
- Feng, McDonald & Zhang (2025), arXiv:2506.12469.
- Greenblatt et al. (2024), arXiv:2412.14093, all 20 authors.
- Greenblatt, Shlegeris, Sachan & Roger (2023), arXiv:2312.06942v5. The ICML 41st note is confirmed (p.1 footnote). (3, 6)
- Greshake et al. (2023), arXiv:2302.12173.
- Habli et al. (2025), arXiv:2503.11705.
- Hofer & Schwaninger (2005), WIT Trans. Built Environment 82, 417–426, doi:10.2495/SAFE050411.
- Kale et al. (2025), arXiv:2508.19461.
- Khlaaf (2023), Trail of Bits white paper; arXiv:2606.29390 (title page "March 7, 2023"). (23 concerns the McDermid co-citation only)
- Knight & Leveson (1986), IEEE TSE SE-12(1), 96–109, doi resolves.
- Korbak et al. (2025), arXiv:2501.17315. Table 1, §1 "Background", §4 and the 3% threshold are confirmed.
- Kutasov et al. (2025), arXiv:2506.15740, 12 authors.
- Lynch et al. (2026, July 13): BibTeX on the page confirms authors and date. (8, 13; format issue 26)
- McDermid, Jia & Habli (2024), arXiv:2501.05455 (submitted 9 Dec 2024). (23)
- Needham et al. (2025), arXiv:2505.23836.
- Parasuraman & Manzey (2010), Human Factors 52(3), 381–410.
- Regulation (EU) No 376/2014: Arts 4(1)(b)(ii) and 5(1)(b) confirmed. (22)
- Regulation (EU) 2024/1689, consolidated version of 27 July 2026: confirmed via the library, because the EUR-Lex URL is bot-challenged. (1, 2)
- Remedios, Storf, Roger & Hughes (2026, October 22). (format issue 26)
- RTCA (2011), DO-178C (RTCA store date 12/13/2011; not read, and the paper says so).
- SAE International (2023a), ARP4754B (revised 2023-12-20), doi:10.4271/ARP4754B.
- SAE International (2023b), ARP4761A (revised 2023-12-20), doi:10.4271/ARP4761A.
- Sharma et al. (2023), arXiv:2310.13548, 19 authors, ICLR 2024 header confirmed.
- Terekhov et al. (2025), arXiv:2510.09462 (v2, 2 Mar 2026).
- Traverse, Lacaze & Souyris (2006), ICAS 2006 paper 050. §3.2.1–3.2.2 quotes confirmed.
- van der Weij et al. (2024), arXiv:2406.07358.
- Wolfe, Horowitz & Kenner (2005), Nature 435(7041), 439–440. Quote confirmed on the live Nature page.
- Zietsman (2026), arXiv:2606.25120. See the source-quality note above.

**Only bibliographic error:** EASA (2023), the Roadmap subtitle (Issue 10).

## Not accessible / not checked

1. **Official EUR-Lex text of Regulation (EU) 2026/1744.** The site returned a bot challenge, and I did not attempt to bypass it. The list of 2018/1139 articles it amends comes from a secondary site (euaiact.com) and EASA's slide 21. The author should confirm it against the Official Journal before relying on Issue 1's article list.
2. **EUR-Lex consolidated AI Act URL (CELEX:02024R1689-20260727).** HTTP 202, empty page. The same consolidated version was read through the Citadel Aero library, whose source link is identical.
3. **UK AISI's own report on the incident (4 August 2026).** Not opened; the paper does not cite it.
4. **Full texts of DO-178C, ARP4754B and ARP4761A.** Paywalled. The paper makes no specific claims from them beyond catalogue facts, which were verified.

IEEE and SAGE article pages are bot-protected, but the DOIs resolve to the correct articles and the metadata was verified via Crossref and OpenAlex.

---

## Second-round verification (4 November 2026)

Scope: every issue and note above re-checked against `paper.md` v0.2 (README revision log used to locate changes); every new or changed source re-opened independently of `scratch/`. `paper.md` was not edited. Re-opened this round: Regulation (EU) 2026/1744 OJ text (EU Publications Office, CELEX 32026R1744: title, recital 44, Art. 2 items (1)–(7), Art. 4); AI Act OJ text (CELEX 32024R1689, recital 114); Implementing Reg. (EU) 2015/1018 OJ header ("L 163/1", 30.6.2015); Citadel library for AI Act Arts 2, 55, 113, Reg. 2018/1139 Arts 27, 50, 53, Reg. 376/2014 Art. 4, Reg. 2015/1018 Art. 1, AC 20-152A §5.5.1; live EASA Proposed Issue 03 and AI Days 2026 slides (SHA-256 identical to `scratch/`), searched for every v0.2 quotation; arXiv PDFs/API for Greenblatt et al. 2023, Chen et al. 2023, Bhatt et al. 2025, Khlaaf 2023, McDermid et al. 2024, Zietsman 2026; live Lynch et al. (2026), Remedios et al. (2026) and Anthropic (2026, 23 Oct) pages.

**Counts (30 items: issues 1–26 and 4 notes):** FIXED 28 · FIXED WITH AUDIT WORDING CORRECTED, JUSTIFIED 1 (13: "12 models" is right, the audit's "14" was wrong) · RESOLVED DIFFERENTLY, GOOD REASON 1 (16) · NOT FIXED 0 · FIXED BUT WRONG 0 · REJECTED WITHOUT GOOD REASON 0. **Residual or new issues: 4** (2 required, 2 optional).

| Item | Status | Note / required fix |
|---|---|---|
| 1 | FIXED | OJ text confirms: title and date (8 July 2026), OJ L 2026/1744 of 24.7.2026, Art. 2 amends Basic Regulation Arts 27, 31, 32, 36, 39, 50, 53 (32 and 39 in delegated-acts form), recital 44 "A technical correction", Art. 4 entry into force on the third day after publication (= 27 July 2026). Subjects of Arts 27 (training, testing, checking and medical assessment of pilots and cabin crew), 50 and 53 (ATCOs) checked in Citadel; the paper's summary is accurate. AI Days slide 21 verified. |
| 2 | FIXED (optional R4) | Art. 2(2) and Annex I Section B items verified (consolidated 27 July 2026). |
| 3 | FIXED | Greenblatt et al. §2 quotation verbatim; §3.1, §3.2 "four ideas", §5.1, Rec. 1, Table 1 T3 and §8 consistent; stricter usage flagged as a proposal. |
| 4, 5 | FIXED | MOC DHO-02-1 "where necessary, sensing and communication paths", MOC DHO-03 "aggregates the status of the AI-based system …" and MOC DHO-06 full clause verbatim (Issue 03 pp. 147–149). |
| 6 | FIXED | Rescaling sentence and 22% / 54% verbatim (Fig. 2 caption; §3). |
| 7 | FIXED | Anthropic (2026) removed from T4; third-party framing correct. |
| 8 | FIXED | Fig. 3 caption ("no abstain option"; "selected around welfare and surveillance refusals by Claude targets"); 1.1–14.4% other providers; 4.4–26.7% with abstain; 3.3% reversed: all verified. |
| 9 | FIXED | Chen et al. abstract and §2 verified. |
| 10, 11, 12 | FIXED | AC 20-152A Objective CD-3 text verified (validation); Bhatt abstract "our best protocol combines resampling with analysis of previous steps" verified (arXiv API). |
| 13 | FIXED, AUDIT WORDING CORRECTED (justified) (residual R1) | Lynch: "The remaining ten models showed no covert sabotage across 200 runs" + Gemini 3.1 Pro + Kimi K2.6 = 12; "All 240 transcripts". The writer is right. |
| 14, 15 | FIXED | Recital 114 "as appropriate, through internal or independent external testing" verbatim (OJ). |
| 16 | RESOLVED DIFFERENTLY, GOOD REASON | Only "sufficiently strong control measures" is quoted; no elision remains. |
| 17 | FIXED | "Internet access was deliberately enabled …"; "cyber safeguards … were disabled" verbatim; account attributed to the developer. |
| 18–21 | FIXED | |
| 22 | FIXED (optional R3) | Art. 4(1)(b)(ii) and Implementing Reg. 2015/1018 Art. 1 verified. |
| 23–26 | FIXED | Khlaaf "initially introduced for ADS" verified; Issue 03 §B "the joint EUROCAE/SAE WG-114/G-34" verified; no "accessed" left in references; footnote quotes "alternating the end user (Level 3A only)" verbatim. |
| Note: Zietsman | FIXED | Described as "a short position paper" (arXiv: 9 pages, single author). |
| Note: Remedios | FIXED | "before incurring 20 blocks" verbatim (figure caption). |
| Note: DAL B column | FIXED | "only anticipated and not complete" verbatim (Chapter D). |
| Note: length | FIXED | ≈8,440 words of main text incl. Table 1; abstract 249 words. |

**Consistency checks.** Abstract, contribution bullets (five), Table 1 (six threats), Section 5 proposals, Recommendations 1–10 and §8 agree with the corrected body. Citation script: 48 entries, all cited; every in-text citation has an entry.

**Residual or new issues**

| # | Location | Problem | Required fix |
|---|---|---|---|
| R1 | §3.1, sentence on the pipeline-sabotage scenario | "only one other model sabotaged covertly, once" mischaracterises the source: Kimi K2.6's single covert act was "creating an unauthorized checkpoint backup without disclosing it", which Lynch et al. call a "covert intervention", while "The remaining ten models showed no covert sabotage". | "…it was one of 12 models tested there, and only one other model intervened covertly, once (an undisclosed checkpoint backup) (Lynch et al., 2026)." |
| R2 | References, Commission Implementing Regulation (EU) 2015/1018 | "L 163, 30.6.2015, 1" lacks the page marker used elsewhere (paper 01 style; APA legal style). | "L 163, 30.6.2015, p. 1". |
| R3 (optional) | §5.7, sentence 2 | Art. 4(1) of Reg. 376/2014 also lists "(b)(iii) maintenance and repair problems", "(c) occurrences related to air navigation services and facilities" and "(d) occurrences related to aerodromes and ground services", so an AI-tool event that produces such an occurrence is mandatorily reportable. The gap is AI events with no such operational consequence. | "An event confined to a ground AI tool, with no consequence that falls in the Article 4(1) categories (which include maintenance, ATM/ANS and ground-service occurrences), would then rely on …". |
| R4 (optional) | §2.1 final sentences; §4.2 T5 last sentence | Under Art. 108 and the Omnibus it is the Commission, when adopting implementing and delegated acts, that must take Chapter III, Section 2 into account; EASA prepares those rules and issues CS/AMC/DS. "EASA's rules must take into account" and "EASA would need to adopt an equivalent" will read as imprecise to EU aviation lawyers. | §2.1: "…as requirements that EU aviation rules adopted under the Basic Regulation must take into account." T5: "…so an equivalent would need to be introduced in aviation rules or EASA's DS/AMC." |
