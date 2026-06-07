#!/usr/bin/env python3
"""NICE Bridge — governança doméstica BRACHAT no Telegram."""
import os, sys, json, time, subprocess, urllib.request, urllib.error, logging
from pathlib import Path

TELEGRAM_TOKEN = os.environ.get("NICE_TELEGRAM_TOKEN")
ALLOWED_CHAT = os.environ.get("NICE_ALLOWED_CHAT_ID")
ZEN_API_KEY = os.environ.get("ZEN_API_KEY")
CLICKUP_TOKEN = os.environ.get("CLICKUP_TOKEN")
ZEN_MODEL = "big-pickle"
POLL_INTERVAL = 1
STATE_FILE = Path("/tmp/nice-bridge-state.json")
REPO_DIR = Path("/opt/brachat/repo")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("/tmp/nice-bridge.log"), logging.StreamHandler()])
log = logging.getLogger("nice")

TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
ZEN_API = "https://opencode.ai/zen/v1/chat/completions"

def git_pull():
    try:
        r = subprocess.run(["git","pull"], cwd=REPO_DIR, capture_output=True, text=True, timeout=15)
        if r.returncode == 0: return True
        return False
    except: return False

def read_json(path):
    try: return json.loads(Path(path).read_text())
    except: return {}

def build_prompt(msg):
    now = time.strftime("%H:%M")
    date = time.strftime("%d/%m/%Y")
    agent_dir = REPO_DIR / "assistant_agents" / "daily" / "nice"
    agent_md = agent_dir / "AGENT.md"
    agent_cache = read_json(agent_dir / "cache.json")
    contacts = read_json(REPO_DIR / "Branding" / "contacts.json") if (REPO_DIR / "Branding" / "contacts.json").exists() else {}

    instructions = ""
    if agent_md.exists():
        instructions = agent_md.read_text()[:2000]
    return f"""Voce eh a NICE, agente de governanca domestica do ecossistema BRACHAT.
Data: {date}  Hora: {now}

{instructions}

Ultimo estado: {json.dumps(agent_cache, ensure_ascii=False)[:500]}

Regras: Responda em portugues. Seja breve (5-8 linhas). Nao use emojis.
Thresholds: <=R$100 automatico. R$101-500 aval Dona Lu. >R$500 bloqueado CEO.
Chame Dona Lu de "Dona Lu" sempre."""

def ask_zen(messages):
    body = json.dumps({"model":ZEN_MODEL,"messages":messages,"max_tokens":1024,"temperature":0.2}).encode()
    req = urllib.request.Request(ZEN_API, data=body, headers={
        "Content-Type":"application/json","Authorization":f"Bearer {ZEN_API_KEY}","User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"Zen: {e}")
        return None

def tg(method, data=None):
    url = f"{TG_API}/{method}"
    if data:
        data = json.dumps(data).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type":"application/json"})
    else:
        req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        log.error(f"TG {method}: {e}")
        return None

def send(chat_id, text):
    if not text: return
    for chunk in [text[i:i+4000] for i in range(0, len(text), 4000)]:
        tg("sendMessage", {"chat_id":chat_id,"text":chunk,"parse_mode":"Markdown"})

def handle_msg(chat_id, text):
    if not text: return
    log.info(f"<< {text[:100]}")
    if text.startswith("/"):
        if text == "/start": send(chat_id, "NICE — governanca domestica online.")
        elif text == "/status":
            ctx = read_json(agent_dir / "cache.json")
            send(chat_id, f"NICE ativa.\nThreshold: {ctx.get('threshold_atual','R$100 auto')}")
        return
    tg("sendChatAction", {"chat_id":chat_id,"action":"typing"})
    git_pull()
    system = build_prompt(text)
    messages = [
        {"role":"system","content":system},
        {"role":"user","content":text}
    ]
    resp = ask_zen(messages)
    if resp:
        send(chat_id, resp)
        log.info(f">> {resp[:100]}")
    else:
        send(chat_id, "Erro ao processar. Tente de novo.")

def main():
    state = {"last_update_id":0}
    if STATE_FILE.exists():
        try: state = json.loads(STATE_FILE.read_text())
        except: pass
    log.info(f"NICE orquestrador iniciado. Chat: {ALLOWED_CHAT}")
    git_pull()
    while True:
        try:
            updates = tg("getUpdates", {"offset":state.get("last_update_id",0)+1,"timeout":10,"allowed_updates":["message"]})
            if updates and updates.get("ok") and updates.get("result"):
                for upd in updates["result"]:
                    state["last_update_id"] = upd["update_id"]
                    if "message" not in upd: continue
                    msg = upd["message"]
                    chat_id = str(msg.get("chat",{}).get("id",""))
                    if chat_id != ALLOWED_CHAT: continue
                    if "text" in msg:
                        handle_msg(chat_id, msg["text"].strip())
            STATE_FILE.write_text(json.dumps(state))
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            log.info("Shutdown."); break
        except Exception as e:
            log.error(f"loop: {e}")
            time.sleep(POLL_INTERVAL*5)

if __name__ == "__main__":
    main()
