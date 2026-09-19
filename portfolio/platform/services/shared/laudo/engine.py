"""Laudo Engine — componente mais crítico (PRD §3.3).

Ordenação de emit: PDF render → hash_content → chain (serializado por tenant)
→ WORM store → persist (transação atômica) → LaudoResult.
"""

from datetime import datetime

from services.shared.laudo.hash_chain import HashChain
from services.shared.laudo.lock import tenant_lock
from services.shared.laudo.models import LaudoRequest, LaudoResult, LaudoType  # noqa: F401
from services.shared.laudo.pdf_generator import render_pdf
from services.shared.laudo.repository import LaudoRepository
from services.shared.laudo.worm_vault import WORMVault

__all__ = ["LaudoEngine", "LaudoRequest", "LaudoResult", "LaudoType"]


class LaudoEngine:
    """O motor de laudos. Serialização da cadeia por tenant (R-2)."""

    def __init__(self, tenant_id: str, worm: WORMVault | None = None):
        self.tenant_id = tenant_id
        self.hash_chain = HashChain(tenant_id)
        self.worm_vault = worm or WORMVault()
        self.repo = LaudoRepository()

    async def emit(self, request: LaudoRequest) -> LaudoResult:
        # 1. PDF com payload + refs (F0-17) — determinístico (F0-18)
        pdf_bytes = render_pdf(request)

        # 2. hash do conteúdo
        content_hash = self.hash_chain.hash_content(pdf_bytes)

        # 3. encadear SÓ com lock por tenant (R-2: evita corrida na cadeia)
        async with tenant_lock(self.tenant_id):
            previous = await self.repo.last_chain_hash(self.tenant_id)
            chain_hash = self.hash_chain.chain_serial(content_hash, previous)

            # 4. gravar no cofre WORM — F0-19: falha aqui NÃO persiste
            worm_key = await self.worm_vault.store(
                tenant_id=self.tenant_id,
                laudo_type=request.laudo_type.value,
                content=pdf_bytes,
                metadata={
                    "sha256": content_hash,
                    "chain_hash": chain_hash,
                },
            )

            # 5. persistir com número sequencial por tenant (mesmo lock)
            record = await self.repo.insert(
                tenant_id=self.tenant_id,
                request=request,
                content_hash=content_hash,
                chain_hash=chain_hash,
                worm_key=worm_key,
            )

        return LaudoResult(
            laudo_id=record.laudo_id,
            laudo_number=record.laudo_number,
            sha256_hash=content_hash,
            chain_hash=chain_hash,
            worm_key=worm_key,
            pdf_url=await self.worm_vault.get_signed_url(worm_key),
            emitted_at=record.emitted_at,
        )

    async def get_pdf(self, worm_key: str, worm: WORMVault | None = None) -> bytes:
        vault = worm or self.worm_vault
        return await vault.fetch(worm_key)