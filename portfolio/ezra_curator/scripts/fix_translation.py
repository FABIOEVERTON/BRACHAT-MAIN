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
    for a, b in FIXES:
        text = text.replace(a, b)
    return text


def sanitize(text: str) -> str:
    text = re.sub(r"[^\x00-\xff]", " ", text)
    return text.strip()


def rebuild(src: Path, out: Path) -> None:
    reader = PdfReader(str(src))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = apply_fixes(text)
        pages.append(text)

    doc = SimpleDocTemplate(
        str(out), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    )
    body = ParagraphStyle("Body", parent=getSampleStyleSheet()["BodyText"], fontSize=9, leading=12, alignment=4)
    flow = []
    for i, page in enumerate(pages, 1):
        t = sanitize(page)
        if t:
            for para in t.split("\n"):
                para = para.strip()
                if para:
                    flow.append(Paragraph(html.escape(para), body))
        if i < len(pages):
            flow.append(Spacer(1, 8))
    doc.build(flow)
    print(f"[ok] {out.name}")


def main() -> None:
    data = Path(__file__).resolve().parent.parent / "data"
    tmp = data / "_tmp"
    tmp.mkdir(exist_ok=True)
    for pdf in sorted(data.glob("*.pdf")):
        rebuild(pdf, tmp / pdf.name)
    for pdf in tmp.glob("*.pdf"):
        pdf.replace(data / pdf.name)
    tmp.rmdir()


if __name__ == "__main__":
    main()
