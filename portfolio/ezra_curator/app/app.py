"""EZRA CURATOR — Knowledge Synthesis Engine."""

import streamlit as st

from app.logging import QueryLogger
from app.rag import system_status

from app.ui.activity import render_activity
from app.ui.chat import render_chat
from app.ui.dashboard import render_dashboard
from app.ui.header import render_header
from app.ui.state import initialize_session_state
from app.ui.styles import load_styles
from app.ui.upload import render_upload


st.set_page_config(
    page_title="EZRA CURATOR",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    """Run the EZRA CURATOR Streamlit application."""
    initialize_session_state()
    load_styles()

    logger = QueryLogger()
    status = system_status()

    render_header(status)
    render_upload()
    render_activity()
    render_dashboard()
    render_chat(logger)

    st.markdown(
        """
        <div class="footer">
            EZRA CURATOR · Knowledge Synthesis Engine · Oracle ONE Challenge
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()