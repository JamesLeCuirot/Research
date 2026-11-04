"""Post-hoc check of the Claude Code harness context, requested by the audit (4 November 2026).
Not pre-registered.

The monitor calls ran through `claude -p` without `--bare`. Claude Code then adds its own content to
each request (for example the definition of the structured-output tool it uses for --json-schema), and
that content was not logged. This script estimates its size from the token usage in
results/monitor_raw.jsonl and checks that it was the same in every condition and throughout the run.
It also summarises Claude Code's own diagnostics log, if available, to check what context was loaded.

Token accounting. Input tokens per call = inputTokens + cacheReadInputTokens +
cacheCreationInputTokens. Only calls with num_turns == 2 (a single API request; 2,109 of 2,176) are
used. The study's own text per call = system prompt + user message + JSON schema, rebuilt exactly
with monitor.py; the audit verified their SHA-256 against the raw records.

1. Size. Per monitor, OLS of input tokens on the characters of the study's own text, pooled over
   single-item and batch calls. The intercept estimates the constant per-call scaffolding in tokens.
2. Same across conditions. In Experiment 2 each item was judged under none, S50 and S1, with
   prompts that differ only in one sentence and the random ID. Token differences within an item
   (S50 minus none, S1 minus none) should therefore be constant: the sentence's token count, plus or
   minus a token or two for the ID. For Experiments 1 and 3, the two monitors saw byte-identical
   prompts (same batch composition and IDs), so Sonnet minus Haiku tokens per batch should also be
   constant if the scaffolding is the same.
3. Same over time. In Experiment 2, the residual after removing item and condition effects (per
   monitor), summarised by 10-minute window and by the git commits made in the repository during the
   run. If Claude Code had injected git status, a commit would shift the token count.
4. Diagnostics log (optional argument: path to the CLAUDE_CODE_DIAGNOSTICS_FILE written during the run).
   For each study window, the script counts process starts, memory/CLAUDE.md files loaded,
   project-context flags, git system-context computations and hook spawns. Only event names, counts
   and boolean or length fields are kept; no personal data is written.

Usage: python posthoc_harness_context.py [/tmp/claude-code-<id>.diag.log]
Writes results/harness_context.json and prints a summary.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from common import DATA, RESULTS, ROOT, read_jsonl
from monitor import schema, system_prompt, user_message

WINDOWS = {  # study windows (UTC), from the run logs
    "generation": ("2026-11-03T22:49:20", "2026-11-03T23:05:30"),
    "calibration": ("2026-11-03T23:09:30", "2026-11-03T23:10:50"),
    "main experiments": ("2026-11-03T23:12:20", "2026-11-04T00:11:45"),
}


def call_table() -> pd.DataFrame:
    items = {it["problem_id"]: it for it in read_jsonl(DATA / "items.jsonl")}
    rows = []
    for r in read_jsonl(RESULTS / "monitor_raw.jsonl"):
        a = r["attempts"][0]
        u = list(a["model_usage"].values())[0]
        sys_txt = system_prompt(r["variant"])
        usr = user_message(r, items)
        sch = json.dumps(schema([s["sid"] for s in r["shown"]]))
        rows.append({
            "call_id": r["call_id"], "batch_key": r["batch_key"], "monitor": r["monitor"].replace("claude-", "").replace("-5-5", ""),
            "experiment": r["experiment"], "condition": r["condition"], "unit": r["unit"], "num_turns": a["num_turns"],
            "at": a["at"], "problem_id": r["shown"][0]["problem_id"], "backdoored": r["shown"][0]["backdoored"],
            "tokens_in": (u["inputTokens"] or 0) + (u["cacheReadInputTokens"] or 0) + (u["cacheCreationInputTokens"] or 0),
            "chars_system": len(sys_txt), "chars_user": len(usr), "chars_schema": len(sch),
        })
    d = pd.DataFrame(rows)
    d["chars_own"] = d.chars_system + d.chars_user + d.chars_schema
    return d


def commits_in_run() -> list[str]:
    try:
        out = subprocess.run(["git", "log", "--since=2026-11-03T23:12:00Z", "--until=2026-11-04T00:12:00Z", "--format=%cI"],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
        return sorted(out)
    except Exception:  # noqa: BLE001
        return []


def diag_summary(path: str) -> dict:
    keep = {"init_started", "memory_files_completed", "user_context_completed", "system_context_started",
            "system_context_completed", "hook_spawn_started", "is_git_check_completed"}
    out = {w: Counter({k: 0 for k in sorted(keep)}) for w in WINDOWS}
    for line in open(path):
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        ev = e.get("event")
        if ev not in keep:
            continue
        t = e["timestamp"][:19]
        w = next((k for k, (a, b) in WINDOWS.items() if a <= t <= b), None)
        if w is None:
            continue
        dd = e.get("data") or {}
        c = out[w]
        c[ev] += 1
        if ev == "memory_files_completed":
            c["memory_files_loaded_total"] += dd.get("file_count", 0)
            c["memory_files_chars_total"] += dd.get("total_content_length", 0)
        if ev == "user_context_completed":
            c["claudemd_chars_total"] += dd.get("claudemd_length", 0)
            c["with_project_context"] += bool(dd.get("has_project_context"))
            c["with_user_email_field"] += bool(dd.get("has_user_email"))
        if ev == "is_git_check_completed":
            c["cwd_is_git_repo"] += bool(dd.get("is_git"))
    return {w: dict(c) for w, c in out.items()}


def main() -> None:
    d = call_table()
    one = d[d.num_turns == 2].copy()
    res = {"note": "post hoc (not pre-registered)", "n_calls": int(len(d)), "n_single_request_calls": int(len(one))}

    # 1. Size of the scaffolding
    size = {}
    for mon, g in one.groupby("monitor"):
        m = smf.ols("tokens_in ~ chars_own", data=g).fit()
        ci = m.conf_int().loc["Intercept"]
        size[mon] = {"intercept_tokens": float(m.params["Intercept"]), "intercept_ci95": [float(ci[0]), float(ci[1])],
                     "tokens_per_char": float(m.params["chars_own"]), "r2": float(m.rsquared), "n": int(len(g)),
                     "mean_tokens_in_single": float(g[g.unit == "single"].tokens_in.mean()),
                     "mean_tokens_in_batch": float(g[g.unit == "batch"].tokens_in.mean()),
                     "mean_chars_own_single": float(g[g.unit == "single"].chars_own.mean()),
                     "mean_chars_own_batch": float(g[g.unit == "batch"].chars_own.mean())}
        size[mon]["share_of_input_single"] = size[mon]["intercept_tokens"] / size[mon]["mean_tokens_in_single"]
        size[mon]["share_of_input_batch"] = size[mon]["intercept_tokens"] / size[mon]["mean_tokens_in_batch"]
        # residual by condition (does the per-call overhead differ by condition?)
        g = g.assign(resid=m.resid)
        size[mon]["mean_residual_by_condition"] = {c: round(float(v), 1) for c, v in g.groupby("condition").resid.mean().items()}
    res["size"] = size

    # 2a. Same across conditions: within-item differences in Experiment 2
    e2 = one[one.experiment == "exp2"]
    w = e2.pivot_table(index=["monitor", "problem_id", "backdoored"], columns="condition", values="tokens_in")
    within = {}
    for mon in sorted(e2.monitor.unique()):
        ww = w.loc[mon]
        within[mon] = {}
        for c in ("S50", "S1"):
            diff = (ww[c] - ww["none"]).dropna()
            within[mon][f"{c}_minus_none"] = {"n": int(len(diff)), "mean": float(diff.mean()), "sd": float(diff.std()),
                                              "min": float(diff.min()), "max": float(diff.max()),
                                              "share_within_2_tokens_of_median": float((abs(diff - diff.median()) <= 2).mean())}
    res["within_item_condition_differences"] = within
    # 2b. Same across monitors: identical batch prompts
    b = one[one.unit == "batch"].pivot_table(index="batch_key", columns="monitor", values="tokens_in").dropna()
    diff = b["sonnet"] - b["haiku"]
    res["sonnet_minus_haiku_identical_batch_prompts"] = {"n_batches": int(len(diff)), "mean": float(diff.mean()), "sd": float(diff.std()),
                                                         "min": float(diff.min()), "max": float(diff.max()),
                                                         "values": {str(k): int(v) for k, v in Counter(diff.astype(int)).most_common(5)}}

    # 3. Same over time (Experiment 2 residuals)
    e2 = e2.copy()
    e2["resid"] = e2.tokens_in - e2.groupby(["monitor", "problem_id", "backdoored"]).tokens_in.transform("mean")
    e2["resid"] = e2.resid - e2.groupby(["monitor", "condition"]).resid.transform("mean")
    t = pd.to_datetime(e2["at"])
    e2["window"] = t.dt.floor("10min").dt.strftime("%H:%M")
    commits = commits_in_run()
    e2["commit_epoch"] = [sum(c[:19] < a[:19] for c in commits) for a in e2["at"]]
    res["over_time"] = {
        "residual_sd_overall": {m: float(g.resid.std()) for m, g in e2.groupby("monitor")},
        "by_10min_window": {f"{m}|{wnd}": {"mean": round(float(g.resid.mean()), 2), "sd": round(float(g.resid.std()), 2), "n": int(len(g))}
                            for (m, wnd), g in e2.groupby(["monitor", "window"])},
        "n_commits_during_run": len(commits),
        "by_commit_epoch": {f"{m}|{ep}": {"mean": round(float(g.resid.mean()), 2), "n": int(len(g))}
                            for (m, ep), g in e2.groupby(["monitor", "commit_epoch"])},
    }
    ep = e2.groupby(["monitor", "commit_epoch"]).resid.agg(["mean", "count"])
    res["over_time"]["max_abs_epoch_mean"] = float(ep["mean"].abs().max())
    res["over_time"]["max_abs_epoch_mean_epochs_with_20plus_calls"] = float(ep[ep["count"] >= 20]["mean"].abs().max())
    res["over_time"]["epoch_with_max_abs_mean"] = {"monitor_epoch": str(ep["mean"].abs().idxmax()), "n_calls": int(ep.loc[ep["mean"].abs().idxmax(), "count"])}

    # 4. Diagnostics log
    if len(sys.argv) > 1:
        res["diagnostics_log"] = diag_summary(sys.argv[1])

    (RESULTS / "harness_context.json").write_text(json.dumps(res, indent=1))
    for mon, s in size.items():
        print(f"{mon}: scaffolding (OLS intercept) {s['intercept_tokens']:.0f} tokens [95% CI {s['intercept_ci95'][0]:.0f}, "
              f"{s['intercept_ci95'][1]:.0f}], {s['tokens_per_char']:.3f} tokens/char, R2 {s['r2']:.4f}, n {s['n']}; "
              f"mean input single {s['mean_tokens_in_single']:.0f}, batch {s['mean_tokens_in_batch']:.0f}")
        print(f"   mean residual by condition: {s['mean_residual_by_condition']}")
    for mon, v in within.items():
        print(f"{mon} within-item differences: " + "; ".join(f"{k}: mean {x['mean']:.2f}, SD {x['sd']:.2f}, range {x['min']:.0f} to {x['max']:.0f}" for k, x in v.items()))
    print("Sonnet minus Haiku, identical batch prompts:", {k: v for k, v in res["sonnet_minus_haiku_identical_batch_prompts"].items()})
    print("Residual SD over time:", res["over_time"]["residual_sd_overall"], "| commits during run:", len(commits),
          "| max |epoch mean|:", round(res["over_time"]["max_abs_epoch_mean"], 2), res["over_time"]["epoch_with_max_abs_mean"],
          "| max over epochs with >= 20 calls:", round(res["over_time"]["max_abs_epoch_mean_epochs_with_20plus_calls"], 2))
    print("10-min windows:", {k: v["mean"] for k, v in res["over_time"]["by_10min_window"].items()})
    if "diagnostics_log" in res:
        print("Diagnostics log:", json.dumps(res["diagnostics_log"], indent=1))


if __name__ == "__main__":
    main()
