"""Stage 6b: run every main-experiment monitor call, in the shuffled order of data/design_main.jsonl.

Resumable: final records go to results/monitor_raw.jsonl (one line per call: valid, or dropped after
3 retries per PREREGISTRATION section 7); every attempt, valid or not, goes to
results/monitor_attempts.jsonl.

Usage: python s7_run_monitors.py [--workers 6] [--limit N]
"""

from __future__ import annotations

import argparse

from common import DATA, RESULTS, Runner, read_jsonl
from monitor import make_work, write_prompt_files


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    write_prompt_files()
    items = {it["problem_id"]: it for it in read_jsonl(DATA / "items.jsonl")}
    specs = sorted(read_jsonl(DATA / "design_main.jsonl"), key=lambda s: s["run_index"])
    if args.limit:
        specs = specs[: args.limit]
    Runner(RESULTS / "monitor_raw.jsonl", workers=args.workers).run(
        specs, make_work(items, RESULTS / "monitor_attempts.jsonl"))


if __name__ == "__main__":
    main()
