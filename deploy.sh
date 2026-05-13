#!/bin/bash

BRANCH=${1:-main}
COMMIT=${2:-unknown}
BOT_DIR="/home/server/REELYNX-discord-bot"
LOG_FILE="/home/server/deploy-webhook/logs/deploy.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

log "🚀 Deploy started: $BRANCH/$COMMIT"

cd $BOT_DIR || exit 1

# Pull изменения
git fetch origin
git reset --hard origin/$BRANCH

if [ $? -ne 0 ]; then
    log "❌ Git pull failed"
    exit 1
fi

log "✅ Code updated"

# Обновляем зависимости если есть venv
if [ -d "$BOT_DIR/venv" ]; then
    source $BOT_DIR/venv/bin/activate
    pip install -r $BOT_DIR/requirements.txt 2>/dev/null
fi

# Перезапускаем бота
sudo systemctl restart discord-bot

sleep 2

if systemctl is-active --quiet discord-bot; then
    log "✅ Bot restarted successfully"
else
    log "❌ Bot failed to start"
    exit 1
fi

log "🎉 Deploy completed"