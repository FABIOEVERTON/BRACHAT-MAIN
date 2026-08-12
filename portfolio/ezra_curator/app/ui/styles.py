"""EZRA CURATOR visual system."""

import streamlit as st


CSS = """
<style>

... YOUR EXISTING  CSS ...

</style>
"""


def load_styles() -> None:
    """Load EZRA CURATOR global styles."""
    st.markdown(CSS, unsafe_allow_html=True)