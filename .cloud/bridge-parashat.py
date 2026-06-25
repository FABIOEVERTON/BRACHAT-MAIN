#!/usr/bin/env python3
"""Parashat Bridge — Estudo diário da Parashá no Telegram.
Dom: panorama | Seg: aliyah 1+2 | Ter: aliyah 3 | Qua: aliyah 4 | Qui: aliyah 6+7 | Sáb: Shabat"""
import os, sys, json, time, subprocess, urllib.request, logging, threading, re
from pathlib import Path
from datetime import datetime, date, timedelta

TK = os.environ.get("PARASHAT_TELEGRAM_TOKEN", "")
CID = os.environ.get("PARASHAT_ALLOWED_CHAT_ID", "8035491919,-1004351928924")
ZK = os.environ["ZEN_API_KEY"]
GK = os.environ.get("GO_API_KEY", "")
CORPUS_PATH = Path("/opt/brachat/parashat_corpus/parashat_corpus.txt")
TG = f"https://api.telegram.org/bot{TK}"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("parashat")

SYSP = Path("/opt/brachat/parashat_sysp.txt").read_text(encoding="utf-8")

# Cronograma 2026 (Israel schedule) — data do Shabat: (parashat, traducao, torah, haftara, brit_chadasha)
CRONOGRAMA = {
    "13/06": ("Korach", "Rebelião", "Nm 16:1 a 18:32", "1 Sm 11:14 a 12:22", "Rm 13:1 a 7"),
    "20/06": ("Chukát", "Estatuto", "Nm 19:1 a 22:1", "Jz 11:1 a 33", "Jo 3:10 a 21"),
    "27/06": ("Balák", "Destruidor", "Nm 22:2 a 25:9", "Mq 5:6 a 6:8", "1Co 1:20 a 31"),
    "04/07": ("Pin'chás", "Pele escura", "Nm 25:10 a 29:40", "1 Rs 18:46 a 19:21", "Jo 2:13 a 22"),
    "11/07": ("Matôt-Mase'ei", "Tribos-Partidas", "Nm 30:1 a 36:13", "—", "—"),
    "18/07": ("DEVARIM", "Palavras", "Dt 1:1 a 3:22", "Is 1:1 a 27", "1Tm 3 a 17"),
    "25/07": ("Va'etchanán", "E eu supliquei", "Dt 3:23 a 7:11", "Is 40:1 a 26", "Mc 12:28 a 34"),
    "01/08": ("Êkev", "Pois que", "Dt 7:12 a 11:25", "Is 49:14 a 51:3", "Rm 8:31 a 39"),
    "08/08": ("Re'ê", "Observe", "Dt 11:26 a 16:17", "Is 54:11 a 55:5", "1Jo 4:1 a 6"),
    "15/08": ("Shoftím", "Juízes", "Dt 16:18 a 21:9", "Is 51:12 a 52:12", "At 3:22 a 23"),
    "22/08": ("Ki Tetze", "Quando saíres", "Dt 21:10 a 25:19", "Is 54:1 a 10", "Mt 5:27 a 30"),
    "29/08": ("Ki Tavô", "Quando entrares", "Dt 26:1 a 29:9", "Is 60:1 a 22", "Ef 1:3 a 6"),
    "05/09": ("Nitsavím-Vayêlech", "De pé-E ele vai", "Dt 29:10 a 31:30", "Is 61:10 a 63:9", "Jo 16:1 a 17:22"),
    "12/09": ("Yom Teruah", "Dia do Toque", "Gn 21:1-34; Nm 29:1-6", "1 Sm 1:1-2:10", "1Ts 4:16 a 18"),
    "19/09": ("Ha'azínu", "Dêem ouvidos", "Dt 32:1 a 52", "2 Sm 22:1 a 51", "Rm 10:14 a 11:12"),
    "26/09": ("Sucot", "Cabanas", "Lv 22:26-23:44; Nm 29:12-16", "Zc 14:1 a 21", "Ap 7:1 a 10"),
    "03/10": ("Shemini Atseret-Vezôt HaB'rachá", "E esta é a benção", "Dt 33:1 a 34:12", "Js 1:1 a 18", "Rm 7:21 a 25"),
}

