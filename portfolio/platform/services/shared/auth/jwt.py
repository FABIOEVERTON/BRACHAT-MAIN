"""Autenticação e autorização compartilhadas (PRD §3.1).

- JWT HS256 (pyjwt) com expiração 1h + refresh 7d
- RBAC por matriz role × permission (nomes EXATOS do PRD §3.1)
- MFA obrigatório para TENANT_ADMIN e WHITELABEL_OPERATOR
- Segredos via env (JWT_SECRET / JWT_SERVICE_SECRET) — nunca em código
"""

import os
import time
from enum import StrEnum

import jwt

# --- Roles e permissions (PRD §3.1, nomes exatos) ---


class Role(StrEnum):
    EZRA_ADMIN = "EZRA_ADMIN"
    TENANT_ADMIN = "TENANT_ADMIN"
    TENANT_AUDITOR = "TENANT_AUDITOR"
    TENANT_VIEWER = "TENANT_VIEWER"
    WHITELABEL_OPERATOR = "WHITELABEL_OPERATOR"
    WHITELABEL_ADMIN = "WHITELABEL_ADMIN"


class Permission(StrEnum):
    LAUDO_EMIT = "laudo:emit"
    LAUDO_VIEW = "laudo:view"
    SCAN_EXECUTE = "scan:execute"
    MONITOR_CONFIGURE = "monitor:configure"
    GATEWAY_CONFIGURE = "gateway:configure"
    TENANT_MANAGE = "tenant:manage"
    BILLING_VIEW = "billing:view"
    WHITELABEL_CONFIGURE = "whitelabel:configure"


# Matriz RBAC: role -> permissions concedidas
RBAC_MATRIX: dict[Role, set[Permission]] = {
    Role.EZRA_ADMIN: set(Permission),  # interno EZRA: tudo
    Role.TENANT_ADMIN: {
        Permission.LAUDO_EMIT,
        Permission.LAUDO_VIEW,
        Permission.SCAN_EXECUTE,
        Permission.MONITOR_CONFIGURE,
        Permission.GATEWAY_CONFIGURE,
        Permission.TENANT_MANAGE,
        Permission.BILLING_VIEW,
    },
    Role.TENANT_AUDITOR: {
        Permission.LAUDO_VIEW,
        Permission.BILLING_VIEW,
    },
    Role.TENANT_VIEWER: {
        Permission.LAUDO_VIEW,
    },
    Role.WHITELABEL_OPERATOR: {
        Permission.LAUDO_EMIT,
        Permission.LAUDO_VIEW,
    },
    Role.WHITELABEL_ADMIN: {
        Permission.LAUDO_VIEW,
        Permission.BILLING_VIEW,
        Permission.WHITELABEL_CONFIGURE,
    },
}

# MFA obrigatório (PRD §3.1 req 3)
MFA_REQUIRED_ROLES = {Role.TENANT_ADMIN, Role.WHITELABEL_OPERATOR}

ACCESS_TOKEN_TTL_S = 3600  # 1h
REFRESH_TOKEN_TTL_S = 7 * 24 * 3600  # 7d

# Proteção: tokens nunca logados (NFR Sec)
_LOGGED_KEYS = frozenset()


def _secret() -> str:
    secret = os.environ.get("JWT_SERVICE_SECRET") or os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET/JWT_SERVICE_SECRET ausente — defina no ambiente")
    return secret


def encode_token(
    *,
    sub: str,
    role: Role | str,
    tenant_id: str | None,
    ttl_s: int = ACCESS_TOKEN_TTL_S,
    typ: str = "access",
) -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "role": str(role),
        "tenant_id": tenant_id,
        "iat": now,
        "exp": now + ttl_s,
        "typ": typ,
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def issue_tokens(*, sub: str, role: Role | str, tenant_id: str | None) -> tuple[str, str]:
    """Retorna (access_token 1h, refresh_token 7d)."""
    access = encode_token(sub=sub, role=role, tenant_id=tenant_id, typ="access")
    refresh = encode_token(
        sub=sub, role=role, tenant_id=tenant_id, ttl_s=REFRESH_TOKEN_TTL_S, typ="refresh"
    )
    return access, refresh


def decode_token(token: str) -> dict:
    """Verifica assinatura/expiração e retorna claims. Lança jwt.InvalidTokenError."""
    return jwt.decode(token, _secret(), algorithms=["HS256"])


def mfa_required_for(role: Role | str) -> bool:
    return Role(role) in MFA_REQUIRED_ROLES