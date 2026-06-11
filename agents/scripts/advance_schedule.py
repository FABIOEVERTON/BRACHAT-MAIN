#!/usr/bin/env python3
import json
import os
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).parent.parent.parent
SCHEDULE_FILE = BASE_DIR / "agents" / "orchestrator_agent" / "schedule_progress.json"

def main():
    if not SCHEDULE_FILE.exists():
        print(f"File not found: {SCHEDULE_FILE}")
        return

    with open(SCHEDULE_FILE, "r") as f:
        data = json.load(f)

    today = datetime.now(timezone.utc).isoformat()
    current_day = data.get("current_day", 0)
    
    data["days_completed"].append({
        "day": current_day,
        "completed_at": today
    })
    
    data["current_day"] = current_day + 1
    data["last_updated"] = today

    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"Schedule advanced. Now on Day {data['current_day']}.")

if __name__ == "__main__":
    main()
