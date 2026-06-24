#!/usr/bin/env python3
"""Update Ezra's state.json with current session data."""
import json, sys, datetime
from pathlib import Path

EZRA_STATE = Path("agents/orchestrator_agents/ezra/state.json")
GLOBAL_STATE = Path("agents/state.json")
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).isoformat()

def load_json(p):
    return json.loads(p.read_text()) if p.exists() else {}

def save_json(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

def update_ezra_state(summary: str, session_type: str = "session"):
    state = load_json(EZRA_STATE)
    state["status"] = "idle"
    state["updated_at"] = NOW
    state.setdefault("sessions", []).append({
        "date": datetime.date.today().isoformat(),
        "type": session_type,
        "summary": summary
    })
    save_json(EZRA_STATE, state)
    print(f"[update_state] ezra state updated ({len(state['sessions'])} sessions)")

def update_global_state(summary: str, blockers: list = None, decisions: list = None, next_steps: list = None):
    state = load_json(GLOBAL_STATE)
    today = datetime.date.today().isoformat()
    last = state.get("last_session", {})
    if last.get("date") == today:
        last["summary"] = summary
        if blockers: last["blockers"] = blockers
        if decisions: last["decisions"] = decisions
        if next_steps: last["next_steps"] = next_steps
    else:
        state["last_session"] = {
            "date": today,
            "summary": summary,
            "blockers": blockers or [],
            "decisions": decisions or [],
            "next_steps": next_steps or []
        }
    state["session_count"] = state.get("session_count", 0) + 1
    state["updated_at"] = NOW
    save_json(GLOBAL_STATE, state)
    print(f"[update_state] global state updated ({state['session_count']} sessions)")

def update_context_memory(blockers: list = None, sections: dict = None):
    ctx = load_json(Path("agents/orchestrator_agents/ezra/context_memory.json"))
    if blockers is not None:
        ctx["blockers"] = blockers
    if sections:
        ctx.update(sections)
    ctx["updated_at"] = datetime.date.today().isoformat()
    save_json(Path("agents/orchestrator_agents/ezra/context_memory.json"), ctx)
    print(f"[update_state] context_memory updated")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", "-s", default="")
    parser.add_argument("--type", "-t", default="session")
    parser.add_argument("--blockers", "-b", nargs="*", default=None)
    parser.add_argument("--decisions", "-d", nargs="*", default=None)
    parser.add_argument("--next-steps", "-n", nargs="*", default=None)
    parser.add_argument("--context-sections", "-c", type=json.loads, default=None)
    args = parser.parse_args()

    if args.summary:
        update_global_state(args.summary, args.blockers, args.decisions, args.next_steps)
        update_ezra_state(args.summary, args.type)
    if args.context_sections:
        update_context_memory(args.blockers, args.context_sections)
