import importlib
import inspect
from pathlib import Path
from typing import Dict
from modules.handlers.exception_handler import log


class CommandLoader:
    """Загрузчик префиксных команд из папки commands"""

    def __init__(self):
        self.commands_package = 'modules.commands'

    def load_commands(self) -> Dict[str, object]:
        """Сканирует папку и возвращает словарь {имя_команды: экземпляр}"""
        commands = {}

        # Путь к папке с командами
        current_dir = Path(__file__).parent.parent
        commands_path = current_dir / 'commands'

        if not commands_path.exists():
            log(f'Папка commands не найдена: {commands_path}', 'warning')
            return commands

        log(f'Поиск команд в: {commands_path}', 'debug')

        # Сканируем все .py файлы
        for file_path in commands_path.glob('*.py'):
            if file_path.name in ['__init__.py', 'base.py']:
                continue

            module_name = file_path.stem

            try:
                # Импортируем модуль
                module = importlib.import_module(f'{self.commands_package}.{module_name}')

                # Импортируем базовый класс
                from modules.commands.base import BaseCommand

                # Ищем классы
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and
                            issubclass(obj, BaseCommand) and
                            obj != BaseCommand):

                        # Создаем экземпляр команды
                        command_instance = obj()
                        commands[command_instance.name] = command_instance

                        # Добавляем алиасы
                        for alias in command_instance.aliases:
                            commands[alias] = command_instance

                        log(f'Найдена команда: {command_instance.name} (алиасы: {command_instance.aliases})', 'debug')

            except Exception as e:
                log(f'Ошибка загрузки {module_name}: {e}', 'error')

        log(f'Загружено префиксных команд: {len(set(cmd.name for cmd in commands.values()))}', 'info')
        return commands