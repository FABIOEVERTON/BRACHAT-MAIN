"""FastAPI dependencies de auth (PRD §3.1 / §9.1).

- get_current_user: lê Authorization Bearer, valida JWT, injeta claims
- require_permission(permission): retorna dependency que aplica RBAC
- 401 para token inválido/ausente; 403 (RFC 7807) para sem permissão (F0-09)
"""

from dataclasses import dataclass
from typing import Annotated, Callable

import jwt as pyjwt
from fastapi import Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse

from services.shared.auth import Permission, PermissionDeniedError, Role, decode_token


@dataclass(frozen=True)
class CurrentUser:
    sub: str
    role: Role
    tenant_id: str | None
    claims: dict

    def has(self, permission: Permission) -> bool:
        from services.shared.auth import has_permission

        return has_permission(self.role, permission)


def problem(status_code: int, title: str, detail: str, type_: str = "about:blank") -> JSONResponse:
    """RFC 7807 (F0-09, PRD §9.1 #2)."""
    from fastapi import Request

    return JSONResponse(
        status_code=status_code,
        content={
            "type": type_,
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": f"urn:ezra:{type_}",
        },
    )


def install_problem_handler(app: "FastAPI") -> None:
    """Registra handler global de HTTPException → RFC 7807 (F0-09)."""

    from fastapi import HTTPException, Request
    from fastapi.responses import JSONResponse as _JSONResponse

    @app.exception_handler(HTTPException)
    async def _http_exception_handler(request: Request, exc: HTTPException) -> _JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "type": "about:blank",
                "title": _title_for(exc.status_code),
                "status": exc.status_code,
                "detail": str(exc.detail),
                "instance": f"urn:ezra:error:{exc.status_code}",
            },
            headers=exc.headers,
        )


def _title_for(code: int) -> str:
    return {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        409: "Conflict",
        429: "Too Many Requests",
    }.get(code, "Error")


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    x_tenant_id: Annotated[str | None, Header()] = None,
) -> CurrentUser:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token ausente",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ", 1)[1]
    try:
        claims = decode_token(token)
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token expirado")
    except pyjwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token inválido")

    try:
        role = Role(claims["role"])
    except (KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="role inválida")

    # Valida tenant context (F0B-03 / S03): claims.tenant_id deve bater com header
    # quando tenant_id é declarado no token. Tenant público (EZRA) admite null.
    user = CurrentUser(sub=claims.get("sub", ""), role=role, tenant_id=claims.get("tenant_id"), claims=claims)

    if user.tenant_id and x_tenant_id and user.tenant_id != x_tenant_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="tenant mismatch")

    # tokens nunca logados (NFR Sec)
    return user


def require_permission(permission: Permission) -> Callable:
    def dependency(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
        if not user.has(permission):
            from services.shared.audit import audit_permission_denied

            audit_permission_denied(
                user=user.sub, role=str(user.role), tenant_id=user.tenant_id,
                permission=str(permission),
            )
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"sem permissão {permission}")
        return user

    return dependency