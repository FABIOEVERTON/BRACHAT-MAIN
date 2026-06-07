# ARQUITETURA BRACHÁT — Mapeamento do Sistema

## 1. PANORAMA GERAL

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
│   │   ├── active-index.json       ← Skills ativas (pequeno, ~4KB)
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
