# Boundary MCP do Ezra OS

Esta pasta é a **boundary de segurança** do Mac. Dados aqui dentro são acessíveis
**apenas** pelo servidor MCP (`server.mjs`) com tools whitelisted — e as permissões
do opencode bloqueiam leitura/escrita direta de `mcp/**`.

## Estrutura

| Caminho | Conteúdo | Classificação |
|---|---|---|
| `credentials/secrets.env` | API keys (Composio, Groq, NVIDIA, Google Studio, etc.) | **Restricted** |
| `audit.log` | Log de acessos a credenciais (append-only) | **Internal** |

> Nota: `personal/` foi removido da boundary a pedido de Fabio. Dados pessoais
> (currículos, schedules) vivem como conteúdo dos subagentes em `.opencode/agents/`.

## Tools do servidor MCP

| Tool | Ação | Restrição |
|---|---|---|
| `mcp_list` | Lista arquivos/pastas | dentro da boundary |
| `mcp_read` | Lê texto de arquivo | sem `credentials/secrets.env` |
| `mcp_write` | Grava arquivo | bloqueado p/ `server.mjs`, `README.md`, `.gitignore`, `audit.log`, `credentials/` |
| `mcp_secrets_list` | Lista nomes das chaves | nunca valores |
| `mcp_secrets_get` | Retorna 1 chave por nome | auditado no `audit.log` |

## Regras

- Nenhum caminho pode escapar da boundary (path traversal bloqueado, inclusive via symlink).
- Credenciais nunca são lidas por `mcp_read` — somente via `mcp_secrets_*`.
- `audit.log` é append-only pelo servidor; escrita via tool é bloqueada.
- Quem protege o `server.mjs` é o permission config do opencode (`read`/`edit` deny em `mcp/**`).

## Origem dos dados

- `credentials/secrets.env` ← ex-`integrations/APIS/.env.log` (normalizado, original deletado com aprovação de Fabio em 2026-07-31).
