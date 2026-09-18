import sqlite3
import uuid
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .state import EmailState
from .agents import (
    classifier_node,
    draft_reply_node,
    schedule_node,
    memory_search_node,
    human_review_node,
)


def route_intent(state: EmailState) -> str:
    """Route to the appropriate node based on email intent."""
    intent = state.get("intent", "unknown")
    phase = state.get("current_phase", "classify")

    if phase == "done":
        return END

    if phase == "human_review":
        return "human_review"

    routes = {
        "reply": "draft_reply",
        "schedule": "schedule",
        "archive": END,
        "search_memory": "memory_search",
        "unknown": "draft_reply",
    }

    return routes.get(intent, "draft_reply")


def build_workflow(db_path: str = ":memory:"):
    """Build the email assistant workflow with SQLite persistence.

    Args:
        db_path: SQLite database path. Use ":memory:" for in-memory.

    Returns:
        Tuple of (compiled_graph, memory_checkpointer)
    """
    graph = StateGraph(EmailState)

    graph.add_node("classifier", classifier_node)
    graph.add_node("memory_search", memory_search_node)
    graph.add_node("draft_reply", draft_reply_node)
    graph.add_node("schedule", schedule_node)
    graph.add_node("human_review", human_review_node)

    graph.set_entry_point("classifier")

    graph.add_conditional_edges("classifier", route_intent, {
        "draft_reply": "draft_reply",
        "schedule": "schedule",
        "memory_search": "memory_search",
        "human_review": "human_review",
        END: END,
    })

    graph.add_edge("memory_search", "draft_reply")
    graph.add_edge("schedule", "human_review")
    graph.add_edge("human_review", END)
    graph.add_edge("draft_reply", END)

    conn = sqlite3.connect(db_path, check_same_thread=False)
    memory = SqliteSaver(conn)

    compiled = graph.compile(
        checkpointer=memory,
        interrupt_before=["human_review"],
    )

    return compiled, memory


def process_email(
    email_content: str,
    sender: str,
    subject: str,
    thread_id: str | None = None,
):
    """Process an email through the workflow.

    Args:
        email_content: Email body text
        sender: Sender email/name
        subject: Email subject
        thread_id: Unique session identifier. Generated if None.

    Returns:
        Tuple of (final_state_dict, memory, graph, config)
    """
    if thread_id is None:
        thread_id = str(uuid.uuid4())

    graph, memory = build_workflow()
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "email_content": email_content,
        "sender": sender,
        "subject": subject,
        "messages": [],
        "intent": "unknown",
        "reply_draft": "",
        "schedule_info": "",
        "memory_context": "",
        "human_approval": "",
        "current_phase": "classify",
        "thread_id": thread_id,
        "needs_human": False,
    }

    final_state = graph.invoke(initial_state, config)

    return final_state, memory, graph, config


def get_snapshot(graph, config):
    """Get a snapshot of the current state for HITL inspection."""
    snapshot = graph.get_state(config)
    return {
        "values": snapshot.values,
        "next": snapshot.next,
        "config": snapshot.config,
        "metadata": snapshot.metadata,
        "created_at": snapshot.created_at,
        "tasks": [str(t) for t in snapshot.tasks],
    }


def human_override(graph, config, updates: dict):
    """Apply human overrides to the paused state.

    Args:
        graph: Compiled graph
        config: Thread config
        updates: Dict of state fields to override

    Returns:
        Updated state after human intervention
    """
    graph.update_state(config, updates)
    return graph.invoke(None, config)
