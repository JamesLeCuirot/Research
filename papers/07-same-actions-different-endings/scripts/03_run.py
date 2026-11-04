"""Step 3: send the cases to the models and record every reply.

Usage:
  python scripts/03_run.py --stage dry      builds every prompt; no API calls, no cost
  python scripts/03_run.py --stage pilot    pilot cases only (needs James's go-ahead)
  python scripts/03_run.py --stage main     main and control cases (needs James's go-ahead)

Every reply is appended to results/raw/<stage>.jsonl, together with the exact model ID, the
provider-reported model, token usage and cost. A rerun skips calls already completed, so it
is safe to restart. The run stops before it can exceed --budget-usd (default 100), or if the
key's own limit is near. The API key is read from .env and never printed.
"""
import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import sys
import threading
import time
import urllib.error
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from tree_logic import extract_json, validate  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODELS = ["anthropic/claude-sonnet-5.5", "openai/gpt-6.1-sol",
          "deepseek/deepseek-v4-pro"]  # google/gemini-3.8-flash dropped for cost under D9
WORDINGS = {
    "W1": "You are an aviation safety investigator in an airline safety department. "
          "Apply Reason's culpability decision tree to the crew's actions in the occurrence below.",
    "W2": "Classify the flight crew's actions in the occurrence below using Reason's culpability decision tree.",
}
FIXED_LINES = ("There is no indication of alcohol, drugs or a medical condition affecting either pilot.\n"
               "No previous safety events are recorded for this crew.")
REPEATS, MAX_TOKENS, ORDER_SEED, MAX_TRIES = 5, 16000, 20261002, 3  # 16000 since D8 (was 4000)


def load_key():
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("No OPENROUTER_API_KEY in .env")


def build_prompt(wording, case, version):
    tree = (ROOT / "prompts" / "tree.md").read_text(encoding="utf-8").strip()
    instr = (ROOT / "prompts" / "instructions.md").read_text(encoding="utf-8").strip()
    outcome = case["safe_outcome"] if version == "safe" else case["bad_outcome"]
    occurrence = f"{case['shared_text'].strip()}\n\nOutcome: {outcome.strip()}\n\n{FIXED_LINES}"
    return f"{WORDINGS[wording]}\n\n{tree}\n\nOCCURRENCE\n\n{occurrence}\n\n{instr}"


def plan(stage):
    cases = json.loads((ROOT / "cases" / "cases.json").read_text(encoding="utf-8"))
    if stage == "pilot":
        cases = [c for c in cases if c["set"] == "pilot"]
    else:
        cases = [c for c in cases if c["set"] in ("main", "control")]
    calls = [{"call_id": f"{m}|{c['case_id']}|{v}|{w}|{r}", "model": m, "case_id": c["case_id"],
              "set": c["set"], "version": v, "wording": w, "repeat": r,
              "prompt": build_prompt(w, c, v)}
             for m in MODELS for c in cases for v in ("safe", "bad") for w in WORDINGS
             for r in range(1, REPEATS + 1)]
    random.Random(ORDER_SEED).shuffle(calls)
    return calls


def call_openrouter(key, model, prompt):
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": MAX_TOKENS, "usage": {"include": True}}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json",
                                          "X-Title": "same-actions-different-endings"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["dry", "pilot", "main"], required=True)
    ap.add_argument("--budget-usd", type=float, default=100.0)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    calls = plan(args.stage)
    words = sum(len(c["prompt"].split()) for c in calls)
    print(f"{args.stage}: {len(calls)} calls; about {words * 1.35 / 1e6:.2f}M input tokens")
    if args.stage == "dry":
        out = ROOT / "results" / "dry-run-sample-prompt.txt"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(calls[0]["prompt"], encoding="utf-8")
        print(f"sample prompt written to {out.relative_to(ROOT)}")
        return

    key = load_key()
    outfile = ROOT / "results" / "raw" / f"{args.stage}.jsonl"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    done, spent = set(), 0.0
    if outfile.exists():
        for line in outfile.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            spent += rec.get("cost_usd") or 0.0
            if rec.get("valid"):
                done.add(rec["call_id"])
    todo = [c for c in calls if c["call_id"] not in done]
    print(f"already complete: {len(done)}; to do: {len(todo)}; spent so far ${spent:.2f}")

    lock, stop = threading.Lock(), threading.Event()
    state = {"spent": spent}

    def work(c):
        if stop.is_set():
            return
        for attempt in range(1, MAX_TRIES + 1):
            rec = {k: c[k] for k in ("call_id", "model", "case_id", "set", "version", "wording", "repeat")}
            rec.update({"attempt": attempt, "time": time.strftime("%Y-%m-%dT%H:%M:%S")})
            try:
                resp = call_openrouter(key, c["model"], c["prompt"])
                text = resp["choices"][0]["message"].get("content") or ""
                usage = resp.get("usage") or {}
                reply = extract_json(text)
                ok, details = validate(reply)
                rec.update({"provider_model": resp.get("model"), "provider": resp.get("provider"),
                            "response_id": resp.get("id"), "usage": usage,
                            "cost_usd": usage.get("cost"), "valid": ok, "details": details,
                            "reply": reply, "raw_text": text if not ok else None})
            except (urllib.error.URLError, KeyError, TimeoutError, json.JSONDecodeError) as e:
                rec.update({"valid": False, "error": repr(e)[:300], "cost_usd": 0.0})
            with lock:
                state["spent"] += rec.get("cost_usd") or 0.0
                with outfile.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                if state["spent"] >= args.budget_usd:
                    stop.set()
            if rec.get("valid") or stop.is_set():
                return
            time.sleep(2 * attempt)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, _ in enumerate(ex.map(work, todo), start=1):
            if i % 50 == 0:
                print(f"  {i}/{len(todo)} calls, ${state['spent']:.2f} spent")
    print(f"finished: ${state['spent']:.2f} spent" + ("; STOPPED at budget" if stop.is_set() else ""))


if __name__ == "__main__":
    main()
