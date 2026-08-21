# EZRA GOVERNANCE FRAMEWORK — Full Architecture

**Autor: Fabio Everton | Agente: Ezra | Ultima atualizacao: Agosto 2026**

---

## 1. VISAO GERAL

O sistema Ezra e um agente autonomo 24/7 que opera em duas instancias OCI, sincronizadas com o Mac local. O Mac e a **fonte unica de verdade**. A OCI recebe atualizacoes apenas via clone do `.opencode`.

```
+------------------------------------------+
|            FONTE UNICA                   |
|           Mac (.opencode/)               |
|   brachat-main/  (portfolio/codigo)      |
|   .opencode/     (cerebro + skills)      |
|   ezra_governance_framework/             |
|                    |                     |
|             sync_opencode.sh             |
|            (rsync Mac -> OCI)            |
+--------------------|---------------------+
                     |
      +--------------+--------------+
      |                             |
+-----v-----------+     +----------v----------+
|  ezra_bot_1     |     |  ezra_bot_2          |
|  163.176.111.95 |     |  137.131.242.180     |
|  A1.Flex ARM    |     |  VM.Standard.E2.1    |
|                 |     |  Micro               |
| ezra-serve      |     |                      |
| bridge_tg       |     | acquirer.py          |
| parashat-bot    |     |  (12GB A1.Flex)      |
| .opencode/      |     |                      |
+-----------------+     +----------------------+
```

---

## 2. O QUE EXISTE (ESTADO ATUAL)

### 2.1 Mac (Local)

| Componente | Status | Descricao |
|-----------|--------|-----------|
| `/Users/mac/.opencode/` | OK | Cerebro do Ezra: skills, plugins, MCP, scripts, referencias |
| `/Users/mac/brachat-main/` | OK | Portfolio: 10 projetos AI/governance |
| `/Users/mac/ezra_governance_framework/` | VAZIO | Este documento — precisa de conteudo |
| `/Users/mac/.oci/` | OK | Config OCI + vault_info.json |
| `sync_opencode.sh` | OK | rsync Mac -> OCI hd |
| `opencode.json` | OK | Config global: plugin ezra-system + MCP OCI server |

### 2.2 ezra_bot_1 (163.176.111.95 — A1.Flex ARM)

| Service | Status | Descricao |
|---------|--------|-----------|
| `ezra-serve` | Rodando | OpenCode serve porta 3791, modelo Nemotron 3.5 Lightning Free |
| `bridge_telegram` | Rodando | Relay Telegram -> opencode serve (token 8555...) |
| `parashat-bot` | Rodando | Bot Torah Study, modelo openai/gpt-oss-120b (Groq), secrets do Vault |
| `.opencode/` | Sincronizado | Clone do Mac, identico (exceto vault config) |
| `governance-ledger.jsonl` | Ativo | 7.298 entradas de audit trail |

### 2.3 ezra_bot_2 (137.131.242.180 — VM.Standard.E2.1.Micro)

| Componente | Status | Descricao |
|-----------|--------|-----------|
| `acquirer.py` | Rodando | Provisionamento 12GB A1.Flex (1.945+ tentativas, 4 dias) |
| `acquirer.service` | Ativo | Systemd service, retry a cada 180s |

### 2.4 OCI Vault (12 secrets)

| Secret | Status |
|--------|--------|
| `ezra-nvidia_api_key` | OK |
| `ezra-nvidia_base_url` | OK |
| `ezra-telegram_token` | OK |
| `ezra-parashat_telegram_token` | OK |
| `ezra-grok_api_key` | OK |
| `ezra-composio_api_key` | OK |
| `ezra-mem0_api_key` | OK |
| `ezra-langfuse_secret_api_key` | OK |
| `ezra-langfuse_public_api_key` | OK |
| `ezra-opencode_go_api_key` | OK |
| `ezra-opencode_zen_api_key` | OK |
| `ezra-opencode_server_password` | OK |

---

## 3. O QUE PRECISA SER FEITO (ROADMAP)

### 3.1 IMEDIATO (esta semana)

