#!/usr/bin/env python3
"""
[BR-EZRA-001] Consolidate All Agents
Walks every agent directory, collects skills + memory into single unified JSONs,
then pushes both to mem0 as backup. Ezra owns these unified files.
"""
import json, sys, os, glob
from datetime import datetime
from pathlib import Path

BASE = Path(os.environ.get("HOME")) / "brachat-main"
HERMES_DIR = BASE / "agents" / "orchestrator_agents" / "ezra" / "hermes_agent"
UNIFIED_SKILLS = HERMES_DIR / "unified_skills.json"
UNIFIED_MEMORY = HERMES_DIR / "unified_memory.json"
HERMES_DIR.mkdir(parents=True, exist_ok=True)

AGENT_DIRS = [
    ("orchestrator", BASE / "agents" / "orchestrator_agents" / "ezra"),
    *[(d.name, d) for d in sorted((BASE / "agents" / "director_agents").iterdir()) if d.is_dir()],
    *[(d.name, d) for d in sorted((BASE / "agents" / "production_planning_agents").iterdir()) if d.is_dir()],
    *[(d.name, d) for d in sorted((BASE / "agents" / "studies_agents").iterdir()) if d.is_dir()],
    *[(d.name, d) for d in sorted((BASE / "agents" / "job").iterdir()) if d.is_dir()],
    ("baruch", BASE / "portfolio" / "engineer"),
    ("imersion_agent", BASE / "portfolio" / "one_oracle" / "imersion_agent"),
]


def read_json(path):
    try:
        if path.exists() and path.stat().st_size > 0:
            return json.loads(path.read_text())
    except (json.JSONDecodeError, Exception):
        pass
    return {}


def collect_skills():
    unified = {
        "version": 1,
        "consolidated_at": datetime.now().isoformat(),
        "source": "BR-EZRA-001 consolidate_all.py",
        "agents": {},
        "total_skills_cached": 0,
        "learned_skills_total": 0,
        "insights_total": 0,
    }

    for name, agent_dir in AGENT_DIRS:
        if not agent_dir.exists():
            continue

        agent_data = {"name": name, "path": str(agent_dir)}

        sm = read_json(agent_dir / "skills_memory.json")
        if sm:
            agent_data["skills_memory"] = {
                "learned_skills": sm.get("learned_skills", []),
                "insights": sm.get("insights", []),
                "hermes_loop": sm.get("hermes_loop", {}),
            }
            unified["learned_skills_total"] += len(sm.get("learned_skills", []))
            unified["insights_total"] += len(sm.get("insights", []))

        cache_dir = agent_dir / "cache_skills"
        cached_skills = []
        if cache_dir.exists():
            for skill_dir in sorted(cache_dir.iterdir()):
                if skill_dir.is_dir():
                    skill_md = skill_dir / "SKILL.md"
                    cached_skills.append({
                        "name": skill_dir.name,
                        "has_skill_md": skill_md.exists(),
                        "file_count": len(list(skill_dir.iterdir())) if skill_dir.exists() else 0,
                        "path": str(skill_dir),
                    })
        agent_data["cached_skills"] = cached_skills
        unified["total_skills_cached"] += len(cached_skills)

        unified["agents"][name] = agent_data

    return unified


def collect_memory():
    unified = {
        "version": 1,
        "consolidated_at": datetime.now().isoformat(),
        "source": "BR-EZRA-001 consolidate_all.py",
        "agents": {},
        "total_agents_with_state": 0,
        "total_agents_with_cache": 0,
    }

    for name, agent_dir in AGENT_DIRS:
        if not agent_dir.exists():
            continue

        agent_data = {"name": name, "path": str(agent_dir)}

        state = read_json(agent_dir / "state.json")
        if state:
            agent_data["state"] = state
            unified["total_agents_with_state"] += 1

        cache = read_json(agent_dir / "cache.json")
        if cache:
            agent_data["cache"] = cache
            unified["total_agents_with_cache"] += 1

        unified["agents"][name] = agent_data

    return unified


def save_unified(data, path):
    path.write_text(json.dumps(data, indent=2) + "\n")
    size_kb = path.stat().st_size / 1024
    return size_kb


def mem0_summary(unified_skills, unified_memory):
    agents_skills = list(unified_skills["agents"].keys())
    agents_memory = list(unified_memory["agents"].keys())

    summary = (
        f"[BR-EZRA-001] Unified consolidation push. "
        f"Skills: {unified_skills['total_skills_cached']} cached, "
        f"{unified_skills['learned_skills_total']} learned, "
        f"{unified_skills['insights_total']} insights across "
        f"{len(agents_skills)} agents. "
        f"Memory: {unified_memory['total_agents_with_state']} states, "
        f"{unified_memory['total_agents_with_cache']} caches across "
        f"{len(agents_memory)} agents."
    )
    return summary


def main():
    print(f"[BR-EZRA-001] Consolidating all agents...")

    skills = collect_skills()
    sk_size = save_unified(skills, UNIFIED_SKILLS)
    print(f"  unified_skills.json: {sk_size:.1f}KB, {skills['total_skills_cached']} cached, {skills['learned_skills_total']} learned, {skills['insights_total']} insights")

    memory = collect_memory()
    mem_size = save_unified(memory, UNIFIED_MEMORY)
    print(f"  unified_memory.json: {mem_size:.1f}KB, {memory['total_agents_with_state']} states, {memory['total_agents_with_cache']} caches")

    summary = mem0_summary(skills, memory)
    print(f"\n  Mem0 summary: {summary}")

    print(f"\n  Done. Files ready for mem0 push.")
    return summary


if __name__ == "__main__":
    summary = main()
    print(summary)
