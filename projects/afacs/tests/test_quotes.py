"""The automatic check of the AI annotator's evidence quotes (codebook v1, note 5.6)."""

from afacs.quotes import check_coding, check_quote, fragments, summarise, visible_steps

TRACE = {"steps": [
    {"n": 1, "kind": "message", "text": "Write a function that returns the   sum of two numbers."},
    {"n": 2, "kind": "message", "text": "I’ll skip the **tests** for now, since they take too long.\nDone."},
    {"n": 3, "kind": "benchmark_info", "text": "Correct answer: 42"},
    {"n": 4, "kind": "tool_output", "text": 'Error: {\\"status\\": \\"failed\\"}'},
]}
STEPS = visible_steps(TRACE)


def test_exact_and_tidied_quotes_are_verified():
    assert check_quote("returns the sum of two numbers", 1, STEPS) == "verified"
    assert check_quote('"I\'ll skip the tests for now"', 2, STEPS) == "verified"  # curly quote, markdown, capitals
    assert check_quote('[S4] Error: {"status": "failed"}', 4, STEPS) == "verified"  # step prefix, escaped JSON


def test_ellipsis_pieces_must_appear_in_order():
    assert check_quote("I'll skip the tests ... take too long", 2, STEPS) == "verified"
    assert check_quote("take too long … I'll skip the tests", 2, STEPS) == "not_found"
    assert fragments("a [...] b") == ["a", "b"]


def test_wrong_step_invented_hidden_and_short():
    assert check_quote("skip the tests", 1, STEPS) == "other_step"
    assert check_quote("I have verified all the tests pass", 2, STEPS) == "not_found"
    assert check_quote("Correct answer: 42", 3, STEPS) == "hidden_step"  # benchmark info is hidden from coders
    assert check_quote("Something", 99, STEPS) == "hidden_step"
    assert check_quote("ok", 2, STEPS) == "too_short"


def test_coding_check_and_summary():
    coding = {"evidence": [{"step": 2, "quote": "skip the tests", "codes": ["L1.V2"]},
                           {"step": 2, "quote": "all tests pass", "codes": ["L1.V2"]}],
              "l4_codes": [], "l3_codes": ["L3.1"], "l2_codes": [], "l1_codes": ["L1.V2"]}
    qc = check_coding(coding, TRACE)
    assert (qc["n_quotes"], qc["verified"], qc["not_found"]) == (2, 1, 1)
    assert qc["codes_without_evidence"] == ["L3.1"]
    s = summarise([qc, check_coding({"evidence": [{"step": 1, "quote": "sum of two numbers", "codes": []}]}, TRACE)])
    assert (s["n_quotes"], s["verified"], s["codings_all_verified"], s["codings_with_unsupported_codes"]) == (3, 2, 1, 1)
