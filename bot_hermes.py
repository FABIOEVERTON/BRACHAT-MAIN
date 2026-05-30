import os
import sys
import logging
import subprocess
import json
import shutil
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
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not TOKEN:
    logger.error("TELEGRAM_HERMES_TOKEN nao configurado!")
    sys.exit(1)

# In-memory history for Fabio's chat
chat_history = []

SYSTEM_INSTRUCTION = (
    "Você é o Hermes, o Agente Executador e Orquestrador do ecossistema BRACHÁT.\n"
    "Seu papel é ajudar o CEO Fábio na execução de tarefas, automação, monitoramento de servidores "
    "e gerenciamento técnico de deploy e infraestrutura do projeto.\n\n"
    "Regras de comportamento:\n"
    "1. Responda sempre em Português Brasileiro de forma clara, técnica e objetiva.\n"
    "2. Seja conciso. Prefira bullet points e tabelas para estruturar informações.\n"
    "3. Você está rodando localmente no Mac do Fábio como o orquestrador principal de execução.\n"
    "4. Mantenha o foco em ações práticas, deploys, status e segurança (Zero-Trust)."
)

# Middleware for authorization
def is_authorized(update: Update) -> bool:
    if not update.effective_chat:
        return False
    return str(update.effective_chat.id) == str(ALLOWED_CHAT_ID)

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    global chat_history
    chat_history = []
    await update.message.reply_text("🧹 Memória de sessão recente do Hermes limpa.")

def lock_project_files(project_path, read_only=True):
    mode = 0o444 if read_only else 0o644
    for root, dirs, files in os.walk(project_path):
        if any(ignored in root for ignored in [".git", "node_modules", "__pycache__", ".venv", "dist", "build"]):
            continue
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".html", ".css", ".json", ".md")) and file not in [".brachat-state.json", ".brachat"]:
                try:
                    os.chmod(os.path.join(root, file), mode)
                except:
                    pass

async def switch_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        await update.message.reply_text("⚠️ Uso: /switch <caminho_do_diretorio_do_projeto>")
        return
        
    path = context.args[0]
    if not os.path.exists(path):
        await update.message.reply_text(f"⚠️ Erro: O caminho '{path}' nao existe no Mac.")
        return
        
    active_path = "/Users/mac/brachat-main/active_project.json"
    with open(active_path, "w") as f:
        json.dump({"active_project_path": path}, f)
        
    git_dir = os.path.join(path, ".git")
    hook_msg = ""
    if os.path.exists(git_dir):
        hooks_dir = os.path.join(git_dir, "hooks")
        os.makedirs(hooks_dir, exist_ok=True)
        dest_hook = os.path.join(hooks_dir, "pre-commit")
        src_hook = "/Users/mac/brachat-main/portfolio/agents_team/hermes/hooks/pre-commit"
        try:
            shutil.copy(src_hook, dest_hook)
            os.chmod(dest_hook, 0o755)
            hook_msg = "\n🛡️ **Git Pre-Commit Hook** de controle rígido instalado com sucesso!"
        except Exception as e:
            hook_msg = f"\n⚠️ Falha ao instalar Git Hook: {str(e)}"
            
    brachat_conf = os.path.join(path, ".brachat")
    if not os.path.exists(brachat_conf):
        with open(brachat_conf, "w") as f:
            json.dump({
                "project_name": os.path.basename(path),
                "language": "Desconhecido",
                "framework": "Nenhum",
                "root_path": path,
                "clickup_list_id": "901714169490"
            }, f, indent=2)
            
    brachat_state = os.path.join(path, ".brachat-state.json")
    if not os.path.exists(brachat_state):
        with open(brachat_state, "w") as f:
            json.dump({
                "phase": "backlog",
                "plan_approved": False,
                "tests_passed": False
            }, f, indent=2)
            
    lock_project_files(path, read_only=True)
            
    await update.message.reply_text(
        f"📂 **Projeto Ativo Alterado!**\n"
        f"📌 **Caminho:** `{path}`\n"
        f"⚙️ Arquivos `.brachat` e `.brachat-state.json` inicializados.{hook_msg}\n"
        f"🔒 Arquivos de código marcados como Read-Only."
    )

