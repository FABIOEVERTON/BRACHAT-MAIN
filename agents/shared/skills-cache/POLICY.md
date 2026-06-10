# Skills Cache — Token Economy Policy

## Principle
1,465 skills available (312MB). Zero loaded in context by default.

## Rules
1. **ALWAYS load**: `skills-cache/active-index.json` (~4KB) — category names + descriptions for searching.
2. **NEVER load**: `skills-cache/master-index.json` (549KB) or any `SKILL.md` unless explicitly needed for current task.
3. **On demand per agent**:
   - Check `{category}/{agent}/cache_skills/` first
   - Search `active-index.json` for matching category
   - grep `master-index.json` for exact skill name → get path
   - Read ONLY the specific `skills-cache/general_skills/<name>/SKILL.md`
   - Cache a copy in `cache_skills/` for next time
   - Discard from context after use
4. **Governance**: `shared/governance/` — loaded at session start.

## Decision pipeline
```
Task arrives → check cache_skills/ → found? → use it
  → NOT found → search active-index.json → grep master-index.json
  → read specific SKILL.md → use → cache locally
```
