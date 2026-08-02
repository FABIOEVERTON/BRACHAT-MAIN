---
name: observability
id: S22
cluster: avaliacao
description: Registra logs, tracing, timeline, eventos e custos para auditoria, debugging e análise retrospectiva.
---

### Objetivo
Registrar tudo que o sistema faz — logs, tracing, timeline, eventos, custos e decisões — para auditoria, debugging e análise retrospectiva.

### Entradas
- Evento a registrar (tipo, payload, timestamp, origem)
- Configuração de retenção e nível de detalhe

### Saídas
- Log estruturado persistido
- Tracing habilitado com span tree por execução
- Timeline reconstruível de qualquer sessão
- Métricas de custo por decisão

### Dependências
- Governance.md (classificação de dados e retenção)
- SK-003 (Eval & Evaluation) para métricas de custo

### Token Budget
- 200-400 tokens por registro de evento (leve, assíncrono)

### Custos
- Baixo. Operação de escrita, sem processamento pesado.

### Segurança
- Logs podem conter PII → aplicar mascaramento automático antes de persistir.
- Tracing não deve expor secrets ou tokens de acesso.
- Reter logs conforme política da Governance (mínimo necessário).

### Testes
1. Todo evento crítico foi registrado com timestamp?
2. Tracing permite reconstruir fluxo completo de uma requisição?
3. Logs sensíveis foram mascarados antes da persistência?
4. Política de retenção foi respeitada (purga automática)?

---
