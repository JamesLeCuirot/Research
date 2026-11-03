"""Run the AI pilot unattended: three annotator runs over the 250 bulk traces.

    uv run python scripts/pilot.py

Runs, in order (codebook v1, prompt annotator_v1, effort high, Claude Code backend):
    sonnet_bulk_r1  claude-sonnet-5-5   primary annotator
    opus_bulk_r1    claude-opus-5-5     second model (model-vs-model agreement)
    sonnet_bulk_r2  claude-sonnet-5-5   same model again (run-vs-run agreement)

Traces go in chunks of 50. After each chunk the encoded public copy of the run
is committed and pushed, so a restarted machine loses at most one chunk
(`afacs-annotate restore` rebuilds the working file). Finished traces are
skipped, so the script can be stopped and started at any time.

A trace that fails twice in a row (e.g. a refusal) is left out of that run.
Exit codes: 0 all runs complete; 3 a chunk stopped early (on a subscription
this is usually a usage limit): run the script again later.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [("sonnet_bulk_r1", "claude-sonnet-5-5"), ("opus_bulk_r1", "claude-opus-5-5"), ("sonnet_bulk_r2", "claude-sonnet-5-5")]
CHUNK = 50
ATTRIBUTION = ("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
               "Claude-Session: https://claude.ai/code/session_01KaEFS39YZUjkGF7oQStm7K")


def bulk_uids() -> list[str]:
    with open(ROOT / "data/processed/bulk_sample.csv") as f:
        return [r["uid"] for r in csv.DictReader(f)]


def done(run: str) -> set[str]:
    path = ROOT / "annotations/llm" / f"{run}.jsonl"
    if not path.exists():
        return set()
    with open(path) as f:
        return {r["uid"] for r in map(json.loads, f) if not r.get("error")}


def sh(*cmd: str) -> int:
    return subprocess.run(cmd, cwd=ROOT).returncode


def commit(run: str, n_done: int, total: int) -> None:
    public = f"annotations/llm/public/{run}.jsonl"
    sh("git", "add", public)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode == 0:
        return
    sh("git", "commit", "-q", "-m", f"AI pilot: {run} {n_done}/{total} traces coded\n\n{ATTRIBUTION}")
    for attempt in range(4):
        if sh("git", "push", "-q", "origin", "HEAD") == 0:
            return
        subprocess.run(["sleep", str(2 ** (attempt + 1))])
    print("  (push failed; the commit is local and will go with the next push)")


def main() -> int:
    uids = bulk_uids()
    for run, model in RUNS:
        attempts: dict[str, int] = {}
        while True:
            # A trace that failed twice (e.g. a refusal) is left out rather than retried for ever.
            todo = [u for u in uids if u not in done(run) and attempts.get(u, 0) < 2]
            if not todo:
                gave_up = [u for u in uids if u not in done(run)]
                print(f"{run}: complete ({len(uids) - len(gave_up)}/{len(uids)} coded"
                      + (f"; gave up on {', '.join(gave_up)}" if gave_up else "") + ")", flush=True)
                break
            chunk = todo[:CHUNK]
            print(f"{run}: {len(done(run))}/{len(uids)} done; coding {len(chunk)} more with {model}", flush=True)
            sh("uv", "run", "afacs-annotate", "run", "--set", ",".join(chunk), "--model", model, "--run-name", run)
            left = [u for u in chunk if u not in done(run)]
            for u in left:
                attempts[u] = attempts.get(u, 0) + 1
            commit(run, len(done(run)), len(uids))
            if len(left) >= 3:  # the annotator stops after three errors in a row: usually a usage limit
                print(f"{run}: {len(left)} traces in this chunk not coded; stopping (usually a usage limit). "
                      "Run the script again later.", flush=True)
                return 3
    print("All runs complete.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
