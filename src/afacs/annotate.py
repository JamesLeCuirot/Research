"""Stage 4 - annotate: have Claude code traces with the AFACS codebook.

Run:
    uv run afacs-annotate estimate --set bulk                   # cost estimate, no API calls
    uv run afacs-annotate show-prompt --uid C03                 # print exactly what the model sees
    uv run afacs-annotate run --set dev --model claude-sonnet-5-5 --run-name sonnet_dev_p0
    uv run afacs-annotate batch-submit --set bulk --run-name sonnet_bulk_p1   # 50% cheaper, async
    uv run afacs-annotate batch-collect --run-name sonnet_bulk_p1

Sets: calibration, dev, test (from the hidden calibration key), bulk (from the
bulk sample), or a comma-separated list of trace uids / calibration ids.

How it works:
- The system prompt is prompts/<prompt>.md with the codebook pasted in. It is
  identical for every trace, so it is marked for prompt caching: after the
  first call it is billed at a tenth of the normal rate.
- The user message is the trace, rendered exactly as the human coder sees it
  (MAST labels hidden).
- The reply is forced into a fixed JSON shape (structured outputs) whose
  allowed codes are read from the codebook, so the model cannot invent codes.
- Every output line records the model, prompt version, codebook version, a
  hash of the full system prompt, token usage and the request id, so any
  annotation can be traced back to exactly what produced it.
- If the model declines a request (a "refusal"), the trace is recorded as an
  error. We deliberately do not fall back to a different model: an agreement
  study needs every annotation to come from the same annotator.

Needs ANTHROPIC_API_KEY in .env for everything except `estimate` and `show-prompt`.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from afacs import paths
from afacs.ingest import load_traces
from afacs.render import render_markdown
from afacs.schema import (
    CONFIDENCE,
    CURRENT_CODEBOOK,
    DEEPEST_LAYER,
    FAILURE_OBSERVED,
    LAYER_COLUMNS,
    VIOLATION_FLAGS,
    codebook_text,
    layer_of,
    load_codebook_codes,
    validate_coding,
)

DEFAULT_MODEL = "claude-sonnet-5-5"  # bulk annotator, per the plan
SECOND_MODEL = "claude-opus-5-5"  # optional second annotator for LLM-LLM agreement
DEFAULT_PROMPT = "annotator_v0"
DEFAULT_EFFORT = "high"
MAX_TOKENS = 32000

# US dollars per million tokens (Anthropic first-party prices as of Oct 2026;
# check https://www.anthropic.com/pricing before relying on them). Cache writes
# cost 1.25x input; batch requests cost half of everything.
PRICES = {
    "claude-sonnet-5-5": {"input": 2.00, "output": 10.00, "cache_read": 0.20, "cache_write": 2.50},
    "claude-opus-5-5": {"input": 4.00, "output": 20.00, "cache_read": 0.20, "cache_write": 5.00},
}

USER_TEMPLATE = "Code the following trace with the AFACS codebook.\n\n<trace>\n{trace}\n</trace>"


# ---------------------------------------------------------------------------
# Prompt and output schema
# ---------------------------------------------------------------------------


def system_prompt(prompt_name: str, codebook_version: str) -> str:
    template = (paths.PROMPTS_DIR / f"{prompt_name}.md").read_text()
    return template.replace("{codebook}", codebook_text(codebook_version))


def prompt_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def output_schema(codes: dict[str, str]) -> dict:
    """JSON schema for the model's reply. Allowed codes come from the codebook."""

    def code_list(layer: str) -> dict:
        allowed = sorted(c for c in codes if layer_of(c) == layer)
        return {"type": "array", "items": {"type": "string", "enum": allowed}}

    properties = {
        "failure_observed": {"type": "string", "enum": FAILURE_OBSERVED},
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "step": {"type": "integer"},
                    "quote": {"type": "string"},
                    "codes": {"type": "array", "items": {"type": "string", "enum": sorted(codes)}},
                },
                "required": ["step", "quote", "codes"],
                "additionalProperties": False,
            },
        },
        "causal_summary": {"type": "string"},
        **{column: code_list(layer) for layer, column in LAYER_COLUMNS.items()},
        "deepest_layer": {"type": "string", "enum": DEEPEST_LAYER},
        "violation_flag": {"type": "string", "enum": VIOLATION_FLAGS},
        "confidence": {"type": "string", "enum": CONFIDENCE},
        "notes": {"type": "string"},
    }
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def coding_to_row(coding: dict) -> dict:
    """Flatten the model's JSON into the same columns as the human coding sheet."""
    row = {
        "failure_observed": coding["failure_observed"],
        "deepest_layer": coding["deepest_layer"],
        "violation_flag": coding["violation_flag"],
        "confidence": coding["confidence"],
        "evidence_quotes": " | ".join(f'[S{e["step"]}] "{e["quote"]}"' for e in coding["evidence"]),
        "notes": (coding["causal_summary"] + (" || " + coding["notes"] if coding["notes"] else "")).strip(),
    }
    for column in LAYER_COLUMNS.values():
        row[column] = ";".join(coding[column])
    return row


