"""Interface Streamlit: EZRA CURATOR — Knowledge Synthesis Engine."""
import os
import sys
import time
import json
import math
from pathlib import Path
from collections import Counter

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import config  # noqa: E402
from app.logging import QueryLogger  # noqa: E402
from app.rag import answer_question, get_collection, system_status  # noqa: E402
from app.loaders import load_document  # noqa: E402

st.set_page_config(page_title="EZRA CURATOR", page_icon="", layout="wide", initial_sidebar_state="collapsed")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg0: #0B0D14;
    --bg1: #121520;
    --bg2: #161B26;
    --glass: rgba(22, 27, 38, 0.6);
    --glass-strong: rgba(22, 27, 38, 0.82);
    --line: rgba(255, 255, 255, 0.1);
    --cyan: #00F2FE;
    --purple: #9B51E0;
    --magenta: #FF007A;
    --green: #00FF87;
    --yellow: #F6C945;
    --blue: #4D7CFE;
    --red: #FF4D4D;
    --text: #E8ECFF;
    --text-muted: #8A93B8;
    --mono: 'JetBrains Mono', ui-monospace, 'SF Mono', Menlo, monospace;
}

html, body, [data-testid="stAppViewContainer"] {
    height: 100vh;
    max-height: 100vh;
    overflow: hidden;
    background: linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 100%);
    color: var(--text);
    font-family: 'Inter', -apple-system, sans-serif;
}

[data-testid="stHeader"] { background: transparent; height: 0; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stMainMenu"] { display: none !important; }
[data-testid="stAppDeployButton"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* Cyberpunk: grid overlay + neon glow orbs */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(800px 420px at 85% -10%, rgba(155, 81, 224, 0.16), transparent 60%),
        radial-gradient(720px 420px at 5% 110%, rgba(0, 242, 254, 0.12), transparent 60%),
        radial-gradient(520px 300px at 50% 50%, rgba(255, 0, 122, 0.05), transparent 60%),
        linear-gradient(rgba(0, 242, 254, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 242, 254, 0.03) 1px, transparent 1px);
    background-size: auto, auto, auto, 42px 42px, 42px 42px;
}

.main .block-container {
    padding: 0;
    max-width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    z-index: 1;
}

/* ===== TOP BAR ===== */
.top-bar {
    display: grid;
    grid-template-columns: 1.3fr 1.1fr 1fr 0.9fr;
    gap: 16px;
    padding: 14px 24px;
    background: rgba(11, 13, 20, 0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--line);
    position: sticky;
    top: 0;
    z-index: 10;
}
.top-bar > div { display: flex; align-items: center; gap: 8px; }
.brand {
    font-weight: 700;
    font-size: 1.15rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--cyan);
    text-shadow: 0 0 12px rgba(0, 242, 254, 0.55), 0 0 32px rgba(0, 242, 254, 0.22);
    white-space: nowrap;
}
.brand small {
    font-weight: 400;
    color: var(--text-muted);
    font-size: 0.6rem;
    margin-left: 10px;
    letter-spacing: 2px;
    text-shadow: none;
}

.status-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px var(--green), 0 0 22px rgba(0, 255, 135, 0.6);
    animation: pulse 1.6s ease-in-out infinite;
    flex-shrink: 0;
}
.status-dot.degraded {
    background: var(--magenta);
    box-shadow: 0 0 10px var(--magenta), 0 0 22px rgba(255, 0, 122, 0.6);
}

.pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 0.62rem;
    font-weight: 600;
    font-family: var(--mono);
    background: var(--glass);
    border: 1px solid var(--line);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    white-space: nowrap;
}
.pill-accent { color: var(--cyan); border-color: rgba(0, 242, 254, 0.35); box-shadow: 0 0 12px rgba(0, 242, 254, 0.18); }
.pill-success { color: var(--green); border-color: rgba(0, 255, 135, 0.35); box-shadow: 0 0 12px rgba(0, 255, 135, 0.18); }
.pill-warn { color: var(--yellow); border-color: rgba(246, 201, 69, 0.35); }
.pill-danger { color: var(--magenta); border-color: rgba(255, 0, 122, 0.4); box-shadow: 0 0 12px rgba(255, 0, 122, 0.22); }

