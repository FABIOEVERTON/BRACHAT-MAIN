# Ezra Agent — Autonomous AI Assistant (24/7 Production)

**Personal AI agent running 24/7 on Oracle Cloud Infrastructure. Telegram interface, persistent memory, multi-skill architecture, governance built-in. Not a demo — daily driver.**

## What It Does

Ezra is a self-directed agent that plans, executes, remembers, and learns. It scans freelance platforms, manages schedules, learns from every interaction, and enforces governance on every action.

## Architecture

```mermaid
graph TD
    subgraph "User Interface"
        F[Fabio] -->|Telegram| TG[Telegram API]
    end

    subgraph "Bridge (Node.js)"
        TG --> BR[bridge_telegram.js<br/>relay only, no logic<br/>600s timeout]
    end

    subgraph "Agent Server (OCI VM)"
        BR -->|Basic Auth| SRV[opencode serve<br/>127.0.0.1:3791]
        SRV --> BRAIN[Agent Brain<br/>EZRA_SYSTEM.txt]
    end

    subgraph "Skills Engine"
        BRAIN --> SK1[agent-freelancer<br/>9 platforms, Playwright]
        BRAIN --> SK2[ai-job-search-agent<br/>email + platforms]
        BRAIN --> SK3[compliance-checker<br/>LGPD / NIST / EU AI Act]
        BRAIN --> SK4[...<br/>pluggable skills]
    end

    subgraph "Tool Layer"
        SK1 --> PW[Playwright<br/>web scraping]
        SK2 --> CM[Composio<br/>Gmail, LinkedIn]
        SK1 --> TG2[Telegram API]
        SK3 --> MCP[MCP Server<br/>secrets, integrations]
        SK4 --> OCI[OCI SDK<br/>deploy, storage]
    end

    subgraph "Governance Layer"
        BRAIN --> GL[governance-ledger.jsonl<br/>immutable audit trail]
        BRAIN --> HITL[HITL approval gates<br/>high-risk actions]
        BRAIN --> POL[Policy enforcement<br/>OPA / Rego]
        BRAIN --> PII[PII filter<br/>sensitive data blocked]
    end

    subgraph "Persistence"
        BRAIN --> MEM[mem0<br/>long-term memory]
        BRAIN --> DB[(SQLite<br/>checkpoints)]
    end
```

## Infrastructure

```mermaid
graph LR
    subgraph "Mac (Local)"
        MC[Mac Mini] -->|rclone| GD[Google Drive<br/>source of truth]
        MC -->|rsync + SSH| VM
        MC -->|LaunchAgents| LA[4x/day backup<br/>daily commit<br/>2x freelance scan<br/>3min sync]
    end

    subgraph "Oracle Cloud"
        VM[ezra_bot_1<br/>163.176.111.95<br/>A1.Flex ARM]
        VM2[ezra_bot_2<br/>137.131.242.180<br/>utilitarios]
    end

    subgraph "Services on VM"
        SRV[opencode serve<br/>port 3791]
        BR2[bridge_telegram.js<br/>Telegram relay]
        PB[parashat-bot<br/>Torah study]
        NBLM[nblm-refresh<br/>daily 03:00 UTC]
        AR[anti-reclaim<br/>idle protection]
    end

    GD -->|git pull| VM
    VM --> SRV
    VM --> BR2
    VM --> PB
    VM --> NBLM
    VM --> AR
```

## Deploy Components

| Service | File | Purpose |
|---------|------|---------|
| **Ezra Brain** | `ezra-serve.service` | OpenCode serve on port 3791, auto-restart, warmup on boot |
| **Telegram Bridge** | `bridge_telegram.service` + `bridge_telegram.js` | Zero-logic relay, 600s timeout, Basic Auth to server |
| **Parashat Bot** | `parashat-bot.service` | Torah study bot, Groq + NotebookLM, daily 09:00 BRT |
| **NotebookLM Refresh** | `nblm-refresh.timer` | Daily auth cookie refresh at 03:00 UTC |
| **Anti-Reclaim** | `anti-reclaim.service` + `anti-reclaim.py` | Synthetic load to prevent OCI free-tier instance reclaim |
| **Sync Pipeline** | `sync-ezra.sh` | Mac → Drive → GitHub → VM (rsync + git push + systemctl restart) |

## Data Flow

```mermaid
sequenceDiagram
    participant F as Fabio
    participant T as Telegram
    participant B as Bridge
    participant S as OpenCode Server
    participant A as Agent Brain
    participant SK as Skills
    participant GL as Governance Ledger

    F->>T: "scan freelance platforms"
    T->>B: message
    B->>S: POST /session/{id}/message
    S->>A: route to skill
    A->>SK: agent-freelancer.execute()
    SK->>SK: Playwright scraping
    SK-->>A: results
    A->>GL: log action (hash chain)
    A-->>S: response
    S-->>B: response
    B-->>T: sendMessage chunks
    T-->>F: results
```

## Security

- **Secrets**: `secrets.env` ONLY on Mac. VM uses `.env` with its own keys. Nothing in git.
- **Auth**: Basic auth (`opencode:PASSWORD`) between bridge and server.
- **Backup**: rclone → Google Drive (4x/day). Source of truth: `brachat-main` on Drive.
- **Sync**: Mac → Drive → GitHub → VM. Never edit VM directly.

## Files

```
ezra_agent/
├── README.md
├── .opencode/              # Brain config (instructions, skills, plugins, reference)
└── deploy/
    ├── ezra-serve.service          # systemd: opencode serve 24/7
    ├── bridge_telegram.js          # Telegram relay (zero logic)
    ├── bridge_telegram.service     # systemd: bridge
    ├── ezra-warmup.sh              # Post-startup warmup (sends "warm-ok")
    ├── parashat-bot.service        # systemd: Torah study bot
    ├── nblm-refresh.timer          # systemd timer: NotebookLM auth refresh
    ├── anti-reclaim.py             # Synthetic load (idle protection)
    ├── anti-reclaim.service        # systemd: anti-reclaim
    └── sync-ezra.sh               # Pipeline: Mac → Drive → GitHub → VM
```
