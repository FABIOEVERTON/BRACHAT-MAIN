# Hermes Gateway — Configuração

Orquestrador multi-provider com fallback automático.

## Configuração

- **Provider primário**: Qwen 2.5 Coder 7B (Ollama em Windows, 192.168.18.11:11434)
- **Fallback**: Big-Pickle (OpenCode Zen)
- **Temperatura**: 0.0 (respostas determinísticas)
- **Streaming**: habilitado
- **Max tokens por resposta**: 100

## Estrutura

```
~/.hermes/
├── config.yaml          # Config principal
├── gateway.log          # Logs do gateway
├── skills/              # Skills do Hermes
├── sessions/            # Sessões
├── memories/            # Memórias
└── logs/                # Logs
```

## Arquivos

- `config.yaml` — Config completa com providers, fallback, geração
- Nota: Arquivos `.env` com chaves de API foram omitidos por segurança
