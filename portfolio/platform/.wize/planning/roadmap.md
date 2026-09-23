# Cronograma Ultra-Granular Passo a Passo (Roadmap Arquivo por Arquivo)

* **Princípio de Execução:** Transparência total. Cada arquivo, modelo, endpoint e script será exibido, explicado e testado individualmente com você antes de avançar para o próximo.

---

## 🧱 BLOCO 1: Fundação do Back-end & Banco Multi-Tenant (Dias 1 a 4)

### Passo 1.1: Docker & Ambiente PostgreSQL 16
* **Arquivo:** `docker-compose.yml`
* **O que faz:** Sobe o container PostgreSQL 16 local na porta 5432, configurado com suporte a schemas múltiplos e persistência em volume seguro.
* **Validação:** Container rodando e respondendo ao comando de ping.

### Passo 1.2: Gerenciador de Configuração & Variáveis de Ambiente
* **Arquivos:** `services/shared/config.py`, `.env.example`
* **O que faz:** Carrega com segurança variáveis de ambiente (JWT_SECRET, DATABASE_URL, AWS_REGION sa-east-1, WORM_ENABLED) via Pydantic `BaseSettings`.
* **Validação:** Script de teste de leitura das configs.

### Passo 1.3: Conexão com Banco & Gerenciador de Schemas (`schema-per-tenant`)
* **Arquivos:** `services/shared/database.py`, `services/shared/tenant_manager.py`
* **O que faz:** Cria a engine assíncrona SQLAlchemy/asyncpg e a função `create_tenant_schema(tenant_slug)` que roda o DDL `CREATE SCHEMA IF NOT EXISTS tenant_{slug}` dinamicamente.
* **Validação:** Teste de criação e isolamento de 2 schemas diferentes.

### Passo 1.4: Modelos de Dados Centrais (Users, Tenants, WhiteLabel)
* **Arquivos:** `services/shared/models/tenants.py`, `services/shared/models/users.py`
* **O que faz:** Define as tabelas públicas de controle: `public.tenants` (ID, nome, slug, plano, status, white_label_parent_id) e `public.users` (ID, tenant_id, email, senha com hash Argon2, role).
* **Validação:** Migração de criação das tabelas no banco.

### Passo 1.5: Serviço de Autenticação JWT & Criptografia de Senhas
* **Arquivo:** `services/shared/auth_service.py`
* **O que faz:** Funções `hash_password`, `verify_password`, `create_access_token` (com payload contendo `tenant_id` e `role`) e decodificação segura.
* **Validação:** Teste unitário de geração e expiração de token.

### Passo 1.6: Middleware de Resolução Automática de Tenant
* **Arquivo:** `services/shared/middleware/tenant_middleware.py`
* **O que faz:** Intercepta cada requisição HTTP, extrai o Bearer token, define a sessão do banco no schema correto (`SET search_path TO tenant_{slug}`) garantindo isolamento total.
* **Validação:** Teste de chamada com token A tentando acessar dados do tenant B (deve ser bloqueado).

---

## 🔐 BLOCO 2: O Motor do Ledger Probatório SHA-256 (Dias 5 a 7)

### Passo 2.1: Modelo do Livro Probatório (`forensic_ledger`)
* **Arquivo:** `services/shared/models/ledger.py`
* **O que faz:** Tabela presente dentro de cada schema do tenant: `id`, `seq_number`, `timestamp`, `module`, `event_type`, `payload_json`, `previous_hash`, `current_hash`.
* **Validação:** Criação da tabela com constraints de unicidade e ordenação.

### Passo 2.2: Serviço de Encadeamento Criptográfico (`ForensicLedgerService`)
* **Arquivo:** `services/shared/services/ledger_service.py`
* **O que faz:** Lógica matemática de hash:
  - Recupera o último hash do tenant (`H_prev`).
  - Calcula `H_current = SHA256(seq + timestamp + module + payload_json + H_prev)`.
  - Grava a transação de forma atômica (impossível inserir evento sem encadear).
* **Validação:** Teste unitário gerando 5 eventos sequenciais e verificando a cadeia.

### Passo 2.3: Verificador de Integridade & Detecção de Adulteração
* **Arquivo:** `services/shared/services/verify_chain.py`
* **O que faz:** Função de auditoria que percorre todo o histórico do banco e valida se todos os hashes batem matematicamente. Se 1 único byte for alterado manualmente, o teste aponta a violação.
* **Validação:** Teste de simulação de ataque/adulteração com detecção imediata.

---

## 🌐 BLOCO 3: APIs dos 3 Módulos de Negócio (Dias 8 a 12)

