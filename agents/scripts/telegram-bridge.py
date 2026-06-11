#!/usr/bin/env python3
"""EZRA Telegram Bridge — conecta Telegram ao OpenCode via Zen API."""
import os, sys, json, time, urllib.request, urllib.error, logging
from pathlib import Path

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ALLOWED_CHAT = os.environ.get("ALLOWED_CHAT_ID")
ZEN_MODEL = "gemma2:2b"
POLL_INTERVAL = 1
STATE_FILE = Path("/tmp/telegram-bridge-state.json")
LOG_FILE = Path("/tmp/telegram-bridge.log")

REPO = Path("/Users/mac/brachat-main")

def git_push(msg="update: ezra state"):
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
    agent_md = REPO / "agents" / "orchestrator_agent" / "orchestrator.md"
    instructions = agent_md.read_text() if agent_md.exists() else ""
    if not instructions:
        instructions = "Voce eh o EZRA, orquestrador do ecossistema BRACHAT. Assistente pessoal do Fabio Everton. Responda de forma direta, objetiva e em portugues."
    return instructions

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
log = logging.getLogger(__name__)

TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
ZEN_API = "https://opencode.ai/zen/v1/chat/completions"

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
def ask_llama(sys_prompt, user_msg):
    try:
        payload = json.dumps({
            "model": "gemma2:2b",
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_msg}
            ],
            "stream": False
        }).encode()
        req = urllib.request.Request("http://147.15.18.252:11434/api/chat", data=payload, headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())["message"]["content"].strip()
    except Exception as e:
        log.error(f"Llama erro: {e}")
        return None

def handle_msg(chat_id, text):
    if not text:
        return
    log.info(f"<< {text[:100]}")
    if text.startswith("/"):
        if text == "/start":
            send(chat_id, "EZRA online via Llama local. Envie sua mensagem.")
        return
    tg("sendChatAction", {"chat_id": chat_id, "action": "typing"})
    conv_id = f"telegram-{chat_id}"
    resp = ask_llama(get_system_prompt(), text)
    if resp:
        send(chat_id, resp)
        log.info(f">> {resp[:100]}")
        git_push(f"update: ezra state on msg '{text[:20]}'")
    else:
        send(chat_id, "Erro ao processar. Tente de novo.")

def main():
    state = {"last_update_id": 0}
    if STATE_FILE.exists():
        try: state = json.loads(STATE_FILE.read_text())
        except: pass
    log.info(f"EZRA bridge (Llama) started. Listening for {ALLOWED_CHAT}...")
    while True:
        try:
            updates = tg("getUpdates", {"offset": state.get("last_update_id", 0) + 1, "timeout": 10, "allowed_updates": ["message"]})
            if updates and updates.get("ok") and updates.get("result"):
                for upd in updates["result"]:
                    state["last_update_id"] = upd["update_id"]
                    if "message" not in upd: continue
                    msg = upd["message"]
                    chat_id = str(msg.get("chat", {}).get("id", ""))
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
