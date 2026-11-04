# Design claims against documentation

*4 November 2026. The AI annotator saw only the trace, so every design code it gave (L4.1–L4.3) is an inference about how the system was built. This check takes its most frequent design claims for each framework (from the primary Sonnet run, `sonnet_bulk_r1`) and tests them against the framework's paper, documentation and source code at the version MAST appears to have run, against MAST's own description, and against framework messages in the logs.*

*Method. Three research agents each checked two frameworks, citing sources. I re-counted their log-based figures against the local traces (MathChat repeat-detection messages, the MetaGPT role sequence, OpenManus duplicate-response nudges, and AppWorld calls to a non-existent supervisor API); all matched. MAST publishes no configuration or versions for any framework, so "as MAST ran it" is reconstructed from the logs. No benchmark questions, answers, patches or tests are reproduced here.*

**Verdicts:** confirmed · partly true (part of the claim holds) · contradicted · not settled (public sources cannot decide).

## Summary

| Framework | Claims checked | Confirmed | Partly true | Contradicted | Not settled |
|---|---|---|---|---|---|
| MetaGPT | 5 | 2 | 3 | 0 | 0 |
| AG2 | 4 | 1 | 2 | 1 | 0 |
| Magentic-One | 6 | 2 | 3 | 1 | 0 |
| OpenManus | 4 | 1 | 3 | 0 | 0 |
| HyperAgent | 3 | 0 | 3 | 0 | 0 |
| AppWorld | 2 | 1 | 0 | 0 | 1 |
| **All** | **24** | **7** | **14** | **2** | **1** |

**The pattern.** The annotator usually pointed at the right weakness but overstated it as an absence. It said "no verifier", "no termination logic" or "no loop detection" where the system has the mechanism but in a weak form:
- MetaGPT has a reviewer, but it reviews only the tests; it also has round and budget caps.
- MathChat detects repeated results.
- Magentic-One's orchestrator asks itself every turn whether it is in a loop, and re-plans when stalled.
- OpenManus has a duplicate-response detector, but it only nudges.
- HyperAgent's editor has a syntax check, and running tests is optional.

A weak mechanism that did not work leaves the same trace as a missing one, so a trace cannot tell "absent" from "present but ineffective".

**Two claims put a failure at the wrong layer:**
- Magentic-One's failed audio transcription is a run-time fault (L2.1). The design includes transcription.
- OpenManus's missing Python packages come from how MAST set up the environment, not from OpenManus's design.

**The annotator missed limits it could not see.** These include Magentic-One's 20-turn budget and a web-reading limit after the first page read.

**Implication for AFACS.** Design factors coded from a trace alone should be read as "no effective safeguard visible in the trace", not "no safeguard in the design". A future codebook version could grade the evidence for L4 codes as it does for violations: *documented* (confirmed from design records) or *inferred* (from the trace alone).

## Findings about MAST itself

The check also found discrepancies in MAST's documentation, which add to the reconstruction problems in the information audit.

1. **MetaGPT is not what MAST describes.**
   - The MAST paper calls MetaGPT an SOP-based system with "agents such as a Coder and a Verifier", listed among "systems with explicit verifiers".
   - The logs show MetaGPT's small three-role example instead (`examples/build_customized_multi_agents.py`). 425 of the 430 traces follow its exact sequence: Coder, Tester, Reviewer, Tester, Reviewer.
   - In that example the reviewer gives "one critical comment" on the tests only, and nothing ever revises the code.
