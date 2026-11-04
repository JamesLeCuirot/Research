# Just Culture for Machines: Why Penalising Disclosure Teaches Concealment

**Author:** James Le Cuirot (Citadel Aero)
**Status:** working draft v0.4 for author review (4 November 2026): the audited v0.3 text converted to the LaTeX technical-report house style with IEEE numeric references. Not peer reviewed.
**Files:** `paper.tex` and `references.bib` (source of truth; build with `papers/_build/build.sh papers/01-just-culture-for-machines`), `paper.pdf` (built; do not edit), `paper.bbl` (kept for arXiv submission), `sources.md` (verification log for every reference and the literature-search log; entries changed in v0.2 are marked **[v0.2]**), `AUDIT.md` (independent audit and second-round verification; not edited). The v0.3 Markdown source (`paper.md`, `paper.html`) remains in git history.
**Length:** about 7,760 words of main text excluding Table 1 and the Annex 19 footnote (about 8,140 including Table 1), counted as whitespace-separated tokens from §1 to §8 without citation numbers (v0.3, with author–date citations: about 8,040 and 8,490); abstract 248 words; 52 references (51 at conversion, plus Daniels et al. 2026 added under decision A6); 22 pages.

## Abstract

Aviation learned that when reports of error feed punishment, people stop reporting and the hazards stay hidden. Its protected arrangements, among them NASA's Aviation Safety Reporting System, the FAA's Aviation Safety Action Program and flight data programmes, EU Regulation 376/2014 and ICAO Annex 19, keep the data that safety programmes gather, whether reported or recorded, out of blame and enforcement, leave enforcement to independently obtained evidence, and exclude wilful misconduct and gross negligence from protection. This paper argues that AI training faces a similar incentive structure. When a model's own disclosures (its chain of thought, self-reports or confessions) set the reward or penalty for the behaviour they disclose, optimisation acts on the disclosure as well as on the behaviour. A simple argument makes the conditions explicit: if the task reward does not already penalise a misbehaviour, and the model can pair it, at no cost in task reward, with a disclosure the monitor scores no worse than an honest one, then no penalty computed only from the disclosure can make good behaviour score higher than concealed misbehaviour. The argument concerns the ordering of rewards, not what training will reach, but experiments that trained reasoning models against chain-of-thought monitors observed the predicted concealment. OpenAI's confession method, which rewards confessions only for honesty, is in effect a just-culture design. The paper proposes six design principles and five falsifiable predictions, and sets out where the analogy fails: models are not moral agents, and the mechanism is optimisation pressure rather than fear.

## The argument in one paragraph

