# Agent Nice — Household Governance Agent

**Runtime governance for domestic operations with self-evolution, approval gates, and kashrut compliance.**

## What It Does

Agent Nice is a domestic governance agent that manages household tasks with the same rigor as enterprise AI systems. It enforces financial approval gates, kashrut dietary compliance, and self-evolves through a 4-stage learning pipeline (Hermes Agent).

## Architecture

```mermaid
graph TD
    subgraph "Agent Core (BR-NICE-014)"
        NICE[Agent Nice<br/>nice.md persona]
        CACHE[cache.json<br/>session state]
        CTX[context_memory.json<br/>learned preferences]
        STATE[state.json<br/>agent lifecycle]
    end

    subgraph "Governance Gates"
        G1{≤ R$100?<br/>Auto approve}
        G2{R$101–500?<br/>Dona Lu approval}
        G3{> R$500?<br/>CEO Fábio approval}
        NICE --> G1
        G1 -->|No| G2
        G2 -->|No| G3
    end

    subgraph "Operational Data"
        SHOP[shopping_list.json<br/>pending purchases]
        PANTRY[pantry.json<br/>current inventory]
        FIN[finance.json<br/>account balance]
        CACHE --> SHOP
        CACHE --> PANTRY
        CACHE --> FIN
    end

    subgraph "Hermes Self-Evolution Pipeline"
        SF[Skill Factory<br/>packages tasks as SKILL.md]
        GEPA[GEPA Evolver<br/>LLM-guided prompt mutations]
        DAR[Darwinian Evolver<br/>fitness-based selection]
        BG[Background Review<br/>preference extraction]

        SF --> GEPA --> DAR --> BG
        BG -->|insights| STATE
    end

    subgraph "External"
        LU[Dona Lu<br/>Telegram approval]
        FABIO[CEO Fábio<br/>escalation]
        EZRA[EZRA<br/>consolidation to mem0]
    end

    G2 -->|notify| LU
    G3 -->|escalate| FABIO
    STATE -->|memory feed| EZRA
```

## How It Works

1. **CHECK** — Reads `cache.json` and all integration files (shopping, pantry, finance).
2. **SKILL CACHE** — Retrieves needed skills from `shared/general_skills/` and copies to `cache_skills/`.
3. **PLAN** — Organizes agenda, checks commitments, verifies pantry, compares prices.
4. **KASHRUT CHECK** — Audits grocery items for banned substances (carmine/E120, pork, bacon, ham, gelatin). Strictly blocks or warns.
5. **DECIDE & CONTACT** — Applies financial heuristics. Contacts Dona Lu or CEO as needed.
6. **LOG** — Registers expenses and tasks in `cache.json` and internal JSON files.

## Hermes Self-Evolution

```mermaid
flowchart LR
    subgraph "Pipeline (hermes_agent_self_evolution.py)"
        S1[Skill Factory<br/>identify + package] --> S2[GEPA Evolver<br/>prompt mutations]
        S2 --> S3[Darwinian Evolver<br/>fitness selection]
        S3 --> S4[Background Review<br/>preference extraction]
    end

    subgraph "Output"
        SK[cache_skills/<br/>learned SKILL.md files]
        SM[skills_memory.json<br/>pattern confidence]
        CTX2[context_memory.json<br/>learned_preferences]
    end

    S4 --> SK
    S4 --> SM
    S4 --> CTX2
```

### Components

| Component | Purpose |
|-----------|---------|
| **Skill Factory** | Identifies repeated successful tasks, packages them as `SKILL.md` with provenance |
| **GEPA Evolver** | LLM-guided prompt mutations: tone changes, constraint add/remove, example injection |
| **Darwinian Evolver** | Population of solutions with fitness scores; kills worst, mutates survivors |
| **Background Review** | Analyzes state/cache for patterns, extracts user preferences, consolidates learnings |

## Verification Levels

| Level | What It Verifies |
|-------|-----------------|
| **N1** | Agenda, calendar, and bills verified |
| **N2** | Contact with Dona Lu made and pantry checked |
| **N3** | Kashrut compliance checks executed strictly |
| **N4** | Expenses and lists registered in `cache.json` |
| **N5** | Daily summary and balance sent for accountability |

## Constraints

- **Zero-Trust**: Cannot execute financial payments directly; only organizes lists and schedules.
- **MVI Limits**: All file writes strictly <200 lines.
- **Memory Constraint**: Never loads full history from previous days.
- **Max Context**: 2K tokens per session.
- **Forbidden**: Any task not described in `nice.md`.

## Files

```
agent_nice/
├── nice.md                    # Agent persona and contracts
├── state.json                 # Agent lifecycle state
├── context_memory.json        # Learned preferences + system rules
├── skills_memory.json         # Hermes loop state + learned skills
├── cache.json                 # Session state
├── shopping_list.json         # Pending purchases
├── pantry.json                # Current inventory
├── finance.json               # Account balance
├── receipts/                  # Expense receipts
└── hermes_agent/
    ├── hermes_agent_self_evolution.py  # Pipeline orchestrator
    ├── skill_factory.py                # Task → SKILL.md packaging
    ├── gepa_evolver.py                 # LLM-guided prompt evolution
    ├── darwinian_evolver.py            # Fitness-based population evolution
    ├── background_review.py            # Preference extraction
    ├── population/                     # Evolution population data
    └── reviews/                        # Background review logs
```

## Tech Stack

- **Language**: Python
- **Model**: custom-proxy/big-pickle (temperature: 0)
- **Persistence**: JSON files (state, cache, memory)
- **Governance**: Financial approval gates, kashrut compliance, MVI limits
- **Self-Evolution**: Hermes Agent (4-stage pipeline)
