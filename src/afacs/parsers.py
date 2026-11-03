"""Split each framework's raw log into numbered steps.

MAST stores every trace as one long string, and each of the seven frameworks
writes its log in a different format. This module has one small parser per
format. Each parser returns a list of `Step`s: who spoke, what kind of step it
was, and the text.

Design rules:
- Keep the agents' text verbatim. We only cut the log *around* it (timestamps,
  separators) and drop a few kinds of pure noise that carry no behavioural
  information (package-install logs, token-usage counters, a ChatDev web-server
  warning repeated hundreds of times). Every dropped character is counted in
  `ParsedTrace.dropped_chars`, so the ingest audit can show nothing else went
  missing.
- Anything the agents never saw (benchmark answers, gold patches, post-hoc
  evaluation) is kept but marked `kind="benchmark_info"`, so the renderer can
  flag it clearly to the coder.
"""

from __future__ import annotations

import ast
import re
import textwrap
from dataclasses import dataclass, field

# Step kinds
MESSAGE = "message"  # an agent's own output (reasoning, plan, code, answer)
TOOL_OUTPUT = "tool_output"  # what the environment returned (code execution, terminal)
SYSTEM = "system"  # framework/harness bookkeeping (initialisation, loop entry/exit)
BENCHMARK_INFO = "benchmark_info"  # metadata or evaluation the agents never saw

# An agent turn with no text is evidence (e.g. a coder that produced nothing), so
# we keep it as a step with this placeholder instead of dropping it.
EMPTY_TURN = "(empty message: the agent produced no text in this turn)"


def _or_empty(text: str) -> str:
    return text if text.strip() else EMPTY_TURN


@dataclass
class Step:
    agent: str
    text: str
    kind: str = MESSAGE


@dataclass
class ParsedTrace:
    parser: str
    steps: list[Step] = field(default_factory=list)
    dropped_chars: int = 0  # characters deliberately removed as noise
    notes: list[str] = field(default_factory=list)

    def add(self, agent: str, text: str, kind: str = MESSAGE) -> None:
        """Append a step, skipping empty ones."""
        text = text.strip("\n")
        if text.strip():
            self.steps.append(Step(agent=agent.strip(), text=text, kind=kind))


# --------------------------------------------------------------------------
# AG2 (AutoGen), main format: a run of Python dict reprs separated by spaces,
# e.g. {'content': [...], 'role': 'user', 'name': 'Agent_Problem_Solver'} {...}
# --------------------------------------------------------------------------


def _split_top_level_dicts(text: str) -> list[str]:
    """Return each top-level {...} chunk, ignoring braces inside quoted strings."""
    chunks, depth, start = [], 0, None
    in_string, quote, i = False, "", 0
    while i < len(text):
        ch = text[i]
        if in_string:
            if ch == "\\":
                i += 2  # skip the escaped character
                continue
            if ch == quote:
                in_string = False
        elif ch in ("'", '"'):
            in_string, quote = True, ch
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                chunks.append(text[start : i + 1])
                start = None
        i += 1
    return chunks


def parse_ag2_dicts(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="ag2_dicts")
    for chunk in _split_top_level_dicts(raw):
        try:
            msg = ast.literal_eval(chunk)
        except (ValueError, SyntaxError):
            out.notes.append("unparseable message chunk kept as raw text")
            out.add("unknown", chunk, SYSTEM)
            continue
        content = msg.get("content")
        if isinstance(content, list):
            text = "\n".join(str(x) for x in content)
        else:
            text = "" if content is None else str(content)
        extras = {k: v for k, v in msg.items() if k not in ("content", "role", "name")}
        for k, v in extras.items():
            text += f"\n[{k}]: {v}"
        kind = TOOL_OUTPUT if text.lstrip().startswith("exitcode:") else MESSAGE
        out.add(str(msg.get("name", msg.get("role", "unknown"))), _or_empty(text), kind)
    return out


# --------------------------------------------------------------------------
# AG2 MathChat on GSM-Plus: a YAML-like dump with the benchmark record first
# (instance_id / problem_statement / other_data) and then `trajectory:` with
# content/role/name entries.
# --------------------------------------------------------------------------


def _split_yaml_header(raw: str) -> tuple[str, str]:
    """Split 'instance_id ... other_data ...' header from the 'trajectory:' body."""
    idx = raw.find("\ntrajectory:\n")
    if idx == -1:
        return raw, ""
    return raw[:idx], raw[idx + len("\ntrajectory:\n") :]


