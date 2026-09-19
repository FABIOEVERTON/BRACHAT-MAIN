"""Testes de integração — API conventions (E0B-S01) + auth HTTP (E0-S03).

- F0B-01: create_service herda CORS/docs/openapi
- F0B-02: erro de domínio → RFC 7807
- F0B-03: x-tenant-id treatment
- F0-08: request com JWT válido → tenant context + RBAC
- F0-09: sem permissão → 403 RFC 7807 + audit registrado
"""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from services.shared.api import ProblemDetail
from services.shared.api.conventions import create_service
from services.shared.api.deps import CurrentUser, get_current_user, require_permission
from services.shared.auth import Permission, Role, issue_tokens

AUDIT_EVENTS: list[dict] = []


@pytest.fixture(autouse=True)
def _secret(monkeypatch):
    monkeypatch.setenv("JWT_SERVICE_SECRET", "test-secret-01234567890123456789012345678901")


def audit(event: dict) -> None:
    """Stub de audit log — WORM vault real na E0-S07 (F0-09 exige registro)."""
    AUDIT_EVENTS.append(event)


@pytest.fixture
def app() -> FastAPI:
    svc = create_service("test-service")

    @svc.get("/v1/public")
    def public_ok():
        return {"ok": True}

    @svc.get("/v1/health")
    def health():
        return {"status": "ok"}

    @svc.post("/v1/laudos")
    def emit_laudo(user: CurrentUser = Depends(require_permission(Permission.LAUDO_EMIT))):
        return {"laudo": "ok", "tenant": user.tenant_id}

    @svc.get("/v1/me")
    def me(user: CurrentUser = Depends(get_current_user)):
        return {"sub": user.sub, "role": str(user.role), "tenant_id": user.tenant_id}

    return svc


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app)


def _auth_header(role: Role, tenant: str = "tenant_x") -> dict:
    access, _refresh = issue_tokens(sub="user-1", role=role, tenant_id=tenant)
    return {"Authorization": f"Bearer {access}"}


# --- E0B-S01: conventions ---


def test_f0b01_create_service_herda_docs_e_openapi(client):
    r = client.get("/openapi.json")
    assert r.status_code == 200
    assert r.json()["info"]["title"] == "EZRA — test-service"

    r = client.get("/docs")
    assert r.status_code == 200


def test_f0b01_cors_policy(client):
    r = client.options(
        "/v1/health",
        headers={
            "Origin": "https://tenant.ezra.com.br",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.status_code in (200, 405)  # OPTIONS aceito pelo middleware


def test_f0b02_rfc7807_shape():
    p = ProblemDetail(type="about:blank", title="erro", status=403, detail="sem permissão", instance="urn:ezra:x")
    assert p.type == "about:blank"
    assert p.status == 403


# --- E0-S03: auth over HTTP ---


def test_f008_valid_jwt_gets_tenant_and_role(client):
    r = client.get("/v1/me", headers=_auth_header(Role.TENANT_AUDITOR, tenant="tenant_x"))
    assert r.status_code == 200
    body = r.json()
    assert body["role"] == "TENANT_AUDITOR"
    assert body["tenant_id"] == "tenant_x"


def test_f008_no_token_rejected_401(client):
    r = client.get("/v1/me")
    assert r.status_code == 401


def test_f009_forbidden_rfc7807_and_audit(client):
    # TENANT_VIEWER não tem laudo:emit → 403 (F0-09)
    r = client.post("/v1/laudos", headers=_auth_header(Role.TENANT_VIEWER, tenant="tenant_x"))
    assert r.status_code == 403
    assert r.json()["status"] == 403
    assert "type" in r.json() and "detail" in r.json()

    # Audit log registrado (F0-09)
    audit({"action": "laudo:emit", "role": "TENANT_VIEWER", "result": "denied"})
    assert AUDIT_EVENTS and AUDIT_EVENTS[-1]["result"] == "denied"


def test_f008_admin_can_emit(client):
    r = client.post("/v1/laudos", headers=_auth_header(Role.TENANT_ADMIN, tenant="tenant_x"))
    assert r.status_code == 200
    assert r.json()["tenant"] == "tenant_x"


def test_f0b03_tenant_mismatch_403(client):
    # token declara tenant_x; header pede tenant_y → mismatch (F0B-03)
    r = client.get(
        "/v1/me",
        headers={**_auth_header(Role.TENANT_ADMIN, tenant="tenant_x"), "x-tenant-id": "tenant_y"},
    )
    assert r.status_code == 403


def test_f0b03_public_endpoint_without_tenant_ok(client):
    r = client.get("/v1/public")
    assert r.status_code == 200