# TUTORIAL & SYSTEM CONTRACTS — BRACHÁT Ecosystem

> ⚡ **AUTO-LOAD & SOURCE OF TRUTH:** This document contains 100% of the system rules, contracts, and architecture. All future audits MUST base their evaluation solely on this document.
> 🔒 **MANDATORY ACTION:** Read this file FIRST before taking any other action. Do not re-index the entire project.

---

## 0. ABSOLUTE SYSTEM RULES (From GEMINI.md)

- **OpenCode:** DIRECTLY CONNECTED to the agent.
- **Ezra:** Central intelligence and system coordinator.
- **Gilmario:** Agent responsible for editing Aisio's book (created on 05/29/2026).
- **Global WhatsApp Business:** +55 61 99650-6881 (Chromium/Puppeteer).
- **Aisio Contact:** +55 61 99116-3206.

## Efficiency and LLM Rules (MANDATORY)
- **Minimum Output:** ALWAYS respond with the lowest possible number of tokens (~67 tokens).
- **Minimum Input:** Read/search only what is strictly necessary.
- **Temperature:** `0.0` for any model. Deterministic and direct answers.
- **Documents:** Any generated document MUST BE WRITTEN IN **ENGLISH**.
- **Chat:** Respond in Brazilian Portuguese, straight to the point.

## File Rules
- **Subagents:** Only for justified parallelism.
- **Reading:** Use `StartLine`/`EndLine`. Do not index `node_modules`, `dist`, or binaries. Prefer `grep_search`.
- **Editing:** Use `multi_replace_file_content` for non-contiguous, `replace_file_content` for contiguous. NEVER rewrite entire files.
- **References:** Use `@filename` when referencing files.

## Memory and Context (Must REALLY work)
- Save permanent facts (phones, decisions) to Mem0 immediately with `user_id: "fabio"`.
- Use `CONVERSATION_SUMMARY.md` for temporary context.
- Do not re-explain what has already been done.

## Code Standards
- Python / Node.js.
- Clean code, no `console.log`.
- Commits: `type: short description`.


---

## 1. ARCHITECTURE & OVERVIEW


O BRACHÁT é um ecossistema de **agentes de IA** que trabalham juntos para te ajudar a estudar, caçar vagas, criar projetos e manter sua rotina. Cada agente tem um papel específico, e todos se conectam através de um **orquestrador central**.

### Como funciona por cima

**O Cérebro (Orquestrador)**  
Quando você abre uma sessão, o **Orquestrador** entra em ação primeiro. Ele lê o relógio (`date`), consulta seu estado (`state.json`), descobre qual é o horário e a atividade da sua rotina, e **despacha o agente certo** para aquele momento. Ele não pensa nem executa tarefas — só gerencia quem faz o quê e quando.

**Os 12 Agentes Diários**  
Cada um cuida de uma área específica da sua vida:
- **Job Hunter** — varre vagas de emprego
- **Inglês** — prepara exercícios de vocabulário e leitura
- **Estudos** — acompanha seu progresso no cronograma
- **Portfólio** — cria drafts de posts e projetos
- **Python** — material de Python Masterclass
- **Google Skills** — cobra seus cursos
- **Torá** — lição e reflexão
- **Filosofia** — leitura e discussão
- **PMP** — material de certificação
- **ML Engineer** — estudos de machine learning
- **Certificações** — acompanha certificações
- **Freelancer** — encontra trabalhos freelas

Eles se comunicam via `cache.json` — cada um salva seu progresso num arquivo, e o Orquestrador lê esses arquivos para saber o que já foi feito.

**Os 5 Diretores**  
São agentes especialistas que fiscalizam e orientam áreas maiores:
- **Aísio** — Diretor de Governança. Vigia se os outros agentes estão seguindo as regras. É o único que pode bloquear ações não autorizadas.
- **Nice** — Diretora de Marketing e Voz do Cliente. Cuida da sua presença online e comunicação.
- **Gilmário** — Diretor Técnico. Supervisiona qualidade técnica dos projetos.
- **Jessica** — Diretora de Design. Cuida da identidade visual e UX.
- **Josué** — Diretor de Estratégia. Planejamento e visão de longo prazo.

**Os Serviços de Fundo (Builder)**  
O Builder contém os scripts que rodam 24h por dia: o **ClickUp Daemon** sincroniza suas tasks, o **Telegram Bridge** mantém você conectado via Telegram, e os **daemons** garantem que tudo fique ligado mesmo com o Mac fechado.

**Como a Informação Flui**
```
Orquestrador → lê state.json + dispatch-schedule
            → descobre horário
            → ativa o agente do momento
            → agente lê cache.json de outros agentes
            → agente executa tarefa
            → agente salva progresso no próprio cache.json
            → Orquestrador consolida no fim do dia
```

---

## 2. FUNÇÃO DAS PASTAS

