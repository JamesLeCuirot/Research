"""Information-audit detectors on small synthetic log snippets (no data download needed)."""

from afacs.info_audit import DETECTORS, FRAMEWORKS, ITEMS, JUDGEMENTS, STATUSES, SUB, complete_task_logged, shown_share


def fires(key, raw, trace=None):
    return DETECTORS[key][1](trace or {"steps": [], "parse_notes": []}, raw)


def test_every_cell_has_a_valid_judgement():
    for key, _, _ in ITEMS:
        for fw in FRAMEWORKS:
            status, reason = JUDGEMENTS[key][fw]
            assert status in STATUSES and reason.strip()


def test_line_timestamps_ignore_dates_inside_content():
    assert SUB["line_timestamps"][1]({}, "[2025-05-14 06:22:10] NEW MESSAGES:")
    assert SUB["line_timestamps"][1]({}, "2025-03-31 21:52:44.052 | INFO     | app.agent.base:run:140 - x")
    assert not SUB["line_timestamps"][1]({}, '    "created_at": "2023-05-18 10:00:00"')  # app data, indented


def test_run_identifiers_skip_bare_uuids():
    assert SUB["run_identifiers"][1]({}, "instance_id: pydata__xarray-4493")
    assert SUB["run_identifiers"][1]({}, "******** Task 17/25 (cf6abd2_3) ********")
    assert not SUB["run_identifiers"][1]({}, "file 'b7f857e4-d8aa-4387-af2a-0e844df5b9d8.xlsx'")


def test_configuration_detectors():
    assert SUB["sampling_params"][1]({}, "ChatGPTConfig(temperature=0.2, top_p=1.0)")
    assert SUB["model_identifier"][1]({}, "| **model_type** | ModelType.GPT_4O |")
    assert SUB["scaffold_versions"][1]({}, "Successfully installed autogen-core-0.4.9")
    assert not SUB["seed"][1]({}, "the seed question asks")


def test_tool_error_detector():
    assert fires("tool_errors", "Traceback (most recent call last):\n  File x")
    assert fires("tool_errors", "2025-03-31 21:52:44.052 | ERROR    | app.llm:ask_tool:250 - API error")
    assert fires("tool_errors", "exitcode: 1 (execution failed)")
    assert not fires("tool_errors", "exitcode: 0 (execution succeeded)")


def test_reasoning_and_system_prompt_detectors():
    assert fires("reasoning", "✨ Manus's thoughts: search the web")
    assert fires("reasoning", "  Thought: I need to open the file")
    assert not fires("reasoning", "I thought about it")
    assert fires("system_prompts", "| **assistant_role_prompt** | You are the CPO |")


def test_complete_task_logged_respects_parse_notes():
    step = {"kind": "message", "agent": "user", "text": "What is 2+2?"}
    assert complete_task_logged({"steps": [step], "parse_notes": []}, "")
    assert not complete_task_logged({"steps": [step], "parse_notes": ["task text truncated in log"]}, "")
    assert not complete_task_logged({"steps": [], "parse_notes": []}, "")


def test_shown_share_hides_zero_on_partial():
    assert shown_share({"status": "partial", "detector_share": 0.0}) is None
    assert shown_share({"status": "absent", "detector_share": 0.0}) == 0.0
    assert shown_share({"status": "present", "detector_share": None}) is None
