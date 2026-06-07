# Brachat — Portfolio

Sistema de agente de IA com orquestração multi-modelo, memória persistente e biblioteca de +1400 skills especializados.

## Arquitetura

```
┌──────────────────────────────────────────────────┐
│                   Hermes Gateway                │
│            (Orquestrador + Produto)              │
├──────────────────────────────────────────────────┤
│   ┌──────────────┐         ┌──────────────────┐  │
│   │  Qwen 2.5    │  ←fallback→  │  Big-Pickle    │  │
│   │  (Windows)   │         │  (OpenCode Zen)  │  │
│   └──────────────┘         └──────────────────┘  │
├──────────────────────────────────────────────────┤
│   Skills Library: 1475 skills especializados     │
│   Memory System: JSON persistente com cache      │
│   Telegram: Conectado via Hermes Gateway         │
└──────────────────────────────────────────────────┘
```

## Componentes

| Componente | Descrição |
|------------|-----------|
| `hermes/` | Hermes Gateway config — orquestrador multi-provider |
| `opencode-config/` | Config OpenCode com modelo big-pickle (free) |
| `memory-system/` | Sistema de memória persistente em JSON |
| `skills/` | Catálogo de 1475 skills para IA |

## Stack

- **Modelos**: Qwen 2.5 Coder 7B (Ollama), Big-Pickle (OpenCode Zen)
- **Orquestrador**: Hermes Agent v0.15.2
- **Infra**: macOS, Python 3.14, Ollama (Windows)
- **Integrações**: Telegram, OpenCode Zen API

## Como usar

```bash
# Hermes Gateway (auto-inicia via launchctl)
hermes gateway run

# OpenCode CLI
opencode run
```
