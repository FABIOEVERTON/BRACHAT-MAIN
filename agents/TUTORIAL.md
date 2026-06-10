# TUTORIAL — Como entender o ecossistema BRACHÁT

> Leia este documento **primeiro**. Ele te guia pelos arquivos que você precisa ler para entender 100% do sistema, dos agentes, das regras e dos protocolos.

---

## 1. ORDEM DE LEITURA

Para entender tudo, leia os arquivos nesta ordem:

1. `TUTORIAL.md` ← **você está aqui** — visão geral + mapa
2. `assistant_agents/REGRAS.md` — regras do ecossistema (hierarquia, contratos, economia)
3. `assistant_agents/.opencode/agent/orquestrador.md` — orquestrador (dispatch, schedule, protocolos)
4. `assistant_agents/state.json` — estado atual (perfil, rotina, cronograma)
5. `assistant_agents/skills-cache/index.json` — index de skills disponíveis
6. `assistant_agents/daily/{nome}/AGENT.md` — cada agente individual (ver lista abaixo)
7. Se aplicável: `assistant_agents/shared/harness_template.md` — template harness (se existir)

Tempo estimado de leitura completa: 5-10 minutos.

---

## 2. VISÃO GERAL DO SISTEMA

BRACHÁT é um ecossistema de agentes pessoais para **Fábio Everton**:

- **Orquestrador**: dispatch puro (temperatura 0, sem reasoning) — coordena todos os agentes
- **11 daily agents**: cada um cuida de uma área (estudo, trabalho, portfólio)
- **Tracking**: ciclo CHECK → EXECUTA → CONFIRM → LOG em cache.json persistente
- **Schedule**: rotina diária 07:00-22:30
- **Armazenamento**: `writings_studies/{area}/summaries/` para conhecimento de longo prazo

---

## 3. ARQUITETURA OBRIGATÓRIA — O PADRÃO HARNESS

**Definido em**: `assistant_agents/REGRAS.md` (seção 0)

Todo agente DEVE ter estas 5 seções:

```
### 🧠 Núcleo Central
- Harness: papel, missão, o que faz
- LLM: modelo + temperatura

### ⚙️ Módulo de Habilidades (Skills)
- Operational Procedure: steps numerados (sempre começam com CHECK e terminam com LOG)
- Decision Heuristics: regras de decisão (atalhos lógicos)

### 🧩 Módulo de Memória (Memory)
- Working Context: o que carrega no início (cache.json, state.json)
- Episodic Experience: daily_log no cache.json
- Semantic Knowledge: base de conceitos (writings_studies/, skills-cache)
- Personal Memory: perfil do usuário + preferências específicas

### 🔗 Módulo de Protocolos (Protocols)
- Agent-Agent: como se comunica com outros agentes (sempre via cache.json)
- Agent-Tools: ferramentas que usa (webfetch, Composio, Playwright, WhatsApp Business, etc)

### ⚖️ Ferramentas de Regulação, Avaliação e Operação
- Normative Constraints: limites éticos e regras (MVI, approval gates)
- Sandbox: ambiente isolado
- Evaluator: como avalia resultados
- Approval Loop: ciclo de aprovação humana
- Sub-Agent Orchestration: delegação para sub-agentes
- Observability: cache.json + daily_log
- Compression: economia de tokens
```

---

## 4. REGRAS FUNDAMENTAIS DO SISTEMA

**Arquivo fonte**: `assistant_agents/REGRAS.md`

| Regra | Descrição | Onde se aplica |
|-------|-----------|----------------|
| Hierarquia LLM | Orquestrador T°0 (sem reasoning), Gerentes T°0.2-0.3, Produtores T°0 (zero reasoning) | Todos os agentes |
| MVI | Arquivos <200 linhas | Todo arquivo do sistema |
| Step-by-step | Toda tarefa `[ATIVO]`/`[MATERIAL]`/`[FAÇO]` deve vir com steps numerados | Orquestrador + daily agents |
| Approval gate | >R$500 precisa de aprovação humana | Freelancer, Job-hunter |
| Cross-domain | PROIBIDO sem permissão explícita do orquestrador | Todos os agentes |
| CHECK/LOG obrigatório | Todo agente começa lendo cache.json e termina escrevendo | Daily agents |
| Budget | NUNCA inventar/estimar/converter valores. Sempre reportar o EXATO | Freelancer, Job-hunter |
| Zero-Trust | Ferramentas externas só com permissão do usuário | Orquestrador |

---

## 5. AGENTES DISPONÍVEIS

**Todos os agentes estão em**: `assistant_agents/daily/{nome}/`

