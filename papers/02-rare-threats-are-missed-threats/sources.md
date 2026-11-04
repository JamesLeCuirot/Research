# Sources and verification log: paper 02, "Do LLM Monitors Miss Rare Threats?"

Reference checks were made on **3 November 2026**; the Phase 2 additions (Cain et al., 2013; the Korbak et al. "across space" quote; the provenance table for results) on **4 November 2026**. For each reference: how it was verified, and each claim in `paper.md` it supports, with a verbatim quote or a locator. Quotes are copied from the source text as retrieved (PDF text extraction, publisher page, or a fetch of the HTML page). "Bibliographic only" means the record was confirmed but the content was not opened; such sources are cited only for general background.

Methods used:

- **arXiv API** (`export.arxiv.org/api/query?id_list=...`) for title, authors, dates, comments and abstract; then the **arXiv PDF** downloaded and converted to text with `pdftotext` for quotes and section locators.
- **Crossref API** (`api.crossref.org/works/DOI`) for DOI, title, authors, journal, volume, issue and pages.
- **Europe PMC** (search API and full-text XML) and **PubMed Central** pages (read with WebFetch) for full texts of author manuscripts.
- **OpenAlex** (`api.openalex.org/works/doi:...`) for abstracts where the publisher page was not reachable. This is a secondary index of the publisher's abstract and is marked as such.

---

## Human factors and signal detection

