---
name: orquestracao
id: S23
cluster: orquestracao
description: Quebra problemas complexos em subtarefas especializadas e coordena agentes em fluxos sequenciais ou paralelos com handoff seguro.
---

### Objetivo
Quebrar problemas complexos em subtarefas especializadas e coordenar agentes em fluxos sequenciais ou paralelos com handoff seguro de contexto e circuit breakers.

### Entradas
- Problema complexo / tarefa com múltiplas etapas
- Agentes disponíveis para alocação
- Restrições de orçamento, tempo e profundidade

### Saídas
- Decomposição em subtarefas, alocação de agentes, protocolo de handoff
- Fluxo orquestrado executado com handoffs concluídos e resultados consolidados
- Circuit breakers ativados em caso de falha

### Dependências
- SK-023 (Agent Factory) para criar agentes que não existem

### Token Budget
- 1000-3000 tokens (depende do número de agentes)

### Custos
- Médio-Alto. Cada agente na chain consome tokens de execução + handoff.

### Segurança
- Handoff limitado a 2000 tokens por transferência.
- Circuit breaker: 3 falhas → pausa.
- Máximo 5 agentes paralelos, 3 níveis de profundidade.
- Contexto não deve vazar entre agentes durante handoff.

### Testes
1. Subtarefas cobrem o problema sem sobreposição?
2. Handoff preserva contexto essencial sem duplicar?
3. Circuit breaker interrompe após 3 falhas?
4. Consolidação combina outputs sem perder informação?

---
