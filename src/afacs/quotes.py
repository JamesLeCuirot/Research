"""Check the AI annotator's evidence quotes against the trace (codebook v1, note 5.6).

The annotator must back every code with short verbatim quotes, each citing a
step. This module checks each quote against the step it cites, so the paper
can report how often the annotator's evidence is genuine rather than
paraphrased or made up.

Each quote gets one status:
- `verified`: found in the cited step (after tidying whitespace, curly
  quotes, capitals and markdown; a quote shortened with "..." must have each
  piece in the step, in order);
- `other_step`: not in the cited step but found in another visible step
  (the wording is genuine; the step reference is wrong);
- `not_found`: in no step the annotator could see (paraphrased or invented);
- `hidden_step`: cites a step that is hidden from coders (benchmark
  information) or does not exist;
- `too_short`: under 5 characters once tidied, too short to check.

It also lists codes that the annotator assigned without any evidence item.

Run:
    uv run afacs-annotate check-quotes --run-name sonnet_bulk_p1
"""

from __future__ import annotations

import re
import unicodedata

STATUSES = ("verified", "other_step", "not_found", "hidden_step", "too_short")
MIN_CHARS = 5

_TRANSLATE = str.maketrans({
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "–": "-", "—": "-", "−": "-",
    "`": None, "*": None, "\\": None,
})
_ELLIPSIS = re.compile(r"\[\s*(?:\.\.\.|…)\s*\]|\.\.\.|…")
_STEP_PREFIX = re.compile(r"^\s*\[?S\d+\]?\s*[:\-]?\s*", re.IGNORECASE)
_EDGE = " \"'.,;:!?()[]{}"


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").translate(_TRANSLATE)
    return re.sub(r"\s+", " ", text).strip().lower()


def fragments(quote: str) -> list[str]:
    """The pieces of a quote that must appear in order (split at '...')."""
    quote = _STEP_PREFIX.sub("", quote or "")
    pieces = [normalise(p).strip(_EDGE) for p in _ELLIPSIS.split(quote)]
    return [p for p in pieces if p]


def contains_in_order(haystack: str, pieces: list[str]) -> bool:
    pos = 0
    for piece in pieces:
        found = haystack.find(piece, pos)
        if found < 0:
            return False
        pos = found + len(piece)
    return True


def visible_steps(trace: dict) -> dict[int, str]:
    """Normalised text of each step the annotator saw (benchmark information is hidden)."""
    return {s["n"]: normalise(s.get("text", "")) for s in trace["steps"] if s.get("kind") != "benchmark_info"}


def check_quote(quote: str, step: int, steps: dict[int, str]) -> str:
    pieces = fragments(quote)
    if sum(len(p) for p in pieces) < MIN_CHARS:
        return "too_short"
    if step in steps and contains_in_order(steps[step], pieces):
        return "verified"
    if any(contains_in_order(text, pieces) for n, text in steps.items() if n != step):
        return "other_step"
    if step not in steps:
        return "hidden_step"
    return "not_found"


def check_coding(coding: dict, trace: dict) -> dict:
    """Check every evidence item in one coding. Stored on the run record as `quote_check`."""
    steps = visible_steps(trace)
    items = [{"step": e.get("step"), "status": check_quote(e.get("quote", ""), e.get("step"), steps)}
             for e in coding.get("evidence", [])]
    supported = {c for e in coding.get("evidence", []) for c in e.get("codes", [])}
    assigned = [c for col in ("l4_codes", "l3_codes", "l2_codes", "l1_codes") for c in coding.get(col, [])]
    counts = {s: sum(i["status"] == s for i in items) for s in STATUSES}
    return {"n_quotes": len(items), **counts, "items": items,
            "codes_without_evidence": [c for c in assigned if c not in supported]}


def summarise(checks: list[dict]) -> dict:
    """Totals across a run."""
    total = {s: sum(c[s] for c in checks) for s in STATUSES}
    n_quotes = sum(c["n_quotes"] for c in checks)
    return {
        "n_codings": len(checks),
        "n_quotes": n_quotes,
        **total,
        "share_verified": total["verified"] / n_quotes if n_quotes else float("nan"),
        "codings_with_quotes": sum(c["n_quotes"] > 0 for c in checks),
        "codings_all_verified": sum(c["n_quotes"] > 0 and c["verified"] == c["n_quotes"] for c in checks),
        "codings_with_unsupported_codes": sum(bool(c["codes_without_evidence"]) for c in checks),
    }


def report_lines(summary: dict) -> list[str]:
    """Markdown section for the analysis report."""
    n = summary["n_quotes"]

    def share(k):
        return f"{summary[k]} ({summary[k] / n:.1%})" if n else "0"

    return [
        "## Evidence check: are the annotator's quotes genuine?", "",
        f"Each of the annotator's {n} evidence quotes (across {summary['n_codings']} codings) was checked against "
        "the step it cites (codebook v1, note 5.6).", "",
        "| Result | Quotes |", "|---|---|",
        f"| Found in the cited step | {share('verified')} |",
        f"| Found, but in a different step | {share('other_step')} |",
        f"| Not found in any visible step (paraphrased or invented) | {share('not_found')} |",
        f"| Cites a hidden or non-existent step | {share('hidden_step')} |",
        f"| Too short to check | {share('too_short')} |", "",
        f"Codings whose quotes were all found in the cited step: {summary['codings_all_verified']} of the "
        f"{summary['codings_with_quotes']} that gave quotes (codings of traces judged failure-free usually give none). "
        f"Codings with at least one code that no evidence item supports: {summary['codings_with_unsupported_codes']}.", "",
    ]
