import sys
import asyncio
import discord
from datetime import datetime
from typing import Optional
import os
from pathlib import Path

# ANSI цвета (только для консоли)
COLORS = {
    'debug': '\033[90m',
    'info': '\033[94m',
    'notice': '\033[96m',
    'warning': '\033[93m',
    'error': '\033[91m',
    'success': '\033[92m',
    'critical': '\033[95m',
    'bold': '\033[1m',
    'reset': '\033[0m',
}

LOG_LEVELS = {
    'debug': 10,
    'info': 20,
    'notice': 25,
    'warning': 30,
    'error': 40,
    'critical': 50,
}

IS_SYSTEMD = 'JOURNAL_STREAM' in os.environ or 'INVOCATION_ID' in os.environ

_current_level = os.getenv('LOG_LEVEL', 'INFO').lower()
CURRENT_LOG_LEVEL = LOG_LEVELS.get(_current_level, 20)

LOG_FILE = os.getenv('LOG_FILE', '/var/log/bot.log')
if LOG_FILE:
    log_path = Path(LOG_FILE)
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(f"=== Log started at {datetime.now().isoformat()} ===\n")
    except Exception as e:
        print(f"⚠️ Cannot create log file {LOG_FILE}: {e}")
        LOG_FILE = None

LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID')
if LOG_CHANNEL_ID:
    try:
        LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)
    except ValueError:
        LOG_CHANNEL_ID = None

ICONS = {
    'debug': '🔍',
    'info': 'ℹ️',
    'notice': '📘',
    'warning': '⚠️',
    'error': '❌',
    'success': '✅',
    'critical': '💀',
}

LEVEL_COLORS = {
    'debug': 0x808080,
    'info': 0x3498db,
    'notice': 0x2ecc71,
    'warning': 0xf1c40f,
    'error': 0xe74c3c,
    'success': 0x2ecc71,
    'critical': 0x992d22,
}


def write_to_file(message: str, level: str, error: Optional[Exception] = None):
    if not LOG_FILE:
        return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    microseconds = datetime.now().strftime('%f')[:3]
    icon = ICONS.get(level, '📌')
    file_output = f"[{timestamp}.{microseconds}] {icon} [{level.upper()}] {message}"
    if error:
        file_output += f"\n  └─ Ошибка: {str(error)}"
        if level == 'critical':
            import traceback
            tb = traceback.format_exc()
            if tb and tb != 'NoneType: None\n':
                file_output += f"\n  └─ Traceback:\n{tb}"
    file_output += "\n"
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(file_output)
            f.flush()
    except Exception as e:
        print(f"⚠️ Cannot write to log file {LOG_FILE}: {e}", file=sys.stderr)


async def _send_discord_log(message: str, level: str, error: Optional[Exception] = None):
    if not LOG_CHANNEL_ID:
        return
    from modules.services.message_manager import MessageManager
    global _bot
    if _bot is None:
        return
    channel = _bot.get_channel(LOG_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.TextChannel):
        return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    icon = ICONS.get(level, '📌')
    title = f"{icon} {level.upper()}"
    color = LEVEL_COLORS.get(level, 0x3498db)
    description = message
    if error:
        description += f"\n```py\n{str(error)}\n```"
    await MessageManager.send_embed(
        channel=channel,
        title=title,
        description=description,
        color=discord.Color(color),
        timestamp=timestamp,
        footer="REELYNX Log System"
    )


_bot = None

def set_bot(bot):
    global _bot
    _bot = bot


def log(message: str, level: str = 'notice', error: Optional[Exception] = None):
    level = level.lower()
    level_value = LOG_LEVELS.get(level, 25)
    if level_value < CURRENT_LOG_LEVEL:
        return

    write_to_file(message, level, error)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    microseconds = datetime.now().strftime('%f')[:3]
    if IS_SYSTEMD:
        icon = ICONS.get(level, '📌')
        console_output = f"[{timestamp}.{microseconds}] {icon} [{level.upper()}] {message}"
        if error:
            console_output += f"\n  └─ Error: {str(error)}"
            if level == 'critical':
                import traceback
                tb = traceback.format_exc()
                if tb and tb != 'NoneType: None\n':
                    console_output += f"\n  └─ Traceback:\n{tb}"
        print(console_output, file=sys.stderr)
    else:
        output = [f"{COLORS['bold']}[{timestamp}.{microseconds}]{COLORS['reset']}"]
        icon = ICONS.get(level, '📌')
        color = COLORS.get(level, COLORS['notice'])
        output.append(f"{color}{icon} [{level.upper()}]{COLORS['reset']}")
        output.append(f"{COLORS['bold']}{message}{COLORS['reset']}")
        if error:
            output.append(f"\n  {COLORS['error']}└─ Ошибка: {str(error)}{COLORS['reset']}")
            if level == 'critical':
                import traceback
                tb = traceback.format_exc()
                if tb and tb != 'NoneType: None\n':
                    output.append(f"  {COLORS['error']}└─ Traceback:{COLORS['reset']}")
                    for line in tb.split('\n'):
                        if line.strip():
                            output.append(f"    {COLORS['debug']}{line}{COLORS['reset']}")
        print(' '.join(output))

    # Отправка в Discord только если есть running loop
    if LOG_CHANNEL_ID and _bot:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop is not None:
            asyncio.create_task(_send_discord_log(message, level, error))

    if level == 'critical':
        sys.exit(1)


class ExceptionHandler:
    @staticmethod
    async def handle_command_error(ctx: dict, error: Exception):
        message = ctx.get('message')
        command = ctx.get('command', 'unknown')
        log(f'Ошибка в команде {command}: {error}', 'error', error)
        if message:
            await message.channel.send(f'❌ Ошибка выполнения команды `{command}`')
            if CURRENT_LOG_LEVEL <= 10:
                await message.channel.send(f'```py\n{error}\n```')