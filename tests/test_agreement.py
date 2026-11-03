"""Agreement measures on small made-up codings where the right answer is known."""

from afacs.agreement import any_violation, codes_of, kappa, measures
from afacs.schema import load_codebook_codes

CODES = sorted(load_codebook_codes("v0"))


def row(l4="", l3="", l2="", l1="", deepest="L1", flag="none", failure="yes"):
    return {"l4_codes": l4, "l3_codes": l3, "l2_codes": l2, "l1_codes": l1, "deepest_layer": deepest,
            "violation_flag": flag, "failure_observed": failure, "confidence": "high"}


def test_kappa_basics():
    assert kappa([1, 0, 1, 0], [1, 0, 1, 0]) == 1.0
    assert kappa([1, 1, 1], [1, 1, 1]) is None  # no variation: undefined, not "perfect"
    assert abs(kappa([1, 0, 1, 0], [0, 1, 0, 1]) - (-1.0)) < 1e-9


def test_identical_codings_agree_perfectly_where_defined():
    A = {
        "a": row(l3="L3.4", l1="L1.E2", deepest="L3"),
        "b": row(l2="L2.1", l1="L1.V2", deepest="L2", flag="V2"),
        "c": row(l4="L4.1", l1="L1.E1", deepest="L4"),
        "d": row(failure="no", deepest="none"),
    }
    m = measures(A, A, list(A), CODES)
    assert m["layer_L3"] == 1.0 and m["layer_L1"] == 1.0
    assert m["codes_macro"] == 1.0
    assert m["any_violation"] == 1.0
    assert m["deepest_layer_weighted"] == 1.0


def test_layer_disagreement_lowers_kappa():
    A = {u: row(l3="L3.1" if i % 2 else "", l1="L1.E2") for i, u in enumerate("abcdef")}
    B = {u: row(l3="L3.1" if i < 3 else "", l1="L1.E2") for i, u in enumerate("abcdef")}
    m = measures(A, B, list(A), CODES)
    assert m["layer_L3"] is not None and m["layer_L3"] < 1.0
    assert m["layer_L1"] is None  # both always coded L1: undefined


def test_helpers():
    r = row(l3="L3.1; L3.4", l1="L1.V?")
    assert codes_of(r) == {"L3.1", "L3.4", "L1.V?"}
    assert any_violation(r) == 1
