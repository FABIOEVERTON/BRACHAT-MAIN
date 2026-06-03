# OpenCode — Config Big-Pickle

Configuração do OpenCode com modelo big-pickle (OpenCode Zen, free tier).

## Setup

```json
{
  "provider": {
    "ollama": {
      "name": "Ollama (Windows - Qwen)",
      "options": {
        "baseURL": "http://192.168.18.11:11434"
      },
      "models": {
        "qwen2.5-coder:7b": {
          "name": "Qwen 2.5 Coder 7B (Windows)"
        }
      }
    }
  }
}
```

## Agentes

| Agente | Função |
|--------|--------|
| `OpenAgent` | Agente universal para queries e tarefas |
| `OpenCoder` | Orquestrador de codificação complexa |

## Subagentes

- `QwenWindows` — Subagente via Ollama no Windows
- `ContextScout` — Descoberta de contexto
- `ExternalScout` — Documentação externa
- `TaskManager` — Breakdown de tarefas
- `TestEngineer` — Testes
- `DocWriter` — Documentação

## Skills do OpenCode

- `context7` — Documentação de bibliotecas
- `task-management` — Gerenciamento de tarefas
- `chat-config` — Config de chat (temp 0, streaming, chunks 100t)
