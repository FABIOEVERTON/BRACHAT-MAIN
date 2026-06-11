# TUTORIAL — Ecossistema BRACHÁT

> Leia este documento **primeiro** para entender 100% do sistema: pastas, arquivos, agentes, regras e fluxos.
>
> **Depois** leia `cloud/sites/walkthrough.md` para o guia prático de infraestrutura (VPS, services, deploy, firewall).

---

## 1. ORDEM DE LEITURA RECOMENDADA

1. `TUTORIAL.md` ← **você está aqui**
2. `cloud/sites/walkthrough.md` — guia prático de infraestrutura em nuvem
3. `agents/director_agents/aisio/governance/REGRAS.md` — regras do ecossistema
4. `agents/orchestrator_agent/orchestrator.md` — EZRA, o orquestrador
5. `agents/metadata.json` — registro de todos os 20 agentes
6. `agents/state.json` — perfil do usuário, rotina, cronograma
7. `agents/shared/skills-cache/active-index.json` — index de skills (~4KB)
8. `agents/director_agents/aisio/aisio.md` — Aísio, o gatekeeper

---

## 2. VISÃO GERAL

BRACHAT é um ecossistema pessoal de **agentes IA** para **Fábio Everton**. Cada agente tem papel único, e todos se coordenam via **EZRA** (orquestrador). Aísio (gatekeeper) valida toda ação antes de executar.

```
Fábio (Telegram / CLI)
   │
   ▼ EZRA (orquestrador)
   │   ├── Lê state.json, schedule, cache dos agentes
   │   └── Antes de cada dispatch → consulta Aísio
   │
   ├── 5 Diretores (governança, operações, ensino, jurídico, casa)
   ├── 5 Diretores (governança, operações, ensino, jurídico, casa)
   ├── 11 Agentes de Estudo reais (inglês, dev, aristotle, etc)
   ├── 2 Agentes Produtores (job hunter, freelancer)
   ├── 2 Builders (arquiteto + programador)
   └── 24/7 Daemons (Telegram bridges com fallback robusto, e ClickUp service agora integrado via systemd)
```

**Três princípios fundamentais:**
1. **Nada executa sem aprovação de Aísio** — toda ação passa pelo gatekeeper
2. **MVI — Maximum Viable Information** — arquivos <200 linhas, prompts <60 linhas
3. **CHECK/LOG obrigatório** — todo agente começa lendo cache e termina escrevendo

---

## 3. ÁRVORE COMPLETA DO SISTEMA

