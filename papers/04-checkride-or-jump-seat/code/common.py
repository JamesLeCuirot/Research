"""Shared helpers: one model call through Claude Code headless mode, with retries."""

import json
import random
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
DATA = PAPER / "data"
RESULTS = PAPER / "results"
FIGURES = PAPER / "figures"
PROMPTS = PAPER / "prompts"

MAX_PARALLEL = 4  # agreed ceiling: another experiment uses the same mechanism
_lock = threading.Lock()


def call_claude(system: str, user: str, model: str, effort: str = "low", schema: dict | None = None,
                timeout: int = 600) -> dict:
    """One call to `claude -p` with tools, MCP servers and slash commands switched off."""
    cmd = [
        "claude", "-p", "--model", model, "--effort", effort, "--output-format", "json",
        "--tools", "", "--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence",
        "--system-prompt", system,
    ]
    if schema is not None:
        cmd += ["--json-schema", json.dumps(schema)]
    try:
        proc = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"is_error": True, "result": f"timed out after {timeout} s"}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"is_error": True, "result": (proc.stderr or proc.stdout or "no output").strip()[:500]}


def call_with_retry(system, user, model, effort="low", schema=None, attempts=4) -> dict:
    out = {}
    for k in range(attempts):
        out = call_claude(system, user, model, effort, schema)
        ok = not out.get("is_error") and (schema is None or isinstance(out.get("structured_output"), dict))
        if ok:
            out["_attempts"] = k + 1
            return out
        time.sleep(min(60, 5 * 2 ** k) + random.random() * 3)
    out["_attempts"] = attempts
    return out


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def done_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids = set()
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if not r.get("error"):
                ids.add(r["id"])
    return ids


def append(path: Path, record: dict) -> None:
    with _lock:
        with open(path, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_jobs(jobs: list[dict], worker, label: str) -> None:
    """Run jobs in parallel (at most MAX_PARALLEL at once), printing progress."""
    n = len(jobs)
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as pool:
        futures = {pool.submit(worker, j): j for j in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            j = futures[fut]
            try:
                status = fut.result()
            except Exception as e:  # keep going; failures are logged and can be re-run
                status = f"exception: {e!r}"[:200]
            print(f"[{label} {i}/{n}] {j['id']}: {status}", flush=True)
