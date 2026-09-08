import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from .state import EssayState
from .agents import (
    planner_node,
    researcher_node,
    writer_node,
    reflector_node,
    critic_node,
)


def should_continue(state: EssayState) -> str:
    phase = state.get("current_phase", "done")
    if phase == "done":
        return END
    return phase


def build_workflow(db_path: str = ":memory:"):
    """Build the essay creator workflow with SQLite persistence.

    Args:
        db_path: SQLite database path. Use ":memory:" for in-memory.

    Returns:
        Tuple of (compiled_graph, memory_checkpointer)
    """
    graph = StateGraph(EssayState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("reflector", reflector_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("planner")

    graph.add_conditional_edges("planner", should_continue, {
        "researching": "researcher",
        END: END,
    })
    graph.add_conditional_edges("researcher", should_continue, {
        "writing": "writer",
        END: END,
    })
    graph.add_conditional_edges("writer", should_continue, {
        "reflecting": "reflector",
        END: END,
    })
    graph.add_conditional_edges("reflector", should_continue, {
        "critiquing": "critic",
        END: END,
    })
    graph.add_conditional_edges("critic", should_continue, {
        "writing": "writer",
        END: END,
    })

    conn = sqlite3.connect(db_path, check_same_thread=False)
    memory = SqliteSaver(conn)

    compiled = graph.compile(
        checkpointer=memory,
        interrupt_before=["critic"],
    )

    return compiled, memory


def run_essay(topic: str, thread_id: str | None = None, max_iterations: int = 3):
    """Run the essay creation workflow.

    Args:
        topic: Essay topic
        thread_id: Unique session identifier. Generated if None.
        max_iterations: Max write-reflect-critique cycles.

    Returns:
        Tuple of (final_state_dict, memory, graph, config)
    """
    import uuid

    if thread_id is None:
        thread_id = str(uuid.uuid4())

    graph, memory = build_workflow()

    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "topic": topic,
        "messages": [],
        "draft": "",
        "research_notes": "",
        "critique": "",
        "reflection": "",
        "planner_output": "",
        "current_phase": "planning",
        "iteration": 0,
        "max_iterations": max_iterations,
        "thread_id": thread_id,
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
