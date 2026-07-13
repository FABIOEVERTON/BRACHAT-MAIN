# Startup

## 1. EMAIL — SPARK (CLIENTE PRINCIPAL)
Abrir Spark no Mac (ja aberto). Usar Spark para todas as acoes de email: ler, responder, arquivar, lixeira.
Checar Gmail via Composio API, resumir na tela por clusters, perguntar o que quer fazer. So passar com autorizacao expressa.
**IMPORTANTE**: Ao responder emails de vagas, usar Spark para replies (mais rapido e com templates). Depois mover para lixeira pelo Spark.

### AI JOB SEARCH AGENT
Comandos disponiveis (ver `skills_job_agent.md`):
- `/start` — Clonar repo AI Job Search, instalar dependências, preparar ambiente MCP
- `/setup` — Perfil LinkedIn → resume estruturado
- `/scrape` — Buscar vagas por compatibilidade (High/Medium/Low)
- `/apply [LINK]` — Score + Cover Letter + CV customizados
- `/interview` — Guia STAR + gaps honestos

## 2. CALENDAR
Mostrar agenda do dia no Google Calendar, perguntar se quer adicionar algo. So passar com autorizacao expressa.

## 3. APLICACAO DE CURRICULO — PIPELINE CHATGPT

### 3.1 PLATAFORMAS POR DIA
- **Segunda-feira**: Glassdoor
- **Terca-feira**: Job Bank Canada
- **Quarta-feira**: Jobot, Top Startups, Contra
- **Quinta-feira**: Arc.dev, Turing, Freelancer, Joblet.ai
- **Sexta-feira**: BairesDev, Guru, LinkedIn

### 3.2 CARGOS-ALVO PERMANENTES (disparar automaticamente sempre que encontrar):

**A. AI & Cloud (Foco Atual):**
- AI Solutions Architect / Cloud Architect (OCI)
- AI Governance Lead / Compliance Officer
- AI Workflow Automation Specialist / Prompt Engineer

**B. Operacoes, Projetos & Estrategia:**
- Director of Operations (COO)
- Technical Program Manager (TPM)
- Legal Operations Manager

**C. Suporte Executivo Internacional:**
- Assistente Executivo Remoto (Executive Assistant)
- Remote Personal Assistant (Familias Estrangeiras de Alta Renda)

### 3.3 PASSO 1 — KEYWORD EXTRACTION POR VAGA
Para cada vaga encontrada que bate com os cargos-alvo:

1. Copiar descricao completa da vaga
2. Passar para o LLM com prompt: "Extraia as 10-15 principais palavras-chave (habilidades tecnicas, soft skills, ferramentas, certificacoes) desta descricao de vaga. Retorne como lista."
3. Salvar keywords em `resumes_storage/keywords/[vaga_nome].json`
4. Usar essas keywords no passo 2 para pontuar e tailor o curriculo

### 3.4 PASSO 2 — RESUMO NO METODO XYZ GOOGLE
TODO bullet point de experiencia no curriculo DEVE seguir o formato:

> "Accomplished [X] as measured by [Y], by doing [Z]"

**Exemplos:**
- "Accomplished 40% reduction in ticket resolution time as measured by before/after SLA metrics, by building an AI triage agent with LangChain"
- "Accomplished R$30M+ in managed project portfolio as measured by client retention rate, by leading 60+ B2B enterprise engagements as primary technical liaison"
- "Accomplished multi-agent LLM orchestration platform as measured by 22 concurrent agents with <500ms latency, by architecting Python/FastAPI backend with pgvector RAG"

Regra: TODO novo curriculo gerado DEVE usar XYZ. Curriculos antigos serao refatorados sob demanda.

### 3.5 PASSO 3 — SCRAPING + PLANILHA
Para cada plataforma do dia:

1. **Scrape**: Usar Playwright para navegar na plataforma, buscar cada cargo-alvo, extrair: titulo, empresa, link, descricao, data, salario, requisitos
2. **Planilha CSV**: Salvar em `resumes_storage/planilha_[PLATAFORMA]_[DATA].csv` com colunas:
   - `link | cargo | empresa | match_score | keywords_extraidas | curriculo_gerado | status`
3. **Match score**: LLM avalia de 0-10 o fit entre curriculo base e descricao da vaga
4. **Priorizar**: Apenas vagas com score >= 7 avancam para aplicacao

### 3.6 PASSO 4 — AUTO-APPLY
Para cada vaga com score >= 7:

1. Gerar curriculo XYZ personalizado com as keywords extraidas
2. Salvar em `resumes_storage/[cargo]_[empresa].pdf`
3. Se houver email direto: enviar via Gmail com curriculo anexado e cover letter
4. Se exigir portal: tentar Easy Apply / preenchimento automatico via Playwright
5. Registrar em `state.json` + `planilha_[PLATAFORMA]_[DATA].csv` como "sent"
6. Esperar 30-60s entre aplicacoes para evitar rate limit

Regras:
- Max 15 aplicacoes/dia (gate U12)
- Nao aplicar em vagas que exigem autorizacao de trabalho que Fabio nao tem (US sem sponsorship, Canada sem SIN, etc.)
- Se plataforma pedir cartao de credito para aplicar, pular

## 4. FREELANCER
Enumerar: Contra (qua), Freelancer (qui), Guru (sex). Entrar no que Fabio falar. Ficar ouvindo e auxiliando enquanto aplica. So passar com autorizacao expressa.

## 5. ESTUDO (todos os dias, apos as plataformas)

Blocos diarios fixos:

- **ESTUDO_ORACLE_ONE** — Cursos Tech ONE (n8n, LangChain, RAG, OCI, LLMs, Agentes)
- **ESTUDO_OCI_CERTIFICACAO_DA_VEZ** — 22 certificacoes em 5 fases (SCHEDULE_OFICIAL.md). Progresso: 0%
- **ESTUDO_CONCURSO_DA_VEZ** — Concurso Embratur/FAPETEC (SCHEDULE_OFICIAL.md → EIXO 2)
- **ESTUDO_CONCURSO_TCU** — Concurso TCU (SCHEDULE_OFICIAL.md → EIXO 1)
- **ESTUDO_INGLES** — Vocabulario diario via NotebookLM

Mostrar na tela o cronograma do dia (SCHEDULE_OFICIAL.md). Abrir site. Ficar ouvindo.