DOW = {0: "segunda", 1: "terça", 2: "quarta", 3: "quinta", 4: "sexta", 5: "sábado", 6: "domingo"}
ALIYAH_SCHEDULE = {
    0: ("📖 Panorama Geral", "panorama"),
    1: ("📜 Aliyah 1 + 2", "aliyah 1 e 2"),
    2: ("📜 Aliyah 3", "aliyah 3"),
    3: ("📜 Aliyah 4", "aliyah 4"),
    4: ("📜 Aliyah 6 + 7", "aliyah 6 e 7"),
}

states = {}
LAST_SENT_FILE = Path("/opt/brachat/state/parashat_last_sent.json")

def load_state():
    p = Path("/opt/brachat/state/parashat_states.json")
    if p.exists():
        try: return json.loads(p.read_text())
        except: return {}
    return {}

def save_state(st):
    p = Path("/opt/brachat/state/parashat_states.json")
    p.parent.mkdir(exist_ok=True)
    p.write_text(json.dumps(st, ensure_ascii=False, indent=2))

def get_week_parashat():
    """Find the Parashah for the current study week (Sun-Sat)."""
    today = date.today()
    # Find the upcoming Shabat (Saturday)
    days_ahead = 5 - today.weekday()  # 5 = Saturday
    if days_ahead < 0:
        days_ahead += 7
    shabat = today + timedelta(days=days_ahead)
    key = shabat.strftime("%d/%m")
    for dt, info in sorted(CRONOGRAMA.items()):
        if dt == key:
            return info, key
    # If not found, rewind to find nearest past Shabat
    for dt, info in sorted(CRONOGRAMA.items(), reverse=True):
        dd, mm = dt.split("/")
        cmp_date = date(2026, int(mm), int(dd))
        if cmp_date <= shabat:
            return info, dt
    return None, None

def ask_llm(msgs):
    for model, key, api_url in [
        ("big-pickle", ZK, "https://opencode.ai/zen/v1/chat/completions"),
        ("kimi-k2.6", GK, "https://opencode.ai/zen/go/v1/chat/completions"),
    ]:
        if not key: continue
        try:
            data = json.dumps({"model": model, "messages": msgs, "stream": False}).encode()
            req = urllib.request.Request(api_url, data=data, headers={
                "Content-Type": "application/json", "Authorization": f"Bearer {key}",
                "User-Agent": "curl/8.0"
            })
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())["choices"][0]["message"]["content"].strip()
        except Exception as e:
            log.warning(f"LLM {model} falhou: {e}")
            continue
    return "Erro: LLM sem resposta."

CORPUS_CACHE = None

def load_corpus():
    global CORPUS_CACHE
    if CORPUS_CACHE is not None:
        return CORPUS_CACHE
    if not CORPUS_PATH.exists():
        log.warning(f"Corpus not found at {CORPUS_PATH}")
        CORPUS_CACHE = ""
        return ""
    try:
        text = CORPUS_PATH.read_text(encoding="utf-8")
        CORPUS_CACHE = text
        log.info(f"Corpus loaded: {len(text)} chars")
        return text
    except Exception as e:
        log.error(f"Corpus load error: {e}")
        CORPUS_CACHE = ""
        return ""

# ── Torah reference helpers ─────────────────────────────────────
TORAH_BOOKS = {"GN":"GENESIS","EX":"EXODUS","LV":"LEVITICUS","NM":"NUMBERS","DT":"DEUTERONOMY"}
TORAH_REF_RE = re.compile(r'(Gn|Ex|Lv|Nm|Dt)\s+(\d+)[:;,]\d+\s*(?:a|to|[-–])\s*(\d+)[:;,]\d+', re.IGNORECASE)

BOOK_INDEX_CACHE = None

