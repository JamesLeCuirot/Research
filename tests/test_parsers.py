"""Parser tests on small hand-made snippets of each log format (no download needed)."""

from afacs.parsers import BENCHMARK_INFO, EMPTY_TURN, SYSTEM, TOOL_OUTPUT, parse_trace


def agents(parsed):
    return [s.agent for s in parsed.steps]


def test_ag2_dicts_handles_braces_inside_strings():
    raw = (
        "{'content': ['Solve x {not a dict}', 'line two'], 'role': 'user', 'name': 'chat_manager'} "
        "{'content': ['exitcode: 0 (execution succeeded)', 'Code output: 5'], 'role': 'assistant', 'name': 'Agent_Verifier'} "
        "{'content': [], 'role': 'user', 'name': 'Agent_Problem_Solver'}"
    )
    p = parse_trace("AG2", raw)
    assert agents(p) == ["chat_manager", "Agent_Verifier", "Agent_Problem_Solver"]
    assert p.steps[0].text == "Solve x {not a dict}\nline two"
    assert p.steps[1].kind == TOOL_OUTPUT
    assert p.steps[2].text == EMPTY_TURN


def test_ag2_mathchat_yaml():
    raw = (
        "instance_id: abc\n"
        "problem_statement: Joey has some points.\n"
        "other_data:\n"
        "  correct: False\n"
        "trajectory:\n"
        "      content:\n"
        "            Let's use Python.\n"
        "      role: user\n"
        "      name: mathproxyagent\n"
        "      \n"
        "      content: 9\n"
        "      role: assistant\n"
        "      name: assistant\n"
    )
    p = parse_trace("AG2", raw)
    assert p.steps[0].kind == BENCHMARK_INFO and "correct: False" in p.steps[0].text
    assert agents(p)[1:] == ["mathproxyagent", "assistant"]
    assert p.steps[2].text == "9"


def test_metagpt_blocks_and_empty_task():
    sep = "\n" + "-" * 80 + "\n"
    raw = (
        "=== MetaGPT Agent Communication Log - Started ===\n\n"
        "[2025-05-13 09:55:55] FROM: Human TO: {'<all>'}\nACTION: x.UserRequirement\nCONTENT:\n"
        + sep
        + "\n[2025-05-13 09:55:55] NEW MESSAGES:\n\nSimpleCoder: \nprint('hi')\n"
        + sep
        + "\n[2025-05-13 09:56:00] NEW MESSAGES:\n\nSimpleReviewer: \n"
        + sep
    )
    p = parse_trace("MetaGPT", raw)
    assert "empty task requirement" in p.notes
    humans = [s for s in p.steps if s.agent == "Human"]
    assert humans and "EMPTY" in humans[0].text
    assert [s.agent for s in p.steps if s.kind != SYSTEM] == ["Human", "SimpleCoder", "SimpleReviewer"]
    assert p.steps[-1].text == EMPTY_TURN


def test_magentic_drops_install_log_and_splits_turns():
    raw = (
        "pip install lots of things\n" * 50
        + "SCENARIO.PY STARTING !#!#\n"
        "---------- user ----------\nWhat is 2+2?\n"
        "---------- MagenticOneOrchestrator ----------\nPlease compute.\n"
        "---------- ComputerTerminal ----------\n4\n"
        "---------- MagenticOneOrchestrator ----------\nFINAL ANSWER: 4\nSCENARIO.PY COMPLETE !#!#\nRUN.SH COMPLETE !#!#\n"
    )
    p = parse_trace("Magentic", raw)
    assert p.dropped_chars > 1000
    non_system = [s for s in p.steps if s.kind != SYSTEM]
    assert [s.agent for s in non_system] == ["user", "MagenticOneOrchestrator", "ComputerTerminal", "MagenticOneOrchestrator"]
    assert non_system[2].kind == TOOL_OUTPUT
    assert non_system[3].text == "FINAL ANSWER: 4"
    assert "SCENARIO.PY COMPLETE" in p.steps[-1].text


def test_openmanus_groups_by_agent_step_and_drops_token_counts():
    raw = (
        "INFO     [browser_use] setup\n"
        "2025-03-31 21:52:44.052 | INFO     | __main__:run_flow:20 - Read prompt from task.txt\n"
        "2025-03-31 21:52:44.052 | INFO     | app.flow.planning:_create_initial_plan:138 - Creating plan\n"
        "2025-03-31 21:52:49.897 | INFO     | app.agent.base:run:140 - Executing step 1/20\n"
        "2025-03-31 21:52:51.409 | INFO     | app.llm:update_token_count:250 - Token usage: Input=1\n"
        "2025-03-31 21:52:51.410 | INFO     | app.agent.toolcall:think:81 - ✨ Manus's thoughts: search\n"
        "2025-03-31 21:52:52.000 | INFO     | app.agent.toolcall:act:150 - 🎯 Tool done! Result:\nline two of result\n"
        "2025-03-31 21:52:53.000 | INFO     | app.agent.base:run:140 - Executing step 2/20\n"
    )
    p = parse_trace("OpenManus", raw)
    manus = [s for s in p.steps if s.agent == "Manus"]
    assert len(manus) == 2
    assert "thoughts: search" in manus[0].text and "line two of result" in manus[0].text
    assert "Token usage" not in "\n".join(s.text for s in p.steps)
    assert p.dropped_chars > 0
    assert any(s.agent == "planner" and s.kind == "message" for s in p.steps)  # plans are LLM output


