import os
import sys
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("AntigravityBot")

# Load environment variables
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

TOKEN = os.environ.get("TELEGRAM_ANTIGRAVITY_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
ALLOWED_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8035491919")

if not TOKEN:
    logger.error("TELEGRAM_ANTIGRAVITY_TOKEN nao configurado!")
    sys.exit(1)

if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY nao configurado!")
    sys.exit(1)

# In-memory history for Fabio's chat: list of {"role": "user"|"model", "parts": [{"text": "..."}]}
chat_history = []

# System Prompt detailing Antigravity's role and rules
SYSTEM_INSTRUCTION = (
    "Você é o Antigravity, o Arquiteto de IA do ecossistema BRACHÁT. "
    "Seu papel é ajudar o CEO Fábio no planejamento estratégico, design de sistemas, "
    "organização de agentes e lógica de código do projeto.\n\n"
    "Regras de comportamento:\n"
    "1. Responda sempre em Português Brasileiro de forma clara, técnica e objetiva.\n"
    "2. Seja conciso. Prefira bullet points e tabelas para estruturar informações longas.\n"
    "3. Lembre-se de que o Hermes executa as tarefas na nuvem e você planeja as ações com o Fábio.\n"
    "4. Mantenha a rastreabilidade e segurança em primeiro lugar (Zero-Trust)."
)

def is_authorized(update: Update) -> bool:
    if not update.effective_chat:
        return False
    return str(update.effective_chat.id) == str(ALLOWED_CHAT_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Acesso não autorizado.")
        return
    global chat_history
    chat_history = [] # Reset history on start
    await update.message.reply_text(
        "🧠 Olá, Fábio! Eu sou o Antigravity (Arquiteto).\n\n"
        "Estou online na nuvem 24/7 para planejar a arquitetura do ecossistema com você.\n"
        "Use /clear para limpar a nossa memória de sessão recente."
    )

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    global chat_history
    chat_history = []
    await update.message.reply_text("🧹 Memória de sessão recente limpa com sucesso.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    
    text = update.message.text
    global chat_history
    
    # Add user message to history
    chat_history.append({"role": "user", "parts": [{"text": text}]})
    
    # Limit history size to last 20 messages to conserve tokens
    if len(chat_history) > 20:
        chat_history = chat_history[-20:]
        
    await update.channel_chat_created # Keep connection alive or send typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Call Gemini API directly via REST
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": chat_history,
            "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1000
            }
        }
        
        logger.info("Enviando requisicao para o Gemini API...")
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            try:
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                # Add assistant reply to history
                chat_history.append({"role": "model", "parts": [{"text": reply}]})
                await update.message.reply_text(reply, parse_mode="Markdown")
            except (KeyError, IndexError) as parse_err:
                logger.error(f"Erro ao parsear resposta do Gemini: {parse_err}. JSON: {data}")
                await update.message.reply_text("⚠️ Ocorreu um erro ao processar a resposta da IA.")
        else:
            logger.error(f"Erro no Gemini API: Status {response.status_code}. Detalhes: {response.text}")
            await update.message.reply_text(f"⚠️ Erro de API do Gemini: {response.status_code}")
            
    except Exception as e:
        logger.error(f"Erro ao chamar Gemini: {str(e)}")
        await update.message.reply_text(f"⚠️ Ocorreu um erro na comunicação: {str(e)}")

from telegram.request import HTTPXRequest

def get_app():
    req = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app = Application.builder().token(TOKEN).request(req).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear_history))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app

if __name__ == "__main__":
    logger.info("Iniciando Antigravity Telegram Bot de forma isolada...")
    app = get_app()
    app.run_polling()
