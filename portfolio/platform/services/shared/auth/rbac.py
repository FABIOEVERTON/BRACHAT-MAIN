"""RBAC — verificação de permissões (PRD §3.1).

has_permission(role, permission) via RBAC_MATRIX.
Falha de permissão → PermissionDeniedError (o handler converte em 403 RFC 7807).
"""

from services.shared.auth.jwt import Permission, RBAC_MATRIX, Role


class PermissionDeniedError(Exception):
    """Sem permissão para a ação — converte em 403 RFC 7807 (F0-09)."""


def has_permission(role: Role | str, permission: Permission | str) -> bool:
    try:
        r = Role(role)
    except ValueError:
        return False
    return permission in RBAC_MATRIX[r]


def require_permission(role: Role | str, permission: Permission | str) -> None:
    if not has_permission(role, permission):
        raise PermissionDeniedError(f"role {role} não tem permissão {permission}")


def permissions_for(role: Role | str) -> set[str]:
    try:
        return {str(p) for p in RBAC_MATRIX[Role(role)]}
    except (KeyError, ValueError):
        return set()