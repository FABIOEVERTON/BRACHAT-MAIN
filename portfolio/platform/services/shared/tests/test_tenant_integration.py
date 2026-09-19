"""Testes de integração — isolamento cross-tenant (E0-S04 F0-13, F0-15).

Requer Postgres 16: usa DATABASE_URL_TEST ou default localhost:5433 (compose ezra-dev).
Prova o AC CRÍTICO: dados do tenant A INVISÍVEIS no schema do tenant B.
"""

import os

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import NullPool
from uuid import uuid4

from services.shared.db.models import TenantBranch, TenantPlan, tenant_schema
from services.shared.tenant.service import create_tenant, get_tenant_status

TEST_DB_URL = os.environ.get(
    "DATABASE_URL_TEST",
    "postgresql+asyncpg://ezra:dev_password@localhost:5433/ezra",
)


@pytest_asyncio.fixture
async def engine() -> AsyncEngine:
    eng = create_async_engine(TEST_DB_URL, poolclass=NullPool)
    # schema public.tenants garantido
    async with eng.begin() as conn:
        await conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS public.tenants ("
                "id VARCHAR(36) PRIMARY KEY, slug VARCHAR(63) UNIQUE, branch VARCHAR(16), "
                "plan VARCHAR(16), whitelabel_config_id VARCHAR(36), active_products TEXT[], "
                "chain_anchor_hash VARCHAR(64), created_at TIMESTAMPTZ, status VARCHAR(16))"
            )
        )
    yield eng
    await eng.dispose()


@pytest.mark.asyncio
async def test_f013_cross_tenant_isolation(engine: AsyncEngine):
    a = await create_tenant(engine, slug=f"t-a-{uuid4().hex[:8]}", branch=TenantBranch.GOV_AI, plan=TenantPlan.DIRECT)
    b = await create_tenant(engine, slug=f"t-b-{uuid4().hex[:8]}", branch=TenantBranch.GOV_AI, plan=TenantPlan.DIRECT)
    assert a.id != b.id

    schema_a = tenant_schema(a.id)
    schema_b = tenant_schema(b.id)

    async with engine.begin() as conn:
        # cria tabela de dados em cada schema
        await conn.execute(text(f'CREATE TABLE IF NOT EXISTS "{schema_a}".saldo (valor INT)'))
        await conn.execute(text(f'CREATE TABLE IF NOT EXISTS "{schema_b}".saldo (valor INT)'))
        await conn.execute(text(f'INSERT INTO "{schema_a}".saldo VALUES (100)'))
        await conn.execute(text(f'INSERT INTO "{schema_b}".saldo VALUES (999)'))

    # Query no schema A NÃO vê dado do B
    async with engine.connect() as conn:
        await conn.execute(text(f'SET LOCAL search_path TO "{schema_a}", public'))
        row_a = (await conn.execute(text("SELECT valor FROM saldo"))).scalar()
        assert row_a == 100  # só o valor de A

    async with engine.connect() as conn:
        await conn.execute(text(f'SET LOCAL search_path TO "{schema_b}", public'))
        row_b = (await conn.execute(text("SELECT valor FROM saldo"))).scalar()
        assert row_b == 999  # só o valor de B (nada do A)

    # Assert bilateral: prova isolamento por construção (ADR-002)
    assert row_a != row_b


@pytest.mark.asyncio
async def test_f012_schema_created_on_tenant_creation(engine: AsyncEngine):
    t = await create_tenant(engine, slug=f"t-hook-{uuid4().hex[:8]}", branch=TenantBranch.GOV_MUNICIPAL)
    schema = tenant_schema(t.id)
    async with engine.connect() as conn:
        found = (
            await conn.execute(
                text("SELECT 1 FROM information_schema.schemata WHERE schema_name = :s"),
                {"s": schema},
            )
        ).scalar()
    assert found == 1


@pytest.mark.asyncio
async def test_f015_suspended_tenant_status_persisted(engine: AsyncEngine):
    t = await create_tenant(engine, slug=f"t-susp-{uuid4().hex[:8]}", branch=TenantBranch.GOV_AI)
    # suspende direto no banco (mudança de status)
    async with engine.begin() as conn:
        await conn.execute(
            text("UPDATE public.tenants SET status = 'suspended' WHERE id = :id"), {"id": t.id}
        )
    status = await get_tenant_status(engine, t.id)
    assert status.value == "suspended"