# ---------------------------------------------------------------------------
# Which traces
# ---------------------------------------------------------------------------


def resolve_set(name: str) -> list[str]:
    """Turn a set name (or a comma-separated list of ids) into trace uids."""
    key_rows = []
    if paths.CALIBRATION_KEY.exists():
        with open(paths.CALIBRATION_KEY) as f:
            key_rows = list(csv.DictReader(f))
    cal_to_uid = {r["cal_id"]: r["uid"] for r in key_rows}
    if name == "calibration":
        return [r["uid"] for r in key_rows]
    if name in ("dev", "test"):
        return [r["uid"] for r in key_rows if r["split"] == name]
    if name == "bulk":
        with open(paths.BULK_SAMPLE) as f:
            return [r["uid"] for r in csv.DictReader(f)]
    return [cal_to_uid.get(x.strip(), x.strip()) for x in name.split(",") if x.strip()]


# ---------------------------------------------------------------------------
# Cost estimate
# ---------------------------------------------------------------------------


def estimate_tokens(text: str) -> int:
    """Rough token count without the API: ~3.5 characters per token (conservative for code/JSON)."""
    return round(len(text) / 3.5)


def estimate(uids: list[str], traces: dict[str, dict], prompt_name: str, output_tokens: int, client=None) -> None:
    system = system_prompt(prompt_name, CURRENT_CODEBOOK)
    users = [USER_TEMPLATE.format(trace=render_markdown(traces[u], title="Trace to code")) for u in uids]
    if client is not None:
        count = lambda text, model: client.messages.count_tokens(  # noqa: E731
            model=model, messages=[{"role": "user", "content": text}]
        ).input_tokens
        method = "exact (count_tokens API)"
    else:
        count = lambda text, model: estimate_tokens(text)  # noqa: E731
        method = "approximate (characters / 3.5)"

    print(f"{len(uids)} traces · token counts {method} · assumed {output_tokens:,} output tokens per trace (thinking + JSON)")
    for model, p in PRICES.items():
        sys_tokens = count(system, model)
        trace_tokens = sum(count(u, model) for u in users)
        n = len(uids)
        cost = (
            p["cache_write"] * sys_tokens  # first call writes the cache
            + p["cache_read"] * sys_tokens * max(n - 1, 0)  # the rest read it
            + p["input"] * trace_tokens
            + p["output"] * output_tokens * n
        ) / 1e6
        print(
            f"  {model:18s} system {sys_tokens:,} tok (cached) · traces {trace_tokens:,} tok · "
            f"standard ≈ ${cost:,.2f} · batch ≈ ${cost / 2:,.2f}"
        )
    print("  (Output length is the big unknown: run ~5 dev traces first and use their real usage to refine this.)")


# ---------------------------------------------------------------------------
# Calling the API
# ---------------------------------------------------------------------------


def load_env() -> None:
    """Read KEY=value lines from .env into the environment (tiny stand-in for python-dotenv)."""
    env = paths.ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def make_client():
    import anthropic

    load_env()
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY not found. Copy .env.example to .env and add your key.")
    return anthropic.Anthropic()