```
brachat-main/                                   ← RAIZ
│
├── TUTORIAL.md                                 ← Este documento
├── README.md                                   ← Descrição geral
├── ARCHITECTURE.md                             ← Documento legado (desatualizado)
├── state.json                                  ← Estado central do sistema
├── opencode.json                               ← Config OpenCode CLI
│
├── .opencode/                                  ← Config do OpenCode
│   ├── instructions/memory.md                  ← Startup protocol (carregado em toda sessão)
│   └── package.json
│
├── agents/                                     ← TODOS OS AGENTES VIVEM AQUI
│   ├── TUTORIAL.md                             ← Tutorial legado (desatualizado)
│   ├── README.md
│   ├── state.json                              ← Perfil do usuário (262 linhas)
│   ├── metadata.json                           ← Registry de 20 agentes (149 linhas)
│   │
│   ├── orchestrator_agent/                     ← EZRA — O CÉREBRO
│   │   ├── orchestrator.md                     ← Dispatch puro, temperatura 0
│   │   ├── state.json
│   │   └── cache_skills/
│   │
│   ├── director_agents/                        ← 5 DIRETORES
│   │   ├── aisio/                              ← Dr. Aísio — Runtime Gatekeeper
│   │   │   ├── aisio.md                        ← Missão, validação, heurísticas
│   │   │   ├── state.json
│   │   │   ├── governance/                     ← 6 arquivos de governança
│   │   │   │   ├── AGCP.md                     ← AI Governance Control Protocol
│   │   │   │   ├── QILIS.md                    ← Interpretability System
│   │   │   │   ├── REGRAS.md                   ← Regras do ecossistema
│   │   │   │   ├── REGULATORY.md               ← LGPD, EU AI Act, NIST, PL 2338
│   │   │   │   ├── DEVSECOPS.md                ← Commit boundary & pipeline
│   │   │   │   └── boundary.sh                 ← CLI de validação de 8 estágios
│   │   │   ├── frameworks/                     ← 3 frameworks regulatórios
│   │   │   │   ├── lgpd.md + lgpd.opa          ← LGPD (referência + política OPA)
│   │   │   │   ├── eu-ai-act.md + eu-ai-act.opa← EU AI Act (ref + política OPA)
│   │   │   │   └── nist-ai-rmf.md + nist-ai-rmf.opa ← NIST AI RMF (ref + política OPA)
│   │   │   ├── harness/harness.md              ← Padrão harness mandatório
│   │   │   ├── memory/README.md                ← Sistema de memória
│   │   │   └── cache_skills/
│   │   │
│   │   ├── nice/nice.md                        ← Dr. Nice — Governança Doméstica
│   │   ├── josue/josue.md                      ← Dr. Josué — Diretor de Operações
│   │   ├── gilmario/gilmario.md                ← Dr. Gilmário — Ensino, Branding
│   │   └── jessica/jessica.md                  ← Dr. Jessica — Diretora Jurídica
│   │
│   ├── studies_agents/                         ← 12 AGENTES DE ESTUDO
│   │   ├── john/john.md                        ← Inglês C2 (Mr. John Who)
│   │   ├── dev/dev.md                          ← Python Masterclass (Mr. Dev)
│   │   ├── aristotle/aristotle.md              ← Filosofia (Mr. Aristotle)
│   │   ├── temer/temer.md                      ← Política (Mr. Temer)
│   │   ├── badge/badge.md                      ← Certificações (Mr. Badge)
│   │   ├── eduardo/eduardo.md                  ← PMP (Mr. Eduardo)
│   │   ├── calculus/calculus.md                ← ML Engineering (Mr. Calculus)
│   │   ├── google/google.md                    ← Google Skills (Mr. Google)
│   │   ├── showcase/showcase.md                ← Portfólio (Mr. Showcase)
│   │   ├── justus/justus.md                    ← Job Hunter (Mr. Justus)
│   │   ├── freela/freela.md                    ← Freelancer (Mr. Freela)
│   │   └── studies/                            ← Agente de Estudos (consolida)
│   │
│   ├── builder_agents/                         ← 2 BUILDERS
│   │   ├── architect/architect.md              ← Planejamento
│   │   └── artur/artur.md                      ← Programação
│   │
│   ├── shared/                                 ← BIBLIOTECA COMPARTILHADA
│   │   ├── general_skills/                     ← 1.481 skills individuais
│   │   ├── skills-cache/                       ← Índices de skills
│   │   │   ├── active-index.json               ← ~4KB (carregado em toda sessão)
│   │   │   ├── master-index.json               ← ~549KB (NUNCA carregar completo)
│   │   │   └── POLICY.md                       ← Política de economia de tokens
│   │   ├── tools/yahoo_mail_cli.py             ← Ferramenta de e-mail
│   │   ├── DB_obsidian/                        ← Banco de dados Obsidian
│   │   └── build_notebooklm.py                 ← Script de base NotebookLM
│   │
│   ├── auditing/                               ← Auditorias passadas
│   │   ├── AUDITORIA.md
│   │   └── rebuild-2026-06-07.md
│   │
│   └── scripts/                                ← Scripts de infraestrutura
│       ├── telegram-bridge.py                  ← Bridge EZRA
│       ├── nice-telegram-bridge.py             ← Bridge NICE
│       ├── rewrite_schedule.py
│       └── run.sh
│
├── writings_studies/                           ← CONHECIMENTO DE LONGO PRAZO
│   ├── OFICIAL_SCHEDULE.md                     ← Cronograma unificado de estudos (13.655 linhas)
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
├── cloud/                                      ← INFRAESTRUTURA EM NUVEM
│   ├── agents/README.md
│   ├── daemons/                                ← 2 launchd plists (EZRA + NICE)
│   ├── dashboard/                              ← Dashboard web (porta 8080)
│   │   ├── dashboard.py
│   │   ├── server.py
│   │   └── index.html
│   ├── scripts/clickup_daemon.py
│   ├── scripts/clickup_daemon.py
│   └── sites/                                  ← systemd services, bridges, deploy
│       ├── walkthrough.md                      ← Guia prático de infraestrutura (leitura obrigatória)
│       ├── deploy.sh                           ← Script de deploy automatizado
│       ├── bridge-ezra.py                      ← Telegram bridge do EZRA (24/7)
│       ├── bridge-nice.py                      ← Telegram bridge da NICE (24/7)
│       ├── brachat-ezra.service                ← systemd: bridge EZRA
│       ├── brachat-nice.service                ← systemd: bridge NICE
│       ├── brachat-dashboard.service           ← systemd: HTTP (porta 8080)
│       └── brachat-malha.service               ← systemd: WebSocket (porta 8765)
│
├── integrations/                               ← INTEGRAÇÕES EXTERNAS
│   ├── agenda_lu.json
│   ├── apis/
│   ├── blocks.json
│   ├── contacts.json
│   ├── instagram/
│   ├── state.json
│   └── whatsapp/                               ← Baileys client, fila, servidor
│
├── portfolio/                                  ← PROJETOS E PUBLICAÇÕES
│   ├── products/
│   ├── README.md
│   └── state.json
│
├── branding/                                   ← MARCA PESSOAL
│   └── whatsapp/
│       ├── auth_baileys/
│       └── status.json
│
├── assistant_agents/                           ← VAZIO (legado — não usar)
│
└── .github/
```