def build_book_index(corpus):
    """Build a multi‑book index of chapter→section positions from the JPS corpus.
    
    Returns {book_name: [(chapter_num, section_start, section_end), ...]}
    where each entry covers one section (which may span multiple chapters).
    """
    index = {}
    pat = re.compile(r'(\d+)\s*\n(GENESIS|EXODUS|LEVITICUS|NUMBERS|DEUTERONOMY) \n(\d+)')
    for m in pat.finditer(corpus):
        ch = int(m.group(1))
        book = m.group(2)
        pos = m.start()
        # Find the end of this section — look AFTER the current match end
        next_pat = re.compile(
            r'\d+\s*\n(GENESIS|EXODUS|LEVITICUS|NUMBERS|DEUTERONOMY) \n\d+', re.DOTALL)
        next_m = next_pat.search(corpus, m.end())
        end = next_m.start() if next_m else len(corpus)
        index.setdefault(book, []).append((ch, pos, end))
    return index

def get_book_index():
    global BOOK_INDEX_CACHE
    if BOOK_INDEX_CACHE is not None:
        return BOOK_INDEX_CACHE
    corpus = load_corpus()
    if not corpus or len(corpus) < 100:
        BOOK_INDEX_CACHE = {}
        return {}
    BOOK_INDEX_CACHE = build_book_index(corpus)
    return BOOK_INDEX_CACHE

def find_sections_by_torah_ref(question):
    """If the question contains a Torah reference, return matching corpus text."""
    m = TORAH_REF_RE.search(question)
    if not m:
        return None
    book_abbr = m.group(1).upper()
    start_ch = int(m.group(2))
    end_ch = int(m.group(3))
    full_name = TORAH_BOOKS.get(book_abbr)
    if not full_name:
        return None

    index = get_book_index()
    sections = index.get(full_name, [])
    if not sections:
        return None

    # Find sections whose chapter falls within [start_ch, end_ch]
    relevant = []
    for ch, pos, end in sections:
        if start_ch <= ch <= end_ch:
            relevant.append((pos, end))
        elif len(relevant) > 0 and ch > end_ch:
            break
    if not relevant:
        return None

    corpus = load_corpus()
    result = []
    seen = set()
    for pos, end in relevant:
        text = corpus[pos:end].strip()
        key = text[:200]
        if key in seen:
            continue
        seen.add(key)
        result.append(text[:7000])
    return "\n\n".join(result)[:14000] if result else None


def query_local_corpus(question):
    corpus = load_corpus()
    if not corpus or len(corpus) < 100:
        return None

    # 1) Try Torah‑reference lookup first (most reliable)
    torah_result = find_sections_by_torah_ref(question)
    if torah_result:
        return torah_result

    # 2) Fallback: keyword‑based search
    keywords = set()
    for w in question.lower().split():
        w = w.strip(",.!?;:()[]{}\"\"''")
        if len(w) > 3 and w not in STOPWORDS:
            keywords.add(w)

    parashat_names = ["korach","chukat","balak","pinchas","matot","maseei","devarim",
        "vaetchanan","ekev","ree","shoftim","tetze","tavo","nitsavim","vayelech",
        "haazinu","bereshit","noach","lech","vayera","chayei","toledot",
        "vayetze","vayishlach","vayeshev","miketz","vayigash","vayechi",
        "shemot","vaera","bo","beshalach","yitro","mishpatim","terumah",
        "tetzaveh","tisa","vayakhel","pekudei","vayikra","tzav","shemini",
        "tazria","metzora","acharei","kedoshim","emor","behar","bechukotai",
        "bemidbar","nasso","behaalot","shlach"]
    book_names = ["genesis","exodo","levitico","numeros","deuteronomio",
        "torah","pentateuco","shemot","vayikra","bemidbar",
        "neviim","ketuvim","tanakh","tanach","samuel","salmos","proverbios"]

    all_terms = set(k.strip() for k in keywords)
    for pn in parashat_names:
        for kw in keywords:
            if kw[:4] in pn or pn[:4] in kw:
                all_terms.add(pn)
    for bn in book_names:
        for kw in keywords:
            if kw[:4] in bn or bn[:4] in kw:
                all_terms.add(bn)

    sections = re.split(r'={5,}\s*FONTE:|\n={5,}', corpus)
    scored = []
    for sec in sections:
        if len(sec) < 200:
            continue
        sec_lower = sec.lower()
        matches = sum(1 for t in all_terms if t in sec_lower)
        if matches > 0:
            scored.append((matches, sec[:8000]))
    scored.sort(key=lambda x: -x[0])

    if not scored:
        return None

    result_parts = []
    seen = set()
    for score, text in scored[:5]:
        source_match = re.search(r'FONTE:\s*(\S+)', text)
        src = source_match.group(1) if source_match else "corpus"
        if src in seen:
            continue
        seen.add(src)
        clean = re.sub(r'={5,}\s*FIM:.*?={5,}', '', text[:6000]).strip()
        if clean:
            result_parts.append(f"[{src}]\n{clean[:4000]}")
    return "\n\n".join(result_parts)[:14000] if result_parts else None

