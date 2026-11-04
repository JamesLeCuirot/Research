"""Information audit (RQ2): do the MAST traces hold what incident investigators need?

Run:  uv run afacs-info-audit

The checklist is the 18 kinds of information that Ezell, Roberts-Gaal & Chan
(2025, "Incident Analysis for AI Agents", Table 1) say investigators need to
identify the causes of an AI-agent incident, grouped as activity logs, system
documentation & access, and tool-related information. Items marked * are mainly
needed to reconstruct (re-run) an incident.

For each of MAST's seven frameworks and each item we record:
- a STATUS: present / partial / absent / n/a (the item does not arise in these
  benchmark runs, e.g. tool information for agents that use no tools). The
  status is a documented judgement, written below with its reason.
- an automatic DETECTOR share where a reliable one exists: the share of the
  framework's traces in which a format-specific pattern fires (for example a
  timestamp at the start of a log line). The share is evidence for the status,
  not the status itself, and the run reports any cell where the two disagree.
- for items without a reliable detector, the judgement rests on reading the
  three sampled traces listed for each framework (first, middle and last by id).

Outputs: data/processed/info_audit.json, docs/information_audit.md (committed)
and figures/info_audit.png.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

from afacs import paths  # noqa: E402
from afacs.analysis import BLUE_RAMP, GRID, INK, INK_2, SURFACE  # noqa: E402
from afacs.ingest import load_traces  # noqa: E402

SOURCE = "Ezell, C., Roberts-Gaal, X. & Chan, A. (2025). Incident Analysis for AI Agents. AIES 2025. arXiv:2508.14231, Table 1."

# (key, category, Ezell et al.'s item name exactly as in their Table 1)
ITEMS = [
    ("system_prompts", "Activity logs", "System prompts"),
    ("user_prompts", "Activity logs", "User prompts"),
    ("external_info", "Activity logs", "External information"),
    ("scaffolding_logs", "Activity logs", "Scaffolding component logs"),
    ("reasoning", "Activity logs", "Model reasoning traces"),
    ("responses", "Activity logs", "Model responses and actions"),
    ("log_metadata", "Activity logs", "Log metadata (e.g., timestamps, identifiers, location)"),
    ("docs_changelogs", "System documentation & access", "System docs & change logs"),
    ("artifacts", "System documentation & access", "System artifacts"),
    ("configurations", "System documentation & access", "System configurations (e.g., seeds, version, temperature)*"),
    ("access", "System documentation & access", "Model & system access (e.g., API)*"),
    ("tool_id", "Tool-related information", "Tool identification & version"),
    ("tool_actions", "Tool-related information", "Tool actions & services enabled"),
    ("tool_docs", "Tool-related information", "Documentation & usage guides"),
    ("access_reqs", "Tool-related information", "Access requirements (e.g., API keys)"),
    ("personalization", "Tool-related information", "Personalization & stored data"),
    ("tool_state", "Tool-related information", "Tool state details"),
    ("tool_errors", "Tool-related information", "Tool errors & limitations"),
]
NAME = {k: name for k, _, name in ITEMS}
FRAMEWORKS = ["AG2", "MetaGPT", "ChatDev", "Magentic", "OpenManus", "AppWorld", "HyperAgent"]
STATUSES = ["present", "partial", "absent", "n/a"]

# ---------------------------------------------------------------------------
# Automatic detectors: format-specific patterns, each documented by what it finds.
# ---------------------------------------------------------------------------

TASK_NOTES = {"empty task requirement", "task text truncated in log", "task text missing from log"}
NON_AGENT = {"user", "Human", "user (GitHub issue)", "benchmark", "note", "system"}


def _rx(pattern: str, flags: int = 0):
    compiled = re.compile(pattern, flags)
    return lambda trace, raw: bool(compiled.search(raw))


def complete_task_logged(trace: dict, raw: str) -> bool:
    """The task text is in the log in full (not empty, truncated or missing)."""
    if TASK_NOTES & set(trace.get("parse_notes", [])):
        return False
    first = next((s for s in trace["steps"] if s["kind"] not in ("system", "benchmark_info")), None)
    return bool(first and first["text"].strip())


def agent_output_logged(trace: dict, raw: str) -> bool:
    return any(s["kind"] == "message" and s["agent"] not in NON_AGENT for s in trace["steps"])


# Sub-detectors used for several items (key -> (description, function)).
SUB = {
    "line_timestamps": ("a timestamp at the start of log lines",
                        _rx(r"^\[?\d{4}-\d\d-\d\d \d\d:\d\d:\d\d", re.M)),
    "run_identifiers": ("a run, task or instance identifier",
                        # Bare UUIDs are left out on purpose: in these logs they occur inside content
                        # (URLs, page reference numbers, attachment file names), not as run identifiers.
                        _rx(r"instance_id: \S|Task \d+/\d+ \(\w+\)|plan_\d{6,}|\*\*Timestamp\*\*: \d{14}")),
    "sampling_params": ("sampling parameters (e.g. temperature=...)", _rx(r"ChatGPTConfig\(|\btemperature\s*=\s*\d")),
    "model_identifier": ("a model identifier inside the log", _rx(r"ModelType\.\w+")),
    "scaffold_versions": ("versions of the scaffolding packages", _rx(r"autogen-(?:core|agentchat|ext)(?:==|-)\d")),
    "seed": ("a random seed", _rx(r"(?i)\bseed\s*[=:]\s*\d")),
}

DETECTORS = {
    "system_prompts": ("role or phase prompts logged ('assistant_role_prompt', 'phase_prompt')",
                       _rx(r"\*\*(?:assistant_role_prompt|user_role_prompt|phase_prompt)\*\*")),
    "user_prompts": ("the full task text is logged (not empty, truncated or missing)", complete_task_logged),
    "external_info": ("retrieved web pages, files, repository code or app data appear in the log",
                      _rx(r"The web browser is open to the page|Observed output of cmd `(?:browser_use|web_search)`|"
                          r"\bopen_file\b|get_all_symbols|Code Execution Output|-{10} FileSurfer -{10}")),
    "scaffolding_logs": ("log records written by the framework itself",
                         _rx(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+ \| \w+\s*\| [\w.]+:\w+:\d+ - |"
                             r"^\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d INFO\]|HyperAgent_\S+ - INFO - Initialized|"
                             r"SCENARIO\.PY (?:STARTING|COMPLETE)|Entering \w+ Agent message loop|"
                             r"=== MetaGPT Agent Communication Log", re.M)),
    "reasoning": ("a labelled reasoning section ('thoughts:' field or ReAct 'Thought:')",
                  _rx(r"Manus's thoughts:|^\s*Thought:", re.M)),
    "responses": ("at least one agent output", agent_output_logged),
    "log_metadata": ("timestamps on log lines or a run identifier", lambda t, r: SUB["line_timestamps"][1](t, r) or SUB["run_identifiers"][1](t, r)),
    "configurations": ("sampling parameters, a model identifier or scaffolding versions",
                       lambda t, r: any(SUB[k][1](t, r) for k in ("sampling_params", "model_identifier", "scaffold_versions", "seed"))),
    "tool_id": ("tool calls by name",
                _rx(r"Tools being prepared: \[|\w+\._run\(|apis\.\w+\.\w+\(|-{10} (?:WebSurfer|FileSurfer|ComputerTerminal) -{10}|exitcode: \d")),
    "tool_actions": ("a list of the agents' or tools' available capabilities",
                     _rx(r"(?i)we have assembled (?:the following|a great) team|api_docs\.show_(?:app|api)_descriptions")),
    "tool_docs": ("tool documentation requested and logged (api_docs.show_api_doc)", _rx(r"api_docs\.show_api_doc\(")),
    "access_reqs": ("credentials retrieved in the trace", _rx(r"show_account_passwords|\"password\":")),
    "personalization": ("user profile or memory settings", _rx(r"apis\.supervisor\.show_(?:profile|account)|with_memory")),
    "tool_state": ("reports of a tool's state (browser page, viewport)", _rx(r"(?i)viewport shows|The web browser is open to the page|Navigated to")),
    "tool_errors": ("tool, execution or API errors recorded in the log (share = traces in which at least one occurs)",
                    _rx(r"Traceback \(most recent call last\)|exitcode: [1-9]|exited with an error|POSIX exit code: [1-9]|"
                        r"Execution failed|^\S.*\| ERROR\s*\||Error executing", re.M)),
}

# ---------------------------------------------------------------------------
# Judgements (status + reason) for every framework x item. Written from the
# detector results and from reading the sampled traces; see the module docstring.
# ---------------------------------------------------------------------------

ALL_ABSENT = {
    "docs_changelogs": "No system documentation, model cards or change logs come with the traces or the dataset card.",
    "artifacts": "No model weights, checkpoints or snapshot of the scaffolding code; at most configuration file paths are logged.",
    "access": "The models were reached through vendor APIs or local servers that the dataset does not identify, and MAST names models without versions (e.g. 'Claude'), so the exact system cannot be re-run.",
}
NO_TOOLS = "The agents use no tools in these runs."

JUDGEMENTS: dict[str, dict[str, tuple[str, str]]] = {
    "system_prompts": {
        "AG2": ("partial", "MathChat runs log the instruction template sent as the first user turn ('Let's use Python to solve a math problem...'); MMLU group chats open with agents describing their roles; the agents' system messages are not logged."),
        "MetaGPT": ("absent", "The role definitions of SimpleCoder, SimpleTester and SimpleReviewer are not logged."),
        "ChatDev": ("present", "Every phase logs the role prompts and the phase prompt."),
        "Magentic": ("partial", "The orchestrator's first message restates the request, the team and an initial plan, which shows parts of its prompt templates; the agents' system prompts are not logged."),
        "OpenManus": ("absent", "No system or planning prompts are logged."),
        "AppWorld": ("absent", "The task, the agents' code and its outputs are logged; the agents' instructions are not."),
        "HyperAgent": ("absent", "Planner and intern prompts are not logged, only their responses."),
    },
    "user_prompts": {
        "AG2": ("present", "The problem is the first message of every run."),
        "MetaGPT": ("present", "Logged as the 'UserRequirement' message; in 4 traces it is empty, a harness defect (see data audit)."),
        "ChatDev": ("present", "Logged as 'task_prompt'; empty in 1 trace."),
        "Magentic": ("present", "Logged as the 'user' turn."),
        "OpenManus": ("partial", "29 of 30 logs print only the first ~50 characters of the task; in the remaining run the task was typed in interactively and never logged."),
        "AppWorld": ("present", "Logged under the task banner."),
        "HyperAgent": ("present", "The GitHub issue text is logged as the problem statement."),
    },
    "external_info": {
        "AG2": ("n/a", "No access to external sources; code output is computed locally."),
        "MetaGPT": ("n/a", "No access to external sources."),
        "ChatDev": ("n/a", "No access to external sources."),
        "Magentic": ("present", "Web pages (visible text and page titles) and file contents returned to the agents are logged."),
        "OpenManus": ("present", "Browser and search results returned to the agent are logged."),
        "AppWorld": ("present", "Data returned by the app APIs is logged in full."),
        "HyperAgent": ("present", "Repository file contents and code-search results are logged in the agents' observations."),
    },
    "scaffolding_logs": {
        "AG2": ("absent", "Only the list of messages is logged."),
        "MetaGPT": ("partial", "A log header and message-routing lines (sender, recipient, action class); nothing from inside the framework."),
        "ChatDev": ("present", "Timestamped INFO records for every phase, chat parameters, and a cost and duration summary."),
        "Magentic": ("partial", "Container set-up and package installation, scenario start, end and runtime; nothing from the orchestration code between turns."),
        "OpenManus": ("present", "Records from each component (flow, planner, agent, tools) with source locations, plus token counts."),
        "AppWorld": ("partial", "Message-loop entry and exit markers and the send_message API's returns."),
        "HyperAgent": ("partial", "Initialisation lines and agent-to-agent hand-offs."),
    },
    "reasoning": {
        "AG2": ("partial", "Reasoning appears only where the model writes it into its messages."),
        "MetaGPT": ("partial", "Reasoning appears only inside messages (mainly the reviewer's critiques)."),
        "ChatDev": ("partial", "Reasoning appears only inside the role-play messages."),
        "Magentic": ("partial", "The orchestrator writes a fact sheet and plan; other agents' reasoning appears only inside their messages."),
        "OpenManus": ("present", "A labelled 'thoughts' field precedes each tool selection."),
        "AppWorld": ("partial", "Reasoning appears only as comments in the agents' code."),
        "HyperAgent": ("present", "ReAct-style 'Thought:' sections precede actions."),
    },
    "responses": {fw: ("present", "Agent outputs and actions are the bulk of every log.") for fw in FRAMEWORKS},
    "log_metadata": {
        "AG2": ("absent", "No timestamps or identifiers, except the 30 GSM-Plus runs, which carry a benchmark instance id."),
        "MetaGPT": ("partial", "Timestamps on every message; no run identifier."),
        "ChatDev": ("present", "Timestamps on every record; the run start time and log file name identify the run. Location is not recorded (not meaningful for benchmark runs)."),
        "Magentic": ("absent", "No timestamps or identifiers; only the total runtime."),
        "OpenManus": ("present", "Timestamps on every record and plan identifiers. Location is not recorded."),
        "AppWorld": ("partial", "Task identifiers (e.g. 'Task 17/25 (cf6abd2_3)'); no timestamps (dates inside app data are content, not log metadata)."),
        "HyperAgent": ("partial", "The SWE-bench instance id; no timestamps."),
    },
    "configurations": {
        "AG2": ("absent", "No sampling parameters, seeds, model or framework versions."),
        "MetaGPT": ("absent", "No sampling parameters, seeds, model or framework versions."),
        "ChatDev": ("partial", "Sampling parameters (temperature 0.2, top_p 1.0) and a model enum are logged; no seed, model snapshot or framework version. The enum contradicts MAST's metadata in one group (see below)."),
        "Magentic": ("partial", "Scaffolding package versions (autogen 0.4.9) appear in the install log; no sampling parameters, seed or model version."),
        "OpenManus": ("absent", "Token counts only; no sampling parameters, seed or versions."),
        "AppWorld": ("absent", "No sampling parameters, seeds or versions."),
        "HyperAgent": ("absent", "No sampling parameters, seeds or versions."),
    },
    "tool_id": {
        "AG2": ("partial", "Code-execution results ('exitcode: 0') appear in about a quarter of traces, from a named executor agent in group chats; no versions."),
        "MetaGPT": ("n/a", NO_TOOLS),
        "ChatDev": ("partial", "The framework runs the generated program in a test phase; the executor is not identified or versioned."),
        "Magentic": ("partial", "Tool-using agents are named (WebSurfer, FileSurfer, ComputerTerminal) and scaffolding package versions are in the install log; the browser version is not logged."),
        "OpenManus": ("partial", "Tool names are logged ('Tools being prepared: [...]'); no versions."),
        "AppWorld": ("partial", "App and API names are visible in the agents' code (apis.<app>.<api>); no versions."),
        "HyperAgent": ("partial", "Tool names are visible in calls (e.g. get_all_symbols._run, open_file); no versions."),
    },
    "tool_actions": {
        "AG2": ("partial", "Group-chat runs (MMLU) open with agents describing what they can do; other runs list nothing."),
        "MetaGPT": ("n/a", NO_TOOLS),
        "ChatDev": ("n/a", NO_TOOLS),
        "Magentic": ("present", "The orchestrator's opening message lists each agent and what it can do."),
        "OpenManus": ("partial", "The tools used and their arguments are logged; the full set of enabled tools is not."),
        "AppWorld": ("present", "Agents request and log the lists of available apps and APIs."),
        "HyperAgent": ("partial", "Intern roles and the tools they call are visible; the full toolset is not listed."),
    },
    "tool_docs": {
        "AG2": ("absent", "No tool documentation is logged."),
        "MetaGPT": ("n/a", NO_TOOLS),
        "ChatDev": ("n/a", NO_TOOLS),
        "Magentic": ("partial", "Only incidental usage messages from tools (e.g. 'No code blocks found ... Please provide at least one markdown-encoded code block')."),
        "OpenManus": ("absent", "Tool documentation given to the agent is not logged."),
        "AppWorld": ("present", "API documentation that the agents request is logged in full."),
        "HyperAgent": ("absent", "Tool documentation given to the agents is not logged."),
    },
    "access_reqs": {
        "AG2": ("n/a", "Local code execution needs no credentials."),
        "MetaGPT": ("n/a", NO_TOOLS),
        "ChatDev": ("n/a", NO_TOOLS),
        "Magentic": ("absent", "How the agents were authorised to use the web and files is not logged."),
        "OpenManus": ("absent", "How the agent was authorised to use the browser and search tools is not logged."),
        "AppWorld": ("present", "Credentials are retrieved and used inside the trace (supervisor.show_account_passwords, logins)."),
        "HyperAgent": ("absent", "Repository and execution access is not described."),
    },
    "personalization": {
        "AG2": ("n/a", "Benchmark runs with no user profile or memory."),
        "MetaGPT": ("n/a", "Benchmark runs with no user profile or memory."),
        "ChatDev": ("partial", "The memory setting is logged ('with_memory: False'); there is no stored user data."),
        "Magentic": ("n/a", "Benchmark runs with no user profile or memory."),
        "OpenManus": ("n/a", "Benchmark runs with no user profile or memory."),
        "AppWorld": ("present", "The simulated user's profile, accounts and app data are read through APIs and logged."),
        "HyperAgent": ("n/a", "Benchmark runs with no user profile or memory."),
    },
    "tool_state": {
        "AG2": ("absent", "Only the output of each execution."),
        "MetaGPT": ("n/a", NO_TOOLS),
        "ChatDev": ("partial", "Test-phase reports show whether the program ran; no wider environment state."),
        "Magentic": ("present", "The web agent reports the current URL, page title and how much of the page is in view."),
        "OpenManus": ("partial", "Navigation results ('Navigated to ...') in about half the runs; little other state."),
        "AppWorld": ("partial", "App state is visible only through the API outputs the agents request."),
        "HyperAgent": ("partial", "File paths and line ranges in observations; no summary of repository or environment state."),
    },
    "tool_errors": {
        "AG2": ("present", "Failed code executions are logged with their error: tracebacks returned by the MathChat proxy ('Error: Traceback ...') and exit codes in group chats."),
        "MetaGPT": ("n/a", NO_TOOLS),
        "ChatDev": ("present", "Test-phase failures are logged with tracebacks."),
        "Magentic": ("present", "Terminal errors and failed web actions are logged."),
        "OpenManus": ("present", "Tool failures and the agent's 'stuck state' handling are logged."),
        "AppWorld": ("present", "Execution errors and tracebacks from the agents' code are logged."),
        "HyperAgent": ("present", "Errors from code execution and failed tool calls appear in the observations."),
    },
}
for key, reason in ALL_ABSENT.items():
    JUDGEMENTS[key] = {fw: ("absent", reason) for fw in FRAMEWORKS}

# What MAST's own metadata provides, outside the logs.
MAST_METADATA = {
    "provides": ["framework name (mas_name)", "model name without version (llm_name: 'GPT-4o', 'GPT-4o-mini', 'Claude', 'Qwen', 'CodeLlama')",
                 "benchmark name (benchmark_name; wrong for OpenManus and imprecise for AG2 GSM-Plus)",
                 "an index within each group (trace_id; not unique across groups)", "14 MAST failure-mode labels from an LLM judge"],
    "missing": ["model versions or snapshot dates", "run timestamps or unique run identifiers", "sampling parameters and seeds",
                "framework versions", "task outcome (success or failure on the benchmark)", "system prompts or agent configurations"],
}


# ---------------------------------------------------------------------------


def sampled(traces: list[dict]) -> list[str]:
    """The three traces read for manual judgements: first, middle and last by id."""
    ids = sorted(t["uid"] for t in traces)
    return [ids[0], ids[len(ids) // 2], ids[-1]]


def model_identity(traces: list[dict], raw: dict[str, str]) -> dict[str, dict[str, int]]:
    """Model identifiers that appear inside the logs, by MAST group, next to MAST's own model name."""
    out: dict[str, Counter] = defaultdict(Counter)
    for t in traces:
        for m in set(re.findall(r"ModelType\.\w+", raw[t["uid"]])):
            out[f"{t['source_key']} (MAST: {t['model']})"][m] += 1
    return {k: dict(v) for k, v in sorted(out.items())}