---

## 4. CADA PASTA EM DETALHE

### 4.1 `agents/` — O Cérebro do Sistema

**`agents/orchestrator_agent/orchestrator.md`** — EZRA
- Temperatura 0, sem reasoning
- Único ponto de contato com Fábio
- Lê `state.json` + `OFICIAL_SCHEDULE.md` + `schedule_progress.json` + `cache.json` de todos os agentes
- Antes de todo dispatch → consulta Aísio
- Gerencia sessão: `date` → report → dispatch → log

**`agents/director_agents/aisio/`** — Dr. Aísio
- Runtime gatekeeper: nada executa sem aprovação
- Valida contra: AGCP, QILIS, REGULATORY, DEVSECOPS, REGRAS
- OPA policies em `frameworks/*.opa` para LGPD, EU AI Act, NIST
- Log em `.opencode/governance-ledger.jsonl` (append-only)
- Decisões: APPROVED / DENIED / POLICY_VIOLATION / CONSTRAINT_VIOLATION

**`agents/director_agents/nice/nice.md`** — Dr. Nice
- Governança doméstica: compras, contas, agenda da Dona Lu
- Gatilhos financeiros: ≤R$100 auto, R$101-500 consulta Lu, >R$500 bloqueado

**`agents/director_agents/josue/josue.md`** — Dr. Josué
- Diretor de Operações: demandas operacionais, viabilidade, alocação de recursos

**`agents/director_agents/gilmario/gilmario.md`** — Dr. Gilmário
- Ensino, Branding & Autoridade: revisa material de estudo, produz conteúdo de branding
- Rejeita material >200 linhas

**`agents/director_agents/jessica/jessica.md`** — Dr. Jessica
- Diretora Jurídica: analisa contratos, emite pareceres, pode vetar
- Memória isolada — invisível para outros agentes

**`agents/studies_agents/`** — 11 Agentes de Estudo e 1 Consolidador

