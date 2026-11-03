# From RSP to SMS: Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System

**Author:** James Le Cuirot (Citadel Aero)
**Status:** draft v0.2 for author review (3 November 2026), revised after an independent audit (`AUDIT.md`). Not peer reviewed. Not committed by the drafting agent.
**Length:** about 7,100 words of prose plus about 1,600 words in three tables (about 8,700 words of main text, excluding references). This is slightly above the STYLE.md guide of "about 6,000–8,500" once tables are counted. Abstract 250 words. 40 references.

## Files

| File | Contents |
|---|---|
| `paper.md` | The paper (Pandoc Markdown, YAML header per `../STYLE.md`) |
| `sources.md` | Verification log: how each reference was checked, with quotes and locators, the prior-work search log and the v0.2 searches for companion documents |
| `AUDIT.md` | Independent audit of v0.1 (not edited by the author's agent) |
| `README.md` | This summary and the revision log |

## Abstract

Frontier AI developers publish safety frameworks, such as Anthropic's Responsible Scaling Policy, OpenAI's Preparedness Framework and Google DeepMind's Frontier Safety Framework. In 2026 Anthropic also published risk reports, incident investigations and monitoring statistics. Commercial aviation manages operational safety through the Safety Management System (SMS) defined in ICAO Annex 19: four components and twelve elements, run in practice on safety performance indicators, management of change, occurrence reporting and monitoring of routine operations. This paper maps the three frameworks, OpenAI's companion compliance framework and Anthropic's 2026 operational artefacts onto the twelve SMS elements, with the EU General-Purpose AI Code of Practice as a reference point, using documents public on 3 November 2026. The documents contain more SMS-like machinery than a reading of the headline frameworks alone suggests: hazard identification and risk acceptance throughout, incident response plans, security change management and audits, and security detection targets set as goals. The remaining gaps are specific. No developer publishes indicators with targets, alert levels and trends for its safety controls, such as monitors and classifiers. None documents a change process aimed at those controls' settings with hazard assessment. None publishes an occurrence taxonomy or measures detection latency. Training for safety-assurance roles is not described, and independent assurance covers security controls more than safety controls in practice. Anthropic's oversight metrics (coverage, review latency and escalation rate) are safety performance indicators in all but name. The paper proposes twelve AI safety performance indicators for testing and notes practices aviation could adopt. No prior element-by-element mapping was found.

## Main findings in one paragraph

Across 15 rows (the 12 Annex 19 elements, with 3.1 split into occurrence investigation, routine-operations monitoring and internal audit), Anthropic rates "described" on 10, OpenAI on 6 (Preparedness Framework plus its Frontier Governance Framework) and Google DeepMind on 3. Only Google DeepMind has "not described" ratings (key safety personnel; training). The documents contain more SMS than v0.1 credited: OpenAI's incident response plan with severity determination and root-cause investigation, its formal change management and independent security audits; Anthropic's security detection targets (Roadmap goals), evaluation-partner requirements and environment re-certification; and the EU Code's near-miss inputs and pre-release change assessment. The gaps that remain concern the SMS functions applied to the safety controls themselves: indicators with targets, alert levels and trends for monitors and classifiers; a change process aimed at their settings (thresholds, filters, exemptions, scaffold permissions) with hazard assessment; a published occurrence taxonomy and detection-latency measures (2026 latencies ran from about three to eleven months); training for safety-assurance roles; and independent audit of safety controls in practice.

## What to check before this goes further

1. **Annex 19 Amendment 2** becomes applicable on **26 November 2026**. It keeps 4 components and 12 elements, renames three, deletes Standard 3.1.2 and redefines SPI. The paper uses the 2nd edition as its baseline and notes the changes. Source: ICAO State letter AN 8/3.1-25/64, hosted by the Nigerian CAA, read from page images. Decide whether to switch the baseline after 26 November.
2. **Table 2 ratings** remain single-coder judgements. The most debatable are OpenAI "D" on 3.2 (management of change; see revision log W3), Anthropic and OpenAI "P" on 4.1 (security-awareness training only), and OpenAI "P" on 1.3 (a committee rather than a post).
3. **Documents not read.** Anthropic's Frontier Compliance Framework (portal would not open), the SB 53 statute (leginfo 403; an official Senate floor analysis was used) and OpenAI's web pages (403). If you can obtain the FCF, rows 1.4, 3.1a and 3.2 for Anthropic may change.
4. **Doc 9859.** The copy read was hosted by a private foundation (ffac.ch); the reference now cites ICAO and the ICAO Store. Please spot-check the quoted paragraphs (4.3.1.3, 4.4.5.2, 4.4.6.1–2, 9.4.4.1, 9.4.5.8, 9.5.4.3, 9.5.4.15, 9.5.5.4–7) against a licensed copy.
5. **ICAO Annex 6 Part I, 3.3.3** is still seen only via the CAA New Zealand checklist. The text now avoids the ambiguous 1 January 2027 clause.
6. **Regulation (EC) No 300/2008** (§7.2) was checked only in its UK assimilated text.
7. **Transparency bias and source of assistance.** Anthropic publishes most and rates highest, and the AI assistant used is Anthropic's. Both are disclosed.
8. **SPI table (Section 6)** remains a set of proposals; indicator 10 is now credited to OpenAI's framework.
9. **Length.** About 8,700 words including tables. If you want to be strictly within 8,500, the easiest cut is Section 2 (aviation background).

## Open questions

- Is the airline (operator) SMS the right comparator, or would the Part 21 design and production SMS now in 14 CFR Part 5 be closer for a developer that designs, builds and operates its own product?
- Should Anthropic's RSP be rated on the policy alone as well as with its artefacts, to make the transparency effect visible?
- Can coverage, review latency and escalation rate be defined with common denominators across developers? Section 5.1 shows that even one developer's documents report coverage differently.
- Who would "accept" a frontier developer's SMS? The EU AI Office (Art. 55 and the Code) is the nearest analogue.
- Should the SPIs be split by threat model (misuse safeguards versus misalignment monitoring)?
- How should alert levels be set when baselines move with every model and monitor release?

## Ideas for developing it

- **Citadel Aero SMS-for-AI template**: an SMS manual annex for AI systems mapped to Annex 19 (with Amendment 2), 14 CFR Part 5 and ORO.GEN.200; an SPI register based on Table 3; a management-of-change form for model, prompt, scaffold, monitor and threshold changes; and an occurrence classification for AI-related events.
- **Second coder and Delphi round** on Table 2 and the SPI set.
- **Trend series** from successive Anthropic Risk Reports, testing whether Doc 9859-style alert levels would have fired.
- **Companion paper on change management for AI safety controls**, built on the Section 5.2 cases.
- **Obtain the Anthropic FCF** and any Google DeepMind compliance document and re-rate.

## Revision log

### v0.2, 3 November 2026 (response to `AUDIT.md`)

Each audit item was re-checked against the source in this session before changing the text. Details and quotations are in `sources.md` (entries marked "v0.2").

| Audit item | Finding (short) | Action |
|---|---|---|
| W1 | "near misses only as context" was wrong | Removed. §3.5 and §5.3 now say near misses are defined and feed Measures 2.1, 1.3 and 7.6, but no document sets a near-miss reporting duty or indicator. Verified in the Code (Measures 1.3(2), 2.1(1)(a)(ii), 7.6(4), Glossary). |
| W2 | Metrics page also reports 100% offline ingestion | Accepted. §3.2 and §5.1 now report both offline figures with dates and scopes (100% "ingested" on one platform in August; 25%/5% subsampling and "About half of agent scaffold tokens" seen as of 15 July; 31 August expansion) and use the discrepancy as the denominator example. "Do not contradict" removed. |
| W3 | OpenAI PF App. C.3 has formal change management; EU Code M7.6 requires pre-release assessment | Accepted after checking both. Row 3.2 for OpenAI re-rated **P → D** (the process covers "all modifications to systems, applications, and infrastructure" before deployment; the comment notes it is framed as security practice). §5.2, abstract and §9 rewritten: the remaining gap is a change process aimed at safety-control settings with hazard assessment. |
| W4 | Board, not committee, may reverse | Fixed in §3.3 and row 1.2. |
| W5 | Wrong Annex 19 locators | Fixed to "Annex 19, App. 2, 1.1.1(d)" and "App. 2, 4.2(d)". |
| W6 | Doc 9859 uses both "trigger" and "alert level" | Fixed in §1.1 (verified Fig. 4-5 and 9.5.4.15). |
| W7 | EASA AMC version note wrong; complex operators | Verified in Citadel; reference corrected; §2.4 says "for complex operators". |
| W8 | APA 7 author truncation | Tamkin et al. truncated (19 authors, ellipsis, last). |
| O1 | SPI claim overstated | Accepted. Row 3.1, §5.1, abstract and §9 now credit the Roadmap's security detection metrics (as goals for 1 July 2027) and PF App. C.1, and confine the gap to safety controls. Indicator 10 credited to OpenAI ("Time to patching a new known jailbreak"). |
| O2 | Not all four cases were changes | Accepted. §5.2 separates documented changes (filters; threshold) from configuration failures (contractor flag; legacy instructions). |
| O3 | Selective RSP §3.2 quote; prospective controls omitted | Accepted. Full sentence quoted; RL-environment checks, specification and re-certification, pre-merge review and the Roadmap configuration-approval goal added. |
| O4 | ERP comment overstated | Accepted. Row 1.4 cites OpenAI's AIRP, PF 24x7 response, GDM's possible 24/7 response, Anthropic's partner requirements and response procedures; the remaining gap is coordination in advance with interfacing organisations. |
| O5 | Assurance claim overstated | Accepted with one qualification. §5.5 and row 3.1c now credit independent assurance of security controls (PF App. C.3; FGF SOC 2/ISO 27001; GDM penetration testing) and quote RSP §3.6 more fully. **Qualification:** EU Code App. 4.5(1) is conditional ("if internal expertise is inadequate"), so the paper says "where internal expertise is inadequate" rather than that the Code requires regular external reviews outright. |
| O6 | Missing METR caveat on 79% | Added in §3.2 (both caveats quoted). |
| O7 | Training understated | Accepted. Row 4.1 now A = P and O = P (security-awareness training; OpenAI evidence from the FGF), G = N; §5.4 rewritten to cite EU Code App. 4.4(2) and Anthropic's note on reviewers dismissing flags. **Note:** Anthropic's evidence is from its 2024 *planned* ASL-3 safeguards, and the paper says so. |
| O8 | OpenAI artefacts not searched | Accepted and exceeded: the FGF PDF was found on cdn.openai.com and incorporated into OpenAI's ratings. The incident disclosure and OpenAI–METR investigation remain unassessed (403) and the scope note says so. |
| O9 | Detection latency incomplete | Added about seven months for the fourth incident and the first scan's miss; range now about three to eleven months. |
| O10 | §7.2 ignored aviation security testing | Accepted. §7.2 now cites Reg (EC) No 300/2008, Annex II 1.1(12) and 8.1 (verified in the UK assimilated text; EU text not opened) and reframes the proposal as extending that practice to SMS detection. |
| O11 | §7.3 one-sided | Accepted. §7.3 cites Reg (EU) No 996/2010 Art. 16(6) (verified, EU and UK) and limits the comparison to operator-held SMS data; row 4.2 comment adjusted. |
| O12 | "where appropriate" | Fixed in §2.3. |
| O13 | Upward reporting exists | Row 1.2 comment and §5.6 qualified. |
| O14 | Reporter protection exists | Row 1.1 comment now credits RSP §4(4) and OpenAI's Raising Concerns Policy. |
| O15 | Detection-source discussion unbalanced | Added the Risk Report's statement that App. 6.5 incidents were found internally; qualified the AISI case. |
| U1 | Taxonomy claim unchecked against compliance frameworks | FGF read: it determines severity internally but publishes no taxonomy. Claim limited to "the documents assessed"; FCF inaccessibility stated. Row 3.1a for OpenAI re-rated **P → D** on the strength of the FGF's documented incident process. |
| S1 | 31 August post omitted | Added as Anthropic (2026e); used in §3.2, §5.1, §5.2, §5.4 and rows 1.1, 1.4, 3.2. Anthropic reference letters renumbered. |
| S2 | Companion frameworks and SB 53 not considered | FGF included. FCF and SB 53 statute could not be opened; explicit scope note in §1.3 and §8; SB 53 described from an official Senate floor analysis in §3.5. No Google DeepMind compliance document was found. |
| S3 | AI Act binding basis missing | Added Art. 55(1)(c) and Art. 113 (verified via Citadel) in §3.5 and §8. |
| S4 | Amendment 2 SPI definition | Added in §1.1 (verified from page image). |
| S5 | February 2026 Risk Report not mentioned | §3.2 now says the August report is the second; "earlier" wording fixed. |
| N1–N4 | Not accessible | Recorded in §1.3, §8 and `sources.md` section E. Annex 6 wording simplified to avoid the ambiguous clause (N4). |
| R1 | Doc 9859 third-party URL | Removed; reference cites ICAO as publisher with the ICAO Store URL (verified); copy consulted recorded only in `sources.md`. |
| R2, R3 | Hosts not named | Swiss FOCA and Nigerian CAA named in the references. |
| R4, R5 | As W7, W8 | Done. |
| R6 | Retrieval dates | Added to Anthropic (2026a) and (2026b). |
| R7 | Stelling year | **Not changed** to 2026: kept 2025 (version 1, December 2025) and the reference states that version 5 (30 April 2026) was consulted, an option the audit allows. |
| R8 | Favaro & Wright undated | Kept; inferred year recorded in `sources.md`. |
| A7 | Consistency and length | Near-miss inconsistency removed; "framework" scope defined in §4; length stated accurately above (about 8,700 including tables). |

No audit finding was rejected outright. Two were applied with qualifications (O5, O7), one rating went further than the audit's minimum (W3: D rather than P), and one optional change was not made (R7).

### v0.1, 3 November 2026

First full draft.
