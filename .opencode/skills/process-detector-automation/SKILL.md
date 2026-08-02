---
name: process-detector-automation
id: S27
cluster: integracao
description: Identifica tarefas repetitivas e implementa automações inteligentes com detecção, implementação e medição de ROI.
---

### Objetivo
Identificar tarefas repetitivas e implementar automações inteligentes (metodologia Pascal Bornet) desde a detecção até a medição de ROI.

### Entradas
- Logs de atividades, observações de padrões
- Processo candidato e métricas de linha de base (tempo, custo, erros)

### Saídas
- Tarefa classificada (COPY-PASTE, DECISÃO RECORRENTE, etc.) com score de automação
- Decisão: AUTOMATIZAR_AGORA, AUTOMATIZAR_SESSÃO, CRIAR_TEMPLATE, MANTER_MANUAL
- Process Audit, Architecture (A/B/C/D), Build, ROI medido, Knowledge Transfer

### Dependências
- SK-023 (Agent Factory) se padrão C ou D (novo agente)
- Diretriz: Integrations/APIS/ ou Composio para automações externas

### Token Budget
- 400-800 por detecção + 2000-5000 por automação completa

### Custos
- Alto. Detecção é leve, mas implementação + teste + medição consomem.

### Segurança
- Logs podem conter dados operacionais → mascarar antes.
- Automações com acesso externo passam por HITL.
- Toda automação deve ter rollback documentado.

### Testes
1. Detectou padrão com 3+ repetições?
2. Score reflete corretamente frequência/tempo/complexidade?
3. Tempo economizado > 50%?
4. ROI > 3x em 3 meses?
5. Knowledge Transfer permite desativação segura?

---
