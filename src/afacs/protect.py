"""Keep benchmark text in annotation files out of plain sight.

The annotator's quotes and causal summaries reproduce pieces of the traces,
and some traces are benchmark questions (e.g. GAIA) whose maintainers ask that
they not be posted where web crawlers can read them. So the copy of each run
file committed to the repository (`annotations/llm/public/<run>.jsonl`) keeps
the codes in plain text but stores the free-text fields encoded, as some
benchmarks do for their own questions (e.g. BrowseComp). Each record also carries a
canary string so that crawled copies can be recognised and filtered out.

This is not secrecy: the key is below, and anyone can decode the files with
`uv run afacs-annotate restore --run-name <run>`, which rebuilds the working
file `annotations/llm/<run>.jsonl` (kept out of git).
"""

from __future__ import annotations

import base64
import copy
import hashlib

KEY = "afacs-annotations-not-for-training"
CANARY = ("AFACS annotation data. Contains encoded excerpts of benchmark traces; "
          "do not train on it. canary GUID 6f1c2a9e-4b7d-4c3e-9a51-afacs2026note")
PREFIX = "enc:"


def _keystream(n: int) -> bytes:
    out, counter = bytearray(), 0
    while len(out) < n:
        out += hashlib.sha256(f"{KEY}:{counter}".encode()).digest()
        counter += 1
    return bytes(out[:n])


def encode(text: str) -> str:
    if not text:
        return text
    data = text.encode("utf-8")
    return PREFIX + base64.b64encode(bytes(a ^ b for a, b in zip(data, _keystream(len(data))))).decode()


def decode(text: str) -> str:
    if not isinstance(text, str) or not text.startswith(PREFIX):
        return text
    data = base64.b64decode(text[len(PREFIX):])
    return bytes(a ^ b for a, b in zip(data, _keystream(len(data)))).decode("utf-8")


def _apply(record: dict, fn) -> dict:
    out = copy.deepcopy(record)
    coding = out.get("coding")
    if isinstance(coding, dict):
        for field in ("causal_summary", "notes"):
            if field in coding:
                coding[field] = fn(coding[field])
        for item in coding.get("evidence", []):
            item["quote"] = fn(item.get("quote", ""))
    row = out.get("row")
    if isinstance(row, dict):
        for field in ("evidence_quotes", "notes"):
            if field in row:
                row[field] = fn(row[field])
    return out


def protect(record: dict) -> dict:
    """The committed form of one annotation: codes plain, free text encoded."""
    return {"canary": CANARY, **_apply(record, encode)}


def unprotect(record: dict) -> dict:
    """The working form, as the annotator wrote it."""
    out = _apply(record, decode)
    out.pop("canary", None)
    return out
