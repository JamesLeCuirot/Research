"""Stage 2 - render: turn one trace into a readable markdown file with numbered steps.

Run:
    uv run afacs-render C07                      # a calibration trace, by its C-number
    uv run afacs-render Magentic_One_GPT4o__065  # any trace, by its unique id
    uv run afacs-render C07 --show-mast          # also show MAST's labels (NOT for blind coding)

The same function produces the text the LLM annotator reads, so the human coder
and the model always see exactly the same trace.
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from afacs import design, paths
from afacs.ingest import load_traces
from afacs.parsers import BENCHMARK_INFO, SYSTEM, TOOL_OUTPUT

KIND_LABELS = {
    TOOL_OUTPUT: " · tool / environment output",
    SYSTEM: " · framework log",
    BENCHMARK_INFO: " · ⚠ NOT VISIBLE TO THE AGENTS (benchmark information)",
}

READING_NOTE = (
    "How to read this: each numbered step is one turn in the run. The name after the step number "
    "is who produced it. Text inside the boxes is verbatim from the log. Steps marked "
    "*framework log* are bookkeeping by the multi-agent framework, not an agent's words. Steps marked "
    "*NOT VISIBLE TO THE AGENTS* hold benchmark information (correct answers, gold patches, the "
    "benchmark's own pass/fail check) that the agents never saw; during coding their content is "
    "hidden, so code from what the agents did. Cite evidence by step number, e.g. [S12]."
)

HIDDEN_BENCHMARK_TEXT = (
    "[Hidden during coding: benchmark information the agents never saw. The step is kept so step "
    "numbers stay the same. View it after coding with `afacs-render <id> --show-benchmark`.]"
)


def fence_for(text: str) -> str:
    """A code fence longer than any run of backticks inside the text, so it can't break out."""
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def shorten(text: str, max_chars: int | None) -> str:
    """Optionally cut the middle out of very long steps, saying exactly how much was cut."""
    if max_chars is None or len(text) <= max_chars:
        return text
    head, tail = text[: max_chars // 2], text[-max_chars // 2 :]
    return f"{head}\n\n[... {len(text) - len(head) - len(tail):,} characters omitted ...]\n\n{tail}"


def render_markdown(
    trace: dict,
    title: str | None = None,
    show_mast: bool = False,
    show_benchmark: bool = not design.HIDE_BENCHMARK_INFO_WHEN_CODING,
    max_step_chars: int | None = None,
) -> str:
    """Markdown for one trace. Defaults are the blind-coding view: no MAST labels, benchmark info hidden."""
    lines = [f"# {title or trace['uid']}", ""]
    lines.append(f"- **Framework:** {trace['framework']} · **Model:** {trace['model']} · **Benchmark:** {trace['benchmark']}")
    lines.append(f"- **Trace id:** `{trace['uid']}` · **Steps:** {trace['n_steps']} · **Length:** about {trace['approx_tokens']:,} tokens")
    if show_mast:
        flagged = [f"{c} {design.MAST_NAMES[c]}" for c, v in trace["mast_labels"].items() if v == 1]
        lines.append(f"- **MAST labels:** {'; '.join(flagged) if flagged else 'none'}")
    lines += ["", f"> {READING_NOTE}", ""]
    for step in trace["steps"]:
        hidden = step["kind"] == BENCHMARK_INFO and not show_benchmark
        text = HIDDEN_BENCHMARK_TEXT if hidden else shorten(step["text"], max_step_chars)
        fence = fence_for(text)
        lines.append(f"### [S{step['n']}] {step['agent']}{KIND_LABELS.get(step['kind'], '')}")
        lines += ["", f"{fence}text", text, fence, ""]
    return "\n".join(lines)


def calibration_lookup() -> dict[str, str]:
    """Map calibration ids (C01...) to trace uids, from the coding sheet."""
    if not paths.CALIBRATION_SHEET.exists():
        return {}
    with open(paths.CALIBRATION_SHEET) as f:
        return {row["cal_id"]: row["uid"] for row in csv.DictReader(f)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("trace", help="a calibration id like C07, or a trace uid")
    ap.add_argument("--out", type=Path, help="output file (default: print to screen)")
    ap.add_argument("--show-mast", action="store_true", help="include MAST's labels in the header (not for blind coding)")
    ap.add_argument("--show-benchmark", action="store_true", help="show benchmark information (not for blind coding)")
    ap.add_argument("--max-step-chars", type=int, help="shorten steps longer than this (default: never)")
    args = ap.parse_args()

    uid, title = args.trace, None
    cal = calibration_lookup()
    if args.trace in cal:
        uid, title = cal[args.trace], f"Calibration trace {args.trace}"
    traces = {t["uid"]: t for t in load_traces()}
    if uid not in traces:
        raise SystemExit(f"Unknown trace {args.trace!r}")
    md = render_markdown(traces[uid], title=title, show_mast=args.show_mast,
                         show_benchmark=args.show_benchmark, max_step_chars=args.max_step_chars)
    if args.out:
        args.out.write_text(md)
        print(f"wrote {args.out}")
    else:
        print(md)


if __name__ == "__main__":
    main()
