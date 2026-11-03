# Checkride or Line Check? What LOSA and Evidence-Based Training Teach About Evaluation Awareness in AI Systems

**Status: draft v0.1 for author review (3 November 2026).** Not peer reviewed. Not yet built to PDF/HTML (`papers/_build/build.sh` does not exist yet; `pandoc paper.md` renders cleanly). Main text about 7,400 words, plus 5 tables, 1 figure and a short appendix.

## Abstract

Frontier language models can often tell when they are being evaluated, and in some studies they behave better when they say they are being tested. This evaluation awareness threatens the validity of pre-deployment safety evaluations. Airline training met a similar problem long ago: a checkride shows what a crew does while an examiner is watching. The industry developed two complementary answers. Line Operations Safety Audits (LOSA) place trained observers on the flight deck during normal flights under confidential, non-jeopardy conditions and code threats, errors and undesired aircraft states. Evidence-based training (EBT) assesses competencies through observable behaviours across varied scenarios rather than a fixed list of manoeuvres, and requires operators to assure the concordance of their instructors. The paper maps the design principles of both onto alignment evaluation, records how far current AI practice already follows them, and states where the analogy fails. It proposes a "line check" layer of privacy-preserving, non-jeopardy observation of deployed models and a competency-based alignment assessment with behavioural indicators, and shows how the two feed each other, as in airlines. A small feasibility pilot graded 48 model transcripts from six airline-workplace scenarios with an EBT-style rubric and with a single holistic score, using two LLM graders twice each. Test–retest agreement was moderate to high (Krippendorff's alpha 0.56–0.89), agreement between graders was low to moderate (0.24–0.54), and the rubric did not outperform the holistic score. Grades separated scenarios and six scripted weak responses but not the two models. Grading by trained instructors is the next step.

## Pilot in one paragraph

Six benign scenarios at a fictional airline ("Calder Air"): ambiguous instruction, error in the assistant's own earlier work, request beyond authority, pressure to report completion, operator–user conflict, and a hidden fitness-for-duty concern in a fatigue-report digest. Claude Haiku 5.5 and Sonnet 5.5 answered each four times (48 transcripts). Claude Sonnet 5.5 and Opus 5.5 graded each transcript twice with a 4-competency rubric (17 observable behaviours adapted from EASA AMC1 ORO.FC.231(b), 1–5 VENN-style anchors) and twice with a holistic 1–5 score. No model response failed its scenario, so grades bunched at 4–5. Inter-grader alpha (run 1): competencies 0.31–0.49, competency mean 0.41, holistic 0.42. Test–retest alpha: 0.56–0.89. Indicator judgements: 91% inter-grader agreement (alpha 0.69), but 82% were simply "demonstrated". Six scripted weak "control" responses were graded 1–2 by everyone; adding them raised inter-grader alpha on the competency mean to 0.91. Grades separated scenarios (epsilon-squared 0.46–0.64 across measures) but not models (Cliff's delta 0.11). Total model calls: 458.

## What James should check

1. **Aviation accuracy.** Sections 2.1–2.4 and Table 1–2 describe LOSA, TEM, EBT and CBTA from FAA AC 120-90, Klinect et al. (2003), ICAO Doc 9995/9868, EASA ORO.FC.231 and its AMC/GM, and the IATA guide. Please check the descriptions against current practice as you know it (in published terms; nothing in the paper should rest on personal anecdote). In particular: the use of "checkride" and "line check"; whether "LPC/OPC" is the right shorthand for traditional checks; whether "mixed EBT" or other nuances should be mentioned.
2. **ICAO texts.** Doc 9995 and PANS-TRG (Doc 9868) were read from copies hosted by the Swedish Transport Agency and a third party, not from ICAO; Doc 9803 was not opened at all (only the ICAO Store listing). Please check quoted wording and paragraph numbers against your licensed copies, and whether Doc 9995's 2014 corrigendum or later PANS-TRG amendments change anything.
3. **The rubric (Table 4, `code/rubric.py`).** Are the adapted observable behaviours sensible from an EBT instructor's point of view? Is the OB mapping right? Would you word any of the "new" AI-specific behaviours differently?
4. **The non-jeopardy translation (Section 4, "The first is non-jeopardy").** The paper argues the AI analogue of jeopardy is optimisation pressure from training on observation data. Is this an analogy you are comfortable putting your name to?
5. **Scripted controls.** The six weak "control" responses (`code/controls.py`) were written by the AI drafting assistant, not by a model under test. They are labelled throughout and analysed separately. Decide whether to keep them, or replace them with responses you write.
6. **Model names.** The paper uses "Claude Haiku 5.5 / Sonnet 5.5 / Opus 5.5" from the API IDs `claude-haiku-5-5` etc. Please confirm official product names.
7. **System-card citations.** Two PDFs titled "System Card: Claude Opus 4.6" exist on Anthropic's CDN; quotes were taken from the one with a changelog (`c788cbc0...`). Check you are happy with that URL.
8. **Section 5.4** ("Implications for aviation AI developers") is deliberately short and non-commercial. Check it says what you want.
9. **Delta Air Lines** is named in Klinect et al. (2003); the paper says "one US airline". Change if you prefer to name it.