Aviation protects safety-programme data, whether self-reported (ASRS, ASAP, occurrence reports) or recorded (FOQA). It bars their use for blame while allowing safety action, keeps an independent evidence route open (the FAA's "sole-source" rule), defines exceptions in advance, gives custody to third parties, and measures the reporting flow. In RL training, under four stated conditions (A1–A4 in §4.1), a penalty from a monitor that reads only the disclosure can push disclosed misbehaviour below good behaviour, but it cannot push concealed misbehaviour below good behaviour. The policy has two exits, honesty and concealment, and the penalty rewards both. This concerns reward ordering, not training dynamics. The paper draws its own dividing line by *decoupling cost*: how cheaply the policy can change a signal without changing the behaviour it measures. On that basis it proposes six principles:

- **P1:** protect disclosure channels from any training signal for the disclosed behaviour (a use-based protection, as in aviation).
- **P2:** correct behaviour on evidence the model cannot cheaply change, applied to every episode regardless of disclosure.
- **P3:** reward the accuracy of reports, never their absence.
- **P4:** bound the protection in advance, by type of response rather than by intent.
- **P5:** separate custody of disclosures from training, including staff reporting channels.
- **P6:** track disclosure recall against independently detected misbehaviour.

The cost is stated plainly (§7). Misbehaviour that is visible only in a disclosure, and for which no detector or class-wide fix can be built, stays uncorrected in training and is handled operationally.

## What James should check

1. **Aviation accuracy and tone.** Sections 2.1–2.6 and the left and right columns of Table 1. In particular: the recast S1 (safety-programme data, reported or recorded); the paragraph after Table 1 explaining why P2 departs from aviation's FOQA protection; the Article 16(6) criminal-law carve-out; and the Danish case, now presented as confounded by the change to mandatory reporting.
2. **Corrections to the brief.**
   - (a) Marx (2001) uses four concepts. The error / at-risk / reckless triad is Marx's later model, now sourced to his 2007 PSNet interview.
   - (b) NASA's slide shows both NASA and the FAA funding ASRS.
   - (c) AC 00-46F's waiver is ¶12.3 in the FAA PDF; NASA's briefing calls it "9.c".
   - (d) § 13.401 is in Part 13 Subpart I, not Subpart E.
   - (e) ICAO Annex 19 Amendment 2 applies from **26 November 2026** and renumbers 5.3 → 5.4. Update the chapter citations if the paper is finalised after that date.
3. **Sources seen only in part:**
   - Reason (1997): via GAIN's summary.
   - Marx (2001): via PSNet and GAIN.
   - Dekker (2025): table of contents and publisher description only.
   - OpenAI's Raising Concerns Policy: PDF seen; the web page and its date were not accessible.
   - Greenblatt & Fish (2025) and Dearnaley (2026): blog posts, read in full but not peer reviewed.

   If you hold the books, please check the wording against them and add page numbers.
4. **The formal argument (§4.1).** It is now stated with assumptions A1–A4 and presented as close to definitional. Check that this is clear to aviation readers.
5. **Balance.** The paper cites Anthropic's and OpenAI's reporting policies and several Anthropic studies, and it was drafted with Claude. The AI-assistance statement says so.
6. **Reference style (IEEE numeric since v0.4).** Regulations keep their legal designation in the text (e.g., "14 CFR §91.25", "Art. 16(10)") with the citation number where the source is used. Marx (2001) and Reason (1997) keep their own entries in the reference list although only secondary accounts were seen; the in-text wording ("as cited in", "summary of") and each entry's note say so. Dekker (2025), the ICAO documents (read from copies hosted by national authorities), GAIN (SKYbrary copy) and the EU texts carry similar notes on what was consulted. LessWrong authors are cited by the names shown on the site; "mako yass" is a screen name.

## Open questions

- Where exactly should the P4 line sit for AI? The paper draws it by type of response (no gradient through disclosures; operational responses allowed). Is there a case for any intent-like exception?
- Is ASRS-style **leniency for disclosure** (H4), or Dearnaley's reward for verified hackability reports, ever safe for models, or does it always create a "misbehave, then confess" incentive?
- How much **low-bandwidth selection** (checkpoint choice, halting runs) is safe before it acts like training pressure (H5)?
- How should **decoupling cost** be measured in practice, so that P1 and P2 can be applied to a new signal (for example white-box probes, which read activations rather than text)?
- Should **disclosure custody** (P5) sit with an external body, by analogy with NASA's role? Golchin & Wetter (2026) found that models choose the least strict monitor, so the design of the reporting channel itself matters.

## How to develop it further

- **The experiment (Section 6).**
  - *Setting:* an open-weight reasoning model in coding environments with deliberately hackable tests.
  - *Measurement:* ground truth from held-out tests and exploit-signature detectors; disclosure recall from a frozen monitor never used in training.
  - *Arms:* seven, with H2 matched by the number of episodes corrected and H1 using a CoT-only monitor.
  - *Protocol:* several seeds per arm and pre-registered thresholds. Paper 02 in this repository has a pre-registration that could serve as a model. Compute needs have not been estimated.
  - *Already observed:* H1 has largely been seen already (Baker et al., 2025; Emmons et al., 2025). The new parts are H1 for confessions, and H2–H5.
- **A short practitioner version** for flight safety audiences, and a short AI-safety version focusing on P2 and H2.
- **Possible venues** (to be checked): AI-safety workshops at ML conferences; human-factors or safety-science journals for the aviation framing.
- **Leads not followed up:**
  - McGregor et al. (2024, arXiv:2410.12104) on human flaw reporting.
  - Gomez's 2025 escalation-channel study.
  - The "decoupled confessions" passage of arXiv:2604.13602.
  - Semantic Scholar and OpenAlex searches, which were rate-limited.

## Revision log

### v0.2 (4 November 2026): response to the independent audit (`AUDIT.md`, 3 November 2026)

Every finding was re-checked against the source itself before it was applied. No finding was rejected. Two optional items were applied only in part (n16, n19), for the reasons given.

**Major**

| Item | Finding | Action |
|---|---|---|
| M1 | Formal claim summarised without its conditions | Abstract, §1 bullet and §8 now state the conditions: the task reward does not already penalise the misbehaviour, concealment costs no task reward, the monitor reads only the disclosure, and a disclosure no worse than an honest one is available. They also say the result concerns reward ordering, not training dynamics. §4.1 now lists A1–A4 (A4 defined with "no worse than the best disclosure available with $b_g$"). It adds the auditor's points: the penalty *can* push disclosed misbehaviour below good behaviour (explaining Baker's early improvement), and the quantitative form $\lambda m > T(b_m)-T(b_g)$ for imperfect concealment. It says the result is close to definitional. |
| M2 | Emmons et al. used against its own finding | Full PDF read. §3.4 quotes the full clause, including "iterative optimization against the monitor". It reports the §7 RL result: evasion learned against a weak monitor after hundreds of thousands of episodes, not learned against a symbolic monitor, and "a reason to be cautious". §4.1, §7 and H1 now cite Emmons as supporting evidence. |
| M3 | Danish 15→980 figure confounded | §2.5 quotes "It is punishable not to report an incident in aviation". It says the rise reflects both changes and cannot be attributed to protection alone. The 40–50 figure was dropped, and the Danish figures were removed from P6's aviation basis. |
| M4 | Art. 16(6) quoted without its opening | Quoted from "Without prejudice to applicable national criminal law"; OJ text checked via the EU Publications Office. A new sentence notes that criminal proceedings remain possible unless a Member State extends protection (Art. 16(7)). |
| M5 | "Disclosed misbehaviour is corrected" overclaimed | §7 rewritten with the auditor's wording, plus three mitigations: withdraw or redesign the vulnerable environment class (no per-episode detector needed); operational responses; P4 exceptions decided in advance by a party other than the training team, with the monitorability cost measured. P2 now mentions withdrawing environments. |
| M6 | FOQA inconsistency | S1 recast as "Protected safety-programme data, whether self-reported ... or recorded". §2.2 says FOQA data are "recorded, not self-reported, yet ... also protected", and §2.6 names aviation's actual dividing line. A new paragraph after Table 1 explains the difference. Aviation's protection attaches to *use*; this paper draws its line by *decoupling cost*, and P2 departs from aviation deliberately for telemetry. Aviation's use-based logic is kept for disclosures (P1 now says the protection attaches to a use) and for held-out evaluation telemetry. Abstract and Table 1 FOQA row updated. |
| M7 | Adjacent work missing | Retrieved and verified Greenblatt & Fish (2025) via the LessWrong API, the 2022 mako yass answer, Golchin & Wetter (2026) and Dearnaley (2026). All are cited in §3.7; Golchin & Wetter also appear in §3.3, P5 and §7; Dearnaley in P3; Greenblatt & Fish in §7. The novelty claim (§1, §3.7) now says the idea of not penalising model disclosures is older, and limits the contribution to the institutional mapping, the formal statement and the principles and predictions. |

