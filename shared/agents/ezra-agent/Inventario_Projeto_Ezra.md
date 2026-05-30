# INVENTÁRIO DO PROJETO — Ezra_Agent

**Last Updated:** 25/04/2026 | Phase 2 → Phase 3 Transition
**Current Phase:** Phase 3 — Contracts & Interfaces

---

## 1. VISÃO MACRO

> Agente autônomo conversacional via Telegram, com memória persistente (Supabase + Vault local via sync), skills modulares declarativas/executáveis, fallback de LLMs e containerização Docker para deploy em Vercel/Render.

### Atores

| Actor                     | Type       | Description                                                                                   |
| ------------------------- | ---------- | --------------------------------------------------------------------------------------------- |
| Usuário Principal (Fabio) | Admin/User | Único interagente via Telegram; gerencia skills, avalia outputs e consulta vault no Obsidian. |

### Fluxos Principais

1. Ingestão & Roteamento: Telegram → `bridge.py` → `Skills.yaml` → Injeta `personality` + carrega `specific` → Executa (Docker subprocess) → Responde.
2. Persistência & Logging: Toda interação gera logs JSON estruturados (4 categorias) + nota Obsidian (.md com frontmatter, CoT, tags, links, avaliação).
3. LLM Fallback: `qwen3.6` → `glm-5.1` → `gemma3` (trigger: latência >2s, erro HTTP/rate limit, ou queda de qualidade detectada).

### Integrações Externas

- Telegram Bot API
- Supabase (PostgreSQL + Storage)
- Obsidian Vault (via Supabase Storage + custom sync scripts)
- Git (versionamento de skills, prompts e vault)
- Cloud Provider (Vercel/Render via Docker)

---

## 2. TECH STACK

| Layer              | Technology                               | Version | Justification                                                            |
| ------------------ | ---------------------------------------- | ------- | ------------------------------------------------------------------------ |
| Runtime/Deploy     | Docker                                   | 24+     | Portabilidade Vercel/Render; isolamento de execução                      |
| Orquestração       | Docker Compose / Render CLI              | -       | Deploy consistente entre ambientes                                       |
| Language           | Python                                   | 3.11+   | Ecossistema maduro para AI agents; async, subprocess, typing nativo      |
| Telegram Interface | python-telegram-bot                      | 20+     | Biblioteca oficial; suporte a async, webhooks, rate limiting             |
| LLM Client         | OpenAI-compatible + custom fallback      | -       | Suporte a múltiplos providers; fallback controlado por latência/erro     |
| Memory DB          | Supabase (PostgreSQL)                    | 15+     | Persistência fora do container efêmero; JSONB para logs estruturados     |
| Vault Sync         | Supabase Storage + Custom Python Scripts | -       | Sync bidirecional; container salva .md → script local puxa para Obsidian |
| Logging            | structlog + Python logging               | -       | Logs JSON estruturados; níveis DEBUG a CRITICAL; sanitização de secrets  |
| Skills Registry    | YAML + Pydantic                          | -       | Leitura declarativa de Skills.yaml; validação de schema pré-execução     |
| Skill Execution    | subprocess + asyncio                     | -       | Execução isolada de scripts Python/Shell; timeout controlado             |
| Config Management  | pydantic-settings + .env                 | -       | Validação em startup; separação de secrets via env vars                  |

### Architectural Pattern

- Pattern: Event-Driven Agent with Modular Skill Registry + Persistent Knowledge Vault
- Justification: Separa roteamento, execução e persistência; permite evolução incremental de skills; garante memória científica no Obsidian com sync controlado.

### Performance Targets

- RPS: 1-5 req/s (pico 10)
- SLA Feedback: <2s (typing indicator)
- SLA Resposta Completa: <30s (com skill executável)
- Vault Sync Latency: <60s (assíncrono)
- Data Volume: Logs 90 dias (debug), 2 anos (auditoria); Vault limitado por storage Supabase + Git LFS

---

## 3. COMPONENTS

### Component: `bridge.py` (Telegram Gateway)

- Responsibility: Receber mensagens Telegram, autenticar usuário, rotear para executor, gerenciar estado de sessão
- Connects To: Telegram Bot API, Skill Router, Structured Logger, Session Store
- Owned By: Ezra_Agent
- Status: ✅ Ready

### Component: `Skill Router`

- Responsibility: Ler `Skills.yaml` com validação Pydantic, carregar skill permitida, injetar personality skills, delegar execução
- Connects To: `SKILLS_STORAGE/`, `vault/Ezra_mem`, LLM Orchestrator, Structured Logger
- Owned By: Ezra_Agent
- Status: ✅ Ready

