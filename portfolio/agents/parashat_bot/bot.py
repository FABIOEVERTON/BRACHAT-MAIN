import json
import logging
import os
import sys
from datetime import time as dtime
from zoneinfo import ZoneInfo

from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import study

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("parashat")

BASE = os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("America/Sao_Paulo")
TOKEN = os.environ.get("PARASHAT_TELEGRAM_API_KEY") or ""
GROUP_HINT = os.environ.get("YESHIVA_CHAT_ID") or ""
CHAT_FILE = os.path.join(BASE, "chat_ids.json")
MODEL = os.environ.get("LLM_MODEL", "llama-3.3-70b-versatile")
GROQ_KEY = os.environ.get("GROQ_API_KEY") or (__import__("mcp_client").groq_key_from_mcp() or "")


def split_text(text, limit=4000):
    text = text or "."
    chunks, cur = [], ""
    for paragraph in text.split("\n"):
        if len(cur) + len(paragraph) + 1 > limit and cur:
            chunks.append(cur)
            cur = paragraph
        else:
            cur = f"{cur}\n{paragraph}" if cur else paragraph
    if cur:
        chunks.append(cur)
    if not chunks:
        chunks = [text[:limit]]
    return chunks


def load_chat_ids():
    try:
        with open(CHAT_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_chat_ids(data):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def pick_target_chat(chat_ids):
    if GROUP_HINT:
        return GROUP_HINT
    for cid, info in chat_ids.items():
        if isinstance(info, dict) and info.get("type") == "group" and "yeshiva" in (info.get("title") or "").lower():
            return cid
    for cid, info in chat_ids.items():
        if isinstance(info, dict) and info.get("type") == "group":
            return cid
    return None


def record_chat(update):
    chat = update.effective_chat
    if not chat:
        return
    chat_ids = load_chat_ids()
    kind = "group" if chat.type in ("group", "supergroup") else "private"
    chat_ids[str(chat.id)] = {"type": kind, "title": chat.title or ""}
    save_chat_ids(chat_ids)


async def on_my_chat_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat and chat.type in ("group", "supergroup"):
        record_chat(chat)
        log.info("recorded group chat %s (%s)", chat.id, chat.title)


def call_llm(prompt, user_text):
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.4,
        max_tokens=2048,
    )
    return resp.choices[0].message.content


async def generate_and_send(query_hint, target, bot):
    await bot.send_message(chat_id=target, text="Buscando a parasha...")
    parashot = study.fetch_parashot()
    p = study.find_by_query(parashot, query_hint) if query_hint else study.next_parashot(parashot)
    if not p:
        await bot.send_message(
            chat_id=target,
            text="Nao encontrei essa parasha em btf.org.br/parashot/. Tente o nome (ex: Bereshit) ou a data do shabat (ex: 25/10/25).",
        )
        return
    prompt = study.load_prompt()
    user_text = study.build_user_text(p, query_hint)
    log.info("generating study for %s (%s)", p["parasha"], p["data"])
    try:
        text = call_llm(prompt, user_text)
    except Exception as e:
        log.exception("llm error")
        await bot.send_message(chat_id=target, text=f"Erro ao gerar o estudo: {e}")
        return
    header = f"*{p['parasha']}* ({p['data']}) - {p['traducao']}\nTorah: {p['torah']}"
    for chunk in split_text(header + "\n\n" + text):
        await bot.send_message(chat_id=target, text=chunk)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    record_chat(update)
    await update.message.reply_text(
        "Shalom! Sou o motor de estudo da Torah pelo racionalismo judaico.\n"
        "Uso: /parashat <nome ou data>  |  ex: /parashat Bereshit ou /parashat 25/10/25\n"
        "Sem argumento, envio a parasha da semana. Estudos diarios as 09:00 no grupo."
    )


async def cmd_parashat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    record_chat(update)
    query = " ".join(context.args) if context.args else ""
    await generate_and_send(query, update.effective_chat.id, context.bot)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    record_chat(update)
    query = (update.message.text or "").strip()
    await generate_and_send(query, update.effective_chat.id, context.bot)


async def daily_job(context: ContextTypes.DEFAULT_TYPE):
    chat_ids = load_chat_ids()
    target = pick_target_chat(chat_ids)
    if not target:
        log.info("no group chat target yet for daily job")
        return
    await generate_and_send("", target, context.bot)


def main():
    if not TOKEN:
        log.error("PARASHAT_TELEGRAM_API_KEY not set")
        sys.exit(1)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("parashat", cmd_parashat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_my_chat_member))
    app.job_queue.run_daily(daily_job, time=dtime(hour=9, minute=0, tzinfo=TZ), days=tuple(range(7)))
    log.info("parashat bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
