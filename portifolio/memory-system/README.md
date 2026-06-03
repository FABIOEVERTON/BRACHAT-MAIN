# Memory System — Memória Persistente

Sistema de memória em JSON com cache de skills.

## Funcionamento

1. Cada interação relevante salva um JSON em `.mem0/`
2. Apenas o arquivo mais recente é carregado
3. Arquivos anteriores são automaticamente deletados
4. Instruções fixas (como "buscar skills") são preservadas

## Estrutura

```
.mem0/
├── _instruction.json       # Instrução fixa (sempre carregada)
└── skills-cache/
    └── index.json          # Índice de 1475 skills (458 KB)
```

## Como usar

```python
import memory
memory.save("contexto", {"dados": {...}})
latest = memory.latest()  # retorna último + instrução
```

## Componentes

- `memory.py` — Biblioteca de memória (save, latest, list_all)
- `skills-cache/index.json` — Índice pesquisável de 1475 skills