| ID | Prioridade | Tarefa | Dependencia |
|----|-----------|--------|-------------|
| F01 | ALTA | Testar Parashat bot no Telegram (/parashat Bereshit) | Usuario enviar msg |
| F02 | ALTA | Verificar se Nemotron responde via Telegram (Ezra bot) | Teste manual |
| F03 | ALTA | Atualizar vault_info.json no Mac com 3 novos secrets | Feito, falta atualizar |
| F04 | MEDIA | Verificar que todos os servicos sobrevivem a reboot | Teste manual |

### 3.2 CURTO PRAZO (2 semanas)

| ID | Prioridade | Tarefa | Dependencia |
|----|-----------|--------|-------------|
| C01 | ALTA | Configurar mem0 para persistencia de memoria do Ezra | OCI Vault |
| C02 | ALTA | Implementar oci_server.py tools para mem0 | mem0 API |
| C03 | MEDIA | Configurar Langfuse para observabilidade | Langfuse Cloud |
| C04 | MEDIA | Implementar oci_server.py tools para Langfuse | Langfuse API |
| C05 | MEDIA | Sincronizar ezra_governance_framework/ com brachat-main/AI-Governance/ | Este doc |
| C06 | MEDIA | Criar .env para ezra_bot_1 que le do Vault (remover hardcoded) | OCI Vault |
| C07 | BAIXA | Implementar oci_server.py tool para Composio | Composio API |

### 3.3 MEDIO PRAZO (1 mes)

| ID | Prioridade | Tarefa | Dependencia |
|----|-----------|--------|-------------|
| M01 | ALTA | Implementar ezra_control_plane (Runtime Governance Gate) | spec pronto |
| M02 | ALTA | Integrar governance-ledger.jsonl com OCI Vault | Vault |
| M03 | ALTA | Implementar agent-freelancer com Playwright (9 plataformas) | Playwright |
| M04 | MEDIA | Implementar ai-job-search-agent (LinkedIn, InfoJobs) | Composio |
| M05 | MEDIA | Configurar anti-reclaim para protecao idle | OCI |
| M06 | MEDIA | Implementar nblm-refresh para NotebookLM | NotebookLM |
| M07 | BAIXA | Publicar README do ezra_agent no GitHub | brachat-main |

### 3.4 LONGO PRAZO (3 meses)

| ID | Prioridade | Tarefa | Dependencia |
|----|-----------|--------|-------------|
| L01 | ALTA | Migrar bots para A1.Flex 12GB quando adquirido | ezra_bot_2 |
| L02 | ALTA | Publicar ezra_control_plane como case study | M01 |
| L03 | MEDIA | Integrar WhatsApp Bot | — |
| L04 | MEDIA | Publicar artigo sobre governanca AI em OCI | L02 |
| L05 | BAIXA | Enviar opencode configurado para filho do Fabio | — |

---

## 4. BRACHAT-MAIN — Portfolio e Codigo

### 4.1 Estrutura

```
brachat-main/
  AI-Governance/           VAZIO — precisa de conteudo
  portfolio/
    ezra_agent/            Agente autonomo 24/7 (Telegram + OCI)
    ezra_control_plane/    SPEC PRONTO, codigo NAO IMPLEMENTADO
    ezra_curator/          RAG corporativo (Streamlit + ChromaDB)
    parashat_bot/          Bot Torah Study (Groq + MCP)
    agent_nice/            Agente domestico (self-evolution)
    essay_creator/         Pipeline 5-agentes LangGraph
    exec-email-assistant/  Roteamento intencional email
    code-connect/          Full-stack (React + NestJS)
    langchain_hands_on/    Pesquisa 4-agentes RAG
    langraph_hands_on/     LangGraph com state + persistence
  tests/
  pyproject.toml
  requirements.txt
  ruff.toml
  README.md
```

### 4.2 Projetos que Precisam de Trabalho

| Projeto | Estado | O que falta |
|---------|--------|-------------|
| ezra_control_plane | SPEC pronto | Codigo: Gate, Registry, Blink Engine, Ledger, Policy Engine |
| AI-Governance/ | VAZIO | Conteudo: politicas, frameworks, templates de governanca |
| agent-freelancer | Skill existe | Implementacao: Playwright scraping 9 plataformas |
| ai-job-search-agent | Skill existe | Implementacao: LinkedIn, InfoJobs, email via Composio |

### 4.3 Projetos Funcionais

