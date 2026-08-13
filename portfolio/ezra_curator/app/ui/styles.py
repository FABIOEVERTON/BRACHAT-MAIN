"""EZRA CURATOR visual system — dark premium chat-first."""

import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ============================================================
   BASE
   ============================================================ */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background: #121218;
}

div[data-testid="stAppViewContainer"] > .main {
    background: #121218;
    padding-top: 0.5rem;
}

/* ============================================================
   REMOVE STREAMLIT CHROME
   ============================================================ */
#MainMenu,
header[data-testid="stHeader"],
footer[data-testid="stFooter"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}

div[data-testid="stAppViewContainer"] {
    background: #121218;
}

/* ============================================================
   TOP BAR
   ============================================================ */
.ezra-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0;
}

.ezra-logo {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35);
}

.ezra-brand-title {
    color: #f5f3ff;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.2px;
    line-height: 1.2;
}

.ezra-brand-sub {
    color: #8b8ba3;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.3px;
}

.ezra-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 999px;
    white-space: nowrap;
}

.ezra-chip-on {
    color: #7ce7a8;
    background: rgba(46, 160, 90, 0.12);
    border: 1px solid rgba(46, 160, 90, 0.35);
}

.ezra-chip-degraded {
    color: #ffd479;
    background: rgba(240, 170, 40, 0.10);
    border: 1px solid rgba(240, 170, 40, 0.35);
}

/* ============================================================
   HERO (EMPTY STATE)
   ============================================================ */
.ezra-hero {
    text-align: center;
    margin-top: 16vh;
    padding: 0 16px;
}

.ezra-hero-logo {
    width: 76px;
    height: 76px;
    margin: 0 auto 22px;
    border-radius: 22px;
    background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%);
    color: #ffffff;
    font-size: 42px;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 12px 34px rgba(124, 58, 237, 0.4);
}

.ezra-hero h1 {
    color: #f5f3ff;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.3px;
    margin: 0 0 10px;
}

.ezra-hero p {
    color: #9a9ab0;
    font-size: 15px;
    max-width: 560px;
    margin: 0 auto 30px;
    line-height: 1.6;
}

/* ============================================================
   SUGGESTION CHIPS
   ============================================================ */
div[data-testid="stButton"] > button {
    width: 100%;
    border: 1px solid #33333f;
    background: #1c1c22;
    color: #d9d9e8;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 500;
    padding: 10px 14px;
    transition: all 0.15s ease;
}

div[data-testid="stButton"] > button:hover {
    border-color: #a78bfa;
    background: #24242c;
    color: #f5f3ff;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.12);
}

div[data-testid="stButton"] > button:focus:not(:active) {
    border-color: #a78bfa;
    color: #f5f3ff;
}

/* ============================================================
   CHAT MESSAGES
   ============================================================ */
div[data-testid="stChatMessage"] {
    max-width: 860px;
    margin-left: auto;
    margin-right: auto;
    padding: 6px 0;
}

div[data-testid="stChatMessageContent"] {
    font-size: 15px;
    line-height: 1.7;
    color: #e8e8f2;
    border-radius: 14px;
    padding: 14px 18px;
    max-width: 100%;
}

div[data-testid="stChatMessageContent"] p {
    margin: 0 0 8px;
}

div[data-testid="stChatMessageContent"] p:last-child {
    margin-bottom: 0;
}

div[data-testid="stChatMessageContent"] code {
    background: #24242c;
    color: #a78bfa;
    border-radius: 5px;
    padding: 2px 5px;
    font-size: 13px;
}

div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"])
    div[data-testid="stChatMessageContent"] {
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.22), rgba(167, 139, 250, 0.14));
    border: 1px solid rgba(167, 139, 250, 0.28);
    margin-left: 12%;
}

div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"])
    div[data-testid="stChatMessageContent"] {
    background: #1c1c22;
    border: 1px solid #2b2b36;
    margin-right: 6%;
}

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    color: #ffffff !important;
}

[data-testid="chatAvatarIcon-user"] {
    background: #2b2b36;
    color: #a78bfa !important;
}

