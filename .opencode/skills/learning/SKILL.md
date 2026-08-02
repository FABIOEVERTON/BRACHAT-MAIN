---
name: learning
id: S19
cluster: memoria
description: Aprende com experiências passadas extraindo padrões e propondo melhorias controladas com auditoria obrigatória.
---

### Objetivo
Aprender com experiências passadas de forma controlada: extrair padrões, propor melhorias, passar por auditoria e aprovação, e só então atualizar templates.

### Entradas
- Experiência registrada (execução, erro, acerto, feedback do usuário)
- Base de conhecimento atual (templates, skills, agentes)

### Saídas
- Padrão extraído
- Proposta de melhoria (template novo ou alterado)
- Decisão: APROVADO, REJEITADO, PRECISA_REVISÃO
- Template atualizado (se aprovado)

### Dependências
- SK-026 (Observability) para acessar experiências registradas
- SK-002 (Revisão de Diffs) para auditar a proposta
- HITL (SK-007) para aprovação final

### Token Budget
- 1000-2000 tokens por ciclo de aprendizado

### Custos
- Médio. Extração + proposta + auditoria + atualização.

### Segurança
- Proibido aprender autonomamente sem auditoria.
- Proposta de melhoria não pode alterar PRINCIPLES.md ou Governance.md sem HITL.
- Padrões extraídos não devem conter PII.

### Testes
1. Padrão extraído é generalizável (não overfitting)?
2. Proposta foi rejeitada se violava princípios?
3. Template atualizado passou por revisão antes de aplicar?

---