| Projeto | Estado | Observacao |
|---------|--------|------------|
| ezra_agent | Deployed | Rodando em ezra_bot_1 |
| ezra_curator | Pronto | RAG com ChromaDB + reranking |
| essay_creator | Pronto | 5-agentes LangGraph + HITL |
| exec-email-assistant | Pronto | Intent routing + semantic memory |
| code-connect | Pronto | pnpm monorepo React + NestJS |
| langchain_hands_on | Pronto | 4-agentes RAG |
| langraph_hands_on | Pronto | LangGraph com state + persistence |

---

## 5. .OPCODE — Cerebro do Ezra

### 5.1 Estrutura (Mac = fonte unica)

```
.opencode/
  instructions/
    EZRA_SYSTEM.sudo.md    System prompt SudoLang (persona + regras)
  skills/                   33 skills (todas com SKILL.txt)
    agent-factory/          Cria agentes completos
    agent-freelancer/       Scan 9 plataformas freelance
    ai-job-search-agent/    Busca vagas + emails
    ai-privacy-security/    Protecao dados + LGPD
    governance-policy/      Politicas OPA/Rego
    memory-management/      Gestao memoria (mem0)
    observability/          Langfuse + traces
    ...                     (33 skills total)
  plugins/
    ezra-system.ts/.js      Plugin V1 (compile -> ezra-system.js)
  mcp/
    oci_server.py           MCP Server: OCI Vault + LLM + tools
    oci_sandbox.py          Sandbox isolation layer
    server.mjs              Boundary server (brachat-mcp)
    credentials/
      secrets.env           Referencias VAULT: (sem plaintext)
  scripts/
    sync_opencode.sh        rsync Mac -> OCI hd
  docs/
    oci_deployment_guide.md
    oci_integration_setup.md
  data/
    pending_tasks.md        Tasks pendentes (9 diarias + 13 longo prazo)
    agenda-semanal.md       Agenda semanal completa
    freelance-products.md   Produtos freelance
    como-conseguir-clientes.md
  reference/                Referencias persistentes
  cache/                    Cache temporario
  logs/                     Logs de execucao
  state.json                Estado persistente (session, skills, memory)
  governance-ledger.jsonl   Audit trail imutavel (SHA-256 chain)
```

### 5.2 O que o .opencode Precisa

| Componente | Estado | O que falta |
|-----------|--------|-------------|
| EZRA_SYSTEM.sudo.md | Pronto | — |
| 33 skills | Pastas criadas | SKILL.txt com conteudo real em cada uma |
| ezra-system plugin | Compilado | Teste end-to-end |
| oci_server.py | Funcional | Adicionar tools: mem0, Langfuse, Composio |
| server.mjs | Funcional | — |
| secrets.env (Vault refs) | Pronto | — |
| state.json | Funcional | Integracao com mem0 |
| governance-ledger.jsonl | Ativo | Integrar com OCI Vault |

---

## 6. EZRA_GOVERNANCE_FRAMEWORK — Este Documento

### 6.1 O que e

O `ezra_governance_framework/` e o diretorio onde Fabio mantem a documentacao de governanca do sistema Ezra. Atualmente esta VAZIO — este ARCHITECTURE.md e o primeiro conteudo.

### 6.2 O que precisa ter

| Arquivo | Descricao | Status |
|---------|-----------|--------|
| ARCHITECTURE.md | Este documento — visao full do sistema | CRIANDO |
| GOVERNANCE_POLICY.md | Politicas de governanca (OPA/Rego rules) | PENDENTE |
| DEPLOYMENT_GUIDE.md | Guia completo de deploy OCI | PENDENTE |
| SECURITY.md | Seguranca: Vault, secrets, audit trail | PENDENTE |
| LEDGER_SPEC.md | Especificacao do governance-ledger.jsonl | PENDENTE |
| CONSTITUTION.md | Hash chain, imutabilidade, compliance | PENDENTE |

### 6.3 Sync com brachat-main

O `brachat-main/AI-Governance/` tambem esta vazio. Conteudo deve ser espelhado entre `ezra_governance_framework/` e `brachat-main/AI-Governance/`.

---

## 7. OCI — Infraestrutura Cloud

### 7.1 Instancias