### Wolfe, Horowitz & Kenner (2005), *Nature*, doi:10.1038/435439a
- **Verified:** Crossref record (title "Rare items often missed in visual searches", *Nature* 435(7041), 439–440, May 2005). Full text read in the authors' NIH accepted manuscript, PMC4224304 (https://pmc.ncbi.nlm.nih.gov/articles/PMC4224304/), via WebFetch. The manuscript states it was "Published in final edited form as: Nature. 2005 May 26;435(7041):439–440. doi: 10.1038/435439a." Note: the manuscript's own title is "Rare targets are often missed in visual search"; the reference list uses the published title.
- **Source of the figures:** the primary source (the authors' accepted manuscript), not a secondary summary.
- **Claims supported:**
  - Misses 7% at 50%, 16% at 10%, 30% at 1% prevalence (Sections 1, 2.2): "50% prevalence produced 7% miss errors, typical for laboratory search tasks of this sort." / "10% prevalence produced 16% errors, while at 1% prevalence errors soared to 30%." / "Target prevalence was 1%, 10% or 50%."
  - Task description (Section 2.2): "We compared performance on high and low prevalence versions of an artificial baggage-screening task." / "Observers looked for "tools" among objects drawn from other categories." / "Semi-transparent objects were presented on noisy backgrounds and could overlap."
  - Early quitting (Sections 2.2, 4.3): "Observers abandon search in less than the average time required to find a target."
- Cross-check: Wolfe et al. (2013, Introduction) summarise this study as "miss errors rose from about 7% at 0.5 prevalence to 30% at 0.02 prevalence". The "0.02" differs from the primary source's 1%; the paper uses the primary source.

### Wolfe, Horowitz, Van Wert, Kenner, Place & Kibbi (2007), *JEP: General*, doi:10.1037/0096-3445.136.4.623
- **Verified:** Crossref (136(4), 623–638). Full text read in NIH author manuscript PMC2662480 (https://pmc.ncbi.nlm.nih.gov/articles/PMC2662480/) via WebFetch (first 100,000 of 121,150 characters plus targeted queries).
- **Claims supported:**
  - Robust; criterion shift, not sensitivity (Sections 1, 2.2) — Abstract: "A series of experiments show this prevalence effect is very robust." / "In signal detection terms, the prevalence effect can be explained as a criterion shift and not a change in sensitivity." / "Several efforts to induce observers to adopt a better criterion fail."
  - Remedy (Sections 1, 2.2, 5.5) — Abstract: "However, a regime of brief retraining periods with high prevalence and full feedback allows observers to hold a good criterion during periods of low prevalence with no feedback." Experiment 7: "intermittent short periods of high prevalence with feedback were combined with long periods of low prevalence with no feedback." / "There were no significant effects of prevalence." / "Pooling across epochs, the average miss rate for low prevalence was 0.21 versus 0.18 for high prevalence." / "and false alarms were correspondingly increased (t(36) = 11.49, p = .00)." / "In this experiment, we succeeded in 'curing' the prevalence effect."
  - Failed attempts to move the criterion (Section 2.2, paraphrased) — Abstract: "Several efforts to induce observers to adopt a better criterion fail." Experiment 2: "this massive slowing had no appreciable effect on errors."
  - Faster "no" responses (Section 2.2) — Experiment 2: "observers respond 'no' much more quickly at 2% prevalence than at 50%".
  - Criterion shift as sensible (Section 2.1) — Introduction: "the prevalence effect is a very sensible behavior unless the goal is to minimize misses". (Also: "You will be less likely to call something a target if the a priori probability of a target is lower.")
  - Remedy raised false alarms too (Sections 2.2, 7.4) — Experiment 7 results, quoted above.

### Wolfe, Brunelli, Rubinstein & Horowitz (2013), *Journal of Vision*, doi:10.1167/13.3.33
- **Verified:** Crossref (13(3), 33; Dec 2013). Full text read via PMC3848386 (https://pmc.ncbi.nlm.nih.gov/articles/PMC3848386/) with WebFetch.
- **Claims supported (Section 2.2):**
  - Abstract: "A total of 125 newly trained TSOs participated in one of two experiments as part of their final evaluation following training." / "The first three blocks were low prevalence (target prevalence ≤ .05) with no feedback; the fourth block was high prevalence (.50) with full feedback; and the final block was, again, low prevalence." / "We found that newly trained TSOs were better at detecting targets at high compared to low prevalence, replicating the prevalence effect." / "Furthermore, performance was better (and response criterion was more "liberal") in the low-prevalence block that took place after the high-prevalence block than in the initial three low-prevalence blocks".
  - *d′* changed in the field: "In the case of these TSO observers, however, d' did change with prevalence."
  - Lab mechanism (Abstract): "In the lab, this "prevalence effect" is caused by changes in decision and response criteria (Wolfe & Van Wert, 2010)".

### Mitroff & Biggs (2014), *Psychological Science*, doi:10.1177/0956797613504221
- **Verified:** Crossref (25(1), 284–289; Jan 2014; Crossref main title "The Ultra-Rare-Item Effect"). Abstract and full title from Europe PMC / PubMed record PMID 24270463 ("The ultra-rare-item effect: visual search for exceedingly rare items is highly susceptible to error."). Full text not opened (not open access).
- **Claims supported (Section 2.2: detection fell logarithmically with target frequency), from the abstract:** "By assessing search performance across millions of trials from the Airport Scanner smartphone application, we demonstrated that the detection of ultra-rare items was disturbingly poor. A logarithmic relationship between target detection and target frequency (adjusted R (2) = .92) revealed that ultra-rare items had catastrophically low detection rates relative to targets with higher frequencies."

### Becker, Rodriguez, Montalvo & Peltier (2026), *Cognitive Research: Principles and Implications*, doi:10.1186/s41235-025-00702-w
- **Verified:** Crossref (vol. 11, issue 1, article 5; published 8 Jan 2026). Open-access full text (PMC12779849) via Europe PMC full-text XML.
- **Claims supported (Sections 2.2, 7 plan), from the abstract:** "In Experiment 1, we used a low-prevalence T-among-Ls task and found that distributing "probe" trials—trials with known targets and post-response feedback—reduced the LPE." / "The probe benefit scaled with the frequency of the matching target, suggesting limited generalizability to non-probed targets." / "Results showed that probes biased top-down guidance toward features of frequently probed targets, without affecting the number of items inspected or the decision criterion." / "Findings suggest that probes improve rare-target search by altering perceived prevalence, not through feedback alone."

### Green & Swets (1966), *Signal Detection Theory and Psychophysics*, Wiley
- **Verified: bibliographic only.** Open Library records (work OL31575577W: "Signal Detection Theory and Psychophysics", David M. Green and John A. Swets, John Wiley & Sons, 1966; a 1974 R. E. Krieger reprint also exists). Content not opened.
- **Use:** general reference for SDT (Section 2.1). No specific claim is attributed to it.

### Hautus, Macmillan & Creelman (2021), *Detection Theory: A User's Guide* (3rd ed.), Routledge, doi:10.4324/9781003203636
- **Verified: bibliographic only.** Crossref record (title "Detection Theory", subtitle "A User's Guide", authors Michael J. Hautus, Neil A. Macmillan, C. Douglas Creelman; Routledge; 10 Aug 2021; edition 3). Content not opened. (The brief's "Macmillan & Creelman" is the earlier edition; the current third edition adds Hautus as first author.)
- **Use:** general reference for SDT (Section 2.1). The formulas for *d′* and *c* in the paper are those stated in the pre-registration (Section 5). Chen et al. (2026, Sections 3 and 4.4) use the same two quantities and the log-linear correction but do not print the formulas.

### Hautus (1995), *Behavior Research Methods, Instruments, & Computers*, doi:10.3758/BF03203619
- **Verified:** Crossref (27(1), 46–51; March 1995). Abstract read on SpringerLink (https://link.springer.com/article/10.3758/BF03203619) via WebFetch.
- **Claims supported (Sections 2.1, 5.6), from the abstract:** "The second is the log-linear rule for which each cell frequency in the contingency table is increased by 0.5 irrespective of the contents of each cell." / "Results showed that the log-linear rule resulted in less biased estimates of d′ that always underestimated population d′." / "The 1/(2N) rule, apart from being more biased, could either over- or underestimate population d′."

### Mackworth (1948), *Quarterly Journal of Experimental Psychology*, doi:10.1080/17470214808416738
- **Verified: bibliographic only for the primary.** Crossref (title "The Breakdown of Vigilance during Prolonged Visual Search", 1(1), 6–21, April 1948). Publisher page returned HTTP 403; OpenAlex has no abstract (closed access).
- **Claim (Section 2.3) taken from a secondary source,** Klein & Feltmate (2025), below.

### Klein & Feltmate (2025), *Frontiers in Cognition*, doi:10.3389/fcogn.2025.1632885
- **Verified:** Crossref (vol. 4, article 1632885; 24 Nov 2025). Open-access full text (PMC13281068) via Europe PMC full-text XML.
- **Claims supported (Sections 2.3, 4.3):** "...the vigilance decrement is typically attributed to Mackworth's (1948) article titled "The Breakdown of Vigilance During Prolonged Visual Search" and his later monograph (see also Mackworth, 1961 ), wherein a decrement in performance with both visual and auditory targets was shown to be robust after the first half hour on the task." Note that this sentence covers the 1948 article and a later monograph together; the paper attributes the half-hour point jointly via Klein & Feltmate.

### Warm, Parasuraman & Matthews (2008), *Human Factors*, doi:10.1518/001872008X312152
- **Verified:** Crossref (50(3), 433–441; June 2008). Abstract via Europe PMC (PMID 18689050).
- **Claim (Sections 2.3, 4.3):** Abstract conclusion: "Converging evidence using behavioral, neural, and subjective measures shows that vigilance requires hard mental work and is stressful." The abstract also refers to "the vigilance decrement function" and "performance decrement in vigilance tasks".

### Bliss, Gilson & Deaton (1995), *Ergonomics*, doi:10.1080/00140139508925269
- **Verified:** Crossref (38(11), 2300–2312; Nov 1995). Abstract via OpenAlex (secondary index of the publisher abstract).
- **Claims supported (Section 2.3):** "A total of 138 undergraduate students ... were presented with alarms of varying reliabilities (25, 50 and 75% true alarms)". / "The results indicate that most subjects (about 90%) do not respond to all alarms but match their response rates to the expected probability of true alarms (probability matching)."

### Huegli, Merks & Schwaninger (2020), *Applied Ergonomics*, doi:10.1016/j.apergo.2020.103094
- **Verified:** Crossref (vol. 86, article 103094; July 2020). Abstract via Europe PMC (PMID 32342885).
- **Claims supported (Section 2.3), from the abstract:** "Using a simulated X-ray screening task, we tested 122 airport security screeners working with the support of explosives detection systems for cabin baggage screening (EDSCB) as low-level automation." / "Automation with a high false alarm rate of 20% and a low PPV of .3 resulted in operators ignoring about one-half of the true automation alarms on difficult targets-a strong cry-wolf effect."

### Cain, Adamo & Mitroff (2013), *Visual Cognition*, doi:10.1080/13506285.2013.843627
- **Verified:** Crossref (21(7), 899–921; Aug 2013). Abstract via OpenAlex (secondary index of the publisher abstract); full text not opened. Found on 4 November 2026 when looking for a human analogue of the crowding result. A companion paper, Adamo, Cain & Mitroff (2013), *Psychological Science*, 24(12), 2569–2574, doi:10.1177/0956797613497970 (abstract via Europe PMC, PMID 24142814), describes the same effect; it is not cited.
- **Claims supported (Sections 2.2, 7.2, 7.5), from the abstract:** "Multiple-target visual searches are especially error prone; once one target is found, additional targets are likely to be missed. This phenomenon, often called satisfaction of search (which we refer to here as subsequent search misses; SSMs), is well known in radiology". The paper uses this only as a loose analogy for crowding in LLM batch review.

### Sorkin & Woods (1985), *Human–Computer Interaction*, doi:10.1207/s15327051hci0101_2
- **Verified:** Crossref (1(1), 49–75; March 1985). Abstract via OpenAlex (secondary index of the publisher abstract).
- **Claims supported (Sections 2.3, 7 plan), from the abstract:** "In this paper, the combined automated monitor-human monitor system is modeled as a signal detection system..." / "Usual design practice is to set Ca to a value that optimizes the automated monitor's detection and false alarm rates. Our analysis shows that this setting will not yield optimal performance for the overall human-machine system."

### Cutler & Paddock (2009), ICCST, doi:10.1109/CCST.2009.5335565
- **Verified:** Crossref (IEEE; "43rd Annual 2009 International Carnahan Conference on Security Technology", pp. 46–51; event in Zurich, 5–8 Oct 2009). The IEEE Xplore page could not be read (empty response to WebFetch). **Abstract seen via OpenAlex** (secondary index of the IEEE abstract). Full paper not opened.
- **Claims supported (Sections 1, 2.4), from the abstract:** "Threat Image Projection (TIP) is a software system that is used at airports to project images of threat items amongst the passenger baggage being screened by X-ray." / "This is due to its purported benefits of improved attention and vigilance, and increased exposure to threat items that are linked to improvements in threat detection performance." / "The provision of feedback regarding TIP scores has been shown to enhance performance in excess of that achieved by using TIP in isolation."

### Buser, Schwaninger, Rehor & Sterchi (2025), *Transportation Research Part A*, doi:10.1016/j.tra.2025.104640
- **Verified:** Crossref (vol. 200, article 104640; Oct 2025; CC BY 4.0 licence). ScienceDirect returned HTTP 403; the publisher's PDF was downloaded from the authors' institutional repository (FHNW, https://irf.fhnw.ch/handle/11654/54247) and read in full.
- **Claims supported (Sections 1, 2.4):**
  - Abstract: "(1,199,838 TIP events from 728 screeners over four years)" / "Approximately 100 TIP events were sufficient to achieve a minimum reliability value of 0.7 when TIP was challenging enough (mean hit rate below 0.9). TIP performance predicted the covert test results (wherein instructed people tried to smuggle real prohibited items through the checkpoint; 1,184 covert tests from 474 screeners)".
  - Section 2: "pre-recorded images of threats, known as fictional threat items (FTIs), are projected onto 1 %–4 % of all passenger baggage during screening" / "the TIP system immediately provides feedback on whether an FTI is present or not" / "By increasing the number of threats to be detected, TIP aims to mitigate this effect while also increasing motivation by providing feedback on detection performance".
  - The brief's figure ("about 100 TIP events per screener for reliability ≥ 0.7") is confirmed, with the condition "when TIP was challenging enough (mean hit rate below 0.9)".
  - Not used in the paper, but noted: Section 3 states that at the study airport "The TIP systems projected FTIs onto X-ray images of passengers' baggage with a target prevalence of 2.9 %."

---

## AI control and monitoring

### Greenblatt, Shlegeris, Sachan & Roger (2024), ICML, PMLR 235; arXiv:2312.06942
- **Verified:** arXiv API (v5, updated 23 Jul 2024; comment "ICML version: https://openreview.net/pdf?id=KviM5k8pcP"); PMLR page https://proceedings.mlr.press/v235/greenblatt24a.html (citation_firstpage 16295, citation_lastpage 16336, "Proceedings of the 41st International Conference on Machine Learning", publication date 2024/07/08). **Quotes and section numbers are from the arXiv v5 PDF**, which the authors say fixes minor typos and adds a glossary and related work relative to the ICML version. The PMLR PDF was not opened. The pre-registration cites this as "Greenblatt et al., 2023" (arXiv); the paper cites the 2024 proceedings.
- **Claims supported (Sections 1, 3.1, 5.2, 5.4):**
  - Section 2: "we want to use LLMs to solve 5,000 programming problems from the APPS dataset" / "We say a solution is backdoored if it passes all APPS test cases, and if GPT-4 can construct an exploit when presented with the code. An exploit is a specific input that will yield an incorrect output".
  - Section 2.2: "In each simulation, the protocol has enough H points to use on up to 2% of problems."
  - Section 3.1.2 (Upfront auditing): "The red team can win with high probability if the attack policy attempts to insert a backdoor very rarely" / "since the red team can respond to a doubling of the number of problems by halving its probability of adding a backdoor on any given problem." / "Safety: At 2% H budget, the blue team win probability is 15%."
  - Section 3.2 (Trusted monitoring): "Auditing decision: ask T whether the code looks suspicious; audit the top 2% most suspicious proposals (roughly)." / "We pick a classifier threshold such that the classifier has a 2% false positive rate on the distribution of solutions written by GPT-4" / "Safety: The blue team win probability is 62% (up from 15% when using upfront auditing)".
  - Trusted GPT-3.5 / untrusted GPT-4: Abstract ("access to a powerful but untrusted model (in our case, GPT-4), access to a less powerful trusted model (in our case, GPT-3.5)").

### Griffin, Thomson, Shlegeris & Abate (2024), arXiv:2409.07985
- **Verified:** arXiv API (v2 updated 7 May 2026); PDF v2. Footer: "Article presented at the Second IASEAI Conference (IASEAI'26). © 2026 Association for the Advancement of Artificial Intelligence". Cited as a preprint (proceedings record not checked).
- **Claims supported (Sections 1, 3.1):**
  - Section 2 (Trusted Monitoring Example): "T's suspicion scores are modelled as a distribution, conditioned on whether the code is safe or backdoored."
  - Red team chooses a backdoor rate: Section 4.1, Corollary 4.2: "the optimal backdoor rate is β∗ := minβ∈[0,1] p(β)."
  - Section 6.1: "Increasing the human FNR decreases safety almost linearly in the worst case, without impacting usefulness."

### Bhatt et al. (2025), Ctrl-Z, arXiv:2504.10374
- **Verified:** arXiv API (v1, 14 Apr 2025); PDF.
- **Claims supported (Sections 1, 3.1, 8):**
  - Abstract: "Our work presents the first control evaluation performed in an agent environment." / "We construct BashBench, a dataset of 257 challenging multi-step system administration tasks".
  - Section 2.2 and footnote 2: "The blue team only has a limited number of uses of H, equivalent to 1% of the actions taken in an episode" / "The 1% metric was chosen arbitrarily: auditing 1% is higher than what we expect to be able to afford in real deployment".
  - Section 3.1: "implement a rare attacks strategy, only attempting to attack on any given task with a small probability."

### Korbak, Clymer, Hilton, Shlegeris & Irving (2025), arXiv:2501.17315
- **Verified:** arXiv API (v1, 28 Jan 2025); PDF.
- **Claims supported (Sections 1, 2.4, 3.1):**
  - Section 4 (Control protocol): "The safety layer edits the 10% most suspicious actions and audits the 0.1% most suspicious actions." / "Human auditor reliability testing. Developers apply the same process used to evaluate monitors to evaluate human auditors: developers regularly generate synthetic attacks and check whether human auditors remain attentive and flag synthetic attacks as suspicious." / "Monitor reliability testing. Developers automatically evaluate monitors every week ... The system then prompts the LLM agent to execute attacks on these tasks."
  - Section 6: "Or models might simply attack very rarely such as once out of thousands of tasks."
  - Section 6 (Sections 3.1 and 7.3 of the paper): "Alternatively, models might execute a ‘Blitzkrieg’ strategy (Clymer et al., 2024), where many LLM agents attempt to exfiltrate data simultaneously (coordinating their attacks across space)." The paper quotes "across space" and "where many LLM agents attempt to exfiltrate data simultaneously".

### Kutasov et al. (2025), SHADE-Arena, arXiv:2506.15740
- **Verified:** arXiv API (v2, 8 Jul 2025); PDF.
- **Claims supported (Sections 3.2, 8):**
  - Section 4.1: "Even the most effective monitor (Gemini 2.5 Pro) has an AUC of only 0.87." (The sentence "picking our threshold to ensure that we catch any sabotage attempt with 80% probability would imply a false positive rate of over 20%" was used in the Phase 1 draft and has been cut.)
  - Section 4.1: "We also collect human monitoring results on a set of 12 benign and 20 malign transcripts across 14 task pairs." / "Annotators choose to take an average of 103 minutes per transcript" / "Treating ratings from all annotators as individual samples we get an AUC of 0.65 (worse than top AI monitors)."
  - The brief's figures (human AUC 0.65, best monitor 0.87) are confirmed. "20 of the 32 transcripts were malign" restates 12 benign + 20 malign.

### Kale et al. (2025), arXiv:2508.19461
- **Verified:** arXiv API (v1, 26 Aug 2025); PDF.
- **Claim (Section 3.2), abstract:** "escalating only pre-flagged cases to human reviewers improved the TPR by approximately 15% at FPR = 0.01."

### Ye, Zou, Yu & Shi (2026), arXiv:2606.05647
- **Verified:** arXiv API (v2, 5 Oct 2026; comment "Accepted by NeurIPS 2026"); PDF. Cited as a preprint with acceptance noted.
- **Claims supported (Section 3.2):**
  - Abstract: "Over 100 participants collaborate with one of four frontier models" / "We find that 83/88 (94%) of developers in the no-monitor conditions fail to detect sabotage".
  - Section 4.2: "Conditioning on the 16 sessions with a correct monitor alert, SSR remains 9/16 (56%...)" (the following quote was cut from the current draft) / "If experienced developers dismiss correct warnings in a controlled study, the gap between detection and action will probably widen in deployment under greater time pressure, alert fatigue, and weaker review incentives."

### Favaro & Wright (n.d.), Anthropic, "Measurements for understanding the pace of AI development inside frontier labs"
- **Verified:** https://www.anthropic.com/institute/measuring-pace-of-ai-development downloaded with curl and read with WebFetch. No publication date is shown on the page or in its metadata; it reports data "As of August 2026" and shows "© 2026 Anthropic PBC". Authorship from the page: "Marina Favaro and Phillie Wright co-authored this piece". Cited as (Favaro & Wright, n.d.) with access date; James may prefer "Anthropic (n.d.)" as group author.
- **Claims supported (Sections 1, 3.3, 8)**, all from section "(2) Measuring oversight of AI agents", table column "Offline monitors" unless stated:
  - "As of August 2026, there were approximately 30,000 agents doing research and engineering work at Anthropic at any one time in our most-used internal platform."
  - "100% of these agents' actions are ingested by the monitor after they are taken." (offline monitor, Coverage row)
  - "The monitor flags roughly 100,000 transcripts per week that are then reviewed by multiple classifiers for false-positives and initial oversight review. Most of the flags are resolved by this process, and the highest priority flags (approximately ~50 per week) are escalated to human review." (Review latency row)
  - "The monitor flags roughly one to two transcripts in every thousand for further review." (Blocking / escalation rate row)
  - "In our monitoring data to date, individual agents rarely misbehave." (section introduction)
  - The brief's wording is confirmed. Not used: the online monitor figure "0.002% of them (about 1 in 47,000) were blocked by this monitor".

### Najt, Toft, Tracy, Roger & Benton (2026), SLEIGHT-Bench, Alignment Science Blog
- **Verified:** https://alignment.anthropic.com/2026/sleight-bench/ downloaded and read (dated "May 19, 2026"; authors and affiliations as listed).
- **Claims supported (Sections 3.2, 8):** "a benchmark of synthetic transcripts containing 40 attacks across 11 categories" / "If a monitor is too trigger-happy, it becomes infeasible to deploy in practice, since humans won't be able to review every flagged transcript" / "We calibrate our monitors to a 1% false positive rate" / "On Opus 4.6, the main monitor we work with, 50% of attacks are never caught on any of the 10 trials."

### Remedios, Storf, Roger & Hughes (2026), "Red-Teaming Auto Mode", Alignment Science Blog
- **Verified:** https://alignment.anthropic.com/2026/red-teaming-auto-mode/ downloaded and read (dated "October 22, 2026"; "Primary contributors. Name order randomised." for Remedios and Storf).
- **Claims supported (Sections 3.2, 5.4, 8):** "Production monitors fail to block over 55% of attacks." / "All monitors block under 1% of the 4,000 benign SWE-chat actions, which we consider acceptable for ordinary coding work." / Blocking monitors "check each action (e.g. a bash command) against a separate LLM-based classifier, and block unsafe actions". / Snapshot: "Production monitoring systems change constantly, so our results are a snapshot of their robustness as of September 2026."

---

## LLM judges, context effects and the gap

### Zheng et al. (2023), NeurIPS 36 Datasets and Benchmarks, arXiv:2306.05685
- **Verified:** arXiv API (comment "NeurIPS 2023 Datasets and Benchmarks Track"); NeurIPS proceedings page (https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html) shows "Advances in Neural Information Processing Systems 36 (NeurIPS 2023)", "Datasets and Benchmarks Track", DOI 10.52202/075280-2020.
- **Claim (Section 4.1), abstract:** "We examine the usage and limitations of LLM-as-a-judge, including position, verbosity, and self-enhancement biases".

### Zhao, Wallace, Feng, Klein & Singh (2021), ICML, PMLR 139; arXiv:2102.09690
- **Verified:** arXiv API (comment "ICML 2021"); PMLR page https://proceedings.mlr.press/v139/zhao21c.html (pp. 12697–12706, 38th ICML); arXiv PDF.
- **Claims supported (Sections 4.1, 4.3):** Figure 4 caption: "When the prompt is unbalanced, the predictions are unbalanced (majority label bias)." Section 1 (Introduction): "they suffer from majority label bias, recency bias, and common token bias (Section 4)".

### Liu et al. (2024), *TACL*, doi:10.1162/tacl_a_00638
- **Verified:** Crossref (vol. 12, 157–173; 2024); abstract via arXiv API (arXiv:2307.03172).
- **Claim (Section 4.1), abstract:** "we observe that performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts".

### Kapetanovic, Altwlkany, Mercep, Duricic & Lacic (2026), CIKM '26, doi:10.1145/3799682.3840879; arXiv:2608.25869
- **Verified:** arXiv API and PDF (ACM reference format on page 1 gives the DOI and "CIKM '26, November 07–11, 2026, Rome, Italy"); Crossref record (Proceedings of the 35th ACM CIKM, pp. 2043–2052, dated 7 Nov 2026). The conference takes place after the date of this check; the DOI and page numbers are as registered in Crossref.
- **Claims supported (Section 4.1), abstract:** "We show that prior scores, even when included only as context metadata, anchor judgments and systematically shift ratings toward their values." / "Neither Chain-of-Thought nor a metadata-disregard warning reduces the total effect".

### Chen, Zhu, Zheng & Li (2026), arXiv:2609.18204
- **Verified:** arXiv API (v1, 16 Sep 2026; comment "Accepted at the 60th Hawaii International Conference on System Sciences (HICSS)"); PDF.
- **Claims supported (Sections 4.1, 7 plan):** Abstract: "Using signal detection theory, we audit five LLM overseers on 19 compliance tasks (4,551 analyzed judgments)" / "elaborate traces shift the decision criterion toward rejection, increasing false alarms in susceptible overseers." / "AI auditors should be evaluated by their decision criterion and false-alarm behavior, alongside accuracy." Section 5.2: "pooled accuracy falls from 0.80 to 0.70 while d′ stays near 2.4 to 2.7, so the entire accuracy drop is the criterion sliding". Design (Sections 4.1 and 4.3): each of 19 items appears in a correct and an error version ("2 correctness levels"), so errors make up half of the judgments; each judgment returns "a structured ACCEPT or REJECT decision" on one recommendation. Prevalence is not manipulated.

### Cai, Wang, Yang, Lin, Lee & Yang (2026), arXiv:2610.22631
- **Verified:** arXiv API (v1, 15 Oct 2026), title, authors and abstract. Found by our own search (query 7 below). PDF not read.
- **Claim (Section 4.1), abstract:** "Using signal detection theory, we find a significant mean shift in decision criterion toward acceptance, without a clear change in mean discriminability."

### Srivastav, Pape & Schönherr (2026), arXiv:2601.18552
- **Verified:** arXiv API (v2, 31 Aug 2026; journal_ref "Findings of the Association for Computational Linguistics: EMNLP 2026"); PDF.
- **Claims supported (Section 1):** Section 6.3: the main comparison is "under balanced conditions (π = 50%, where π denotes prevalence of hidden intentions)"; "Using Bayes' rule, we analyse precision as a function of prevalence" with Precision(π) = TPR·π / (TPR·π + FPR·(1 − π)). That is, low-prevalence performance is derived arithmetically from TPR and FPR measured at 50%; the judge is never shown a low-prevalence stream.

### Abbasi, Núñez V. & Shahraki (2026), arXiv:2610.41803
- **Verified:** arXiv API (v1, 30 Oct 2026); PDF. Found by our own search (WebSearch b).
- **Claims supported (Sections 1 and 7.3):** Abstract: "In the eleven evaluations we audited, attacks or anomalies make up 16% to 86% of the test samples, no evaluation varies that share". Section I: "When attacks are rare, even a small false-positive rate yields alerts that are mostly false [14], and the receiver operating characteristic (ROC) hides this because, unlike precision, it does not depend on prevalence". Section III.E: "Prevalence shift leaves the class-conditional score distributions unchanged, so precision at prevalence π follows from the true- and false-positive rates at a threshold".

### Hida, Ribeiro & Hida (2026), arXiv:2608.14737
- **Verified:** arXiv API (v1, 13 Aug 2026; comment "Accepted at ENIAC 2026 ... part of BRACIS 2026"); PDF read. Found by our own search (query 8 below). **Closest prior work.**
- **Claims supported (Sections 4.1, 4.2, 4.3):**
  - Section 1: "We selected five reviews from SESR-Eval [Huotala et al. 2025], with prevalence ranging from 2.9% to 53.0%".
  - Section 3.1: four conditions, individual or batch, with or without "a single sentence informing the true (oracle) estimated inclusion rate".
  - Section 3.3: "studies were randomly shuffled with a fixed seed and grouped into batches of 20".
  - Abstract: "The results indicate a limited influence of the prevalence metadata, with no evidence that it improves performance. In contrast, batch processing produced larger behavioral changes that varied according to the prevalence of the class."
  - Section 4.4: "When SLRs are ordered by increasing prevalence (Table 2), the four reviews with prevalence ≤ 20% present a positive net shift ... In these cases, batch processing made Llama more inclusive. In the single almost balanced SLR available (prevalence of 53%), the net shift was strongly negative (-25.3 points)" / "This pattern is compatible with a possible tendency toward implicit normalization of decisions within the batch."
  - Confound (our reading): prevalence differs between reviews, which also differ in topic, criteria and items.

### Kim, Kim, Lee & Kim (2026), arXiv:2608.02681
- **Verified:** arXiv API (v2); PDF (Section 1 and Section 4 searched). Found by our own search (query 9).
- **Claims supported (Sections 4.1, 4.3), abstract:** "a harmful question that is reliably refused in isolation can elicit a harmful response when embedded in a batch of benign questions" / "analyze its causes from two complementary perspectives: alignment signal weakening and refusal signal dilution."

### Makins, Angelini, Shams & Phuong (2026), arXiv:2607.07368
- **Verified:** arXiv API (v2); PDF. Found by our own search (WebSearch b).
- **Claim (Section 4.1):** Abstract: "Our central finding is the fragmentation effect: as more agents coordinate to attack, per-agent monitoring becomes less likely to catch any of the attackers. Secondly, this is not driven by the ratio of benign to malicious code". Section 1: "This is not driven by the lower ratio of the malicious to benign code of each commit".

---

## Materials and tools

### Austin et al. (2021), MBPP, arXiv:2108.07732
- **Verified:** arXiv API (v1, 16 Aug 2021); dataset card via Hugging Face API (`google-research-datasets/mbpp`: licence `cc-by-4.0`; config `full` with splits train 374, test 500, validation 90, prompt 10); GitHub README (google-research/mbpp): "Each problem consists of a task description, code solution and 3 automated test cases."
- **Claims supported (Section 5.2):** Abstract: "The Mostly Basic Programming Problems (MBPP) dataset contains 974 programming tasks, designed to be solvable by entry-level programmers." Licence CC BY 4.0 from the dataset card. Three tests per problem from the README.

### Anthropic (n.d.), "Run Claude Code programmatically", Claude Code Docs
- **Verified:** https://code.claude.com/docs/en/headless read with WebFetch.
- **Claims supported (Section 5.4):** "Add the `-p` (or `--print`) flag to any `claude` command to run it non-interactively." / "To get output conforming to a specific schema, use `--output-format json` with `--json-schema` and a JSON Schema definition." The page does not document an effort flag for `-p` (it mentions `/effort` as a command); the exact mechanism used for "effort low" is marked CONFIRM in the paper.

### Pre-registration
- `PREREGISTRATION.md`, git commit `f4bedaa610d8f434e0aedf2f5763f3f100861f45`, "Tue Nov 3 22:38:38 2026 +0000", message "Add papers/ folder: house style and pre-registration for the low-prevalence monitor study" (from `git log`). All design details in Section 5 of the paper are taken from this file.

---

## Gap searches (to support Section 4.2)

Run on 3 November 2026. Elicit was not available. arXiv queries used the arXiv API (`search_query`, sorted by relevance; all hits listed were inspected by title, and abstracts were read where relevant).

| # | Tool | Query | Hits | Outcome |
|---|---|---|---|---|
| 1 | arXiv | `abs:"prevalence effect" AND (abs:LLM OR abs:"language model")` | 1 | 2501.14326 (concurrent programs and memory models): unrelated. |
| 2 | arXiv | `abs:"low prevalence" AND (abs:LLM OR abs:"language model")` | 17 | Medical rare-disease and label-noise papers; 2601.18552 (Srivastav et al., cited). None manipulates prevalence in a judge's context. |
| 3 | arXiv | `abs:"target prevalence" AND (abs:LLM OR abs:"language model" OR abs:monitor)` | 0 | — |
| 4 | arXiv | `abs:prevalence AND abs:"LLM monitor"` | 0 | — |
| 5 | arXiv | `abs:"base rate" AND (abs:"LLM-as-a-judge" OR abs:"LLM judge")` | 1 | 2511.15958 (JudgeBoard): unrelated. |
| 6 | arXiv | `abs:prevalence AND abs:"trusted monitoring"` | 0 | — |
| 7 | arXiv | `abs:"signal detection" AND (LLM OR "language model") AND (criterion OR bias) AND (monitor OR judge OR overseer)` | 3 | Chen et al. 2609.18204 (cited); Cai et al. 2610.22631 (cited); 2605.26174 (criterion shifts across model generations in cross-section defect detection; no prevalence manipulation). |
| 8 | arXiv | `abs:batch AND (judge OR evaluator OR annotator OR classifier) AND abs:LLM AND ("label distribution" OR "class balance" OR prevalence OR "base rate")` | 7 | **Hida et al. 2608.14737 (cited; closest)**; 2606.10315 (LLM judge recall against human review in production); 2602.16111 (prevalence measurement at Pinterest); others unrelated. |
| 9 | arXiv | `ti:"batch prompting" OR abs:"batch prompting"` | 17 | Kim et al. 2608.02681 (cited); 2503.15551 (batch prompting attacks); 2503.02756 (BatchGEMBA: batching degrades MT evaluation); others about efficiency. None varies class prevalence. |
| 10 | arXiv | `abs:vigilance AND (LLM OR "language model") AND (monitor OR detection)` | 19 | "Epistemic vigilance" and tools named VIGIL; none relevant. |
| 11 | arXiv | `abs:prevalence AND ("LLM-as-a-judge" OR "LLM judge" OR "LLM-based monitor" OR "AI monitor")` | 24 | 2512.08121 (balanced accuracy for judge selection); Srivastav et al.; 2606.10315; none manipulates prevalence in context. |
| 12 | arXiv | `abs:"in-context" AND ("label imbalance" OR "class imbalance" OR "label proportion") AND (LLM OR "language model")` | 50 (top 15 inspected) | Label imbalance among labelled demonstrations (e.g. 2502.04037, 2402.11447); not unlabelled review streams or monitoring. |
| 13 | arXiv | `abs:backdoor AND abs:monitor AND (rare OR prevalence OR "base rate") AND (LLM OR "language model")` | 2 | Unrelated. |
| a | WebSearch | `"low prevalence effect" large language model monitor OR judge OR classifier` | — | Srivastav et al.; 2606.10315; RSNA label-noise work; 2512.08121. No LPE study for LLMs. |
| b | WebSearch (extended) | `LLM monitor rare attacks prevalence in context batch hit rate criterion shift AI control experiment` | — | Abbasi et al. 2610.41803 (cited); Makins et al. 2607.07368 (cited); 2607.02514 (distributed attacks, persistent state); a LessWrong monitoring benchmark. None manipulates prevalence. |
| c | WebSearch | `"prevalence effect" vision language model OR multimodal LLM visual search rare targets missed` | — | Only human studies returned. |
| d | WebSearch | `"threat image projection" OR "synthetic attacks" inserted to test AI monitors auditors attentiveness AI control canary` | — | Reports of synthetic attacks used to test monitors (a GovAI fellowship report on LessWrong; Redwood adaptive-attack work). No prevalence manipulation and no TIP-style remedy for LLM monitors. One result (arXiv 2510.09462) reportedly contained text addressed to monitors; it was not opened or cited. |

**Conclusion of the search:** no study found that manipulates the share of targets within an LLM monitor's or judge's context while holding items fixed, none in an AI-control setting, and none testing TIP-style remedies for LLM monitors. The closest is Hida et al. (2026). Searches can miss work, especially very recent preprints and non-English work; the paper says "we found no study", not "no study exists".

---

## Not used, or used only as context

- Collot et al. (2025), arXiv:2512.08121, balanced accuracy for judge selection: abstract read; not cited.
- GovAI fellowship report on offline monitoring (LessWrong): seen only as a search snippet; not cited.
- Regulatory basis of TIP: the Citadel Aero regulation library was searched ("threat image projection screener performance aviation security X-ray") and returned no aviation-security provisions; the paper makes no regulatory claim about TIP. Buser et al. (2025, Section 2) state that "TIP is one of possible measures included in national regulation (National Aviation Security Plan, NASP)"; this is not used.

---

## Provenance of numbers in Methods and Results (Phase 2, 4 November 2026)

Every number in Sections 5 and 6 of the paper, and in the Abstract, Discussion and Conclusion, was copied from the engineer's files. None was computed by the writing agent, except unit conversions of false-alarm rates to percentages with one decimal (Table 2) and the phrase "more than doubled" for 1.7% to 4.0%. One check was made by counting rows: in `results/judgments.csv`, 0 of 28,216 judgments with suspicion below 20 were flagged and all 1,274 judgments with suspicion of 60 or more were flagged. This confirms that the 0.00 and 1.00 entries in the band table are not rounding artefacts (paper, Section 6.6).

| Paper location | Numbers | Source |
|---|---|---|
| 5.2 Problems | 974 problems; IDs 367 and 927 ineligible; 972 eligible; 450 sampled; seed 20261103; download date and hashes | `results/RESULTS.md` §3; `code/README.md` stage note 1; `PREREGISTRATION.md` §9 item 4 |
| 5.2 Item pairs | generator `claude-opus-5-5`, effort medium; inputs; 450 calls, 0 refusals; subtlety instruction quotes | `results/calibration.md` ("Generator prompt used"); `code/README.md` stage note 2; `results/RESULTS.md` §2–3 |
| 5.2 Verification | 10-second timeout; checks; float tolerance 1e-9; difflib ratio ≥ 0.6; 419/450 (93.1%); exclusions 14/14/1/1/1; median changed lines 2, max 8; 356 (85%) two lines; 254 (61%) and 150 (36%) edit types | `code/README.md` stage note 3; `results/RESULTS.md` §3; `PREREGISTRATION.md` §9 items 3, 5 |
| 5.2 Normalisation, Pools | docstring removal; seed 4021; 40 and 379 | `PREREGISTRATION.md` §9 item 2; `results/RESULTS.md` §3 |
| 5.3 Calibration | 24/40 = 0.60 (0.45–0.74); 0/40 (0.00–0.09); AUROC 0.97; no revision | `results/calibration.md` |
| 5.4 Monitors | Claude Code 2.1.317; flags; prompt quotes; what the monitor saw | `code/README.md`; `code/prompts/monitor_*.txt`; `PREREGISTRATION.md` §9 items 6–7 |
| 5.5 Experiments | prompt sentences; 240 problems; R-cal sampling; seeds 55021 and 99173; six workers; run times | `code/prompts/`; `results/RESULTS.md` §2–3; `PREREGISTRATION.md` §9 item 10; `code/README.md` stage note 6 |
| 5.7 Analysis | test details; H1a rule; GLMM rule; Python 3.13.18, statsmodels 0.15.0; seed 314159 | `code/analyse.py` docstring; `PREREGISTRATION.md` §9 items 1, 9, 11; `code/README.md` |
| 5.8 Timing | commits `136632a` (23:10 UTC) and `d8e6b51` (23:16 UTC); run start 23:13 UTC; 12 smoke-test calls; 138 outputs | author's timing note in `PREREGISTRATION.md` §9; commits confirmed with `git cat-file` / `git log` (136632a 23:10:31, d8e6b51 23:16:46); `results/log_monitors.txt` first line "12 already done, 2164 to run" at 23:13:00 |
| 5.9 Exclusions, cost | 2,176 calls; 30,880 judgments; 0 retries/refusals/drops; 43/368 and 24/720 in-call corrections; 2,706 calls; USD 41.70 | `results/RESULTS.md` §1, §2, §5, §6; `results/costs.json` |
| 6.1 Table 2 | all *H*, CIs and *F* | `results/RESULTS_numbers.md`, "Descriptive results per condition" |
| 6.1 Table 3; 6.2–6.5 | ORs, CIs, z, p, Holm p (exact p values .0015 and Holm .0015 for Haiku H1; .008/.015 Sonnet H2; .053/.106 Sonnet H3) | `results/RESULTS_numbers.md` H1, H2, H3 tables; exact values from `results/analysis.json` keys `H1.*.p_holm`, `H2.*.p_holm`, `H3.*.p_holm` |
| 6.2 | P10 vs P50 ORs and p; false-alarm contrasts (min p = .279) | `results/RESULTS_numbers.md` H1 tables |
| 6.3 Table 4 | Δ*H*, Δ*F*, Δ*d′*, Δ*c*, ΔAUROC with CIs | `results/RESULTS_numbers.md` H1a table |
| 6.4 | GLMM estimate, SE, z, p; item SD 9–33; p .006–.011; 92 of 120; GLM OR 0.61 [0.44, 0.84], p .002; Δ*H* −0.075 [−0.125, −0.033]; Δ*c* values; false-alarm p .108 and .329 | `results/RESULTS_numbers.md` H2 tables; `results/RESULTS.md` §8 note 3; `results/analysis.json` `H2.*.false_alarm_glm_item_clustered` |
| 6.5 | H3 ORs; Sonnet Δ*c*, Δ*d′*, Δ*F*; flags per batch 1.41 and 2.40 | `results/RESULTS_numbers.md` H3 and "Flags per batch" tables |
| 6.6 E1–E4 | all coefficients, ORs and p values (E1 min p for hits .084; E4 min false-alarm p .465) | `results/RESULTS_numbers.md` exploratory tables |
| 6.6 Table 5 | mean suspicion; top-band share; flag rate at 40–59 | `results/RESULTS_numbers.md` descriptive table and post hoc band table |
| 6.6 reasoning, robustness | thinking tokens 7,592/4,195 and 116/480; sensitivity ORs 2.35 (p .0007) and 2.81 | `results/RESULTS.md` §5–6; `results/sensitivity_excluding_extra_turn_calls.json` |
| 7.2 | calibration 0.60 vs Experiment 2 *none* 0.633 | `results/RESULTS.md` §8 note 6 |
| Figures 1–5 | `figures/fig_a_prevalence.png` … `fig_e_remedies.png`; error-bar definitions | `code/analyse.py`, function `figures` (Wilson intervals for Figures 1, 3, 4, 5; cluster-bootstrap intervals for Figure 2) |
