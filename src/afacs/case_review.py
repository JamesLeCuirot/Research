"""Build the Case Review page: four AI codings for James to review against their traces.

    uv run python -m afacs.case_review        # writes data/case_review.html (not committed: it holds traces)

Each case shows the trace (benchmark records included: this is a review after
the fact, not blind coding), the AI's coding from all three pilot runs, MAST's
labels, what the documentation check found where relevant, and a short review
form. Reviews are saved in the page's private database (collection
"reviews"), which Claude reads back with the ArtifactData tool.
"""

from __future__ import annotations

import json
import re

from afacs import design, paths
from afacs.ingest import load_traces
from afacs.schema import load_codebook_codes

RUNS = [("sonnet_bulk_r1", "Sonnet, run 1"), ("opus_bulk_r1", "Opus"), ("sonnet_bulk_r2", "Sonnet, run 2")]
TEMPLATE = paths.ROOT / "src/afacs/templates/case_review.html"
OUTPUT = paths.ROOT / "data/case_review.html"

CASES = [
    {
        "id": "K1",
        "uid": "MetaGPT_ProgramDev-v2_Qwen__043",
        "title": "A failure traced to the design",
        "question": ("All three AI runs trace this failure to the design: nothing in the system runs or checks the "
                     "code (L4.1). Does the trace support placing the deepest cause in the design, rather than "
                     "only in what the agents did?"),
        "how": [
            "Three agents take turns: SimpleCoder writes the code, SimpleTester writes test cases for it, and "
            "SimpleReviewer comments on the tests. Then the tester and reviewer go round once more.",
            "None of them can run code. Everything is text, so a 'test' here is only written, never executed.",
            "The run always stops after this fixed sequence of turns.",
        ],
        "design": ("Documentation check: confirmed. MAST ran MetaGPT's three-role example, in which no agent runs "
                   "the code and the coder never revises it; the reviewer comments only on the tests "
                   "(docs/design_check.md)."),
    },
    {
        "id": "K2",
        "uid": "AG2_Olympiad_GPT4o__150",
        "title": "A violation, or an honest error?",
        "question": ("All three AI runs code a violation with 'inferred' evidence. In the AI's reading, the "
                     "assistant presents 'verification' code that only returns an answer fixed in advance. Is that "
                     "right, and if so, is it a departure from a requirement the agent had registered, or could it "
                     "be an honest error?"),
        "how": [
            "The assistant is an AI model solving a maths competition problem. It may write Python code.",
            "The mathproxyagent is not an AI. It runs any code it receives and sends back the output, or a fixed "
            "message ('Continue...') when there is no code.",
            "The chat ends when an answer appears inside \\boxed{...}. Nothing checks that the answer is right.",
            "The opening message (step 1) sets the rules the assistant was given.",
        ],
        "design": ("Documentation check: the proxy only runs code and sends fixed replies, so there is no "
                   "verifier (confirmed). It does detect repeated identical results."),
    },
    {
        "id": "K3",
        "uid": "AppWorld_Test-C_GPT-4o__000",
        "title": "Flagged by MAST, passed by the benchmark",
        "question": ("MAST's judge flagged a failure mode in this trace. The benchmark's own check (the last step) "
                     "says the task passed, and all three AI runs, which could not see that check, found no failure. "
                     "Was there a failure? What does this case say about using flat failure labels as the record "
                     "of what went wrong?"),
        "how": [
            "A Supervisor agent holds the user's accounts and passwords. It talks to app agents (for example a "
            "Spotify agent) with send_message.",
            "Each app agent writes Python calls to its app (apis.spotify..., apis.phone...) and replies with reply(...).",
            "'framework log' steps are bookkeeping. The last step, marked as not visible to the agents, is the "
            "benchmark's own pass/fail check.",
            "The trace is long but each step is short; you can skim the code and focus on what the agents say.",
        ],
        "design": "This multi-agent set-up was built by MAST's authors from AppWorld's single-agent baseline.",
    },
    {
        "id": "K4",
        "uid": "Magentic_One_GPT4o__029",
        "title": "A missing tool, or a team that didn't use the one it had?",
        "question": ("All three AI runs code a missing tool (L4.2): the agent asked to read an image says it cannot "
                     "interpret images. The documentation shows that another agent, the WebSurfer, works from "
                     "screenshots and could have been sent the image, but never was. Is this a design gap, a "
                     "supervision or coordination failure, or both?"),
        "how": [
            "An Orchestrator plans the work and directs four agents. WebSurfer controls a web browser and sees "
            "screenshots of pages. FileSurfer opens local files by converting them to text. Coder writes code, "
            "and ComputerTerminal runs it.",
            "The Orchestrator keeps a plan (its 'ledger'). Every turn it asks itself whether the task is done and "
            "whether the team is stuck, and it re-plans if so.",
            "This is a GAIA task. Please don't copy its question into anything public.",
        ],
        "design": ("Documentation check: 'no tool can view images' is partly true. FileSurfer cannot interpret "
                   "images, but WebSurfer is multimodal and can open local files; it was never asked to."),
    },
]


def load_runs() -> dict[str, dict[str, dict]]:
    out = {}
    for run, _ in RUNS:
        with open(paths.LLM_ANNOTATIONS / f"{run}.jsonl") as f:
            out[run] = {r["uid"]: r for r in map(json.loads, f)}
    return out


def coding_view(rec: dict) -> dict:
    c, row = rec["coding"], rec["row"]
    return {
        "failure_observed": row["failure_observed"],
        "l4": row["l4_codes"], "l3": row["l3_codes"], "l2": row["l2_codes"], "l1": row["l1_codes"],
        "error_functions": row.get("error_functions", ""),
        "deepest": row["deepest_layer"],
        "violation": row["violation_flag"], "evidence_grade": row["violation_evidence"],
        "confidence": row["confidence"],
        "summary": c.get("causal_summary", ""),
        "notes": c.get("notes", ""),
        "evidence": [{"step": e["step"], "quote": e["quote"], "codes": e["codes"]} for e in c.get("evidence", [])],
    }


def outcome_text(trace: dict) -> str:
    for s in trace["steps"]:
        if s["kind"] == "benchmark_info":
            m = re.search(r'"success":\s*(true|false)', s["text"])
            if m:
                return f"The benchmark's own check says the task {'passed' if m.group(1) == 'true' else 'failed'} (step {s['n']})."
    return "No benchmark verdict is recorded in this log, so whether the final answer was right is not known."


def build() -> None:
    traces = {t["uid"]: t for t in load_traces()}
    runs = load_runs()
    codes = load_codebook_codes("v1")
    cases = []
    for case in CASES:
        t = traces[case["uid"]]
        cases.append({
            **case,
            "framework": t["framework"], "model": t["model"], "benchmark": t["benchmark"],
            "mast": [[k, design.MAST_NAMES[k]] for k in design.MAST_CODES if t["mast_labels"].get(k) == 1],
            "outcome": outcome_text(t),
            "steps": [{"n": s["n"], "agent": s.get("agent", ""), "kind": s["kind"], "text": s["text"]} for s in t["steps"]],
            "runs": [{"name": label, **coding_view(runs[run][case["uid"]])} for run, label in RUNS],
        })
    data = {"cases": cases, "codes": codes}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    OUTPUT.write_text(TEMPLATE.read_text().replace("/*__DATA__*/", blob))
    print(f"wrote {OUTPUT.relative_to(paths.ROOT)} ({len(cases)} cases, {OUTPUT.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    build()
