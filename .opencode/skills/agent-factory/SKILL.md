---
name: agent-factory
id: S01
cluster: orquestracao
description: Cria, instancia e valida agentes completos do design ao blueprint com conformidade obrigatória.
---

### Objetivo
Criar, instanciar e validar agentes completos — do design ao blueprint — garantindo que todo agente nasça com persona, estado, arquitetura, testes e conformidade com o Agent Blueprint obrigatório.

### Entradas
- Solicitação de novo agente (tarefa, domínio, nível de autonomia)
- Definição do agente (persona, estado, habilidades, template)
- Recursos alocados (token budget, storage, permissões)
- Aprovação da Governance (High risk → HITL obrigatório)

### Saídas
- Agente instanciado com diretório próprio
- Persona.md, state.json, startup.md gerados
- Skills opcionais e testes validados
- Agente registrado no state.json do orchestrator
- Relatório de conformidade com Agent Blueprint

### Integração com n8n — Regra Obrigatória (aprovada por Fabio, 02/ago/2026)

**Se um agente/workflow for usar n8n, ENTRAR NA URL do n8n** (`http://localhost:5678` local / URL pública na nuvem). Sempre acessar a instância do n8n pela URL — nunca tentar contornar.

- Credenciais do n8n no MCP: `N8N_EMAIL` (jae.engenharia@gmail.com) e `N8N_PASSWORD` — via `mcp_secrets_get`.
- Workflow MCP server do Ezra: `ezra-mcp` (id `8Q8c3ttyF4gPqijS`), endpoint `/webhook/mcp`.
- NUNCA apagar credenciais MCP ao mexer na integração (regra de segurança vigente).

### Skill Creation Criteria — Regra de Ouro

**Antes de criar skill nova, perguntar ao Fabio. SEMPRE.** Não criar sem autorização explícita.

Passos obrigatórios antes de perguntar:

1. **Provar que não existe**: listar todas as skills existentes com assunto similar e explicar porque cada uma NÃO cobre o caso
2. **Provar que não dá pra refinar**: mostrar que tentou estender skill existente e não foi possível sem misturar assuntos
3. **Provar frequência**: mostrar que o padrão repetiu 3+ vezes em 7 dias

Uma skill aprovada só se:
- Nenhuma skill existente cobre o assunto (provado)
- Não é possível refinar/extender skill existente sem misturar assuntos (provado)
- Frequência mínima de 3+ vezes em 7 dias (provado)
- **Assunto único**: uma skill = um assunto. Não pode misturar responsabilidades.
- ROI positivo (tempo economizado/mês > manutenção)
- Skill budget < 40. Se >= 40, precisa arquivar uma antes.
- Token budget, custo, segurança, testes e metadata completos

### Dependências
- Governance.md (aprovação para High/Critical risk)
- SK-010 (Arquitetura de Harness) para sandbox

### Token Budget
- 2000-4000 tokens por criação completa (design → instanciação → validação)

### Custos
- Alto. Criação envolve múltiplos passos (design, instanciar, validar).

### Segurança
- **High risk.** Criação de agente com execução externa requer HITL obrigatório.
- Agente instanciado herda restrições de segurança do parent orchestrator.
- Blueprint validation é gate obrigatório — não pode ser pulado.
- Toda instanciação registrada no governance-ledger.

### Testes
1. Persona.md é carregado corretamente?
2. State.json persiste entre execuções?
3. 3 cenários testados: sucesso, falha, edge case?
4. Destruição do agente limpa todos os artefatos?
5. Token budget não excede o alocado?
6. Blueprint validation aprovou o agente?

---
