import os
import sys
import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("HermesBot")

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

TOKEN = os.environ.get("TELEGRAM_HERMES_TOKEN")
ALLOWED_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8035491919")

if not TOKEN:
    logger.error("TELEGRAM_HERMES_TOKEN nao configurado!")
    sys.exit(1)

# Middleware for authorization
def is_authorized(update: Update) -> bool:
    if not update.effective_chat:
        return False
    return str(update.effective_chat.id) == str(ALLOWED_CHAT_ID)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        await update.message.reply_text("Acesso nao autorizado. Este e um canal de governanca privado do BRACHÁT.")
        return
    await update.message.reply_text(
        "👋 Ola, Fabio. Eu sou o Hermes (Nuvem).\n\n"
        "Estou pronto para executar tarefas do ecossistema BRACHÁT. Comandos disponiveis:\n"
        "📌 /status - Status do container e recursos\n"
        "📌 /git - Status da sincronizacao com o GitHub"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    try:
        # Check disk space
        df = subprocess.check_output(["df", "-h", "/"]).decode("utf-8")
        # Check memory usage (free -m doesn't always work on macOS/Debian-slim without procps, so let's check carefully)
        try:
            free = subprocess.check_output(["free", "-m"]).decode("utf-8")
        except:
            free = "Nao disponivel"
        
        status_msg = f"⚡ **BRACHÁT Core - Status da Nuvem**\n\n**Disco:**\n`{df}`\n\n**Memoria:**\n`{free}`"
        await update.message.reply_text(status_msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Erro ao obter status: {str(e)}")

async def git_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    try:
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
        last_commit = subprocess.check_output(["git", "log", "-1", "--oneline"]).decode("utf-8").strip()
        remote = subprocess.check_output(["git", "remote", "-v"]).decode("utf-8").strip()
        
        msg = (
            f"🐙 **Git Status (BRACHÁT-MAIN)**\n\n"
            f"**Branch Ativa:** `{branch}`\n"
            f"**Commit Recente:** `{last_commit}`\n\n"
            f"**Remotos:**\n`{remote}`"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Erro ao ler Git: {str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    text = update.message.text
    logger.info(f"Mensagem recebida do Fabio: {text}")
    
    # 1. Sinaliza acao de typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    clickup_key = os.environ.get("CLICKUP_API_KEY")
    if not clickup_key:
        await update.message.reply_text("⚠️ Erro: CLICKUP_API_KEY nao configurada na nuvem!")
        return
        
    list_id = "901714169490"
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        "Authorization": clickup_key,
        "Content-Type": "application/json"
    }
    
    import asyncio
    import requests
    
    payload = {
        "name": f"📥 [Telegram] {text[:30]}...",
        "description": f"Mensagem recebida pelo Telegram Bot:\n\n{text}\n\nChat ID: {update.effective_chat.id}\nMessage ID: {update.message.message_id}",
        "status": "to do",
        "tags": ["telegram_pending"]
    }
    
    try:
        res = await asyncio.to_thread(requests.post, url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            task_data = res.json()
            await update.message.reply_text(
                f"📥 Mensagem enfileirada no ClickUp com sucesso!\n"
                f"📌 **Tarefa:** [{task_data.get('name')}]({task_data.get('url')})\n"
                f"⏳ Aguardando processamento pelo Mac local..."
            )
        else:
            await update.message.reply_text(f"⚠️ Erro ao criar tarefa no ClickUp: HTTP {res.status_code}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro ao conectar com ClickUp: {str(e)}")

from telegram.request import HTTPXRequest

def get_app():
    # Helper to build the application for main.py async runner
    req = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
    app = Application.builder().token(TOKEN).request(req).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("git", git_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app

if __name__ == "__main__":
    logger.info("Iniciando Hermes Telegram Bot de forma isolada...")
    app = get_app()
    app.run_polling()