| Pasta | Agente | Temperatura | Função |
|-------|--------|-------------|--------|
| `john/` | Mr. John Who | 0.3 | Inglês C2 — vocabulário + leitura + exercícios |
| `dev/` | Mr. Dev | 0.2 | Python Masterclass — fases 1-2 |
| `aristotle/` | Mr. Aristotle | 0.3 | Filosofia — diálogo socrático |
| `temer/` | Mr. Temer | 0.2 | Política — contexto + questões |
| `badge/` | Mr. Badge | 0.2 | Certificações AWS/GCP/Azure — MVI + quiz |
| `eduardo/` | Mr. Eduardo | 0.2 | PMP — domínios People/Process/Business |
| `calculus/` | Mr. Calculus | 0.2 | ML Engineering — paper + exercício + code review |
| `google/` | Mr. Google | 0.2 | Google Skills — cobra transcrições |
| `showcase/` | Mr. Showcase | 0.3 | Portfólio — drafts LinkedIn |
| `justus/` | Mr. Justus | 0 | Job Hunter — varre LinkedIn, Indeed, Gupy, GeekHunter |
| `freela/` | Mr. Freela | 0 | Freelancer — varre Workana, 99Freelas, Fiverr |
| `studies/` | Estudos | 0.2 | Consolida progresso de todos |

Cada agente tem: `AGENT.md` + `state.json` + `cache_skills/`

**`agents/builder_agents/`** — 2 Builders

| Pasta | Agente | Função |
|-------|--------|--------|
| `architect/` | Mr. Architect | Planejamento, priorização, estrutura |
| `artur/` | Mr. Artur | Implementação, segurança, code review |

**`agents/shared/`** — Biblioteca Compartilhada
- `general_skills/` — 1.481 skills individuais (carregar sob demanda)
- `skills-cache/active-index.json` — 13 categorias, ~4KB (carregar sempre)
- `skills-cache/master-index.json` — índice completo, ~549KB (NUNCA carregar)
- `skills-cache/POLICY.md` — política de uso
- `DB_obsidian/` — banco de dados Obsidian
- `tools/yahoo_mail_cli.py` — ferramenta de e-mail
- `build_notebooklm.py` — script de base NotebookLM

### 4.2 `writings_studies/` — Conhecimento de Longo Prazo

- `OFICIAL_SCHEDULE.md` — cronograma unificado (13.655 linhas, Mês 1-5 com dias detalhados manhã/tarde/noite, hands-on com commit, evidência obrigatória)
- Subpastas por área: `ai-engineering/`, `ai-governance/`, `cloud-architecture/`, `software-engineering/`, `certifications/`, `law/`, `judaism/`, etc.
- Cada área tem notebooks numerados e `summaries/` com resumos MVI

### 4.3 `cloud/` — Infraestrutura

- `daemons/` — 2 plists launchd (EZRA Telegram + NICE Telegram)
- `dashboard/` — dashboard web em Python (porta 8080 no VPS)
- `sites/` — systemd services no VPS (147.15.18.252)
  - `brachat-clickup.service`: serviço que roda de fato o poll no ClickUp.

### 4.4 `integrations/` — Conexões Externas

- `contacts.json` — agenda de contatos
- `whatsapp/` — cliente Baileys, fila de mensagens, servidor
- `instagram/` — integração Instagram
- `apis/` — configurações de API

### 4.5 `portfolio/` — Projetos e Publicações

- `products/` — produtos criados
- `state.json` — estado do portfólio

### 4.6 `branding/` — Marca Pessoal

- `whatsapp/` — autenticação Baileys + status

---

## 5. ARQUITETURA DE EXECUÇÃO

### 5.1 Ciclo de Sessão

1. EZRA abre sessão
2. Roda `date` → descobre horário
3. Lê `state.json` → sabe quem é Fábio, qual a rotina
4. Lê `schedule_progress.json` → O script `advance_schedule.py` gerencia a passagem de dias (começando agora do Day 1, não mais o Day 0 paralisado).
5. Lê `cache.json` de todos os agentes → sabe o que foi feito
6. Reporta a Fábio: "Ontem você fez X. Ficou pendente Y."
7. Dispatcha o agente do horário

