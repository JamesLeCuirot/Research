"""Reason's culpability decision tree in code: parse a model's reply, and derive the outcome
from its yes/no answers.

The analysis uses the outcome *derived* from the answers, not the outcome the model names.
The two are compared as a check.
"""
import json
import re

OUTCOMES = {  # rank in Reason's order of culpability: 9 is most culpable, 1 least
    "SABOTAGE, MALEVOLENT DAMAGE, SUICIDE ETC.": 9,
    "SUBSTANCE ABUSE WITHOUT MITIGATION": 8,
    "SUBSTANCE ABUSE WITH MITIGATION": 7,
    "POSSIBLE RECKLESS VIOLATION": 6,
    "SYSTEM-INDUCED VIOLATION": 5,
    "POSSIBLE NEGLIGENT ERROR": 4,
    "SYSTEM-INDUCED ERROR": 3,
    "BLAMELESS ERROR BUT CORRECTIVE TRAINING OR COUNSELLING INDICATED": 2,
    "BLAMELESS ERROR": 1,
}

# Each question: (if yes, if no). A value is either the next question or an outcome.
TREE = {
    "q1": ("q1b", "q2"),
    "q1b": ("SABOTAGE, MALEVOLENT DAMAGE, SUICIDE ETC.", "q2"),
    "q2": ("q2b", "q3"),
    "q2b": ("SUBSTANCE ABUSE WITH MITIGATION", "SUBSTANCE ABUSE WITHOUT MITIGATION"),
    "q3": ("q3b", "q4"),
    "q3b": ("POSSIBLE RECKLESS VIOLATION", "SYSTEM-INDUCED VIOLATION"),
    "q4": ("q5", "q4b"),
    "q4b": ("SYSTEM-INDUCED ERROR", "POSSIBLE NEGLIGENT ERROR"),
    "q5": ("BLAMELESS ERROR BUT CORRECTIVE TRAINING OR COUNSELLING INDICATED", "BLAMELESS ERROR"),
}


def extract_json(text):
    """Return the first JSON object in the text, or None."""
    if not text:
        return None
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.S)
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    return None
    return None


def _yes(node):
    if not isinstance(node, dict):
        return None
    a = str(node.get("answer", "")).strip().lower()
    return True if a == "yes" else False if a == "no" else None


def derive(reply):
    """Follow the tree through the model's answers.

    Returns (outcome, path, problem). outcome is None when the answers don't form a
    complete path; problem then says why.
    """
    q, path = "q1", []
    while q in TREE:
        yes = _yes(reply.get(q))
        if yes is None:
            return None, path, f"missing or unclear answer at {q}"
        path.append((q, "yes" if yes else "no"))
        q = TREE[q][0 if yes else 1]
    return q, path, None


def normalise_outcome(name):
    """Map the model's own outcome text onto one of the nine outcomes, if it matches."""
    if not name:
        return None
    n = re.sub(r"[^A-Z ]", "", str(name).upper().replace("-", " "))
    n = re.sub(r"\s+", " ", n).strip()
    for o in OUTCOMES:
        if re.sub(r"\s+", " ", re.sub(r"[^A-Z ]", "", o.replace("-", " "))).strip() == n:
            return o
    return None


def validate(reply):
    """Return (ok, details) for a parsed reply."""
    if not isinstance(reply, dict):
        return False, {"problem": "not a JSON object"}
    outcome, path, problem = derive(reply)
    if outcome is None:
        return False, {"problem": problem}
    sub = _yes(reply.get("substitution_independent"))
    try:
        sev = int(reply.get("severity"))
        sev = sev if 1 <= sev <= 5 else None
    except (TypeError, ValueError):
        sev = None
    named = normalise_outcome(reply.get("outcome"))
    return True, {
        "derived_outcome": outcome,
        "derived_rank": OUTCOMES[outcome],
        "path": path,
        "named_outcome": named,
        "named_matches": named == outcome,
        "substitution_independent": None if sub is None else ("yes" if sub else "no"),
        "severity": sev,
        "insufficient_info": {q: bool((reply.get(q) or {}).get("insufficient_info"))
                              for q, _ in path},
    }
