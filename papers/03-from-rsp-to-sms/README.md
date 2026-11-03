# From RSP to SMS: Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System

**Author:** James Le Cuirot (Citadel Aero)
**Status:** draft v0.1 for author review (3 November 2026). Not peer reviewed. Not committed.
**Length:** about 7,000 words of prose plus about 1,500 words in three tables (about 8,500 words of main text in total, excluding references). Abstract 244 words. 33 references.

## Files

| File | Contents |
|---|---|
| `paper.md` | The paper (Pandoc Markdown, YAML header per `../STYLE.md`) |
| `sources.md` | Verification log: how each reference was checked, with quotes and locators, plus the prior-work search log |
| `README.md` | This summary |

## Abstract

Frontier AI developers publish safety frameworks, such as Anthropic's Responsible Scaling Policy, OpenAI's Preparedness Framework and Google DeepMind's Frontier Safety Framework. During 2026 Anthropic also began to publish operational artefacts: periodic risk reports, incident investigations and monitoring statistics. Commercial aviation manages operational safety through the Safety Management System (SMS) defined in ICAO Annex 19: four components and twelve elements, run in practice on safety performance indicators, management of change, occurrence reporting and the monitoring of routine operations. This paper reads the three frameworks, Anthropic's 2026 operational artefacts and the safety and security chapter of the EU General-Purpose AI Code of Practice against the twelve SMS elements, using only documents public on 3 November 2026. Hazard identification and risk assessment are well described in all three frameworks. Safety assurance and safety promotion are much less developed. The gaps that matter most are safety performance indicators with targets, alert levels and trend analysis; a prospective change-management process for safeguards, monitors, scaffolds and configurations; a defined occurrence taxonomy with detection-latency measures; safety training; and independent audit of practice rather than of documents. Anthropic's proposed oversight metrics (coverage, review latency and escalation rate) are safety performance indicators in all but name. The paper proposes twelve AI safety performance indicators with example alert logic, offered as proposals for testing. It also identifies practices aviation could adopt, including capability thresholds as forward-looking hazard identification and candid public risk reporting. A literature search found no prior element-by-element mapping of this kind.

## Main findings in one paragraph

Across 15 rows (the 12 Annex 19 elements, with 3.1 split into occurrence investigation, routine-operations monitoring and internal audit), Anthropic rates "described" on 10, OpenAI on 5 and Google DeepMind on 3. All three are strong on safety risk management. None describes safety training. None defines operational SPIs with targets and alert levels. None describes a prospective change process for safeguards, monitors, thresholds and configurations, and Anthropic's own Risk Report shows that such changes recur in its incidents (a classifier threshold copied by hand; a flag that disabled blocking and logging for about eleven months; second-stage monitor filters changed without measuring recall). Anthropic's 2026 incident investigations are a strong occurrence-investigation function in practice (blameless approach, wide retrospective search, independent METR investigation, public revision of preliminary findings) but no framework has an occurrence taxonomy or detection-latency measure. The EU Code of Practice is structurally the closest document to an SMS.

## What to check before this goes further