### Component: `LLM Orchestrator`

- Responsibility: Gerenciar fallback (qwen3.6 → glm-5.1 → gemma3), injetar prompt + contexto, capturar Chain of Thought, medir latência
- Connects To: LLM Providers API, Obsidian Writer, Structured Logger, Fallback State Store
- Owned By: Ezra_Agent
- Status: ✅ Ready

### Component: `Obsidian Writer + Sync`

- Responsibility: Estruturar nota .md com frontmatter; salvar no Supabase Storage; script local sincroniza para Obsidian
- Connects To: Supabase Storage, Custom Sync Script, Structured Logger
- Owned By: Ezra_Agent
- Status: ⚠️ Pending Phase 3 (contract definition)

### Component: `Structured Logger`

- Responsibility: Emitir logs JSON em 4 categorias; sanitização de dados sensíveis; retenção configurável
- Connects To: Supabase Logs Table, Console
- Owned By: Ezra_Agent
- Status: ✅ Ready

### Component: `Skill Executor`

- Responsibility: Executar skills `executable` via subprocess com timeout, capturar stdout/stderr, isolar contexto
- Connects To: `SKILLS_STORAGE/specific/`, Structured Logger, Resource Monitor
- Owned By: Ezra_Agent
- Status: ✅ Ready

---

## 4. CONTRACTS & INTERFACES

_(A ser entregue na FASE 3 — Contracts & Interfaces)_

- OpenAPI 3.1: Webhook Telegram, Endpoints de Sync, Healthcheck
- Internal Contracts: Strict typing para Skill Registry, LLM Request/Response, Log Entry, VaultNote Sync
- Schema DB: Migration scripts para PostgreSQL + JSONB constraints

---

## 5. DATA SCHEMA

### Entity: InteractionLog

| Field              | Type        | Constraints                                         | Description                     |
| ------------------ | ----------- | --------------------------------------------------- | ------------------------------- |
| id                 | UUID        | PK                                                  | Identificador único             |
| timestamp          | TIMESTAMPTZ | NOT NULL, default now()                             | Momento da interação            |
| actor_id           | TEXT        | NOT NULL                                            | ID do usuário                   |
| message_input      | TEXT        | -                                                   | Texto recebido do Telegram      |
| message_output     | TEXT        | -                                                   | Resposta gerada pelo agente     |
| skill_used         | TEXT        | FK → Skills.id                                      | Skill executada, se aplicável   |
| llm_used           | TEXT        | -                                                   | Modelo LLM que gerou a resposta |
| latency_ms         | INTEGER     | CHECK >= 0                                          | Tempo total de processamento    |
| fallback_triggered | BOOLEAN     | default false                                       | Se o fallback foi acionado      |
| category           | TEXT        | CHECK IN ('audit','security','error','performance') | Categoria do log                |
| metadata           | JSONB       | -                                                   | Dados estruturados adicionais   |
| sanitized          | BOOLEAN     | default true                                        | Confirmação de sanitização      |

### Entity: VaultNote

| Field                 | Type        | Constraints                    | Description                      |
| --------------------- | ----------- | ------------------------------ | -------------------------------- |
| id                    | UUID        | PK                             | Identificador da nota            |
| file_path             | TEXT        | UNIQUE, NOT NULL               | Caminho relativo no vault        |
| frontmatter           | JSONB       | -                              | Metadados YAML parseados         |
| content_hash          | TEXT        | -                              | SHA256 para detecção de conflito |
| last_modified         | TIMESTAMPTZ | -                              | Última modificação               |
| sync_source           | TEXT        | CHECK IN ('container','local') | Origem da última atualização     |
| supabase_storage_path | TEXT        | -                              | Caminho no bucket do Supabase    |

---

## 6. ARCHITECTURAL RISK LOG

| ID   | Risk                                              | Severity | Status                                                      |
| ---- | ------------------------------------------------- | -------- | ----------------------------------------------------------- |
| R-01 | Conflito de sync bidirecional no vault            | Medium   | ⚠️ Mitigação: resolução por timestamp + hash                |
| R-02 | Timeout em skill executável bloqueando resposta   | Medium   | ✅ Mitigação: subprocess com timeout + fallback de resposta |
| R-03 | Vazamento de secrets via logs ou erro             | High     | ✅ Mitigação: sanitização pré-escrita + pydantic-settings   |
| R-04 | Custo de LLM fallback em cadeia                   | Low      | ⚠️ Monitoramento de tokens via metadata                     |
| R-05 | Dependência de conexão com Supabase em serverless | Medium   | ⚠️ Mitigação: retry com backoff + cache local (cache.py)    |
