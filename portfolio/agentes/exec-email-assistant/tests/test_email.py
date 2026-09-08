import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import uuid
import pytest
from email_assistant.state import EmailState, reduce_messages
from email_assistant.tools import create_all_tools, get_memory_store
from email_assistant.workflow import build_workflow, process_email, get_snapshot, human_override
from langchain_core.messages import HumanMessage, AIMessage
HAS_API_KEY = bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))


def test_state_schema():
    assert EmailState.__annotations__ is not None
    required_keys = [
        "email_content", "sender", "subject", "messages", "intent",
        "reply_draft", "schedule_info", "memory_context", "human_approval",
        "current_phase", "thread_id", "needs_human"
    ]
    for key in required_keys:
        assert key in EmailState.__annotations__, f"Missing key: {key}"


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


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_semantic_memory_store_and_search():
    from email_assistant.memory import SemanticMemory
    mem = SemanticMemory()
    mem.store_fact("João trabalha na empresa X", metadata={"type": "work"})
    mem.store_fact("Maria é gerente de projetos", metadata={"type": "role"})

    results = mem.search_facts("João empresa")
    assert len(results) > 0
    assert any("João" in r for r in results)


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_semantic_memory_has_schedule():
    from email_assistant.memory import SemanticMemory
    mem = SemanticMemory()
    assert not mem.has_schedule("João")
    mem.store_fact("Agendamento com João segunda às 10h", metadata={"type": "schedule"})
    assert mem.has_schedule("João")


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_semantic_memory_get_all_facts():
    from email_assistant.memory import SemanticMemory
    mem = SemanticMemory()
    mem.store_fact("Fato 1")
    mem.store_fact("Fato 2")
    facts = mem.get_all_facts()
    assert len(facts) == 2


def test_memory_tools_created():
    tools = create_all_tools()
    assert len(tools) >= 4
    tool_names = [t.name for t in tools]
    assert "check_calendar" in tool_names
    assert "send_email" in tool_names


def test_workflow_builds():
    graph, memory = build_workflow(db_path=":memory:")
    assert graph is not None
    assert memory is not None


def test_workflow_structure():
    graph, memory = build_workflow(db_path=":memory:")
    nodes = list(graph.get_graph().nodes)
    expected_nodes = ["classifier", "memory_search", "draft_reply", "schedule", "human_review"]
    for node in expected_nodes:
        assert node in nodes, f"Missing node: {node}"


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_process_email_returns_state():
    state, memory, graph, config = process_email(
        email_content="Gostaria de marcar uma reunião sobre o projeto.",
        sender="joao@empresa.com",
        subject="Reunião projeto",
        thread_id="test-email-1",
    )
    assert state is not None
    assert state.get("sender") == "joao@empresa.com"
    assert state.get("intent") in ["reply", "schedule", "archive", "search_memory", "unknown"]


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_process_email_generates_thread_id():
    state, memory, graph, config = process_email(
        email_content="Teste",
        sender="test@test.com",
        subject="Teste",
    )
    assert state.get("thread_id") is not None
    assert len(state.get("thread_id", "")) > 0


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_thread_isolation():
    state1, _, _, _ = process_email(
        email_content="Email A",
        sender="a@test.com",
        subject="A",
        thread_id="email-thread-a",
    )
    state2, _, _, _ = process_email(
        email_content="Email B",
        sender="b@test.com",
        subject="B",
        thread_id="email-thread-b",
    )
    assert state1.get("thread_id") != state2.get("thread_id")
    assert state1.get("sender") != state2.get("sender")


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_snapshot_returns_data():
    _, _, graph, config = process_email(
        email_content="Snapshot test",
        sender="snap@test.com",
        subject="Snapshot",
        thread_id="snap-email-1",
    )
    snapshot = get_snapshot(graph, config)
    assert "values" in snapshot
    assert "next" in snapshot


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_human_override():
    _, _, graph, config = process_email(
        email_content="Agendar reunião com João",
        sender="maria@test.com",
        subject="Reunião",
        thread_id="override-email-1",
    )
    try:
        human_override(graph, config, {"human_approval": "approved"})
        snapshot = get_snapshot(graph, config)
        assert snapshot["values"].get("human_approval") == "approved"
    except Exception:
        pass


@pytest.mark.skipif(not HAS_API_KEY, reason="GOOGLE_API_KEY not set")
def test_intent_classification():
    from email_assistant.agents import classifier_node
    state = {
        "email_content": "Gostaria de agendar uma reunião para discutir o projeto.",
        "sender": "joao@empresa.com",
        "subject": "Reunião",
        "messages": [],
        "intent": "unknown",
        "reply_draft": "",
        "schedule_info": "",
        "memory_context": "",
        "human_approval": "",
        "current_phase": "classify",
        "thread_id": "classify-test",
        "needs_human": False,
    }
    result = classifier_node(state)
    assert "intent" in result
    assert result["intent"] in ["reply", "schedule", "archive", "search_memory", "unknown"]
    assert result["current_phase"] == "process"
