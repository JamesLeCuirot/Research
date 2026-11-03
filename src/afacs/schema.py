"""The AFACS coding schema: which codes exist, and what a valid coding looks like.

The list of codes is read from the codebook markdown itself (codebook/v0.md,
v1.md, ...), so the codebook file is the single source of truth. A code is any
bullet line that starts with a back-ticked id, e.g.

    - `L3.4` Deficient specification: an ambiguous, contradictory or incomplete task.

Both the human coding sheet and the LLM annotator produce rows with the same
fields (CODING_FIELDS), and both are checked with `validate_coding`.
"""

from __future__ import annotations

import re
from pathlib import Path

from afacs import paths

CURRENT_CODEBOOK = "v0"

LAYER_COLUMNS = {"L4": "l4_codes", "L3": "l3_codes", "L2": "l2_codes", "L1": "l1_codes"}
FAILURE_OBSERVED = ["yes", "no", "unclear"]
DEEPEST_LAYER = ["L1", "L2", "L3", "L4", "none"]
VIOLATION_FLAGS = ["none", "V1", "V2", "V?"]
CONFIDENCE = ["high", "medium", "low"]

# The fields a coder fills in for each trace (human sheet and LLM output alike).
CODING_FIELDS = [
    "failure_observed",  # proposed operational addition: lets controls be coded "no"
    "l4_codes",
    "l3_codes",
    "l2_codes",
    "l1_codes",
    "deepest_layer",
    "violation_flag",
    "confidence",
    "evidence_quotes",
    "notes",
]

CODE_LINE = re.compile(r"^- `(L[1-4]\.[A-Z0-9?]+)`\s*(.+)$")


def load_codebook_codes(version: str = CURRENT_CODEBOOK) -> dict[str, str]:
    """Return {code: short description} parsed from codebook/<version>.md."""
    path = paths.CODEBOOK_DIR / f"{version}.md"
    codes = {}
    for line in path.read_text().splitlines():
        m = CODE_LINE.match(line.strip())
        if m:
            codes[m.group(1)] = m.group(2).strip()
    if not codes:
        raise ValueError(f"No codes found in {path}")
    return codes


def codebook_text(version: str = CURRENT_CODEBOOK) -> str:
    return (paths.CODEBOOK_DIR / f"{version}.md").read_text()


def split_codes(cell: str | None) -> list[str]:
    """'l3.1; L3.4' -> ['L3.1', 'L3.4']. Accepts ; , or whitespace as separators."""
    if not cell:
        return []
    parts = re.split(r"[;,\s]+", str(cell).strip())
    return [p.upper() for p in parts if p]


def layer_of(code: str) -> str:
    return code.split(".")[0]


def validate_coding(row: dict, codes: dict[str, str]) -> tuple[list[str], list[str]]:
    """Check one coding row. Returns (errors, warnings).

    Errors are things that make the row unusable (unknown code, code in the wrong
    column, value not in the allowed list). Warnings are internal inconsistencies
    worth a second look (e.g. deepest_layer doesn't match the deepest code given).
    """
    errors, warnings = [], []

    def check_choice(field: str, allowed: list[str]) -> str:
        value = str(row.get(field, "") or "").strip()
        if value not in allowed:
            errors.append(f"{field}={value!r} is not one of {allowed}")
        return value

    failure = check_choice("failure_observed", FAILURE_OBSERVED)
    deepest = check_choice("deepest_layer", DEEPEST_LAYER)
    flag = check_choice("violation_flag", VIOLATION_FLAGS)
    check_choice("confidence", CONFIDENCE)

    all_codes = []
    for layer, column in LAYER_COLUMNS.items():
        for code in split_codes(row.get(column)):
            if code not in codes:
                errors.append(f"{column}: unknown code {code!r}")
            elif layer_of(code) != layer:
                errors.append(f"{column}: {code} belongs in {LAYER_COLUMNS[layer_of(code)]}")
            all_codes.append(code)

    if failure == "no":
        if all_codes:
            warnings.append("failure_observed is 'no' but codes were given")
        if deepest not in ("none", ""):
            warnings.append("failure_observed is 'no' but deepest_layer is not 'none'")
    if failure == "yes" and not all_codes:
        errors.append("failure_observed is 'yes' but no codes were given")

    if all_codes and deepest in DEEPEST_LAYER and deepest != "none":
        deepest_coded = max(int(layer_of(c)[1]) for c in all_codes)
        if int(deepest[1]) != deepest_coded:
            warnings.append(f"deepest_layer is {deepest} but the deepest code given is at L{deepest_coded}")

    v_codes = {c for c in all_codes if c.startswith("L1.V")}
    expected_flag = "none"
    if "L1.V2" in v_codes:
        expected_flag = "V2"
    elif "L1.V1" in v_codes:
        expected_flag = "V1"
    elif "L1.V?" in v_codes:
        expected_flag = "V?"
    if flag in VIOLATION_FLAGS and flag != expected_flag:
        warnings.append(f"violation_flag is {flag} but the L1 codes imply {expected_flag}")

    return errors, warnings
