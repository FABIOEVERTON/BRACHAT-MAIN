"""Repositório de laudos — numbering sequencial por tenant (PRD §3.3, F0-16).

- laudo_number: ex "LAI-2026-0042" — sequencial por tenant NUNCA reinicia
  (Protected behavior). Padrão: {TIPO}-{ano}-{sequencial:04d}.
- last_chain_hash: último hash da cadeia do tenant (âncora na E0-S06).
- insert: persiste registro; chamado DENTRO do tenant_lock (R-2).

FASE 0: store in-process (dict) — dev/demo sem banco. A camada SQLAlchemy
(schema_per_tenant, S04) substitui na FASE 1 sem mudar o contrato.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from services.shared.laudo.engine import LaudoRequest


@dataclass
class LaudoRecord:
    laudo_id: str
    tenant_id: str
    product_id: str
    laudo_type: str
    laudo_number: str
    sha256_hash: str
    chain_hash: str
    worm_key: str
    emitted_at: datetime


class LaudoRepository:
    def __init__(self) -> None:
        self._records: dict[str, LaudoRecord] = {}
        self._chain: dict[str, str] = {}  # tenant_id -> último chain_hash
        self._seq: dict[str, int] = {}  # tenant_id -> contador

    async def last_chain_hash(self, tenant_id: str) -> str | None:
        return self._chain.get(tenant_id)

    async def count(self) -> int:
        return len(self._records)

    async def insert(self, *, tenant_id: str, request: LaudoRequest,
                     content_hash: str, chain_hash: str, worm_key: str) -> LaudoRecord:
        seq = self._seq.get(tenant_id, 0) + 1
        self._seq[tenant_id] = seq
        number = f"{request.laudo_type.value}-{datetime.now(timezone.utc).year}-{seq:04d}"

        record = LaudoRecord(
            laudo_id=str(uuid4()),
            tenant_id=tenant_id,
            product_id=request.product_id,
            laudo_type=request.laudo_type.value,
            laudo_number=number,
            sha256_hash=content_hash,
            chain_hash=chain_hash,
            worm_key=worm_key,
            emitted_at=datetime.now(timezone.utc),
        )
        self._records[record.laudo_id] = record
        self._chain[tenant_id] = chain_hash
        return record

    async def get(self, laudo_id: str) -> LaudoRecord | None:
        return self._records.get(laudo_id)

    async def list_by_tenant(self, tenant_id: str) -> list[LaudoRecord]:
        return [r for r in self._records.values() if r.tenant_id == tenant_id]