/* ============================================================
   SOURCES ACCORDION
   ============================================================ */
[data-testid="stExpander"] {
    max-width: 860px;
    margin: 6px auto 0;
    border: 1px solid #2b2b36 !important;
    background: #181820 !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    font-size: 13px;
    font-weight: 600;
    color: #a78bfa;
    padding: 4px 10px;
    transition: color 0.15s ease;
}

[data-testid="stExpander"] summary:hover {
    color: #c4b5fd;
}

[data-testid="stExpander"] .ezra-source {
    font-size: 13px;
    color: #c8c8da;
    padding: 6px 8px;
    border-radius: 8px;
    transition: background 0.15s ease;
}

[data-testid="stExpander"] .ezra-source:hover {
    background: #24242c;
}

[data-testid="stExpander"] .ezra-source .ezra-src-name {
    color: #f5f3ff;
    font-weight: 600;
}

[data-testid="stExpander"] .ezra-source .ezra-src-snippet {
    color: #8b8ba3;
    font-size: 12px;
    margin-top: 2px;
    line-height: 1.5;
}

/* ============================================================
   FEEDBACK BUTTONS
   ============================================================ */
.ezra-fb {
    display: flex;
    gap: 4px;
    padding: 2px 4px;
}

.ezra-fb button {
    background: transparent;
    border: none;
    color: #6f6f88;
    font-size: 13px;
    cursor: pointer;
    padding: 2px 7px;
    border-radius: 6px;
    transition: all 0.15s ease;
}

.ezra-fb button:hover {
    color: #a78bfa;
    background: rgba(167, 139, 250, 0.12);
}

.ezra-fb .ezra-fb-done {
    color: #7ce7a8;
    font-size: 12px;
    padding: 2px 7px;
}

/* ============================================================
   TYPING INDICATOR
   ============================================================ */
.ezra-typing {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 2px;
}

.ezra-typing span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #a78bfa;
    animation: ezra-blink 1.3s infinite ease-in-out;
}

.ezra-typing span:nth-child(2) { animation-delay: 0.18s; }
.ezra-typing span:nth-child(3) { animation-delay: 0.36s; }

@keyframes ezra-blink {
    0%, 80%, 100% { opacity: 0.25; transform: translateY(0); }
    40% { opacity: 1; transform: translateY(-4px); }
}

/* ============================================================
   CHAT INPUT
   ============================================================ */
div[data-testid="stChatInput"] {
    max-width: 860px;
    margin: 0 auto 10px;
}

div[data-testid="stChatInput"] textarea {
    background: #1c1c22 !important;
    color: #e8e8f2 !important;
    border: 1px solid #33333f !important;
    border-radius: 16px !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    transition: border 0.15s ease, box-shadow 0.15s ease;
}

div[data-testid="stChatInput"] textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}

div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #a78bfa, #7c3aed) !important;
    border-radius: 12px !important;
}

/* ============================================================
   FOOTER
   ============================================================ */
.ezra-footer {
    text-align: center;
    color: #5f5f78;
    font-size: 11.5px;
    padding: 18px 0 22px;
}

.ezra-footer .ezra-dot {
    color: #7ce7a8;
}

/* ============================================================
   MISC
   ============================================================ */
[data-testid="stPopoverButton"] {
    border-radius: 999px !important;
    border: 1px solid #33333f !important;
    background: #1c1c22 !important;
    color: #d9d9e8 !important;
    font-size: 13px !important;
    padding: 7px 14px !important;
}

[data-testid="stPopoverButton"]:hover {
    border-color: #a78bfa !important;
    color: #f5f3ff !important;
}

::-webkit-scrollbar {
    width: 9px;
    height: 9px;
}

::-webkit-scrollbar-track {
    background: #121218;
}

::-webkit-scrollbar-thumb {
    background: #33333f;
    border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4a4a5c;
}

::selection {
    background: rgba(167, 139, 250, 0.35);
}
"""


def load_styles() -> None:
    """Load EZRA CURATOR global styles."""
    st.html(f"<style>{CSS}</style>")
