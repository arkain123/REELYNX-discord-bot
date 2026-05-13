import importlib
import inspect
from pathlib import Path
from typing import List
from modules.handlers.exception_handler import log


class InlineCommandLoader:
    """Загрузчик слеш-команд из папки inline_commands"""

    def __init__(self):
        self.commands_package = 'modules.inline_commands'

    def load_commands(self) -> List[object]:
        """Сканирует папку и возвращает список экземпляров команд"""
        commands = []

        # Путь к папке с командами
        current_dir = Path(__file__).parent.parent
        commands_path = current_dir / 'inline_commands'

        if not commands_path.exists():
            log(f'Папка inline_commands не найдена: {commands_path}', 'warning')
            return commands

        log(f'Поиск слеш-команд в: {commands_path}', 'debug')

        # Сканируем все .py файлы
        for file_path in commands_path.glob('*.py'):
            if file_path.name in ['__init__.py', 'base.py']:
                continue

            module_name = file_path.stem

            try:
                # Импортируем модуль
                module = importlib.import_module(f'{self.commands_package}.{module_name}')

                # Импортируем базовый класс
                from modules.inline_commands.base import InlineCommand

                # Ищем классы
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and
                            issubclass(obj, InlineCommand) and
                            obj != InlineCommand):
                        # Создаем экземпляр команды
                        command_instance = obj()
                        commands.append(command_instance)
                        log(f'Найдена слеш-команда: /{command_instance.name}', 'debug')

            except Exception as e:
                log(f'Ошибка загрузки {module_name}: {e}', 'error')

        log(f'Загружено слеш-команд: {len(commands)}', 'info')
        return commands