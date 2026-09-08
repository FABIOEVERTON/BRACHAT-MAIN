"""EZRA CURATOR — chat-first interface."""

import html as html_lib

import streamlit as st

from app.logging import QueryLogger
from app.rag import RagResult, answer_question

PLACEHOLDER = (
    "Pergunte algo sobre os documentos... "
    "(ex.: Quais linguagens são usadas no back-end?)"
)

TYPING_HTML = (
    '<div class="ezra-typing">'
    "<span></span><span></span><span></span>"
    "</div>"
)

SUGGESTIONS = [
    "Quais documentos você tem?",
    "Resuma os documentos",
    "Qual linguagem é usada no back-end?",
    "Qual o produto mais vendido em dezembro/2015?",
]


def _hero() -> None:
    """Render the empty-state hero with suggestion chips."""

    st.markdown(
        """
        <div class="ezra-hero">
            <div class="ezra-hero-logo">◈</div>
            <h1>Pergunte sobre os documentos</h1>
            <p>
                Agente de IA que responde com base apenas nos documentos
                anexados — sempre citando as fontes e admitindo quando
                não sabe.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    row_one, row_two = st.columns(2, gap="medium")

    for column, label in zip(
        (row_one, row_one, row_two, row_two),
        SUGGESTIONS,
    ):
        with column:
            if st.button(label, use_container_width=True):
                st.session_state["_pending_prompt"] = label


def _source_snippet(source: dict) -> str:
    """Return a safe, short excerpt for a source."""
    snippet = str(source.get("excerpt") or "").strip()
    if snippet:
        return html_lib.escape(snippet[:180])
    return ""


def _render_sources(msg: dict) -> None:
    """Render the sources accordion for an assistant message."""

    sources = msg.get("sources") or []

    if not sources:
        return

    with st.expander(f"📄 Fontes ({len(sources)})"):
        for source in sources:
            name = html_lib.escape(
                str(source.get("source") or "?")
            )
            category = html_lib.escape(
                str(source.get("category") or "Geral")
            )
            snippet = _source_snippet(source)

            snippet_html = (
                f'<div class="ezra-src-snippet">{snippet}…</div>'
                if snippet
                else ""
            )

            st.markdown(
                (
                    f'<div class="ezra-source">'
                    f'  <div class="ezra-src-name">📄 {name} · {category}</div>'
                    f"  {snippet_html}"
                    f"</div>"
                ),
                unsafe_allow_html=True,
            )


def _render_feedback(index: int, msg: dict, logger: QueryLogger) -> None:
    """Render discreet thumbs feedback for an assistant message."""

    if msg.get("role") != "assistant":
        return

    if msg.get("feedback"):
        st.markdown(
            (
                '<div class="ezra-fb">'
                '<span class="ezra-fb-done">✓ Obrigado pelo feedback</span>'
                "</div>"
            ),
            unsafe_allow_html=True,
        )
        return

    up, down, spacer = st.columns([1, 1, 10], gap="small")

    if up.button("👍", key=f"fb-up-{index}", help="Resposta útil"):
        msg["feedback"] = "up"
        logger.feedback(msg.get("question", ""), "up")
        st.rerun()

    if down.button("👎", key=f"fb-down-{index}", help="Não ajudou"):
        msg["feedback"] = "down"
        logger.feedback(msg.get("question", ""), "down")
        st.rerun()

    with spacer:
        st.markdown("")


def _render_answer(msg: dict, logger: QueryLogger, index: int) -> None:
    """Render an assistant answer card with sources and feedback."""

    with st.chat_message("assistant"):
        st.markdown(msg.get("content", ""))
        _render_sources(msg)

    _render_feedback(index, msg, logger)


def _render_message(index: int, msg: dict, logger: QueryLogger) -> None:
    """Render a single chat message."""

    role = msg.get("role")

    if role == "user":
        with st.chat_message("user"):
            st.markdown(msg.get("content", ""))
    elif role == "assistant":
        _render_answer(msg, logger, index)


def _handle_prompt(prompt: str, logger: QueryLogger) -> None:
    """Process a user prompt and render the assistant answer."""

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        typing = st.empty()
        typing.markdown(TYPING_HTML, unsafe_allow_html=True)

        result: RagResult = answer_question(prompt, logger)

        typing.empty()
        st.markdown(result.answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result.answer,
            "sources": result.sources,
            "question": prompt,
            "feedback": None,
        }
    )


def render_chat(logger: QueryLogger) -> None:
    """Render the full chat experience (history + hero + input)."""

    pending = st.session_state.pop("_pending_prompt", None)

    if pending:
        _handle_prompt(pending, logger)

    if not st.session_state.messages:
        _hero()

    for index, msg in enumerate(st.session_state.messages):
        _render_message(index, msg, logger)

    prompt = st.chat_input(PLACEHOLDER)

    if prompt:
        _handle_prompt(prompt, logger)