def request_params(trace: dict, model: str, effort: str, system: str, schema: dict) -> dict:
    return {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": USER_TEMPLATE.format(trace=render_markdown(trace, title="Trace to code"))}],
        "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": schema}},
    }


def message_to_record(msg, uid: str, meta: dict, codes: dict[str, str]) -> dict:
    """Turn an API response into one line of the output file."""
    usage = getattr(msg, "usage", None)
    record = {
        "uid": uid,
        **meta,
        "model_served": getattr(msg, "model", None),
        "request_id": getattr(msg, "_request_id", None) or getattr(msg, "id", None),
        "stop_reason": msg.stop_reason,
        "usage": {
            k: getattr(usage, k, None)
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
        }
        if usage
        else {},
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "error": None,
    }
    if msg.stop_reason == "refusal":
        details = getattr(msg, "stop_details", None)
        record["error"] = f"refusal ({getattr(details, 'category', None)})"
        return record
    if msg.stop_reason == "max_tokens":
        record["error"] = "max_tokens reached before the JSON was complete"
        return record
    text = next((b.text for b in msg.content if b.type == "text"), "")
    try:
        coding = json.loads(text)
    except json.JSONDecodeError as e:
        record["error"] = f"invalid JSON: {e}"
        return record
    record["coding"] = coding
    record["row"] = coding_to_row(coding)
    errors, warnings = validate_coding(record["row"], codes)
    record["validation_errors"], record["validation_warnings"] = errors, warnings
    return record


def run_meta(model: str, prompt_name: str, effort: str, run_name: str, system: str) -> dict:
    return {
        "run_name": run_name,
        "model_requested": model,
        "prompt_version": prompt_name,
        "codebook_version": CURRENT_CODEBOOK,
        "system_prompt_sha": prompt_hash(system),
        "effort": effort,
    }


def done_uids(out_path: Path) -> set[str]:
    """Traces already annotated successfully in this run (so a run can be resumed)."""
    if not out_path.exists():
        return set()
    with open(out_path) as f:
        return {r["uid"] for r in map(json.loads, f) if not r.get("error")}


def run_sync(client, uids, traces, model, effort, prompt_name, run_name) -> None:
    system = system_prompt(prompt_name, CURRENT_CODEBOOK)
    codes = load_codebook_codes(CURRENT_CODEBOOK)
    schema = output_schema(codes)
    meta = run_meta(model, prompt_name, effort, run_name, system)
    out_path = paths.LLM_ANNOTATIONS / f"{run_name}.jsonl"
    paths.LLM_ANNOTATIONS.mkdir(parents=True, exist_ok=True)
    skip = done_uids(out_path)
    todo = [u for u in uids if u not in skip]
    print(f"{len(todo)} to annotate ({len(skip)} already done) -> {out_path.relative_to(paths.ROOT)}")
    for i, uid in enumerate(todo, start=1):
        params = request_params(traces[uid], model, effort, system, schema)
        with client.messages.stream(**params) as stream:
            msg = stream.get_final_message()
        record = message_to_record(msg, uid, meta, codes)
        with open(out_path, "a") as f:
            f.write(json.dumps(record) + "\n")
        u = record["usage"]
        status = record["error"] or ("ok" if not record.get("validation_errors") else "ok (validation errors)")
        print(f"  [{i}/{len(todo)}] {uid}: {status} · in {u.get('input_tokens')} cache-read {u.get('cache_read_input_tokens')} out {u.get('output_tokens')}")


def batch_submit(client, uids, traces, model, effort, prompt_name, run_name) -> None:
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    system = system_prompt(prompt_name, CURRENT_CODEBOOK)
    schema = output_schema(load_codebook_codes(CURRENT_CODEBOOK))
    # custom_id must be short and simple, so we use the position and keep a map.
    id_map = {f"t{i:04d}": uid for i, uid in enumerate(uids)}
    requests = [
        Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**request_params(traces[uid], model, effort, system, schema)))
        for cid, uid in id_map.items()
    ]
    batch = client.messages.batches.create(requests=requests)
    manifest = {"batch_id": batch.id, "id_map": id_map, **run_meta(model, prompt_name, effort, run_name, system)}
    paths.LLM_ANNOTATIONS.mkdir(parents=True, exist_ok=True)
    (paths.LLM_ANNOTATIONS / f"{run_name}.batch.json").write_text(json.dumps(manifest, indent=2))
    print(f"Submitted batch {batch.id} with {len(requests)} requests. Collect later with:")
    print(f"  uv run afacs-annotate batch-collect --run-name {run_name}")


