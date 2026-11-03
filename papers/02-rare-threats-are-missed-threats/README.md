# Rare Threats Are Missed Threats

*A pre-registered test of the low-prevalence effect in LLM code monitors* (paper 02)

**James Le Cuirot** · Citadel Aero · Draft v0.1, 3 November 2026

## Abstract (draft; results pending)

AI control protocols use language-model monitors to review the work of more capable, untrusted AI systems and to pass the most suspicious items to a small human audit budget. In deployment, real attacks are expected to be rare. In human visual search, rare targets are missed far more often than common ones. This low-prevalence effect is mainly a shift in decision criterion, and airport security counters it with Threat Image Projection, which inserts fictional threats into live screening. This pre-registered study asks whether large language model (LLM) monitors show the same effect. Two Claude models reviewed short Python solutions to MBPP problems, some containing a verified backdoor that passes the given tests but returns a wrong answer on one trigger input. We varied the share of backdoored submissions within a 40-item batch (50%, 10% or 2.5%), stated a base rate for single-item judgments (50% or 1%), and tested two remedies at 2.5%: a labelled calibration block modelled on Threat Image Projection, and an instruction to judge each item independently. Signal detection measures separate changes in criterion from changes in sensitivity. **[Results pending.]**

## Status

| Part | State |
|---|---|
| Pre-registration | Committed 3 November 2026 (`f4bedaa`), before monitor data. |
| Introduction, Background (human factors; AI control; LLM judges and the gap), Methods, Limitations skeleton, closing statements, references | **Drafted (Phase 1).** About 5,700 words of text, plus Table 1. |
| Results, Discussion, Conclusion, numbers in the Abstract | **Pending.** Marked `<!-- RESULTS PENDING -->`. To be written only from `results/RESULTS.md` and `figures/`. |
| Method details that depend on the run | Marked `<!-- CONFIRM FROM results/ -->` (12 places). |
| `code/`, `data/`, `results/`, `figures/` | Being built by a separate engineer agent; not touched by the writing agent. |
| Sources | 39 references, all opened or checked this session; log in `sources.md`. |

## What James should check

1. **Title.** "Rare Threats Are Missed Threats" asserts a result. If H1 is not supported (the pre-registration allows that), change it. The subtitle is phrased as a test to stay neutral.
2. **Closest prior work.** Hida et al. (2026, arXiv:2608.14737) found that batching made one model *more* inclusive at low prevalence, the opposite of a human-style effect. The paper presents this as a competing prediction (Sections 4.1–4.3). Check that framing.
3. **Citation choices.**
   - Greenblatt et al. is cited as the ICML 2024 paper (PMLR 235). The pre-registration calls it "2023" (arXiv). Quotes were taken from arXiv v5.
   - The Anthropic deployment figures are cited as Favaro & Wright (n.d.), the named co-authors of the page, which shows no date. You may prefer "Anthropic (n.d.)".
   - Griffin et al. (2024) is cited as a preprint (v2, 2026). The PDF footer says it was presented at IASEAI '26; the proceedings record was not checked.
4. **Sources seen only in part.** Abstract only: Cutler & Paddock (2009, via the OpenAlex index, because IEEE Xplore was not readable), Mitroff & Biggs (2014), Huegli et al. (2020), Bliss et al. (1995), Sorkin & Woods (1985), Warm et al. (2008). Bibliographic record only: Green & Swets (1966) and Hautus et al. (2021), cited only as general SDT references. Mackworth (1948) is described through Klein & Feltmate (2025). If you have library access, the Cutler & Paddock full text would be worth reading.
5. **Wolfe et al. (2005) figures.** 7% / 16% / 30% misses at 50% / 10% / 1% prevalence, confirmed from the authors' accepted manuscript (PMC4224304). Wolfe et al. (2013) misreport the low level as "0.02"; the paper follows the primary source.
6. **CONFIRM markers in Methods (Section 5).** These include:
   - MBPP version and whether all 974 problems were used
   - the final generator prompt and settings
   - the execution time limit
   - the edit-distance measure and threshold
   - counts of generated, excluded and kept pairs, and the size of the main pool
   - calibration rounds and their results
   - exact CLI flags, how "effort low" was set, the Claude Code version and run dates
   - the monitor prompt file, and whether the monitor saw the task text and the tests
   - invalid outputs, dropped batches and refusals
   - deviations from the pre-registration
7. **Two points to raise with the engineer now.**
   - **Docstrings.** The pre-registration says `ast` parse and unparse "strips comments and docstrings". Python's `ast.unparse` keeps docstrings unless they are removed explicitly. Check that the code removes them.
   - **H1a.** The pre-registration requires the change in *c* to be "larger in standardised units" than the change in *d′* but does not define standardised units. The analysis code will need a definition, and it should be reported as an interpretation of the pre-registration.
8. **Calibration-block confound.** R-cal raises in-context prevalence *and* shows worked examples with triggers. A benefit cannot be attributed to either alone (listed in Limitations). Becker et al. (2026) suggest probe benefits are specific to the probed target type.
9. **Length.** The house target for empirical papers is 5,000–7,000 words. Phase 1 text is about 5,700 words, so Results, Discussion and Conclusion together should stay near 1,300–1,500 words, or the background should be cut further.
10. **AI-assistance statement.** It says the experimental code was written with AI assistance under your direction, and that Claude models were the generator and the monitors under study. Adjust if needed.

## Open questions

- Is 2.5% (one in 40) low enough to say anything about deployment, where flags run at about one or two per thousand and true attacks are presumably rarer?
- In deployment, most monitors judge one transcript per call. Where does "experienced prevalence" arise in practice: within long agent transcripts that are mostly benign actions, in batched review, or in monitors with memory across items?
- If the effect shows in flags but not in AUROC, does it matter for protocols that threshold suspicion scores externally, or only for monitors that act on their own decision?

## How to develop it

- **Other monitor families.** Run the same items with GPT, Gemini and open-weight monitors. This tests whether the result is a property of LLM monitors in general or of one family, and it removes the shared-family link between generator and monitor.
- **Agent-transcript domain.** Move to multi-step agent settings (for example BashBench, SHADE-Arena or LinuxArena-style tasks), where the benign actions within one transcript give the monitor an "experienced prevalence" without batching.
- **Lower prevalence and longer contexts.** Test 1 in 100 or 1 in 400 with larger batches, and separate prevalence from batch length.
- **Human comparison.** Run human reviewers on the same items at the same prevalences, which gives a direct test of the analogy. Separately, vary the positive predictive value of monitor escalations to human auditors to measure a cry-wolf effect in AI audit (Bliss et al., 1995; Huegli et al., 2020).
- **TIP in deployment.** Insert known synthetic attacks, with feedback, into a monitor's stream over time (Korbak et al., 2025). Measure the monitor's hit rate and criterion as it drifts. Use Buser et al. (2025) to work out how many inserted attacks give a reliable estimate.
- **Probe similarity.** Following Becker et al. (2026), compare calibration examples of the same backdoor type as the target with examples of a different type.
- **Aviation link.** The same design applies to LLM tools that screen aviation documents for rare safety-relevant items, such as maintenance records or occurrence reports. Keep this short and factual in the paper.

## Files

- `paper.md`: the paper (source of truth). Build with `papers/_build/build.sh`.
- `sources.md`: verification log and the gap-search record.
- `PREREGISTRATION.md`: the registered design.
- `code/`, `data/`, `results/`, `figures/`: experiment (engineer agent).