def _header_fields(header: str) -> tuple[str, str]:
    """Return (problem statement, everything else) from a YAML-like benchmark header."""
    m = re.search(r"^problem_statement:(.*?)(?=^other_data:|\Z)", header, re.S | re.M)
    problem = textwrap.dedent(m.group(1)).strip() if m else ""
    rest = header[: m.start()] + header[m.end() :] if m else header
    return problem, rest.strip()


def parse_ag2_mathchat(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="ag2_mathchat_yaml")
    header, body = _split_yaml_header(raw)
    out.add("benchmark", "Benchmark record (agents saw only the problem statement, via the first message):\n\n" + header, BENCHMARK_INFO)
    for entry in re.split(r"(?m)^      content:", body)[1:]:
        m = re.search(r"(?s)^(.*?)\n      role: (.*?)\n      name: (.*?)(?:\n|$)", entry)
        if not m:
            out.add("unknown", entry, SYSTEM)
            continue
        text = textwrap.dedent(m.group(1)).strip()
        out.add(m.group(3), _or_empty(text), MESSAGE)
    return out


# --------------------------------------------------------------------------
# MetaGPT: blocks separated by a line of 80 dashes. A block is either the task
# ("FROM: Human ... CONTENT:") or "NEW MESSAGES:" followed by "Role: text".
# --------------------------------------------------------------------------

METAGPT_ROLES = ("SimpleCoder", "SimpleTester", "SimpleReviewer")


def parse_metagpt(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="metagpt")
    role_re = re.compile(rf"^({'|'.join(METAGPT_ROLES)}): ?", re.M)
    for block in re.split(r"\n-{80}\n", raw):
        block = block.strip("\n")
        task = re.search(r"FROM: (.*?) TO: .*?\nACTION: .*?\nCONTENT:\n?(.*)", block, re.S)
        if task:
            before = block[: task.start()]
            before = re.sub(r"\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\]\s*$", "", before)
            out.add("system", before, SYSTEM)
            text = task.group(2)
            if not text.strip():
                text = "[The task requirement in this trace is EMPTY: the harness passed no task text.]"
                out.notes.append("empty task requirement")
            out.add(task.group(1), text)
            continue
        if "NEW MESSAGES:" in block:
            body = block.split("NEW MESSAGES:", 1)[1]
            parts = role_re.split(body)
            # parts = [preamble, role1, text1, role2, text2, ...]
            out.add("system", parts[0], SYSTEM)
            for role, text in zip(parts[1::2], parts[2::2]):
                out.add(role, _or_empty(text))
            continue
        out.add("system", block, SYSTEM)
    return out


# --------------------------------------------------------------------------
# Magentic-One: a Docker/pip install log, then "SCENARIO.PY STARTING !#!#",
# then turns introduced by "---------- AgentName ----------".
# --------------------------------------------------------------------------


def parse_magentic(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="magentic")
    marker = "SCENARIO.PY STARTING !#!#"
    idx = raw.find(marker)
    if idx != -1:
        out.dropped_chars += idx + len(marker)
        out.notes.append(f"dropped {idx + len(marker)} chars of install log before the run started")
        raw = raw[idx + len(marker) :]
    parts = re.split(r"\n?-{10} (.+?) -{10}\n", raw)
    out.add("system", parts[0], SYSTEM)
    for agent, text in zip(parts[1::2], parts[2::2]):
        # The run's closing harness lines get appended to the last turn; split them off.
        tail = re.search(r"\n?SCENARIO\.PY COMPLETE !#!#.*\Z", text, re.S)
        if tail:
            text, tail_text = text[: tail.start()], tail.group(0)
        else:
            tail_text = ""
        kind = TOOL_OUTPUT if agent == "ComputerTerminal" else MESSAGE
        out.add(agent, _or_empty(text), kind)
        out.add("system", tail_text, SYSTEM)
    return out


# --------------------------------------------------------------------------
# OpenManus: a loguru log. Records look like
#   2025-03-31 21:52:44.052 | INFO     | app.agent.toolcall:think:81 - message
# We group records into one step per agent step ("Executing step N/20") so a
# step reads as: thoughts -> tool choice -> tool result.
# --------------------------------------------------------------------------

OPENMANUS_TRUNCATION_NOTE = (
    "[Note added by AFACS, not part of the log: this log prints only the first ~50 characters "
    "of the task. The agents received the full task text (their plans refer to details not shown "
    "here). The truncation is an artefact of the logging, not of what the agents were given.]"
)

