"""Serviço de tenant — criação com hook de schema (F0-12..F0-15).

create_tenant: persiste tenant em public.tenants + cria schema tenant_{id}
no hook de criação (session única — evita transações aninhadas/loops).
"""

import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from services.shared.db.models import Tenant, TenantBranch, TenantPlan, TenantStatus, tenant_schema


async def create_tenant(
    engine: AsyncEngine,
    *,
    slug: str,
    branch: TenantBranch,
    plan: TenantPlan = TenantPlan.DIRECT,
    active_products: list[str] | None = None,
) -> Tenant:
    tenant = Tenant(
        id=str(uuid.uuid4()),
        slug=slug,
        branch=branch,
        plan=plan,
        active_products=active_products or [],
        status=TenantStatus.ACTIVE,
    )
    schema = tenant_schema(tenant.id)

    async with AsyncSession(engine) as session:
        # Hook: schema do tenant criado antes da persistência (mesma transação/session)
        await session.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
        session.add(tenant)
        await session.commit()
        await session.refresh(tenant)

    return tenant


async def get_tenant_status(engine: AsyncEngine, tenant_id: str) -> TenantStatus | None:
    async with AsyncSession(engine) as session:
        tenant = await session.get(Tenant, tenant_id)
        if tenant is None:
            return None
        return TenantStatus(tenant.status)