| Agente | Role | T° | Arquivo | Cache |
|--------|------|----|---------|-------|
| **orquestrador** | Dispatch puro, coordena tudo | 0 | `.opencode/agent/orquestrador.md` | N/A (lê todos) |
| **nice** | Governança doméstica (Dona Lu) | 0.2 | `daily/nice/AGENT.md` | `daily/nice/cache.json` |
| **ingles** | Tutor de inglês (vocabulário, leitura) | 0.3 | `daily/ingles/AGENT.md` | `daily/ingles/cache.json` |
| **politica** | Estudo de Política (teoria, gestão pública, cidadania) | 0.2 | `daily/politica/AGENT.md` | `daily/politica/cache.json` |
| **filosofia** | Estudo de filosofia (correntes, diálogo) | 0.3 | `daily/filosofia/AGENT.md` | `daily/filosofia/cache.json` |
| **certificacoes** | Certificações cloud (AWS/GCP/Azure) | 0.2 | `daily/certificacoes/AGENT.md` | `daily/certificacoes/cache.json` |
| **google-skills** | Cursos Google Skills Boost | 0.2 | `daily/google-skills/AGENT.md` | `daily/google-skills/cache.json` |
| **python** | Curso Python Masterclass | 0.2 | `daily/python/AGENT.md` | `daily/python/cache.json` |
| **pmp** | Certificação PMP | 0.2 | `daily/pmp/AGENT.md` | `daily/pmp/cache.json` |
| **ml-engineer** | ML Engineering | 0.2 | `daily/ml-engineer/AGENT.md` | `daily/ml-engineer/cache.json` |
| **job-hunter** | Caça vagas (LinkedIn, Indeed, Gupy) | 0 | `daily/job-hunter/AGENT.md` | `daily/job-hunter/cache.json` |
| **freelancer** | Workana + freelas | 0 | `daily/freelancer/AGENT.md` | `daily/freelancer/cache.json` |
| **portfolio** | Posts LinkedIn | 0.3 | `daily/portfolio/AGENT.md` | `daily/portfolio/cache.json` |
| **nice** | Governança doméstica (Dona Lu) | 0.2 | `daily/nice/AGENT.md` | `daily/nice/cache.json` |
| **josue** | Diretor Executivo & Comercial | 0.1 | `directors/josue/AGENT.md` | `directors/josue/cache.json` |
| **gilmario** | Diretor Ensino, Branding & Autoridade | 0.2 | `directors/gilmario/AGENT.md` | `directors/gilmario/cache.json` |
| **aisio** | Diretor Governança, Compliance & Auditoria | 0 | `directors/aisio/AGENT.md` | `directors/aisio/cache.json` |
| **jessica** | Diretora Jurídica (memória isolada) | 0.1 | `directors/jessica/AGENT.md` | `directors/jessica/cache.json` |

---

## 6. SCHEDULE DIÁRIO

**Fonte**: orquestrador.md (tabela de dispatching)

| Horário | Atividade | Tipo |
|---------|-----------|------|
| 07:00 | Acordar — saudação | Saudação |
| 07:15 | Job hunting scan | `[FAÇO]` |
| 07:30 | Inglês — user estuda | `[MATERIAL]` → `[VOCÊ ESTUDA]` |
| 08:00 | Certificações — user estuda | `[MATERIAL]` → `[VOCÊ ESTUDA]` |
| 08:30 | Google Skills (todos os dias) | `[MATERIAL]` → `[VOCÊ ESTUDA]` |
| 09:00-11:00 | Deep work — user trabalha | `[FUNDO]` |
| 11:00 | Python — user estuda | `[MATERIAL]` → `[VOCÊ ESTUDA]` |
| 12:00-14:00 | Almoço | `[FUNDO]` |
| 14:00-17:00 | Freelancer | `[FAÇO]` |
| 17:00 | Portfólio | `[FAÇO]` |
| 18:00 | PMP | `[MATERIAL]` → `[VOCÊ ESTUDA]` |
| 19:00-20:00 | Livre | `[FAÇO]` |
| 20:00 | Política + Filosofia | `[MATERIAL]` → `[VOCÊ ESTUDA]` |
| 21:00 | Review noturno | `[FAÇO]` |

**Legenda**:
- `[MATERIAL]` = preparo conteúdo para o usuário
- `[FAÇO]` = executo a tarefa
- `[VOCÊ ESTUDA]` = usuário estuda o material
- `[FUNDO]` = rodo em silêncio sem interromper

---

## 7. PROTOCOLOS CRÍTICOS

### 7.1 Início de sessão (orquestrador)
1. Rode `date` para saber horário atual
2. Leia `state.json` + `skills-cache/index.json`
3. Leia `daily/*/cache.json` de cada agente
4. Reporte ao usuário o que foi feito ontem e o que ficou pendente

### 7.2 Ciclo de cada agente
1. **CHECK**: lê cache.json → sabe o que já foi feito
2. **EXECUTA**: faz a tarefa (prepara material, busca vagas, etc.)
3. **CONFIRM**: pergunta ao usuário "fez/conseguiu?"
4. **LOG**: escreve daily_log no cache.json com status

