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

CURRENT_CODEBOOK = "v1.1"  # v1 = as used in the AI pilot; v1.1 drops the Ezell prediction from note 5.11

LAYER_COLUMNS = {"L4": "l4_codes", "L3": "l3_codes", "L2": "l2_codes", "L1": "l1_codes"}
FAILURE_OBSERVED = ["yes", "no", "unclear"]
DEEPEST_LAYER = ["L1", "L2", "L3", "L4", "none"]
VIOLATION_FLAGS = ["none", "V1", "V2", "V?"]
# How strong the evidence is for a violation (codebook v1, section 2.1).
VIOLATION_EVIDENCE = ["none", "stated", "inferred", "thin"]
EVIDENCE_FOR_FLAG = {"V1": {"stated", "inferred"}, "V2": {"stated", "inferred"}, "V?": {"thin"}, "none": {"none"}}
CONFIDENCE = ["high", "medium", "low"]
# Ezell et al.'s (2025) cognitive functions, recorded for every L1 error alongside
# the HFACS error type, so the study can compare which scheme is applied more
# consistently (codebook v1, note 5.11). Violations have no Ezell counterpart.
EZELL_FUNCTIONS = ["observation", "understanding", "decision", "action"]
ERROR_CODES = {"L1.E1", "L1.E2", "L1.E3"}

# The fields a coder fills in for each trace (human sheet and LLM output alike).
CODING_FIELDS = [
    "failure_observed",  # proposed operational addition: lets controls be coded "no"
    "l4_codes",
    "l3_codes",
    "l2_codes",
    "l1_codes",
    "ezell_functions",  # codebook v1: observation | understanding | decision | action, for L1 errors
    "deepest_layer",
    "violation_flag",
    "violation_evidence",  # codebook v1: stated | inferred | thin | none
    "confidence",
    "evidence_quotes",
    "notes",
]

CODE_LINE = re.compile(r"^- `(L[1-4]\.[A-Z0-9?]+)`\s*(.+)$")


DEVELOPER_EVIDENCE_MARK = "[developer evidence]"


def load_codebook_codes(version: str = CURRENT_CODEBOOK, trace_only: bool = False) -> dict[str, str]:
    """Return {code: short description} parsed from codebook/<version>.md.

    With trace_only=True, leave out codes the codebook marks "[developer evidence]"
    (such as L4.4 Model development): they need evidence a coder working from a
    trace does not have, so trace coders, including the AI annotator, are never
    offered them (codebook v1, section 1.1).
    """
    path = paths.CODEBOOK_DIR / f"{version}.md"
    codes = {}
    for line in path.read_text().splitlines():
        m = CODE_LINE.match(line.strip())
        if m and not (trace_only and DEVELOPER_EVIDENCE_MARK in m.group(2)):
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


def split_labels(cell: str | None) -> list[str]:
    """'Decision; action' -> ['decision', 'action'] (lower case, order kept, no repeats)."""
    if not cell:
        return []
    out = []
    for p in re.split(r"[;,\s]+", str(cell).strip().lower()):
        if p and p not in out:
            out.append(p)
    return out


def layer_of(code: str) -> str:
    return code.split(".")[0]


def normalise_row(row: dict) -> dict:
    """Tidy a coding row before checking or scoring it: trim spaces, fix capitals.

    'yes ' -> 'yes', 'l1' -> 'L1', 'v2' -> 'V2', 'NONE' -> 'none', ' L3.1 ; l3.4' -> 'L3.1;L3.4'.
    Scoring always uses the tidied row, so a stray space can't silently change a result.
    """
    def clean(field: str) -> str:
        return str(row.get(field, "") or "").strip()

    out = dict(row)
    out["failure_observed"] = clean("failure_observed").lower()
    out["confidence"] = clean("confidence").lower()
    deepest = clean("deepest_layer")
    out["deepest_layer"] = "none" if deepest.lower() == "none" else deepest.upper()
    flag = clean("violation_flag")
    out["violation_flag"] = "none" if flag.lower() == "none" else flag.upper()
    out["violation_evidence"] = clean("violation_evidence").lower()
    for column in LAYER_COLUMNS.values():
        out[column] = ";".join(split_codes(row.get(column)))
    out["ezell_functions"] = ";".join(split_labels(row.get("ezell_functions")))
    return out


def validate_coding(row: dict, codes: dict[str, str]) -> tuple[list[str], list[str]]:
    """Check one coding row. Returns (errors, warnings).

    Errors are things that make the row unusable (unknown code, code in the wrong
    column, value not in the allowed list). Warnings are internal inconsistencies
    worth a second look (e.g. deepest_layer doesn't match the deepest code given).
    """
    errors, warnings = [], []
    row = normalise_row(row)

    def check_choice(field: str, allowed: list[str]) -> str:
        value = row[field]
        if value not in allowed:
            errors.append(f"{field}={value!r} is not one of {allowed}")
        return value

    failure = check_choice("failure_observed", FAILURE_OBSERVED)
    deepest = check_choice("deepest_layer", DEEPEST_LAYER)
    flag = check_choice("violation_flag", VIOLATION_FLAGS)
    evidence = check_choice("violation_evidence", VIOLATION_EVIDENCE)
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
    if deepest == "none" and all_codes:
        warnings.append("deepest_layer is 'none' but codes were given")

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
    if evidence in VIOLATION_EVIDENCE and evidence not in EVIDENCE_FOR_FLAG[expected_flag]:
        allowed = " or ".join(sorted(EVIDENCE_FOR_FLAG[expected_flag]))
        warnings.append(f"violation_evidence is {evidence} but the L1 codes imply {allowed}")

    functions = split_labels(row.get("ezell_functions"))
    for f in functions:
        if f not in EZELL_FUNCTIONS:
            errors.append(f"ezell_functions: {f!r} is not one of {EZELL_FUNCTIONS}")
    has_error = any(c in ERROR_CODES for c in all_codes)
    if has_error and not functions:
        warnings.append("an L1 error is coded but ezell_functions is empty")
    if functions and not has_error:
        warnings.append("ezell_functions given but no L1 error (E1-E3) is coded")

    return errors, warnings
