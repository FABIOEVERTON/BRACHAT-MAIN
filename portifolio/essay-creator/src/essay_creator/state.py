from __future__ import annotations
import operator
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage


def reduce_messages(
    left: list[BaseMessage],
    right: list[BaseMessage] | list[dict],
) -> list[BaseMessage]:
    """Merge message lists using message IDs for deduplication.

    When a human updates state via update_state(), messages with the same ID
    replace existing ones instead of being appended.
    """
    left_map = {m.id: m for m in left if hasattr(m, "id") and m.id}
    right_msgs = []
    for msg in right:
        if isinstance(msg, dict):
            from langchain_core.messages import convert_from_dict
            msg = convert_from_dict(msg)
        right_msgs.append(msg)

    for msg in right_msgs:
        if hasattr(msg, "id") and msg.id:
            left_map[msg.id] = msg
        else:
            left_map[id(msg)] = msg

    return list(left_map.values())


class EssayState(TypedDict):
    topic: str
    messages: Annotated[list[BaseMessage], reduce_messages]
    draft: str
    research_notes: str
    critique: str
    reflection: str
    planner_output: str
    current_phase: Literal[
        "planning", "researching", "writing", "reflecting", "critiquing", "done"
    ]
    iteration: int
    max_iterations: int
    thread_id: str