.chain { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.chain .node {
    background: var(--glass);
    border: 1px solid var(--line);
    color: var(--text-muted);
    padding: 3px 9px;
    border-radius: 999px;
    font-size: 0.58rem;
    font-weight: 600;
    font-family: var(--mono);
}
.chain .node.active {
    color: var(--cyan);
    border-color: rgba(0, 242, 254, 0.5);
    box-shadow: 0 0 14px rgba(0, 242, 254, 0.35);
}
.chain .arrow {
    color: var(--magenta);
    font-size: 0.72rem;
    text-shadow: 0 0 8px rgba(255, 0, 122, 0.7);
    animation: arrowFlow 1.2s ease-in-out infinite;
}
.chunk-count {
    font-size: 0.62rem;
    color: var(--cyan);
    font-family: var(--mono);
    text-shadow: 0 0 8px rgba(0, 242, 254, 0.4);
}

/* ===== UPLOAD ZONE ===== */
.upload-zone {
    padding: 14px 24px;
    background: linear-gradient(180deg, rgba(18, 21, 32, 0.8), rgba(18, 21, 32, 0.35));
    border-bottom: 1px solid var(--line);
}
.upload-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.upload-title {
    font-weight: 700;
    font-size: 0.8rem;
    color: var(--purple);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: var(--mono);
    text-shadow: 0 0 10px rgba(155, 81, 224, 0.5);
}
.upload-ok { font-size: 0.58rem; color: var(--text-muted); font-family: var(--mono); letter-spacing: 1px; }
.file-icons { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.file-ico {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 5px 11px;
    border-radius: 7px;
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 1px;
    background: rgba(22, 27, 38, 0.55);
    border: 1px solid var(--line);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}
.ico-pdf { color: var(--red); border-color: rgba(255, 77, 77, 0.4); box-shadow: 0 0 10px rgba(255, 77, 77, 0.18); }
.ico-csv { color: var(--green); border-color: rgba(0, 255, 135, 0.4); box-shadow: 0 0 10px rgba(0, 255, 135, 0.18); }
.ico-txt { color: var(--yellow); border-color: rgba(246, 201, 69, 0.4); box-shadow: 0 0 10px rgba(246, 201, 69, 0.18); }
.ico-md { color: var(--purple); border-color: rgba(155, 81, 224, 0.4); box-shadow: 0 0 10px rgba(155, 81, 224, 0.18); }
.ico-docx { color: var(--blue); border-color: rgba(77, 124, 254, 0.4); box-shadow: 0 0 10px rgba(77, 124, 254, 0.18); }
.ico-html { color: var(--cyan); border-color: rgba(0, 242, 254, 0.4); box-shadow: 0 0 10px rgba(0, 242, 254, 0.18); }

/* ===== MAIN GRID ===== */
.main-grid {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto 1fr;
    gap: 16px;
    padding: 16px 24px 24px;
    overflow: hidden;
    min-height: 0;
}

/* ===== PANELS (glassmorphism) ===== */
.panel {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    min-height: 0;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.panel:hover { border-color: rgba(0, 242, 254, 0.25); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 18px rgba(0, 242, 254, 0.12); }
.panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--line);
}
.panel-title {
    font-weight: 700;
    font-size: 0.75rem;
    color: var(--cyan);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-family: var(--mono);
    text-shadow: 0 0 8px rgba(0, 242, 254, 0.35);
}
.panel-subtitle { font-size: 0.6rem; color: var(--text-muted); font-family: var(--mono); letter-spacing: 1px; }

/* ===== CHAT PANEL ===== */
.chat-panel { grid-column: 1 / -1; grid-row: 2; }
.chat-messages { flex: 1; overflow-y: auto; padding-right: 8px; margin-bottom: 16px; }
.chat-message {
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    animation: fadeIn 0.2s ease;
    background: var(--glass-strong);
    border: 1px solid var(--line);
}
.chat-message.user { border-left: 3px solid var(--cyan); box-shadow: 0 0 14px rgba(0, 242, 254, 0.1); }
.chat-message.assistant { border-left: 3px solid var(--purple); box-shadow: 0 0 14px rgba(155, 81, 224, 0.12); }
.chat-message .role {
    font-size: 0.62rem;
    font-weight: 700;
    color: var(--cyan);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: var(--mono);
}
.chat-message.assistant .role { color: var(--purple); }
.chat-message .content { font-size: 0.85rem; line-height: 1.55; color: var(--text); }
.chat-message .sources {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--line);
    font-size: 0.62rem;
    color: var(--text-muted);
    font-family: var(--mono);
}
.chat-input-wrap { position: relative; }

