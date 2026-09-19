"""Testes — HashChain SHA-256 (E0-S06, PRD §3.4, ADR-004).

Cobre:
- F0-21: âncora — chain_hash = SHA256(content + tenant_id) no primeiro laudo
- F0-22: encadeamento — chain_hash = SHA256(content + previous_chain_hash)
- F0-23: sequência reprodutível (2º incorpora 1º)
- F0-24: verificação externa por perito (script verify reproduz)
"""

import hashlib

import pytest

from services.shared.laudo.hash_chain import HashChain


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def test_f021_anchor_when_no_previous():
    """Sem laudo anterior, previous = tenant_id (âncora)."""
    tenant_id = "tenant_abc"
    content = b"conteudo do laudo"
    content_hash = hashlib.sha256(content).hexdigest()

    hc = HashChain(tenant_id)
    result = hc.chain_serial(content_hash, previous=None)

    expected = sha256(f"{content_hash}{tenant_id}")
    assert result == expected


def test_f022_chaining_with_previous():
    tenant_id = "tenant_abc"
    content_hash = "a" * 64
    previous_chain = "b" * 64

    hc = HashChain(tenant_id)
    result = hc.chain_serial(content_hash, previous=previous_chain)

    assert result == sha256(f"{content_hash}{previous_chain}")


def test_f023_sequence_is_reproducible():
    """Dois laudos em sequência: chain2 incorpora chain1 (F0-23)."""
    tenant_id = "tenant_seq"
    content1 = b"laudo 1"
    content2 = b"laudo 2"
    h1 = hashlib.sha256(content1).hexdigest()
    h2 = hashlib.sha256(content2).hexdigest()

    hc = HashChain(tenant_id)
    chain1 = hc.chain_serial(h1, previous=None)  # âncora
    chain2 = hc.chain_serial(h2, previous=chain1)

    assert chain2 == sha256(f"{h2}{chain1}")
    # verificabilidade: perito recalcula do zero partindo de tenant_id
    recomputed = sha256(f"{h2}{sha256(f'{h1}{tenant_id}')}")
    assert chain2 == recomputed


def test_f024_external_verification(tmp_path):
    """Script externo recalcula a cadeia completa e bate (F0-24)."""
    tenant_id = "tenant_ext"
    entries = [(f"content{i}".encode(), f"chain{i}") for i in range(1, 4)]

    hc = HashChain(tenant_id)
    # simula: cada entrada = (content_bytes, chain_hash_real_persistido)
    stored: list[tuple[bytes, str]] = []
    prev = None
    for content, _ in entries:
        ch = hc.hash_content(content)
        chain = hc.chain_serial(ch, previous=prev)
        stored.append((content, chain))
        prev = chain

    # perito: recalcula independentemente
    recomputed_prev = None
    for content, stored_chain in stored:
        ch = hashlib.sha256(content).hexdigest()
        anchor = recomputed_prev if recomputed_prev else tenant_id
        expected = sha256(f"{ch}{anchor}")
        assert expected == stored_chain  # bate com o persistido
        recomputed_prev = stored_chain