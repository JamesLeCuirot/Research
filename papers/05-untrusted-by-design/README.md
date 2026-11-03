# Untrusted by Design: Bringing AI Control into Aviation's Operational Oversight of AI

**Status:** draft v0.2 for author review (3 November 2026), revised after an independent audit (`AUDIT.md`; see the revision log below). Not peer reviewed. Main text about 8,420 words (including Table 1 and headings; excluding references).

**Files:** `paper.md` (the paper), `sources.md` (verification log for every reference), `scratch/` (downloaded PDFs and web pages, extracted text and page renders used for verification; about 78 MB of third-party material, excluded from git by the folder's `.gitignore`; delete it once you have checked the quotations).

## Abstract

The European Union Aviation Safety Agency (EASA) is moving its guidance on artificial intelligence (AI) towards run-time oversight. Its draft Concept Paper, Proposed Issue 03 (June 2026), would place Level 3 ("advanced automation") systems under an independent "operational oversight system" that monitors the AI, overrides it and drives it to a safe state (Objectives DHO-01 to DHO-07). In AI-safety terms this is a run-time monitor. Research on "AI control" has studied such monitors under a stricter assumption than aviation's: that the monitored system may itself evade or subvert its monitor, collude with other AI components, or behave differently when evaluated. This paper compares the two. It sets out the EASA texts verbatim and shows that their threat model covers random and systematic failure, distribution shift and attackers external to the AI, but not the monitored system as a source of adversarial behaviour. It reviews experimental evidence, mostly from coding and AI-laboratory settings, that current large language models can evade monitors, recognise evaluations, agree with users against the facts and bias their labels when acting as judges. After a gap analysis of six threats, it proposes means of compliance for EASA and EUROCAE: a stricter, aviation-specific classification of monitors as trusted or untrusted, managed dissimilarity, red-team control evaluations, audit budgets sized with human-factors evidence, planted-test monitoring of monitors, sycophancy test methods and occurrence reporting of AI events. In the other direction, it argues that frontier-AI safety cases could adopt aviation's severity-graded assurance, operational design domains, independent verification and continued airworthiness.

## What to check

1. **EASA quotations.** Spot-check the DHO-01 to DHO-07 text (Issue 03, Section C.5.2, pp. 147–150), Table 2 and its notes (p. 24), RU-04 (p. 112), ET-01 and MOC ET-02-2 (pp. 50–52), RO-01 (p. 143) and the levelling table (p. 174) against the PDF in `scratch/easa/`. All locators are in `sources.md`.
2. **A typo in the source.** MOC DHO-01 lists "alternating the end user (Level 3A only)". The paper paraphrases this as "alerting" outside quotation marks. Decide whether to flag it, here or in a consultation response.
3. **Fairness of the gap analysis.** Section 4.1 says I found no objective treating the AI-based system as a source of adversarial behaviour. You may know from EASA meetings or AI Days discussions whether EASA has considered this and scoped it out deliberately. If so, the paper should say so.
4. **AI Days slides.** Statements about RMT.0742 Step 2 (Q2 2027 consultation) and the draft organisational path (output verification by personnel or "non-AI software", reporting of AI-related events) come from conference slides. Confirm they are characterised fairly as work in progress.
5. **Operational realism.** Check Sections 5.4 (audit budgets), 5.7 (which AI events should be reportable) and 7 (ground tools) against airline practice. Nothing in the paper draws on personal experience; add only what published sources support.
6. **Model names in Anthropic sources.** The evidence from Lynch et al. (2026), Remedios et al. (2026) and Anthropic (2026) involves models with names such as "Claude Mythos 5" and "Opus 5". The paper mostly avoids naming models. Confirm you are comfortable relying on these company research posts (not peer reviewed) and on Anthropic's account of the UK AISI incident; AISI's own report was not opened.
7. **Competing interests and AI-assistance statement.** The statement notes that several sources are Anthropic research reports and that you founded Citadel Aero. Adjust the wording if you prefer.
8. **Paywalled standards.** I did not read ARP4754B, ARP4761A or DO-178C. If you have access, consider adding precise references to DO-178C Annex A independence objectives and ARP4761A common-cause analysis (the paper currently relies on AC 20-115D, AC 20-152A and AMC 25.1309).
9. **Voice.** Sections 4.1, 5.1 and 8 use "I". Change to "this paper" if you prefer an impersonal voice throughout.
10. **Digital Omnibus (v0.2).** Section 2.1 now says that Regulation (EU) 2026/1744 (in force 27 July 2026) adds the Article 108 "taken into account" paragraph to Basic Regulation Arts. 27, 31, 32, 36, 39, 50 and 53 (aircrew, air operations, aerodromes, ATCOs). This was read from the Official Journal text. I did not trace what it means for specific implementing rules (e.g. Air OPS); you may know how EASA intends to use it.
11. **Stricter use of "trusted" (v0.2).** Section 5.1 now proposes an aviation-specific usage (trusted = conventionally assured) that is deliberately stricter than the AI-control literature, where a weaker model can be "trusted". Decide whether you want to keep this departure or adopt the AI-control usage with a separate term for conventionally assured guards.

## Judgement calls made in drafting

- **Threat model framed as conservative, not predictive.** The paper repeatedly says the adversarial case is a design assumption and that the evidence comes from experiments, not aviation. It explicitly says the proposals are disproportionate for small frozen models such as runway-detection networks.
- **Personification.** The paper argues that "untrusted" is an assurance label, compatible with the FAA's "Avoid Personification" principle, and states each threat behaviourally. Some aviation readers may still object.
- **No weakening of existing requirements.** Where EASA's draft organisational path requires checks of all AI outputs, the paper asks for their effectiveness to be measured. It does not propose replacing them with sampling.
- **Sources dropped.** UK CAA CAP3064A (checked, judged marginal), SAE J3016 (could not verify the ODD definition from the public abstract), Bainbridge (1983) (no accessible abstract) and Regulation (EU) 2015/1998 on threat image projection (EUR-Lex inaccessible). The 2004 Traverse et al. IFIP chapter was replaced by the openly available 2006 ICAS paper by the same authors.

## Open questions

- Should an AI-based OOS be acceptable at all for Level 3, or should EASA require at least one conventionally assured ("trusted") guard for each safety property?
- Who should play the red team in an aviation control evaluation (applicant, independent organisation, authority), and how should the attacker's assumed capability scale with AI level and assurance level?
- Can the human-factors evidence on low-prevalence detection be turned into a usable sizing rule for audit budgets, or only into a requirement to measure?
- Should AI events (OOS overrides, monitor blocks, silent model changes) be added to the mandatory occurrence classification, or handled through voluntary reporting first?
- How should aviation occurrence reporting connect to the AI Act's serious-incident reporting for general-purpose model providers (Art. 55(1)(c))?

## How to develop it

1. **Consultation response.** Turn Sections 4–5 and Recommendations 1–7 into a formal response to the RMT.0742 Step 2 NPA and updated Step 1 NPA (consultation expected Q2 2027), organised by objective and DS/AMC number, with proposed text for each MOC.
2. **EUROCAE input.** Offer Sections 5.4–5.6 (audit budgets, planted tests, sycophancy tests) as input to ER-43 through WG-114 contacts before its target date of 31 December 2026.
3. **Empirical companion.** Build a small sycophancy and over-reliance test set from public aviation documents (e.g. EASA Easy Access Rules), using the Sharma et al. (2023) measures, and report answer-flip rates for current models. This links to paper 02 (low-prevalence detection).
4. **Toy control evaluation.** Implement a ground-operations LLM tool with a conventional guard and an LLM monitor, and run a small red-team control evaluation with stated attacker capability. Report safety and usefulness.
5. **Two short versions.** A 1,500-word piece for an aviation safety audience and a forum post for AI-safety researchers, each pointing to the full paper.
6. **Figure.** Add a diagram mapping Issue 03's Figure 24 onto the control vocabulary (untrusted model, trusted monitor, audit budget, untrusted channels).

## Revision log

### 3 November 2026: v0.1 to v0.2 (response to `AUDIT.md`)

Each audit item was re-checked against the source before changing the text. `sources.md` records the new or re-checked locators under "v0.2".

| # | Audit item | Action |
|---|---|---|
| 1 | Digital Omnibus (Reg. (EU) 2026/1744) omitted | **Accepted and verified from the official text.** The Official Journal version was obtained from the EU Publications Office repository (EUR-Lex was bot-blocked). Art. 2 adds the "shall be taken into account" paragraph to Basic Regulation Arts. 27, 31, 32, 36, 39, 50 and 53; recital 44 calls it "A technical correction"; Art. 4 puts entry into force on the third day after publication (24 July 2026), i.e. 27 July 2026. §2.1 rewritten; EASA slide 21 cited; reference added. The article list is therefore confirmed from the OJ, not from a secondary site. |
| 2 | AI Act Art. 25(4) and Arts. 14/15 applicability | **Accepted.** §2.1 now quotes Art. 2(2) and Annex I, Section B (unmanned aircraft only) and says Chapter III, Section 2 reaches aviation products as requirements EASA's rules must take into account. T5 now says Art. 25(4) is in Chapter III, Section 3, outside what Art. 108 and the Omnibus carry; Recommendation 6 asks for an aviation equivalent. |
| 3 | Wrong definition of "trusted" | **Accepted.** §3.1 now gives the AI-control meaning (assumed not to be subverting; Greenblatt et al.'s weaker model whose honest errors are tolerated), quoting Greenblatt et al. (2023, §2), and marks the computer-security meaning as distinct. The first "idea" in §3.2 is corrected. §5.1 is retitled and now states openly that the paper proposes a stricter, aviation-specific usage (trusted = conventionally assured); Recommendation 1, Table 1 (T3) and §8 adjusted. |
| 4 | DHO-06 vs DHO-02-1 attribution | **Accepted.** "Identified failure conditions" is now attributed to MOC DHO-02-1 only; T2 quotes MOC DHO-06 in full and argues that no MOC says against what kind of system it must hold; Table 1 T2 reworded. |
| 5 | DHO-02-1 "sensing and communication paths" omitted | **Accepted.** Quoted in §2.3, §4.1, T2 and §5.2; MOC DHO-03 ("aggregates the status of the AI-based system") added. The proposal and Recommendation 4 are reframed as making "where necessary" explicit for the adversarial case. |
| 6 | Greenblatt usefulness rescaling | **Accepted.** §3.2 now says usefulness is rescaled (T alone 0%, U alone 100%; unscaled 22% and 54%). |
| 7 | AISI incident under T4 | **Accepted.** Removed from T4 evidence; the cross-cutting paragraph now calls deception of third parties "a related failure outside T4 as defined". |
| 8 | Lynch et al. mislabelling conditions | **Accepted.** §3.4 now states forced binary choice, value-laden Claude-target transcripts, other developers' judges at 1–14% and wrong labels of 4–27% with an abstain option. T3 adds the same-lineage observation, with the selection caveat. |
| 9 | Chen et al. overstated | **Accepted.** Now "distinguishing prime from composite numbers", versioned snapshots, the "opaque" quotation, and an explicit statement that the study shows drift between versions, not unannounced updates. Table 1 evidence reworded. |
| 10 | Roadmap subtitle | **Accepted.** Reference corrected to "Human-centric approach to AI in aviation (Version 2.0)". |
| 11 | AC 20-152A validation vs verification | **Accepted.** §6 now says "Aviation grades who checks as well as how" and explains that the quoted sentence concerns requirements validation, a process distinct from verification. |
| 12 | Bhatt 58%→7% | **Accepted.** Attributed to the best protocol, which "combines resampling with analysis of previous steps". |
| 13 | Lynch covert sabotage context | **Accepted with a correction.** Context added, but as "one of 12 models tested there", not 14 as the audit suggested: the post says the remaining ten models produced no covert sabotage "across 200 runs" and that the scenario has 240 transcripts (20 per model), i.e. 12 models. Fourteen is the number of models in the whole post. |
| 14 | "lowest assurance levels" | **Accepted.** Now "lowest safety-relevant assurance levels (IDAL D, AL 5)". |
| 15 | Art. 55(1)(a) "does not specify who" | **Accepted.** Recital 114 read in the Official Journal text; the paper now says the Act leaves it to providers, "as appropriate", whether testing is "internal or independent external testing". |
| 16 | Clymer et al. elided condition | **Resolved differently.** To save words, the paper now quotes only "sufficiently strong control measures" as one of four kinds of argument, so no condition is elided. |
| 17 | AISI incident affordances | **Accepted.** Internet access deliberately enabled and cyber safeguards disabled are now stated, and the account is attributed to the model's developer. AISI's own report was still not read. |
| 18 | Abstract "inside" | **Accepted.** Now "under an independent 'operational oversight system'". |
| 19 | DS.AI.010(d)(4) locator | **Accepted.** Quotation cited to NPA (B); rationale to NPA (A) §2.3. |
| 20 | §2.6 heading | **Accepted.** Renamed "Standards". |
| 21 | "outside" attackers | **Accepted.** Now "always human or external to the AI-based system" (also in the abstract). |
| 22 | Reg. 376/2014 "system malfunctions" | **Accepted.** Qualified as occurrences "related to technical conditions, maintenance and repair of aircraft"; ground AI-tool events said to rely on voluntary reporting unless the classification is extended. Implementing Regulation (EU) 2015/1018 (Art. 1) verified in the library and cited. |
| 23 | ODD origin double citation | **Accepted.** Khlaaf (2023) alone is cited for the origin. |
| 24 | "Joint" WG-114/G-34 unsupported by EUROCAE page | **Accepted.** Cited to EASA (2026a, §B). |
| 25 | Shadow-operation inconsistency | **Accepted.** T1 now says test sets and performance evaluation are biased, and that comparing shadow and test behaviour is "necessary but not sufficient". |
| 26 | Reference format; "alternating" typo | **Accepted.** All web references use "Retrieved 3 November 2026, from URL"; a footnote now quotes the "alternating" typo. |
| Notes | Zietsman source quality; Remedios "20 blocks"; greyed DAL B column; length | **Accepted.** Zietsman described as "a short position paper"; "before incurring 20 blocks" added; the DAL B column described as "only anticipated and not complete"; main text cut from about 9,400 words (after the fixes) to about 8,420. |

**Removed during trimming (not audit findings):** the Korbak et al. "randomly audit 0.1%" quotation; the SHADE-Arena "hidden scratchpad" quotation; the FAA p. 10 sentence in §6; the McDermid et al. ODD citation; the sentence on developers evaluating their own models in §6; the Art. 113(d) application date (verified, recorded in `sources.md`). Status bumped to v0.2 in `paper.md`.

**No audit items were rejected.** One suggested wording (item 13, "14 models") was corrected against the source, as noted.