STOPWORDS = {"que","para","como","por","com","dos","das","nas","nos",
    "mais","mas","era","sao","tem","uma","sua","qual","este","esta",
    "sobre","entre","apos","ate","pelo","pela","aos","pra","pro","sob"}

def tg(method, data=None):
    tout = 60 if method == "getUpdates" else 15
    try:
        url = f"{TG}/{method}"
        body = json.dumps(data).encode() if data else None
        hdrs = {"Content-Type": "application/json"} if data else {}
        req = urllib.request.Request(url, data=body, headers=hdrs)
        with urllib.request.urlopen(req, timeout=tout) as r:
            return json.loads(r.read())
    except Exception as e:
        if method == "getUpdates" and "timed out" in str(e).lower():
            return None
        log.error(f"TG error {method}: {e}")
        return None

def send(chat_id, text):
    if not text: return True
    for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        resp = tg("sendMessage", {"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"})
        if resp is None:
            resp = tg("sendMessage", {"chat_id": chat_id, "text": chunk})
        if resp is None or not resp.get("ok"):
            return False
    return True

def send_daily_study(chat_id):
    """Send the day's Parashah study to the given chat. Retries until success."""
    while True:
        try:
            parashat, dt_key = get_week_parashat()
            if not parashat:
                log.warning("No parashat found for this week")
                time.sleep(300)
                continue
            hoje = date.today()
            wd = hoje.weekday()  # 0=Mon, 6=Sun

            # Fix weekday: in Python Mon=0, Sun=6; convert to Sun=0
            wd_sun = (wd + 1) % 7  # Sun=0, Mon=1, ..., Sat=6

            p_name, p_trad, p_torah, p_haft, p_brit = parashat

            # Shabat (Saturday = 6 in Sun-based)
            if wd_sun == 6:
                msg = (
                    f"*Shabat Shalom!* 🕎\n\n"
                    f"Parashá da semana: *{p_name}* ({p_trad})\n"
                    f"📖 Torah: {p_torah}\n"
                    f"📜 Haftará: {p_haft}\n"
                    f"📜 B'rit Chadashá: {p_brit}\n\n"
                    f"Que este Shabat seja de descanso e estudo da Palavra!"
                )
                if send(chat_id, msg):
                    return True
                log.warning("Send failed, retrying in 60s")
                time.sleep(60)
                continue

            # Friday (Sexta = 5 in Sun-based) — skip / rest day
            if wd_sun == 5:
                log.info("Friday — rest day, no daily study")
                return True

            # Sunday-Thursday study
            if wd_sun not in ALIYAH_SCHEDULE:
                return True

            title, study_topic = ALIYAH_SCHEDULE[wd_sun]
            dia_name = DOW[wd]

            context = f"Parasha: {p_name} ({p_trad})\nTorah: {p_torah}\nEstudo de {DOW[wd]}: {study_topic}"

            # Consulta corpus local
            local_corpus = query_local_corpus(f"{p_name} {study_topic} {p_torah}")

            sysp_content = SYSP + f"\n\n{context}"
            if local_corpus:
                sysp_content += f"\n\n[FONTE LOCAL — TORAH_CORPUS]\n{local_corpus[:4000]}\n[/FONTE]\n\nUse EXCLUSIVAMENTE a fonte acima. Se nao tiver info, avise."

            msgs = [
                {"role": "system", "content": sysp_content + "\n\nGere um estudo conciso baseado na fonte. Máximo 3000 caracteres."},
                {"role": "user", "content": f"Estudo de {dia_name} — {p_name}: {title}"},
            ]

            response = ask_llm(msgs)
            header = f"*{p_name}* — {title}\n_{p_torah}_\n\n"
            fonte = "📖 *Fonte: Corpus Local TORAH_CORPUS*" if local_corpus else "⚠️ *Sem fonte do corpus — resposta baseada no prompt genérico*"
            if send(chat_id, header + response + "\n\n" + fonte):
                return True
            log.warning("Send failed, retrying in 60s")
            time.sleep(60)
        except Exception as e:
            log.error(f"send_daily_study error: {e}")
            time.sleep(60)

