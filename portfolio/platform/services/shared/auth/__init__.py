"""Auth compartilhada — API pública (PRD §3.1)."""

from services.shared.auth.jwt import (
    ACCESS_TOKEN_TTL_S,
    REFRESH_TOKEN_TTL_S,
    MFA_REQUIRED_ROLES,
    Permission,
    Role,
    decode_token,
    encode_token,
    issue_tokens,
    mfa_required_for,
)
from services.shared.auth.rbac import (
    PermissionDeniedError,
    has_permission,
    permissions_for,
    require_permission,
)

__all__ = [
    "ACCESS_TOKEN_TTL_S",
    "REFRESH_TOKEN_TTL_S",
    "MFA_REQUIRED_ROLES",
    "Permission",
    "Role",
    "decode_token",
    "encode_token",
    "issue_tokens",
    "mfa_required_for",
    "PermissionDeniedError",
    "has_permission",
    "permissions_for",
    "require_permission",
]