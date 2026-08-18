# brachat-main

**Portfolio of production AI agents and governance systems. Every project here is built by Fabio Everton, with Ezra (AI assistant) operating under his direct supervision. Nothing deploys without governance.**

## What This Repo Is

This is not a collection of demos or tutorials. Each project is a working system — deployed, tested, and governed. The common thread: **runtime governance that cannot be bypassed**.

```mermaid
graph TD
    subgraph "Repo Structure"
        ROOT[brachat-main] --> PORT[portfolio/<br/>10 projects]
        ROOT --> OPS[ops/<br/>deploy scripts, services]
        ROOT --> AGENTS[agents/<br/>shared skills, memory]
    end

    subgraph "Governance Requirement"
        PORT --> GW[Every agent passes through<br/>policy gate before execution]
        GW --> POL[OPA / Rego<br/>deterministic rules]
        GW --> AU[governance-ledger.jsonl<br/>immutable audit trail]
        GW --> HITL[Human approval<br/>for high-risk actions]
    end

    subgraph "Built By"
        F[Fabio Everton<br/>author, supervisor] -->|writes code| PORT
        EZ[Ezra<br/>AI assistant] -->|drafts, research, automation| PORT
        F -->|approves everything| EZ
    end
```

## Runtime Governance — The Non-Negotiable

Every agent in this portfolio enforces the same rule: **if it cannot be audited, it cannot execute.**

This is not a feature. It is a constraint on architecture.

```mermaid
flowchart LR
    subgraph "Every Agent Action"
        A[Tool Call] --> G{Governance Gate}
        G -->|allow| E[Execute]
        G -->|deny| BLOCK[Blocked]
        G -->|approve| H[Human Queue<br/>60s timeout]
        H -->|approved| E
        H -->|rejected| BLOCK
    end

    subgraph "What Gets Recorded"
        E --> L[ledger entry<br/>hash chain]
        BLOCK --> L
        L --> AUDIT[Replayable evidence<br/>immutable, verifiable]
    end
```

### Enforcement Rules

| Rule | Implementation |
|------|---------------|
| **Deterministic** | Authorization by code (OPA/Rego), never by LLM opinion |
| **Immutable** | SHA-256 hash chain on every decision entry |
| **Scoped** | Derived credential per task, not global access |
| **Rate-limited** | Anti-drip: max N destructive actions per time window |
| **Fail-closed** | If gate cannot decide → deny |
| **Auditable** | Full replay from ledger: who, what, when, outcome |

## Projects

| Project | Category | What It Demonstrates |
|---------|----------|---------------------|
| [**ezra_agent**](portfolio/ezra_agent) | Autonomous Agent | 24/7 Telegram agent with skills, memory, OCI deploy |
| [**ezra_curator**](portfolio/ezra_curator) | RAG | Corporate document RAG with reranking, fallbacks, citations |
| [**essay_creator**](portfolio/essay-creator) | Multi-Agent Pipeline | 5-agent LangGraph system with HITL and iterative refinement |
| [**exec-email-assistant**](portfolio/exec-email-assistant) | Multi-Agent Pipeline | Intent-based email routing with semantic memory |
| [**ezra_control_plane**](portfolio/ezra_control_plane) | Governance | Runtime gate that limits damage of compromised agents |
| [**agent_nice**](portfolio/agent_nice) | Autonomous Agent | Household governance with financial gates + self-evolution |
| [**parashat_bot**](portfolio/parashat_bot) | RAG + Bot | Weekly Torah study with NotebookLM + Groq |
| [**langchain_hands_on**](portfolio/langchain_hands_on) | Research Pipeline | 4-agent RAG research system (LangChain + Gemini) |
| [**langraph_hands_on**](portfolio/langraph_hands_on) | Research Pipeline | Same pipeline rebuilt on LangGraph with state + persistence |
| [**code-connect**](portfolio/code-connect) | Full-Stack | pnpm monorepo: React (Vite) + NestJS |

## How Projects Are Built

```mermaid
flowchart TD
    subgraph "Author"
        F[Fabio] -->|defines| SPEC[spec, requirements,<br/>governance rules]
        F -->|reviews| CODE[code, tests, deploy]
        F -->|approves| DEP[deployment]
    end

    subgraph "Ezra (AI Assistant)"
        EZ[Ezra] -->|drafts| CODE
        EZ -->|writes| TESTS[tests]
        EZ -->|generates| DOCS[documentation]
        EZ -->|automates| OPS[deploy scripts]
        EZ -->|never| DEP
    end

    subgraph "Governance"
        SPEC --> GW[governance gate]
        CODE --> GW
        GW -->|pass| DEP
        GW -->|fail| FIX[returns to Fabio]
    end
```

Every project follows this rule:
- **Fabio** writes specs, defines governance constraints, reviews code, approves deployment.
- **Ezra** drafts code, generates tests, automates ops — under Fabio's supervision.
- **Ezra never deploys independently.** Every deployment requires Fabio's explicit approval.

## Infrastructure

```mermaid
graph LR
    subgraph "Mac (Local)"
        DRIVE[Google Drive<br/>source of truth]
        LA[LaunchAgents<br/>4x backup, 2x scan,<br/>daily commit, 3min sync]
    end

    subgraph "Oracle Cloud"
        VM[ezra_bot_1<br/>163.176.111.95<br/>A1.Flex ARM]
    end

    subgraph "Services"
        SRV[opencode serve :3791]
        BR[bridge_telegram.js]
        PB[parashat-bot]
        AR[anti-reclaim]
    end

    DRIVE -->|git pull| VM
    VM --> SRV
    VM --> BR
    VM --> PB
    VM --> AR
```

- **Compute**: Oracle Cloud A1.Flex (ARM, always-free tier)
- **Source of truth**: Google Drive → GitHub → VM
- **Secrets**: Never in git. `secrets.env` on Mac, `.env` on VM.
- **Backup**: rclone → Google Drive (4x/day)

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Languages** | Python · SQL · Rego · Bash · JavaScript · TypeScript |
| **Frameworks** | LangChain · LangGraph · FastAPI · NestJS · OpenCode |
| **AI/LLM** | OpenAI · Gemini · Cohere · Ollama · Groq · RAG |
| **Governance** | OPA/Rego · NIST AI RMF · EU AI Act · LGPD |
| **Infra** | Oracle Cloud (OCI) · Docker · PostgreSQL · pnpm |

## Contact

**Fabio Everton** — [jae.engenharia@gmail.com](mailto:jae.engenharia@gmail.com) · [LinkedIn](https://linkedin.com/in/fabioeverton) · [GitHub](https://github.com/FABIOEVERTON)

---

*Last updated: August 2026*
