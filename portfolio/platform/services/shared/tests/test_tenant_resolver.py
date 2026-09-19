"""Testes unit — tenant resolver TS (PRD §8.2) espelhado em Python.

Valida a regra de subdomínio (F0-07 claims tenant): ezra.com.br → ezra/gov_ai;
cliente.ezra.com.br → cliente; customDomain → gov_municipal.
"""

import pytest

from services.shared.tenant.resolver import resolve_tenant_sync


def test_ezra_root():
    t = resolve_tenant_sync("ezra.com.br")
    assert t["x-tenant-id"] == "ezra"
    assert t["x-tenant-branch"] == "gov_ai"


def test_ezra_subdomain():
    t = resolve_tenant_sync("prefeitura.ezra.com.br")
    assert t["x-tenant-id"] == "prefeitura"
    assert t["x-tenant-branch"] == "gov_ai"


def test_www_is_normalized():
    t = resolve_tenant_sync("www.ezra.com.br")
    assert t["x-tenant-id"] == "ezra"


def test_custom_domain_whitelabel():
    t = resolve_tenant_sync("auditoria.bancaxyz.com.br")
    assert t["x-tenant-branch"] == "gov_municipal"
    assert t["x-tenant-id"] == "auditoria"