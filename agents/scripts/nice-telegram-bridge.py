#!/usr/bin/env python3
import os, sys, json, time, urllib.request, urllib.error, logging
from pathlib import Path

TELEGRAM_TOKEN = os.environ.get("NICE_TELEGRAM_TOKEN")
ZEN_API_KEY = os.environ.get("ZEN_API_KEY")
ZEN_MODEL = "big-pickle"
POLL_INTERVAL = 1
STATE_FILE = Path("/tmp/nice-telegram-bridge-state.json")
CHAT_FILE = Path("/tmp/nice-telegram-chat.json")
LOG_FILE = Path("/tmp/nice-telegram-bridge.log")
BROADCAST_FILE = Path("/tmp/nice-broadcast.json")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
ZEN_API = "https://opencode.ai/zen/v1/chat/completions"

REPO = Path("/Users/mac/brachat-main")

def git_push(msg="update: nice state"):
    import subprocess
    try:
        subprocess.run(["git", "add", "."], cwd=REPO, check=True, capture_output=True, timeout=15)
        res = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, check=True, capture_output=True, text=True, timeout=15)
        if res.stdout.strip():
            subprocess.run(["git", "commit", "--no-verify", "-m", msg], cwd=REPO, check=True, capture_output=True, timeout=15)
            subprocess.run(["git", "push"], cwd=REPO, check=True, capture_output=True, timeout=15)
            log.info("Git changes pushed successfully.")
        return True
    except Exception as e:
        log.error(f"Git push failed: {e}")
        return False

def get_system_prompt():
    agent_md = REPO / "agents" / "director_agents" / "nice" / "nice.md"
    instructions = agent_md.read_text() if agent_md.exists() else ""
    if not instructions:
        instructions = (
            "Você é a NICE, assistente de governança doméstica da Dona Lu (Luciana Everton). "
            "Você ajuda com compras, contas, agenda, saúde, escola e tarefas de casa. "
            "Seja educada, calorosa e prática."
        )
    return f"Voce eh a NICE, agente de governanca domestica BRACHAT.\nData: {time.strftime('%d/%m/%Y %H:%M')}\n\n{instructions}\n\nRegras: Portugues, breve, sem emojis."

ALLOWED_CHAT = None
if CHAT_FILE.exists():
    try:
        data = json.loads(CHAT_FILE.read_text())
        ALLOWED_CHAT = data.get("chat_id")
        log.info(f"Loaded allowed chat: {ALLOWED_CHAT}")
    except:
        pass

def tg(method, data=None):
    url = f"{TG_API}/{method}"
    if data:
        data = json.dumps(data).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    else:
        req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        log.error(f"TG {method}: {e}")
        return None

def send(chat_id, text):
    if not text:
        return
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
    for chunk in chunks:
        tg("sendMessage", {"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"})

def broadcast(text):
    if ALLOWED_CHAT:
        send(ALLOWED_CHAT, text)
        return True
    return False

def ask_zen(msg):
    body = json.dumps({
        "model": ZEN_MODEL,
        "messages": [
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": msg}
        ],
        "max_tokens": 1024,
        "temperature": 0.2
    }).encode()
    req = urllib.request.Request(
        ZEN_API, data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ZEN_API_KEY}",
            "User-Agent": "Mozilla/5.0"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read())
            return resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        log.error(f"ZEN: {e}")
        return None

WELCOME_MSG = (
    "\U0001f3e0 *Nice \u2014 Assistente de Governan\u00e7a Dom\u00e9stica*\n\n"
    "Shalom Dona Lu! Sou a Nice, sua assistente pessoal para o dia a dia da casa.\n\n"
    "\U0001f6d2 *Compras* \u2014 mercado, feira, farm\u00e1cia\n"
    "\U0001f4b0 *Contas* \u2014 boletos, vencimentos, pagamentos\n"
    "\U0001f4c5 *Agenda* \u2014 consultas, escola, eventos\n"
    "\U0001f9a0 *Sa\u00fade* \u2014 rem\u00e9dios, exames, cuidados\n"
    "\U0001f4da *Escola* \u2014 tarefas, reuni\u00f5es, material\n\n"
    "Gastos at\u00e9 R$100 resolvo na hora. At\u00e9 R$500 pe\u00e7o sua confirma\u00e7\u00e3o.\n"
    "Me mande o que precisar! \U0001f60a"
)

def handle_msg(chat_id, text):
    if not text:
        return
    log.info(f"<< {text[:100]}")
    if text.startswith("/"):
        if text == "/start":
            send(chat_id, WELCOME_MSG)
        elif text == "/chatid":
            send(chat_id, f"Seu chat ID: `{chat_id}`")
        return
    tg("sendChatAction", {"chat_id": chat_id, "action": "typing"})
    resp = ask_zen(text)
    if resp:
        formatted = f"\U0001f3e0 *Nice:*\n{resp}"
        send(chat_id, formatted)
        log.info(f">> {resp[:100]}")
        git_push(f"update: nice state on msg '{text[:20]}'")
    else:
        send(chat_id, "\U0001f3e0 *Nice:* Desculpe, tive um erro. Pode repetir?")

def process_broadcasts():
    if not BROADCAST_FILE.exists():
        return
    try:
        data = json.loads(BROADCAST_FILE.read_text())
        pending = data.get("pending", [])
        if not pending:
            return
        sent = []
        for item in pending:
            ok = broadcast(item.get("text", ""))
            sent.append({**item, "status": "sent" if ok else "no_chat"})
        data["pending"] = []
        data["history"] = data.get("history", []) + sent
        BROADCAST_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        log.info(f"Broadcast: {len(sent)} messages sent")
    except Exception as e:
        log.error(f"broadcast error: {e}")

def main():
    global ALLOWED_CHAT
    state = {"last_update_id": 0}
    if STATE_FILE.exists():
        try: state = json.loads(STATE_FILE.read_text())
        except: pass

    if ALLOWED_CHAT:
        log.info(f"Nice bridge (direct API) started. Listening for {ALLOWED_CHAT}...")
    else:
        log.info("Nice bridge started. NO chat locked.")

    last_broadcast_check = 0
    while True:
        try:
            now = time.time()
            if now - last_broadcast_check >= 30:
                process_broadcasts()
                last_broadcast_check = now

            updates = tg("getUpdates", {"offset": state.get("last_update_id", 0) + 1, "timeout": 10, "allowed_updates": ["message"]})
            if updates and updates.get("ok") and updates.get("result"):
                for upd in updates["result"]:
                    state["last_update_id"] = upd["update_id"]
                    if "message" not in upd: continue
                    msg = upd["message"]
                    chat_id = str(msg.get("chat", {}).get("id", ""))

                    if ALLOWED_CHAT is None:
                        ALLOWED_CHAT = chat_id
                        CHAT_FILE.write_text(json.dumps({"chat_id": chat_id}, indent=2))
                        log.info(f"Registered chat ID: {chat_id}")
                        send(chat_id, WELCOME_MSG)

                    if chat_id != ALLOWED_CHAT:
                        log.info(f"Ignored {chat_id}")
                        continue

                    if "text" in msg:
                        handle_msg(chat_id, msg["text"].strip())

            STATE_FILE.write_text(json.dumps(state))
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            log.info("Shutdown.")
            break
        except Exception as e:
            log.error(f"loop: {e}")
            time.sleep(POLL_INTERVAL * 5)

if __name__ == "__main__":
    main()