**Moderate**

| Item | Finding | Action |
|---|---|---|
| m1 | Confession judge's calibration source misdescribed | Now "a confession from an independent instance of GPT-5-Thinking that had not been trained to confess". |
| m2 | Joint 4.36% figure | Replaced with the conditional 74.3% figure (≥50% in 11/12, >90% in 4/12) and the authors' "light RL training" / "proof-of-concept" caveat. |
| m3 | NASA history "begins with" 1974 | Now "NASA's account of the programme's background includes ...". |
| m4 | Reason's definition "as quoted in" GAIN | Now "In ... GAIN Working Group E's (2004, §2.1, Figure 1) summary of Reason (1997) ..."; the quotation is GAIN's §2.1 rendering. |
| m5 | Annex 19 Standard vs Recommendation | §2.4 now says the protection is a Standard for voluntary systems (5.3.1) and a Recommendation for mandatory ones (5.3.2). The Note 1 quotation ("premise of the whole approach") was removed. |
| m6 | Inoculation finding misattributed | §7 now uses the auditor's wording: MacDiarmid for RL framing; Wichers and Tan for the general inoculation finding. |
| m7 | Baker setup qualifiers missing | §1 and §3.4 now say the obfuscation run used a non-frontier agent and a CoT-only monitor (with the authors' remark that simple hacks evaded it only for that reason). §1 now describes the frontier monitor correctly: it read CoT and actions. |
| m8 | ASRS waiver is itself coupling | §4.1: the rules remove the *adverse* dependence on $d$, and the waiver adds a *favourable* one. |
| m9 | Detector comparison ignores false positives | Condition now $\lambda(r-f) > T(b_m)-T(b_g)$, plus "The operative difference is not where the signal comes from but whether the policy can change the signal without changing the behaviour." This became the decoupling-cost criterion used in §4.2 and P2. |
| m10 | Dekker content not disclosed | Text now says "Judging by its chapter titles and publisher's description (the text was not seen)"; the "flowchart" clause was dropped. |
| m11 | Wei & Heim published version | Now cited as *Proc. AAAI* 40(44), 38016–38029, DOI 10.1609/aaai.v40i44.41139 (verified via arXiv journal_ref and doi.org); in-text year 2026. |
| m12 | Mixed monitors; H1 scope | §4.1 adds $M=\alpha M_d(d)+(1-\alpha)D(b)$, linked to Wagner's combined arm. H1 is now restricted to a CoT-only monitor. |
| m13 | P2 omits feedback spillover | P2 Weaknesses now names feedback spillover and Drori et al.'s two mitigations ("Mind"/"Face" models; removing the reinforcing gradient term). Verified in the PDF. |
| m14 | H2 matched recall is a moving target | H2 now matches the number of episodes corrected per round (subsampling detector flags). |
| m15 | Sole-source framing | §1, Table 1 and §4.3 now say the AI rule is adapted from, and stricter than, ASAP, which uses sole-source reports for non-punitive corrective action (¶¶1, 15, 16.1). |
| m16 | Anthropic policy wording; balance | Wording now "an update to which was released internally in February 2026 and posted in March 2026". OpenAI's Raising Concerns Policy added as a comparator after reading its PDF. |

**Minor**

| Item | Finding | Action |
|---|---|---|
| n1 | Skalse quote dropped symbols | Quote removed; now "formalised by Skalse et al., 2022"; reference cites NeurIPS 2022 (PDF footer checked). |
| n2 | "Georgiv" | Corrected to "Georgiev" (PDF byline). |
| n3 | Li et al. published at ICLR 2026 | Reference and in-text year updated (PDF header checked). |
| n4 | Taufeeque et al. published at ICML 2026 | Cited as *Proceedings of the 43rd ICML* (PMLR 306), from the PDF. |
| n5 | Cundy & Gleave, Skaf et al. at NeurIPS 2025 | Optional; applied (PDF footers checked). |
| n6 | OJ citation for Reg 376/2014 | Added "OJ L 122, 24.4.2014, p. 18"; verified via the Publications Office. |
| n7 | ¶A.4 vs ¶18.4 | Exclusion now cited to ¶18.4 (with ¶A.4); the Big Five are listed without quotation marks. |
| n8 | MacDiarmid sabotage task | Now "asked afterwards to write a classifier prompt for detecting reward hacking, the model attempted sabotage 12% of the time". |
| n9 | Krakovna URL redirect | Updated to deepmind.google/blog/... |
| n10 | Group-author abbreviations | Introduced at first use: FAA, ICAO, NASA ASRS, GAIN. FAA and ICAO are also spelled out in §1. |
| n11 | Internal note in Marx reference | Removed. Marx, Reason and Dekker are now handled consistently, with disclosure in the text. |
| n12 | SMS definition | Replaced with Annex 19's Chapter 1 definition. |
| n13 | Undefined ML jargon | Glosses added for GRPO (learns from the model's own current outputs), KL regularisation, AUROC, checkpoint and adapter weights. |
| n14 | Length | Trimmed to ~8,490 tokens including Table 1 (~8,040 excluding); one table row was merged. |
| n15 | ASRS waiver excludes controllers | Short parenthetical added (¶12.3 Note). |
| n16 | Part 193 | Applied in part. § 193.7(d) ("Information obtained by the FAA through another means is not protected") was added to §2.2 and S3. The (b)(3) rationale was left out for length and because Part 193 concerns public disclosure, not enforcement. |
| n17 | Wagner's reasoning-only arm supports the argument | §3.4 now calls it "the disclosure-only case"; §4.1 says the reasoning-only monitor was persuaded. |
| n18 | Triad credited to Marx's later model | Verified: Marx describes "three classes of human fallibility" in a 2007 PSNet interview, now cited (PSNet, 2007). |
| n19 | Reason's "informed culture" | Applied in part: no new claim was made. The paper keeps the attribution to GAIN's summary, because Reason (1997) could not be read to check the auditor's point. |
| n20 | H1 already largely observed | H1 now says so; the untested part is coupling through confession content. |
| n21 | PSNet byline | Author changed to "UC Davis PSNet Editorial Team". |

**Also corrected:** `sources.md` now records § 13.401 in Part 13 Subpart I, not Subpart E. The paper's YAML date and the AI-assistance statement mark the draft as v0.2.

### v0.3 (4 November 2026)

Second-round verification fixes applied by the lead session (see AUDIT.md, "Second-round verification"): all required items applied verbatim as specified by the verifier.

### v0.4 (4 November 2026): LaTeX conversion

The conversion itself changed format only: no argument, number, quotation or claim was changed. The author-decision edits that followed (A3–A6) are listed separately below.

- **Source.** `paper.md` (Pandoc Markdown, APA author–date) replaced by `paper.tex` (house preamble from `papers/STYLE.md`, `techreport.sty`) and `references.bib` (IEEE numeric, `IEEEtran.bst`). Title now "Just Culture for Machines: Why Penalising Disclosure Teaches Concealment"; date line "Working draft v0.4, 4 November 2026. Not peer reviewed."; no keywords or status box.
- **Citations.** Every author–date citation became `\cite` (numbered in order of first use), with locators kept (e.g. [n, §3.2], [n, ¶16.4, Note]); narrative citations read "Baker et al. [n]". Bare locators that referred to a cited work, such as "(§3.2)" or Baker et al.'s "(Table 1)", now carry the citation number so they cannot be confused with this paper's own sections and table. "As cited in" information for Marx (2001) is kept by citing PSNet and GAIN alongside it. Regulations keep their legal designation in the text, now written "14 CFR §91.25" (was "14 C.F.R. § 91.25").
- **Structure and typography.** Numbered `\section`/`\subsection` as before, with `\label`/`\ref` cross-references; bold lead-ins (ASRS, ASAP, FOQA, S1–S6, P1–P6, H1–H5, §7 objections) as run-in `\paragraph` headings; A1–A4 as a list; the §4.1 inequality as numbered Equation (1) (the text has no equation references); Table 1 as a booktabs `tabularx` table with the caption above; large counts via `siunitx` (`\num`); `sources.md` via `\code`. No US spellings were found outside quotations, titles and proper names.
- **Closing text.** "Acknowledgements and AI-assistance statement" and "Disclaimer" replaced by the standard Acknowledgement section from `STYLE.md` (AI assistance, Competing interests, Disclaimer, Materials). The audit sentence reads "checked the references and quotations against their sources" (the template's "references, quotations" without the bracketed "and analysis"). Paper-specific provenance notes (ICAO texts read from copies hosted by national authorities; EU texts via the Publications Office and EASA Easy Access Rules; GAIN via SKYbrary; Reason, Marx and Dekker not seen in full) moved to the `note` fields in `references.bib`.
- **Check 8a (`check_bib.py`).** 51 entries, the same 51 references as the v0.3 list, all cited; no missing or unused keys. 21 OK against Crossref/arXiv. 3 CHECK, all resolved: Dekker (Crossref stores the subtitle separately, so the title match is 0.47), Mitrani Hadida (checker takes "Hadida" as the arXiv surname), Li et al. (ICLR 2026 version cited; arXiv v1 is 2025). 27 NO-ID (regulations, ACs, ICAO, GAIN, books, web pages and blog posts) confirmed field by field against `sources.md`; the three 14 CFR section headings were re-checked in the regulation library (eCFR 2026-10-29). Author lists for arXiv papers, including the full 41-author Korbak et al. and 22-author MacDiarmid et al. lists, come from the arXiv API, except "Georgiev" (Skaf et al.), which follows the PDF byline as recorded in `sources.md`.
- **Check 8b (`compare_text.sh`).** The whole word diff was read. Every difference is citation format (author–date removed, legal designations re-spaced), section numbers now generated by LaTeX, list bullets turned into run-in headings, digit grouping by `siunitx`, the `\code{sources.md}` identifier (dropped by Pandoc's LaTeX reader, present in the PDF), the title block and author footnote, the standard closing text and the reference list. The abstract was compared separately and is identical (248 words). No lost sentence, changed number, dropped table row or altered quotation was found.

**Author decisions applied: A3, A4, A5, A6 (4 November 2026).** These edits are the only changes after the conversion that are not formatting. `compare_text.sh` against the v0.3 Markdown (dfd94b7) shows the conversion differences listed above plus exactly these three additions: the §2.4 footnote, the Daniels et al. sentence in §3.5 and the limitations sentence in §7.
- **A3 (impersonal voice).** No change needed: "I", "we", "our", "us", "my" and "me" occur only inside quotations. The other hits were a `\label`, "US", "i.e." and "(i)".
- **A4 (Annex 19 Amendment 2).** The 2nd edition stays the baseline. A footnote where Annex 19 is introduced (§2.4) states that Amendment 2 applies from 26 November 2026, and lists its changes as verified in the State letter's attached amendment text (redline pages viewed as images):
  - SMS framework component 1 and elements 3.1 and 3.3 are renamed. This is one component and two elements; the decision text said "three elements".
  - Standard 3.1.2 of Appendix 2 is deleted.
  - "Safety performance indicator" is redefined.
  - 5.3 is renumbered 5.4, so the paper's 5.3.1, 5.3.2 and 5.3.4 become 5.4.1, 5.4.2 and 5.4.4.
  - The SMS definition and the quoted Appendix 3 text are unchanged, apart from "the SDCPS" for "each SDCPS".
- **A5 (second ICAO copy).** Every Annex 19 quotation and paragraph number was cross-checked against a second, independently hosted copy (Swiss FOCA/BAZL), and all matched. The two copies are textually identical apart from one extra title page. This is recorded in `sources.md` (ICAO 2016, [v0.4]) and in the reference note.
- **A6 (company sources).** OpenAI and Anthropic research reports and blog posts are kept and labelled in `references.bib` as company research reports, not peer reviewed; affiliations were checked on each PDF's first page.
  - Added Daniels et al. (2026; UMass Amherst, MATS, Google DeepMind) as independent corroboration next to MacDiarmid et al. in §3.5.
  - The Tan et al. note records its ICLR 2026 acceptance (OpenReview record; the camera-ready PDF could not be opened, so the arXiv text stays cited).
  - No arXiv or peer-reviewed versions were found of the blog posts by Wang et al., Hopkins et al. or Wagner et al.
  - A sentence in §7 ("Limits of the evidence") names the results that rest on a single company's account, and where other groups report the same direction.
- **Checks after the decisions.** `build.sh`: 22 pages, no errors, no undefined references, no overfull boxes. `check_bib.py`: 52 entries, all cited, none missing; 22 OK, the same 3 explained CHECKs, 27 NO-ID, no NOT-FOUND.

**Fixes after the independent v0.4 conversion check (`AUDIT.md`, "v0.4 conversion check", 4 November 2026).** The check found the conversion clean. Applied:
- **Required (4d, 4e, 5b).** The §2.4 Amendment 2 footnote now:
  - opens its list "Among other changes" and also names the redefinition of "safety information";
  - spells out SDCPS (safety data collection and processing system);
  - uses double quotation marks for its verbatim quotations;
  - is marked at the end of the first sentence of §2.4, not directly after "Annex 19".

  The other changes in the amendment are recorded in `sources.md` under ICAO (2025): redefined "safety performance", new "safety objective", trimmed "safety performance target", replaced Appendix 2 3.1.1.
- **Optional (applied).**
  - The §7 limitations sentence lists Wichers et al.'s inoculation results among the Anthropic results that Tan et al. corroborate.
  - Emmons et al. (Google DeepMind and Google) and Krakovna et al. (DeepMind blog) are labelled as company outputs, as the OpenAI and Anthropic entries are.
  - The bib header comment now gives 52 entries, and the `sources.md` header the current version.
  - Shared items (PDF author metadata, footnote links, sorted and compressed citations, `et~al.`, braced note fields) were done centrally and are not repeated here. The Materials URL is unchanged.
- **Checks after these fixes.** `build.sh`: 22 pages, no errors, no undefined references, no overfull boxes. `check_bib.py`: 52 entries, all cited, none missing; 22 OK, the same 3 explained CHECKs, 27 NO-ID, no NOT-FOUND.
