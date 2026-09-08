from __future__ import annotations
import operator
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field


def reduce_messages(
    left: list[BaseMessage],
    right: list[BaseMessage] | list[dict],
) -> list[BaseMessage]:
    """Merge message lists using message IDs for deduplication."""
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


class EmailState(TypedDict):
    email_content: str
    sender: str
    subject: str
    messages: Annotated[list[BaseMessage], reduce_messages]
    intent: Literal["reply", "schedule", "archive", "search_memory", "unknown"]
    reply_draft: str
    schedule_info: str
    memory_context: str
    human_approval: str
    current_phase: Literal[
        "classify", "process", "draft_reply", "schedule", "human_review", "done"
    ]
    thread_id: str
    needs_human: bool


class ClassificationOutput(BaseModel):
    intent: str = Field(description="Classified intent: reply, schedule, archive, search_memory, unknown")
    confidence: float = Field(ge=0.0, le=1.0, description="Classification confidence")


class ScheduleOutput(BaseModel):
    person: str = Field(description="Person to schedule with")
    date: str = Field(description="Suggested date")
    duration: str = Field(description="Estimated duration")
    purpose: str = Field(description="Meeting purpose")


class ReplyOutput(BaseModel):
    greeting: str = Field(description="Professional greeting")
    body: str = Field(description="Reply body")
    closing: str = Field(description="Professional closing")
