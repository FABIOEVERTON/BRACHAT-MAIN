"""Tenant — contexto e resolução (PRD §3.2, §8.2)."""

from services.shared.tenant.context import (
    TenantContextError,
    current_tenant,
    set_tenant_schema,
)
from services.shared.tenant.resolver import TenantContextHeaders, resolve_tenant_sync

__all__ = [
    "TenantContextError",
    "current_tenant",
    "set_tenant_schema",
    "TenantContextHeaders",
    "resolve_tenant_sync",
]