"""Tests for the sampling helpers, the coding schema, and the renderer."""

from afacs.render import fence_for, render_markdown
from afacs.sample import balanced_allocation
from afacs.schema import load_codebook_codes, split_codes, validate_coding


def test_balanced_allocation_caps_small_groups_and_redistributes():
    assert balanced_allocation({"A": 100, "B": 100, "C": 10}, 90) == {"A": 40, "B": 40, "C": 10}
    assert sum(balanced_allocation({"A": 3, "B": 2}, 10).values()) == 5  # can't exceed what exists
    assert balanced_allocation({"A": 50, "B": 50, "C": 50}, 10) == {"A": 4, "B": 3, "C": 3}


def test_codebook_v0_codes_are_parsed():
    codes = load_codebook_codes("v0")
    assert len(codes) == 16
    assert {"L4.1", "L3.4", "L2.3", "L1.E3", "L1.V2", "L1.V?"} <= set(codes)


def test_split_codes_is_forgiving():
    assert split_codes("l3.1; L3.4,L3.3") == ["L3.1", "L3.4", "L3.3"]
    assert split_codes("") == []
    assert split_codes(None) == []


def _row(**kw):
    base = {
        "failure_observed": "yes", "l4_codes": "", "l3_codes": "L3.4", "l2_codes": "", "l1_codes": "L1.E2",
        "deepest_layer": "L3", "violation_flag": "none", "confidence": "medium", "evidence_quotes": "", "notes": "",
    }
    base.update(kw)
    return base


def test_valid_row_passes():
    errors, warnings = validate_coding(_row(), load_codebook_codes("v0"))
    assert errors == [] and warnings == []


def test_wrong_column_and_unknown_code_are_errors():
    codes = load_codebook_codes("v0")
    errors, _ = validate_coding(_row(l2_codes="L3.1"), codes)
    assert any("belongs in l3_codes" in e for e in errors)
    errors, _ = validate_coding(_row(l1_codes="L1.X9"), codes)
    assert any("unknown code" in e for e in errors)


def test_inconsistencies_are_warnings():
    codes = load_codebook_codes("v0")
    _, warnings = validate_coding(_row(deepest_layer="L1"), codes)
    assert any("deepest_layer" in w for w in warnings)
    _, warnings = validate_coding(_row(l1_codes="L1.V2"), codes)
    assert any("violation_flag" in w for w in warnings)


def test_fence_survives_backticks_in_text():
    assert fence_for("plain") == "```"
    assert fence_for("has ```python fences```") == "````"


def test_render_hides_mast_labels_by_default():
    trace = {
        "uid": "X__001", "framework": "AG2", "model": "GPT-4o", "benchmark": "GSM", "n_steps": 1,
        "approx_tokens": 10, "mast_labels": {"1.1": 1}, "steps": [{"n": 1, "agent": "a", "kind": "message", "text": "hi"}],
    }
    assert "MAST labels" not in render_markdown(trace)
    assert "MAST labels" in render_markdown(trace, show_mast=True)
