#!/usr/bin/env python3

"""Corrige artefatos de tradução nos PDFs PT-BR (nomes próprios)."""

import html
import re
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


FIXES = [
    ("Holy Pegasus Soluciones", "Santos Pegasus Soluciones"),
    ("Soluções Holy Pegasus", "Santos Pegasus Soluciones"),
    ("Holy Pegasus", "Santo Pegasus"),
    ("Holy", "Santo"),
]


def apply_fixes(text: str) -> str:
    """Aplica as correções de tradução definidas em FIXES."""
    for source, replacement in FIXES:
        text = text.replace(source, replacement)

    return text


def sanitize(text: str) -> str:
    """Remove caracteres que não são suportados pela fonte padrão."""
    text = re.sub(r"[^\x00-\xff]", " ", text)
    return text.strip()


def rebuild(src: Path, out: Path) -> None:
    """Extrai o texto do PDF, corrige os artefatos e recria o arquivo."""
    reader = PdfReader(str(src))
    pages: list[str] = []

    for page in reader.pages:
        text = page.extract_text() or ""
        text = apply_fixes(text)
        pages.append(text)

    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        alignment=4,
    )

    doc = SimpleDocTemplate(
        str(out),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    flow = []

    for page_number, page_text in enumerate(pages, 1):
        text = sanitize(page_text)

        if text:
            for paragraph_text in text.split("\n"):
                paragraph_text = paragraph_text.strip()

                if paragraph_text:
                    flow.append(
                        Paragraph(
                            html.escape(paragraph_text),
                            body,
                        )
                    )

        if page_number < len(pages):
            flow.append(Spacer(1, 8))

    doc.build(flow)

    print(f"[ok] {out.name}")


def main() -> None:
    """Processa todos os PDFs diretamente dentro de data/."""
    data = Path(__file__).resolve().parent.parent / "data"
    tmp = data / "_tmp"

    tmp.mkdir(exist_ok=True)

    try:
        pdfs = sorted(data.glob("*.pdf"))

        for pdf in pdfs:
            rebuild(
                pdf,
                tmp / pdf.name,
            )

        for pdf in sorted(tmp.glob("*.pdf")):
            pdf.replace(data / pdf.name)

    finally:
        if tmp.exists():
            tmp.rmdir()


if __name__ == "__main__":
    main()