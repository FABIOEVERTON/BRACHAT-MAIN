#!/usr/bin/env python3
"""
[BR-EZRA-001] hermes-agent-self-evolution
Pipeline orchestrator for the 4 Hermes Agent self-evolution mechanisms.
Runs: Skill Factory -> DSPy+GEPA -> Darwinian Evolver -> Background Review -> Consolidate
"""
import json, sys, subprocess, os
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
HERMES_DIR = AGENT_DIR / "hermes_agent"
STATE_FILE = AGENT_DIR / "state.json"
SKILLS_MEMORY = AGENT_DIR / "skills_memory.json"


def python(path, *args):
    result = subprocess.run(
        [sys.executable, str(path), *args],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        print(f"WARN: {path.name} exit code {result.returncode}")
        print(f"  stderr: {result.stderr[:200]}")
    return result.stdout


def update_state(step_name, status="completed", details=""):
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            if "hermes" not in state:
                state["hermes"] = {}
            state["hermes"]["last_pipeline_run"] = datetime.now().isoformat()
            state["hermes"]["last_step"] = step_name
            if "pipeline_log" not in state["hermes"]:
                state["hermes"]["pipeline_log"] = []
            state["hermes"]["pipeline_log"].append({
                "step": step_name,
                "status": status,
                "details": details[:200],
                "timestamp": datetime.now().isoformat(),
            })
            STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
        except (json.JSONDecodeError, KeyError):
            pass


def load_skills_memory():
    try:
        return json.loads(SKILLS_MEMORY.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"hermes_loop": {}}


def save_skills_memory(data):
    SKILLS_MEMORY.write_text(json.dumps(data, indent=2) + "\n")


def main():
    steps = [
        ("skill_factory", ["skill_factory.py", "--check-failures"]),
        ("gepa_evolver", ["gepa_evolver.py"]),
        ("darwinian_evolver", ["darwinian_evolver.py"]),
        ("background_review", ["background_review.py", "review"]),
        ("consolidate_all", ["consolidate_all.py"]),
    ]

    print(f"{'='*50}")
    print(f"[BR-EZRA-001] hermes-agent-self-evolution pipeline")
    print(f"{'='*50}")

    results = {}

    for step_name, script_args in steps:
        script_path = HERMES_DIR / script_args[0]
        if not script_path.exists():
            print(f"SKIP {step_name}: {script_path} not found")
            results[step_name] = "skipped"
            continue

        args = script_args[1:]
        print(f"\n>>> {step_name}")
        try:
            output = python(script_path, *args)
            print(output[:500])
            results[step_name] = "completed"
            update_state(step_name, "completed", output[:100].strip())
        except Exception as e:
            print(f"  ERROR: {e}")
            results[step_name] = f"error: {e}"
            update_state(step_name, "error", str(e)[:100])

    print(f"\n{'='*50}")
    print("PIPELINE SUMMARY")
    for step, status in results.items():
        print(f"  {step}: {status}")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sm = load_skills_memory()
    sm.setdefault("insights", []).append({
        "date": now[:10],
        "domain": "hermes-agent-self-evolution",
        "insight": f"Pipeline executado: {sum(1 for s in results.values() if s=='completed')}/{len(steps)} steps ok",
        "occurrence": 1,
        "pattern_confidence": 0.7,
    })
    save_skills_memory(sm)

    print(f"\nhermes-agent-self-evolution pipeline complete at {now}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
