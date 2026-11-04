"""Step 2: grade every transcript.

Two conditions, each run twice (test-retest) by two grader models:
  rubric   - competency framework: 17 observable-behaviour judgements, four 1-5
             competency grades, then an overall 1-5 grade;
  holistic - a single overall 1-5 conduct grade, with no competency framework.
48 transcripts x 2 conditions x 2 graders x 2 runs = 384 calls.

Run from the repository root:
    uv run python papers/04-checkride-or-jump-seat/code/grade.py
Re-running skips grades already obtained without error.
"""

import json
import random
import sys

from common import DATA, PROMPTS, append, call_with_retry, done_ids, now, run_jobs
from rubric import (GRADER_USER_PREFIX, HOLISTIC_SYSTEM, RUBRIC_SYSTEM, holistic_schema, rubric_schema)
from scenarios import SCENARIOS, transcript_for_grader

GRADERS = ["claude-sonnet-5-5", "claude-opus-5-5"]
RUNS = [1, 2]
EFFORT = "low"
CONDITIONS = {
    "rubric": (RUBRIC_SYSTEM, rubric_schema()),
    "holistic": (HOLISTIC_SYSTEM, holistic_schema()),
}
OUT = DATA / "grades.jsonl"
SCEN = {s["id"]: s for s in SCENARIOS}


def worker(job: dict) -> str:
    system, schema = CONDITIONS[job["condition"]]
    user = GRADER_USER_PREFIX + transcript_for_grader(SCEN[job["t"]["scenario"]], job["t"]["response"])
    out = call_with_retry(system, user, job["grader"], EFFORT, schema)
    rec = {
        "id": job["id"], "transcript_id": job["t"]["id"], "scenario": job["t"]["scenario"], "agent_model": job["t"]["model"],
        "condition": job["condition"], "grader": job["grader"], "run": job["run"], "effort": EFFORT,
        "grades": out.get("structured_output") if isinstance(out.get("structured_output"), dict) else None,
        "model_served": ", ".join(out.get("modelUsage") or {}) or None,
        "usage": out.get("usage"), "attempts": out.get("_attempts"), "created_at": now(),
        "error": None if isinstance(out.get("structured_output"), dict) else str(out.get("result"))[:300],
    }
    append(OUT, rec)
    return "error: " + rec["error"] if rec["error"] else "ok"


def control_transcripts() -> dict:
    """The six scripted controls (see controls.py), written to data/ for the record."""
    from controls import CONTROLS
    recs = {}
    for c in CONTROLS:
        tid = f"{c['scenario']}|scripted-control|1"
        recs[tid] = {"id": tid, "scenario": c["scenario"], "model": "scripted-control", "sample": 1,
                     "intended_level": c["intended_level"], "response": c["response"]}
    with open(DATA / "control_transcripts.jsonl", "w") as f:
        for r in recs.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return recs


def main() -> None:
    PROMPTS.mkdir(exist_ok=True)
    (PROMPTS / "grader_rubric_system.txt").write_text(RUBRIC_SYSTEM)
    (PROMPTS / "grader_holistic_system.txt").write_text(HOLISTIC_SYSTEM)
    (PROMPTS / "grader_schemas.json").write_text(json.dumps({"rubric": rubric_schema(), "holistic": holistic_schema()}, indent=2))
    if "--controls" in sys.argv:
        # Scripted controls: graded once (run 1) by each grader in each condition (24 calls).
        transcripts, runs = control_transcripts(), [1]
    else:
        transcripts = [json.loads(l) for l in open(DATA / "transcripts.jsonl")]
        transcripts, runs = {t["id"]: t for t in transcripts if not t.get("error")}, RUNS
    done = done_ids(OUT)
    jobs = [
        {"id": f"{tid}|{c}|{g}|r{r}", "t": t, "condition": c, "grader": g, "run": r}
        for tid, t in sorted(transcripts.items()) for c in CONDITIONS for g in GRADERS for r in runs
    ]
    jobs = [j for j in jobs if j["id"] not in done]
    random.Random(20261103).shuffle(jobs)  # spread conditions, graders and runs over time
    if "--dry-run" in sys.argv:
        print(f"{len(transcripts)} transcripts, {len(jobs)} grading jobs to run")
        return
    run_jobs(jobs, worker, "grade")


if __name__ == "__main__":
    main()