OPENMANUS_RECORD = re.compile(
    r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+ \| (?P<level>\w+)\s*\| (?P<source>[\w.]+):(?P<func>\w+):\d+ - ",
    re.M,
)


def parse_openmanus(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="openmanus")
    starts = list(OPENMANUS_RECORD.finditer(raw))
    if not starts:
        out.add("system", raw, SYSTEM)
        return out
    out.add("system", raw[: starts[0].start()], SYSTEM)

    current_agent, current_lines = None, []

    def flush():
        if current_agent is not None:
            # The planner's plans are written by the LLM, so they count as agent output.
            out.add(current_agent, "\n".join(current_lines), SYSTEM if current_agent == "system" else MESSAGE)
        if current_agent == "system" and any(l.startswith("Read prompt from task.txt:") and l.endswith("...") for l in current_lines):
            out.notes.append("task text truncated in log")
            out.add("note", OPENMANUS_TRUNCATION_NOTE, SYSTEM)

    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(raw)
        message = raw[m.end() : end].rstrip("\n")
        source, func = m.group("source"), m.group("func")
        if source == "app.llm" and func == "update_token_count":
            out.dropped_chars += end - m.start()
            continue
        if source == "app.agent.base" and func == "run" and message.startswith("Executing step"):
            flush()
            current_agent, current_lines = "Manus", [f"[{message}]"]
            continue
        if source.startswith("app.agent") or source.startswith("app.tool") or source == "app.llm":
            if current_agent != "Manus":
                flush()
                current_agent, current_lines = "Manus", []
            current_lines.append(message)
            continue
        # Planning flow and the top-level runner become their own steps.
        flush()
        current_agent = "planner" if source.startswith("app.flow") else "system"
        current_lines = [message]
    flush()
    return out


# --------------------------------------------------------------------------
# AppWorld: a task banner, then blocks introduced by header lines such as
# "Response from Supervisor Agent", "Code Execution Output", and (indented by
# 4 spaces) nested sub-agent conversations. Ends with the benchmark's own
# "Evaluation" JSON, which the agents never saw.
# --------------------------------------------------------------------------

APPWORLD_HEADER = re.compile(
    r"^(?P<indent> {0}| {4})(?P<header>Response from .+|Reply from .+ to .+|Message to .+|"
    r"Code Execution Output|Evaluation|Entering .+ message loop|Exiting .+ message loop)[ \t]*$",
    re.M,
)


def parse_appworld(raw: str) -> ParsedTrace:
    """AppWorld: the Supervisor agent writes code; `send_message` hands a request to an
    app sub-agent (Spotify, phone, ...), which runs its own loop:

        Entering phone Agent message loop
            Message to phone Agent        <- first one: the Supervisor's request
            Response from phone Agent     <- the sub-agent's code
            Message to phone Agent        <- later ones: that code's execution output
            Reply from phone Agent to Supervisor
        Exiting phone Agent message loop
        Response from send_message API    <- the reply, as returned to the Supervisor
        Message to Supervisor Agent       <- the same text again, as delivered

    We label each block by what it is, and collapse word-for-word repeats of the
    previous step into a pointer, so the coder doesn't read the same output twice.
    """
    out = ParsedTrace(parser="appworld")
    heads = list(APPWORLD_HEADER.finditer(raw))
    preamble = raw[: heads[0].start()] if heads else raw
    preamble = re.sub(r"\*{10,}[^\n]*\*{10,}", "", preamble)  # task banner
    out.add("user", textwrap.dedent(preamble).strip())
    in_loop, messages_in_loop = False, 0
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(raw)
        header = m.group("header").strip()
        body = textwrap.dedent(raw[m.end() : end]).strip("\n")
        if out.steps and body.strip() and body.strip() == out.steps[-1].text.strip():
            body = f"(identical to the previous step [S{len(out.steps)}], passed on unchanged)"
        if header == "Evaluation":
            out.add("AppWorld evaluation", body, BENCHMARK_INFO)
        elif header.startswith(("Entering", "Exiting")):
            in_loop, messages_in_loop = header.startswith("Entering"), 0
            out.add("system", header + ("\n" + body if body.strip() else ""), SYSTEM)
        elif header == "Code Execution Output" or header.startswith("Response from send_message API"):
            out.add(header, body, TOOL_OUTPUT)
        elif header.startswith("Message to"):
            if in_loop and messages_in_loop == 0:
                out.add(f"{header} (request from the Supervisor)", body or "(empty)")
            else:
                out.add(f"{header} (code execution output)" if in_loop else header, body or "(empty)", TOOL_OUTPUT)
            if in_loop:
                messages_in_loop += 1
        else:
            out.add(header, body if body.strip() else "(empty)")
    return out


