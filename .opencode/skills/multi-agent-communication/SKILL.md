---
name: multi-agent-communication
id: S21
cluster: orquestracao
description: Coordena comunicação entre múltiplos agentes garantindo handoff seguro, contexto preservado e respostas consolidadas.
---

### Objetivo
Rotear, coordenar e consolidar comunicação entre múltiplos agentes (Hermes, Especialistas, Supervisor, Reviewer, Workers) garantindo handoff seguro, contexto preservado e respostas consolidadas.

### Entradas
- Requisição multiagente (tarefa, domínios envolvidos, nível de supervisão)
- Agentes disponíveis (definições dos agentes existentes)
- Protocolo de comunicação (síncrono/assíncrono, prioridade, timeout)

### Saídas
- Roteamento da requisição para o agente correto
- Resposta consolidada de múltiplos agentes
- Auditoria de cada handoff (origem, destino, tokens, timestamp)

### Dependências
- SK-023 (Agent Factory) para instanciar agentes que não existem
- SK-005 (Orquestração e Decomposição) para coordenar fluxos complexos
- SK-007 (HITL) para aprovação em ações de alto risco

### Token Budget
- 800-1500 tokens por ciclo de comunicação (roteamento + consolidação)

### Custos
- Médio. Cada agente envolvido consome tokens de execução + handoff.

### Segurança
- Handoff limitado a 2000 tokens por transferência.
- Hermes não deve expor contexto interno de um agente a outro sem necessidade.
- Supervisor pode cancelar/corrigir mensagens antes de entregar ao destino.
- Reviewer só recebe output anonimizado se o agente de origem operar com dados sensíveis.

### Testes
1. Mensagem chegou ao agente destino correto?
2. Contexto foi preservado sem vazamento entre agentes?
3. Supervisor interrompeu fluxo quando necessário?
4. Resposta consolidada não perdeu informação dos agentes individuais?
5. Timeout foi respeitado sem deadlock?

---
