import os
import json
from datetime import datetime

def consolidate_mem0_heartbeat():
    brain_state_path = os.path.expanduser("~/brachat-main/agents/brain-state.json")
    try:
        with open(brain_state_path, 'r') as f:
            brain_state = json.load(f)
    except FileNotFoundError:
        print(f"Error: brain-state.json not found at {brain_state_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in brain-state.json at {brain_state_path}")
        return

    # Get the last session summary
    if "sessions" in brain_state and len(brain_state["sessions"]) > 0:
        last_session = brain_state["sessions"][-1]
        summary_text = f"Heartbeat: {last_session["summary"]}"
        metadata = {
            "source": "mem0_heartbeat_script",
            "last_session_date": last_session["date"],
            "last_session_duration": last_session["duration"],
            "session_count": brain_state.get("session_count", 0)
        }

        # Simulate Mem0 add_memory call (replace with actual tool call in production)
        # For now, just print the payload to confirm it would work
        print(f"Simulating Mem0 add_memory call:")
        print(f"  text: {summary_text}")
        print(f"  metadata: {json.dumps(metadata, indent=2)}")

        # In a real scenario, this would be a tool call:
        # mem0_add_memory(text=summary_text, metadata=metadata, user_id="fabio_everton")
    else:
        print("No sessions found in brain-state.json to consolidate.")

if __name__ == "__main__":
    consolidate_mem0_heartbeat()
