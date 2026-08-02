---
name: governanca-hitl
id: S17
cluster: governanca
description: Integra julgamento humano em pontos críticos para garantir alinhamento ético, conformidade e responsabilidade nas decisões do agente.
---

### Objetivo
Integrar julgamento humano em pontos críticos para garantir alinhamento ético, conformidade e responsabilidade.

### Entradas
- Fluxo do processo
- Pontos de risco identificados

### Saídas
- Pause points mapeados, interrupções implementadas, chain of thought exposta, feedback loop configurado

### Dependências
- Governance.md (políticas de HITL)

### Token Budget
- 400-800 tokens

### Custos
- Médio. Requer intervenção humana, que tem custo de tempo.

### Segurança
- Crítico. Implementa os gates de segurança definidos na Governance.

### Testes
1. Pause points param antes de toda ação irreversível?
2. Chain of thought é auditável por humano?
3. Feedback do humano atualiza o sistema?

---
