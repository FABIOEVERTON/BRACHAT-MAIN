<div align="center">
  <h1>BRACHÁT ECOSYSTEM</h1>
  <p><strong>Personal AI Operating System & Multi-Agent Network</strong></p>
  <p>English · Temperature Zero · Deterministic</p>
</div>

---

**BRACHÁT** is an autonomous, private ecosystem of Artificial Intelligence agents designed to govern daily routine, software engineering, financial automation, certification studies, and knowledge management. Every action goes through a **dual governance gate** (Aísio validates before and after) and is orchestrated by a central intelligence (Ezra).

---

## System Architecture

```
Fábio → Ezra (Orchestrator)
          ↓
     GATE_ENTRY (Aísio validates)
          ↓
     ┌────┴────┐
     │         │
  Directors  Production
  ┌──┴──┐    ┌──┴──┐
  Nice  │    │  Artur (Planner)
  Jessica│   │    ↓
  Gilmario│  │  GATE_AÍSIO
  Josué  │   │    ↓
     │   │   Baruch (Terminal)
     │   │    ↓
     │   │  Worker + QA code
     │   │    ↓
     └───┴────┘
          ↓
     GATE_EXIT (Aísio validates)
          ↓
       Ezra delivers
```

### Deterministic code flow
1. **Fábio** → demand to **Ezra**
2. **Ezra** → validates at **GATE_ENTRY** (reads governance.md + ledger)
3. **Ezra** → passes to **Artur** to write spec at `/portfolio/tasks/[project].md`
4. **Artur** → **Baruch** via bridge (`dispatch_to_baruch.sh` — terminal with Claude Code CLI)
5. **Baruch** → creates **Worker** (BR-OP-xx-001) + **QA** (BR-OP-xx-QA) + `cache.json` + code + tests
6. **QA** tests → **Baruch** reports → **GATE_EXIT** (Aísio validates) → **Ezra** delivers

---

## Agents

| ID | Agent | Role |
|----|-------|------|
| BR-EZRA-001 | **Ezra** | Central Orchestrator — sole interface with Fábio, 14 mandatory checks, state.json + Mem0 memory |
| BR-AISIO-010 | **Aísio** | Governance Director — enforces U1-U11 rules, dual gate on every action, immutable ledger |
| BR-NICE-002 | **Nice** | Domestic Director — routine, bills, reminders |
| BR-JESSIC-012 | **Jéssica** | Legal Director — LGPD, contracts, regulatory risk |
| BR-GILMAR-004 | **Gilmário** | Education Director — studies, schedule, certifications |
| BR-JOSUE-005 | **Josué** | Commercial Director — sales, OLX (via Playwright on VM) |
| BR-ARTUR-006 | **Artur** | Production Planner — writes specs, dispatches to Baruch |
| BR-BARUCH-003 | **Baruch** | Software Engineer — codes via Claude Code CLI in terminal, worker + QA |
| BR-JUSTUS | **Justus** | Job Hunter — searches and applies to jobs via Gmail |

---

## Portfolio (Agent-Delivered Projects)

Projects built end-to-end by the Brachat multi-agent system. See [`portfolio/README.md`](./portfolio/README.md) for the full showcase.

| Project | Type | Status |
|---------|------|--------|
| [ONE Imersion Agent](./portfolio/one_oracle/imersion_agent/) | n8n AI Agent (HR Buddy) | ✅ Complete |

---

## Studies & Certifications

6 certification tracks in weekly rotation + Oracle ONE program:
1. **OCI Foundations** (Seg)
2. **OCI AI Foundations** (Ter)
3. **OCI GenAI Pro** (Qua)
4. **OCI Architect Pro** (Qui)
5. **OCI Multicloud Pro** (Sex)
6. **AIGP** (Sáb)

Schedule: `agents/studies_agents/materials/SCHEDULE_FULL.md` — 138 days, ONE + Certs + Concurso integrados. Progress at `schedule_progress.json`.

---

## Governance (U1-U11 Rules)

All system rules centralized in `agents/director_agents/aisio/governance.md` — single source of truth:

| # | Rule | Description |
|---|------|-------------|
| U1 | **MVI** | No file >200 lines |
| U2 | **Temperature zero** | Every agent `temperature: 0.0` |
| U3 | **No secrets** | No key/token hardcoded |
| U4 | **Mandatory tests** | All new code must have automated tests |
| U5 | **Financial HITL** | >R$500 requires human approval |
| U6 | **Destructive HITL** | Delete/overwrite/infra require approval |
| U7 | **Cross-domain** | Only with orchestrator permission |
| U8 | **Traceability** | Every log/commit starts with `[BR-ID]` |
| U9 | **Self-review** | Agent reviews own output before delivering |
| U10 | **Immutable ledger** | Every action logged in `governance-ledger.jsonl` |
| U11 | **English only** | All agents, prompts, logs, commits in English |

---

## Infrastructure

### Local (macOS)
- **LLM Proxy**: `clampproxy` on port 4000
- **OpenCode**: port 8080 (Zen API)
- **Mem0**: MCP server (offline — key needs renewal)
- **launchd daemons**: Ezra bridge (Telegram → Zen API), Nice bridge
- **n8n**: low-code automations

### Cloud
- **VM Oracle** (147.15.0.196): 24/7 services (Ezra, Nice, ClickUp)
- **VPS Hetzner**: alternative for bridges

### Baruch (Claude Code CLI)
- `alias claudecode` → `ANTHROPIC_BASE_URL=http://localhost:4000 /Users/mac/.local/bin/claude`
- Workspace: `/portfolio/`
- Rules injected via `portfolio/engineer/CLAUDE.md`
- Bridge: `portfolio/_bridge/dispatch_to_baruch.sh`

---

## Directory Structure

```
brachat-main/
├── .cloud/                  ← Daemons launchd, scripts, dashboard
├── .opencode/               ← OpenCode config + governance-ledger
├── agents/
│   ├── orchestrator_agents/ezra/  ← Ezra (orchestrator + state)
│   ├── director_agents/           ← Aísio, Nice, Jéssica, Gilmário, Josué
│   ├── production_planning_agents/artur/ ← Artur (planner)
│   ├── job/justus/               ← Justus (job hunter)
│   ├── studies_agents/           ← Materials, schedule, certifications
│   └── shared/                   ← Skills library (+1400 skills)
├── portfolio/                ← 🎯 Projects delivered by agent orchestration
│   ├── README.md             ← Project index & showcase
│   ├── engineer/             ← Baruch (CLAUDE.md + persona)
│   ├── _bridge/              ← Dispatch script to Baruch
│   ├── tasks/                ← Project specs
│   └── one_oracle/           ← Oracle ONE 2026 projects
├── integrations/             ← SSH keys, APIs
├── docs/                     ← Assets, documentation
├── cloud/                    ← VPS deploy configs
└── n8n/                      ← Low-code automations
```

---

## Known Blockers

- **Mem0 MCP offline** — key changed, awaiting restart
- **Playwright+Chromium** — not installed on Oracle VM (blocks Josué)
- **Badge cache** — AWS AI Practitioner shows "not_started" (outdated)
- **LinkedIn** — security challenge blocks ~60% of jobs
- **Job portals** — Gupy, Workable, Greenhouse blocked
- **50% of agents** — empty cache (never activated)

---

*Ecosystem governed locally via AI Agent Specification. Temperature 0.0. Deterministic.*
