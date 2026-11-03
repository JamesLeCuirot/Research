# AFACS: a plain-English guide to what we are doing

*For James. Read this before any interview. Every part of the project is explained here without assuming a machine-learning background. Where a decision was made on your behalf, it is listed in section 5 so you can overrule it.*

---

## 1. The project in one paragraph

AI "agents" are language models (like Claude or GPT-4o) that act in steps: they plan, call tools, write code, and talk to other agents. When several agents work together it is called a *multi-agent system*. These systems fail a lot. The best-known study of why (MAST, Cemri et al. 2025) collected 1,642 recordings of such systems running (*traces*) and had another AI label each failure with one of 14 flat categories, e.g. "1.1 Disobey Task Specification". Aviation learned long ago that flat labels hide two things: **layered causation** (Reason's Swiss cheese, HFACS: the visible unsafe act sits on top of preconditions, supervision and organisational factors), and the difference between an **error** (an unintended slip or mistake) and a **violation** (a departure from a known requirement). For AI, that second distinction is roughly *capability problem vs alignment problem*, which is what AI-safety people care most about. We adapt HFACS to agent traces (AFACS), re-code a sample of MAST traces with it, measure whether it can be applied reliably, and show what it reveals that the flat labels miss.

### The direction, as decided on 3 November

The first paper **builds on Ezell, Roberts-Gaal & Chan (2025), "Incident Analysis for AI Agents"**, rather than competing with it. Their framework has three categories of cause (system factors, contextual factors, cognitive errors) and was written for single agents, without data. AFACS extends it to multi-agent systems with the HFACS structure, and answers several of the open challenges in their Appendix B. The four research questions are now:

1. **Cross-walk.** How do Ezell et al.'s categories map onto HFACS, and what does a multi-agent setting add? (A supervision/orchestration tier, coordination between agents, and violations with graded evidence.) Mapping: `docs/crosswalk_ezell.md`.
2. **Information adequacy.** Do real multi-agent logs contain the 18 kinds of information Ezell et al. say investigators need? (`docs/information_audit.md`; no coding needed.)
3. **Applicability.** Can the extended framework be applied consistently? Claude codes the 250-trace bulk sample twice (two models, and a re-run), and we measure agreement, set against MAST's own judge agreeing with itself at κ 0.43. This shows **consistency, not correctness**.
4. **Flat labels.** How do MAST's 14 labels map onto the extended framework?

**Human validation becomes paper 2.** Recruited coders who can read code will use the Coding Desk and the frozen 30-trace calibration set, which the AI pilot never touches. Your role in paper 1 is the framework itself: the cross-walk, codebook v1, and expert review of a few AI codings as case studies.

## 2. The pipeline, stage by stage

```
 MAST dataset ──► 1 ingest ──► 2 render ──► 3 sample ──┬──► James hand-codes 30 traces (calibration)
 (Hugging Face)   clean +      readable     choose     │            │
                  split into   markdown     which      │            ▼
                  steps                     traces     └──► 4 annotate (Claude codes the same traces, then 250 more)
                                                                    │
                                                        5 agreement ◄┘  (does Claude code like James? RQ1)
                                                                    │
                                                        6 analysis      (RQ2-RQ4, figures, write-up)
```

Each stage is one Python file in `src/afacs/` and one command. You can run any of them with `uv run <command> --help` to see what it does.

### Stage 1: ingest (`afacs-ingest`, `ingest.py` + `parsers.py`)

**What it does.** Downloads the MAST data, checks it is exactly the version we expect, cleans it, and splits every trace into numbered steps ("[S1] user asks...", "[S2] orchestrator replies...").

**Why it matters.**
- *Reproducibility.* We download a pinned version (a fixed "revision" of the dataset) and check its fingerprint (a SHA-256 hash: a long number computed from the file's exact bytes; change one byte and the number changes). Anyone re-running the project gets byte-identical data.
- *Data quality.* We found real problems in the MAST data (section 4). Ingest flags them and writes `docs/data_audit.md`, so they are documented, not hidden.
- *Step numbers.* MAST stores each trace as one long blob of text, in seven different log formats (one per framework). To cite evidence ("the orchestrator ignored the error at S14") we need steps. `parsers.py` has one small parser per format. They keep the agents' words verbatim and only strip log clutter (timestamps, separators) and a few kinds of pure noise (package-installation logs, token counters). Every character dropped is counted, and a check confirmed that only clutter is lost.

**In an interview:** "The first job was data hygiene. I pinned the dataset version, audited it, and found duplicates, mislabelled metadata, and a corrupt group, which I excluded with documented reasons."

### Stage 2: render (`afacs-render`, `render.py`)

**What it does.** Turns one trace into a readable markdown file: a header, a reading note, then each step in a box. Try `uv run afacs-render C01`.

**Why it matters.** You (the expert) and Claude (the annotator) must see *exactly the same thing*, otherwise any disagreement could be about what each of you saw rather than how you each applied the codebook. So the annotator reads the same rendering. MAST's labels are **hidden** by default, so neither of you is anchored by them. Steps holding information the agents never saw (the benchmark's correct answer, or its own pass/fail verdict) are **hidden during coding**: a visible "success: true" would give away the controls, and knowing the answer tempts you to judge the outcome rather than the process. The step stays in place as a placeholder so step numbers don't change, and you can view it after coding with `--show-benchmark`. Where a log has a known artefact (OpenManus logs print only the first ~50 characters of the task), a clearly marked "Note added by AFACS" says so.

### Stage 3: sample (`afacs-sample`, `sample.py`, `design.py`)

**What it does.** Picks which traces get coded.

- **Calibration set (30 traces), for you.** 5 traces from each of 6 frameworks. In 4 of the frameworks, one of the 5 is a trace MAST said was *fine* (a **control**) instead of a failed one. Every framework has 5 rows, so the sheet doesn't reveal where the controls are. Shuffled and renamed C01–C30.
- **Bulk set (250 traces), for Claude later.** Spread evenly across frameworks so small frameworks aren't swamped.

**Key ideas.**
- *Stratified sample:* instead of drawing 30 at random from everything (which would give mostly AG2 and MetaGPT, the big groups), we draw a fixed number from each group (*stratum*). That way every framework is represented.
- *Blind coding and controls:* you don't see MAST's labels, and you don't know which 4 traces MAST judged fine. If you also code those as fine, good; if you find failures MAST missed, that's a finding. It also stops you assuming every trace is "guilty".
- *Dev/test split, decided in advance:* 18 traces are **dev** (used to tune Claude's instructions), 12 are **test** (never looked at while tuning; used once, at the end, to report agreement honestly). The split is fixed *now*, before any coding, and stored in a hidden key file (`data/processed/calibration_key.csv`; don't open it while coding). A fingerprint of that file (`annotations/human/calibration_key.sha256`) is committed, so anyone can later check the key wasn't changed: `uv run afacs-sample calibration --verify`. Aviation analogy: you brief the approach before you fly it, not after you see how it went. In research this is called *pre-registration*: it stops you, even unconsciously, choosing a test set that flatters the result.
- *Random seed:* the random draws use a fixed seed (a starting number for the random generator), so the same traces come out every time.

### Stage 4: annotate (`afacs-annotate`, `annotate.py`, `prompts/annotator_v0.md`)

**What it does.** Sends each trace to Claude with instructions plus the codebook, and gets back a coding in the same columns as your sheet.

**Key ideas.**
- *The prompt* (`prompts/annotator_v0.md`) is the instruction sheet: "you are a safety investigator... code every layer where there is evidence... apply the violation rule strictly... quote evidence with step numbers". The codebook is pasted in. You can read exactly what Claude sees with `uv run afacs-annotate show-prompt --uid C01`.
- *Structured output:* the API forces Claude's reply into a fixed form (a JSON "schema"), and the only codes it is allowed to use are the ones in the codebook. It cannot invent a code or skip a field.
- *Prompt caching:* the instructions + codebook are the same for every trace, so the API stores them after the first call and charges a tenth of the price for re-reading them.
- *Versioning:* each annotation records the model, the prompt version, the codebook version, and a fingerprint of the full instructions. If anything changes, we can tell which annotations came from which version.
- *Models:* `claude-sonnet-5-5` for the bulk run; `claude-opus-5-5` optionally as a second annotator. These models give slightly different answers if asked twice (there is no way to make them fully deterministic), so we will also measure Claude-vs-Claude agreement.
- *Cost:* estimated with `uv run afacs-annotate estimate --set bulk`. Roughly **$14 for 250 traces with Sonnet** (about $7 via the half-price "batch" service, which returns results within 24 hours), $28 with Opus. Calibration-size runs cost about $2. The whole project should cost well under $60.
- *Refusals:* if Claude declines to process a trace, it is recorded as an error, not quietly handed to a different model, because an agreement study needs one fixed annotator.

**Runs on:** your Claude subscription, through Claude Code's headless mode (the default `--backend claude-code`). No API key is needed; the calls count against your plan's usage limits, and a run that hits a limit stops and resumes where it left off. The direct API route (`--backend api`, key in `.env`) remains available, and is the only way to use the half-price batch service.

### Stage 5: agreement (`afacs-agreement`, `agreement.py`) — RQ1

**What it does.** Compares two sets of codings of the same traces (you vs Claude, or Claude vs Claude) and reports how well they agree.

**Cohen's kappa (κ), explained.** Suppose you and Claude each say yes/no to "is there an L3 factor?" for 12 traces, and you agree on 10. That's 83% agreement. But if both of you say "yes" to almost everything, you'd agree a lot by chance alone. κ corrects for that:

> κ = (observed agreement − agreement expected by chance) ÷ (1 − agreement expected by chance)

κ = 1 is perfect, 0 is no better than chance, negative is worse than chance. A common reading (Landis & Koch, 1977): 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, above 0.80 almost perfect. It's widely used for inter-rater reliability in HFACS studies as well as in machine learning, so reviewers from both worlds know it.

**What we compute.** κ for each layer (present / absent), each code, error vs violation, the deepest layer, and failure observed. With only 12 test traces, κ is imprecise, so each headline κ comes with a **95% bootstrap confidence interval**: we re-draw the 12 traces with replacement 2,000 times, recompute κ each time, and report the range covering the middle 95%. Wide intervals are expected and must be reported honestly. Where an interval would be meaningless (e.g. one of you marked nearly every trace "yes"), it is left out and the report shows how many "yes" answers each coder gave.

**Why per code, never pooled.** An easy mistake (I made it at first on the MAST data) is to put all codes in one long list and compute one κ. Codes that are almost always "no" then count as agreement, and κ is inflated. On MAST's duplicates, pooling gave 0.54, while the correct per-code average is 0.43.

**Also:** `uv run afacs-agreement check-sheet` checks your coding sheet for typos and inconsistencies (an unknown code, a code in the wrong column, a deepest layer that doesn't match your codes).

### Stage 6: analysis (`afacs-analysis`, `analysis.py`) — RQ2, RQ3, RQ4

- **RQ2, latent causes:** what share of failed traces have a contributing factor above the unsafe-act layer (L2, L3 or L4)?
- **RQ3, errors vs violations:** what share carry a violation code, by framework and by model? And does MAST's "1.1 Disobey Task Specification" mix errors and violations?
- **RQ4, the cross-walk:** for traces with each MAST label, which AFACS layers and codes appear? A heatmap shows where MAST labels map neatly onto one layer and where they spread across several (conflation).

Shares come with **Wilson 95% intervals**, a standard and well-behaved interval for a proportion when samples are small.

## 3. The codebook

`codebook/v0.md` is your original draft. `codebook/v1.md` is the current draft: your decisions so far (keep "violation", defined behaviourally; grade the evidence for every violation), a proposed L4.4 Model development code from Ezell et al., the Ezell category for each layer, the *proposed* operational notes carried over from v0, and the open questions still to decide. The codebook file is the single source of truth: the code list the software accepts is read straight from it (`CURRENT_CODEBOOK` in `src/afacs/schema.py` is now `"v1"`).

The proposed notes add **no new categories**. They add one field, `failure_observed` (yes / no / unclear), needed for the controls, and they spell out the violation rule as three questions in order. Accept, edit or delete them.

## 4. What we found in the MAST data (and why it matters)

Full numbers are in `docs/data_audit.md`; figures in `figures/`.

1. **Duplicates.** 1,642 rows but only 1,537 distinct traces. 30 Magentic traces appear under two names.
2. **MAST's judge disagrees with itself.** Those 30 duplicated traces were labelled twice by MAST's AI judge (OpenAI's o1). The two labellings agree with a mean per-code κ of only **0.43** ("moderate"), from 0.67 for some codes down to about 0 for others (`figures/mast_judge_test_retest.png`). This is a useful finding: the flat labels we are comparing against are themselves noisy. Small sample (30), so call it indicative.
3. **A corrupt group.** "ChatDev with CodeLlama" has 100 rows but only 30 distinct traces, and copies of the same trace carry unrelated labels. We excluded it.
4. **Wrong metadata.** OpenManus traces are tagged as a programming benchmark but are really GAIA questions; the AG2 "GSM" traces are GSM-Plus. Corrected. Two traces filed as HyperAgent are actually ChatDev logs; excluded.
   OpenManus logs print only the first ~50 characters of each task (the agents got the full text); the rendered traces carry a note so nobody codes that as a bad task specification.
5. **Empty tasks.** In 5 traces the task text is empty: the experiment gave the agents nothing to do, yet MAST labels them, e.g., "Disobey Task Specification". There was no specification to disobey. This is a neat illustration of why layered coding matters (and an open codebook question: how to code test-harness defects).
6. **MAST's "human-labelled" file is unreliable.** It has 19 traces (not 21), uses three different versions of the taxonomy, and within each round different traces carry identical labels. The original annotation sheets (PDFs in MAST's GitHub repo) show different labels per trace, so the file was assembled incorrectly. We don't use it.
7. **No success/failure record.** MAST doesn't record whether each task actually succeeded. So "failed trace" means "MAST's judge flagged at least one failure mode". Only AppWorld and some AG2 traces carry the benchmark's own pass/fail.
8. **Model is tangled with framework.** Most frameworks ran only one model, and "Claude" has no version number. So comparisons between models are only possible within MetaGPT and AG2, and are exploratory.

## 5. Decisions made on your behalf (please review)

All study-design numbers live in `src/afacs/design.py` with their reasons.

| Decision | Why | Change it? |
|---|---|---|
| Exclude ChatDev | Traces are 60k–500k tokens (100+ pages each): too long to hand-code or to validate the annotator on | Possible, but costly in your time |
| Length cap ~30k tokens | Same reason; applied equally to calibration and bulk so the annotator is validated on the same kind of trace it codes | Easy |
| 30 traces: 5 per framework, 4 of them controls in place of a failed trace | Balance across frameworks; controls test for failures MAST missed; equal rows per framework keep the controls hidden | Frozen now (fingerprint committed) |
| Dev 18 / test 12, fixed in advance | Honest test of the annotator | Don't change after coding starts |
| Hide benchmark answers/verdicts while coding | Keeps controls hidden; code the process, not the outcome | Easy |
| Weight bulk results back to the eligible pool | The bulk sample over-represents small frameworks/models on purpose; weights undo that for overall figures | — |
| Exclude the two traces shown to you during planning | You saw their MAST labels, so coding them wouldn't be blind | — |
| Balanced bulk sample of 250 | Enough per framework to compare frameworks (RQ3) | Easy |
| No fallback to another model on refusals | One fixed annotator | Easy |
| Annotator effort "high" | Quality over cost; cost is small anyway | Easy |
| MIT licence for the code | Standard for a public portfolio repo | Your call |
| Don't commit the traces | Benchmark maintainers ask that questions (e.g. GAIA) not be reposted where web crawlers can find them | Recommended |
| Build paper 1 on Ezell et al. (2025); human validation in paper 2 | Positions AFACS as an extension; avoids a reference coding built on misread technical traces | **Decided by you** |
| Keep the term "violation", defined behaviourally | Continuity with HFACS; no claim about intent | **Decided by you** |
| Grade the evidence for every violation (stated / inferred / thin) | Makes the most contested judgement transparent | **Decided by you** |
| Add L4.4 Model development (from Ezell et al.) | Their system factors include training and feedback, which v0 had no code for | **Proposed: your call** (codebook v1, open question 1) |
| Run the annotator through Claude Code on your subscription | Your preference; no API key needed | **Decided by you** |
| AI pilot on the bulk sample only, never the 30 calibration traces | Keeps those traces untouched for human coders in paper 2 | Recommended |

## 6. What you do next

1. **Review codebook v1** (`codebook/v1.md`) and the cross-walk (`docs/crosswalk_ezell.md`). Decide on L4.4, the "[proposed]" operational notes and the open questions. Correct the cross-walk wherever your human-factors judgement differs from my draft.
2. **Approve the AI pilot.** Once codebook v1 is settled, Claude codes the 250 bulk traces through your subscription (it may take several sessions because of usage limits).
3. **Expert case studies.** Review a handful of the AI's codings with the trace beside you, and say where you agree or disagree and why. These become the case studies.
4. **Optional:** code the 10 short AG2 and MetaGPT calibration traces yourself (about 2 hours) as a small human anchor. Not required for paper 1.
5. **Read the paper draft** (`paper/afacs.pdf`) as it fills in.

## 7. Questions you should be ready for

- **"Hasn't this been done?"** Not as far as a careful search found (`docs/related_work.md`). The closest is Ezell, Roberts-Gaal & Chan (AIES 2025), who cite HFACS and propose a three-part framework for AI-agent incidents; this paper builds directly on theirs. They code no traces, measure no agreement, and their framework is for single agents with no supervision tier, no coordination and no violations. AFACS extends it on exactly those points and tests it on real traces. The closest *method* is Wiegmann & Shappell (2001): an aviation psychologist and a commercially rated pilot re-coded 319 NTSB causal factors into HFACS and got κ = 0.71. AFACS does the same kind of study on AI-agent traces, reading the raw traces rather than investigators' conclusions.
- **"Isn't HFACS itself unreliable?"** It is contested: Olsen & Shorrock (2010) found low agreement for a modified version used in air traffic control; a review (Cohen et al., 2015) found reliability is better with training and when the framework stays close to the original. That is why AFACS keeps the original four tiers and reports agreement at layer level, not only for fine-grained codes.
- **"Isn't using an LLM to judge an LLM circular?"** For correctness, yes, which is why paper 1 claims only consistency: whether the framework can be applied the same way twice, compared with MAST's own judge (κ 0.43 against itself). Whether the codes are *right* needs human coders, and that is paper 2, with a frozen, pre-registered set of traces the AI never touched.
- **"Why didn't you hand-code the traces yourself?"** Coding needs two skills: human-factors judgement, which I have, and reading technical agent logs (code patches, API calls), which is a different expertise. A reference coding built on misread traces would undermine the agreement test, so I designed the framework and the validation protocol, and the validation will use coders who can read the code, as Wiegmann and Shappell paired a psychologist with a pilot.
- **"Do AI agents really decide to break rules?"** We take no position on intent. Agents do weigh options, and their written reasoning sometimes names a rule and then departs from it (Baker et al., 2025). AFACS records that behaviour and grades its evidence (stated, inferred, thin), because "could not" and "registered the rule and did otherwise" need different fixes.
- **"Doesn't 'violation' imply the model *intended* to break a rule?"** No. The violation rule is behavioural: the requirement was in the agent's context, the trace shows the agent registered it (or the deviation can't plausibly be accidental), and it proceeded otherwise. We make no claim about intent or mental states. HFACS itself works from observable behaviour.
- **"Why κ and not percentage agreement?"** Percentage agreement rewards agreeing by chance: if both coders mark almost everything "no", they agree a lot without skill. κ removes chance agreement.
- **"How will the human validation work?"** In paper 2: 30 traces fixed in advance (26 failed, 4 hidden controls), a held-out set of 12 chosen before any coding, with a fingerprint of the hidden key committed so nobody can quietly change it.
- **"Why not use TRAIL?"** Its licence prohibits redistributing it. We cite it.
- **"What's the unit of analysis?"** One trace = one coding, multi-label across layers.
- **"What does AFACS show that MAST doesn't?"** Where failures sit in the layers, how often supervision and coordination are involved, how often failures are violations rather than errors (and on what evidence), and which MAST labels merge different causes (e.g. 1.1 can hold errors, violations, and even cases with no task at all).
- **"How did you use AI tools to build this?"** Claude Code wrote the pipeline under my direction; the framework, the codebook and the expert coding are mine; every design decision is written down in `design.py` and this guide.

## 8. Map of the repository

| Path | What it is |
|---|---|
| `README.md` | The write-up (research note), with figures |
| `docs/GUIDE.md` | This guide |
| `docs/CODING_GUIDE.md` | How to hand-code the calibration traces |
| `docs/data_audit.md` | Generated report on MAST data quality |
| `docs/related_work.md`, `docs/references.bib` | Literature review and references |
| `codebook/v0.md`, `codebook/v1.md` | The AFACS codebook (versioned; v1 is current) |
| `docs/crosswalk_ezell.md` | How Ezell et al.'s framework maps onto AFACS |
| `docs/information_audit.md` | What MAST's logs contain against Ezell et al.'s information needs |
| `paper/` | The paper (LaTeX source and PDF) |
| `prompts/annotator_v0.md` | The instructions given to Claude (versioned) |
| `annotations/human/calibration_sheet.csv` | Your coding sheet |
| `annotations/llm/` | Claude's codings, one file per run |
| `src/afacs/` | The code: `design.py` (all choices), `ingest.py`, `parsers.py`, `render.py`, `sample.py`, `schema.py`, `annotate.py`, `agreement.py`, `analysis.py` |
| `tests/` | Automated checks (`uv run pytest`) |
| `figures/` | Charts for the write-up |
| `results/` | Agreement and analysis tables (created when run) |
| `data/` | Downloaded and processed data (not committed; recreate with `uv run afacs-ingest`) |

**To recreate everything from scratch:**

```bash
uv sync
uv run afacs-ingest
uv run afacs-sample calibration --renders-only   # checks the frozen set; writes the trace files, never the sheet
uv run afacs-sample bulk
uv run afacs-analysis mast
```
