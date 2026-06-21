# Brachat — Portfolio

**Built by AI Agent Orchestration** — Every project here was planned, executed, and delivered by the [Brachat Ecosystem](https://github.com/FABIOEVERTON/BRACHAT-MAIN) multi-agent system.

> Portfolio of productions and projects produced through **AI agent orchestration** — Ezra (orchestrator), Artur (planner), Baruch (engineer), and specialized agents working in deterministic pipeline with dual governance gate (Aísio).

---

## Projects

| Project | Type | Agents Involved | Description |
|---------|------|----------------|-------------|
| [ONE Oracle / Imersion Agent](./one_oracle/imersion_agent/) | n8n AI Agent | `opencode` + `Ezra` | HR Buddy — Virtual HR assistant built during Oracle Next Education (ONE) 2026 Imersion. Telegram + Cohere + RAG + MySQL. |

---

## How projects are made

1. **Fábio** requests → **Ezra** (orchestrator) validates via GATE_ENTRY (Aísio)
2. **Artur** writes spec → **Baruch** (Claude Code CLI) executes with Worker + QA
3. **QA** tests → **GATE_EXIT** (Aísio validates) → **Ezra** delivers
4. Output lands in `portfolio/` with `cache.json` tracking

See full architecture at [Brachat Main README](https://github.com/FABIOEVERTON/BRACHAT-MAIN).

---

## Structure

```
portfolio/
├── README.md              ← This file — project index
├── engineer/              ← Baruch (Claude Code) config
├── _bridge/               ← Dispatch scripts to engineering agents
├── tasks/                 ← Project specifications (by Artur)
└── one_oracle/            ← Oracle ONE 2026 projects
    ├── README.md          ← ONE program overview
    └── imersion_agent/    ← HR Buddy AI Agent (n8n)
```
