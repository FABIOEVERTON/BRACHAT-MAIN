# ECOSYSTEM RULES — BRACHÁT ASSISTANT AGENTS

## 0. HARNESS PATTERN — MANDATORY FOR EVERY AGENT

### 🧠 Central Core
* **Harness**: Central module (the "safety belt") that interconnects, controls and stabilizes the agent.
* **LLM**: Model and temperature configuration.

### ⚙️ Skills Module
* **Operational Procedure**: Operational procedures and execution flows.
* **Decision Heuristics**: Decision heuristics (logical shortcuts to solve problems).

### 🧩 Memory Module
* **Working Context**: Immediate context of the current task.
* **Episodic Experience**: History of events, successes and failures.
* **Semantic Knowledge**: Facts and concepts base.
* **Personal Memory**: User profile and agent characteristics.

### 🔗 Protocols Module
* **Agent-Agent**: Communication protocols between agents.
* **Agent-Tools**: Rules and integrations with external tools.

### ⚖️ Regulation, Evaluation and Operation Tools
* **Normative Constraints**: Ethical limits, security and unbreakable rules.
* **Sandbox**: Isolated environment for testing/actions without affecting the real environment.
* **Evaluator**: Internal evaluator that analyzes results before proceeding.
* **Approval Loop**: Approval cycle (human in the loop for critical actions).
* **Sub-Agent Orchestration**: Coordination and delegation to sub-agents.
* **Observability**: Monitoring and tracking of actions.
* **Compression**: Data/context compression to avoid token overflow.

---

## 1. LLM Hierarchy

| Layer | Agents | Reasoning | Model | T° |
|-------|---------|-----------|--------|----|
| Orchestrator | `orchestrator/` | Minimal (dispatch only) | Fast (sonnet/gpt-4o-mini) | 0 |
| Managers | `studies/*` (english, politics, philosophy, pmp, ml, certifications) | Moderate (prepare/teach) | Medium | 0.2 |
| Producers | `studies/job-hunter/`, `studies/freelancer/` | ZERO — deterministic | Any | 0 |

**Golden rule**: production agents NEVER have reasoning. They only execute fixed steps.

## 2. Agent structure

```
{category}/{name}/
├── AGENT.md      ← Agent prompt (max 60 lines)
├── {name}.md     ← Full harness file (max 60 lines)
├── cache.json    ← Recent results (max 5KB)
└── metadata.json ← Metadata (dependencies, version, author)
```

## 3. Execution contract (all agents)

- **Dashboard**: Fixed URL `http://147.15.18.252:8080`. On startup protocol, open this URL in browser and confirm HTTP 200 before any other educational or productive action. Report status in initial report.
- **Python (Phase 2)**: DAILY, 11:00-12:00. Runs in parallel with all phases. Python checkpoint is independent of others — can advance through Python blocks even if other phases are behind.
- Always load `state.json` before acting
- Never write outside the allowed directory
- Mandatory logging of each action
- Financial threshold: R$500 max without human approval
- Cross-domain: PROHIBITED without orchestrator approval
- Files <200 lines (MVI)
- Approval gate for delete/archive
- **Daily progression rule**: each day is an atomic unit. Only advance to Day N+1 when ALL items of Day N have checkpoints marked as [DELIVERED] in cache.json, confirmed by response or task pasted by the user. If the user does not complete 100% of the day, I resume exactly where they left off in the next session — without skipping, without advancing.
- English: every new vocabulary item MUST be scheduled for review at 24h, 3d, 7d, 30d and 90d (spaced repetition). The English cache.json maintains the active deck with upcoming reviews.
- Studies: every piece of content taught OR pasted by the user MUST be organized inside `writings_studies/{category}/` in the correct subfolder. Each study session generates or updates a file in the corresponding folder with: date, topic, content summary, checkpoint. Everything scheduled for review according to 24h/3d/7d/30d/90d cycle. The `estudos` cache.json maintains the pending reviews index.
- Teaching method: ALWAYS simplify for memorization. Deliver in: short topics (bullet points), tricks/mnemonics, practical examples from Fábio's context. NEVER dump long theoretical text without a summary first.
- **Portuguese (Main Study)**: sole source is the `STUDIES_BOOK` notebook from NotebookLM. Every Portuguese class day, use excerpts from the **3 books** in the notebook (Sertillanges, Kahneman, Dee Brown) in the hands-on — one excerpt from each, alternating each day. The checkpoint always requires the user to identify text type, central idea and inference for each excerpt.

## 4. Token economy

- Prompts <60 lines
- Cache replaces repeated search
- Responses <5 lines default (deepen only when asked)
- Never rewrite entire files — surgical edits
- ContextScout before any implementation
- skills-cache/index.json loaded once per session

## 5. Memory

- Single source: `/Users/mac/.opencode/state.json`
- Each agent can save cache in `{category}/{name}/cache.json`
- Cache is persistent per day (NEVER reset between sessions of the same day). Reset only on date change via orchestrator in startup protocol.

## 6. Mem0 — Selective Backup + Operational Heartbeat

Mem0 is used for TWO purposes:

### A. Strategic Backup (selective)
1. User's strategic decisions (e.g., career change, new approved project)
2. Consolidated learnings marked with `mem0: true` flag in cache
3. Jéssica's legal opinions approved by the user
4. Progress milestones (e.g., completed certification, accepted proposal)

Format: `{"type": "strategic_memory", "agent": "<name>", "content": "<summary>", "date": "<ISO>"}`

Who can send: any agent, as long as the entry has `mem0: true` flag.
Who audits: Aísio, weekly.

### B. Operational Heartbeat (every 30 min)
A lightweight heartbeat via `com.brachat.mem0-heartbeat` (launchd) that consolidates all agents' state.json summaries and writes to Mem0 API.

Purpose: enables session continuity — when a new session starts, it reads mem0 first (step 3 of startup protocol) instead of all individual state.json files. This replaces the need for daily operational memory reading of individual caches.

Format: `{"type": "heartbeat", "source": "launchd_30min", "content": "<consolidated_summary>", "date": "<ISO>"}`

Automatically removed after 7 days (TTL via API).
