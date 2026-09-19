"""Render de PDF de laudo — determinístico (PRD §3.3, F0-18)."""

import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from services.shared.laudo.models import LaudoRequest


def _payload_lines(payload: dict) -> list[tuple[str, str]]:
    return [(str(k), str(v)) for k, v in sorted(payload.items())]


def _strip_volatile_metadata(pdf: bytes) -> bytes:
    """Remove campos voláteis (/CreationDate, /ModDate, /ID) para que o hash do
    conteúdo seja determinístico (F0-18) mantendo o texto integral."""
    import re as _re

    out = pdf
    for pat in (rb"/CreationDate\s*\([^)]*\)", rb"/ModDate\s*\([^)]*\)", rb"/ID\s*\[[^\]]*\]"):
        out = _re.sub(pat, b"", out)
    return out


def render_pdf(request: LaudoRequest) -> bytes:
    """Gera PDF determinístico (mesmo input → mesmos bytes, F0-18)."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleSmall", parent=styles["Title"], fontSize=14)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11)

    story: list = [
        Paragraph(f"LAUDO EZRA — {request.laudo_type.value}", title),
        Spacer(1, 6),
        Paragraph(f"Produto: {request.product_id}", h2),
        Paragraph(f"Tenant: {request.tenant_id}", styles["Normal"]),
        Paragraph(f"Gerado por: {request.generated_by}", styles["Normal"]),
        Spacer(1, 8),
        Paragraph("Justificativa / payload", h2),
        Table(
            _payload_lines(request.payload),
            style=TableStyle(
                [
                    ("FONTNAME", (0, 0), (0, -1), "Courier-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Courier"),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            ),
        ),
        Spacer(1, 10),
    ]

    # F0-33 (PRD §3.6): signatário = operador white-label (name/title/register).
    # EZRA nunca é signatária; aparece apenas em rodapé como "sistema de suporte".
    if request.signatory:
        signer = request.signatory
        story.append(Paragraph("Assinatura", h2))
        story.append(Paragraph(f"Nome: {signer.get('name', '')}", styles["Normal"]))
        story.append(Paragraph(f"Cargo: {signer.get('title', '')}", styles["Normal"]))
        story.append(Paragraph(f"Registro: {signer.get('register', '')}", styles["Normal"]))
        story.append(Paragraph("Sistema tecnológico de suporte: EZRA (Plataforma EZRA)", styles["Italic"]))
    else:
        story.append(Paragraph("Assinatura: EZRA — Plataforma EZRA", h2))

    story.append(Paragraph("Referências normativas", h2))
    story.append(Paragraph("<br/>".join(f"• {r}" for r in sorted(request.normative_refs))))

    doc.build(story)
    return _strip_volatile_metadata(buf.getvalue())