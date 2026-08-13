"""EZRA CURATOR top bar."""

import streamlit as st

from app.ui.upload import render_upload


def render_header(status: dict) -> None:
    """Render the top bar with brand, status chip and document upload."""

    active = bool(
        status.get("llm_provider")
        and status.get("llm_provider") != "indisponível"
    )

    chip_cls = "ezra-chip-on" if active else "ezra-chip-degraded"
    chip_label = "● Ativo" if active else "● Degradado"

    brand_html = (
        '<div class="ezra-brand">'
        '  <div class="ezra-logo">◈</div>'
        '  <div>'
        '    <div class="ezra-brand-title">EZRA CURATOR</div>'
        '    <div class="ezra-brand-sub">Agente de IA · RAG sobre documentos</div>'
        '  </div>'
        "</div>"
    )

    chip_html = (
        f'<div class="ezra-chip {chip_cls}">{chip_label}</div>'
    )

    left, right = st.columns([6, 1], gap="medium")

    with left:
        st.markdown(brand_html, unsafe_allow_html=True)

    with right:
        st.markdown(chip_html, unsafe_allow_html=True)
        render_upload()