/* Streamlit native chat input - floating glass bar */
[data-testid="stChatInput"] {
    background: rgba(22, 27, 38, 0.8);
    border: 1px solid rgba(0, 242, 254, 0.25);
    border-radius: 999px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), 0 0 16px rgba(0, 242, 254, 0.12);
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--cyan);
    box-shadow: 0 0 0 2px rgba(0, 242, 254, 0.18), 0 0 28px rgba(255, 0, 122, 0.25);
}
[data-testid="stChatInput"] textarea {
    color: var(--text);
    font-family: var(--mono);
    font-size: 0.85rem;
    background: transparent;
    caret-color: var(--cyan);
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--text-muted); }
[data-testid="stChatInput"] button { color: var(--cyan); }

/* ===== DASHBOARD / METRICS ===== */
.dashboard-panel { grid-column: 2; grid-row: 1; overflow-y: auto; }
.metric-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.metric-card {
    background: rgba(22, 27, 38, 0.6);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover { border-color: rgba(255, 0, 122, 0.35); box-shadow: 0 0 16px rgba(255, 0, 122, 0.15); }
.metric-label {
    font-size: 0.58rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: var(--mono);
    margin-bottom: 4px;
}
.metric-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--cyan);
    font-family: var(--mono);
    line-height: 1.2;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.35);
}
.metric-value.hero {
    font-size: 3.2rem;
    color: var(--cyan);
    text-shadow: 0 0 16px rgba(0, 242, 254, 0.6), 0 0 42px rgba(0, 242, 254, 0.3);
}
.metric-delta { font-size: 0.6rem; color: var(--text-muted); margin-top: 4px; font-family: var(--mono); }

/* ===== CHARTS ROW (donut / sparkline / radar) ===== */
.charts-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 12px; }
.chart-card {
    background: rgba(11, 13, 20, 0.6);
    border: 1px solid var(--line);
    border-radius: 10px;
    padding: 12px;
    min-height: 150px;
}
.chart-card .panel-title { margin-bottom: 10px; font-size: 0.62rem; }
.chart-wrap { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.donut {
    width: 96px; height: 96px;
    border-radius: 50%;
    position: relative;
    animation: spinIn 0.6s ease;
}
.donut-core {
    position: absolute;
    inset: 13px;
    border-radius: 50%;
    background: #0B0D14;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: var(--mono);
    font-size: 1rem;
    font-weight: 700;
    color: var(--cyan);
    text-align: center;
    line-height: 1.2;
    box-shadow: inset 0 0 18px rgba(0, 0, 0, 0.6);
}
.donut-core small { font-size: 0.5rem; color: var(--text-muted); font-weight: 400; }
.donut-legend { width: 100%; }
.lg { display: flex; align-items: center; gap: 6px; padding: 2px 0; }
.lg-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; box-shadow: 0 0 6px currentColor; }
.lg-name { flex: 1; font-size: 0.55rem; color: var(--text-muted); font-family: var(--mono); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.lg-val { font-size: 0.58rem; color: var(--cyan); font-family: var(--mono); }
svg.chart-svg { width: 100%; height: 60px; display: block; }

/* ===== DOCUMENT USAGE BARS ===== */
.doc-usage { margin-top: 12px; }
.doc-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    background: rgba(11, 13, 20, 0.55);
    border: 1px solid var(--line);
    border-radius: 8px;
    margin-bottom: 8px;
}
.doc-name {
    font-size: 0.65rem;
    font-weight: 600;
    color: var(--text);
    flex: 1;
    font-family: var(--mono);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.doc-bar { flex: 2; height: 6px; background: rgba(255, 255, 255, 0.06); border-radius: 3px; overflow: hidden; }
.doc-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--cyan), var(--purple));
    border-radius: 3px;
    box-shadow: 0 0 8px rgba(0, 242, 254, 0.5);
    transition: width 0.3s ease;
}
.doc-pct { font-size: 0.62rem; color: var(--cyan); font-weight: 600; font-family: var(--mono); min-width: 45px; text-align: right; }
.doc-chunks { font-size: 0.55rem; color: var(--text-muted); font-family: var(--mono); }