def run_audit(traces: list[dict], raw: dict[str, str]) -> dict:
    by_fw = defaultdict(list)
    for t in traces:
        by_fw[t["framework"]].append(t)
    result = {"source": SOURCE, "frameworks": {}, "mismatches": []}
    for fw in FRAMEWORKS:
        ts = by_fw[fw]
        entry = {"n_traces": len(ts), "sampled_traces": sampled(ts), "items": {}}
        for key, _, _ in ITEMS:
            status, reason = JUDGEMENTS[key][fw]
            share = None
            if key in DETECTORS and status != "n/a":
                share = round(sum(DETECTORS[key][1](t, raw[t["uid"]]) for t in ts) / len(ts), 3)
            cell = {"status": status, "detector_share": share, "reason": reason,
                    "basis": "detector + judgement" if share is not None else f"manual: read {', '.join(entry['sampled_traces'])}"}
            if key in ("log_metadata", "configurations"):
                subs = ("line_timestamps", "run_identifiers") if key == "log_metadata" else ("sampling_params", "model_identifier", "scaffold_versions", "seed")
                cell["sub_shares"] = {s: round(sum(SUB[s][1](t, raw[t["uid"]]) for t in ts) / len(ts), 3) for s in subs}
            entry["items"][key] = cell
            # Flag judgements that the detector contradicts, so they get a second look.
            # Error logging is an event, not a fixed feature: a low share means few errors happened,
            # so for that item only a share of zero questions a "present" judgement.
            if share is not None:
                too_low = share == 0 if key == "tool_errors" else share < 0.50
                if (status == "absent" and share > 0.10) or (status == "present" and too_low):
                    result["mismatches"].append(f"{fw} / {NAME[key]}: status {status} but detector share {share:.0%}")
        result["frameworks"][fw] = entry
    result["summary"] = {key: dict(Counter(result["frameworks"][fw]["items"][key]["status"] for fw in FRAMEWORKS)) for key, _, _ in ITEMS}
    result["model_identity_in_logs"] = model_identity(traces, raw)
    om = by_fw["OpenManus"]
    result["openmanus_logged_events"] = {
        "runs": len(om),
        "harness_timeout_after_1h": sum(bool(re.search(r"Request processing timed out after 1 hour", raw[t["uid"]])) for t in om),
        "model_api_errors": sum(bool(re.search(r"\| ERROR\s*\| app\.llm:\w+:\d+ - .*API error", raw[t["uid"]])) for t in om),
        "stuck_state_detected": sum(bool(re.search(r"Agent detected stuck state", raw[t["uid"]])) for t in om),
    }
    result["mast_metadata"] = MAST_METADATA
    return result