1. **Annex 19 Amendment 2.** It becomes applicable on **26 November 2026**, three weeks after this draft. It keeps 4 components and 12 elements but renames three, deletes Standard 3.1.2 (verification against SPIs and SPTs) and moves SPIs and targets into a Note pointing to Doc 9859. The paper uses the 2nd edition as its baseline and notes the changes (Sections 2.2 and 2.3, Table 1). The source is ICAO State letter AN 8/3.1-25/64, obtained from the Nigerian CAA website, with the redline read from page images. Please check this against your own ICAO access or your CAA's material, and decide whether the paper should switch its baseline to the amended text after 26 November.
2. **Table 2 ratings (D/P/N).** These are my single-coder judgements. The ones most open to challenge are: Anthropic "D" on 1.1 (no statement of unacceptable behaviour), 1.3 (RSO as safety manager) and 3.1b (routine monitoring that is partly sampled); OpenAI "D" on 1.3 (SAG) and 3.3; Google DeepMind "N" on 1.3. A second coder, ideally an airline safety manager, would strengthen this.
3. **Transparency bias and source of assistance.** Anthropic publishes far more than the others, so it rates higher, and the AI assistant used to draft this paper is made by Anthropic. The paper says both things (Sections 1.3 and 8, and the AI-assistance statement). Consider whether an independent reader should check the tone of Sections 3.2 and 5.3, which give Anthropic credit.
4. **ICAO Annex 6 Part I, 3.3.3 (FDA programme).** Seen only as reproduced in the CAA New Zealand compliance checklist for Amendment 49 (25 August 2025). Paragraph numbers and thresholds have changed across amendments. Please confirm against the current Annex 6 Part I.
5. **Doc 9859 copy.** The 4th edition PDF used is hosted by a third party (ffac.ch). Paragraph numbers quoted (4.3.1.3, 4.4.5.2, 4.4.6.1–2, 9.4.4.1, 9.4.5.8, 9.5.4.3, 9.5.4.15, 9.5.5.4–7) should be spot-checked against your own copy.
6. **OpenAI.** openai.com returned 403 throughout, so Preparedness Framework v2 (15 April 2025) is assessed as the current version. Secondary trackers mention an OpenAI "Frontier Governance Framework" (May 2026), not seen. Please check whether anything newer should be included.
7. **The SPI table (Section 6).** All twelve indicators and every example threshold are proposals. Check that the leading/lagging labels and alert logic read correctly to an airline SMS practitioner, and that the analogies (smoke-detector test; "change process that covers a new aircraft type but not procedures") are ones you are comfortable with.
8. **Competing-interests line.** The paper states that you founded Citadel Aero, which builds AI tools for aviation. It does not mention your airline role or employer. Decide whether you want a short author note giving your SFO/FSO background (STYLE.md allows it).
9. **Title split.** The YAML uses title "From RSP to SMS" and subtitle "Reading Frontier AI Safety Frameworks Through ICAO's Safety Management System". Change if you prefer a single title.

## Open questions

- Is the airline (operator) SMS the right comparator, or would the Part 21 design and production SMS that 14 CFR Part 5 now covers be a closer analogy for a developer that designs, builds and operates its own product?
- Should Anthropic's RSP be rated twice, once on the policy alone and once with its artefacts, to make the transparency effect visible?
- Can coverage, review latency and escalation rate be defined with common denominators so that developers can be compared, or are they useful only within one organisation over time?
- Who would "accept" a frontier developer's SMS? The EU AI Office under the Code of Practice is the nearest analogue; the paper does not go further.
- Should the SPIs be split by threat model (misuse safeguards versus misalignment monitoring), since the data sources and failure modes differ?
- How should alert levels be set when baselines move with every model and monitor release? Doc 9859's standard-deviation method assumes stability.

## Ideas for developing it

- **Citadel Aero SMS-for-AI template.** A practical pack for airlines and other aviation organisations that deploy AI tools: an SMS manual annex for AI systems mapped to Annex 19 (including Amendment 2), 14 CFR Part 5 and ORO.GEN.200; an SPI register based on Table 3; a management-of-change form for model, prompt, scaffold and monitor updates; and an occurrence classification for AI-related events. This is the most direct practical output and fits Section 7.4.
- **Second coder and Delphi round.** Re-rate Table 2 with one airline safety manager and one AI-safety researcher; report agreement. A short Delphi on the SPI set would turn the proposals into a consensus starter list.
- **Track the numbers over time.** Anthropic's Risk Reports appear every three to six months. Extract coverage, latency, escalation and detection-rate figures from each to build the first public trend series, and test whether Doc 9859-style alert levels would have fired.
- **Companion short paper on management of change for AI safeguards.** Section 5.2 could stand alone as a focused piece for an AI-safety venue, using Anthropic's disclosed incidents as cases.
- **Feedback.** Consider sharing the draft with people who run these processes (for example the RSO function at Anthropic, METR, or the EU AI Office's code-of-practice team) and with an aviation regulator's SMS specialists.
