#!/usr/bin/env python3
"""
[BR-EZRA-001] Skill Factory
Identifies complex tasks solved successfully and packages them as SKILL.md.
Part of the Hermes Agent self-evolution system.
"""
import json, sys, os, re, hashlib
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
SKILL_POOL = Path(os.environ.get("HOME")) / "brachat-main" / "agents" / "shared" / "general_skills"
CACHE_SKILLS = AGENT_DIR / "cache_skills"
SKILLS_MEMORY = AGENT_DIR / "skills_memory.json"
STATE_MEMORY = AGENT_DIR / "context_memory.json"
INDEX_FILE = Path(os.environ.get("HOME")) / "brachat-main" / "agents" / "skills-cache" / "active-index.json"

SKILL_TEMPLATE = """---
name: {name}
description: "{description}"
risk: safe
source: skill-factory
date_added: "{date}"
---

# {title}

## Origin
- **Task**: {task_summary}
- **Created by**: Skill Factory (BR-EZRA-001)
- **Evolution marker**: <!-- Evolution: {date} | source: skill-factory | agent: ezra -->

## When to Use
{when_to_use}

## Procedure
{procedure}

## Verification
{verification}
"""


def load_skills_memory():
    try:
        return json.loads(SKILLS_MEMORY.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"learned_skills": [], "insights": [], "hermes_loop": {}, "version": 1}


def save_skills_memory(data):
    SKILLS_MEMORY.write_text(json.dumps(data, indent=2) + "\n")


def slugify(name):
    return re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-"))[:60]


def skill_exists_in_pool(name):
    if (SKILL_POOL / slugify(name)).exists():
        return True
    if (CACHE_SKILLS / slugify(name)).exists():
        return True
    memory = load_skills_memory()
    return any(s["name"] == slugify(name) for s in memory["learned_skills"])


def create_skill(name, description, title, task_summary, when_to_use, procedure, verification):
    slug = slugify(name)
    out_dir = CACHE_SKILLS / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    content = SKILL_TEMPLATE.format(
        name=slug,
        description=description[:200],
        date=datetime.now().strftime("%Y-%m-%d"),
        title=title,
        task_summary=task_summary.strip(),
        when_to_use=when_to_use.strip(),
        procedure=procedure.strip(),
        verification=verification.strip(),
    )

    skill_path = out_dir / "SKILL.md"
    skill_path.write_text(content)

    return skill_path


def update_skills_memory(name, description, task_summary, confidence=0.7):
    data = load_skills_memory()
    slug = slugify(name)

    existing = [s for s in data["learned_skills"] if s["name"] == slug]
    if existing:
        existing[0]["occurrence"] += 1
        existing[0]["pattern_confidence"] = min(1.0, existing[0]["pattern_confidence"] + 0.1)
        existing[0]["last_applied"] = datetime.now().isoformat()
        existing[0]["cache_status"] = "cached"
    else:
        data["learned_skills"].append({
            "name": slug,
            "learned_at": datetime.now().strftime("%Y-%m-%d"),
            "source": "skill-factory",
            "applied_to": task_summary,
            "pattern_confidence": confidence,
            "occurrence": 1,
            "cache_status": "cached",
            "description": description[:200],
        })

    data["insights"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "domain": "skill-factory",
        "insight": f"Skill Factory criou skill '{slug}': {task_summary[:100]}",
        "occurrence": len(existing) + 1 if not existing else existing[0]["occurrence"],
    })

    save_skills_memory(data)
    return slug


def main():
    if len(sys.argv) < 5:
        print("USAGE: skill_factory.py <name> <title> <task_summary_file> <procedure_file>")
        print("  Creates a SKILL.md from a solved task.")
        sys.exit(1)

    name = sys.argv[1]
    title = sys.argv[2]
    task_summary = Path(sys.argv[3]).read_text().strip()
    procedure = Path(sys.argv[4]).read_text().strip()

    if skill_exists_in_pool(name):
        print(f"SKIP: Skill '{name}' already exists in pool or cache.")
        sys.exit(0)

    description = title
    when_to_use = f"Use this skill when: {task_summary[:300]}"
    verification = "1. Test the procedure works in a fresh environment\n2. Verify each step produces expected output\n3. Log results to cache.json"

    skill_path = create_skill(name, description, title, task_summary, when_to_use, procedure, verification)
    slug = update_skills_memory(name, description, task_summary)

    print(f"SKILL CREATED: {skill_path}")
    print(f"REGISTERED: skills_memory.json[{slug}]")
    print(f"STATUS: cached in cache_skills/{slug}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
