# parashat_bot

Telegram bot de estudo da Parashá semanal (Torá), com consulta ao NotebookLM (caderno TORAH_STUDIES).

## Arquivos
- `bot.py` - bot Telegram (telegram bot 8200447454)
- `study.py` - geração do estudo (Groq + NotebookLM com citações [1][2])
- `prompt.txt` - prompt base
- `requirements.txt` - python-telegram-bot 21.10, openai 1.55.3, requests, bs4, tzdata
- `parashat-bot.service` - systemd (EnvironmentFile=bot.env)
- `bot.env.example` - modelo de variáveis (PARASHAT_TELEGRAM_API_KEY, GROQ_API_KEY, YESHIVA_CHAT_ID, LLM_MODEL)

## Setup
```
python3 -m venv venv && venv/bin/pip install -r requirements.txt
cp bot.env.example bot.env  # preencher chaves
sudo cp parashat-bot.service /etc/systemd/system/ && sudo systemctl enable --now parashat-bot
```
Estudo: usa venv/bin/python (deps) + CLI notebooklm (notebooklm-py 0.8.0) para contexto com citações.

## Praxe
Salvar tudo no Google Drive e comitar de lá. Projeto versionado no brachat-main (Drive -> GitHub -> VM).