def test_openmanus_truncated_task_gets_a_note():
    raw = (
        "2025-03-31 21:52:44.052 | INFO     | __main__:run_flow:20 - Read prompt from task.txt: What country had the least...\n"
        "2025-03-31 21:52:49.897 | INFO     | app.agent.base:run:140 - Executing step 1/20\n"
    )
    p = parse_trace("OpenManus", raw)
    assert "task text truncated in log" in p.notes
    assert any(s.agent == "note" and "Note added by AFACS" in s.text for s in p.steps)


def test_appworld_headers_nested_and_evaluation():
    raw = (
        "\n\n******************** Task 1/2 (abc_1)  ********************\n"
        "Mark my note as done.\n"
        "Response from Supervisor Agent\n    print(apis.x())\n    \n"
        "Code Execution Output\n\n    [1, 2]\n    \n"
        "Entering phone Agent message loop\n"
        "    Message to phone Agent\n        do it\n"
        "    Reply from phone Agent to Supervisor\n        done\n"
        "Exiting phone Agent message loop\n"
        "Evaluation\n{\n    \"success\": false\n}\n"
    )
    p = parse_trace("AppWorld", raw)
    assert p.steps[0].agent == "user" and "Mark my note" in p.steps[0].text
    assert [s.agent for s in p.steps[1:3]] == ["Response from Supervisor Agent", "Code Execution Output"]
    assert p.steps[2].kind == TOOL_OUTPUT and p.steps[2].text == "[1, 2]"
    assert any(s.agent == "Reply from phone Agent to Supervisor" and s.text == "done" for s in p.steps)
    assert any(s.agent == "Message to phone Agent (request from the Supervisor)" and s.kind == "message" for s in p.steps)
    assert p.steps[-1].kind == BENCHMARK_INFO and '"success": false' in p.steps[-1].text


def test_appworld_loop_outputs_and_repeats():
    raw = (
        "Task text.\n"
        "Entering phone Agent message loop\n"
        "    Message to phone Agent\n        list contacts\n"
        "    Response from phone Agent\n        print(apis.phone.list())\n"
        "    Message to phone Agent\n        [\"Ann\", \"Bob\"]\n"
        "    Reply from phone Agent to Supervisor\n        Ann, Bob\n"
        "Exiting phone Agent message loop\n"
        "Response from send_message API\n    Ann, Bob\n"
        "Message to Supervisor Agent\n    Ann, Bob\n"
    )
    p = parse_trace("AppWorld", raw)
    second = [s for s in p.steps if s.agent.startswith("Message to phone Agent")][1]
    assert second.kind == TOOL_OUTPUT and second.agent.endswith("(code execution output)")
    last = p.steps[-1]
    assert last.agent == "Message to Supervisor Agent" and last.kind == TOOL_OUTPUT
    assert last.text.startswith("(identical to the previous step [S")


def test_hyperagent_speakers():
    raw = (
        "instance_id: x__y-1\n"
        "problem_statement:\n  Fix the bug.\n"
        "other_data:\n  patch: |\n    + fixed\n"
        "trajectory:\n"
        "  HyperAgent_x__y-1 - INFO - Initialized tools\n"
        "  HyperAgent_x__y-1 - INFO - Planner's Response: Thought: look\n  \n  Intern Name: Codebase Navigator\n"
        "  HyperAgent_x__y-1 - INFO - Inner-Navigator-Assistant's Response: found it\n"
        "  HyperAgent_x__y-1 - INFO - Navigator->Planner: here is the file\n"
    )
    p = parse_trace("HyperAgent", raw)
    assert p.steps[0].agent == "user (GitHub issue)" and p.steps[0].text == "Fix the bug."
    assert p.steps[1].kind == BENCHMARK_INFO and "+ fixed" in p.steps[1].text
    assert agents(p)[2:] == ["system", "Planner", "Navigator", "Navigator -> Planner"]
    assert "Intern Name: Codebase Navigator" in p.steps[3].text


def test_chatdev_drops_noise_records():
    raw = (
        "[2025-27-07 19:21:30 INFO] **[Preprocessing]**\n\n**task_prompt**: Build a CLI\n\n"
        "[2025-27-07 19:21:30 INFO] flask app.py did not start for online log\n"
        "[2025-27-07 19:21:31 INFO] Chief Executive Officer: **[Start Chat]** hello\n"
    )
    p = parse_trace("ChatDev", raw)
    assert p.dropped_chars > 0
    assert any(s.agent == "Chief Executive Officer" for s in p.steps)
    assert "empty task requirement" not in p.notes
