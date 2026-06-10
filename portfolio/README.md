# Brachat — Portfolio

Sistema de agente de IA com orquestração multi-modelo, memória persistente e biblioteca de +1400 skills especializados.

## Arquitetura

```
┌──────────────────────────────────────────────────┐
│                    BRACHÁT                       │
│            (Orquestrador + Produto)              │
├──────────────────────────────────────────────────┤
│   ┌──────────────┐         ┌──────────────────┐  │
│   │  Qwen 2.5    │  ←fallback→  │  Big-Pickle    │  │
│   │  (Windows)   │         │  (OpenCode Zen)  │  │
│   └──────────────┘         └──────────────────┘  │
├──────────────────────────────────────────────────┤
│   Skills Library: 1475 skills especializados     │
│   Memory System: JSON persistente com cache      │
│   Telegram: Conectado via EZRA Gateway           │
└──────────────────────────────────────────────────┘
```

## Componentes

| Componente | Descrição |
|------------|-----------|
| `ezra/` | EZRA orchestrator config |
| `opencode-config/` | Config OpenCode com modelo big-pickle (free) |
| `memory-system/` | Sistema de memória persistente em JSON |
| `skills/` | Catálogo de 1475 skills para IA |

## Stack

- **Modelos**: Qwen 2.5 Coder 7B (Ollama), Big-Pickle (OpenCode Zen)
- **Orquestrador**: EZRA v1.0
- **Infra**: macOS, Python 3.14, Ollama (Windows)
- **Integrações**: Telegram, OpenCode Zen API

## Como usar

```bash
# OpenCode CLI
opencode run
```
