---
name: architecture-library
id: S06
cluster: arquitetura
description: Mantém e consulta biblioteca de componentes reutilizáveis para reutilizar soluções em vez de reinventá-las.
---

### Objetivo
Manter e consultar uma biblioteca de componentes reutilizáveis (Harness Patterns, Loop Patterns, Memory Patterns, Governance Patterns, Skill Patterns, Agent Patterns, Prompt Patterns) para reutilizar soluções em vez de reinventá-las.

### Entradas
- Consulta por padrão ("preciso de um pattern para loop com checkpoint")
- Novo pattern para catalogar
- Contexto do problema a resolver

### Saídas
- Pattern mais relevante retornado com: nome, descrição, quando usar, exemplo, custo estimado
- Pattern catalogado com metadados (tipo, versão, dependências, tags)

### Dependências
- SK-013 (Pensamento Sistêmico) para análise de qual pattern se aplica
- SK-001 (Spec) para adaptar pattern ao contexto

### Token Budget
- 400-800 tokens por consulta ou catálogo

### Custos
- Baixo. Consulta a biblioteca local.

### Segurança
- Patterns não devem conter credenciais ou dados específicos de cliente.
- Uso de pattern é recomendação, não decisão automática — sempre passar por Governance.

### Testes
1. Pattern retornado é o mais relevante para o problema?
2. Consulta sem match retornou fallback útil?
3. Pattern catalogado tem metadados completos?

---