# --------------------------------------------------------------------------
# HyperAgent (SWE-bench Lite): a YAML-like benchmark record (issue text plus
# other_data, which includes the gold patch), then `trajectory:` with lines
#   HyperAgent_<instance> - INFO - Planner's Response: ...
# --------------------------------------------------------------------------

HYPERAGENT_RECORD = re.compile(r"^  HyperAgent_\S+ - (?P<level>\w+) - ", re.M)


def _hyperagent_speaker(message: str) -> tuple[str, str, str]:
    """Return (agent, text, kind) for one HyperAgent log message.

    "Planner's Response: ..."                  -> Planner
    "Inner-Navigator-Assistant's Response: ..." -> Navigator
    "Navigator->Planner: ..."                  -> Navigator -> Planner (a hand-back)
    anything else ("Initialized tools")        -> system
    """
    m = re.match(r"^(?P<who>[\w\-]+(?:->[\w\-]+)?)(?P<resp>'s Response)?: ", message)
    if m and (m.group("resp") or "->" in m.group("who")):
        who = m.group("who").replace("Inner-", "").replace("-Assistant", "").replace("->", " -> ")
        return who, message[m.end() :], MESSAGE
    return "system", message, SYSTEM


def parse_hyperagent(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="hyperagent")
    header, body = _split_yaml_header(raw)
    problem, meta = _header_fields(header)
    out.add("user (GitHub issue)", problem)
    out.add("benchmark", "SWE-bench record (not shown to the agents; may include the gold patch):\n\n" + meta, BENCHMARK_INFO)
    starts = list(HYPERAGENT_RECORD.finditer(body))
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        message = textwrap.dedent("  " + body[m.end() : end]).strip("\n")
        agent, text, kind = _hyperagent_speaker(message)
        out.add(agent, _or_empty(text) if kind == MESSAGE else text, kind)
    return out


# --------------------------------------------------------------------------
# ChatDev: records start with "[YYYY-DD-MM HH:MM:SS INFO] ". Very long; excluded
# from the study, but parsed so the ingest audit can report on it.
# --------------------------------------------------------------------------

CHATDEV_RECORD = re.compile(r"^\[\d{4}-\d\d-\d\d \d\d:\d\d:\d\d INFO\] ", re.M)
CHATDEV_NOISE = ("flask app.py did not start for online log", "HTTP Request: POST", "**[OpenAI_Usage_Info Receive]**")


def parse_chatdev(raw: str) -> ParsedTrace:
    out = ParsedTrace(parser="chatdev")
    if re.search(r"\*\*task_prompt\*\*: *\n", raw):
        out.notes.append("empty task requirement")
    starts = list(CHATDEV_RECORD.finditer(raw))
    if not starts:
        out.add("system", raw, SYSTEM)
        return out
    out.add("system", raw[: starts[0].start()], SYSTEM)
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(raw)
        message = raw[m.end() : end]
        if message.startswith(CHATDEV_NOISE):
            out.dropped_chars += end - m.start()
            continue
        who = re.match(r"^([A-Z][\w ]{2,40}?): ", message)
        if who and who.group(1) != "System":
            out.add(who.group(1), message[who.end() :])
        else:
            out.add("system", message, SYSTEM)
    return out


# --------------------------------------------------------------------------
# Dispatcher
# --------------------------------------------------------------------------


def parse_trace(framework: str, raw: str) -> ParsedTrace:
    """Pick the right parser for a framework (and, for AG2, sniff which format)."""
    if framework == "AG2":
        if raw.lstrip().startswith("instance_id:"):
            return parse_ag2_mathchat(raw)
        return parse_ag2_dicts(raw)
    parsers = {
        "MetaGPT": parse_metagpt,
        "Magentic": parse_magentic,
        "OpenManus": parse_openmanus,
        "AppWorld": parse_appworld,
        "HyperAgent": parse_hyperagent,
        "ChatDev": parse_chatdev,
    }
    if framework not in parsers:
        raise ValueError(f"No parser for framework {framework!r}")
    return parsers[framework](raw)
