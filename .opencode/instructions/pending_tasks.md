# Pending Tasks

Schema: cada item possui `status` (pending | in_progress | done | blocked), `prioridade`, `dependencias` e `autorizacao`. Numeração original preservada. Remoção apenas com autorização explícita de Fabio.

## Em aberto

### 28. Instalar n8n e conectar ao Composio (via dashboard de clientes)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: n8n v2.32.7 instalado via Docker (container `n8n`, porta 5678, restart automático); owner account criada (`jae.engenharia@gmail.com`); credenciais `N8N_EMAIL`/`N8N_PASSWORD` gravadas no MCP (11 chaves no secrets.env); regra de acesso na skill agent-factory (S01) — usar n8n = entrar na URL; direção definida: Ezra acessa n8n diretamente via MCP Server Trigger (grátis, sem Composio pago); workflow `ezra-mcp` (id 8Q8c3ttyF4gPqijS) ativo, endpoint `/webhook/mcp`.

### 1. Ajustar cronograma do TCDF
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: títulos simplificados para "Dia N" (115 cabeçalhos); dia da semana e data removidos. Diagnóstico: 104/115 datas tinham dia da semana errado (calendário 2027 aplicado a datas 2026) e Dia 1 tinha "30/ago" (corrigido). Header (30/jul início, 22/nov prova) e períodos/simulados confirmados corretos.

### 2. Configurar os IPs públicos da OCI
- status: pending | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio

### 3. Colocar os bots na OCI (Ezra e Parashat e suas atribuições)
- status: pending | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio

### 4. Colocar o script de busca de nuvem na OCI (captura dos 2 gigas)
- status: pending | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio

### 5. Fazer cronograma diário de estudos
- status: pending | prioridade: media | dependencias: nenhuma | autorizacao: Fabio

### 6. Colocar brachat-main dentro do Docker
- status: in_progress | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Progresso: estrutura `docker/` criada e validada — `Dockerfile.ezra` (base `ghcr.io/anomalyco/opencode` Alpine, +git/curl/jq/python3/nodejs/npm, plugins npm install, `opencode serve --port 3789`), `docker-compose.yml` (ezra + n8n + open-webui com volumes), `.dockerignore` (também copiado para a raiz do contexto) e `.env.example` (12 segredos + `OPENCODE_SERVER_PASSWORD`). Build de teste OK (imagem ezra 1.18.11); servidor headless validado: HTTP 200 em `http://0.0.0.0:3789`. Falta: subir via `docker compose` com `secrets.env` local, dockerizar n8n/open-webui conforme infra atual e mover Ezra do host nativo para o container.

