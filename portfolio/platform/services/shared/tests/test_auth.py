"""Testes unit — auth JWT + RBAC (E0-S03: F0-07, F0-08, F0-10, F0-11).

Cobre:
- F0-07: JWT válido 1h com claims de roles/permissions/tenant
- F0-08: decode/verify injeta claims corretos
- F0-10: refresh expira > 7d; access expira após 1h
- F0-11: MFA obrigatório para TENANT_ADMIN e WHITELABEL_OPERATOR
"""

import time
from unittest.mock import patch

import jwt as pyjwt
import pytest

from services.shared.auth import (
    ACCESS_TOKEN_TTL_S,
    REFRESH_TOKEN_TTL_S,
    Permission,
    Role,
    decode_token,
    encode_token,
    has_permission,
    issue_tokens,
    mfa_required_for,
    permissions_for,
)


@pytest.fixture(autouse=True)
def _secret(monkeypatch):
    monkeypatch.setenv("JWT_SERVICE_SECRET", "test-secret")


def test_f07_access_token_has_claims_and_expires_1h(_secret):
    token, _refresh = issue_tokens(
        sub="user-1", role=Role.TENANT_ADMIN, tenant_id="tenant_x"
    )
    claims = decode_token(token)
    assert claims["sub"] == "user-1"
    assert claims["role"] == "TENANT_ADMIN"
    assert claims["tenant_id"] == "tenant_x"
    assert claims["typ"] == "access"
    # 1h de vida
    assert claims["exp"] - claims["iat"] == ACCESS_TOKEN_TTL_S


def test_f07_refresh_token_lasts_7d(_secret):
    _access, refresh = issue_tokens(sub="user-1", role=Role.TENANT_ADMIN, tenant_id="tenant_x")
    claims = decode_token(refresh)
    assert claims["typ"] == "refresh"
    assert claims["exp"] - claims["iat"] == REFRESH_TOKEN_TTL_S


def test_f08_decode_injects_correct_claims(_secret):
    token = encode_token(
        sub="auditor-9", role=Role.TENANT_AUDITOR, tenant_id="tenant_y", typ="access"
    )
    claims = decode_token(token)
    assert claims["tenant_id"] == "tenant_y"
    assert claims["role"] == "TENANT_AUDITOR"


def test_f10_expired_access_token_rejected(_secret):
    with patch("time.time", return_value=1_700_000_000):
        token = encode_token(
            sub="u", role=Role.TENANT_VIEWER, tenant_id="t", ttl_s=1, typ="access"
        )
    with patch("time.time", return_value=1_700_000_000 + 7200):  # 2h depois
        with pytest.raises(pyjwt.ExpiredSignatureError):
            decode_token(token)


def test_f10_expired_refresh_invalidates_session(_secret):
    with patch("time.time", return_value=1_700_000_000):
        token = encode_token(
            sub="u",
            role=Role.TENANT_VIEWER,
            tenant_id="t",
            ttl_s=REFRESH_TOKEN_TTL_S,
            typ="refresh",
        )
    # 8 dias depois (> 7d) → inválido (F0-10: usuário re-autentica)
    with patch("time.time", return_value=1_700_000_000 + 8 * 24 * 3600):
        with pytest.raises(pyjwt.ExpiredSignatureError):
            decode_token(token)


@pytest.mark.parametrize(
    ("role", "permission", "expected"),
    [
        # Matriz RBAC (PRD §3.1) — amostra
        (Role.TENANT_ADMIN, Permission.LAUDO_EMIT, True),
        (Role.TENANT_ADMIN, Permission.WHITELABEL_CONFIGURE, False),
        (Role.TENANT_AUDITOR, Permission.LAUDO_VIEW, True),
        (Role.TENANT_AUDITOR, Permission.LAUDO_EMIT, False),
        (Role.TENANT_VIEWER, Permission.LAUDO_VIEW, True),
        (Role.TENANT_VIEWER, Permission.SCAN_EXECUTE, False),
        (Role.WHITELABEL_OPERATOR, Permission.LAUDO_EMIT, True),
        (Role.WHITELABEL_ADMIN, Permission.WHITELABEL_CONFIGURE, True),
        (Role.EZRA_ADMIN, Permission.TENANT_MANAGE, True),
        (Role.EZRA_ADMIN, Permission.LAUDO_EMIT, True),
    ],
)
def test_rbac_matrix(role, permission, expected):
    assert has_permission(role, permission) is expected


def test_rbac_full_matrix_consistency():
    """Nenhuma role retorna permissões fora da matriz; EZRA_ADMIN tem tudo."""
    for role in Role:
        granted = permissions_for(role)
        assert granted == {str(p) for p in _granted(role)}


def _granted(role: Role) -> set[Permission]:
    from services.shared.auth.jwt import RBAC_MATRIX

    return RBAC_MATRIX[role]


def test_f11_mfa_required_roles():
    assert mfa_required_for(Role.TENANT_ADMIN) is True
    assert mfa_required_for(Role.WHITELABEL_OPERATOR) is True
    assert mfa_required_for(Role.TENANT_VIEWER) is False
    assert mfa_required_for(Role.EZRA_ADMIN) is False
    assert mfa_required_for(Role.TENANT_AUDITOR) is False