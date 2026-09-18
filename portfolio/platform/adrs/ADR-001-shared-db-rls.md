---
status: accepted
date: 2026-09-17
deciders: Tony Stark, Nick Fury
---

# ADR-001 — Shared Database com Row-Level Security (RLS)

## Contexto

PRD §2.1: equilibrar custo (entrada R$ 1.890/mês), isolamento estrito e compliance. Opções: db-per-tenant (custo altíssimo), schema-per-tenant (migrações complexas), shared DB.

## Opções

1. **Database-per-tenant** — isolamento máximo; custo de nuvem e operacional inviável no MVP.
2. **Schema-per-tenant** — médio custo; DDL migrações via Alembic complexas; reservado para Tier 3.
3. **Shared DB + RLS nativo do PostgreSQL** — um banco gerenciado; isolamento no kernel do banco.

## Decisão

**Adotar opção 3**: PostgreSQL 16 com `ENABLE ROW LEVEL SECURITY` + `FORCE ROW LEVEL SECURITY` em 100% das tabelas de negócio, `SET LOCAL app.current_tenant_id` por requisição, e filtro `WHERE tenant_id = :tenant_id` explícito no SQLAlchemy como segunda barreira.

## Consequências

- (+) Custo otimizado; um único banco gerenciado.
- (+) Isolamento aplicado no kernel do banco — falha no código Python não vaza dados.
- (−) Toda tabela nova exige RLS + política + índice `tenant_id` — gate de review obrigatório (Hawkeye).
- (−) Tabelas de alta volumetria (Audit_Logs) exigem particionamento planejado desde o início.