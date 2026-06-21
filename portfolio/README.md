# Brachat — Portfolio

AI agent system with multi-model orchestration, persistent memory, and a library of +1400 specialized skills.

## Architecture

```
┌──────────────────────────────────────────────────┐
│                    BRACHÁT                       │
│            (Orchestrator + Product)              │
├──────────────────────────────────────────────────┤
│   ┌──────────────┐         ┌──────────────────┐  │
│   │  Qwen 2.5    │  ←fallback→  │  Big-Pickle    │  │
│   │  (Windows)   │         │  (OpenCode Zen)  │  │
│   └──────────────┘         └──────────────────┘  │
├──────────────────────────────────────────────────┤
│   Skills Library: 1475 specialized skills        │
│   Memory System: Persistent JSON with cache      │
│   Telegram: Connected via EZRA Gateway           │
└──────────────────────────────────────────────────┘
```

## Components

| Component | Description |
|-----------|-------------|
| `ezra/` | EZRA orchestrator config |
| `opencode-config/` | OpenCode config with big-pickle (free) model |
| `memory-system/` | Persistent memory system in JSON |
| `skills/` | Catalog of 1475 AI skills |
| `one_oracle/imersion_agent/` | AI Agent built during **Oracle Next Education (ONE) 2026** — HR Buddy (n8n, Cohere, Telegram, RAG, MySQL) |

## Stack

- **Models**: Qwen 2.5 Coder 7B (Ollama), Big-Pickle (OpenCode Zen)
- **Orchestrator**: EZRA v1.0
- **Infra**: macOS, Python 3.14, Ollama (Windows)
- **Integrations**: Telegram, OpenCode Zen API

## Usage

```bash
# OpenCode CLI
opencode run
```