/* ===== ACTIVITY LOG (terminal) ===== */
.activity-panel { grid-column: 1; grid-row: 1; background: rgba(8, 9, 13, 0.85); }
.activity-panel .panel-title { color: var(--green); text-shadow: 0 0 8px rgba(0, 255, 135, 0.4); }
.activity-list { flex: 1; overflow-y: auto; padding-right: 8px; }
.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px;
    background: rgba(11, 13, 20, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    margin-bottom: 8px;
    font-family: var(--mono);
}
.activity-time { font-size: 0.58rem; color: var(--cyan); white-space: nowrap; margin-top: 2px; }
.activity-content { flex: 1; font-size: 0.65rem; color: var(--text); line-height: 1.4; }
.activity-content .q { font-weight: 500; color: var(--green); }
.activity-content .meta { color: var(--text-muted); font-size: 0.55rem; margin-top: 2px; }
.activity-badge {
    font-size: 0.52rem;
    padding: 2px 7px;
    border-radius: 999px;
    font-weight: 700;
    font-family: var(--mono);
    letter-spacing: 0.5px;
}
.activity-badge.live { color: var(--green); border: 1px solid rgba(0, 255, 135, 0.4); box-shadow: 0 0 10px rgba(0, 255, 135, 0.25); }
.activity-badge.query { color: var(--magenta); border: 1px solid rgba(255, 0, 122, 0.4); box-shadow: 0 0 10px rgba(255, 0, 122, 0.2); }

/* ===== FOOTER ===== */
.footer {
    grid-column: 1 / -1;
    text-align: center;
    padding: 12px;
    color: var(--text-muted);
    font-size: 0.6rem;
    border-top: 1px solid var(--line);
    font-family: var(--mono);
    letter-spacing: 1px;
}

/* ===== STREAMLIT WIDGET OVERRIDES ===== */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(22, 27, 38, 0.5);
    border: 1px dashed rgba(0, 242, 254, 0.35);
    border-radius: 12px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--magenta);
    box-shadow: 0 0 16px rgba(255, 0, 122, 0.2);
}
[data-testid="stFileUploaderDropzone"] small { color: var(--text-muted); font-family: var(--mono); }
[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
    background: rgba(22, 27, 38, 0.6);
    border: 1px solid var(--line);
    border-radius: 8px;
    color: var(--text);
    font-family: var(--mono);
}
button[kind="primary"] {
    background: linear-gradient(90deg, #9B51E0, #FF007A) !important;
    border: none !important;
    color: #fff !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-family: var(--mono);
    font-weight: 700 !important;
    border-radius: 8px !important;
    box-shadow: 0 0 16px rgba(255, 0, 122, 0.35);
    transition: box-shadow 0.2s ease, transform 0.15s ease;
}
button[kind="primary"]:hover { box-shadow: 0 0 28px rgba(255, 0, 122, 0.6); transform: translateY(-1px); }
button[kind="primary"]:disabled { opacity: 0.4; box-shadow: none; }
[data-testid="stSpinner"] { color: var(--cyan) !important; }
[data-testid="stAlert"] { background: rgba(22, 27, 38, 0.7); border: 1px solid var(--line); border-radius: 10px; }
[data-testid="stAlert"] p { color: var(--text); font-family: var(--mono); font-size: 0.75rem; }

/* ===== ANIMATIONS ===== */
@keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
@keyframes arrowFlow { 0%, 100% { transform: translateX(0); opacity: 1; } 50% { transform: translateX(3px); opacity: 0.6; } }
@keyframes spinIn { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }

/* ===== SCROLLBARS ===== */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0, 242, 254, 0.18); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 0, 122, 0.3); }