| Instancia | IP | Shape | OS | Funcao |
|-----------|-----|-------|-----|--------|
| ezra_bot_1 | 163.176.111.95 | A1.Flex ARM (4 OCPU, 24GB) | Ubuntu 22.04 | Bots + .opencode |
| ezra_bot_2 | 137.131.242.180 | VM.Standard.E2.1.Micro | Ubuntu 22.04 | Provisionamento 12GB |

### 7.2 Compartimentos

| Compartimento | OCID |
|---------------|------|
| ezra_Bots | ocid1.compartment.oc1..aaaaaaaace3t5eg73h6p2lu5acasysqeblsmiwsv543xvcqr4sqethau7uoa |
| ezra_core | ocid1.compartment.oc1..aaaaaaaace3t5eg73h6p2lu5acasysqeblsmiwsv543xvcqr4sqethau7uoa |

### 7.3 OCI Vault

| Recurso | ID |
|---------|-----|
| Vault | ocid1.vault.oc1.sa-saopaulo-1.ffvimjo6aaeza... |
| Master Key | ocid1.key.oc1.sa-saopaulo-1.ffvimjo6aaeza... |
| Endpoint | https://ffvimjo6aaeza-management.kms.sa-saopaulo-1.oraclecloud.com |
| Regiao | sa-saopaulo-1 |
| Tenancy | ocid1.tenancy.oc1..aaaaaaaa5huauyfyakeckggssoykg5armfcs4osmm3b4jmypswsu5k3wozpq |

### 7.4 O que falta na OCI

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Migrar bots para 12GB A1.Flex | ALTA | Quando acquirer.py conseguir provisionar |
| Adicionar OCI Logging | MEDIA | Logs centralizados dos servicos |
| Adicionar OCI Monitoring | MEDIA | Alertas de CPU, memoria, disco |
| Configurar OCI Notifications | BAIXA | Notificacoes via email/Telegram |

---

## 8. BOT PARASHAT — Torah Study

### 8.1 O que faz

Bot Telegram que gera estudos semanais da Torah pelo racionalismo judaico. Busca parashot de `btf.org.br/parashot`, combina com NotebookLM (131 fontes), e gera analise de 21 secoes usando Groq LLM.

### 8.2 Stack

- **Bot**: python-telegram-bot 21.10
- **LLM**: Groq API (openai/gpt-oss-120b)
- **RAG**: NotebookLM CLI (TORAH_STUDIES notebook, 131 fontes)
- **Scraping**: requests + BeautifulSoup (btf.org.br)
- **Secrets**: OCI Vault via MCP (oci_vault_get_secret)

### 8.3 Fluxo

```
Usuario -> /parashat Bereshit
  -> bot.py recebe comando
  -> study.py busca parashot em btf.org.br/parashot
  -> study.py busca contexto (NotebookLM + studies/)
  -> mcp_client.py envia para llm_mcp_server.py
  -> llm_mcp_server.py chama Groq API
  -> Resposta volta para bot.py
  -> bot.py envia para Telegram (chunks de 4000 chars)
```

### 8.4 Arquivos

| Arquivo | Descricao |
|---------|-----------|
| bot.py | Bot principal: handlers, polling, daily job |
| study.py | Lookup parashah: fetch, find, build context |
| mcp_client.py | Cliente MCP JSON-RPC para llm_mcp_server.py |
| llm_mcp_server.py | Servidor MCP leve: proxy LLM via OpenAI API |
| prompt.txt | Template 21 secoes racionalistas (176 linhas) |
| bot.env | Config: LLM_MODEL, LLM_BASE_URL (sem secrets) |

### 8.5 O que falta no Parashat Bot

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Testar end-to-end via Telegram | ALTA | Envio manual de /parashat |
| Adicionar daily study automático | MEDIA | Envio as 09:00 BRT para grupo |
| Integrar mais fontes de estudo | BAIXA | Expandir materials em studies/ |
| Monitoramento de erros | MEDIA | Alertas quando LLM falha |

---

## 9. BOT EZRA — Autonomous Agent

### 9.1 O que faz

Agente autonomo 24/7 que planeja, executa, lembra e aprende. Escaneia plataformas freelance, gerencia agenda, persiste memoria via mem0, e enforce governanca em toda acao.

### 9.2 Stack

