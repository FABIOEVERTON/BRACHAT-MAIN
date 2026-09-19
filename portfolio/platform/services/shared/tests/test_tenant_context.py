"""Testes unit — tenant context (E0-S04 F0-12).

Cobre F0-12: set_tenant_schema aplica search_path scoped + ContextVar.
Sem banco: conn é mock (assert SQL emitido).
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection

from services.shared.tenant.context import current_tenant, set_tenant_schema


class FakeConnection:
    """Registra o SQL executado sem tocar banco."""

    def __init__(self):
        self.executed: list[str] = []

    async def execute(self, stmt):
        # stmt é um SQLAlchemy TextClause; recupera o texto compilado
        self.executed.append(str(stmt.compile(compile_kwargs={"literal_binds": True})))
        return None


@pytest.mark.asyncio
async def test_f012_set_tenant_schema_sets_search_path_and_contextvar():
    conn = FakeConnection()
    await set_tenant_schema(conn, "tenant_abc")  # type: ignore[arg-type]
    assert current_tenant.get() == "tenant_abc"
    assert len(conn.executed) == 1
    sql = conn.executed[0]
    assert "SET LOCAL search_path" in sql
    assert "tenant_abc" in sql
    # NUNCA global: sem "SET search_path" sem LOCAL
    assert "SET LOCAL" in sql


@pytest.mark.asyncio
async def test_search_path_includes_public():
    conn = FakeConnection()
    await set_tenant_schema(conn, "tenant_xyz")
    assert "public" in conn.executed[0]