async def status_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    active_path = "/Users/mac/brachat-main/active_project.json"
    if not os.path.exists(active_path):
        await update.message.reply_text("⚠️ Nenhum projeto ativo configurado. Use `/switch <caminho>`.")
        return
        
    with open(active_path, "r") as f:
        data = json.load(f)
    path = data.get("active_project_path")
    
    brachat_conf = os.path.join(path, ".brachat")
    brachat_state = os.path.join(path, ".brachat-state.json")
    
    if not os.path.exists(brachat_conf) or not os.path.exists(brachat_state):
        await update.message.reply_text(f"⚠️ Arquivos de configuração não encontrados no diretório ativo `{path}`.")
        return
        
    with open(brachat_conf, "r") as f:
        conf = json.load(f)
    with open(brachat_state, "r") as f:
        state = json.load(f)
        
    msg = (
        f"📂 **Status do Projeto Ativo**\n\n"
        f"👤 **Nome:** {conf.get('project_name')}\n"
        f"📍 **Diretório:** `{path}`\n"
        f"🎯 **Linguagem:** {conf.get('language')} | **Framework:** {conf.get('framework')}\n\n"
        f"⚙️ **Fase Atual:** `{state.get('phase', 'backlog').upper()}`\n"
        f"📋 **Plano Aprovado:** {'✅ Sim' if state.get('plan_approved') else '❌ Não'}\n"
        f"🧪 **Testes Passaram:** {'✅ Sim' if state.get('tests_passed') else '❌ Não'}"
    )
    await update.message.reply_text(msg)

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
    
    global chat_history
    chat_history.append({"role": "user", "parts": [{"text": text}]})
    if len(chat_history) > 20:
        chat_history = chat_history[-20:]
        
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    if not GOOGLE_API_KEY:
        await update.message.reply_text("⚠️ Erro: GOOGLE_API_KEY nao configurada localmente!")
        return
        
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
    
    import asyncio
    import requests
    
    try:
        response = await asyncio.to_thread(requests.post, url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            try:
                reply = data["candidates"][0]["content"]["parts"][0]["text"]
                chat_history.append({"role": "model", "parts": [{"text": reply}]})
                
                try:
                    await update.message.reply_text(reply, parse_mode="Markdown")
                except Exception as parse_err:
                    logger.warning(f"Falha ao enviar com Markdown, tentando texto puro: {parse_err}")
                    await update.message.reply_text(reply)
            except (KeyError, IndexError) as parse_err:
                logger.error(f"Erro ao parsear resposta do Gemini: {parse_err}. JSON: {data}")
                await update.message.reply_text("⚠️ Ocorreu um erro ao processar a resposta da IA.")
        else:
            logger.error(f"Erro no Gemini API: Status {response.status_code}. Detalhes: {response.text}")
            await update.message.reply_text(f"⚠️ Erro de API do Gemini: {response.status_code}")
    except Exception as e:
        logger.error(f"Erro ao chamar Gemini: {str(e)}")
        await update.message.reply_text(f"⚠️ Ocorreu um erro na comunicação: {str(e)}")

async def trabalhar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    if not context.args:
        await update.message.reply_text("⚠️ Uso: /trabalhar <instrução de desenvolvimento>")
        return
        
    text = " ".join(context.args)
    
    active_path = "/Users/mac/brachat-main/active_project.json"
    if not os.path.exists(active_path):
        await update.message.reply_text("⚠️ Nenhum projeto ativo configurado. Use `/switch <caminho>` primeiro.")
        return
        
    with open(active_path, "r") as f:
        data = json.load(f)
    project_path = data.get("active_project_path")
    
    brachat_conf = os.path.join(project_path, ".brachat")
    if not os.path.exists(brachat_conf):
        await update.message.reply_text("⚠️ Erro: Arquivo .brachat não encontrado na raiz do projeto ativo.")
        return
        
    with open(brachat_conf, "r") as f:
        conf = json.load(f)
        
    list_id = conf.get("clickup_list_id", "901714169490")
    clickup_key = os.environ.get("CLICKUP_API_KEY")
    
    if not clickup_key:
        await update.message.reply_text("⚠️ Erro: CLICKUP_API_KEY não configurada!")
        return
        
    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        "Authorization": clickup_key,
        "Content-Type": "application/json"
    }
    payload = {
        "name": f"📥 [{conf.get('project_name')}] {text[:30]}...",
        "description": f"Instrução: {text}\n\nProjeto: {conf.get('project_name')}\nCaminho: {project_path}",
        "status": "to do",
        "tags": ["brachat_researcher"]
    }
    
    import requests
    import asyncio
    
    try:
        res = await asyncio.to_thread(requests.post, url, headers=headers, json=payload, timeout=15)
        if res.status_code in [200, 201]:
            task_data = res.json()
            task_id = task_data.get("id")
            
            state_path = os.path.join(project_path, ".brachat-state.json")
            with open(state_path, "w") as f:
                json.dump({
                    "active_task_id": task_id,
                    "active_task_name": task_data.get("name"),
                    "phase": "researcher",
                    "plan_approved": False,
                    "tests_passed": False
                }, f, indent=2)
                
            await update.message.reply_text(
                f"🚀 **Fábrica de Software Iniciada!**\n"
                f"📥 **Tarefa:** [{task_data.get('name')}]({task_data.get('url')})\n"
                f"🔍 **Fase Atual:** `RESEARCHER` (Pesquisa técnica ativa localmente)..."
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
    app.add_handler(CommandHandler("clear", clear_history))
    app.add_handler(CommandHandler("switch", switch_project))
    app.add_handler(CommandHandler("status_projeto", status_project))
    app.add_handler(CommandHandler("trabalhar", trabalhar))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("git", git_status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app

if __name__ == "__main__":
    logger.info("Iniciando Hermes Telegram Bot de forma isolada...")
    app = get_app()
    app.run_polling()