- **Brain**: OpenCode serve (porta 3791, modelo Nemotron 3.5 Lightning Free)
- **Interface**: Telegram via bridge_telegram.js (relay zero-logica)
- **Memory**: mem0 (long-term), state.json (short-term)
- **Governance**: governance-ledger.jsonl (SHA-256 hash chain)
- **Skills**: 33 skills em .opencode/skills/
- **Plugins**: ezra-system.ts (persona + regras)
- **MCP**: oci_server.py (Vault + LLM + tools)

### 9.3 Fluxo

```
Fabio -> Telegram -> bridge_telegram.js
  -> opencode serve:3791
  -> EZRA_SYSTEM.txt (persona + regras)
  -> skill routing (manifest.txt)
  -> skill execution
  -> governance gate (ledger)
  -> resposta -> Telegram -> Fabio
```

### 9.4 O que falta no Ezra Bot

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Configurar mem0 para persistencia | ALTA | Criar tool MCP para mem0 |
| Implementar agent-freelancer | ALTA | Playwright scraping 9 plataformas |
| Implementar ai-job-search-agent | ALTA | LinkedIn, InfoJobs, email |
| Configurar Langfuse | MEDIA | Observabilidade (traces, custo) |
| Integrar Composio | MEDIA | Gmail, LinkedIn APIs |
| Anti-reclaim | MEDIA | Protecao idle (se necessario) |
| nblm-refresh | BAIXA | Auth cookie refresh diario |

---

## 10. FLUXO DE DADOS E SINCRONIZACAO

### 10.1 Regra Fundamental

**Mac = fonte unica de verdade.**

- OCI recebe atualizacoes APENAS via `sync_opencode.sh` (rsync Mac -> OCI)
- Nunca editar direto na OCI (exceto logs e dados gerados)
- secrets.env no Mac tem referencias VAULT: (sem plaintext)
- Bots na OCI leem secrets via MCP tool (oci_vault_get_secret)

### 10.2 sync_opencode.sh

```
Mac .opencode/ --(rsync -avz --delete)--> OCI .opencode/

Exclui: *.pem, *.key, node_modules/, cache/, logs/, state.json
Inclui: secrets.env (com referencias VAULT:), scripts/, mcp/, skills/
```

### 10.3 O que falta na sincronizacao

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Automatizar sync via cron/launchd | ALTA | Sync automatico a cada X minutos |
| Adicionar verificacao pos-sync | MEDIA | Testar servicos apos sync |
| Rollback automatico | BAIXA | Se sync corromper, reverter |

---

## 11. SEGREDO E VAULT

### 11.1 Arquitetura de Seguranca

```
Mac (secrets.env com referencias VAULT:)
  |
  +--> sync_opencode.sh --> OCI .opencode/secrets.env (mesmas referencias)
         |
         +--> bot.py le referencias
         |
         +--> mcp_client.py chama oci_server.py
         |
         +--> oci_server.py usa OCI SDK
         |
         +--> OCI Vault retorna valor real
```

### 11.2 Regras

1. NUNCA plaintext em secrets.env
2. NUNCA commits de secrets
3. Bots leem via MCP (oci_vault_get_secret)
4. Vault e a unica fonte de verdade para secrets
5. vault_info.json no Mac documenta IDs (nao valores)

### 11.3 O que falta

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Atualizar vault_info.json com 3 novos secrets | ALTA | opencode_go, opencode_zen, server_password |
| Rotacao de secrets | MEDIA | Rotacionar keys periodicamente |
| Audit log no Vault | BAIXA | Rastrear quem acessou cada secret |

---

## 12. GOVERNANCA RUNTIME

### 12.1 governance-ledger.jsonl

Cada acao do agent gera uma entrada no ledger:

```json
{
  "block_id": 1,
  "prev_hash": "abc123...",
  "ts": "2026-08-20T14:22:30Z",
  "action": "tool_call",
  "tool": "oci_vault_get_secret",
  "args": {"secret_name": "ezra-grok_api_key"},
  "outcome": "allow",
  "hash": "def456..."
}
```

### 12.2 ezra_control_plane (SPEC PRONTO, NAO IMPLEMENTADO)

O control plane e um gate que intercepta toda tool call e decide: allow, deny, ou approve (HITL).