### 5.2 Fluxo de Dispatch

```
EZRA quer despachar agente X
   │
   ▼ Consulta Aísio
   │
   ├── Aísio valida contra:
   │   ├── governance/AGCP.md (ciclo de vida da ação)
   │   ├── governance/QILIS.md (interpretabilidade)
   │   ├── governance/REGRAS.md (regras do sistema)
   │   ├── governance/REGULATORY.md (LGPD, EU AI Act, NIST)
   │   ├── governance/DEVSECOPS.md (commit boundary)
   │   └── frameworks/*.opa (OPA policies)
   │
   ├── APPROVED → EZRA despacha
   └── DENIED → EZRA para e pergunta a Fábio
```

### 5.3 Ciclo de Cada Agente

1. **CHECK** — lê `state.json` + `cache.json` próprio
2. **EXECUTA** — faz a tarefa
3. **CONFIRM** — pergunta a Fábio se fez/conseguiu
4. **LOG** — escreve `daily_log` no `cache.json`

### 5.4 Padrão Harness (Mandatório)

Todo agente DEVE ter 5 seções:
1. **Núcleo Central** — papel, missão, LLM
2. **Habilidades** — steps numerados (sempre CHECK → ... → LOG)
3. **Memória** — working context, experiência episódica, conhecimento semântico
4. **Protocolos** — comunicação entre agentes + ferramentas
5. **Regulação** — limites éticos, approval gates, observabilidade

### 5.5 Approval Gates

| Situação | Regra |
|----------|-------|
| Compra ≤R$100 | Nice decide automático |
| Compra R$101-500 | Nice consulta Dona Lu |
| Compra >R$500 | Bloqueado |
| Proposta freela >R$500 | Aprovação humana |
| Post LinkedIn | Fábio revisa e publica |
| Cross-domain | PROIBIDO sem permissão |
| Novo agente | Precisa AUTHORIZED no ledger |
| Hardcoded secret | POLICY_VIOLATION → DENY |

---

## 6. GOVERNANÇA — Aísio em Detalhe

Aísio é o coração da governança. Seus arquivos em `director_agents/aisio/`:

| Arquivo | Função |
|---------|--------|
| `aisio.md` | Missão, fluxo de validação, heurísticas de decisão |
| `governance/AGCP.md` | Ciclo de vida da ação em 6 estados + 20 códigos de rejeição |
| `governance/QILIS.md` | Sistema de interpretabilidade em 6 estágios |
| `governance/REGRAS.md` | 13 regras do ecossistema |
| `governance/REGULATORY.md` | Mapeamento de compliance (LGPD, EU AI Act, NIST) |
| `governance/DEVSECOPS.md` | Pipeline de commit em 8 estágios |
| `governance/boundary.sh` | CLI que implementa a validação de 8 estágios |
| `frameworks/lgpd.md` | Referência completa da LGPD |
| `frameworks/lgpd.opa` | Política OPA de compliance LGPD |
| `frameworks/eu-ai-act.md` | Referência completa do EU AI Act |
| `frameworks/eu-ai-act.opa` | Política OPA de compliance EU AI Act |
| `frameworks/nist-ai-rmf.md` | Referência completa do NIST AI RMF |
| `frameworks/nist-ai-rmf.opa` | Política OPA de compliance NIST |
| `harness/harness.md` | Template do padrão harness |
| `memory/README.md` | Documentação do sistema de memória |

### Níveis de Verificação (N1-N5)

| Nível | O que acontece |
|-------|----------------|
| N1 | Regras carregadas e parseadas |
| N2 | Ação validada contra todos os frameworks |
| N3 | Decisão emitida (APPROVED/DENIED) |
| N4 | Log no ledger com evidência |
| N5 | Fábio notificado se negado |

---

## 7. SKILLS — Biblioteca de Especialização

Local: `agents/shared/skills-cache/`

