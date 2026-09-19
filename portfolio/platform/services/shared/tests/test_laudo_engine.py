"""Testes — LaudoEngine (E0-S05, PRD §3.3).

Cobre:
- F0-16: emit completo retorna LaudoResult com todos os campos
- F0-17: PDF contém payload + normative_refs
- F0-18: determinismo — mesmo payload → hashes de conteúdo idênticos, ids distintos
- F0-19: atomicidade — falha no WORM → nenhum registro parcial
- F0-20: perf smoke < 60s (latência emissão simples)
"""

import asyncio
import io
import time

import pytest
from pypdf import PdfReader

from services.shared.laudo.engine import LaudoEngine, LaudoRequest, LaudoType
from services.shared.laudo.worm_vault import WORMVault


@pytest.fixture
def worm() -> WORMVault:
    return WORMVault(endpoint_url="http://localhost:4566", bucket="ezra-worm")


def _req(tenant_id: str, laudo_type: LaudoType = LaudoType.INVENTARIO_ALGORITIMICO) -> LaudoRequest:
    return LaudoRequest(
        tenant_id=tenant_id,
        product_id="sentinel",
        laudo_type=laudo_type,
        payload={"modelo": "gpt-4o", "versao": "1.2.3", "regra": "LAS_001"},
        generated_by="user-1",
        normative_refs=["LGPD Art. 37", "ANPD Res. 2/2022"],
    )


@pytest.mark.asyncio
async def test_f016_emit_returns_complete_result(worm):
    engine = LaudoEngine("t-engine", worm=worm)
    result = await engine.emit(_req("t-engine"))

    assert result.laudo_id
    assert result.laudo_number.startswith("LAI-")  # ex: LAI-2026-0001
    assert result.laudo_number.endswith("-0001")
    assert len(result.sha256_hash) == 64
    assert len(result.chain_hash) == 64
    assert result.worm_key
    assert result.pdf_url
    assert result.emitted_at


@pytest.mark.asyncio
async def test_f017_pdf_contains_payload_and_refs(worm):
    engine = LaudoEngine("t-pdf", worm=worm)
    result = await engine.emit(_req("t-pdf"))

    pdf = await engine.get_pdf(result.worm_key, worm)
    assert pdf[:4] in (b"%PDF", b"%\x93\x8c\x8d")  # assinatura PDF
    text = PdfReader(io.BytesIO(pdf)).pages[0].extract_text()
    assert "gpt-4o" in text
    assert "LGPD Art. 37" in text
    assert "LAS_001" in text


@pytest.mark.asyncio
async def test_f018_same_payload_deterministic_content_distinct_ids(worm):
    engine = LaudoEngine("t-det", worm=worm)
    r1 = await engine.emit(_req("t-det"))
    r2 = await engine.emit(_req("t-det"))

    # ids/números distintos (F0-18)
    assert r1.laudo_id != r2.laudo_id
    assert r1.laudo_number != r2.laudo_number
    assert r1.laudo_number.endswith("-0001")
    assert r2.laudo_number.endswith("-0002")

    # conteúdo idêntico (determinismo do PDF render)
    assert r1.sha256_hash == r2.sha256_hash

    # cadeia: chain2 incorpora chain1 (sequência) — base F0-23
    assert r1.chain_hash != r2.chain_hash


class FailingWorm(WORMVault):
    """WORM que falha no store — testa atomicidade (F0-19)."""

    async def store(self, **kwargs) -> str:  # type: ignore[override]
        raise RuntimeError("vault indisponível")


@pytest.mark.asyncio
async def test_f019_failure_produces_no_partial_state():
    engine = LaudoEngine("t-atom", worm=FailingWorm())
    from services.shared.laudo.repository import LaudoRepository

    repo = LaudoRepository()
    before = await repo.count()
    with pytest.raises(RuntimeError):
        await engine.emit(_req("t-atom"))
    after = await repo.count()
    assert after == before  # nenhum registro parcial


@pytest.mark.asyncio
async def test_f020_emit_latency_under_60s(worm):
    engine = LaudoEngine("t-perf", worm=worm)
    _ = await engine.emit(_req("t-perf"))  # warmup
    start = time.perf_counter()
    await engine.emit(_req("t-perf"))
    elapsed = time.perf_counter() - start
    assert elapsed < 60.0
    print(f"  emit latency: {elapsed:.2f}s (NFR < 60s)")