# Manifest Tools — Regra de Verificação Mínima de Ferramentas

> **REGRA OBRIGATÓRIA (economia de tokens):** Sempre que Fabio pedir algo que exija ferramenta, **ANTES de executar** consultar o resumo abaixo (ESTÁTICO — não re-verificar). Reportar em 1–2 linhas se precisar instalar algo. Atualizar este arquivo APÓS qualquer instalação/remoção.

> **REGRA OBRIGATÓRIA (segurança de credenciais MCP):** Ao mexer em credenciais de MCP, **NUNCA apagar nada** (nenhuma chave, header, servidor ou credential). Adicionar/modificar sempre preservando o existente. Qualquer remoção exige autorização explícita de Fabio.

> **DIRETRIZ DE ARQUITETURA DE FERRAMENTAS (aprovada por Fabio, 02/ago/2026):** **NÃO tudo via MCP.** MCP para integrações externas/agênticas (Composio, n8n, mem0, brachat-mcp); CLI/LIB nativos para operações internas determinísticas (git, docker, node/python, arquivos). MCP = expor/tornar acessível; CLI/LIB = executar operações de sistema. Exceção exige autorização explícita de Fabio. Detalhe na skill `busca-integracao-ferramentas` (S10).

> **REGRA DE PRODUÇÃO — IMAGEM PRÓPRIA (aprovada por Fabio, 02/ago/2026):** **Todo projeto de produção no git DEVE ter imagem própria (Dockerfile)**. Motivo: quem receber o repo não precisa saber configurar o ambiente — `docker compose up` sobe. Execução nativa só para desenvolvimento. O Ezra é dockerizado (`docker/Dockerfile.ezra`). Projetos do portfólio: Dockerfile próprio quando produção; compartilhar via imagem, não via instruções de setup. Referência: skill `deployment` (S12).

## Ordem de verificação (usar o resumo, não executar comandos)

1. **MCP** — já disponível? (tools abaixo)
2. **Composio** — já conectado? (apps/connections)
3. **CLI** — binário já instalado? (abaixo)
4. **LIB** — biblioteca/package já presente? (abaixo)

## Formato de resposta (mínimo de tokens)

Se já existe: `✅ via <MCP|Composio|CLI|LIB>` + executar.

Se falta:
```
⚠ falta: <item>
→ ação: <instalar LIB | compor no Composio | instalar CLI | adicionar MCP>
→ autorização de Fabio antes de instalar.
```

---

# RESUMO ESTÁTICO (verificado em 02/ago/2026)

## MCP (1 servidor: `brachat-mcp`)
Tools: `mcp_list`, `mcp_read`, `mcp_write`, `mcp_secrets_list`, `mcp_secrets_get`.
Usa: boundary de credenciais. **NÃO** executa ações externas.

## MCP remoto: `composio` (adicionado 02/ago/2026)
URL: `https://connect.composio.dev/mcp` | tipo remote | enabled true | auth OAuth (auto) — autenticado.
Ferramentas `composio_*` disponíveis no opencode.

## n8n (instalado 02/ago/2026 — Docker)
Container: `n8n` (imagem `n8nio/n8n` v2.32.7) | porta `5678` | `--restart unless-stopped`.
UI: `http://localhost:5678` (setup inicial pendente — criar owner account).
Nodes MCP Client disponíveis (`McpClient`, `McpClientTool`, `McpRegistryClientTool`, `McpTrigger`).
Para Composio: MCP Client → HTTP Streamable → `https://connect.composio.dev/mcp` + Header Auth `x-consumer-api-key`.
Regra de segurança: NUNCA apagar credenciais MCP ao mexer na integração.

## Composio
- **CLI instalado** (v0.7.21) + pip: `composio`, `composio-client`, `composio_core`.
- **API key**: presente no secrets (`COMPOSIO_API_KEY`), mas **não exportada** na env — `composio apps` falha até exportar ou `composio login`.
- **Connections**: não verificadas (exige auth). Requer `composio login`/key na env.

## CLI instalados (which ✓)
`node`, `npm`, `python3`, `pip3`, `docker`, `git`, `curl`, `ffmpeg`, `jq`, `opencode`.

## LIB — Python (pip3)
`anthropic` 0.116.0, `openai` 2.45.0, `langchain` 1.3.11, `langchain-anthropic`/`-core`/`-google-genai`/`-openai`/`-protocol`, `google-genai` 2.10.0, `google-generativeai` 0.8.6, `google-api-python-client`, `composio*`, `googletrans`, `groq`(?), `nvidia`(?).

## LIB — Node (`.opencode/node_modules`)
`@opencode-ai/*` (SDK/plugin), `typescript`, `zod`, `effect`, `@ai-sdk`, `uuid`, `yaml`, `ini`, `toml`, etc. **Raiz do projeto: sem `node_modules` e sem `package.json`.**

## Secrets disponíveis (boundary MCP — nomes)
`GOOGLE_STUDIO_API_KEY`, `COMPOSIO_API_KEY`, `GROQ_API_KEY`, `NVIDIA_API_KEY`, `OPENCODE_ZEN_API_KEY`, `OPENCODE_GO_API_KEY`, `MEM0_API_KEY`, `ACESSO_ORACLE`, `TELEGRAM_BOT_TOKEN`.

---

## Ferramentas mapeadas

| # | Tarefa/Função | MCP | Composio | CLI | LIB | Onde/Status |
|---|---|---|---|---|---|---|
| — | _Preencher conforme uso._ | | | | | |
| 1 | Workflow/automação (n8n) | — | Composio via MCP Client (HTTP Streamable) | docker (container `n8n`) | — | porta 5678; setup UI pendente |