- **13 categorias**: linguagens, frontend, backend, cloud-infra, dados-ml-ia, seguranca, devops-ci-cd, automacao, gestao-projetos, governanca, design-criativo, mobile, outros
- **1.465 skills** no total
- **Política**: carregar `active-index.json` (~4KB) em contexto; NUNCA carregar `master-index.json` (~549KB)
- Cada skill tem `SKILL.md` individual — carregar sob demanda

### Fluxo de Loading
1. Verificar `cache_skills/` local do agente
2. Buscar em `active-index.json` pela categoria
3. Grep em `master-index.json` pelo nome exato
4. Load do `SKILL.md` individual
5. Cache local em `cache_skills/`

---

## 8. INFRAESTRUTURA 24/7

### Daemons (launchd no macOS)

| Plist | Função |
|-------|--------|
| `com.brachat.opencode.plist` | Telegram bridge do EZRA (bot @Baruch_Everton_bot) |
| `com.brachat.nice.plist` | Telegram bridge da NICE (bot @luevertonbot) |

### VPS (147.15.18.252) — Oracle Cloud Always Free (Nova Infraestrutura)

Para o guia prático completo (deploy, firewall, manutenção), veja `cloud/sites/walkthrough.md`.

- **Instância**: `VM.Standard.E2.1.Micro` (AMD, 1 vCPU, 1 GB RAM física, 50 GB SSD).
- **Estabilidade**: Configuração de **4 GB de Swap permanente** (`/swapfile` alocado via `dd` de blocos físicos) para evitar qualquer gargalo de Out-Of-Memory (OOM). Total de 5 GB de memória virtual ativa.
- **Segurança e Permissões**: Os serviços systemd rodam sob o usuário `opc` em vez de `root` ou `nobody`, resolvendo erros históricos de permissão.
- **Repositório do Servidor**: `git clone` em `/opt/brachat/repo`. Arquivos em `/opt/brachat/` são **symlinks** para `repo/cloud/`.
- **Serviços Ativos (systemd)**:
  * **`brachat-ezra`**: Telegram bridge do EZRA (bot @Baruch_Everton_bot) — 24/7.
  * **`brachat-nice`**: Telegram bridge da NICE (bot @luevertonbot) — 24/7.
  * **`brachat-dashboard`**: HTTP server na porta `8080` — serve `index.html` + endpoint `/api/status`.
  * **`brachat-malha`**: WebSocket server na porta `8765` — transmite estado real dos agentes a cada 1s.
- **Firewall — Duas Camadas**:
  * **Camada 1 (VM)**: `firewalld` com portas 8080/tcp e 8765/tcp abertas.
  * **Camada 2 (OCI)**: Security List da VCN — **pendente liberar** as portas no Console OCI. Se o dashboard não responder externamente, este é o motivo provável.
- **Dashboard — Como Funciona**:
  * `index.html` abre WebSocket `ws://hostname:8765` e recebe JSON a cada 1s.
  * O servidor WebSocket lê `agents/{director,builder,studies}_agents/*/state.json` do disco.
  * Se um agente tem `daily_log` preenchido, o dashboard mostra ◉ verde. Se vazio, mostra ○ cinza.
  * **Nada é fake** — o dashboard reflete exatamente o estado no filesystem.

### Atualização: Dashboard com Dados Reais (10/06/2026)

O servidor WebSocket (`server.py`) foi corrigido para ler do caminho real (`agents/` em vez de `assistant_agents/`). Agora o dashboard mostra:
- 5 diretores (aisio, gilmario, jessica, josue, nice)
- 2 builders (architect, artur)
- 11 estudos (aristotle, badge, calculus, dev, eduardo, freela, google, john, justus, showcase, temer)
- Status real: verde se o agente já registrou atividade, cinza se nunca foi usado.

### Acesso Externo (Bloqueado)
Atualmente as portas 8080 e 8765 estão bloqueadas no firewall de infraestrutura da OCI (Security List). O dashboard responde **localmente** na VM (`curl localhost:8080` → 200 OK) mas não de fora. Para liberar: **Console OCI > Networking > Security Lists > adicionar Ingress TCP 8080 e 8765**.

