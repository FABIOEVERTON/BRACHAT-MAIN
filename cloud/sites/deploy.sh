#!/usr/bin/env bash
set -euo pipefail

# BRACHÁT CLOUD DEPLOY — sobe bridges no VPS
# Uso: scp -r cloud/cloud user@vps:~ && ssh user@vps ./cloud/deploy.sh

REMOTE_USER="${1:-root}"
REMOTE_HOST="${2:-}"

if [ -z "$REMOTE_HOST" ]; then
    # Modo local (roda direto no VPS)
    cd "$(dirname "$0")"
    echo "Instalando bridges BRACHÁT no VPS..."

    # Secrets
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "Preencha o .env com seus tokens e depois rode de novo"
        exit 1
    fi
    source .env

    # Instala Python se precisar
    command -v python3 >/dev/null 2>&1 || apt-get install -y python3

    # Copia scripts
    mkdir -p /opt/brachat
    cp bridge-ezra.py /opt/brachat/
    cp bridge-nice.py /opt/brachat/
    cp clickup-daemon.py /opt/brachat/
    cp .env /opt/brachat/

    # Instala systemd services
    cp *.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable --now brachat-ezra
    systemctl enable --now brachat-nice
    systemctl enable --now brachat-clickup 2>/dev/null || true

    echo "Pronto. Status:"
    systemctl status brachat-ezra --no-pager | head -5
    systemctl status brachat-nice --no-pager | head -5
else
    # Modo remoto
    echo "Enviando para $REMOTE_USER@$REMOTE_HOST..."
    rsync -avz --delete "$(dirname "$0")"/ "$REMOTE_USER@$REMOTE_HOST":~/brachat-cloud/
    echo "Rodando deploy no VPS..."
    ssh "$REMOTE_USER@$REMOTE_HOST" "cd ~/brachat-cloud && bash deploy.sh"
fi