```
brachat-main/                         ← RAIZ DO ECOSSISTEMA
│
├── ARCHITECTURE.md                   ← Este documento
├── README.md                         ← Descrição geral do projeto
├── TUTORIAL.md                       ← Passo a passo de como usar
├── state.json                        ← Estado central de tudo (canônico)
├── opencode.json                     ← Config do OpenCode (CLI de IA)
├── .opencode/                        ← Config interna do OpenCode
│   └── instructions/memory.md        ← Instrução carregada em toda sessão
│
├── assistant_agents/                 ← CÉREBRO DO SISTEMA — onde vivem os agentes
│   │
│   ├── state.json                    ← Perfil do usuário (Fábio), rotina, fases de estudo
│   ├── REGRAS.md                     ← Regras que todos os agentes seguem
│   ├── AUDITORIA.md                  ← Checklist de verificação do sistema
│   ├── README.md + LICENSE           ← Documentação e licença
│   │
│   ├── .opencode/                    ← Config dos agentes dentro do OpenCode
│   │   └── agent/
│   │       ├── orquestrador.md       ← O cérebro: dispatch de agentes por horário
│   │       └── dispatch-schedule.md  ← Tabela de horários: quem faz o quê e quando
│   │
│   ├── daily/                        ← AGENTES DIÁRIOS (um para cada matéria)
│   │   ├── estudos/                  ← Rastreador de progresso do cronograma
│   │   ├── ingles/                   ← Professor de inglês (C2 Framework)
│   │   ├── python/                   ← Python Masterclass
│   │   ├── torah/                    ← Lição da Torá
│   │   ├── filosofia/                ← Filosofia e reflexão
│   │   ├── certificacoes/            ← Certificações profissionais
│   │   ├── google-skills/            ← Cursos Google
│   │   ├── pmp/                      ← Certificação PMP
│   │   ├── ml-engineer/             ← Machine Learning
│   │   ├── portfolio/               ← Portfólio e projetos
│   │   ├── job-hunter/              ← Caça a vagas de emprego
│   │   └── freelancer/              ← Trabalhos freelancer
│   │   │
│   │   └── (cada pasta contém:)
│   │       ├── AGENT.md             ← Personalidade e instruções do agente
│   │       ├── cache.json           ← Progresso salvo do agente
│   │       └── metadata.json        ← Metadados (categoria, tags)
│   │
│   ├── directors/                    ← DIRETORES (agentes especialistas)
│   │   ├── aisio/                    ← Governança, compliance, auditoria
│   │   ├── nice/                     ← Marketing, comunicação, voz do cliente
│   │   ├── gilmario/                 ← Diretor técnico
│   │   ├── jessica/                  ← Diretora de design
│   │   └── josue/                    ← Estratégia e visão
│   │
│   ├── shared/                       ← BIBLIOTECA COMPARTILHADA
│   │   ├── general_harness/         ← Harness — padrão de execução de agentes
│   │   ├── general_prompts/         ← Templates de prompt reutilizáveis
│   │   ├── general_memory-system/   ← Sistema de memória compartilhada
│   │   ├── general_scripts/         ← Scripts utilitários
│   │   ├── general_skills/          ← +500 skills prontas (biblioteca externa)
│   │   ├── governance/              ← Frameworks de governança:
│   │   │   ├── AGCP.md             ← Agile Governance Control Protocol
│   │   │   ├── QILIS.md            ← Quality, Integrity, Legal, Information Security
│   │   │   ├── DEVSECOPS.md        ← DevSecOps padrão
│   │   │   └── REGULATORY.md       ← Compliance regulatório
│   │   ├── notebooklm/             ← Base de conhecimento do NotebookLM
│   │   ├── DB_obsidian/            ← Banco de dados do Obsidian
│   │   └── build_notebooklm.py     ← Script que gera a base NotebookLM
│   │
│   ├── skills-cache/                ← ÍNDICE DE SKILLS
│   │   ├── active-index.json (~2KB))
│   │   ├── POLICY.md               ← Política de uso das skills
│   │   └── master-index.json       ← Todas as skills disponíveis (grande, ~549KB)
│   │
│   ├── orquestrador/                ← Backup do orquestrador antigo
│   │   └── AGENT.md.bak
│   │
│   └── .apis/.env                   ← Credenciais de API
│
├── branding/                         ← SUA MARCA PESSOAL
│   ├── contacts.json                ← Contatos e número de WhatsApp
│   ├── state.json                   ← Estado local da pasta
│   ├── agenda_lu.json              ← Agenda da Nice
│   ├── governance/blocks.json       ← Bloqueios de governança
│   └── whatsapp/                    ← Código e fila do WhatsApp
│       ├── send.js                  ← Envio de mensagens
│       ├── queue.js + queue.json    ← Fila de mensagens
│       ├── client.js                ← Cliente WhatsApp
│       ├── server.js + start.js     ← Servidor WhatsApp
│       └── package.json             ← Dependências Node.js
│
├── portfolio/                        ← SEUS PROJETOS E PUBLICAÇÕES
│   ├── index.html                   ← Página inicial do portfólio
│   ├── products/                    ← Produtos criados
│   ├── state.json                   ← Estado local
│   └── README.md
│
├── builder/                          ← FÁBRICA DE INFRAESTRUTURA
│   ├── README.md                    ← Descrição geral
│   ├── state.json                   ← Estado local
│   ├── scripts/
│   │   └── clickup_daemon.py        ← Daemon que sincroniza tasks com ClickUp
│   ├── daemons/
│   │   ├── com.brachat.opencode.plist  ← launchd: Telegram bridge EZRA
│   │   └── com.brachat.nice.plist      ← launchd: Telegram bridge NICE
│   └── agents/
│       └── README.md                ← Instruções para criar agentes de produto
│
├── writings_studies/                 ← SEUS ESTUDOS E PRODUÇÕES ESCRITAS
│   ├── official_schedule.md         ← Cronograma de estudos principal
│   ├── state.json                   ← Estado local
│   ├── README.md                    ← Descrição
│   ├── 00_strategy_business/       ← Estratégia, negócios, transformação digital
│   ├── ai-engineering/             ← Engenharia de IA
│   ├── ai-governance/              ← Governança de IA
│   ├── books/aisio_book/           ← Livro sobre Aísio
│   ├── certifications/             ← Certificados (PDFs)
│   ├── cloud-architecture/         ← Cloud, GCP, Kubernetes, Terraform
│   ├── software-engineering/       ← Engenharia de software, padrões, testes
│   ├── general_papers/             ← Artigos acadêmicos
│   ├── judaism/                    ← Estudos judaicos
│   └── law/                        ← Estudos jurídicos
│
├── auditing/                         ← AUDITORIAS PASSADAS
│   ├── system_scaner_prompt.md     ← Prompt usado para escanear
│   └── descoberta-2026-06-07.md    ← Resultados da última auditoria
│
└── auditoria/                        ← RELATÓRIOS DE AUDITORIA
    └── rebuild-2026-06-07.md        ← Relatório do rebuild de 10 fases
```

