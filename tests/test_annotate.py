"""Annotator tests with fake API responses (no network, no API key)."""

import json
from types import SimpleNamespace

from afacs.annotate import coding_to_row, message_to_record, output_schema, request_params, system_prompt
from afacs.schema import load_codebook_codes

CODES = load_codebook_codes("v0")
META = {"run_name": "t", "model_requested": "claude-sonnet-5-5", "prompt_version": "annotator_v0",
        "codebook_version": "v0", "system_prompt_sha": "x", "effort": "high"}

GOOD = {
    "failure_observed": "yes",
    "evidence": [{"step": 3, "quote": "your_code_here", "codes": ["L3.4"]}],
    "causal_summary": "The task text was empty [S2], so the coder emitted a placeholder [S3].",
    "l4_codes": [], "l3_codes": ["L3.4"], "l2_codes": [], "l1_codes": ["L1.E2"],
    "deepest_layer": "L3", "violation_flag": "none", "confidence": "medium", "notes": "",
}


def fake_message(text="", stop_reason="end_turn", stop_details=None):
    usage = SimpleNamespace(input_tokens=100, output_tokens=50, cache_read_input_tokens=2000, cache_creation_input_tokens=0)
    return SimpleNamespace(content=[SimpleNamespace(type="text", text=text)], stop_reason=stop_reason,
                           stop_details=stop_details, usage=usage, model="claude-sonnet-5-5", id="msg_1")


def test_schema_only_allows_codebook_codes_per_layer():
    schema = output_schema(CODES)
    assert schema["properties"]["l3_codes"]["items"]["enum"] == ["L3.1", "L3.2", "L3.3", "L3.4"]
    assert "L1.V?" in schema["properties"]["l1_codes"]["items"]["enum"]
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])


def test_good_reply_becomes_valid_row():
    rec = message_to_record(fake_message(json.dumps(GOOD)), "U1", META, CODES)
    assert rec["error"] is None
    assert rec["row"]["l3_codes"] == "L3.4"
    assert rec["row"]["evidence_quotes"] == '[S3] "your_code_here"'
    assert rec["validation_errors"] == []
    assert rec["usage"]["cache_read_input_tokens"] == 2000
    assert rec["model_served"] == "claude-sonnet-5-5"


def test_refusal_and_truncation_are_recorded_as_errors():
    rec = message_to_record(fake_message(stop_reason="refusal", stop_details=SimpleNamespace(category="cyber")), "U1", META, CODES)
    assert rec["error"] == "refusal (cyber)" and "row" not in rec
    rec = message_to_record(fake_message('{"failure', stop_reason="max_tokens"), "U1", META, CODES)
    assert rec["error"].startswith("max_tokens")


def test_row_flattening_joins_lists():
    row = coding_to_row({**GOOD, "l2_codes": ["L2.1", "L2.3"], "notes": "check S5"})
    assert row["l2_codes"] == "L2.1;L2.3"
    assert row["notes"].endswith("|| check S5")


def test_request_caches_system_prompt_and_hides_mast():
    trace = {"uid": "X__001", "framework": "AG2", "model": "GPT-4o", "benchmark": "GSM", "n_steps": 1,
             "approx_tokens": 10, "mast_labels": {"1.1": 1}, "steps": [{"n": 1, "agent": "a", "kind": "message", "text": "hi"}]}
    system = system_prompt("annotator_v0", "v0")
    assert "`L3.4`" in system  # the codebook is pasted in
    params = request_params(trace, "claude-sonnet-5-5", "high", system, output_schema(CODES))
    assert params["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert "MAST" not in params["messages"][0]["content"]
    assert params["output_config"]["format"]["type"] == "json_schema"


def test_claude_code_result_becomes_record():
    from afacs.annotate import claude_code_to_record
    out = {"is_error": False, "structured_output": GOOD, "session_id": "s1", "stop_reason": "tool_use",
           "modelUsage": {"claude-sonnet-5-5": {}}, "usage": {"input_tokens": 5, "output_tokens": 60,
           "cache_read_input_tokens": 0, "cache_creation_input_tokens": 2000}}
    rec = claude_code_to_record(out, "U1", {**META, "backend": "claude-code"}, CODES)
    assert rec["error"] is None and rec["model_served"] == "claude-sonnet-5-5"
    assert rec["row"]["l3_codes"] == "L3.4" and rec["backend"] == "claude-code"


def test_claude_code_error_is_recorded():
    from afacs.annotate import claude_code_to_record
    rec = claude_code_to_record({"is_error": True, "result": "Usage limit reached"}, "U1", META, CODES)
    assert rec["error"].startswith("Claude Code: Usage limit") and "row" not in rec
