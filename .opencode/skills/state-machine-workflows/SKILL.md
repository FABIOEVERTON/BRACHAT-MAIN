---
name: state-machine-workflows
id: S31
cluster: memoria
description: Cria agentes com memória persistente entre sessões, checkpointing e capacidade de rebobinar para estados anteriores.
---

### Objetivo
Criar agentes com memória de curto e longo prazo, que persistem estado entre sessões e podem "rebobinar" para pontos anteriores.

### Entradas
- Fluxo com múltiplos caminhos
- Requisitos de persistência e checkpoint

### Saídas
- State machine implementada com: estados, transições, checkpoints, time travel

### Dependências
- SK-004 (Estado e Persistência)

### Token Budget
- 800-1500 tokens

### Custos
- Médio. Checkpointing frequente aumenta custo de armazenamento.

### Segurança
- Checkpoints podem conter PII → aplicar LGPD antes de salvar.

### Testes
1. Checkpoint salva a cada 3 transições?
2. Time travel restaura estado anterior?
3. Auto-purga mantém só últimos 10 checkpoints?

---
