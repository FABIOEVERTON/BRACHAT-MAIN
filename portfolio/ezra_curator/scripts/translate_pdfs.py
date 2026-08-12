#!/usr/bin/env python3
"""Traduz os PDFs originais (ES) da Santos Pegasus para PT-BR.

Lê de data/original/*.pdf, traduz página a página via googletrans e
gera data/*.pdf em PT-BR preservando a estrutura básica do documento.
"""
import html
import os
import re
import sys
import time
from pathlib import Path

from googletrans import Translator
from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

SRC_DIR = Path(os.getenv("DATA_DIR", "./data")) / "original"
OUT_DIR = Path(os.getenv("DATA_DIR", "./data"))

MAX_CHARS = 1500
MAX_RETRIES = 4
SLEEP = 1.2


def sanitize(text: str) -> str:
    text = re.sub(r"[^\x00-\xff]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def translate_chunk(tr: Translator, text: str) -> str:
    for attempt in range(MAX_RETRIES):
        try:
            r = tr.translate(text, src="es", dest="pt")
            if r and r.text:
                return r.text
        except Exception:
            pass
        time.sleep(SLEEP * (attempt + 1))
    return text


def translate_page(tr: Translator, text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if len(text) <= MAX_CHARS:
        return translate_chunk(tr, text)
    parts = []
    for i in range(0, len(text), MAX_CHARS):
        parts.append(translate_chunk(tr, text[i : i + MAX_CHARS]))
    return " ".join(parts)


def build_pdf(out_path: Path, pages: list[str]) -> None:
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "BodyPT", parent=styles["BodyText"], fontSize=9, leading=12,
        alignment=4,
    )
    flow = []
    for i, page in enumerate(pages, 1):
        text = sanitize(page)
        if text:
            for para in text.split("\n"):
                para = para.strip()
                if para:
                    flow.append(Paragraph(html.escape(para), body))
        if i < len(pages):
            flow.append(Spacer(1, 8))
    doc.build(flow)


def main() -> None:
    files = sorted(SRC_DIR.glob("*.pdf"))
    if not files:
        print("Nenhum PDF em", SRC_DIR)
        sys.exit(1)
    tr = Translator()
    OUT_DIR.mkdir(exist_ok=True)
    for pdf in files:
        out = OUT_DIR / f"{pdf.stem}.pdf"
        print(f"[traduzindo] {pdf.name} -> {out.name}", flush=True)
        reader = PdfReader(str(pdf))
        pages = []
        for idx, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            translated = translate_page(tr, text)
            pages.append(translated)
            print(f"  pag {idx}/{len(reader.pages)} ok", flush=True)
        build_pdf(out, pages)
        print(f"[ok] {out.name} ({len(pages)} pag)", flush=True)


if __name__ == "__main__":
    main()
