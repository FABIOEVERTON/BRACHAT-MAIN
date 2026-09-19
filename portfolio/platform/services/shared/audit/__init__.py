"""Audit log compartilhado (PRD §3.1)."""

from services.shared.audit.logger import (
    AuditEvent,
    audit_login_failed,
    audit_login_success,
    audit_mfa_required,
    audit_permission_denied,
    log_event,
)

__all__ = [
    "AuditEvent",
    "audit_login_failed",
    "audit_login_success",
    "audit_mfa_required",
    "audit_permission_denied",
    "log_event",
]