### Passo 3.1: API do Ramo 1 — Governança de IA (Sentinel & CPT Controller)
* **Arquivos:** `services/gov-ai/routes.py`, `services/gov-ai/cpt_service.py`
* **O que faz:**
  - Endpoint `/api/v1/ai/validate`: recebe prompt/payload de IA, avalia filtros L1 a L5 em < 50ms, mascara PII e grava evento no Ledger SHA-256.
  - Endpoint `/api/v1/ai/metrics`: retorna total de requisições validadas e bloqueadas.
* **Validação:** Envio de requisição com CPF fictício e confirmação de mascaramento e laudo gerado.

### Passo 3.2: API do Ramo 2 — Setor Público (Radar CAUC & Compras 14.133)
* **Arquivos:** `services/gov-municipal/routes.py`, `services/gov-municipal/cauc_service.py`
* **O que faz:**
  - Endpoint `/api/v1/gov/cauc-status`: lista 27 itens de conformidade fiscal e alertas de vencimento (verde/amarelo/vermelho).
  - Endpoint `/api/v1/gov/compras-audit`: valida se dispensas de licitação respeitam o limite anual da Lei 14.133.
* **Validação:** Teste com certidão vencendo em 5 dias gerando alerta crítico.

### Passo 3.3: API do Ramo 3 — RIGTech (LEX & Alertas Legislativos)
* **Arquivos:** `services/rigtech/routes.py`, `services/rigtech/lex_service.py`
* **O que faz:**
  - Endpoint `/api/v1/rig/proposicoes`: lista Projetos de Lei monitorados e matérias do Diário Oficial.
  - Endpoint `/api/v1/rig/alertas`: contagem e detalhes de alertas de risco por palavras-chave.
* **Validação:** Teste de busca de PLs por tema ("Tributário", "Mineração").

---

## 📊 BLOCO 4: Conexão do Front-end & Motor de Relatórios Dinâmicos (Dias 13 a 17)

### Passo 4.1: Conexão da Autenticação (`/app/login.html` e `/app/cadastro.html`)
* **Arquivos:** `site_oficial/app/js/auth.js`, `site_oficial/app/login.html`, `site_oficial/app/cadastro.html`
* **O que faz:** Formulários agora fazem `fetch` real com a API, gravam JWT no `localStorage`/cookie e redirecionam com sessão ativa.
* **Validação:** Fluxo completo de cadastro -> login -> dashboard na interface.

### Passo 4.2: Hidratação em Tempo Real do Dashboard (`/app/dashboard.html`)
* **Arquivo:** `site_oficial/app/js/dashboard.js`
* **O que faz:**
  - Carrega contadores reais nos 3 cards do topo (PLs RIG: 1.248, Requisições IA: 45.902, Alertas Críticos: 3).
  - Popula a tabela de "Últimas Atividades" diretamente dos eventos reais do Ledger SHA-256.
* **Validação:** Inserir um novo evento no back-end e ver ele aparecer dinamicamente na tela sem recarregar.

### Passo 4.3: Motor de Geração de Laudos Periciais Dinâmicos (PDF / JSON)
* **Arquivos:** `services/shared/report_engine.py`, `services/shared/templates/laudo_template.html`
* **O que faz:** Gera um Laudo Pericial formal contendo: Timbre do cliente/White-label, Resumo Executivo, Tabela de Conformidade, Hash SHA-256 encadeado e Carimbo WORM.
* **Validação:** Geração e abertura de um PDF de teste perfeito e diagramado.

### Passo 4.4: Integração do Botão "Gerar Relatório Geral"
* **Arquivos:** `site_oficial/app/dashboard.html`, `site_oficial/app/js/report_modal.js`
* **O que faz:** Ao clicar no botão, chama a API de relatórios, abre um modal de confirmação com o hash gerado e permite baixar o PDF e o JSON assinado.
* **Validação:** Download direto do PDF no navegador.

---

## 🛡️ BLOCO 5: Testes Globais, Pentest de Segurança & Auditoria (Dias 18 a 20)

### Passo 5.1: Bateria de Testes Automatizados (Hawkeye TEA Gate)
* **Arquivo:** `tests/test_full_suite.py`
* **O que faz:** Executa 100% dos testes unitários, testes de carga (<50ms) e integridade do ledger SHA-256.

### Passo 5.2: Pentest de Segurança SAST/DAST (Natasha Romanoff)
* **Arquivo:** `.wize/security/report.html`
* **O que faz:** Varredura de injeção SQL, cross-tenant leak, secrets e integridade de APIs.

### Passo 5.3: Entrega Final & Documentação de Operação
* **Arquivo:** `walkthrough.md`
* **O que faz:** Manual completo de execução e deploy com o sistema 100% testado e funcional.
