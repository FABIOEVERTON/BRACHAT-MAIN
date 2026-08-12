#!/usr/bin/env python3

"""Traduz os PDFs originais (ES) da Santos Pegasus para PT-BR.

Lê de data/original/*.pdf, traduz página a página via googletrans
e gera data/*.pdf em PT-BR preservando a estrutura básica do documento.
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


SRC_DIR = Path(
    os.getenv("DATA_DIR", "./data")
) / "original"

OUT_DIR = Path(
    os.getenv("DATA_DIR", "./data")
)

MAX_CHARS = 1500
MAX_RETRIES = 4
SLEEP = 1.2


def sanitize(text: str) -> str:
    """Limpa caracteres e espaços problemáticos."""
    text = re.sub(r"[^\x00-\xff]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def translate_chunk(
    translator: Translator,
    text: str,
) -> str:
    """Traduz um bloco de texto com tentativas de retry."""
    for attempt in range(MAX_RETRIES):
        try:
            result = translator.translate(
                text,
                src="es",
                dest="pt",
            )

            if result and result.text:
                return result.text

        except Exception:
            pass

        time.sleep(
            SLEEP * (attempt + 1)
        )

    # Preserva o texto original caso a tradução falhe.
    return text


def translate_page(
    translator: Translator,
    text: str,
) -> str:
    """Traduz uma página, dividindo textos grandes em blocos."""
    text = text.strip()

    if not text:
        return ""

    if len(text) <= MAX_CHARS:
        return translate_chunk(
            translator,
            text,
        )

    parts = []

    for start in range(
        0,
        len(text),
        MAX_CHARS,
    ):
        chunk = text[
            start : start + MAX_CHARS
        ]

        parts.append(
            translate_chunk(
                translator,
                chunk,
            )
        )

    return " ".join(parts)


def build_pdf(
    out_path: Path,
    pages: list[str],
) -> None:
    """Reconstrói um PDF básico a partir das páginas traduzidas."""
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()

    body = ParagraphStyle(
        "BodyPT",
        parent=styles["BodyText"],
        fontSize=9,
        leading=12,
        alignment=4,
    )

    flow = []

    for page_number, page in enumerate(
        pages,
        1,
    ):
        text = sanitize(page)

        if text:
            for paragraph_text in text.split("\n"):
                paragraph_text = paragraph_text.strip()

                if paragraph_text:
                    flow.append(
                        Paragraph(
                            html.escape(
                                paragraph_text
                            ),
                            body,
                        )
                    )

        if page_number < len(pages):
            flow.append(
                Spacer(1, 8)
            )

    doc.build(flow)


def main() -> None:
    """Traduz todos os PDFs encontrados em data/original/."""
    files = sorted(
        SRC_DIR.glob("*.pdf")
    )

    if not files:
        print(
            "Nenhum PDF em",
            SRC_DIR,
        )
        sys.exit(1)

    translator = Translator()

    OUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    for pdf in files:
        out = OUT_DIR / f"{pdf.stem}.pdf"

        print(
            f"[traduzindo] {pdf.name} "
            f"-> {out.name}",
            flush=True,
        )

        reader = PdfReader(
            str(pdf)
        )

        pages: list[str] = []

        for page_number, page in enumerate(
            reader.pages,
            1,
        ):
            text = page.extract_text() or ""

            translated = translate_page(
                translator,
                text,
            )

            pages.append(translated)

            print(
                f"  pag {page_number}/"
                f"{len(reader.pages)} ok",
                flush=True,
            )

        build_pdf(
            out,
            pages,
        )

        print(
            f"[ok] {out.name} "
            f"({len(pages)} pag)",
            flush=True,
        )


if __name__ == "__main__":
    main()