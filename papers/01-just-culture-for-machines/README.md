# Just Culture for Machines: Why Penalising Disclosure Teaches Concealment

**Author:** James Le Cuirot (Citadel Aero)
**Status:** draft v0.1 for author review (3 November 2026). Not peer reviewed. Not committed.
**Files:** `paper.md` (source of truth), `sources.md` (verification log for every reference and the literature-search log).
**Length:** about 8,000 words of main text excluding Table 1 (about 8,500 including it); 44 references.

## Abstract

Aviation learned that when reports of error feed punishment, people stop reporting and the hazards stay hidden. Its response was a set of protected reporting arrangements, among them NASA's Aviation Safety Reporting System, the FAA's Aviation Safety Action Program and flight data programmes, EU Regulation 376/2014 and ICAO Annex 19. These separate the channel through which people disclose from the channel through which they are held to account, and they exclude wilful misconduct and gross negligence from protection. The paper argues that AI training faces the same incentive structure in formal terms. When a model's own disclosures (chain of thought, self-reports, confessions) set the reward or penalty for the behaviour they disclose, optimisation acts on the disclosure as well as the behaviour, and concealment is often the cheaper way to raise reward. A simple argument shows that, where concealment is possible, a penalty computed only from a disclosure can never make good behaviour outscore concealed misbehaviour. Experiments training reasoning models against chain-of-thought monitors show the predicted obfuscation, and OpenAI's confession method is in effect a just-culture design. The paper proposes six design principles (P1–P6), five falsifiable predictions (H1–H5) and an experimental design, and sets out where the analogy fails.

## The argument in one paragraph

Aviation's protected-reporting rules share six features: a designated disclosure channel; a ban on using disclosures for blame while allowing safety action; an independent evidence route that stays open (the FAA's "sole-source" rule); exceptions defined in advance; custody by a third party; and measurement of the reporting flow. In RL training, a penalty computed from a disclosure re-ranks disclosed against concealed misbehaviour but never makes good behaviour beat concealed misbehaviour (Section 4.1). The paper therefore proposes: **P1** protect disclosure channels from any training signal for the disclosed behaviour; **P2** correct behaviour on independent evidence applied to all episodes regardless of disclosure ("a disclosure may tell you where to look, but must not decide which episodes are corrected"); **P3** reward the accuracy of reports, never their absence; **P4** bound the protection in advance, by type of response rather than by intent; **P5** separate custody of disclosures from training (including staff reporting channels); **P6** track disclosure recall against independently detected misbehaviour as a leading indicator.

## What James should check

1. **Aviation accuracy and tone.** Sections 2.1–2.6 and the left and right columns of Table 1. In particular: the description of ASAP and the ERC; the FOQA gatekeeper; whether "flight data monitoring" (EU ORO.AOC.130) is the right European term to pair with FOQA; and whether the Danish 2002 case is fairly presented.
2. **Corrections to the brief.** (a) Marx (2001) uses four concepts (human error, negligence, reckless conduct, knowing violations). The error / at-risk / reckless triad is attributed instead to later healthcare practice (PSNet, 2024). (b) NASA's own slide shows both NASA and the FAA funding ASRS, not the FAA alone. (c) AC 00-46F's waiver is ¶12.3 in the FAA PDF; NASA's briefing calls it "Paragraph 9.c". (d) ICAO Annex 19 Amendment 2 becomes applicable on **26 November 2026** and renumbers 5.3 → 5.4. Update the chapter citations if the paper is finalised after that date.
3. **Partially verified sources** (see `sources.md`). Reason (1997) content is cited through GAIN (2004); Marx (2001) through PSNet and GAIN; Dekker (2025) through its publisher page and table of contents only. If you hold these books, please check the wording against them and add page numbers.
4. **EU text.** Regulation 376/2014 was checked against the EASA Easy Access Rules (via the library) and the legislation.gov.uk copy of the adopted text, because EUR-Lex blocked automated access. The OJ page reference is omitted for that reason.
5. **The formal argument (§4.1).** It is deliberately simple. It holds only under the stated assumptions: the task reward does not penalise the misbehaviour, and concealment is feasible and costs no task reward. Check that the caveats are visible enough for aviation readers.
6. **Reference style.** Regulations are cited in text in legal form (e.g., "14 C.F.R. § 91.25", "Art. 16(10)"). Decide whether the build should list legislation separately.
7. **Disclosure of interest.** Several cited AI studies are Anthropic's, and the drafting assistant is Anthropic's Claude. The AI-assistance statement says so. Decide whether you want that sentence.

## Open questions

- Where exactly should the P4 line sit for AI? The paper argues for drawing it by type of response (no gradient through disclosures; operational responses allowed) rather than by intent. Is there a case for any intent-like exception, such as disclosures of attempted reward tampering?
- Is ASRS-style **leniency for disclosure** (H4) ever a good idea for models, or does it always create a "misbehave, then confess" incentive?
- How much **low-bandwidth selection** (checkpoint choice, halting runs) is safe before it acts like training pressure (H5)?
- Should **disclosure custody** (P5) sit with an external body, by analogy with NASA's role? Who would that be for frontier developers?
- How does the analysis change for **architecturally separated** honesty mechanisms (separate monitor models or adapters) and for **white-box** detectors, which read activations rather than text?

## How to develop it further

- **The experiment (Section 6).** An open-weight reasoning model in coding environments with deliberately hackable tests (as in Baker et al., 2025; Taufeeque et al., 2026). Ground truth from held-out tests and exploit-signature detectors; disclosure recall from a frozen monitor never used in training. Seven arms: task reward only; CoT-monitor penalty (H1); decoupled accuracy-scored confessions; disclosure-triggered vs disclosure-blind correction (H2); confession with a compliance bonus (H3); disclosure waiver at several discounts (H4); a pressure sweep (H5). Several seeds per arm; pre-register thresholds (paper 02 in this repository has a pre-registration that could serve as a model). Compute needs have not been estimated.
- **A short practitioner version** for flight safety audiences ("what AI developers can learn from ASRS"), and a short AI-safety version focusing on P2 (disclosure-blind correction) and H2.
- **Possible venues** (to be checked): AI-safety workshops at ML conferences; human factors or safety-science journals for the aviation framing.
- **Leads not yet followed up:** Greenblatt's Alignment Forum post on offering models a deal to reveal misalignment (adjacent to P4/H4; not cited because not read in full); the reward-hacking survey arXiv:2604.13602, which mentions "decoupled confessions"; Semantic Scholar and OpenAlex searches, which were rate-limited in this session.
