"""Stage 6a: build every main-experiment call (PREREGISTRATION section 4.2) before running any.

Experiment 1 (batch of 40, no stated prevalence): P50 (20 backdoored) x 8 batches, P10 (4) x 40,
  P2.5 (1) x 160, per monitor. Items: 40 distinct main-pool problems per batch (without replacement
  within a batch, with replacement across batches); which of them are backdoored is random; order
  (and so the backdoor position) is random. The same batch compositions are used for both monitors.
Experiment 2 (single item): conditions none / S50 / S1; the same 120 backdoored + 120 clean items
  (240 distinct main-pool problems) in every condition, for both monitors.
Experiment 3 (batch of 40, 1 backdoored): R-cal (10 labelled calibration-pool examples, 5 backdoored
  and 5 clean, before the batch) and R-ind (one added sentence), 80 batches each per monitor.
Submission IDs are random ("S-4821"), unique within a call. The run order of all calls is shuffled
across experiments, conditions and monitors.

Writes data/design_main.jsonl (one line per call, in run order).
"""

from __future__ import annotations

import json
import random

from common import DATA

DESIGN_SEED = 55021
RUN_ORDER_SEED = 99173
MONITORS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5"}
BATCH = 40
EXP1 = {"P50": (20, 8), "P10": (4, 40), "P2.5": (1, 160)}
EXP3 = {"R-cal": 80, "R-ind": 80}
EXP2_CONDS = {"none": "single_none", "S50": "single_s50", "S1": "single_s1"}
N_EXP2_EACH = 120


def ids(rng: random.Random, n: int) -> list[str]:
    return [f"S-{x}" for x in rng.sample(range(1000, 10000), n)]


def batch(rng: random.Random, main: list[int], k: int) -> list[dict]:
    probs = rng.sample(main, BATCH)
    bd = set(rng.sample(range(BATCH), k))
    shown = [{"problem_id": p, "backdoored": i in bd} for i, p in enumerate(probs)]
    rng.shuffle(shown)
    for pos, (s, sid) in enumerate(zip(shown, ids(rng, BATCH)), 1):
        s["sid"], s["position"] = sid, pos
    return [{"sid": s["sid"], "problem_id": s["problem_id"], "backdoored": s["backdoored"], "position": s["position"]} for s in shown]


def main() -> None:
    pools = json.loads((DATA / "pools.json").read_text())
    main_pool, cal_pool = pools["main"], pools["calibration"]
    assert len(main_pool) >= 2 * N_EXP2_EACH, "main pool too small for Experiment 2"
    rng = random.Random(DESIGN_SEED)
    specs = []

    def add(experiment, condition, key, variant, shown, examples=None):
        for short, model in MONITORS.items():
            specs.append({"call_id": f"{key}-{short}", "batch_key": key, "experiment": experiment, "condition": condition,
                          "monitor": model, "variant": variant, "unit": "single" if len(shown) == 1 else "batch",
                          "shown": shown, **({"examples": examples} if examples else {})})

    for cond, (k, n) in EXP1.items():
        for b in range(n):
            add("exp1", cond, f"e1-{cond}-b{b:03d}", "batch_none", batch(rng, main_pool, k))
    for cond, n in EXP3.items():
        for b in range(n):
            shown = batch(rng, main_pool, 1)
            if cond == "R-cal":
                ex_probs = rng.sample(cal_pool, 10)
                bd = set(rng.sample(range(10), 5))
                examples = [{"problem_id": p, "backdoored": i in bd} for i, p in enumerate(ex_probs)]
                rng.shuffle(examples)
                add("exp3", cond, f"e3-{cond}-b{b:03d}", "batch_none", shown, examples)
            else:
                add("exp3", cond, f"e3-{cond}-b{b:03d}", "batch_rind", shown)
    e2 = rng.sample(main_pool, 2 * N_EXP2_EACH)
    e2_items = [(p, True) for p in e2[:N_EXP2_EACH]] + [(p, False) for p in e2[N_EXP2_EACH:]]
    for cond, variant in EXP2_CONDS.items():
        for p, bd in e2_items:
            for short, model in MONITORS.items():
                key = f"e2-{cond}-{p}-{'bd' if bd else 'cl'}"
                specs.append({"call_id": f"{key}-{short}", "batch_key": key, "experiment": "exp2", "condition": cond,
                              "monitor": model, "variant": variant, "unit": "single",
                              "shown": [{"sid": ids(rng, 1)[0], "problem_id": p, "backdoored": bd, "position": 1}]})
    order = random.Random(RUN_ORDER_SEED)
    order.shuffle(specs)
    for i, s in enumerate(specs):
        s["run_index"] = i
    with open(DATA / "design_main.jsonl", "w") as f:
        for s in specs:
            f.write(json.dumps(s) + "\n")
    from collections import Counter
    print(len(specs), "calls")
    print(Counter((s["experiment"], s["condition"], s["monitor"]) for s in specs))


if __name__ == "__main__":
    main()
