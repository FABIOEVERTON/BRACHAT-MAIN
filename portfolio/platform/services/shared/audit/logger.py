"""Audit log estruturado de auth (PRD §3.1 req: "Audit log de cada autenticação").

FASE 0: registro estruturado + append em arquivo (dev) / stdout (container).
FASE 1: persistência no WORM vault (E0-S07) — assinatura e imutabilidade.
Eventos: login.success, login.failed, mfa.required, mfa.verified, token.refresh,
permission.denied, logout.
"""

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AuditEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ts: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    action: str = ""
    user: str = ""
    role: str = ""
    tenant_id: str | None = None
    result: str = "success"  # success | denied | failed
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _sink() -> str | None:
    """Caminho de sink: env EZRA_AUDIT_LOG, senão none (stdout)."""
    return os.environ.get("EZRA_AUDIT_LOG")


def log_event(action: str, *, user: str = "", role: str = "", tenant_id: str | None = None,
              result: str = "success", detail: str | None = None) -> AuditEvent:
    event = AuditEvent(action=action, user=user, role=role, tenant_id=tenant_id,
                       result=result, detail=detail)
    line = json.dumps(event.to_dict(), ensure_ascii=False)
    sink = _sink()
    if sink:
        with open(sink, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    else:
        print(line)
    return event


# Conveniências de domínio (F0-09: evento registrado quando permission denied)
def audit_login_success(user: str, role: str, tenant_id: str | None) -> AuditEvent:
    return log_event("login.success", user=user, role=role, tenant_id=tenant_id)


def audit_login_failed(user: str, detail: str) -> AuditEvent:
    return log_event("login.failed", user=user, detail=detail, result="failed")


def audit_mfa_required(user: str, role: str, tenant_id: str | None) -> AuditEvent:
    return log_event("mfa.required", user=user, role=role, tenant_id=tenant_id, result="denied")


def audit_permission_denied(user: str, role: str, tenant_id: str | None, permission: str) -> AuditEvent:
    return log_event(
        "permission.denied", user=user, role=role, tenant_id=tenant_id,
        result="denied", detail=f"sem permissão {permission}",
    )