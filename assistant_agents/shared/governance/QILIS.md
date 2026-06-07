# QILIS — Quantum-Inspired Lifecycle Interpretability System

Framework de interpretabilidade para todo o lifecycle de agentes e modelos, baseado em princípios quântico-inspirados.

## Core Principles
1. **Lifecycle-wide interpretability** — não só output, mas cada transição de estado
2. **Feature relevance tracing** — DRMP (Dynamic Relevance Metric Propagation) em todas as camadas
3. **Semantic coherence** — AMSE (Adaptive Meaning Semantic Embedding) mantém coerência semântica
4. **Adaptive pruning** — RBCO (Relevance-Based Contextual Optimization) corta features irrelevantes
5. **Evidence capture at decision moment** — justificação pós-inferência sem re-execução

## Implementation in BRACHÁT

### Agent-level QILIS (every agent MUST)
```
Entrada → feature tagging → relevance metrics → lifecycle stage log → interpretable output
```

### Lifecycle stages tracked per action
1. INTENT — o que o agente pretende fazer
2. EVALUATION — quais constraints/policies foram avaliadas
3. DECISION — autorizado/rejeitado/pendente e por quê
4. EXECUTION — o que foi executado, com que dados
5. OUTCOME — resultado observável
6. AUDIT — evidência completa para replay

### QILIS Requirements for Agents
- Cada ação DEVE gerar um trace com relevance metrics
- Features irrelevantes DEVEM ser podadas (RBCO)
- O output DEVE ser interpretável em linguagem natural
- O lifecycle inteiro DEVE ser re-playable a partir do ledger
- Semantic knowledge DEVE ser preservada entre sessões

### Audit-grade AI Interpretability
- Relevance vectors armazenados no cache.json de cada agente
- Ledger de interpretabilidade separado do ledger de ações
- Relatório de interpretabilidade gerado automaticamente no review noturno
- Qualquer agente pode ser interrogado: "por que você decidiu X?"

## Integration with AGCP
- QILIS fornece a camada de interpretabilidade sobre o lifecycle AGCP
- Cada transição de estado AGCP (SUBMITTED → AUTHORIZED → EXECUTED) tem um trace QILIS associado
- Evidence receipts AGCP contêm relevance metrics QILIS
- Para L3+ (deterministic governance), o replay validation inclui os relevance vectors
