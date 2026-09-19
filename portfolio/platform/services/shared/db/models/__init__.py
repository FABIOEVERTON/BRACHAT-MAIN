"""Modelos de banco compartilhados (PRD §2.2 services/shared/db)."""

from services.shared.db.models.tenant import (
    Base,
    Tenant,
    TenantBranch,
    TenantPlan,
    TenantStatus,
    tenant_schema,
)

__all__ = [
    "Base",
    "Tenant",
    "TenantBranch",
    "TenantPlan",
    "TenantStatus",
    "tenant_schema",
]