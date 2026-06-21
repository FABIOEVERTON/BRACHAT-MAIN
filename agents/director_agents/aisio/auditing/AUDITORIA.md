## ⚠️ ABSOLUTE RULE
FORBIDDEN TO EXECUTE ANY TASK NOT DESCRIBED IN THIS FILE

# General Audit — Sunday 06/06

## 1. Directory Structure

- [ ] `assistant_agents/` contains only: `.apis/`, `.config/`, `.opencode/`, `daily/`(12), `directors/`(5), `orquestrador/`, `shared/`, `skills-cache/`, `state.json`, `metadata.json`, `REGRAS.md`, `README.md`, `LICENSE`, `requirements.txt`
- [ ] `shared/` is a single copy (no duplicate in `substracts/` or elsewhere)
- [ ] `daily/` has exactly 12 agent folders, each with `AGENT.md`, `cache.json`, `metadata.json`
- [ ] `directors/` has exactly 5 folders, each with `AGENT.md`, `cache.json` (+ `metadata.json` for Nice)
- [ ] `orquestrador/` has `AGENT.md` and `cache.json`
- [ ] No stray `substracts/` or `__pycache__` directories

## 2. state.json (Canonical)

- [ ] `assistant_agents/state.json` exists and is valid (JSON)
- [ ] `metadata.json` points to the correct path: `"state_path": "assistant_agents/state.json"`
- [ ] `orquestrador/AGENT.md` reference updated
- [ ] `.opencode/agent/orquestrador.md` reference updated
- [ ] state.json content reflects real state (agents, launchd, communication, etc.)

## 3. Agents — Complete Harness (5 Modules)

### Orquestrador (1)
- [ ] `orquestrador/AGENT.md`: Core, Skills, Memory, Protocols, Regulation

### Directors (5)
- [ ] `directors/josue/AGENT.md` — 5 modules
- [ ] `directors/gilmario/AGENT.md` — 5 modules
- [ ] `directors/aisio/AGENT.md` — 5 modules
- [ ] `directors/jessica/AGENT.md` — 5 modules
- [ ] `directors/nice/AGENT.md` — 5 modules

### Daily Agents (12)
- [ ] `daily/ingles/AGENT.md` — 5 modules
- [ ] `daily/politica/AGENT.md` — 5 modules
- [ ] `daily/filosofia/AGENT.md` — 5 modules
- [ ] `daily/certificacoes/AGENT.md` — 5 modules
- [ ] `daily/google-skills/AGENT.md` — 5 modules
- [ ] `daily/python/AGENT.md` — 5 modules
- [ ] `daily/pmp/AGENT.md` — 5 modules
- [ ] `daily/ml-engineer/AGENT.md` — 5 modules
- [ ] `daily/job-hunter/AGENT.md` — 5 modules
- [ ] `daily/freelancer/AGENT.md` — 5 modules
- [ ] `daily/portfolio/AGENT.md` — 5 modules
- [ ] `daily/nice/AGENT.md` — (still exists in daily/ even with copy in directors/)

## 4. Launchd Services

- [ ] `com.brachat.opencode` — EZRA Telegram bridge (active PID)
- [ ] `com.brachat.nice` — Nice Telegram bridge (active PID)
- [ ] `com.brachat.antigravity` — WhatsApp bridge (status OK)
- [ ] `com.brachat.clickup` — ClickUp sync (status OK)
- [ ] All with `KeepAlive=true` and `RunAtLoad=true`
- [ ] Plists point to `assistant_agents/shared/general_scripts/` (no longer `substracts/`)

## 5. Telegram Bridges — Response Test

### EZRA (@Baruch_Everton_bot)
- [ ] Bridge responds in <3s (direct API, no subprocess)
- [ ] Sent message receives coherent response
- [ ] Logs in `/tmp/telegram-bridge.log` active

### Nice (@luevertonbot)
- [ ] Bridge responds in <3s
- [ ] Sent message receives coherent response (Nice persona)
- [ ] Logs active

## 6. Active Connections

- [ ] Telegram (EZRA) — chat Fábio: `8035491919`
- [ ] Telegram (Nice) — chat Dona Lu: `8722951907`
- [ ] ClickUp — connected workspace (Composio)
- [ ] LinkedIn — connected (Composio)
- [ ] WhatsApp (Baileys) — server on port 3456

## 7. Cache.json — Each Agent

- [ ] `orquestrador/cache.json` valid
- [ ] `directors/*/cache.json` valid (5)
- [ ] `daily/*/cache.json` valid (12)
- [ ] `daily/nice/cache.json` (duplicate with directors/nice/ — decide which to keep)

## 8. Skills and Scripts

- [ ] `shared/general_scripts/telegram-bridge.py` — direct API, no subprocess
- [ ] `shared/general_scripts/nice-telegram-bridge.py` — direct API + broadcast
- [ ] `shared/general_harness/` — template harness available
- [ ] `shared/general_skills/` — skills catalog (1,480 dirs)

## 9. Decision Points

- [ ] `daily/nice/` vs `directors/nice/` — remove duplicate from `daily/`
- [ ] `directors/aisio|gilmario|jessica|josue` without `metadata.json` — create or remove dependency
- [ ] WhatsApp Baileys — port 3456 still relevant? Keep or turn off?
- [ ] Old logs in `/tmp/*.log` — clean up

---

**Run:** Sunday, step by step, check each item.
**Criteria:** 100% of each agent and connection verified — no assumptions.
