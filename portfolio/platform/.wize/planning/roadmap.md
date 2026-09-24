# CRONOGRAMA MESTRE DIÁRIO (DO ZERO ABSOLUTO AO GO-LIVE)
## Plataforma BRACHATEC — SaaS B2B/B2G de Governança Probatória

> **REGRA DE OURO:** Execução estritamente diária (sem agrupamentos). Cada dia possui escopo fechado, arquivos definidos e critério de aceite verificável.
> **LEGENDA:** `[X]` Concluído | `[🔄 HOJE]` Em Andamento | `[⏳ PENDENTE]` A Realizar

---

### 🏛️ BLOCO A: FUNDAÇÃO, SITE & POSICIONAMENTO

* `[X]` **Dia 1: Identidade Visual & Front-end Estático**
  * *Entrega:* Construção visual completa das páginas em `site_oficial/` (Home, Gov IA, Setor Público, RIG Tech, Login, Cadastro, Dashboard) com HTML/CSS/JS nativo e i18n (PT, ES, EN).
* `[X]` **Dia 2: Publicação & Infraestrutura de Borda (Cloudflare)**
  * *Entrega:* Deploy do site institucional na Cloudflare Pages com roteamento limpo, SSL/TLS 1.3 e CDN global.
* `[X]` **Dia 3: Configuração do Wize Developer Kit no Repositório**
  * *Entrega:* Inicialização da pasta `.wize/` com `project.toml`, `user.toml` e `tea.toml` para gestão de artefatos e memória do projeto.
* `[X]` **Dia 4: Engenharia de Requisitos & PRD Mestre**
  * *Entrega:* Redação do `brief.md` e `prd.md` consolidando os Critérios de Aceite (AC-01 a AC-14) e as regras comerciais dos 3 ramos.
* `[X]` **Dia 5: Política Global de Clean Code & Qualidade dos Agentes**
  * *Entrega:* Elaboração dos 7 arquivos de qualidade e governança (`WIZE_GLOBAL_ENFORCEMENT_POLICY.md`, `WIZE_CLEAN_CODE_POLICY.md`, `AGENTS.md`, etc.).
* `[X]` **Dia 6: Arquitetura de Microserviços & Bounded Contexts**
  * *Entrega:* Mapeamento dos 6 microserviços com banco de dados isolado (*Database-per-Service*) e formalização da auditoria Controlador vs. Operador (LGPD) nos 129 Filtros.
* `[X]` **Dia 7: Otimização da Jornada de Entrada no Hero**
  * *Entrega:* Implementação da bifurcação guiada na Home (`site_oficial/index.html`) separando *Blindar Minha Organização* de *Parceria White-Label*.

---

### 🎯 BLOCO B: CALIBRAÇÃO DE MERCADO, PREÇOS & CONVERSÃO

* `[🔄 HOJE]` **Dia 8: Benchmarking de Preços & Concorrentes (Pesquisa Manus)**
  * *Entrega:* Varredura de mercado de 5 concorrentes por ramo (Gov IA Brasil/Mundo, Setor Público Brasil, RIG Tech Brasil) mapeando faixas de preço e contratações diretas.
* `[⏳ PENDENTE]` **Dia 9: Calibração Final da Tabela de Preços & Planos**
  * *Entrega:* Ajuste fino dos valores e regras de pacotes (Standard, Enterprise, Dispensa 14.133 e White-Label com Setup Isento) nas 4 páginas do site.
* `[⏳ PENDENTE]` **Dia 10: Simulador de Risco em 60s & Conexão dos CTAs com o App**
  * *Entrega:* Inclusão do mini-quiz de diagnóstico na Home e apontamento de todos os botões de compra para `/app/cadastro.html` sem fricção de e-mail.

---

### 🧱 BLOCO C: INFRAESTRUTURA LOCAL & BANCOS ISOLADOS

* `[⏳ PENDENTE]` **Dia 11: Ambiente Docker de Banco & Fila**
  * *Entrega:* Criação do `docker-compose.yml` subindo PostgreSQL 16 e Redis 7 com volumes persistentes.
* `[⏳ PENDENTE]` **Dia 12: Script de Inicialização dos 6 Bancos Independentes**
  * *Entrega:* Script SQL `init_databases.sql` criando `db_identity`, `db_gov_ai`, `db_gov_municipal`, `db_rigtech`, `db_forensic_ledger` e `db_admin_billing`.

---

### 🔑 BLOCO D: MICROSERVIÇO 1 — `ms-identity` (ACESSO & WHITE-LABEL)

* `[⏳ PENDENTE]` **Dia 13: Modelagem de Dados de Acesso (`db_identity`)**
  * *Entrega:* Tabelas de Organizações, Tenants, Usuários, Perfis (Admin/Tenant/WL) e Chaves de API via SQLAlchemy/Alembic.
* `[⏳ PENDENTE]` **Dia 14: Serviço de Autenticação JWT & Segurança**
  * *Entrega:* Endpoints `/api/v1/auth/login` e `/api/v1/auth/register` com hashing Argon2, refresh tokens e RBAC.
* `[⏳ PENDENTE]` **Dia 15: Conexão Real das Telas de Login e Cadastro**
  * *Entrega:* Conexão de `site_oficial/app/login.html` e `cadastro.html` via `fetch` assíncrono com validação de sessão e redirecionamento para o Dashboard.

---

### 🔐 BLOCO E: MICROSERVIÇO 2 — `ms-forensic-ledger` (PROVA CRIPTOGRÁFICA)

