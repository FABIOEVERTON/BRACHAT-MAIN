"""Streamlit session-state initialization."""

from collections import Counter

import streamlit as st


def initialize_session_state() -> None:
    """Initialize all EZRA session-state values."""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_latency" not in st.session_state:
        st.session_state.last_latency = None

    if "stats" not in st.session_state:
        st.session_state.stats = {
            "total_queries": 0,
            "total_latency": 0.0,
            "fallback_count": 0,
            "doc_hits": Counter(),
            "doc_chunks_used": Counter(),
        }

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []