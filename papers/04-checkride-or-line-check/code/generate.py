"""Step 1: generate the 48 transcripts (6 scenarios x 2 models x 4 samples).

Run from the repository root:
    uv run python papers/04-checkride-or-line-check/code/generate.py
Re-running skips transcripts already generated without error.
"""

import json
import sys

from common import DATA, PROMPTS, append, call_with_retry, done_ids, now, run_jobs
from scenarios import SCENARIOS, agent_system_prompt

AGENT_MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5"]
SAMPLES = 4
EFFORT = "low"
OUT = DATA / "transcripts.jsonl"


def worker(job: dict) -> str:
    s = job["scenario"]
    system = agent_system_prompt(s)
    out = call_with_retry(system, s["final_user"], job["model"], EFFORT)
    rec = {
        "id": job["id"], "scenario": s["id"], "model": job["model"], "sample": job["sample"], "effort": EFFORT,
        "response": out.get("result") if not out.get("is_error") else None,
        "model_served": ", ".join(out.get("modelUsage") or {}) or None,
        "usage": out.get("usage"), "attempts": out.get("_attempts"), "created_at": now(),
        "error": str(out.get("result"))[:300] if out.get("is_error") else None,
    }
    append(OUT, rec)
    return "error: " + rec["error"] if rec["error"] else f"ok ({len(rec['response'] or '')} chars)"


def main() -> None:
    DATA.mkdir(exist_ok=True)
    PROMPTS.mkdir(exist_ok=True)
    # Keep an exact record of every prompt the agents saw.
    (PROMPTS / "agent_prompts.json").write_text(json.dumps(
        [{"scenario": s["id"], "system": agent_system_prompt(s), "user": s["final_user"], "design_note": s["design_note"]}
         for s in SCENARIOS], indent=2, ensure_ascii=False))
    done = done_ids(OUT)
    jobs = [
        {"id": f"{s['id']}|{m}|{k}", "scenario": s, "model": m, "sample": k}
        for s in SCENARIOS for m in AGENT_MODELS for k in range(1, SAMPLES + 1)
    ]
    jobs = [j for j in jobs if j["id"] not in done]
    if "--dry-run" in sys.argv:
        print(f"{len(jobs)} jobs to run")
        return
    run_jobs(jobs, worker, "generate")


if __name__ == "__main__":
    main()
