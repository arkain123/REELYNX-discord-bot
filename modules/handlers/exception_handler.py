import sys
from datetime import datetime
from typing import Optional
import os

# ANSI цвета
COLORS = {
    'debug': '\033[90m',  # Серый
    'info': '\033[94m',  # Синий
    'notice': '\033[96m',  # Циан
    'warning': '\033[93m',  # Желтый
    'error': '\033[91m',  # Красный
    'success': '\033[92m',  # Зеленый
    'critical': '\033[95m',  # Пурпурный
    'bold': '\033[1m',  # Жирный
    'reset': '\033[0m',  # Сброс
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

# Получаем уровень из .env
_current_level = os.getenv('LOG_LEVEL', 'INFO').lower()
CURRENT_LOG_LEVEL = LOG_LEVELS.get(_current_level, 20)

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


def log(message: str, level: str = 'notice', error: Optional[Exception] = None):
    """
    Универсальная функция логирования

    Args:
        message: Текст сообщения
        level: Уровень (debug, info, notice, warning, error, success, critical)
        error: Объект исключения (опционально)
    """
    level = level.lower()

    # Проверяем уровень логирования
    level_value = LOG_LEVELS.get(level, 25)
    if level_value < CURRENT_LOG_LEVEL:
        return

    # Формируем временную метку
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    microseconds = datetime.now().strftime('%f')[:3]

    # Собираем вывод
    output = [f"{COLORS['bold']}[{timestamp}.{microseconds}]{COLORS['reset']}"]

    # Иконка и уровень
    icon = ICONS.get(level, '📌')
    color = COLORS.get(level, COLORS['notice'])
    output.append(f"{color}{icon} [{level.upper()}]{COLORS['reset']}")

    # Сообщение
    output.append(f"{COLORS['bold']}{message}{COLORS['reset']}")

    # Информация об ошибке
    if error:
        output.append(f"\n  {COLORS['error']}└─ Ошибка: {str(error)}{COLORS['reset']}")

        # Для критических ошибок показываем полный traceback
        if level == 'critical':
            import traceback
            tb = traceback.format_exc()
            if tb and tb != 'NoneType: None\n':
                output.append(f"  {COLORS['error']}└─ Traceback:{COLORS['reset']}")
                for line in tb.split('\n'):
                    if line.strip():
                        output.append(f"    {COLORS['debug']}{line}{COLORS['reset']}")

    # Выводим в консоль
    print(' '.join(output))

    # Для критических ошибок прерываем выполнение
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
            if CURRENT_LOG_LEVEL <= 10:  # Если debug режим
                await message.channel.send(f'```py\n{error}\n```')