"""Make a SIMULATED results file, to test the analysis script before any real data exists.

Model "sim/biased" gets a built-in outcome effect: the bad version is pushed up the tree.
Model "sim/fair" has none. The analysis should find an effect for the first and not the second.
Output: results/sim/raw/main.jsonl. This file is never mixed with real results.
"""
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tree_logic import validate  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
rng = random.Random(1)
cases = [c for c in json.loads((ROOT / "cases" / "cases.json").read_text(encoding="utf-8"))
         if c["set"] in ("main", "control")]
PATHS = {  # rank -> answers along the path
    1: {"q1": "no", "q2": "no", "q3": "no", "q4": "yes", "q5": "no"},
    3: {"q1": "no", "q2": "no", "q3": "no", "q4": "no", "q4b": "yes"},
    4: {"q1": "no", "q2": "no", "q3": "no", "q4": "no", "q4b": "no"},
    5: {"q1": "yes", "q1b": "no", "q2": "no", "q3": "yes", "q3b": "no"},
    6: {"q1": "yes", "q1b": "no", "q2": "no", "q3": "yes", "q3b": "yes"},
}
recs = []
for model, effect in (("sim/biased", 0.35), ("sim/fair", 0.0)):
    for c in cases:
        base = rng.choice([1, 1, 3, 4, 5])
        for version in ("safe", "bad"):
            for wording in ("W1", "W2"):
                for rep in range(1, 6):
                    r = base
                    if version == "bad" and rng.random() < effect:
                        r = {1: 4, 3: 4, 4: 5, 5: 6, 6: 6}[base]
                    if rng.random() < 0.1:  # run-to-run noise
                        r = rng.choice(list(PATHS))
                    reply = {q: {"answer": a, "reason": "sim", "insufficient_info": False} for q, a in PATHS[r].items()}
                    reply["outcome"] = "sim"
                    reply["substitution_independent"] = {"answer": "yes" if r <= 3 else "no", "reason": "sim"}
                    reply["severity"] = 4 if version == "bad" else 2
                    ok, details = validate(reply)
                    recs.append({"call_id": f"{model}|{c['case_id']}|{version}|{wording}|{rep}", "model": model,
                                 "case_id": c["case_id"], "set": c["set"], "version": version, "wording": wording,
                                 "repeat": rep, "valid": ok, "details": details, "reply": reply, "cost_usd": 0})
out = ROOT / "results" / "sim" / "raw" / "main.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(json.dumps(r) for r in recs), encoding="utf-8")
print(f"simulated {len(recs)} records -> {out.relative_to(ROOT)}")
