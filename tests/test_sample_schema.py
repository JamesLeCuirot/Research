"""Tests for the sampling helpers, the coding schema, and the renderer."""

import random

from afacs import design
from afacs.render import fence_for, render_markdown
from afacs.sample import balanced_allocation, pick_calibration
from afacs.schema import load_codebook_codes, normalise_row, split_codes, validate_coding


def test_balanced_allocation_caps_small_groups_and_redistributes():
    assert balanced_allocation({"A": 100, "B": 100, "C": 10}, 90) == {"A": 40, "B": 40, "C": 10}
    assert balanced_allocation({"A": 47, "B": 7, "C": 39}, 85) == {"A": 39, "B": 7, "C": 39}
    assert sum(balanced_allocation({"A": 3, "B": 2}, 10).values()) == 5  # can't exceed what exists
    even = balanced_allocation({"A": 50, "B": 50, "C": 50}, 10)
    assert sum(even.values()) == 10 and max(even.values()) - min(even.values()) <= 1


def test_balanced_allocation_random_cases():
    rng = random.Random(0)
    for _ in range(2000):
        avail = {g: rng.randint(0, 60) for g in "ABCDEF"[: rng.randint(1, 6)]}
        total = rng.randint(0, 300)
        alloc = balanced_allocation(avail, total)
        assert sum(alloc.values()) == min(total, sum(avail.values()))
        assert all(0 <= alloc[g] <= avail[g] for g in avail)
        uncapped = [alloc[g] for g in avail if alloc[g] < avail[g]]
        if uncapped:  # groups with room left are within 1 of each other and of the largest share
            assert max(alloc.values()) - min(uncapped) <= 1


def _fake_pool():
    pool = []
    for fw in design.CALIBRATION_FRAMEWORKS:
        for i in range(12):
            pool.append({"uid": f"{fw}__{i:03d}", "framework": fw, "mast_failed": i >= 2,
                         "quality_exclusion": None, "approx_tokens": 1000})
    return pool


def test_calibration_set_is_balanced_and_blind():
    chosen = pick_calibration(_fake_pool(), random.Random(design.SEED))
    assert len(chosen) == len(design.CALIBRATION_FRAMEWORKS) * design.CALIBRATION_PER_FRAMEWORK
    for fw in design.CALIBRATION_FRAMEWORKS:
        rows = [c for c in chosen if c["trace"]["framework"] == fw]
        assert len(rows) == design.CALIBRATION_PER_FRAMEWORK  # same count everywhere: sheet reveals nothing
        assert sum(c["split"] == "test" for c in rows) == design.CALIBRATION_TEST_PER_FRAMEWORK
    controls = [c for c in chosen if c["role"] == "control"]
    assert len(controls) == design.CALIBRATION_CONTROLS
    assert all(c["trace"]["mast_failed"] is False for c in controls)
    assert sum(c["split"] == "test" for c in controls) == design.CALIBRATION_CONTROLS_TEST
    # same seed, same set
    again = pick_calibration(_fake_pool(), random.Random(design.SEED))
    assert [c["trace"]["uid"] for c in chosen] == [c["trace"]["uid"] for c in again]


def test_codebook_v0_codes_are_parsed():
    codes = load_codebook_codes("v0")
    assert len(codes) == 16
    assert {"L4.1", "L3.4", "L2.3", "L1.E3", "L1.V2", "L1.V?"} <= set(codes)


def test_normalise_row_tidies_spaces_and_capitals():
    r = normalise_row({"failure_observed": "Yes ", "deepest_layer": "l3", "violation_flag": "v?", "confidence": " HIGH",
                       "l3_codes": " l3.1 ; L3.4", "l1_codes": "", "l2_codes": "", "l4_codes": ""})
    assert (r["failure_observed"], r["deepest_layer"], r["violation_flag"], r["confidence"]) == ("yes", "L3", "V?", "high")
    assert r["l3_codes"] == "L3.1;L3.4"
    assert normalise_row({"deepest_layer": "NONE", "violation_flag": "None"})["deepest_layer"] == "none"


def test_split_codes_is_forgiving():
    assert split_codes("l3.1; L3.4,L3.3") == ["L3.1", "L3.4", "L3.3"]
    assert split_codes("") == []
    assert split_codes(None) == []


def _row(**kw):
    base = {
        "failure_observed": "yes", "l4_codes": "", "l3_codes": "L3.4", "l2_codes": "", "l1_codes": "L1.E2",
        "deepest_layer": "L3", "violation_flag": "none", "violation_evidence": "none", "confidence": "medium",
        "evidence_quotes": "", "notes": "",
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
    _, warnings = validate_coding(_row(deepest_layer="none"), codes)
    assert any("'none' but codes were given" in w for w in warnings)


def test_fence_survives_backticks_in_text():
    assert fence_for("plain") == "```"
    assert fence_for("has ```python fences```") == "````"


def test_render_hides_mast_labels_and_benchmark_info_by_default():
    trace = {
        "uid": "X__001", "framework": "AppWorld", "model": "GPT-4o", "benchmark": "Test-C", "n_steps": 2,
        "approx_tokens": 10, "mast_labels": {"1.1": 1},
        "steps": [{"n": 1, "agent": "a", "kind": "message", "text": "hi"},
                  {"n": 2, "agent": "AppWorld evaluation", "kind": "benchmark_info", "text": '{"success": true}'}],
    }
    blind = render_markdown(trace)
    assert "MAST labels" not in blind and '"success": true' not in blind and "[S2]" in blind
    assert "MAST labels" in render_markdown(trace, show_mast=True)
    assert '"success": true' in render_markdown(trace, show_benchmark=True)


def test_codebook_v1_adds_l4_4_and_l4_5():
    codes = load_codebook_codes("v1")
    assert len(codes) == 18 and {"L4.4", "L4.5"} <= set(codes)
    assert len(load_codebook_codes("v1", trace_only=True)) == 17


def test_violation_evidence_grading_rules():
    codes = load_codebook_codes("v1")
    ok = _row(l1_codes="L1.V2", violation_flag="V2", violation_evidence="stated")
    errors, warnings = validate_coding(ok, codes)
    assert errors == [] and warnings == []
    _, warnings = validate_coding(_row(l1_codes="L1.V2", violation_flag="V2", violation_evidence="thin"), codes)
    assert any("violation_evidence" in w for w in warnings)
    _, warnings = validate_coding(_row(l1_codes="L1.V?", violation_flag="V?", violation_evidence="thin"), codes)
    assert not any("violation_evidence" in w for w in warnings)
    errors, _ = validate_coding(_row(violation_evidence="maybe"), codes)
    assert any("violation_evidence" in e for e in errors)


def test_trace_only_codes_exclude_developer_evidence():
    full = load_codebook_codes("v1")
    trace = load_codebook_codes("v1", trace_only=True)
    assert set(full) - set(trace) == {"L4.4"}
    errors, _ = validate_coding(_row(l4_codes="L4.4", deepest_layer="L4"), trace)
    assert any("unknown code 'L4.4'" in e for e in errors)
