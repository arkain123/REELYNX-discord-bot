from typing import Dict, Callable, Optional, List
from modules.handlers.exception_handler import log


class CommandHandler:
    """Обработчик префиксных команд"""

    def __init__(self, prefix: str = '!', case_sensitive: bool = False):
        self.prefix = prefix
        self.case_sensitive = case_sensitive
        self.commands: Dict[str, Callable] = {}
        self.middlewares: List[Callable] = []
        log(f'CommandHandler инициализирован с префиксом: {prefix}', 'debug')

    def register(self, name: str, aliases: Optional[List[str]] = None):
        """Декоратор для регистрации команды"""
        aliases = aliases or []

        def decorator(func: Callable):
            self.commands[name] = func
            for alias in aliases:
                self.commands[alias] = func
            return func

        return decorator

    def register_all(self, commands: Dict[str, object]) -> None:
        """Регистрирует список команд из словаря"""
        for cmd_name, cmd_instance in commands.items():
            self.register(cmd_name, cmd_instance.aliases)(cmd_instance.execute)
            log(f'Зарегистрирована команда: {cmd_name}', 'debug')

    def add_middleware(self, middleware: Callable):
        """Добавляет middleware"""
        self.middlewares.append(middleware)

    async def handle(self, message):
        """Обработка сообщения"""
        content = message.content

        if not content.startswith(self.prefix):
            return

        raw_command = content[len(self.prefix):]
        parts = raw_command.split()

        if not parts:
            return

        command_name = parts[0] if self.case_sensitive else parts[0].lower()
        args = parts[1:]

        if command_name not in self.commands:
            return

        context = {
            'message': message,
            'command': command_name,
            'args': args,
            'handler': self
        }

        try:
            for middleware in self.middlewares:
                if not await middleware(context):
                    return

            await self.commands[command_name](context)

        except Exception as e:
            log(f'Ошибка выполнения команды {command_name}: {e}', 'error')
            await message.channel.send(f'❌ Ошибка: {e}')