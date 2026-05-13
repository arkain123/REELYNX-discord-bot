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
log "Current commit: $(git rev-parse HEAD)"
git fetch origin --prune
LATEST_COMMIT=$(git rev-parse origin/$BRANCH)
log "Latest remote commit: $LATEST_COMMIT"
git reset --hard $LATEST_COMMIT
log "New commit: $(git rev-parse HEAD)"

if [ $? -ne 0 ]; then
    log "❌ Git pull failed"
    exit 1
fi

log "✅ Code updated (commit: $(git rev-parse --short HEAD))"

# Обновляем зависимости если есть venv
if [ -d "$BOT_DIR/venv" ]; then
    source $BOT_DIR/venv/bin/activate
    pip install -r $BOT_DIR/requirements.txt 2>/dev/null
    log "📦 Dependencies updated"
fi

# Перезапускаем бота
sudo systemctl restart reelynx-discord-bot

sleep 2

if systemctl is-active --quiet reelynx-discord-bot; then
    log "✅ Bot restarted successfully"
else
    log "❌ Bot failed to start"
    sudo journalctl -u reelynx-discord-bot -n 10 --no-pager >> $LOG_FILE
    exit 1
fi

log "🎉 Deploy completed"