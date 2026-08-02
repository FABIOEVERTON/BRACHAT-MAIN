---
name: busca-integracao-ferramentas
id: S10
cluster: integracao
description: Expande capacidades do agente conectando-o a dados e ações do mundo real via MCP, APIs e protocolos padronizados.
---

### Objetivo
Expandir capacidades do agente conectando-o a dados e ações do mundo real via protocolos padronizados.

### Entradas
- Serviço externo a ser integrado (API, banco, MCP)
- Schema de dados esperado

### Saídas
- Integração MCP ou API configurada, schemas definidos, ferramenta publicada no catálogo

### Dependências
- Composio MCP (caminho primário) e/ou Integrations/APIS/.

### Diretriz de Arquitetura de Ferramentas (aprovada por Fabio, 02/ago/2026)
- **MCP** para integrações **externas/agênticas**: Composio (apps), n8n (workflows), mem0, brachat-mcp — tudo que o agente precisa enxergar como ferramenta e chamar. Um protocolo, auth padronizada, skill-gate por prefixo.
- **CLI/LIB nativos** para operações **internas determinísticas**: git, docker, node/python one-offs, leitura/escrita de arquivo. Sem MCP — cada servidor MCP adiciona schema ao contexto (custo de tokens) sem benefício aqui.
- **Regra prática**: MCP para *expor/tornar acessível*; CLI/LIB para *executar operações de sistema*. Composio continua servindo apps externos; n8n vira MCP server próprio; libs continuam diretas.
- **Exceção**: decisão de colocar uma ferramenta interna no MCP só por autorização explícita de Fabio.
- Referência: `manifest_tools.md` (regra de verificação mínima + resumo estático).

### Acesso ao Composio
- **Ativação on-demand**: Composio permanece **desligado no boot** (custo de schemas). Ativar somente quando a tarefa exigir integração real, via `/mcp` toggle.
- **Escopo**: uso exclusivo para conectar ferramentas externas (Gmail, Google Calendar, Slack, Notion, CRMs, etc.) através de tools MCP do Composio.
- **Auth**: credenciais via OAuth/secret manager (env vars). Nunca hardcoded no repositório.
- **Fluxo**:
  1. Verificar se a tool necessária está disponível no MCP Composio.
  2. Ativar o servidor via `/mcp` quando a dependência for confirmada.
  3. Executar a integração com schema validado agressivamente.
  4. Desligar via `/mcp` ao concluir (volta ao boot enxuto).
- **Segurança**: toda integração passa pela External Integrations Rule do governance-policy. Escrita em APIs externas = risco **High** → aprovação explícita de Fabio.
- **Custo**: cada tool MCP adiciona schema ao contexto. Integrar apenas as ferramentas estritamente necessárias à tarefa.

### Acesso à Boundary Protegida (brachat-mcp)
- Dados sensíveis (credenciais, PII, docs pessoais) vivem em `.opencode/mcp/` e são acessíveis **somente** via servidor MCP `brachat-mcp` (`.opencode/mcp/server.mjs`).
- Permissões do opencode bloqueiam leitura/escrita direta de `.opencode/mcp/**` (Read/Edit/Glob deny). **Nunca** contornar via bash/cat.
- **Tools**: `mcp_list`, `mcp_read`, `mcp_write`, `mcp_secrets_list` (só nomes), `mcp_secrets_get` (1 chave, auditada em `.opencode/mcp/audit.log`).
- **Regras**: credenciais nunca via `mcp_read`; escrita bloqueada em `credentials/`, `server.mjs`, `README.md`, `audit.log`. Path traversal e binários bloqueados no servidor.

### Acesso ao MCP Remoto (OCI)
- Após a migração para OCI, o mesmo servidor roda via HTTP em `.opencode/mcp/server-remote.mjs` (deploy com `.opencode/infra/ezra-core/`).
- **Endpoint**: ALB + listener 8765 → instância `ezra-prod` (privada); healthcheck no workflow `restore-test.yaml`.
- **Auth**: `Authorization: Bearer <token>` — mesmo valor do segredo `ezra/brachat-token` no Vault (nunca em código/env do cliente).
- **Boundary**: `/ezra-data/mcp`; segredos em `/ezra-data/.secrets.env` (0600, populados por `.opencode/iac/scripts/fetch-secrets.sh` direto do Vault, sem chaves em disco).
- **Acesso externo**: credenciais e leitura da boundary **só** via MCP tools — nunca por leitura direta de arquivo/ssh.
- **Fallback**: se o ALB estiver fora, validar primeiro `deploy.yaml`/`backup.yaml` antes de qualquer ação.

### Token Budget
- 600-1000 tokens

### Custos
- Variável. Depende do serviço externo integrado.

### Segurança
- Toda integração deve passar pela External Integrations Rule (governance-policy).
- Schemas devem ter validação agressiva de entrada.

### Testes
1. Ferramenta rejeita inputs malformados?
2. Timeout configurado?
3. Retry com backoff implementado?

---
