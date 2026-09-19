"""Modelos de domínio do laudo — PRD §3.3 EXATO (sem dependências do engine).

LaudoType (10 tipos, RAMO 1/2), LaudoRequest, LaudoResult.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LaudoType(Enum):
    # Ramo 1
    INVENTARIO_ALGORITIMICO = "LAI"
    CONFORMIDADE_ALGORITIMICA = "LCA"
    TRANSICAO_MODELO = "LTM"
    INTEGRIDADE_RUNTIME = "LIR"
    # Ramo 2
    ELEGIBILIDADE_ORCAMENTARIA = "LEO"
    REGULARIDADE_FISCAL = "LRF"
    JUSTIFICATIVA_PRECOS = "LJP"
    CONFORMIDADE_OBJETO = "LCO"
    SANEAMENTO_DILIGENCIAS = "LSD"
    PRESTACAO_CONTAS = "LPC"


@dataclass
class LaudoRequest:
    tenant_id: str
    product_id: str
    laudo_type: LaudoType
    payload: dict
    generated_by: str
    normative_refs: list[str]
    # White-label (F0-33, PRD §3.6): signatário é o OPERADOR, não a EZRA.
    signatory: dict | None = None  # {name, title, register}


@dataclass
class LaudoResult:
    laudo_id: str
    laudo_number: str
    sha256_hash: str
    chain_hash: str
    worm_key: str
    pdf_url: str
    emitted_at: datetime