def load_last_sent():
    if LAST_SENT_FILE.exists():
        try: return json.loads(LAST_SENT_FILE.read_text())
        except: return {}
    return {}

def save_last_sent(data):
    LAST_SENT_FILE.parent.mkdir(exist_ok=True)
    LAST_SENT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def daily_study_scheduler():
    last_sent = load_last_sent()
    while True:
        try:
            now = datetime.now()
            today_str = date.today().isoformat()
            # Send at 9:00-9:05 AM (check every 30s within the window)
            if now.hour == 9 and now.minute < 5:
                for cid_raw in CID.split(","):
                    cid = int(cid_raw.strip())
                    if cid >= 0: continue  # only groups
                    if last_sent.get(str(cid)) != today_str:
                        wd_sun = (date.today().weekday() + 1) % 7
                        if wd_sun <= 4 or wd_sun == 6:
                            log.info(f"Sending daily study to {cid} ({DOW[date.today().weekday()]})")
                            if send_daily_study(cid):
                                last_sent[str(cid)] = today_str
                                save_last_sent(last_sent)
                time.sleep(300)  # wait 5min to avoid re-send in same window
            else:
                time.sleep(60)  # check every minute otherwise
        except Exception as e:
            log.error(f"Daily scheduler: {e}")
            time.sleep(60)

def on_msg(chat_id, text):
    if str(chat_id) not in CID.split(","):
        log.warning(f"Unauthorized: {chat_id}")
        return

    state = states.get(chat_id, {"history": [], "state": 0})

    if text.lower() in ("hoje", "estudar", "parashá", "parashat", "estudo"):
        send_daily_study(chat_id)
        return

    # Interactive LLM chat
    parashat, dt_key = get_week_parashat()
    context = f"Parasha da semana: {parashat[0]} ({parashat[1]}) — Torah: {parashat[2]}" if parashat else ""
    msgs = [{"role": "system", "content": SYSP + "\n\n" + context}]
    for h in state.get("history", [])[-10:]:
        msgs.append(h)
    msgs.append({"role": "user", "content": text})

    response = ask_llm(msgs)
    state.setdefault("history", []).append({"role": "user", "content": text})
    state.setdefault("history", []).append({"role": "assistant", "content": response})
    state["last_active"] = time.time()
    states[chat_id] = state
    save_state(states)
    send(chat_id, response)

def poll():
    offset = 0
    while True:
        try:
            updates = tg("getUpdates", {"offset": offset, "timeout": 30})
            if not updates or "result" not in updates:
                continue
            for u in updates["result"]:
                offset = u["update_id"] + 1
                msg = u.get("message")
                if not msg: continue
                txt = msg.get("text", "")
                cid = msg["chat"]["id"]
                if txt:
                    log.info(f"[{cid}] {txt[:80]}")
                    threading.Thread(target=on_msg, args=(cid, txt)).start()
        except Exception as e:
            log.error(f"Poll error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if not TK:
        log.error("PARASHAT_TELEGRAM_TOKEN not set")
        sys.exit(1)
    states = load_state()
    log.info(f"Parashat iniciado. Chat(s): {CID}")
    log.info(f"Corpus: {CORPUS_PATH} ({CORPUS_PATH.stat().st_size if CORPUS_PATH.exists() else 0} bytes)")
    threading.Thread(target=daily_study_scheduler, daemon=True).start()
    poll()
