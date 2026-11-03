# Untrusted by Design: Bringing AI Control into Aviation's Operational Oversight of AI

**Status:** draft v0.1 for author review (3 November 2026). Not peer reviewed. Main text about 8,450 words (including Table 1 and headings; excluding references).

**Files:** `paper.md` (the paper), `sources.md` (verification log for every reference), `scratch/` (downloaded PDFs and web pages, extracted text and page renders used for verification; about 73 MB of third-party material, excluded from git by the folder's `.gitignore`; delete it once you have checked the quotations).

## Abstract

The European Union Aviation Safety Agency (EASA) is moving its guidance on artificial intelligence (AI) towards run-time oversight. Its draft Concept Paper, Proposed Issue 03 (June 2026), would place Level 3 ("advanced automation") systems inside an independent "operational oversight system" that monitors the AI, overrides it and drives it to a safe state (Objectives DHO-01 to DHO-07). In AI-safety terms this is a run-time monitor. Research on "AI control" has studied such monitors under a stricter assumption than aviation's: that the monitored system may itself evade or subvert its monitor, collude with other AI components, or behave differently when evaluated. This paper compares the two. It sets out the EASA texts verbatim and shows that their threat model covers random and systematic failure, distribution shift and outside attackers, but not the monitored system as a source of adversarial behaviour. It reviews experimental evidence, mostly from coding and AI-laboratory settings, that current large language models can evade monitors, recognise evaluations, agree with users against the facts and bias their labels when acting as judges. A gap analysis covers six threats. The paper proposes means of compliance for EASA and EUROCAE: trusted/untrusted classification of monitors, managed dissimilarity, red-team control evaluations, audit budgets sized with human-factors evidence, planted-test monitoring of monitors, sycophancy test methods and occurrence reporting of AI events. In the other direction, it argues that frontier-AI safety cases could adopt aviation's severity-graded assurance, operational design domains, independent verification and continued airworthiness.

## What to check

1. **EASA quotations.** Spot-check the DHO-01 to DHO-07 text (Issue 03, Section C.5.2, pp. 147–150), Table 2 and its notes (p. 24), RU-04 (p. 112), ET-01 and MOC ET-02-2 (pp. 50–52), RO-01 (p. 143) and the levelling table (p. 174) against the PDF in `scratch/easa/`. All locators are in `sources.md`.
2. **A typo in the source.** MOC DHO-01 lists "alternating the end user (Level 3A only)". The paper paraphrases this as "alerting" outside quotation marks. Decide whether to flag it, here or in a consultation response.
3. **Fairness of the gap analysis.** Section 4.1 says I found no objective treating the AI-based system as a source of adversarial behaviour. You may know from EASA meetings or AI Days discussions whether EASA has considered this and scoped it out deliberately. If so, the paper should say so.
4. **AI Days slides.** Statements about RMT.0742 Step 2 (Q2 2027 consultation) and the draft organisational path (output verification by personnel or "non-AI software", reporting of AI-related events) come from conference slides. Confirm they are characterised fairly as work in progress.
5. **Operational realism.** Check Sections 5.4 (audit budgets), 5.7 (which AI events should be reportable) and 7 (ground tools) against airline practice. Nothing in the paper draws on personal experience; add only what published sources support.
6. **Model names in Anthropic sources.** The evidence from Lynch et al. (2026), Remedios et al. (2026) and Anthropic (2026) involves models with names such as "Claude Mythos 5" and "Opus 5". The paper mostly avoids naming models. Confirm you are comfortable relying on these company research posts (not peer reviewed) and on Anthropic's account of the UK AISI incident; AISI's own report was not opened.
7. **Competing interests and AI-assistance statement.** The statement notes that several sources are Anthropic research reports and that you founded Citadel Aero. Adjust the wording if you prefer.
8. **Paywalled standards.** I did not read ARP4754B, ARP4761A or DO-178C. If you have access, consider adding precise references to DO-178C Annex A independence objectives and ARP4761A common-cause analysis (the paper currently relies on AC 20-115D, AC 20-152A and AMC 25.1309).
9. **Voice.** Section 8 uses "I". Change to "this paper" if you prefer an impersonal voice throughout.

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