/* ===== RESPONSIVE ===== */
@media (max-width: 1100px) {
    .top-bar { grid-template-columns: 1fr 1fr; }
    .main-grid { grid-template-columns: 1fr; grid-template-rows: auto auto 1fr; }
    .dashboard-panel { grid-column: 1; grid-row: 2; }
    .activity-panel { grid-column: 1; grid-row: 3; }
    .chat-panel { grid-column: 1; grid-row: 4; }
    .charts-row { grid-template-columns: 1fr; }
}
</style>
"""

# Initialize session state
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

st.markdown(CSS, unsafe_allow_html=True)

logger = QueryLogger()

# Helpers
def record_query(question: str, result, latency_ms: float):
    st.session_state.stats["total_queries"] += 1
    st.session_state.stats["total_latency"] += latency_ms
    if result.fallback:
        st.session_state.stats["fallback_count"] += 1
    for src in result.sources:
        st.session_state.stats["doc_hits"][src["source"]] += 1
        st.session_state.stats["doc_chunks_used"][src["source"]] += 1

def process_uploaded_files(files):
    if not files:
        return 0, 0
    saved = 0
    for f in files:
        tmp = Path("/tmp") / f.name
        tmp.write_bytes(f.getbuffer())
        docs = load_document(tmp)
        if docs:
            coll = get_collection()
            ids = [f"{tmp.stem}-{d.metadata['chunk']}" for d in docs]
            existing = coll.get(where={"source": tmp.name}, include=[])
            if existing and existing.get("ids"):
                coll.delete(ids=existing["ids"])
            coll.add_texts(
                texts=[d.page_content for d in docs],
                metadatas=[d.metadata for d in docs],
                ids=ids,
            )
            saved += len(docs)
    return len(files), saved

# Get system status
status = system_status()
llm_active = f"{status['llm_provider']} / {status['llm_model']}"
emb_active = f"{status['emb_provider']} / {status['emb_model'].split('/')[-1]}"
degraded = "fallback" in status["emb_error"] or status["llm_provider"] == "indisponível"

try:
    chunk_count = get_collection()._collection.count()
except Exception:
    chunk_count = 0

# Document list for usage tracking
try:
    coll = get_collection()
    metas = coll.get(include=["metadatas"])["metadatas"] or []
    doc_sources = sorted(set(m["source"] for m in metas if m.get("source")))
except Exception:
    doc_sources = []

# ===== CHART DATA (donut / sparkline / radar) =====
_NEON = ["#00F2FE", "#9B51E0", "#FF007A", "#00FF87", "#F6C945", "#4D7CFE"]

_donut_items = st.session_state.stats["doc_hits"].most_common(6)
_donut_total = sum(st.session_state.stats["doc_hits"].values())
if _donut_total > 0 and _donut_items:
    _acc = 0
    _segs = []
    for _i, (_src, _h) in enumerate(_donut_items):
        _d = _h / _donut_total * 100
        _segs.append(f"{_NEON[_i % 6]} {_acc:.1f}deg {_acc + _d:.1f}deg")
        _acc += _d
    if _acc < 100:
        _segs.append(f"#161B26 {_acc:.1f}deg 360deg")
    donut_css = "conic-gradient(" + ", ".join(_segs) + ")"
    _top_src, _top_hits = _donut_items[0]
    donut_center = f"{_top_hits}<small>{_top_src[:14]}</small>"
else:
    donut_css = "conic-gradient(#161B26 0deg 360deg)"
    donut_center = "—"

_ch_vals = [v for _, v in st.session_state.stats["doc_chunks_used"].most_common(12)]
if not _ch_vals:
    _ch_vals = [chunk_count, 0, 0, 0]
_mx = max(_ch_vals) or 1
_n = len(_ch_vals)
_W, _H, _pad = 200, 48, 6
_sp_pts = [
    (round(_pad + _i * (_W - 2 * _pad) / (_n - 1 if _n > 1 else 1), 1),
     round(_H - _pad - (_v / _mx) * (_H - 2 * _pad), 1))
    for _i, _v in enumerate(_ch_vals)
]
spark_path = " ".join(f"{x},{y}" for x, y in _sp_pts)

_CAT_KW = [
    ("Technical", ["engen", "tech", "guia", "manual", "api", "back-end", "backend", "desenvol", "software"]),
    ("Business", ["venda", "vend", "business", "negocio", "negócio", "comerc", "mkt", "mercado"]),
    ("Legal", ["lei", "contrat", "jurid", "compl", "legal", "norma"]),
    ("Operations", ["oper", "suporte", "rh", "people", "folha", "interno"]),
    ("Finance", ["fin", "orc", "contab", "receita"]),
]
_CATS = ["Technical", "Business", "Legal", "Operations", "Finance"]
_cat_vals = {c: 0 for c in _CATS}
for _src, _hits in st.session_state.stats["doc_hits"].items():
    _s = _src.lower()
    _chosen = "Other"
    for _c, _kws in _CAT_KW:
        if any(_k in _s for _k in _kws):
            _chosen = _c
            break
    _cat_vals[_chosen] = _cat_vals.get(_chosen, 0) + _hits

_R, _CX, _CY = 46, 100, 68
_maxv = max(_cat_vals.values()) or 1
_radar_pts = []
for _i, _c in enumerate(_CATS):
    _a = math.radians(-90 + _i * 72)
    _r = _R * (_cat_vals[_c] / _maxv)
    _radar_pts.append((_CX + _r * math.cos(_a), _CY + _r * math.sin(_a)))
radar_path = " ".join(f"{x:.1f},{y:.1f}" for x, y in _radar_pts)
_ring_pts = [(round(_CX + _R * math.cos(math.radians(-90 + _i * 72)), 1),
              round(_CY + _R * math.sin(math.radians(-90 + _i * 72)), 1)) for _i in range(5)]
ring_path = " ".join(f"{x},{y}" for x, y in _ring_pts)
ring_path += f" {_ring_pts[0][0]},{_ring_pts[0][1]}"

prov = (status.get("llm_provider") or "").lower()
def _node(name: str) -> str:
    n = name.lower()
    hit = (n in prov) if n in ("cohere", "mistral", "anthropic") else ("local" in prov or "indisponivel" in prov)
    return f'<span class="node{" active" if hit else ""}">{name}</span>'

chain_html = (
    _node("Cohere") + '<span class="arrow">➔</span>'
    + _node("Mistral") + '<span class="arrow">➔</span>'
    + _node("Anthropic") + '<span class="arrow">➔</span>'
    + _node("Local")
)

now_ts = time.strftime("%H:%M:%S")

# ==================== RENDER ====================

st.markdown(CSS, unsafe_allow_html=True)

# ===== TOP BAR =====
st.markdown(f"""
<div class="top-bar">
    <div>
        <span class="brand">EZRA CURATOR<small>Knowledge Synthesis Engine</small></span>
    </div>
    <div style="justify-content:center;">
        <span class="pill pill-accent">LLM: {llm_active}</span>
        <span class="pill pill-accent" style="margin-left:8px;">Embed: {emb_active}</span>
    </div>
    <div style="justify-content:center;">
        <div class="chain">{chain_html}</div>
    </div>
    <div style="justify-content:flex-end; text-align:right;">
        <div class="chunk-count">{chunk_count} chunks · ChromaDB</div>
        <div style="display:flex;align-items:center;gap:6px;justify-content:flex-end;margin-top:4px;">
            <span class="status-dot{' degraded' if degraded else ''}"></span>
            <span class="pill {'pill-danger' if degraded else 'pill-success'}">{'DEGRADED' if degraded else 'OPERATIONAL'}</span>
            <span class="pill pill-danger" style="margin-left:8px;">FALLBACKS ACTIVE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== UPLOAD ZONE =====