### Desativação da Hetzner (Morto)
A antiga instância Hetzner (`167.233.30.115` - 2 vCPU, 3.7GB RAM) foi **totalmente desativada e descontinuada**. Todos os serviços systemd foram parados na Hetzner antes do reboot final, evitando conflitos de polling no Telegram. Os arquivos e segredos do ecossistema foram limpos da máquina antiga.

### Conexões Ativas (Composio)

### Conexões Ativas 

* **ClickUp:** O Daemon local foi movido para o systemd da VPS (`brachat-clickup.service`) e agora funciona nativamente.
* **Telegram Bridges:** Refatorados. Não utilizam mais o gargalo do Ollama; enviam mensagem de standby se a API central falhar.
* Composio em stand-by e Google Calendar.

---

## 9. REGRAS CRÍTICAS

| Regra | Descrição |
|-------|-----------|
| **Hierarquia LLM** | Orquestrador T°0, Diretores T°0-0.2, Estudos T°0.2-0.3 |
| **MVI** | Arquivos <200 linhas, prompts <60 linhas |
| **Step-by-step** | Toda tarefa com steps numerados |
| **Approval gate** | >R$500 precisa de aprovação humana |
| **Cross-domain** | PROIBIDO sem permissão explícita |
| **CHECK/LOG** | Todo agente começa lendo e termina escrevendo |
| **Budget honesto** | NUNCA inventar/estimar valores |
| **Zero-trust** | Ferramentas externas só com permissão |
| **Mem0 seletivo** | Só backup com flag `mem0: true` |
| **Governança append-only** | Aísio nunca deleta do ledger |

---

## 10. MAPA DE CONEXÕES ENTRE AGENTES

```
EZRA
├── Lê: agents/state.json, writings_studies/OFICIAL_SCHEDULE.md, orchestrator_agent/schedule_progress.json
├── Lê: todos os studies_agents/*/state.json (cache)
├── Consulta: Aísio (para todo dispatch)
└── Escreve: relatório pro usuário

Aísio
├── Lê: governance/*.md, frameworks/*.md
├── Lê: .opencode/governance-ledger.jsonl (últimas 20)
├── Valida: AGCP → QILIS → REGULATORY → DEVSECOPS → REGRAS
├── Valida: frameworks/*.opa (LGPD, EU AI Act, NIST)
└── Escreve: governance-ledger.jsonl (append-only)

Agentes de Estudo (cada um)
├── Lê: próprio state.json (cache local)
├── Lê: writings_studies/{area}/ (conhecimento prévio)
├── Executa: tarefa do dia
└── Escreve: próprio state.json (daily_log)

Job Hunter / Freelancer
├── Lê: próprio state.json
├── Usa: web scraping / APIs externas
├── Respeita: approval gates financeiros
└── Escreve: próprio state.json
```

---

## 11. COMANDOS RÁPIDOS

| Ação | Comando |
|------|---------|
| Iniciar sessão | `date` + ler caches + reportar |
| Ver progresso de hoje | Ler `agents/studies_agents/*/state.json` |
| Ver progresso do schedule | Ler `agents/orchestrator_agent/schedule_progress.json` |
| Ver schedule completo | Ler `writings_studies/OFICIAL_SCHEDULE.md` |
| Validar ação | `task aisio "validate dispatch [agent] for [action]"` |
| Consultar skill | Grep `master-index.json` + load `SKILL.md` |
| Ver ledger | Ler últimas 20 linhas de `.opencode/governance-ledger.jsonl` |
| Ler guia de infraestrutura | `cloud/sites/walkthrough.md` |
| Dashboard (local) | `curl http://147.15.18.252:8080` |
| Status dos serviços | `ssh opc@147.15.18.252 'sudo systemctl status brachat-ezra brachat-nice brachat-dashboard brachat-malha'` |

---

*Documento gerado em 09/06/2026 — Brachát Ecosystem v2.0 — Atualizado em 10/06/2026*
