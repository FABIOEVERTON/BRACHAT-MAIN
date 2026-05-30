import os
import sys
import time
import requests
import json

# Carrega chaves de API a partir do apis.env local
def load_env():
    env_path = "/Users/mac/apis/apis.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()
CLICKUP_API_KEY = os.environ.get("CLICKUP_API_KEY")
TELEGRAM_HERMES_TOKEN = os.environ.get("TELEGRAM_HERMES_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ALLOWED_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8035491919")
LIST_ID = "901714169490"

# Prompt do Sistema para a Antigravity Local
SYSTEM_INSTRUCTION = (
    "Você é o Antigravity, o Arquiteto de IA do ecossistema BRACHÁT.\n"
    "Seu papel é ajudar o CEO Fábio no planejamento estratégico, design de sistemas, "
    "organização de agentes e lógica de código do projeto.\n\n"
    "Regras de comportamento:\n"
    "1. Responda sempre em Português Brasileiro de forma clara, técnica e objetiva.\n"
    "2. Seja conciso. Prefira bullet points e tabelas para estruturar informações longas.\n"
    "3. Você está rodando localmente no Mac do Fábio e respondendo através do bot de execução Hermes.\n"
    "4. Mantenha a segurança em primeiro lugar (Zero-Trust)."
)

def call_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt_text}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 1500
        }
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ Erro de processamento na API do Gemini: HTTP {res.status_code}"
    except Exception as e:
        return f"⚠️ Erro de comunicação com a IA local: {str(e)}"

def send_telegram_reply(chat_id, text, reply_to_id=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_HERMES_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_to_id:
        payload["reply_to_message_id"] = reply_to_id
    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.status_code in [200, 201]
    except Exception as e:
        print(f"Erro ao enviar resposta no Telegram: {str(e)}")
        return False

def update_clickup_task(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "status": "complete"
    }
    try:
        res = requests.put(url, headers=headers, json=payload, timeout=10)
        return res.status_code == 200
    except Exception as e:
        print(f"Erro ao concluir tarefa {task_id} no ClickUp: {str(e)}")
        return False

def check_clickup_queue():
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task?subtasks=true&statuses[]=to do&tags[]=telegram_pending"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json().get("tasks", [])
    except Exception as e:
        print(f"Erro ao consultar fila no ClickUp: {str(e)}")
    return []

def main():
    print(f"🚀 BRACHÁT ClickUp Daemon iniciado. Monitorando a lista {LIST_ID}...")
    sys.stdout.flush()
    
    while True:
        tasks = check_clickup_queue()
        for task in tasks:
            task_id = task.get("id")
            task_name = task.get("name")
            desc = task.get("description", "")
            
            print(f"\n[Fila] Processando tarefa: {task_name} (ID: {task_id})")
            sys.stdout.flush()
            
            # Extrair Chat ID e Message ID da descrição da tarefa
            chat_id = ALLOWED_CHAT_ID
            message_id = None
            
            # A descrição foi formatada como:
            # "Mensagem recebida pelo Telegram Bot:\n\n{text}\n\nChat ID: {chat_id}\nMessage ID: {message_id}"
            user_text = ""
            lines = desc.split("\n")
            in_msg = False
            for line in lines:
                if line.startswith("Chat ID:"):
                    try:
                        chat_id = line.split(":", 1)[1].strip()
                    except:
                        pass
                elif line.startswith("Message ID:"):
                    try:
                        message_id = int(line.split(":", 1)[1].strip())
                    except:
                        pass
                elif line.startswith("Mensagem recebida pelo Telegram Bot:"):
                    in_msg = True
                elif in_msg:
                    if line.strip() == "" and user_text == "":
                        continue
                    if "Chat ID:" in line or "Message ID:" in line:
                        in_msg = False
                    else:
                        user_text += line + "\n"
            
            user_text = user_text.strip()
            if not user_text:
                # Fallback para o nome da tarefa
                user_text = task_name.replace("📥 [Telegram] ", "")
            
            print(f"  Mensagem extraida: \"{user_text}\"")
            print(f"  Chat ID: {chat_id} | Message ID: {message_id}")
            sys.stdout.flush()
            
            # Enviar aviso no Telegram de que o Mac esta processando
            send_telegram_reply(chat_id, "⚙️ **Mac local ativo:** Processando instrução com a Antigravity local...", reply_to_id=message_id)
            
            # Chamar a inteligência da Antigravity (Gemini)
            reply_text = call_gemini(user_text)
            
            # Responder no Telegram
            success = send_telegram_reply(chat_id, reply_text, reply_to_id=message_id)
            
            if success:
                print("  Resposta enviada com sucesso no Telegram.")
                # Marcar a tarefa no ClickUp como concluída
                update_clickup_task(task_id)
                print("  Tarefa ClickUp marcada como concluída.")
            else:
                print("  Falha ao enviar resposta no Telegram. Mantendo na fila.")
            sys.stdout.flush()
            
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDaemon encerrado.")
