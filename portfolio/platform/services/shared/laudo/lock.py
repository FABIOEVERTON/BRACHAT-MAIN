"""Lock por tenant — serialização da cadeia (risk profile R-2, F0-22/23).

Sem lock: dois emits concorrentes do MESMO tenant podem ler o mesmo previous e
gravar dois chain_hash iguais — quebra a cadeia probatória silenciosamente.
tenant_lock serializa leitura+escrita do chain_hash por tenant (in-process dev;
FASE 1+: Redis lock distribuído por tenant_id — mesmo contrato).
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

_lock_registry: dict[str, asyncio.Lock] = {}


@asynccontextmanager
async def tenant_lock(tenant_id: str) -> AsyncIterator[None]:
    lock = _lock_registry.setdefault(tenant_id, asyncio.Lock())
    async with lock:
        yield