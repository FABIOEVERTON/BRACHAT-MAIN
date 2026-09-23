# Arquitetura de Sistemas — BRACHATEC Engine

## 1. Visão Geral dos Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT LAYER                          │
│   site_oficial (Marketing)  │  /app (Portal Autenticado)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / TLS 1.3
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     API GATEWAY / ROUTER                    │
│                 FastAPI Core API Gateway                    │
└──────┬───────────────────────┼───────────────────────┬──────┘
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  Gov-AI SVC  │       │ Gov-Muni SVC │       │  RIGTech SVC │
│ • Sentinel   │       │ • Radar/Vig. │       │ • Lex Scrap. │
│ • CPT Inline │       │ • Compras    │       │ • Alertas    │
│ • TimeTravel │       │ • Executa    │       │ • Prova Time │
└──────┬───────┘       └──────┬───────┘       └──────┬───────┘
       │                      │                      │
       └──────────────────────┼──────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 SHARED SERVICES & LEDGER                    │
│   • Auth & Tenant Manager   • Dynamic Report Engine (PDF)   │
│   • SHA-256 Chained Ledger  • WORM Storage Adapter (S3)     │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                        │
│         PostgreSQL 16 (Schema-per-Tenant Isolated)          │
└─────────────────────────────────────────────────────────────┘
```

## 2. Modelagem do Livro Probatório (Chained Ledger)
Tabela central de auditoria: `tenant_{id}.forensic_ledger`:
* `id`: UUID (Chave Primária)
* `sequence_number`: BigInt sequencial estrito
* `timestamp`: ISO-8601 UTC
* `module`: Enum ('GOV_AI', 'GOV_MUNI', 'RIG_TECH', 'SYSTEM')
* `event_type`: Varchar (ex: 'CPT_PII_BLOCKED', 'CAUC_ALERT', 'LEX_BILL_INDEXED', 'REPORT_ISSUED')
* `payload_json`: JSONB com dados técnicos estruturados
* `previous_hash`: Varchar(64) — Hash SHA-256 do registro `sequence_number - 1`
* `current_hash`: Varchar(64) — `SHA256(sequence_number + timestamp + module + payload_json + previous_hash)`
* `worm_receipt_id`: Varchar opcional (ID de custódia S3 WORM)
