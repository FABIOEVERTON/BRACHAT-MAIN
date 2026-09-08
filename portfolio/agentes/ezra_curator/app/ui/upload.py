"""EZRA CURATOR — discreet document upload."""

from pathlib import Path

import streamlit as st

from app import config
from app.ingest import ingest

_ACCEPTED = ["pdf", "csv"]


def _save_files(files) -> list[Path]:
    """Persist uploaded files into the indexed data directory."""

    data_dir = Path(config.DATA_DIR)
    data_dir.mkdir(parents=True, exist_ok=True)

    saved = []

    for file in files:
        path = data_dir / file.name
        path.write_bytes(file.getvalue())
        saved.append(path)

    return saved


def render_upload() -> None:
    """Render a discreet upload popover for the top bar."""

    with st.popover("Documentos", use_container_width=True):
        st.caption(
            "Anexe arquivos ao acervo do agente. "
            "Eles serão indexados e passarão a responder perguntas."
        )

        files = st.file_uploader(
            "Arquivos (PDF ou CSV)",
            type=_ACCEPTED,
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if files and st.button(
            "Indexar arquivos",
            use_container_width=True,
            type="primary",
        ):
            try:
                _save_files(files)
                result = ingest(
                    data_dir=str(config.DATA_DIR),
                    update_only=True,
                )
                st.success(
                    f"{result['files']} arquivo(s) · "
                    f"{result['chunks']} chunk(s) indexados"
                )
            except Exception as exc:  # noqa: BLE001
                st.error(f"Falha na indexação: {exc}")
