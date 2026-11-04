"""Total calls, tokens and list-price-equivalent cost (from Claude Code's modelUsage) per stage and model.

Counts every attempt, including invalid ones and refusals. Rate-limit/overload errors that returned no
model output are not in the files and cost nothing.

Writes results/costs.json.
"""

from __future__ import annotations

import json
from collections import defaultdict

from common import DATA, RESULTS, read_jsonl


def main() -> None:
    stages = {}
    for p in sorted(DATA.glob("generations_*.jsonl")):
        stages[f"generation_{p.stem.split('_')[1]}"] = read_jsonl(p)
    for p in sorted(RESULTS.glob("calibration_*_raw.jsonl")):
        stages[f"calibration_{p.stem.split('_')[1]}"] = read_jsonl(p)
    stages["main_experiments"] = read_jsonl(RESULTS / "monitor_raw.jsonl")
    out = {"note": "costUSD is Claude Code's list-price-equivalent (costBasis 'list'); calls billed to a "
                   "subscription are not charged this amount.", "stages": {}}
    grand = defaultdict(float)
    for name, recs in stages.items():
        tok = defaultdict(lambda: defaultdict(float))
        n_att = 0
        for r in recs:
            for a in r["attempts"]:
                n_att += 1
                for m, u in (a.get("model_usage") or {}).items():
                    for k in ("inputTokens", "outputTokens", "cacheReadInputTokens", "cacheCreationInputTokens", "costUSD"):
                        tok[m][k] += u.get(k) or 0
        cost = sum(v["costUSD"] for v in tok.values())
        out["stages"][name] = {"records": len(recs), "attempts": n_att,
                               "by_model": {m: {k: round(v, 4) for k, v in d.items()} for m, d in tok.items()},
                               "cost_usd_list": round(cost, 2)}
        grand["attempts"] += n_att
        grand["cost_usd_list"] += cost
        for m, d in tok.items():
            for k, v in d.items():
                grand[f"{m}|{k}"] += v
    out["total"] = {k: round(v, 2) for k, v in grand.items()}
    (RESULTS / "costs.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out["total"], indent=1))


if __name__ == "__main__":
    main()
