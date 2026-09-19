"""Tenant resolver (PRD §8.2) — espelho Python da lógica TS (apps/web/lib/tenant-resolver.ts).

FASE 0: determinístico. S08: lookup customDomain → tenant via cache/DB.
Keys de retorno usam os nomes REAIS dos headers HTTP (x-tenant-id / x-tenant-branch).
"""

from typing import Literal, TypedDict

TenantBranch = Literal["gov_ai", "gov_municipal"]

TenantContextHeaders = TypedDict(
    "TenantContextHeaders",
    {"x-tenant-id": str, "x-tenant-branch": TenantBranch},
)


def resolve_tenant_sync(hostname: str) -> TenantContextHeaders:
    root = hostname.replace("www.", "", 1).lower()
    is_ezra = root == "ezra.com.br" or root.endswith(".ezra.com.br")

    if is_ezra:
        slug = "ezra" if root == "ezra.com.br" else root.split(".")[0] or "ezra"
        return {"x-tenant-id": slug, "x-tenant-branch": "gov_ai"}

    return {"x-tenant-id": root.split(".")[0] or "ezra", "x-tenant-branch": "gov_municipal"}