SYMBOL = {"present": "●", "partial": "◐", "absent": "○", "n/a": "–"}


def shown_share(cell: dict) -> float | None:
    """The detector share worth showing next to a status, or None.

    A partial judgement with a zero share rests on reading the traces (the detector
    only looks for the full form of the item), so a bare 0% there would mislead.
    """
    share = cell["detector_share"]
    if share is None or (cell["status"] == "partial" and share == 0):
        return None
    return share


def write_markdown(audit: dict, path) -> None:
    fws = FRAMEWORKS
    n = {fw: audit["frameworks"][fw]["n_traces"] for fw in fws}
    lines = [
        "# Information audit: what the MAST traces let an investigator see",
        "",
        "Generated by `uv run afacs-info-audit`. Do not edit by hand.",
        "",
        "**Question (RQ2).** Ezell, Roberts-Gaal & Chan (2025) list 18 kinds of information that incident "
        "investigators need to identify why an AI agent failed, and to reconstruct the failure (their Table 1). "
        "Do real multi-agent traces, as published in MAST, contain them?",
        "",
        "**Method.** For each framework and each item we record a status: ● present, ◐ partial, ○ absent, or – "
        "not applicable to these benchmark runs (for example, tool information for agents that use no tools). "
        "Where a reliable automatic detector exists, the table also gives the share of the framework's traces in "
        "which it fires; the status is a judgement informed by that share. Items without a reliable detector were "
        "judged by reading three sampled traces per framework (first, middle and last by id), listed at the end. "
        "Items marked * matter mainly for reconstruction. Only traces that pass the data-quality checks are used.",
        "",
        "| Item | " + " | ".join(f"{fw} (n={n[fw]})" for fw in fws) + " |",
        "|---|" + "---|" * len(fws),
    ]
    category = None
    for key, cat, name in ITEMS:
        if cat != category:
            lines.append(f"| **{cat}** |" + " |" * len(fws))
            category = cat
        cells = []
        for fw in fws:
            c = audit["frameworks"][fw]["items"][key]
            share = f" {shown_share(c):.0%}" if shown_share(c) is not None else ""
            cells.append(f"{SYMBOL[c['status']]}{share}")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    s = audit["summary"]
    def count(key, st):
        return s[key].get(st, 0)
    always_absent = [NAME[k] for k, _, _ in ITEMS if count(k, "absent") == len(fws)]
    mostly_missing = [NAME[k] for k, _, _ in ITEMS if count(k, "present") == 0 and NAME[k] not in always_absent
                      and count(k, "n/a") < len(fws)]
    consistent = [NAME[k] for k, _, _ in ITEMS if count(k, "present") >= 6]
    lines += [
        "",
        "Percentages are detector shares (share of the framework's traces in which the automatic check fires). "
        "No percentage means the status rests on reading the sampled traces.",
        "",
        "## Findings",
        "",
        f"- **Present almost everywhere:** {', '.join(consistent) or 'none'}. The logs are good records of what the agents said and did.",
        f"- **Absent in every framework:** {', '.join(always_absent)}. Nothing in MAST lets an investigator identify, or re-run, the exact system that failed.",
        f"- **Never fully present:** {', '.join(mostly_missing)}. Each is at best partial, and only in some frameworks.",
        "- **Logging depends on the framework, not on the failure.** ChatDev and OpenManus log far more about their own "
        "workings than AG2 or MetaGPT. What an investigator can establish therefore varies with the software that "
        "happened to produce the trace.",
        "- **Hidden reasoning is never logged.** Where reasoning is visible at all, it is what the model chose to write "
        "into its output (OpenManus 'thoughts', HyperAgent 'Thought:'), which Ezell et al. note may not reflect the "
        "model's actual reasoning.",
        "",
        "### Failures the logs record outside the agents",
        "",
        f"OpenManus's logs record events that no agent message would show: the harness timing out after one hour "
        f"({audit['openmanus_logged_events']['harness_timeout_after_1h']} of {audit['openmanus_logged_events']['runs']} runs), "
        f"errors from the model provider's API ({audit['openmanus_logged_events']['model_api_errors']} runs) and the "
        f"framework detecting a stuck agent ({audit['openmanus_logged_events']['stuck_state_detected']} runs). These are "
        "candidate causes above the agent (resource limits, environment), visible only because this framework logs its own components.",
        "",
        "### Model identity inside the logs",
        "",
        "Only ChatDev logs a model identifier. Set against MAST's own model name:",
        "",
        "| MAST group | Model identifier in the log | Traces |",
        "|---|---|---|",
    ]
    for group, ids in audit["model_identity_in_logs"].items():
        for mid, k in ids.items():
            lines.append(f"| {group} | `{mid}` | {k} |")
    lines += [
        "",
        "One group that MAST labels GPT-4o logs a different model enum, so either the metadata or the log is wrong; "
        "another group's log is more specific than MAST's label. Without logged model identifiers, such discrepancies "
        "cannot be detected in the other six frameworks.",
        "",
        "### What MAST's metadata adds outside the logs",
        "",
        "It provides: " + "; ".join(audit["mast_metadata"]["provides"]) + ".",
        "",
        "It does not provide: " + "; ".join(audit["mast_metadata"]["missing"]) + ".",
        "",
        "## Implications for reconstruction and analysis",
        "",
        "- **No incident in this dataset can be re-run exactly.** Model versions are unknown, sampling settings and "
        "seeds are logged only in ChatDev (and seeds nowhere), and no system artifacts are available.",
        "- **The task itself is not always recoverable.** OpenManus logs print only the start of the task (29 of 30) "
        "or omit it (1 of 30), and 5 traces across MetaGPT and ChatDev have an empty task (see `docs/data_audit.md`).",
        "- **Duplicated and mislabelled logs** (data audit) mean that even the link between a log and its metadata "
        "cannot be taken for granted.",
        "- **Supervision and coordination are visible; their configuration is not.** Agent-to-agent messages are well "
        "logged, so a coder can see an orchestrator fail to correct an error, but without system prompts or role "
        "definitions it is often impossible to tell whether the orchestrator was ever instructed to check.",
        "",
        "## Reasons for each judgement",
        "",
    ]
    for key, cat, name in ITEMS:
        lines.append(f"**{name}**")
        lines.append("")
        for fw in fws:
            c = audit["frameworks"][fw]["items"][key]
            extra = ""
            if "sub_shares" in c:
                extra = " (" + ", ".join(f"{SUB[k][0]}: {v:.0%}" for k, v in c["sub_shares"].items()) + ")"
            lines.append(f"- {fw}: {SYMBOL[c['status']]} {c['status']}. {c['reason']}{extra}")
        lines.append("")
    lines += ["## Sampled traces read for the manual judgements", ""]
    for fw in fws:
        lines.append(f"- {fw}: " + ", ".join(f"`{u}`" for u in audit["frameworks"][fw]["sampled_traces"]))
    lines += ["", "## Automatic detectors", ""]
    for key, (desc, _) in DETECTORS.items():
        lines.append(f"- {NAME[key]}: {desc}.")
    lines += ["", f"Source of the checklist: {SOURCE}", ""]
    path.write_text("\n".join(lines))


