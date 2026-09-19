"""Modelo de dados multi-tenant (PRD §3.2, ADR-002 schema-per-tenant).

Tenant em public.tenants; dados do tenant em schema tenant_{id}. Isolamento por
construção — nunca row-level security (decisão ADR-002: único defensável para
laudos com validade jurídica).
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import ARRAY, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TenantBranch(str, enum.Enum):
    GOV_AI = "gov_ai"
    GOV_MUNICIPAL = "gov_municipal"


class TenantPlan(str, enum.Enum):
    DIRECT = "direct"
    WHITELABEL = "whitelabel"


class TenantStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"


def tenant_schema(tenant_id: str) -> str:
    return f"tenant_{tenant_id}"


class Tenant(Base):
    """PRD §3.2 — campos exatos.

    Enums usam String + validação Python (Enum types pg só via migration formal
    no Alembic — evita dependência de CREATE TYPE em dev/test).
    """

    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    slug: Mapped[str] = mapped_column(String(63), unique=True)
    branch: Mapped[str] = mapped_column(String(16))
    plan: Mapped[str] = mapped_column(String(16))
    whitelabel_config_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    active_products: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    chain_anchor_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(String(16), default=TenantStatus.ACTIVE)