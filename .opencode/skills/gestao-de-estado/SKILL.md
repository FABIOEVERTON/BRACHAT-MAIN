---
name: gestao-de-estado
id: S16
cluster: memoria
description: Gerencia memória de curto e longo prazo com checkpointing, compressão e time travel para recuperação de contexto após falhas.
---

### Objetivo
Gerenciar memória de curto e longo prazo, garantindo que o agente recupere o contexto após falhas ou intervenções.

### Entradas
- Schema de estado desejado
- Requisitos de persistência
- Políticas de retenção

### Saídas
- StateSchema tipado, checkpointers configurados, time travel habilitado, estratégia de compressão

### Dependências
- SK-001 (spec do estado)

### Token Budget
- 600-1000 tokens

### Custos
- Baixo. Operação interna de design.

### Segurança
- Estado pode conter PII → aplicar LGPD antes de persistir.

### Testes
1. Checkpoint salva estado a cada N transições?
2. Time travel restaura estado anterior corretamente?
3. Compressão não perde campos críticos?

---
