---
name: arquitetura-harness
id: S07
cluster: arquitetura
description: Projeta a camada de engenharia não-LLM que fornece ambiente seguro e persistente para o agente operar.
---

### Objetivo
Projetar a camada de engenharia não-LLM que fornece o ambiente seguro e persistente para o agente operar.

### Entradas
- Requisitos de execução (isolamento, persistência, segurança)
- Padrão de orquestração escolhido

### Saídas
- Arquitetura de harness: padrão, sandbox, persistência, memória em camadas

### Dependências
- SK-004 (Estado e Persistência)

### Token Budget
- 600-1000 tokens

### Custos
- Baixo. Design, sem execução.

### Segurança
- Sandboxing é requisito de segurança. Isolar execução do host.

### Testes
1. Sandbox isola execução do host?
2. Persistência sobrevive a falha do agente?
3. Camadas de memória operam independentes?

---
