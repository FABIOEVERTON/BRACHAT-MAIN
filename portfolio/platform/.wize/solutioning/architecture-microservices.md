# Arquitetura de Microserviços & Database-per-Service — BRACHATEC Platform

## 1. Visão Geral da Separação por Bounded Contexts

Cada microserviço é um serviço independente em **FastAPI (Python)**, com seu próprio repositório/pasta, ciclo de vida de deploy isolado, dependências próprias e seu **Banco de Dados PostgreSQL 16 exclusivo**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            API GATEWAY / KONG                               │
│      Roteamento TLS 1.3, Rate-Limiting e Validação Inicial de JWT           │
└──────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────┘
       │              │              │              │              │
       ▼              ▼              ▼              ▼              ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐
│  MS-IDENTITY ││  MS-GOV-AI   ││ MS-GOV-MUNI  ││  MS-RIGTECH  ││MS-BILLING-ADM│
│  (Auth & WL) ││(Sentinel/CPT)││(CAUC/14.133) ││ (LEX Scraper)││(Admin/Slack) │
└──────┬───────┘└──────┬───────┘└──────┬───────┘└──────┬───────┘└──────┬───────┘
       │               │               │               │               │
       ▼               ▼               ▼               ▼               ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐
│ DB_IDENTITY  ││  DB_GOV_AI   ││ DB_GOV_MUNI  ││  DB_RIGTECH  ││  DB_BILLING  │
│  (Postgres)  ││  (Postgres)  ││  (Postgres)  ││  (Postgres)  ││  (Postgres)  │
└──────────────┘└──────┬───────┘└──────┬───────┘└──────┬───────┘└──────────────┘
                       │               │               │
                       └───────────────┼───────────────┘
                                       ▼ (Eventos de Auditoria)
                       ┌───────────────────────────────┐
                       │     MESSAGE BUS (RabbitMQ)    │
                       └───────────────┬───────────────┘
                                       ▼
                       ┌───────────────────────────────┐
                       │      MS-FORENSIC-LEDGER       │
                       │ • Encadeamento SHA-256        │
                       │ • Dynamic Report Engine (PDF) │
                       │ • Custódia S3 WORM            │
                       └───────────────┬───────────────┘
                                       ▼
                       ┌───────────────────────────────┐
                       │       DB_FORENSIC_LEDGER      │
                       │   (Postgres Ledger Imutável)  │
                       └───────────────────────────────┘
```

---

## 2. Especificação dos 6 Microserviços & Bancos Independentes

### 1. `ms-identity` (Núcleo de Acesso & Multi-Tenant)
* **Backend:** `services/identity/` (FastAPI / SQLAlchemy)
* **Banco de Dados:** `db_identity`
* **Responsabilidade:**
  - Login e Cadastro pós-pagamento.
  - Geração de tokens JWT corporativos com role-based access control (RBAC).
  - Gestão de parceiros White-Label e vinculação de subtenants.

### 2. `ms-gov-ai` (Ramo 1: Governança de IA & 129 Filtros)
* **Backend:** `services/gov-ai/` (FastAPI / Pydantic)
* **Banco de Dados:** `db_gov_ai`
* **Responsabilidade:**
  - Sentinel Discovery (Mapeamento de Shadow AI e APIs corporativas).
  - Controlador CPT Inline (Avaliação dos 129 filtros em < 50ms).
  - **Módulo de Auditoria Controlador vs Operador (LGPD Arts. 37/39/42):** Mapeamento e checagem de DPAs e limites de atuação dos operadores de IA terceiros.

### 3. `ms-gov-municipal` (Ramo 2: Setor Público & Blindagem Fiscal)
* **Backend:** `services/gov-municipal/` (FastAPI)
* **Banco de Dados:** `db_gov_municipal`
* **Responsabilidade:**
  - Radar & Vigília: monitoramento diário dos 27 itens de regularidade do CAUC e certidões.
  - Módulo Compras: auditoria de editais, contratos e validação da Dispensa de Licitação (Lei 14.133).
  - Módulo Executa: rastreamento de convênios (Transferegov.br).

### 4. `ms-rigtech` (Ramo 3: Inteligência Legislativa & Diários Oficiais)
* **Backend:** `services/rigtech/` (FastAPI / Background Workers)
* **Banco de Dados:** `db_rigtech`
* **Responsabilidade:**
  - Módulo LEX: ingestão e indexação contínua de APIs parlamentares e diários oficiais.
  - Módulo Alerta: correspondência em tempo real por árvores de palavras-chave.
  - Módulo Prova: carimbo de tempo SHA-256 de matérias publicadas contra apagão de dados.

### 5. `ms-forensic-ledger` (Coração Probatório & Relatórios Dinâmicos)
* **Backend:** `services/forensic-ledger/` (FastAPI / ReportLab / Jinja2)
* **Banco de Dados:** `db_forensic_ledger`
* **Responsabilidade:**
  - Consumo de eventos via Message Bus e cálculo sequencial `SHA256(n, payload, H(n-1))`.
  - Emissão de Laudos Periciais em PDF formal com QR Code de validação e exportação JSON assinada.
  - Envio de cópias de segurança para AWS S3 Object Lock (WORM).

### 6. `ms-admin-billing` (Painel do Dono, Cobrança & Slack)
* **Backend:** `services/admin-billing/` (FastAPI / Slack SDK)
* **Banco de Dados:** `db_admin_billing`
* **Responsabilidade:**
  - Painel Super Admin exclusivo do dono (`/admin/dashboard.html`).
  - Webhooks de pagamento (Stripe/Asaas/Pagar.me), gestão freemium e travamento automático de inadimplentes.
  - Disparo de alertas em tempo real no Slack (`#vendas`, `#alertas-dev` e Heartbeat diário).
