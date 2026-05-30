# =========================================================
# IDENTIFICAÇÃO
# =========================================================
# Agent: Ezra Telegram Agent
# Mode: Polling (minimal runtime)
# LLM: Ollama Cloud (qwen3:235b)
# APIs: loaded from APIS_Storage/apis.env
# Memory: Obsidian (future)
# Skills: SKILLS_STORAGE (future)
# =========================================================


# =========================================================
# DEPENDÊNCIAS
# =========================================================
import time
import requests
from pathlib import Path


# =========================================================
# REGRAS / CONFIGURAÇÃO
# =========================================================

API_FILE = Path("/home/mac/brachat-main/apis/apis.env") if Path("/home/mac/brachat-main/apis/apis.env").exists() else Path("/Users/mac/brachat-main/APIS_Storage/apis.env")

OLLAMA_URL = "https://ollama.com/api/chat"
MODEL = "gemma3:4b"

OFFSET = 0


# =========================================================
# CARREGAMENTO DE APIs (SEM ENV DO SISTEMA)
# =========================================================

def load_api_key(key_name: str) -> str:
    if not API_FILE.exists():
        raise FileNotFoundError(f"Arquivo de APIs não encontrado: {API_FILE}")

    with API_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or "=" not in line:
                continue

            k, v = line.split("=", 1)

            if k.strip() == key_name:
                return v.strip()

    raise ValueError(f"Chave não encontrada: {key_name}")


TELEGRAM_TOKEN = load_api_key("TELEGRAM_TOKEN")
OLLAMA_API_KEY = load_api_key("OLLAMA_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


# =========================================================
# LLM CALL (OLLAMA CLOUD)
# =========================================================

def call_llm(user_text: str) -> str:
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": user_text
            }
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        headers=headers,
        timeout=60
    )

    data = response.json()
    return data["message"]["content"]


# =========================================================
# TELEGRAM - GET UPDATES
# =========================================================

def get_updates(offset: int):
    url = f"{TELEGRAM_URL}/getUpdates"

    params = {
        "offset": offset + 1,
        "timeout": 30
    }

    return requests.get(url, params=params, timeout=60).json()


# =========================================================
# TELEGRAM - SEND MESSAGE
# =========================================================

def send_message(chat_id: int, text: str):
    url = f"{TELEGRAM_URL}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, json=payload, timeout=60)


# =========================================================
# LOOP PRINCIPAL (POLLING)
# =========================================================

def run():
    global OFFSET

    while True:
        updates = get_updates(OFFSET)

        if not updates or "result" not in updates:
            time.sleep(1)
            continue

        for update in updates["result"]:
            OFFSET = update["update_id"]

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text")

            if not text:
                continue

            try:
                response = call_llm(text)
            except Exception as e:
                response = f"LLM error: {str(e)}"

            send_message(chat_id, response)


# =========================================================
# ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    run()