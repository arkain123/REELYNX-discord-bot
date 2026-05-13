import sys
from datetime import datetime
from typing import Optional
import os
from pathlib import Path

# ANSI цвета (только для консоли, в файл не пишем)
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

# Уровни логирования
LOG_LEVELS = {
    'debug': 10,
    'info': 20,
    'notice': 25,
    'warning': 30,
    'error': 40,
    'critical': 50,
}

# Определяем, запущены ли мы под systemd
IS_SYSTEMD = 'JOURNAL_STREAM' in os.environ or 'INVOCATION_ID' in os.environ

# Получаем уровень из .env
_current_level = os.getenv('LOG_LEVEL', 'INFO').lower()
CURRENT_LOG_LEVEL = LOG_LEVELS.get(_current_level, 20)

# Получаем путь к файлу лога из .env
LOG_FILE = os.getenv('LOG_FILE', '/var/log/bot.log')

# Создаем директорию для лога если её нет
if LOG_FILE:
    log_path = Path(LOG_FILE)
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        # Проверяем доступность файла
        with open(LOG_FILE, 'a') as f:
            f.write(f"=== Log started at {datetime.now().isoformat()} ===\n")
    except Exception as e:
        print(f"⚠️ Cannot create log file {LOG_FILE}: {e}")
        LOG_FILE = None

# Иконки для разных типов
ICONS = {
    'debug': '🔍',
    'info': 'ℹ️',
    'notice': '📘',
    'warning': '⚠️',
    'error': '❌',
    'success': '✅',
    'critical': '💀',
}


def write_to_file(message: str, level: str, error: Optional[Exception] = None):
    """Запись лога в файл без ANSI кодов"""
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


def log(message: str, level: str = 'notice', error: Optional[Exception] = None):
    """
    Универсальная функция логирования
    """
    level = level.lower()

    # Проверяем уровень логирования
    level_value = LOG_LEVELS.get(level, 25)
    if level_value < CURRENT_LOG_LEVEL:
        return

    # Записываем в файл
    write_to_file(message, level, error)

    # Формируем вывод для консоли/stderr
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    microseconds = datetime.now().strftime('%f')[:3]

    # Если под systemd, не используем ANSI цвета
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

        # Пишем в stderr для systemd (journald)
        print(console_output, file=sys.stderr)
    else:
        # Интерактивный режим
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

    if level == 'critical':
        sys.exit(1)


class ExceptionHandler:
    """Класс для обработки исключений в командах"""

    @staticmethod
    async def handle_command_error(ctx: dict, error: Exception):
        """Обработка ошибок выполнения команд"""
        message = ctx.get('message')
        command = ctx.get('command', 'unknown')

        log(f'Ошибка в команде {command}: {error}', 'error', error)

        if message:
            await message.channel.send(f'❌ Ошибка выполнения команды `{command}`')
            if CURRENT_LOG_LEVEL <= 10:
                await message.channel.send(f'```py\n{error}\n```')