### 29. Subir tudo para o GitHub (commit + push)
- status: in_progress | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Progresso: diagnóstico feito — 55 arquivos deletados (pasta `agents/` não existe mais no disco, mas `.gitignore` ainda a referencia); arquivos modificados (opencode.json, .gitignore, portifolio/*) e novos (certifications/, docker/); estrutura docker/ pronta. Falta: revisar .gitignore (remover referência a agents/), stage seletivo, commit e push para `origin/main`.

### 7. Terminar curso Oracle One
- status: pending | prioridade: media | dependencias: nenhuma | autorizacao: Fabio

### 8. Verificar se falta algo no harness do agente e se há algo no Composio para integrar ao Ezra
- status: pending | prioridade: media | dependencias: nenhuma | autorizacao: Fabio

### 9. Traduzir todos os documentos para inglês
- status: pending | prioridade: baixa | dependencias: nenhuma | autorizacao: Fabio

### 10. Colocar o challenge no NotebookLM
- status: pending | prioridade: media | dependencias: nenhuma | autorizacao: Fabio

### 11. Verificar se há regra de, em toda checagem, verificar no Composio ou no MCP (criar manifest tools)
- status: pending | prioridade: media | dependencias: nenhuma | autorizacao: Fabio

### 12. Verificar qual pós-graduação fazer
- status: pending | prioridade: baixa | dependencias: nenhuma | autorizacao: Fabio

### 13. Preencher o `manifest_tools.md` com todas as ferramentas necessárias
- status: pending | prioridade: media | dependencias: orientação de Fabio sobre a regra de checagem (item 11) | autorizacao: Fabio

### 14. Corrigir o erro EPERM na escrita do `governance-ledger.jsonl` (bloqueia toda auditoria)
- status: done | prioridade: critica | dependencias: nenhuma | autorizacao: Fabio
- Resultado: flag macOS `uchg` removido via `chflags nouchg`; ledger gravando normalmente; entrada `eperm_flag_removed` registrada.

### 15. Corrigir `hashState` para hashear o estado real em `memory-persistence.ts` (F-04)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: `hashState(readState(root))` para before/after, substituindo o objeto sintético.

### 16. Resolver contradição de leitura de memória entre persona.md e mandatory_fixed_rules.md (F-02)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: Opção A — persona.md MEMORY PROTOCOL restrito; reads apenas mediante iniciação explícita de Fabio.

### 17. Corrigir referência à Constitution apontando para a skill `governance-policy` (F-03)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: AUTHORITY HIERARCHY → `.opencode/skills/governance-policy/SKILL.md` (sem arquivo novo).

### 18. Adicionar ledger no handler `session.error` (F-13)
- status: done | prioridade: media | dependencias: nenhuma | autorizacao: Fabio
- Resultado: `session.error` → `appendLedger` (actor `memory-persistence`, action `session_error`, risk Medium).

### 19. Adicionar ledger no hook `experimental.session.compacting` (F-21)
- status: done | prioridade: media | dependencias: nenhuma | autorizacao: Fabio
- Resultado: try/catch + `appendLedger` (action `compaction_context_injected`) + `logHookError`.

### 20. Adicionar guarda de double-flush no `flushMem0` (in-flight) (F-15)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: marca pending → in-flight + `writeState` antes do loop de awaits.

### 21. Corrigir race condition no `flushMem0` (re-ler + merge antes de escrever) (F-07)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: re-lê estado fresco; merge apenas dos status de resultado; `results` Map `ts → flushed|error`.

### 22. Fechar gap de escopo MCP no `skill-gate` (mcp_write/mcp_secrets_get) (F-10)
- status: done | prioridade: alta | dependencias: nenhuma | autorizacao: Fabio
- Resultado: `GATED_MCP_PREFIXES = ["mcp__brachat-mcp__"]` + `isGated()`; ferramentas MCP do servidor passam a exigir skill.

### 23. Adicionar markers em inglês e tag `blocker` no `isDecisionLike` (F-12/F-14)
- status: done | prioridade: media | dependencias: nenhuma | autorizacao: Fabio
- Resultado: markers EN adicionados; discriminador `blocker|preference|decision` com clusters próprios.

### 24. Adicionar coluna Status no `manifest.md` (F-17)
- status: done | prioridade: media | dependencias: nenhuma | autorizacao: Fabio
- Resultado: coluna Status + legenda ACTIVE|DRAFT|DEPRECATED|UNDER_REVISION; flag `uchg` do manifest removido.

### 25. Migrar `pending_tasks.md` para schema estruturado preservando numeração (F-18)
- status: done | prioridade: media | dependencias: nenhuma | autorizacao: Fabio
- Resultado: schema estruturado com status/prioridade/dependencias/autorizacao; numeração original 1–27 preservada.

### 26. Adicionar logging de auditoria no `lean-boot.ts` (F-05/F-20)
- status: done | prioridade: media | dependencias: nenhuma | autorizacao: Fabio
- Resultado: `experimental.chat.system.transform` registra ledger (`system_prompt_skills_stripped`, risco Low, hashes before/after).

### 27. Adicionar nota formal de token_cost nos plugins (F-19)
- status: done | prioridade: baixa | dependencias: nenhuma | autorizacao: Fabio
- Resultado: nota formal em `memory-core.ts` (LedgerEntry.token_cost); runtime não expõe custo — decisão aprovada, sem instrumentação.

## Resolvidas

_Nenhuma tarefa resolvida aguardando autorização de remoção._
