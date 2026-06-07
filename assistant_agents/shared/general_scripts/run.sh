#!/bin/zsh
set -a
source /Users/mac/brachat-main/Portifolio/builder_agents/scripts/.env
set +a
exec python3 /Users/mac/brachat-main/Portifolio/builder_agents/scripts/telegram-bridge.py