Componentes:
- **Registry**: tool -> effect mapping
- **Blink Engine**: damage cards, risk scoring
- **Policy Engine**: YAML rules, OPA/Rego
- **Credential Broker**: derived tokens, scoped access
- **Ledger**: SQLite, append-only, SHA-256 chain

### 12.3 O que falta

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Implementar ezra_control_plane | ALTA | Seguir SPEC.md em brachat-main |
| Integrar ledger com Vault | ALTA | Audit trail imutavel na OCI |
| Definir politicas OPA/Rego | ALTA | Regras de governanca por tool |
| Teste de penetracao | MEDIA | Verificar que agent nao bypassa gate |

---

## 13. PLATAFORMAS FREELANCER

### 13.1 Plataformas (9 total)

| Plataforma | URL | Variavel Usuario | Variavel Senha |
|------------|-----|-----------------|----------------|
| 99Freelas | 99freelas.com.br | 99_FREELA_USUARIO | 99_FREELA_SENHA |
| Workana | workana.com.br | WORKANA_USUARIO | WORKANA_SENHA |
| Get on Board | getonbrd.com | GET_ON_BOARD_USUARIO | GET_ON_BOARD_SENHA |
| GeekHunter | geekhunter.com.br | GEEKHUNTER_USUARIO | GEEKHUNTER_SENHA |
| Turing | turing.com | TURING_USUARIO | TURING_SENHA |
| Arc.dev | arc.dev | ARCDEV_USUARIO | ARCDEV_SENHA |
| Braintrust | braintrust.com | BRAINTRUST_USUARIO | BRAINTRUST_SENHA |
| Remotar | remotar.com.br | REMOTAR_USUARIO | REMOTAR_SENHA |
| Freelancer | freelancer.com | FREELANCER_USUARIO | FREELANCER_SENHA |

### 13.2 O que falta

| Item | Prioridade | Descricao |
|------|-----------|-----------|
| Implementar agent-freelancer | ALTA | Playwright scraping diario |
| Implementar ai-job-search-agent | ALTA | LinkedIn + InfoJobs + email |
| Relatorios via Telegram | MEDIA | Scans as 09:00 e 17:00 |
| Filtro por relevancia | MEDIA | IA para filtrar vagas relevantes |

---

## 14. CERTIFICACOES E AGENDA

### 14.1 Certificacoes em Andamento

| Certificacao | Prioridade |
|-------------|-----------|
| AIGP (AI Governance Professional) | Alta |
| CIPP/E (IAPP) | Alta |
| CKA (Kubernetes) | Alta |
| GH-600 (Git Agent) | Alta |
| OCI Generative AI Professional | Alta |
| OCI Architect Associate | Alta |
| AWS AI Practitioner | Alta |
| Python Institute | Alta |
| Pos-Graduacao GRC Tech (UnP) | Alta |

### 14.2 Scans Automaticos

| Agente | Horario | Acao |
|--------|---------|------|
| agent-freelancer | 09:00, 17:00 | Scan 9 plataformas -> Telegram |
| ai-job-search-agent | 09:00, 17:00 | Scan vagas + emails -> Telegram |
| ezra.commit | 18:00 | Commit automatico GitHub |
| ezra.backup | 9h, 13h, 17h, 21h | Backup Google Drive |
| parashat-bot | 09:00 | Daily Torah study |

---

## 15. PROJETOS LONGO PRAZO

| ID | Tarefa | Dependencia | Status |
|----|--------|-------------|--------|
| P01 | WhatsApp Bot (integrar) | — | Pendente |
| P02 | Integrate UI tools | — | Pendente |
| P03 | Job Search Agent (completar) | — | Pendente |
| P04 | Criar agente do challenge | — | Pendente |
| P05 | Ajustar git e LinkedIn | — | Pendente |
| P06 | Verificar 12GB A1.Flex | — | Em progresso (acquirer.py) |
| P07 | Migrate bots to 12GB A1.Flex | P06 | Pendente |
| P08 | Fazer schedule TCU junto com CGU | — | Pendente |
| P09 | Enviar opencode configurado para filho | — | Pendente |
| P12 | Transcrever material WhatsApp dev | — | Pendente |
| P13 | Vasculhar diariamente edital TCU/SEFAZ-DF | — | Pendente |

---

*Documento gerado por Ezra em 2026-08-20. Atualizar apos cada milestone.*