2. **MathChat's roles are described the other way round.** MAST describes a student agent working with an assistant "capable of Python code execution". In AG2's MathChat, it is the proxy (no LLM) that runs the code.
3. **The HyperAgent model label is doubtful.**
   - MAST's HyperAgent traces are taken from a public SWE-bench submission (`20240925_hyperagent_lite1`), not from MAST's own runs.
   - MAST's paper labels them Claude-3.7-Sonnet, a model released in February 2025, after that submission's September 2024 date (MAST's dataset itself just says "Claude").
   - The submission's metadata says GPT-4o, and HyperAgent's own run script uses Claude-3.5-Sonnet with Claude-3-Haiku.
4. **Some set-ups are MAST's own and unpublished.**
   - **AppWorld:** the multi-agent set-up was built by MAST's authors from AppWorld's single-agent baseline. Its prompts and code are not published.
   - **AG2 MMLU:** the team (Problem Solver, Code Executor, Verifier) adapts the three-agent topology whose prompts MAST publishes for GSM-Plus; the MMLU-specific prompts are not published.
5. **No versions or configurations are published.** For Magentic-One the version appears only in each log's installation output (autogen-agentchat, autogen-core and autogen-ext 0.4.9, built from a local checkout; traceback line numbers agree), run through AutoGen's agbench GAIA template. OpenManus appears to have been run from a local checkout around 30 March 2025. Its one-hour timeout is OpenManus's own default, not MAST's harness.

## Claim by claim

### MetaGPT (L4 in 60 of 60 failed traces)

*As run:* MetaGPT's three-role example. SimpleCoder writes code once; SimpleTester writes tests and rewrites them after each review; SimpleReviewer comments on the tests. All are plain LLM calls with no tools, run with `Team.run(n_round=5)`.

Sources:
- [example code (v0.8.2)](https://github.com/FoundationAgents/MetaGPT/blob/v0.8.2/examples/build_customized_multi_agents.py)
- [team runner](https://github.com/FoundationAgents/MetaGPT/blob/v0.8.2/metagpt/team.py)
- [LLM settings](https://github.com/FoundationAgents/MetaGPT/blob/v0.8.2/metagpt/configs/llm_config.py)
- [MAST paper](https://arxiv.org/html/2503.13657v3)

| Claim | Verdict | Evidence | Note |
|---|---|---|---|
| No agent or step runs the code or tests (~39 traces) | Confirmed | All three actions only call the LLM; no trace contains execution output | A pytest result in one trace was written by the model, not produced by a run |
| Nothing checks the deliverable against the task / no verifier (~9) | Partly true | Reviewer prompt: "Review the test cases and provide one critical comments" | Nothing compares the code with the task, but a reviewer role exists (MAST counts it as a verifier) |
| No termination logic (~14) | Partly true | `n_round = 5`, budget `investment = 3.0`, idle stop, `max_token = 4096` | The run is capped. What is missing is any check on degenerate or repetitive content. One CodeLlama trace has 197 steps, so MAST's v2 settings may differ |
| No revision loop: the coder never revises (~10) | Confirmed | SimpleCoder watches only the user requirement; the tester watches code and reviews | Only the tests are revised. Three CodeLlama logs show the coder again, which the public code does not explain |
| No output length or stop limits (a few, L4.2) | Partly true | Defaults `max_token = 4096`, `stop = None` | MAST's local model serving settings cannot be checked |

### AG2 (L4 in 12 of 31 failed traces)

*As run:*
- **(a) MathChat:** an assistant plus `MathUserProxyAgent`. The proxy has no LLM. It runs code, sends fixed replies, ends the chat at the first boxed answer, and caps automatic replies at 15.
- **(b) MMLU team:** Problem Solver, Code Executor and Verifier. This is MAST's own topology (paper appendix H.1, prompts in L.3–L.5), with the MMLU variant unpublished.

Sources:
- [MathChat proxy (v0.7.5)](https://github.com/ag2ai/ag2/blob/v0.7.5/autogen/agentchat/contrib/math_user_proxy_agent.py)
- [MathChat notebook](https://github.com/ag2ai/ag2/blob/v0.7.5/notebook/agentchat_MathChat.ipynb)
- [MAST topology traces](https://github.com/multi-agent-systems-failure-taxonomy/MAST/tree/main/traces/math_interventions/topology_traces)

| Claim | Verdict | Evidence | Note |
|---|---|---|---|
| (a) The proxy only runs code and replies "Continue"; no verifier or second pass (~7) | Confirmed | The proxy returns a fixed reply when there is no code, and ends at a boxed answer | The only second pass is the prompt asking the assistant to check itself |
| (a) No termination logic or loop detection | Contradicted | `MAX_CONSECUTIVE_AUTO_REPLY = 15`; ends at a boxed answer; repeat detection: "Your query or result is same from the last, please try a new approach." (26 of 429 MathChat traces) | The checks are shallow: repeat detection compares only consecutive execution outputs |
| (b) No outside knowledge source; the Verifier only checks that the answers agree | Partly true | Problem Solver "without tools"; the Verifier is told to "critically evaluate the solutions proposed by other agents step by step" | No knowledge source: confirmed. "Only checks agreement" contradicts the prompt, though the Verifier has no tool of its own and often just notes agreement |
| (b) No procedure when one agent contributes nothing | Partly true | Verifier prompt: "If either proposed solution is missing, do not draw any conclusions; instead, suggest the next speaker" | A procedure exists (ask again), with no fallback beyond that |

### Magentic-One (L4 in 16 of 54 failed traces, almost all L4.2)

*As run:* AutoGen 0.4 `MagenticOneGroupChat` through agbench's GAIA template, with `max_turns = 20`. The orchestrator keeps a task ledger and a per-turn progress ledger, which includes the question "are we in a loop", and re-plans after 3 stalls by default. The 20-turn cap is a binding budget the annotator did not name: 56 of 195 traces use 18–20 worker turns.

Sources:
- [paper (Fourney et al.)](https://arxiv.org/abs/2411.04468)
- [orchestrator (v0.4.7)](https://github.com/microsoft/autogen/blob/python-v0.4.7/python/packages/autogen-agentchat/src/autogen_agentchat/teams/_group_chat/_magentic_one/_magentic_one_orchestrator.py)
- [GAIA template](https://github.com/microsoft/autogen/blob/python-v0.4.7/python/packages/agbench/benchmarks/GAIA/Templates/MagenticOne/scenario.py)

| Claim | Verdict | Evidence | Note |
|---|---|---|---|
| No tool can view or interpret images | Partly true | FileSurfer converts files to Markdown with no image model; the paper calls WebSurfer "inherently multi-modal" and it accepts `file://` URLs | True for FileSurfer (a design limit). Not true for the team: WebSurfer was never asked to open the image (a coordination problem) |
| No working audio transcription | Partly true | Paper: audio "processed through a speech transcription model"; the agbench image installs the transcription packages; the traces show conversion errors | Transcription is in the design and failed at run time: L2.1, not L4.2. Non-speech audio remains a real design gap |
| WebSurfer cannot play videos | Confirmed | Paper: "WebSurfer cannot watch online videos" | It can sometimes use transcripts instead |
| WebSurfer can only scroll; no find-on-page | Partly true | The tool list has no find-on-page action; the reading actions use document question-answering | "Only scroll" is wrong. An undocumented limit: after the first read, the reading actions see only the first 200 lines of a page |
| No verifier | Confirmed | No verifier agent; completion is the orchestrator's own judgement | The paper's own error analysis notes tasks "marked as complete without thorough validation" |
| Nothing breaks loops | Contradicted | Ledger: "Are we in a loop…"; stall counter and re-planning (re-plans seen in 94 of 195 traces) | The mechanism exists but depends on the model judging itself |

### OpenManus (L4 in 19 of 23 failed traces)

*As run:* one agent, Manus (python_execute, browser_use, str_replace_editor, terminate), inside `PlanningFlow`. It was run from a local checkout near commit `964b2af` (30 March 2025), with the task read from a file.

Sources:
- [agent base](https://github.com/FoundationAgents/OpenManus/blob/964b2afc0ffec6e1e4946d11e7830b1db4d3cc52/app/agent/base.py)
- [planning flow](https://github.com/FoundationAgents/OpenManus/blob/964b2afc0ffec6e1e4946d11e7830b1db4d3cc52/app/flow/planning.py)
- [Manus agent](https://github.com/FoundationAgents/OpenManus/blob/964b2afc0ffec6e1e4946d11e7830b1db4d3cc52/app/agent/manus.py)

| Claim | Verdict | Evidence | Note |
|---|---|---|---|
| No loop detection or termination beyond a step cap and a one-hour timeout (~14) | Partly true | `is_stuck()` adds "Observed duplicate responses. Consider new strategies…" (fired in 11 of 30 traces) | A detector exists but only nudges, never stops the run, and misses loops of repeated tool calls |
| Plan steps are marked completed without checking their output (~11) | Confirmed | The planning flow marks a step completed after any normal return, including "reached max steps" | Design (L4.1) |
| A 20-step budget and a one-hour timeout limit the run (~14) | Partly true | `max_steps = 20`; `timeout=3600` (OpenManus's own default) | The step cap applies per plan step and never ended a task. The timeout ended 24 of 30 runs |
| Missing tools or packages (~6) | Partly true (true, but a set-up cause, not design) | Missing modules (e.g. pptx, matplotlib, pytesseract); no install tool | Comes from MAST's environment set-up, not OpenManus's design |

### HyperAgent (L4 in 7 of 13 failed traces)

*As run:* the traces come from a public SWE-bench submission (`20240925_hyperagent_lite1`), not from MAST. A Planner delegates to a Navigator, Editor and Executor. Each returns a condensed summary; the Navigator's is produced by a separate small model.

Sources:
- [paper (Phan et al.)](https://arxiv.org/html/2409.16299)
- [code](https://github.com/FSoft-AI4Code/HyperAgent)
- [SWE-bench submission](https://github.com/swe-bench/experiments/tree/main/evaluation/lite/20240925_hyperagent_lite1)
- [MAST HyperAgent README](https://github.com/multi-agent-systems-failure-taxonomy/MAST/blob/main/traces/HyperAgent/README.md)

| Claim | Verdict | Evidence | Note |
|---|---|---|---|
| No independent verifier or test step; the Planner relies on summaries (~5) | Partly true | Paper: "Summaries … are sent back to the Planner"; the Executor "validates solutions"; the Planner prompt makes testing optional | Summaries: confirmed. Testing exists but is optional and the Planner decides when the task is done (only 6 of 28 traces run a test suite) |
| The Editor only has line-range patching, with no verification (~2–3) | Partly true | Editor arguments: file, start_line, end_line, patch; each edit is linted and rejected on syntax errors | Line-range editing: confirmed. "No verification" is wrong, although the check is syntax-only |
| The environment could not build or run the tests (~2) | Partly true | Every command runs under a built-in timeout (default 60 s); commands run in a fresh, unbuilt clone | Better coded as a design limit (L4.2) than a run-time malfunction; the build-failure explanation is inferred, not documented |

### AppWorld (L4 in 3 of 20 failed traces)

*As run:* MAST's own adaptation (MAST paper, appendix B.2). A Supervisor holds the user's information and credentials, and talks one-to-one with app agents that hold each app's documentation. The prompts are unpublished.

Sources:
- [MAST paper](https://arxiv.org/html/2503.13657)
- [AppWorld paper](https://arxiv.org/html/2407.18901)
- [AppWorld code](https://github.com/StonyBrookNLP/appworld)

| Claim | Verdict | Evidence | Note |
|---|---|---|---|
| Credentials (Supervisor) are split from API knowledge (app agents), so neither holds the full path to authentication | Confirmed | MAST B.2 describes exactly this split; in the traces each agent calls only its own APIs | The split is in what each agent knows, not what it may call. It belongs to MAST's adaptation, not to AppWorld (whose single agent sees the whole path) |
| No standard procedure for passing credentials | Not settled (likely true) | `send_message()` has no credential field, so credentials travel as free text; repeated hand-over failures in the logs | The unpublished prompts may say otherwise |