def draw_figure(audit: dict, path) -> None:
    fws = FRAMEWORKS
    level = {"absent": 0, "partial": 1, "present": 2}
    cmap = ListedColormap([BLUE_RAMP[0], BLUE_RAMP[2], BLUE_RAMP[5]])
    rows = [name for _, _, name in ITEMS]
    data = [[level.get(audit["frameworks"][fw]["items"][k]["status"], float("nan")) for fw in fws] for k, _, _ in ITEMS]
    fig, ax = plt.subplots(figsize=(9.6, 8.4))
    ax.imshow(data, cmap=cmap, vmin=0, vmax=2, aspect="auto")
    for i, (key, _, _) in enumerate(ITEMS):
        for j, fw in enumerate(fws):
            c = audit["frameworks"][fw]["items"][key]
            if c["status"] == "n/a":
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=SURFACE, edgecolor=GRID, hatch="///", linewidth=0))
                ax.text(j, i, "n/a", ha="center", va="center", fontsize=7.5, color=INK_2)
                continue
            label = f"{shown_share(c):.0%}" if shown_share(c) is not None else "M"
            ax.text(j, i, label, ha="center", va="center", fontsize=8,
                    color="white" if c["status"] == "present" else INK, fontweight="bold" if label == "M" else "normal")
    ax.set_xticks(range(len(fws)), [f"{fw}\nn={audit['frameworks'][fw]['n_traces']}" for fw in fws])
    ax.set_yticks(range(len(rows)), rows, fontsize=8.5)
    ax.set_xticks([x - 0.5 for x in range(1, len(fws))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=2)
    for y in (6.5, 10.5):  # separate the three categories
        ax.axhline(y, color=INK_2, linewidth=1.2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    handles = [plt.Rectangle((0, 0), 1, 1, color=BLUE_RAMP[5]), plt.Rectangle((0, 0), 1, 1, color=BLUE_RAMP[2]),
               plt.Rectangle((0, 0), 1, 1, color=BLUE_RAMP[0]),
               plt.Rectangle((0, 0), 1, 1, facecolor=SURFACE, edgecolor=GRID, hatch="///")]
    ax.legend(handles, ["present", "partial", "absent", "not applicable"], loc="upper center", bbox_to_anchor=(0.5, -0.07),
              ncol=4, frameon=False, fontsize=8.5)
    fig.suptitle("What the MAST traces record, against Ezell et al.'s 18 information needs", x=0.01, ha="left",
                 fontweight="bold", fontsize=11)
    fig.text(0.01, 0.945, "Colour: status. Number: share of traces where the automatic check fires. M: judged by reading sampled traces.",
             fontsize=8, color=INK_2)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(path, dpi=200)
    fig.savefig(path.with_suffix(".pdf"))  # vector copy for the paper
    plt.close(fig)


def main() -> None:
    traces = [t for t in load_traces() if t["quality_exclusion"] is None]
    with open(paths.RAW / "MAD_full_dataset.json") as f:
        raw = {f'{r["trace"]["key"]}__{r["trace"]["index"]:03d}': r["trace"]["trajectory"] for r in json.load(f)}
    audit = run_audit(traces, raw)
    paths.PROCESSED.mkdir(parents=True, exist_ok=True)
    (paths.PROCESSED / "info_audit.json").write_text(json.dumps(audit, indent=2))
    write_markdown(audit, paths.DOCS / "information_audit.md")
    paths.FIGURES.mkdir(exist_ok=True)
    draw_figure(audit, paths.FIGURES / "info_audit.png")
    print("wrote data/processed/info_audit.json, docs/information_audit.md, figures/info_audit.png")
    if audit["mismatches"]:
        print("Judgements the detectors question (check these):")
        for m in audit["mismatches"]:
            print("  " + m)
    else:
        print("No judgement contradicts its detector.")


if __name__ == "__main__":
    main()
