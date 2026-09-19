"""Testes — White-label no LaudoEngine (E0-S08, PRD §3.6 regra crítica).

F0-33: laudo emitido sob white-label tem o OPERADOR como signatário
(name/title/register); EZRA apenas como sistema de suporte no rodapé;
hash+WORM permanecem da EZRA (nunca transferíveis).
"""

import io

import pytest
from pypdf import PdfReader

from services.shared.laudo.engine import LaudoEngine, LaudoRequest, LaudoType
from services.shared.laudo.worm_vault import WORMVault

SIGNATORY = {
    "name": "Maria Silva",
    "title": "Perita Contábil",
    "register": "CRC/SP 1SP234567",
}


@pytest.fixture
def worm() -> WORMVault:
    return WORMVault(endpoint_url="http://localhost:4566", bucket="ezra-worm")


def _wl_request() -> LaudoRequest:
    return LaudoRequest(
        tenant_id="bancaxyz",
        product_id="auditoria-contabil",
        laudo_type=LaudoType.PRESTACAO_CONTAS,
        payload={"exercicio": 2025, "demonstracao": "DRE"},
        generated_by="op-wl",
        normative_refs=["CRC Norma 2025"],
        signatory=SIGNATORY,
    )


def _pdf_text(pdf: bytes) -> str:
    return PdfReader(io.BytesIO(pdf)).pages[0].extract_text()


@pytest.mark.asyncio
async def test_f033_laudo_signed_by_operator_not_ezra(worm):
    engine = LaudoEngine("bancaxyz", worm=worm)
    result = await engine.emit(_wl_request())

    pdf = await engine.get_pdf(result.worm_key, worm)
    text = _pdf_text(pdf)

    # Signatário é o operador white-label
    assert "Maria Silva" in text
    assert "CRC" in text
    assert "1SP234567" in text
    # EZRA só como sistema de suporte (nunca signatária)
    assert "sistema tecnológico" in text.lower()
    # Cadeia WORM segue da EZRA (não transferível) — o hash existe no laudo
    assert len(result.sha256_hash) == 64
    assert len(result.chain_hash) == 64
    # PDF foi ao cofre WORM (key existe)
    assert await engine.get_pdf(result.worm_key, worm)