st.markdown("""
<div class="upload-zone">
    <div class="upload-header">
        <span class="upload-title">Ingest New Documents</span>
        <span class="upload-ok">AUTO-INDEX · CHROMADB</span>
    </div>
    <div class="file-icons">
        <span class="file-ico ico-pdf">PDF</span>
        <span class="file-ico ico-csv">CSV</span>
        <span class="file-ico ico-txt">TXT</span>
        <span class="file-ico ico-md">MD</span>
        <span class="file-ico ico-docx">DOCX</span>
        <span class="file-ico ico-html">HTML</span>
    </div>
</div>
""", unsafe_allow_html=True)

up_col1, up_col2 = st.columns([4, 1])
with up_col1:
    uploaded = st.file_uploader(
        "Drop PDF, CSV, TXT, MD, HTML, JSON, DOCX files here",
        type=["pdf", "csv", "txt", "md", "html", "htm", "json", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="uploader"
    )
with up_col2:
    st.write("")
    ingest_clicked = st.button("INDEX NOW", type="primary", use_container_width=True, disabled=not uploaded)

if ingest_clicked and uploaded:
    with st.spinner("Processing and indexing..."):
        count, chunks = process_uploaded_files(uploaded)
        st.success(f"Indexed {count} file(s) — {chunks} chunks added")
        st.rerun()
elif ingest_clicked and not uploaded:
    st.warning("Select at least one file.")

# ===== MAIN GRID =====
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# ===== LEFT: ACTIVITY LOG (terminal) =====
st.markdown("""
<div class="panel activity-panel">
    <div class="panel-header">
        <span class="panel-title">ACTIVITY LOG</span>
        <span class="panel-subtitle">TERMINAL · REAL-TIME</span>
    </div>
    <div class="activity-list" id="activity-list">
""", unsafe_allow_html=True)

# Render activity items (most recent first)
if st.session_state.stats["total_queries"] == 0:
    st.markdown(f"""
    <div class="activity-item">
        <span class="activity-time">[{now_ts}]</span>
        <div class="activity-content">
            <span class="q">System initialized</span>
            <div class="meta">Vector index ready · {chunk_count} chunks · waiting for queries</div>
        </div>
        <span class="activity-badge live">READY</span>
    </div>
    """, unsafe_allow_html=True)
else:
    total = st.session_state.stats["total_queries"]
    avg_lat = st.session_state.stats["total_latency"] / total if total > 0 else 0
    fb = st.session_state.stats["fallback_count"]
    fb_pct = (fb / total * 100) if total > 0 else 0

    st.markdown(f"""
    <div class="activity-item">
        <span class="activity-time">[{now_ts}]</span>
        <div class="activity-content">
            <span class="q">Session summary</span>
            <div class="meta">Queries: {total} · Avg latency: {avg_lat:.0f}ms · Fallbacks: {fb} ({fb_pct:.1f}%)</div>
        </div>
        <span class="activity-badge live">LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    recent_msgs = [m for m in st.session_state.messages if m["role"] == "user"][-5:]
    for i, msg in enumerate(reversed(recent_msgs)):
        st.markdown(f"""
        <div class="activity-item">
            <span class="activity-time">[{now_ts}]</span>
            <div class="activity-content">
                <span class="q">{msg['content'][:80]}{'...' if len(msg['content']) > 80 else ''}</span>
                <div class="meta">Q{total - i} · user query</div>
            </div>
            <span class="activity-badge query">QUERY</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# ===== RIGHT: DOCUMENT USAGE DASHBOARD =====
st.markdown("""
<div class="panel dashboard-panel">
    <div class="panel-header">
        <span class="panel-title">DOCUMENT USAGE</span>
        <span class="panel-subtitle">SEARCH DISTRIBUTION</span>
    </div>
    <div class="metric-grid">
""", unsafe_allow_html=True)

total = st.session_state.stats["total_queries"]
avg_lat = st.session_state.stats["total_latency"] / total if total > 0 else 0
fb = st.session_state.stats["fallback_count"]
fb_pct = (fb / total * 100) if total > 0 else 0

st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Queries</div>
            <div class="metric-value hero">{total}</div>
            <div class="metric-delta">This session: {total} queries</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Avg Latency</div>
            <div class="metric-value">{avg_lat:.0f}ms</div>
            <div class="metric-delta">Generation time</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Fallback Rate</div>
            <div class="metric-value">{fb_pct:.1f}%</div>
            <div class="metric-delta">{fb} of {total} queries</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Indexed Chunks</div>
            <div class="metric-value">{chunk_count}</div>
            <div class="metric-delta">ChromaDB vectors</div>
        </div>
""", unsafe_allow_html=True)

st.markdown("""
    </div>
    <div class="doc-usage">
""", unsafe_allow_html=True)

# Document usage bars
if st.session_state.stats["doc_hits"]:
    total_hits = sum(st.session_state.stats["doc_hits"].values())
    for src, hits in st.session_state.stats["doc_hits"].most_common():
        pct = (hits / total_hits * 100) if total_hits > 0 else 0
        chunks_used = st.session_state.stats["doc_chunks_used"].get(src, 0)
        st.markdown(f"""
        <div class="doc-item">
            <span class="doc-name">{src}</span>
            <div class="doc-bar"><div class="doc-bar-fill" style="width:{pct}%"></div></div>
            <span class="doc-pct">{pct:.1f}%</span>
            <span class="doc-chunks">{hits} hits · {chunks_used} chunks</span>
        </div>
        """, unsafe_allow_html=True)
else:
    for src in doc_sources:
        st.markdown(f"""
        <div class="doc-item">
            <span class="doc-name">{src}</span>
            <div class="doc-bar"><div class="doc-bar-fill" style="width:0%"></div></div>
            <span class="doc-pct">0.0%</span>
            <span class="doc-chunks">0 hits</span>
        </div>
        """, unsafe_allow_html=True)

# ===== CHARTS ROW: donut / sparkline / radar =====
_donut_legend = ""
if _donut_items:
    _donut_legend = "".join(
        f'<div class="lg"><span class="lg-dot" style="background:{_NEON[i % 6]};color:{_NEON[i % 6]}"></span>'
        f'<span class="lg-name">{src[:20]}</span><span class="lg-val">{h}</span></div>'
        for i, (src, h) in enumerate(_donut_items)
    )
else:
    _donut_legend = '<div class="lg"><span class="lg-name" style="color:var(--text-muted)">No usage data yet</span></div>'

st.markdown(f"""
    </div>
    <div class="charts-row">
        <div class="chart-card">
            <div class="panel-title">TOP SOURCES</div>
            <div class="chart-wrap">
                <div class="donut" style="background:{donut_css}">
                    <div class="donut-core">{donut_center}</div>
                </div>
                <div class="donut-legend">{_donut_legend}</div>
            </div>
        </div>
        <div class="chart-card">
            <div class="panel-title">CHUNK UTILIZATION</div>
            <svg class="chart-svg" viewBox="0 0 200 48" preserveAspectRatio="none">
                <line x1="6" y1="42" x2="194" y2="42" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
                <polyline points="{spark_path}" fill="none" stroke="#00F2FE" stroke-width="2"
                          style="filter:drop-shadow(0 0 4px rgba(0,242,254,0.7));"/>
                <polygon points="{spark_path} 194,42 6,42" fill="rgba(0,242,254,0.08)" stroke="none"/>
            </svg>
        </div>
        <div class="chart-card">
            <div class="panel-title">SEARCH DISTRIBUTION</div>
            <svg class="chart-svg" viewBox="0 0 200 130" preserveAspectRatio="xMidYMid meet" style="height:110px;">
                <polygon points="{ring_path}" fill="rgba(0,242,254,0.04)" stroke="rgba(0,242,254,0.18)" stroke-width="1"/>
                <polygon points="{radar_path}" fill="rgba(255,0,122,0.22)" stroke="#FF007A" stroke-width="1.5"
                         style="filter:drop-shadow(0 0 5px rgba(255,0,122,0.6));"/>
            </svg>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== CHAT PANEL (full width bottom) =====
st.markdown("""
<div class="panel chat-panel">
    <div class="panel-header">
        <span class="panel-title">CONVERSATION</span>
        <span class="panel-subtitle">EZRA CURATOR</span>
    </div>
    <div class="chat-messages">
""", unsafe_allow_html=True)

# Render messages
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    role_label = "USER" if msg["role"] == "user" else "EZRA"
    st.markdown(f"""
    <div class="chat-message {role_class}">
        <div class="role">{role_label}</div>
        <div class="content">{msg["content"]}</div>
    </div>
    """, unsafe_allow_html=True)
    if msg["role"] == "assistant" and msg.get("sources"):
        src_html = "".join(f'<span style="margin-right:8px;font-family:JetBrains Mono,monospace;">📄 {s["source"]} <span style="color:var(--purple);">({s["score"]:.2f})</span></span>' for s in msg["sources"])
        st.markdown(f'<div class="chat-message assistant" style="border-left-color:var(--magenta);margin-top:-8px;margin-bottom:16px;"><div class="sources">SOURCES: {src_html}</div></div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center;padding:40px 20px;color:var(--text-muted);">
        <div style="font-size:2rem;margin-bottom:8px;color:var(--cyan);text-shadow:0 0 18px rgba(0,242,254,0.6);">◈</div>
        <div style="font-size:0.9rem;font-weight:500;margin-bottom:4px;color:var(--text);font-family:'JetBrains Mono',monospace;letter-spacing:1px;">READY TO SYNTHESIZE</div>
        <div style="font-size:0.7rem;color:var(--text-muted);font-family:'JetBrains Mono',monospace;">Ask a question about your documents</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    </div>
    <div class="chat-input-wrap">
""", unsafe_allow_html=True)

# Chat input
user_prompt = st.chat_input("Ask about your documents...", key="chat_input")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.spinner("Synthesizing..."):
        t0 = time.time()
        result = answer_question(user_prompt, logger=logger)
        latency = (time.time() - t0) * 1000
    st.session_state.last_latency = latency
    record_query(user_prompt, result, latency)
    st.session_state.messages.append({
        "role": "assistant",
        "content": result.answer,
        "sources": result.sources,
        "fallback": result.fallback,
    })
    st.rerun()

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown("""
<div class="footer">
    EZRA CURATOR · Knowledge Synthesis Engine · Oracle ONE Challenge
</div>
</div>
""", unsafe_allow_html=True)