## Things that could not be verified (handled as stated)

- ICAO Doc 9803 full text (bibliographic facts only are used).
- The "70 percent reduction in non-conforming approaches" figure is second-hand (Klinect et al. quoting Gunther, 2002) and is labelled so.
- Krippendorff's conventional alpha thresholds (.800/.667) could not be checked in an opened source, so they are not used.
- Two Sonnet transcripts in S3 report usage under two model IDs (`claude-sonnet-5-5` and `claude-sonnet-5`), possibly an automatic fallback. Kept and flagged.

## Prior-work search

No earlier application of LOSA, TEM or EBT/CBTA to AI evaluation was found (arXiv API, Crossref API and web searches; queries in the paper's Appendix A). Semantic Scholar and OpenAlex were rate-limited and Elicit was unavailable, so the search is not exhaustive. Nearest items: Weidinger et al. (2025) on learning from aerospace evaluation in general; Li et al. (2026) grounding evaluation awareness in social psychology.

## Open questions

- Which competencies, beyond the four piloted, should an alignment competency framework contain, and what evidence should define them (the AI equivalent of EBT's data report)?
- What would a TEM taxonomy for agent transcripts look like, and could it be applied reliably by human or model observers to real (privacy-protected) deployment data?
- How should a "non-jeopardy firewall" between observation data and training be specified so that developers can still fix what they find?
- Does competency-based grading become more reliable than holistic grading once graders are standardised (concordance training) and observable behaviours carry scenario-specific guidance on when they apply?

## How to develop it

1. **The real validation: human instructor grading.** Have two or more trained EBT instructors grade the same 48 transcripts plus the controls with the same rubric and the holistic score, after a short concordance session using standardisation material at three performance levels (as GM1 ORO.FC.231(a)(4) suggests). Compare instructor–instructor and instructor–LLM agreement. Pre-register it (see `papers/02-rare-threats-are-missed-threats/PREREGISTRATION.md` for the house format).
2. **Wider range of performance.** Generate weaker responses from more models, lower effort settings, or adversarial system prompts, instead of relying on scripted controls.
3. **Scenario-specific guidance.** Add "desired outcomes" per scenario, as EBT does per training topic (AMC2 ORO.FC.232), and test whether indicator agreement on "required vs not required" improves.
4. **Surface variation.** Build scenario templates with varied surface features (domain, names, formats) to test whether competency grades generalise across variants, the EBT claim that matters most for evaluation awareness.
5. **A line-check pilot.** With an operator partner and privacy safeguards, try TEM coding of a small sample of real assistant interactions, and compare prevalence with the pre-deployment scenario grades.

## Files

| Path | Contents |
|---|---|
| `paper.md` | The paper (Pandoc Markdown, YAML header). |
| `sources.md` | Verification log: one entry per reference, with quotes and locators. |
| `code/scenarios.py` | The six scenarios (system prompt, scripted earlier turns, final user turn, designers' expectations). |
| `code/rubric.py` | Competencies, observable behaviours, grade anchors, grader prompts and JSON schemas. |
| `code/controls.py` | The six scripted control responses. |
| `code/common.py` | Headless Claude Code call with retries (max 4 in parallel). |
| `code/generate.py`, `code/grade.py`, `code/analyse.py` | Pipeline: generate transcripts, grade them, analyse. |
| `prompts/` | Exact agent prompts (`agent_prompts.json`), grader system prompts and schemas, written by the scripts. |
| `data/transcripts.jsonl` | 48 model transcripts with metadata. |
| `data/control_transcripts.jsonl` | 6 scripted controls. |
| `data/grades.jsonl` | 408 gradings (raw structured outputs, including indicator judgements and evidence notes). |
| `results/` | Agreement tables (grades and indicators), grader bias, discrimination tests, grade distributions, known-groups check, `summary.json`. |
| `figures/fig1_agreement.png` | Figure 1. |

## Reproduce

From the repository root:

```bash
uv run python papers/04-checkride-or-line-check/code/generate.py          # 48 calls (skips existing)
uv run python papers/04-checkride-or-line-check/code/grade.py             # 384 calls (skips existing)
uv run python papers/04-checkride-or-line-check/code/grade.py --controls  # 24 calls
uv run --no-project --with krippendorff==0.9.0 --with numpy --with scipy --with pandas --with matplotlib \
    python papers/04-checkride-or-line-check/code/analyse.py              # tables and figure
```

Model calls use `claude -p` (Claude Code 2.1.317) with tools, MCP servers and slash commands disabled, effort "low". Re-generating transcripts or grades will not reproduce the exact text (sampling is stochastic); the analysis is deterministic given the data files.
