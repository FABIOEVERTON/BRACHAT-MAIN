"""Tenant context — PRD §3.2 (ContextVar + search_path).

current_tenant: ContextVar carregada por request.
set_tenant_schema: aplica SET search_path TO tenant_{id}, public SCOPED à conexão
do request (nunca global — Protected Behavior, F0-12).
"""

from contextvars import ContextVar

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

from services.shared.db.models import tenant_schema

current_tenant: ContextVar[str | None] = ContextVar("current_tenant", default=None)

PUBLIC_SCHEMA = "public"


async def set_tenant_schema(db: AsyncConnection, tenant_id: str) -> None:
    """Aplica search_path scoped à conexão e carrega o ContextVar (F0-12)."""
    schema = tenant_schema(tenant_id)
    # nunca SET search_path global — sempre scoped à connection do request
    await db.execute(
        text("SET LOCAL search_path TO :schema, public").bindparams(schema=schema)
    )
    current_tenant.set(tenant_id)


def tenant_header(tenant_id: str | None) -> str:
    return tenant_id or current_tenant.get() or ""


class TenantContextError(Exception):
    """Tenant inexistente/suspenso — converte em 403 (F0-15)."""