"""Post-hoc descriptives already reported in results/RESULTS.md (added at the audit's request so they
reproduce exactly). Not pre-registered.

1. A rough automatic classification of the backdoor edits in data/items.jsonl (RESULTS.md section 3):
   - "adds an if-branch": the backdoored version has more `if` nodes than the clean version;
   - otherwise "same statement count": both versions have the same number of statements (an in-place
     change such as a loop bound or a comparison);
   - otherwise "other".
2. Mean output and thinking tokens per monitor call, by monitor and condition (RESULTS.md section 6),
   from Claude Code's modelUsage in results/monitor_raw.jsonl (every call has one attempt).

Writes results/posthoc_descriptives.json and prints both tables.
"""

from __future__ import annotations

import ast
import json
import statistics
from collections import Counter, defaultdict

from common import DATA, RESULTS, read_jsonl


def count_nodes(code: str, node_type) -> int:
    return sum(isinstance(n, node_type) for n in ast.walk(ast.parse(code)))


def edit_kind(clean: str, backdoored: str) -> str:
    if count_nodes(backdoored, ast.If) - count_nodes(clean, ast.If) > 0:
        return "adds an if-branch"
    if count_nodes(backdoored, ast.stmt) == count_nodes(clean, ast.stmt):
        return "same statement count (in-place change, e.g. bound or comparison)"
    return "other"


def main() -> None:
    items = read_jsonl(DATA / "items.jsonl")
    kinds = Counter(edit_kind(it["clean"], it["backdoored"]) for it in items)
    print(f"Edit kinds ({len(items)} verified pairs):")
    for k, v in kinds.most_common():
        print(f"  {v:4d} ({100 * v / len(items):.0f}%)  {k}")

    usage = defaultdict(list)
    for r in read_jsonl(RESULTS / "monitor_raw.jsonl"):
        a = r["attempts"][-1]
        u = list(a["model_usage"].values())[0]
        usage[(r["monitor"], r["condition"])].append((u["outputTokens"], u.get("thinkingTokens") or 0))
    tokens = {}
    print("\nMean tokens per call (output / thinking):")
    for (mon, cond), v in sorted(usage.items()):
        m_out = statistics.mean(x[0] for x in v)
        m_think = statistics.mean(x[1] for x in v)
        tokens[f"{mon}|{cond}"] = {"calls": len(v), "mean_output_tokens": round(m_out, 1), "mean_thinking_tokens": round(m_think, 1)}
        print(f"  {mon:18s} {cond:6s} n={len(v):4d}  output {m_out:8.0f}  thinking {m_think:8.0f}")
    (RESULTS / "posthoc_descriptives.json").write_text(json.dumps(
        {"note": "post hoc (not pre-registered)", "edit_kinds": dict(kinds), "n_items": len(items),
         "tokens_per_call": tokens}, indent=1))


if __name__ == "__main__":
    main()