---

## 3. MAPA DE CONEXÕES

### Quem se conecta com quem

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│  (assistant_agents/.opencode/agent/orquestrador.md)      │
│                                                          │
│  Lê no início:                                           │
│  ├── state.json (root)                                   │
│  ├── assistant_agents/state.json (perfil do usuário)     │
│  ├── dispatch-schedule.md (tabela de horários)           │
│  ├── writings_studies/official_schedule.md (cronograma)  │
│  └── daily/*/cache.json (progresso de cada agente)      │
│                                                          │
│  Despacha:                                               │
│  └── daily/*/AGENT.md → agente do horário               │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│               AGENTES DIÁRIOS                             │
│  (assistant_agents/daily/*/)                              │
│                                                          │
│  Cada agente:                                            │
│  ├── Lê próprio cache.json (estado anterior)            │
│  ├── Lê cache.json de outros agentes (quando precisa)   │
│  ├── Lê studies/ (para materiais de estudo)             │
│  ├── Lê branding/ (para contatos)                       │
│  └── Escreve no próprio cache.json (progresso)          │
│                                                          │
│  Agente ESTUDOS consolida todos os outros:               │
│  └── daily/estudos/cache.json → tabela de progresso     │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                  DIRETORES                                │
│  (assistant_agents/directors/*/)                          │
│                                                          │
│  AÍSIO (governança):                                     │
│  ├── Lê assistant_agents/ (frameworks, regras)           │
│  ├── Lê governance-ledger.jsonl (histórico)              │
│  ├── Lê REGRAS.md, AGCP.md, QILIS.md, DEVSECOPS.md      │
│  ├── Pode BLOQUEAR ações cross-domain                   │
│  └── Escreve em governance-ledger.jsonl (append-only)   │
│                                                          │
│  NICE (comunicação):                                     │
│  ├── Lê branding/ (contatos, estado)                    │
│  ├── Lê director/nice/ (metadados)                     │
│  └── Conecta com Telegram bot @luevertonbot             │
│                                                          │
│  GILMÁRIO (técnico):                                     │
│  └── Supervisiona qualidade de projetos builder/        │
│                                                          │
│  JESSICA (design):                                       │
│  └── Cuida da identidade visual no portfólio/           │
│                                                          │
│  JOSUÉ (estratégia):                                     │
│  └── Planejamento de longo prazo no writings_studies/   │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                  BUILDER (Infraestrutura)                 │
│  (builder/)                                               │
│                                                          │
│  Scripts:                                                │
│  ├── clickup_daemon.py → Conecta no ClickUp via         │
│  │   Composio SDK (cria/lê/atualiza/deleta tasks)       │
│  │   └── Salva cache em builder/cache/clickup.json      │
│  │                                                       │
│  Daemons (launchd — rodam 24/7):                        │
│  ├── com.brachat.opencode.plist                         │
│  │   └── Bridge Telegram → OpenCode (bot EZRA)          │
│  ├── com.brachat.nice.plist                             │
│  │   └── Bridge Telegram → NICE (bot @luevertonbot)    │
│  └── (futuro: com.brachat.clickup.plist)                │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│               RECURSOS EXTERNOS (Composio)               │
│                                                          │
│  Conexões ativas:                                        │
│  ├── ClickUp → gerenciamento de tasks e pipeline        │
│  ├── LinkedIn → posting e networking                    │
│  ├── Telegram → bots EZRA + NICE (comunicação 24/7)    │
│  │                                                       │
│  Disponível para usar:                                   │
│  ├── Gmail, Google Calendar, Google Drive, Google Meet  │
│  ├── Figma, Trello, Cloudflare, Mem0                    │
│  └── ClickUp, Telegram (já conectados)                  │
└─────────────────────────────────────────────────────────┘
```

### Conexões Detalhadas

| Arquivo/Pasta | Lê de | Escreve em | Conecta com |
|---|---|---|---|
| `orquestrador.md` | `state.json`, `dispatch-schedule.md`, `official_schedule.md`, `daily/*/cache.json` | — (só despacha) | Todos os agentes diários |
| `daily/*/AGENT.md` | `cache.json` local | `cache.json` local | Orquestrador, Estudos |
| `daily/estudos/AGENT.md` | `daily/*/cache.json` | `writings_studies/YYYY-MM-DD-progress.md` | Todos os agentes de estudo |
| `aisio/AGENT.md` | `REGRAS.md`, `shared/governance/`, `state.json` | `governance-ledger.jsonl` | Orquestrador (pode bloquear) |
| `nice/AGENT.md` | `integrations/contacts.json`, `directors/nice/metadata.json` | `directors/nice/cache.json` | Telegram bot @luevertonbot |
| `integrations/contacts.json` | — | — | Agentes que precisam de contatos |
| `builder/clickup_daemon.py` | `CLICKUP_LIST_ID` (env) | `builder/cache/clickup.json` | ClickUp via Composio SDK |
| `builder/com.brachat.opencode.plist` | — | — | launchd → Telegram → OpenCode |
| `writings_studies/official_schedule.md` | — | — | Orquestrador (lê todo início de sessão) |
| `assistant_agents/state.json` | — | — | Referência central de perfil e rotina |
| `skills-cache/active-index.json` | `master-index.json` | — | Skills que os agentes podem usar |

### Regras de Dependência

1. **Cross-domain PROIBIDO** — um agente de estudo não pode mexer em vaga de emprego sem autorização de Aísio
2. **Aísio pode bloquear qualquer dispatch** — se o Orquestrador tentar ativar um agente fora da regra, Aísio trava
3. **Cache.json é a memória local** — cada agente só escreve no próprio cache; lê dos outros quando precisa
4. **State.json é canônico** — o estado central em `assistant_agents/state.json` é a fonte da verdade sobre perfil e rotina
5. **Governança é append-only** — Aísio escreve no ledger mas nunca deleta; tudo fica registrado
6. **Builder roda independente** — os daemons launchd rodam 24/7 mesmo sem o OpenCode aberto
7. **Mem0 backup seletivo** — só backup com flag `mem0: true` vai para o Mem0

---

*Documento gerado em 07/06/2026 — Brachát Ecosystem v1*


---

## 2. LOCAL MAC BUILDER (From agents/README.md)


```text
brachat-main/builder/
├── README.md               <-- Este manual de produção do construtor
├── GOVERNANCE_WORKFLOW.md   <-- Manual das 8 fases, AGCP e QUILIS
├── clickup_daemon.py       <-- Daemon de 8 fases (Gemini + Claude + Groq)
├── bot_telegram.py         <-- Bot local do Telegram
├── active_project.json     <-- Estado de apontamento do projeto ativo
├── agentes/                <-- Especificações de cada agente do time (Spec-Kit)
│   ├── ezra.md

│   ├── gilmario.md
│   ├── researcher.md
│   ├── architect.md
│   ├── coder.md
│   └── documenter.md
├── memories/               <-- Arquivos JSON de contextos locais dos agentes
├── logs/                   <-- Logs de stdout/stderr gerenciados pelo launchd
├── hooks/                  <-- Git Pre-Commit Hooks rígidos de injeção automática
├── lazy-gravity-suite/     <-- Ponte WebSocket + Bot Telegram de Controle Remoto
└── governance_repos/       <-- Repositórios de cibersegurança e conformidade clonados
    ├── awesome-ai-agent-governance
    └── Anthropic-Cybersecurity-Skills
```

---

## 🛡️ Governança de IA & Cibersegurança

### A. Divisão de Partições (AGCP)
* **Partição de Análise (Cognitiva):** A IA atua de forma sandboxed nas fases de pesquisa e especificação (`researcher.md` / `architect.md`), gerando propostas de modificações lógicas em texto.
* **Partição de Efeito (Física):** O `clickup_daemon.py` e o `bot_telegram.py` executam comandos locais, testes e controlam as travas físicas de escrita do macOS.

### B. Workspace Guard (Zero-Trust de Escrita)
Os arquivos de código do Mac permanecem bloqueados como **Somente Leitura (`chmod 444`)** por padrão. A escrita só é liberada dinamicamente para **`chmod 644`** após a aprovação manual do CEO Fábio no Telegram (Fase 3 ➔ Fase 4).

### C. Limite de Commit (Commit Limit)
O Git Pre-Commit Hook local valida se as alterações de código correspondem estritamente ao escopo aprovado no `implementation_plan.md` e aborta o commit na hora se houver modificações intrusas.

---

## 🔌 Resiliência contra Quedas e Suspensão

1. **Auto-Start macOS:** O Daemon, os Bots e a Ponte Lazy-Gravity estão integrados como **LaunchAgents do macOS**. Eles iniciam automaticamente com o boot do computador e se auto-recuperam em caso de crash.
2. **Anti-Repouso:** O Mac está configurado via Amphetamine para **nunca dormir** ao fechar a tampa ou ao bloquear a tela, mantendo a esteira de robôs online 24h/dia (conectado à tomada).

---

## 🚀 Como Operar a Fábrica de Software

Pelo chat do **EZRA** no Telegram:
1. **Selecionar Projeto:** `/switch <caminho_do_projeto_no_mac>` (Ex: `/switch /Users/mac/brachat-main`).
2. **Disparar Tarefa:** `/trabalhar <instrução de desenvolvimento>` (Ex: `/trabalhar criar rota de healthcheck`).
3. **Aprovar Planos:** Interagir com o card criado no ClickUp e enviar aprovação no chat.


---

## 3. ORIGINAL TUTORIAL & WORKFLOWS


BRACHAT is a personal **AI agent** ecosystem for **Fábio Everton**. Each agent has a unique role, and all are coordinated via **EZRA** (orchestrator). Aísio (gatekeeper) validates every action before execution.

```text
Fábio (Telegram / CLI)
   │
   ▼ EZRA (orchestrator)
   │   ├── Reads state.json, schedule, agent caches
   │   └── Before each dispatch → consults Aísio
   │
   ├── 5 Directors (governance, operations, teaching, legal, home)
   ├── 11 Real Study Agents (english, dev, aristotle, etc)
   ├── 2 Producer Agents (job hunter, freelancer)
   ├── 2 Builders (architect + programmer)
   └── 24/7 Daemons (Telegram bridges with robust fallback, and ClickUp service now integrated via systemd)
```

**Three fundamental principles:**
1. **Nothing executes without Aísio's approval** — every action goes through the gatekeeper
2. **MVI — Maximum Viable Information** — files <200 lines, prompts <60 lines
3. **Mandatory CHECK/LOG** — every agent starts by reading cache and ends by writing

---

## 3. FULL SYSTEM TREE

```text
brachat-main/                                   ← ROOT
│
├── TUTORIAL.md                                 ← This document
├── README.md                                   ← General description
├── ARCHITECTURE.md                             ← Legacy document (outdated)
├── state.json                                  ← Central system state
├── opencode.json                               ← OpenCode CLI config
│
├── .opencode/                                  ← OpenCode config
│   ├── instructions/memory.md                  ← Startup protocol (loaded every session)
│   └── package.json
│
├── agents/                                     ← ALL AGENTS LIVE HERE
│   ├── TUTORIAL.md                             ← Legacy tutorial (outdated)
│   ├── README.md
│   ├── state.json                              ← User profile (264 lines)
│   ├── metadata.json                           ← Registry of 20 agents (149 lines)
│   │
│   ├── orchestrator_agent/                     ← EZRA — THE BRAIN
│   │   ├── orchestrator.md                     ← Pure dispatch, temperature 0
│   │   ├── state.json
│   │   └── cache_skills/
│   │
│   ├── director_agents/                        ← 5 DIRECTORS
│   │   ├── aisio/                              ← Dr. Aísio — Runtime Gatekeeper
│   │   │   ├── aisio.md                        ← Mission, validation, heuristics
│   │   │   ├── state.json
│   │   │   ├── governance/                     ← 6 governance files
│   │   │   │   ├── AGCP.md                     ← AI Governance Control Protocol
│   │   │   │   ├── QILIS.md                    ← Interpretability System
│   │   │   │   ├── REGRAS.md                   ← Ecosystem rules
│   │   │   │   ├── REGULATORY.md               ← GDPR, EU AI Act, NIST, PL 2338
│   │   │   │   ├── DEVSECOPS.md                ← Commit boundary & pipeline
│   │   │   │   └── boundary.sh                 ← 8-stage validation CLI
│   │   │   ├── frameworks/                     ← 3 regulatory frameworks
│   │   │   │   ├── lgpd.md + lgpd.opa          ← GDPR (reference + OPA policy)
│   │   │   │   ├── eu-ai-act.md + eu-ai-act.opa← EU AI Act (ref + OPA policy)
│   │   │   │   └── nist-ai-rmf.md + nist-ai-rmf.opa ← NIST AI RMF (ref + OPA policy)
│   │   │   ├── harness/harness.md              ← Mandatory harness pattern
│   │   │   ├── memory/README.md                ← Memory system
│   │   │   └── cache_skills/
│   │   │
│   │   ├── nice/nice.md                        ← Dr. Nice — Domestic Governance
│   │   ├── josue/josue.md                      ← Dr. Josué — Operations Director
│   │   ├── gilmario/gilmario.md                ← Dr. Gilmário — Teaching, Branding
│   │   └── jessica/jessica.md                  ← Dr. Jessica — Legal Director
│   │
│   ├── studies_agents/                         ← 11 STUDY AGENTS
│   │   ├── john/john.md                        ← English C2 (Mr. John Who)
│   │   ├── dev/dev.md                          ← Python Masterclass (Mr. Dev)
│   │   ├── aristotle/aristotle.md              ← Philosophy (Mr. Aristotle)
│   │   ├── temer/temer.md                      ← Politics (Mr. Temer)
│   │   ├── badge/badge.md                      ← Certifications (Mr. Badge)
│   │   ├── eduardo/eduardo.md                  ← PMP (Mr. Eduardo)
│   │   ├── calculus/calculus.md                ← ML Engineering (Mr. Calculus)
│   │   ├── google/google.md                    ← Google Skills (Mr. Google)
│   │   ├── showcase/showcase.md                ← Portfolio (Mr. Showcase)
│   │   ├── justus/justus.md                    ← Job Hunter (Mr. Justus)
│   │   ├── freela/freela.md                    ← Freelancer (Mr. Freela)
│   │   └── studies/                            ← Study Agent (consolidates)
│   │
│   ├── builder_agents/                         ← 2 BUILDERS
│   │   ├── architect/architect.md              ← Planning
│   │   └── artur/artur.md                      ← Programming
│   │
│   ├── shared/                                 ← SHARED LIBRARY
│   │   ├── general_skills/                     ← 1,481 individual skills
│   │   ├── skills-cache/                       ← Skill indexes
│   │   │   ├── active-index.json (~2KB) (loaded every session)
│   │   │   ├── master-index.json               ← ~549KB (NEVER load fully)
│   │   │   └── POLICY.md                       ← Token economy policy
│   │   ├── tools/yahoo_mail_cli.py             ← Email tool
│   │   ├── DB_obsidian/                        ← Obsidian database
│   │   └── build_notebooklm.py                 ← NotebookLM base script
│   │
│   ├── auditing/                               ← Past audits
│   │   ├── AUDITORIA.md
│   │   └── rebuild-2026-06-07.md
│   │
│   └── scripts/                                ← Infrastructure scripts
│       ├── telegram-bridge.py                  ← EZRA bridge
│       ├── nice-telegram-bridge.py             ← NICE bridge
│       ├── rewrite_schedule.py
│       └── run.sh
│
├── writings_studies/                           ← LONG-TERM KNOWLEDGE
│   ├── OFICIAL_SCHEDULE.md                     ← Unified study schedule (13,655 lines)
│   ├── state.json
│   ├── 00_strategy_business/
│   ├── ai-engineering/                         ← Notebooks 01-08
│   ├── ai-governance/                          ← Notebooks 01-05
│   ├── books/aisio_book/
│   ├── certifications/
│   ├── cloud-architecture/                     ← Notebooks 01-06
│   ├── software-engineering/                   ← Notebooks 01-07
│   ├── general_papers/
│   ├── judaism/
│   ├── law/
│   └── politica/summaries/
│
├── cloud/                                      ← CLOUD INFRASTRUCTURE
│   ├── agents/README.md
│   ├── daemons/                                ← 2 launchd plists (EZRA + NICE)
│   ├── dashboard/                              ← Web dashboard (port 8080)
│   │   ├── dashboard.py
│   │   ├── server.py
│   │   └── index.html
│   ├── scripts/clickup_daemon.py
│   └── sites/                                  ← VPS systemd services (147.15.18.252)
│       ├── walkthrough.md                      ← Practical infra guide (mandatory reading)
│       ├── deploy.sh                           ← Automated deploy script
│       ├── bridge-ezra.py                      ← EZRA Telegram bridge (24/7)
│       ├── bridge-nice.py                      ← NICE Telegram bridge (24/7)
│       ├── brachat-ezra.service                ← systemd: EZRA bridge
│       ├── brachat-nice.service                ← systemd: NICE bridge
│       ├── brachat-dashboard.service           ← systemd: HTTP (port 8080)
│       └── brachat-malha.service               ← systemd: WebSocket (port 8765)
│
├── integrations/                               ← EXTERNAL INTEGRATIONS
│   ├── agenda_lu.json
│   ├── apis/
│   ├── blocks.json
│   ├── contacts.json
│   ├── instagram/
│   ├── state.json
│   └── whatsapp/                               ← Baileys client, queue, server
│
├── portfolio/                                  ← PROJECTS AND PUBLICATIONS
│   ├── products/
│   ├── README.md
│   └── state.json
│
├── branding/                                   ← PERSONAL BRANDING
│   └── whatsapp/
│       ├── auth_baileys/
│       └── status.json
│
├── assistant_agents/                           ← EMPTY (legacy — do not use)
│
└── .github/
```

---

## 4. EACH FOLDER IN DETAIL

### 4.1 `agents/` — The System Brain

**`agents/orchestrator_agent/orchestrator.md`** — EZRA
- Temperature 0, no reasoning
- Sole point of contact with Fábio
- Reads `state.json` + `OFICIAL_SCHEDULE.md` + `schedule_progress.json` + `cache.json` of all agents
- Before any dispatch → consults Aísio
- Manages session: `date` → report → dispatch → log

**`agents/director_agents/aisio/`** — Dr. Aísio
- Runtime gatekeeper: nothing executes without approval
- Validates against: AGCP, QILIS, REGULATORY, DEVSECOPS, REGRAS
- OPA policies in `frameworks/*.opa` for GDPR, EU AI Act, NIST
- Logs in `.opencode/governance-ledger.jsonl` (append-only)
- Decisions: APPROVED / DENIED / POLICY_VIOLATION / CONSTRAINT_VIOLATION

**`agents/director_agents/nice/nice.md`** — Dr. Nice
- Domestic governance: purchases, bills, Dona Lu's schedule
- Financial triggers: ≤R$100 auto, R$101-500 consults Lu, >R$500 blocked

**`agents/director_agents/josue/josue.md`** — Dr. Josué
- Operations Director: operational demands, feasibility, resource allocation

**`agents/director_agents/gilmario/gilmario.md`** — Dr. Gilmário
- Teaching, Branding & Authority: reviews study material, produces branding content
- Rejects material >200 lines

**`agents/director_agents/jessica/jessica.md`** — Dr. Jessica
- Legal Director: analyzes contracts, issues opinions, can veto
- Isolated memory — invisible to other agents

**`agents/studies_agents/`** — 11 Study Agents and 1 Consolidator

| Folder | Agent | Temperature | Function |
|--------|-------|-------------|----------|
| `john/` | Mr. John Who | 0.3 | English C2 — vocabulary + reading + exercises |
| `dev/` | Mr. Dev | 0.2 | Python Masterclass — phases 1-2 |
| `aristotle/` | Mr. Aristotle | 0.3 | Philosophy — Socratic dialogue |
| `temer/` | Mr. Temer | 0.2 | Politics — context + questions |
| `badge/` | Mr. Badge | 0.2 | Certifications AWS/GCP/Azure — MVI + quiz |
| `eduardo/` | Mr. Eduardo | 0.2 | PMP — People/Process/Business domains |
| `calculus/` | Mr. Calculus | 0.2 | ML Engineering — paper + exercise + code review |
| `google/` | Mr. Google | 0.2 | Google Skills — enforces transcriptions |
| `showcase/` | Mr. Showcase | 0.3 | Portfolio — LinkedIn drafts |
| `justus/` | Mr. Justus | 0 | Job Hunter — scrapes LinkedIn, Indeed, Gupy, GeekHunter |
| `freela/` | Mr. Freela | 0 | Freelancer — scrapes Workana, 99Freelas, Fiverr |
| `studies/` | Estudos | 0.2 | Consolidates progress of all |

Each agent has: `AGENT.md` + `state.json` + `cache_skills/`

**`agents/builder_agents/`** — 2 Builders

| Folder | Agent | Function |
|--------|-------|----------|
| `architect/` | Mr. Architect | Planning, prioritization, structure |
| `artur/` | Mr. Artur | Implementation, security, code review |

**`agents/shared/`** — Shared Library
- `general_skills/` — 1,481 individual skills (load on demand)
- `skills-cache/active-index.json` — 13 categories, ~2KB (always load)
- `skills-cache/master-index.json` — complete index, ~549KB (NEVER load)
- `skills-cache/POLICY.md` — usage policy
- `DB_obsidian/` — Obsidian database
- `tools/yahoo_mail_cli.py` — email tool
- `build_notebooklm.py` — NotebookLM base script

### 4.2 `writings_studies/` — Long-Term Knowledge

- `OFICIAL_SCHEDULE.md` — unified schedule (13,655 lines, Month 1-5 with detailed morning/afternoon/night days, hands-on with commit, mandatory evidence)
- Subfolders by area: `ai-engineering/`, `ai-governance/`, `cloud-architecture/`, `software-engineering/`, `certifications/`, `law/`, `judaism/`, etc.
- Each area has numbered notebooks and `summaries/` with MVI summaries

### 4.3 `cloud/` — Infrastructure

- `daemons/` — 2 launchd plists (EZRA Telegram + NICE Telegram)
- `dashboard/` — Python web dashboard (port 8080 on VPS)
- `sites/` — systemd services on VPS (147.15.18.252)
  - `brachat-clickup.service`: actual service running the ClickUp poll.

### 4.4 `integrations/` — External Connections

- `contacts.json` — contact book
- `whatsapp/` — Baileys client, message queue, server
- `instagram/` — Instagram integration
- `apis/` — API configurations

### 4.5 `portfolio/` — Projects and Publications

- `products/` — created products
- `state.json` — portfolio state

### 4.6 `branding/` — Personal Branding

- `whatsapp/` — Baileys authentication + status

---

## 5. EXECUTION ARCHITECTURE

### 5.1 Session Cycle

1. EZRA opens session
2. Runs `date` → discovers time
3. Reads `state.json` → knows who Fábio is, routine
4. Reads `schedule_progress.json` → The `advance_schedule.py` script manages day progression (now starting from Day 1, no longer paralyzed at Day 0).
5. Reads `cache.json` of all agents → knows what was done
6. Reports to Fábio: "Yesterday you did X. Y is pending."
7. Dispatches the agent for the current time

### 5.2 Dispatch Flow

```text
EZRA wants to dispatch agent X
   │
   ▼ Consults Aísio
   │
   ├── Aísio validates against:
   │   ├── governance/AGCP.md (action lifecycle)
   │   ├── governance/QILIS.md (interpretability)
   │   ├── governance/REGRAS.md (system rules)
   │   ├── governance/REGULATORY.md (GDPR, EU AI Act, NIST)
   │   ├── governance/DEVSECOPS.md (commit boundary)
   │   └── frameworks/*.opa (OPA policies)
   │
   ├── APPROVED → EZRA dispatches
   └── DENIED → EZRA stops and asks Fábio
```

### 5.3 Cycle of Each Agent

1. **CHECK** — reads `state.json` + own `cache.json`
2. **EXECUTE** — performs the task
3. **CONFIRM** — asks Fábio if done/achieved
4. **LOG** — writes `daily_log` in `cache.json`

### 5.4 Harness Pattern (Mandatory)

Every agent file MUST have the following sections (actual structure used across all agents):

| Section | Purpose |
|---------|---------|
| **HARNESS** | Trigger, exit condition, max turns, fallback |
| **PROMPT ECONOMY** | Token budget, cache, memory limits |
| **CONTRACT** | Input/output schema, expected behavior |
| **OPERATIONAL PROCEDURE** | Numbered steps (always CHECK → ... → LOG) |
| **DECISION HEURISTICS** | Rules for branching, error handling, edge cases |
| **VERIFICATION LEVELS (N1-N5)** | Evidence gates from basic to integrated |
| **KNOWLEDGE SOURCE** | URLs, files, APIs to consult |
| **SKILLS** | Skill loading flow, caches, indexes |

The 5 design concerns (Core, Skills, Memory, Protocols, Regulation) are covered across these sections:
- **Core**: HARNESS + CONTRACT + DECISION HEURISTICS
- **Skills**: SKILLS + OPERATIONAL PROCEDURE
- **Memory**: PROMPT ECONOMY + KNOWLEDGE SOURCE
- **Protocols**: OPERATIONAL PROCEDURE (step 1 CHECK, step 8 LOG)
- **Regulation**: VERIFICATION LEVELS (N1-N5) + DECISION HEURISTICS

### 5.5 Approval Gates

| Situation | Rule |
|-----------|------|
| Purchase ≤R$100 | Nice decides automatically |
| Purchase R$101-500 | Nice consults Dona Lu |
| Purchase >R$500 | Blocked |
| Freelance proposal >R$500 | Human approval |
| LinkedIn post | Fábio reviews and publishes |
| Cross-domain | FORBIDDEN without permission |
| New agent | Needs AUTHORIZED in ledger |
| Hardcoded secret | POLICY_VIOLATION → DENY |

---

## 6. GOVERNANCE — Aísio in Detail

Aísio is the heart of governance. His files in `director_agents/aisio/`:

| File | Function |
|------|----------|
| `aisio.md` | Mission, validation flow, decision heuristics |
| `governance/AGCP.md` | Action lifecycle in 6 states + 20 rejection codes |
| `governance/QILIS.md` | Interpretability system in 6 stages |
| `governance/REGRAS.md` | 13 ecosystem rules |
| `governance/REGULATORY.md` | Compliance mapping (GDPR, EU AI Act, NIST) |
| `governance/DEVSECOPS.md` | Commit pipeline in 8 stages |
| `governance/boundary.sh` | CLI implementing the 8-stage validation |
| `frameworks/lgpd.md` | Complete GDPR reference |
| `frameworks/lgpd.opa` | GDPR compliance OPA policy |
| `frameworks/eu-ai-act.md` | Complete EU AI Act reference |
| `frameworks/eu-ai-act.opa` | EU AI Act compliance OPA policy |
| `frameworks/nist-ai-rmf.md` | Complete NIST AI RMF reference |
| `frameworks/nist-ai-rmf.opa` | NIST compliance OPA policy |
| `harness/harness.md` | Harness pattern template |
| `memory/README.md` | Memory system documentation |

### Verification Levels (L1-L5)

| Level | What happens |
|-------|--------------|
| L1 | Rules loaded and parsed |
| L2 | Action validated against all frameworks |
| L3 | Decision issued (APPROVED/DENIED) |
| L4 | Log in ledger with evidence |
| L5 | Fábio notified if denied |

---

## 7. SKILLS — Specialization Library

Location: `agents/shared/skills-cache/`

- **13 categories**: languages, frontend, backend, cloud-infra, data-ml-ai, security, devops-ci-cd, automation, project-management, governance, creative-design, mobile, others
- **1,481 skills** in total
- **Policy**: load `active-index.json (~2KB)) in context; NEVER load `master-index.json` (~549KB)
- Each skill has an individual `SKILL.md` — load on demand

### Loading Flow
1. Check agent's local `cache_skills/`
2. Search in `active-index.json` by category
3. Grep in `master-index.json` by exact name
4. Load the individual `SKILL.md`
5. Local cache in `cache_skills/`

---

## 8. 24/7 INFRASTRUCTURE

### Daemons (launchd on macOS)

| Plist | Function |
|-------|----------|
| `com.brachat.opencode.plist` | EZRA Telegram bridge (bot @Baruch_Everton_bot) |
| `com.brachat.nice.plist` | NICE Telegram bridge (bot @luevertonbot) |

### VPS (147.15.18.252) — Oracle Cloud Always Free (New Infrastructure)

For the complete practical guide (deploy, firewall, maintenance), see `cloud/sites/walkthrough.md`.

- **Instance**: `VM.Standard.E2.1.Micro` (AMD, 1 vCPU, 2 GB physical RAM, 50 GB SSD).
- **Stability**: **4 GB permanent Swap** configuration (`/swapfile` allocated via physical block `dd`) to avoid any Out-Of-Memory (OOM) bottlenecks. Total 6 GB active virtual memory.
- **Security and Permissions**: systemd services run under the `opc` user instead of `root` or `nobody`, resolving historical permission errors.
- **Server Repository**: `git clone` at `/opt/brachat/repo`. Files in `/opt/brachat/` are **symlinks** to `repo/cloud/`.
- **Active Services (systemd)**:
  * **`brachat-ezra`**: EZRA Telegram bridge (bot @Baruch_Everton_bot) — 24/7.
  * **`brachat-nice`**: NICE Telegram bridge (bot @luevertonbot) — 24/7.
  * **`brachat-dashboard`**: HTTP server on port `8080` — serves `index.html` + `/api/status` endpoint.
   * **`brachat-malha`**: WebSocket server on port `8765` — transmits real agent state every 1s.
   * **`brachat-clickup`**: ClickUp task polling daemon — monitors the Hermes_Agent list (ID 901714148420).
- **Firewall — Two Layers**:
  * **Layer 1 (VM)**: `firewalld` with ports 8080/tcp and 8765/tcp open.
  * **Layer 2 (OCI)**: VCN Security List — **pending open** ports in OCI Console. If the dashboard doesn't respond externally, this is the likely reason.
- **Dashboard — How It Works**:
  * `index.html` opens WebSocket `ws://hostname:8765` and receives JSON every 1s.
  * The WebSocket server reads `agents/{director,builder,studies}_agents/*/state.json` from disk.
  * If an agent has a filled `daily_log`, the dashboard shows a green ◉. If empty, shows a gray ○.
  * **Nothing is fake** — the dashboard reflects exactly the state on the filesystem.

### Update: Dashboard with Real Data (06/10/2026)

The WebSocket server (`server.py`) was fixed to read from the actual path (`agents/` instead of `assistant_agents/`). Now the dashboard shows:
- 5 directors (aisio, gilmario, jessica, josue, nice)
- 2 builders (architect, artur)
- 11 studies (aristotle, badge, calculus, dev, eduardo, freela, google, john, justus, showcase, temer)
- Real status: green if the agent has logged activity, gray if never used.

### External Access (Open)
Ports 8080 and 8765 are open in both the VM firewall (`firewalld`) and the OCI Security List. The dashboard responds externally — confirmed `HTTP 200` from outside the VPS.

### Hetzner Deactivation (Dead)
The old Hetzner instance (`167.233.30.115` - 2 vCPU, 3.7GB RAM) was **completely deactivated and discontinued**. All systemd services were stopped on Hetzner before the final reboot, preventing Telegram polling conflicts. Ecosystem files and secrets were purged from the old machine.

### Active Connections

* **ClickUp:** The local Daemon was moved to the VPS systemd (`brachat-clickup.service`) and now runs natively.
* **Telegram Bridges:** Refactored. No longer use the Ollama bottleneck; send a standby message if the central API fails.
* Composio on standby and Google Calendar.

---

## 9. CRITICAL RULES

| Rule | Description |
|------|-------------|
| **LLM Hierarchy** | Orchestrator T°0, Directors T°0-0.2, Studies T°0.2-0.3 |
| **MVI** | Files <200 lines, prompts <60 lines |
| **Step-by-step** | Every task with numbered steps |
| **Approval gate** | >R$500 needs human approval |
| **Cross-domain** | FORBIDDEN without explicit permission |
| **CHECK/LOG** | Every agent starts reading and ends writing |
| **Honest budget** | NEVER invent/estimate values |
| **Zero-trust** | External tools only with permission |
| **Selective Mem0** | Only backup with `mem0: true` flag |
| **Append-only governance**| Aísio never deletes from the ledger |

---

## 10. AGENT CONNECTION MAP

```text
EZRA
├── Reads: agents/state.json, writings_studies/OFICIAL_SCHEDULE.md, orchestrator_agent/schedule_progress.json
├── Reads: all studies_agents/*/state.json (cache)
├── Consults: Aísio (for every dispatch)
└── Writes: report to user

Aísio
├── Reads: governance/*.md, frameworks/*.md
├── Reads: .opencode/governance-ledger.jsonl (last 20)
├── Validates: AGCP → QILIS → REGULATORY → DEVSECOPS → REGRAS
├── Validates: frameworks/*.opa (GDPR, EU AI Act, NIST)
└── Writes: governance-ledger.jsonl (append-only)

Study Agents (each one)
├── Reads: own state.json (local cache)
├── Reads: writings_studies/{area}/ (prior knowledge)
├── Executes: daily task
└── Writes: own state.json (daily_log)

Job Hunter / Freelancer
├── Reads: own state.json
├── Uses: web scraping / external APIs
├── Respects: financial approval gates
└── Writes: own state.json
```

---

## 11. QUICK COMMANDS

| Action | Command |
|--------|---------|
| Start session | `date` + read caches + report |
| View today's progress | Read `agents/studies_agents/*/state.json` |
| View schedule progress | Read `agents/orchestrator_agent/schedule_progress.json` |
| View full schedule | Read `writings_studies/OFICIAL_SCHEDULE.md` |
| Validate action | `task aisio "validate dispatch [agent] for [action]"` |
| Consult skill | Grep `master-index.json` + load `SKILL.md` |
| View ledger | Read last 20 lines of `.opencode/governance-ledger.jsonl` |
| Read infra guide | `cloud/sites/walkthrough.md` |
| Dashboard (local) | `curl http://147.15.18.252:8080` |
| Services status | `ssh opc@147.15.18.252 'sudo systemctl status brachat-ezra brachat-nice brachat-dashboard brachat-malha'` |

---

*Document generated on 06/09/2026 — Brachát Ecosystem v2.0 — Updated on 06/11/2026*

