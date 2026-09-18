import html
import os
import re
import subprocess
import unicodedata
from datetime import datetime, date

import requests

SITE = "https://btf.org.br/parashot/"
BASE = os.path.dirname(os.path.abspath(__file__))
PROMPT_FILE = os.path.join(BASE, "prompt.txt")
STUDIES_DIR = os.path.join(BASE, "studies")
NBLM = os.path.join(BASE, "venv", "bin", "notebooklm")
NBLM_NOTEBOOK = "e4274837-7838-4bbb-a490-8fde601e5c7a"


def load_prompt():
    with open(PROMPT_FILE, encoding="utf-8") as f:
        return f.read()


def _clean(s):
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", "", s)
    return " ".join(s.split()).strip()


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def parse_table(html_text):
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html_text, re.S)
    out = []
    for r in rows:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        cells = [_clean(c) for c in cells]
        if len(cells) >= 8 and re.match(r"^\d{2}/\d{2}/\d{2}$", cells[0]):
            out.append({
                "data": cells[0],
                "parasha": cells[1],
                "especial": cells[2],
                "traducao": cells[3],
                "torah": cells[4],
                "haftara": cells[5],
                "chadasha": cells[6],
                "tehilim": cells[7],
            })
    return out


def fetch_parashot():
    r = requests.get(SITE, timeout=30)
    r.raise_for_status()
    return parse_table(r.text)


def find_by_query(parashot, query):
    q = _norm(query.strip())
    if not q:
        return None
    for p in parashot:
        if q in _norm(p["parasha"]):
            return p
    digits = re.sub(r"[^0-9]", "", query)
    if len(digits) >= 6:
        for p in parashot:
            pdigits = re.sub(r"[^0-9]", "", p["data"])
            if pdigits == digits or pdigits.endswith(digits):
                return p
    for p in parashot:
        if q in _norm(p["traducao"]):
            return p
    return None


def next_parashot(parashot, today=None):
    today = today or date.today()
    best = None
    for p in parashot:
        try:
            d = datetime.strptime(p["data"], "%d/%m/%y").date()
        except (ValueError, TypeError):
            continue
        if d >= today and (best is None or d < best[0]):
            best = (d, p)
    return best[1] if best else (parashot[0] if parashot else None)


def _studies_context():
    extra = ""
    if os.path.isdir(STUDIES_DIR):
        for fn in sorted(os.listdir(STUDIES_DIR)):
            fp = os.path.join(STUDIES_DIR, fn)
            if os.path.isfile(fp) and fn.lower().endswith((".md", ".txt")):
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as f:
                        content = f.read()[:8000]
                    extra += f"\n--- MATERIAL DE ESTUDO: {fn} ---\n{content}\n"
                except OSError:
                    continue
    return extra


def _notebook_context(parasha):
    q = (
        f"Parasha {parasha['parasha']} (data do shabat: {parasha['data']}): "
        "resuma o conteudo e o tema principal com base nas fontes do caderno. "
        "Cite as fontes entre colchetes. Seja completo e fiel aos textos."
    )
    try:
        subprocess.run([NBLM, "use", NBLM_NOTEBOOK], capture_output=True, text=True, timeout=30)
        r = subprocess.run([NBLM, "ask", q], capture_output=True, text=True, timeout=180)
        out = r.stdout or ""
        m = re.search(r"Answer:\s*(.*?)\s*Resumed conversation", out, re.S)
        return m.group(1).strip() if m else ""
    except Exception:
        return ""


def build_user_text(parasha, query_hint=""):
    parts = [
        f"Parasha da semana: {parasha['parasha']}",
        f"Data (shabat): {parasha['data']}",
        f"Shabat especial: {parasha['especial']}",
        f"Traducao: {parasha['traducao']}",
        f"Torah: {parasha['torah']}",
        f"Haftara: {parasha['haftara']}",
        f"B'rit Chadasha: {parasha['chadasha']}",
        f"Tehilim: {parasha['tehilim']}",
    ]
    if query_hint:
        parts.append(f"Pedido especifico do usuario: {query_hint}")
    extra = _studies_context()
    nblm = _notebook_context(parasha)
    if nblm:
        extra += "\n--- CONSULTA AO NOTEBOOKLM (TORAH_STUDIES) ---\n" + nblm
    if extra:
        parts.append("Material de consulta disponivel (use-o como base fiel; preserve as citacoes):\n" + extra)
    return "\n".join(parts)