### 7.3 Fluxo de estudo (Study Flow)
1. Usuário estuda (assiste curso, lê, faz exercício)
2. Usuário me dá transcrição/resumo/tópico
3. Eu sumarizo em MVI (conceito central + key points + exemplo)
4. Salvo em `writings_studies/{area}/summaries/{topico}.md`
5. Usuário pode perguntar depois "o que estudei sobre X?"

### 7.4 Approval Gates
- **Financeiro**: >R$500 → aprovação humana necessária
- **Publicação**: posts LinkedIn → user revisa e publica (eu nunca publico direto)
- **Propostas freela**: eu preparo rascunho → user revisa → user envia
- **Ferramentas externas**: perguntar antes de usar
- **Cross-domain**: PROIBIDO sem permissão do orquestrador

---

## 8. SISTEMA DE MEMÓRIA

### cache.json (cada agente)
```json
{
  "daily_log": {
    "2026-06-05": {
      "status": "completed",
      "details": "Módulo 3 - IAM Policies"
    }
  },
  "ultimo_tema": "IAM Policies"
}
```
- CHECK: lê no início
- LOG: escreve no fim
- Orquestrador lê todos no início da sessão

### writings_studies/ (conhecimento de longo prazo)
```
writings_studies/{area}/summaries/{topico}.md
```
- Salvos em MVI (<200 linhas)
- Consulta: "o que estudei sobre X?" → eu leio o arquivo

### state.json (fonte única da verdade)
- Perfil do usuário
- Rotina diária e cronograma
- Job hunting pipeline
- Armazenado em: `assistant_agents/state.json`

### integrations/contacts.json (agenda WhatsApp)
- Contém número Business + contatos cadastrados
- Agentes consultam: "quem devo contactar?"
- Agentes inserem: novos contatos conforme necessário
- Regra: números em formato internacional sem + (ex: 5561996506881)

---

## 9. ESTRUTURA DE ARQUIVOS COMPLETA

```
brachat-main/
├── TUTORIAL.md                                    ← você está aqui
├── assistant_agents/
│   ├── REGRAS.md                                  ← regras do ecossistema (76 linhas)
│   │
│   ├── .opencode/agent/
│   │   └── orquestrador.md                        ← orquestrador principal (136 linhas)
│   │
│   ├── directors/
│   │   ├── josue/AGENT.md                           ← Diretor Executivo & Comercial
│   │   ├── gilmario/AGENT.md                        ← Diretor de Ensino, Branding & Autoridade
│   │   ├── aisio/AGENT.md                           ← Diretor de Governança, Compliance & Auditoria
│   │   └── jessica/AGENT.md                         ← Diretora Jurídica
│   │
│   ├── daily/
│   │   ├── ingles/AGENT.md + cache.json
│   │   ├── politica/AGENT.md + cache.json
│   │   ├── filosofia/AGENT.md + cache.json
│   │   ├── certificacoes/AGENT.md + cache.json
│   │   ├── google-skills/AGENT.md + cache.json
│   │   ├── python/AGENT.md + cache.json
│   │   ├── pmp/AGENT.md + cache.json
│   │   ├── ml-engineer/AGENT.md + cache.json
│   │   ├── job-hunter/AGENT.md + cache.json
│   │   ├── freelancer/AGENT.md + cache.json
│   │   └── portfolio/AGENT.md + cache.json
│   │

│   └── skills-cache/index.json                    ← index de skills (carregado 1x/sessão)
│
├── writings_studies/                               ← conhecimento de longo prazo
│   ├── certificacoes/summaries/
│   ├── ingles/summaries/
│   ├── python/summaries/
│   ├── google-skills/summaries/
│   ├── politica/summaries/
│   ├── filosofia/summaries/
│   ├── pmp/summaries/
│   └── ml-engineer/summaries/
│
├── portfolio/builder_agents/                      ← agentes de criação (portfólio)
├── branding/
│   ├── contacts.json                                   ← agenda de contatos WhatsApp (agentes consultam/inserem)
│   ├── job_hunting/                                    ← materiais de candidatura
│   └── freelas/                                        ← propostas e projetos freelas
```

---

## 10. COMO COMEÇAR UMA SESSÃO

Se você é um LLM recém-chegado ao sistema:

1. **Leia este tutorial primeiro** (você está aqui)
2. **Leia `assistant_agents/REGRAS.md`** — regras fundamentais
3. **Leia `assistant_agents/.opencode/agent/orquestrador.md`** — dispatch + schedule
4. **Leia `assistant_agents/state.json`** — quem é o usuário, qual a rotina
5. **Execute `date`** — descubra o horário atual
6. **Leia `daily/*/cache.json` de cada agente** — saiba o que foi feito ontem
7. **Reporte ao usuário**: "Ontem você fez [X]. Ficou pendente [Y]."
8. **Pergunte**: "O que vamos fazer agora?"

---

*Documento gerado em 05/06/2026. Mantenha atualizado conforme o sistema evolui.*
