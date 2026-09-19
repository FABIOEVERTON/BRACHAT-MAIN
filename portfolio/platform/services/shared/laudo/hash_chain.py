"""Cadeia de custódia SHA-256 (PRD §3.4, ADR-004).

chain_hash = SHA256(content_hash + previous_chain_hash); âncora = tenant_id.

Protected behavior (R-2 do risk profile): leitura do último hash por tenant DEVE
ser serializada — o chamador deve obter `previous` com lock (SELECT ... FOR UPDATE
ou transação única por tenant) para evitar corrida que quebraria a cadeia
silenciosamente. chain_serial é pura (testável); chain_with_db faz o round-trip.
"""

import hashlib


class HashChain:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    def hash_content(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def chain_serial(self, content_hash: str, previous: str | None) -> str:
        """Puro: chain_hash = SHA256(content_hash + previous).

        previous=None → âncora = tenant_id (primeiro laudo, F0-21).
        """
        anchor = previous if previous else self.tenant_id
        combined = f"{content_hash}{anchor}".encode()
        return hashlib.sha256(combined).hexdigest()

    # NOTE: o round-trip com banco (SELECT último chain_hash + lock por tenant)
    # é implementado na E0-S05 (repositório de laudos) com transação por tenant,
    # garantindo a serialização exigida pelo risk profile R-2.