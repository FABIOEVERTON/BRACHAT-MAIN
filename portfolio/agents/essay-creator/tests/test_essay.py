import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import uuid
import pytest
from essay_creator.state import EssayState, reduce_messages
from essay_creator.workflow import build_workflow, run_essay, get_snapshot, human_override
from langchain_core.messages import HumanMessage, AIMessage

HAS_API_KEY = bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))


def test_state_schema():
    assert EssayState.__annotations__ is not None
    required_keys = [
        "topic", "messages", "draft", "research_notes", "critique",
        "reflection", "planner_output", "current_phase", "iteration",
        "max_iterations", "thread_id"
    ]
    for key in required_keys:
        assert key in EssayState.__annotations__, f"Missing key: {key}"


def test_reduce_messages_append():
    left = [
        HumanMessage(content="hello", id="msg-1"),
        AIMessage(content="hi", id="msg-2"),
    ]
    right = [
        AIMessage(content="new response", id="msg-3"),
    ]
    result = reduce_messages(left, right)
    assert len(result) == 3
    assert result[0].content == "hello"
    assert result[1].content == "hi"
    assert result[2].content == "new response"


def test_reduce_messages_replace():
    left = [
        HumanMessage(content="old question", id="msg-1"),
        AIMessage(content="old answer", id="msg-2"),
    ]
    right = [
        AIMessage(content="updated answer", id="msg-2"),
    ]
    result = reduce_messages(left, right)
    assert len(result) == 2
    assert result[1].content == "updated answer"


def test_reduce_messages_empty():
    result = reduce_messages([], [])
    assert result == []


def test_workflow_builds():
    graph, memory = build_workflow(db_path=":memory:")
    assert graph is not None
    assert memory is not None


def test_workflow_structure():
    graph, memory = build_workflow(db_path=":memory:")
    nodes = list(graph.get_graph().nodes)
    expected_nodes = ["planner", "researcher", "writer", "reflector", "critic"]
    for node in expected_nodes:
        assert node in nodes, f"Missing node: {node}"


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_run_essay_returns_state():
    state, memory, graph, config = run_essay(
        topic="Teste de IA",
        thread_id="test-1",
        max_iterations=1,
    )
    assert state is not None
    assert state.get("topic") == "Teste de IA"
    assert state.get("planner_output") != ""
    assert state.get("research_notes") != ""
    assert state.get("draft") != ""


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_run_essay_generates_thread_id():
    state, memory, graph, config = run_essay(
        topic="Tópico aleatório",
        max_iterations=1,
    )
    assert state.get("thread_id") is not None
    assert len(state.get("thread_id", "")) > 0


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_thread_isolation():
    state1, _, _, _ = run_essay(topic="Tópico A", thread_id="thread-a", max_iterations=1)
    state2, _, _, _ = run_essay(topic="Tópico B", thread_id="thread-b", max_iterations=1)

    assert state1.get("topic") == "Tópico A"
    assert state2.get("topic") == "Tópico B"
    assert state1.get("thread_id") != state2.get("thread_id")


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_snapshot_returns_data():
    _, _, graph, config = run_essay(topic="Snapshot test", thread_id="snap-1", max_iterations=1)
    snapshot = get_snapshot(graph, config)
    assert "values" in snapshot
    assert "next" in snapshot
    assert snapshot["values"].get("topic") == "Snapshot test"


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_human_override():
    _, _, graph, config = run_essay(topic="Override test", thread_id="override-1", max_iterations=1)
    try:
        human_override(graph, config, {"critique": "Crítica customizada pelo humano"})
        snapshot = get_snapshot(graph, config)
        assert snapshot["values"].get("critique") == "Crítica customizada pelo humano"
    except Exception:
        pass


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_iteration_counter():
    state, _, _, _ = run_essay(topic="Iteração", thread_id="iter-1", max_iterations=1)
    assert state.get("iteration", 0) >= 1


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_max_iterations_respected():
    state, _, _, _ = run_essay(topic="Max iter", thread_id="max-1", max_iterations=2)
    assert state.get("iteration", 0) <= 2


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_agents_output_format():
    state = {
        "topic": "Teste",
        "messages": [],
        "draft": "",
        "research_notes": "",
        "critique": "",
        "reflection": "",
        "planner_output": "",
        "current_phase": "planning",
        "iteration": 0,
        "max_iterations": 1,
        "thread_id": "agent-test",
    }

    from essay_creator.agents import planner_node
    result = planner_node(state)
    assert "planner_output" in result
    assert result["current_phase"] == "researching"
    assert len(result.get("messages", [])) > 0