* `[⏳ PENDENTE]` **Dia 16: Modelagem do Livro Probatório Imutável (`db_forensic_ledger`)**
  * *Entrega:* Tabela `forensic_ledger` sequencial estrita com constraints de integridade e hash anterior.
* `[⏳ PENDENTE]` **Dia 17: Motor de Encadeamento SHA-256 & Verificador Anti-Fraude**
  * *Entrega:* Serviço matemático `ForensicLedgerService` que calcula `SHA256(n, payload, H(n-1))` e script de auditoria `verify_chain.py`.
* `[⏳ PENDENTE]` **Dia 18: Dynamic Report Engine (Gerador de Laudos Periciais em PDF)**
  * *Entrega:* Motor de renderização de PDF formal com cabeçalho pericial, resumo de riscos, QR Code de validação e carimbo WORM.

---

### 🌐 BLOCO F: MICROSERVIÇOS DE NEGÓCIO DOS 3 RAMOS

* `[⏳ PENDENTE]` **Dia 19: `ms-gov-ai` — Sentinel Discovery & Mascaramento PII**
  * *Entrega:* API de inventário de modelos, detecção de Shadow AI e sanitização automática de CPFs/cartões/senhas no `db_gov_ai`.
* `[⏳ PENDENTE]` **Dia 20: `ms-gov-ai` — Controlador CPT Inline & Auditoria Controlador-Operador**
  * *Entrega:* Avaliador em tempo real dos 129 Filtros em < 50ms e módulo de verificação de DPAs/responsabilidade de operadores terceiros (LGPD).
* `[⏳ PENDENTE]` **Dia 21: `ms-gov-municipal` — Radar & Vigília do CAUC**
  * *Entrega:* Monitoramento dos 27 itens de conformidade fiscal de prefeituras e cálculo de prazos de vencimento do SICONFI (RREO/RGF) no `db_gov_municipal`.
* `[⏳ PENDENTE]` **Dia 22: `ms-gov-municipal` — Módulo Compras & Executa**
  * *Entrega:* Validador de limite anual de Dispensa de Licitação (Lei 14.133) e rastreador de convênios Transferegov.br.
* `[⏳ PENDENTE]` **Dia 23: `ms-rigtech` — Módulo LEX (Indexador de Diários Oficiais)**
  * *Entrega:* Coleta e processamento de textos de APIs legislativas e diários oficiais usando IA no `db_rigtech`.
* `[⏳ PENDENTE]` **Dia 24: `ms-rigtech` — Módulo Alerta & Módulo Prova**
  * *Entrega:* Motor de correspondência de risco por árvore de palavras-chave e carimbo de tempo SHA-256 contra apagão de dados.

---

### 📊 BLOCO G: DINAMIZAÇÃO DO DASHBOARD DO CLIENTE (`/app/dashboard.html`)

* `[⏳ PENDENTE]` **Dia 25: Hidratação dos Cards de Métricas em Tempo Real**
  * *Entrega:* Integração dos 3 cards superiores (PLs RIG, IAs validadas, Alertas Críticos) com os endpoints de agregação dos microserviços.
* `[⏳ PENDENTE]` **Dia 26: Feed de Atividades do Ledger & Ação "Gerar Relatório Geral"**
  * *Entrega:* Listagem ao vivo dos eventos SHA-256 na tela e modal funcional de emissão/download do Laudo Pericial em PDF.

---

### 👑 BLOCO H: MICROSERVIÇO 6 — `ms-admin-billing` (PAINEL DO DONO & SLACK)

* `[⏳ PENDENTE]` **Dia 27: Gestão Financeira & Webhooks de Pagamento**
  * *Entrega:* Modelagem do `db_admin_billing`, integração de webhooks (Stripe/Asaas) para ativação imediata pós-pagamento.
* `[⏳ PENDENTE]` **Dia 28: Regras Freemium, Travamento por Inadimplência & Alertas Slack**
  * *Entrega:* Motor de degustação, bloqueio automático de acesso após 7 dias de atraso e notificações em tempo real nos canais `#vendas` e `#alertas-dev` do Slack.
* `[⏳ PENDENTE]` **Dia 29: Construção da Tela Super Admin (`/admin/dashboard.html`)**
  * *Entrega:* Interface exclusiva do dono com MRR consolidado, lista de tenants e botões de ação rápida (Liberar/Travar).

---

### 🛡️ BLOCO I: AUDITORIA DE SEGURANÇA, PENTEST & HOMOLOGAÇÃO

* `[⏳ PENDENTE]` **Dia 30: Bateria de Testes Globais & Pentest com Natasha Romanoff**
  * *Entrega:* Execução dos 6 Gates de Teste do Hawkeye e varredura estática/dinâmica (SAST/DAST) com relatório `report.html` (Zero Brechas).

---

### 🚀 BLOCO J: DEPLOY EM PRODUÇÃO NA AWS & GO-LIVE

* `[⏳ PENDENTE]` **Dia 31: Provisionamento AWS São Paulo (`sa-east-1`) via Terraform**
  * *Entrega:* Criação do RDS PostgreSQL Multi-AZ, S3 Object Lock (WORM 10 anos), ECS Fargate e Redis ElastiCache.
* `[⏳ PENDENTE]` **Dia 32: CI/CD, Conexão DNS Cloudflare ➔ AWS & GO-LIVE OFICIAL**
  * *Entrega:* Publicação dos microserviços em produção, apontamento de domínio e lançamento oficial da plataforma BRACHATEC.
