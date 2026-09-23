# EPIC-01: Core Multi-Tenant, Autenticação e Ledger SHA-256

* **Objetivo:** Estabelecer a fundação do sistema: banco de dados PostgreSQL 16 schema-per-tenant, autenticação JWT e motor de encadeamento criptográfico.
* **Stories:**
  * `STORY-01.1`: Setup do Monorepo, Configurações e Modelagem de Banco com Alembic / SQLAlchemy.
  * `STORY-01.2`: Serviço de Autenticação, Registro pós-pagamento e Middleware de Tenant.
  * `STORY-01.3`: Motor Core de Encadeamento SHA-256 (`ForensicLedgerService`).
