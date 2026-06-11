# TUTORIAL — BRACHÁT Ecosystem

> ⚡ **AUTO-LOAD:** Read this document **first** to understand 100% of the system: folders, files, agents, rules, and workflows.
>
> **Then** read `cloud/sites/walkthrough.md` for the practical infrastructure guide (VPS, services, deploy, firewall).

---

## 1. RECOMMENDED READING ORDER

1. `TUTORIAL.md` ← **you are here**
2. `cloud/sites/walkthrough.md` — practical cloud infrastructure guide
3. `agents/director_agents/aisio/governance/REGRAS.md` — ecosystem rules
4. `agents/orchestrator_agent/orchestrator.md` — EZRA, the orchestrator
5. `agents/metadata.json` — registry of all 20 agents
6. `agents/state.json` — user profile, routine, schedule
7. `agents/shared/skills-cache/active-index.json` — skills index (~4KB)
8. `agents/director_agents/aisio/aisio.md` — Aísio, the gatekeeper

---

## 2. OVERVIEW

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
│   ├── state.json                              ← User profile (262 lines)
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
│   │   │   ├── active-index.json               ← ~4KB (loaded every session)
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
- `skills-cache/active-index.json` — 13 categories, ~4KB (always load)
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

Every agent MUST have 5 sections:
1. **Core** — role, mission, LLM
2. **Skills** — numbered steps (always CHECK → ... → LOG)
3. **Memory** — working context, episodic experience, semantic knowledge
4. **Protocols** — inter-agent communication + tools
5. **Regulation** — ethical limits, approval gates, observability

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
- **1,465 skills** in total
- **Policy**: load `active-index.json` (~4KB) in context; NEVER load `master-index.json` (~549KB)
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

- **Instance**: `VM.Standard.E2.1.Micro` (AMD, 1 vCPU, 1 GB physical RAM, 50 GB SSD).
- **Stability**: **4 GB permanent Swap** configuration (`/swapfile` allocated via physical block `dd`) to avoid any Out-Of-Memory (OOM) bottlenecks. Total 5 GB active virtual memory.
- **Security and Permissions**: systemd services run under the `opc` user instead of `root` or `nobody`, resolving historical permission errors.
- **Server Repository**: `git clone` at `/opt/brachat/repo`. Files in `/opt/brachat/` are **symlinks** to `repo/cloud/`.
- **Active Services (systemd)**:
  * **`brachat-ezra`**: EZRA Telegram bridge (bot @Baruch_Everton_bot) — 24/7.
  * **`brachat-nice`**: NICE Telegram bridge (bot @luevertonbot) — 24/7.
  * **`brachat-dashboard`**: HTTP server on port `8080` — serves `index.html` + `/api/status` endpoint.
  * **`brachat-malha`**: WebSocket server on port `8765` — transmits real agent state every 1s.
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

### External Access (Blocked)
Currently, ports 8080 and 8765 are blocked in the OCI infrastructure firewall (Security List). The dashboard responds **locally** on the VM (`curl localhost:8080` → 200 OK) but not externally. To open: **OCI Console > Networking > Security Lists > add Ingress TCP 8080 and 8765**.

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
