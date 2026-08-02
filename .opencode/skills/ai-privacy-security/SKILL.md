---
name: ai-privacy-security
id: S03
cluster: seguranca
description: Protege dados, identidade e operações em sistemas que processam informações sensíveis com auditoria e controles.
---

### Objetivo
Proteger dados, identidade e operações em um mundo onde IA processa informações sensíveis.

### Entradas
- Sistema/agente a ser auditado
- Dados processados (classificação)
- Regulamentos aplicáveis (LGPD, Marco Legal IA)

### Saídas
- Auditoria de dados, arquitetura de proteção (Zero Trust, Mínimo Privilégio), protocolo para agentes, checklist mensal

### Dependências
- Governance.md (seções de segurança e LGPD)

### Token Budget
- 800-1500 tokens

### Custos
- Médio. Auditoria e implementação de controles.

### Segurança
- **Critical.** Esta skill define a segurança do sistema.
- Toda recomendação deve seguir Least Privilege e Zero Trust.

### Testes
1. Dados sensíveis foram mapeados?
2. PII removido antes de enviar ao LLM?
3. Checklist mensal é acionável?

---