def batch_collect(client, run_name: str, wait: bool) -> None:
    manifest = json.loads((paths.LLM_ANNOTATIONS / f"{run_name}.batch.json").read_text())
    while True:
        batch = client.messages.batches.retrieve(manifest["batch_id"])
        if batch.processing_status == "ended" or not wait:
            break
        print(f"  status {batch.processing_status}, still processing {batch.request_counts.processing}; checking again in 60s")
        time.sleep(60)
    if batch.processing_status != "ended":
        print(f"Batch not finished yet ({batch.processing_status}). Re-run later, or add --wait.")
        return
    codes = load_codebook_codes(manifest["codebook_version"])
    meta = {k: manifest[k] for k in ("run_name", "model_requested", "prompt_version", "codebook_version", "system_prompt_sha", "effort")}
    out_path = paths.LLM_ANNOTATIONS / f"{run_name}.jsonl"
    n = 0
    with open(out_path, "w") as f:
        for result in client.messages.batches.results(manifest["batch_id"]):
            uid = manifest["id_map"][result.custom_id]
            if result.result.type == "succeeded":
                record = message_to_record(result.result.message, uid, meta, codes)
            else:
                record = {"uid": uid, **meta, "error": f"batch result {result.result.type}"}
            f.write(json.dumps(record) + "\n")
            n += 1
    print(f"Wrote {n} annotations to {out_path.relative_to(paths.ROOT)}")


# ---------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("estimate", "run", "batch-submit"):
        p = sub.add_parser(name)
        p.add_argument("--set", required=True, help="calibration | dev | test | bulk | comma-separated ids")
        p.add_argument("--prompt", default=DEFAULT_PROMPT)
        if name == "estimate":
            p.add_argument("--output-tokens", type=int, default=4000, help="assumed output tokens per trace")
            p.add_argument("--exact", action="store_true", help="use the count_tokens API (needs a key)")
        else:
            p.add_argument("--model", default=DEFAULT_MODEL)
            p.add_argument("--effort", default=DEFAULT_EFFORT, choices=["low", "medium", "high", "xhigh", "max"])
            p.add_argument("--run-name", required=True, help="output file name, e.g. sonnet_dev_p0")
    p = sub.add_parser("batch-collect")
    p.add_argument("--run-name", required=True)
    p.add_argument("--wait", action="store_true", help="keep polling until the batch ends")
    p = sub.add_parser("show-prompt")
    p.add_argument("--uid", required=True, help="trace uid or calibration id")
    p.add_argument("--prompt", default=DEFAULT_PROMPT)
    args = ap.parse_args()

    if args.command == "batch-collect":
        batch_collect(make_client(), args.run_name, args.wait)
        return

    traces = {t["uid"]: t for t in load_traces()}
    if args.command == "show-prompt":
        uid = resolve_set(args.uid)[0]
        print("=== SYSTEM PROMPT (cached) ===\n")
        print(system_prompt(args.prompt, CURRENT_CODEBOOK))
        print("\n=== USER MESSAGE ===\n")
        print(USER_TEMPLATE.format(trace=render_markdown(traces[uid], title="Trace to code")))
        return

    uids = resolve_set(args.set)
    missing = [u for u in uids if u not in traces]
    if missing:
        raise SystemExit(f"Unknown trace ids: {missing[:5]}")
    if args.command == "estimate":
        estimate(uids, traces, args.prompt, args.output_tokens, client=make_client() if args.exact else None)
    elif args.command == "run":
        run_sync(make_client(), uids, traces, args.model, args.effort, args.prompt, args.run_name)
    elif args.command == "batch-submit":
        batch_submit(make_client(), uids, traces, args.model, args.effort, args.prompt, args.run_name)


if __name__ == "__main__":
    main()
