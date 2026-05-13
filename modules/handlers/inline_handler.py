from typing import Dict, Any
from discord import app_commands, Interaction
from modules.handlers.exception_handler import log


class InlineCommandHandler:
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree
        self.commands: Dict[str, Any] = {}

    def register(self, cmd_instance) -> None:
        """Регистрирует команду с сохранением всех декораторов"""
        if not self.tree:
            log('Tree не инициализирован', 'error')
            return

        self.commands[cmd_instance.name] = cmd_instance

        # Создаем команду и регистрируем callback
        self.tree.command(
            name=cmd_instance.name,
            description=cmd_instance.description
        )(cmd_instance.callback)

        log(f'Зарегистрирована слеш-команда: /{cmd_instance.name}', 'info')

    def register_all(self, commands: list) -> None:
        for cmd_instance in commands:
            self.register(cmd_instance)

    async def sync(self) -> None:
        if not self.tree:
            log('Tree не инициализирован', 'error')
            return

        try:
            synced = await self.tree.sync()
            log(f'Синхронизировано {len(synced)} слеш-команд', 'success')
            for cmd in synced:
                # Получаем параметры через options
                params = [opt.name for opt in cmd.options] if hasattr(cmd, 'options') else []
                param_text = f" ({', '.join(params)})" if params else ""
                log(f'  /{cmd.name}{param_text} - {cmd.description}', 'debug')
        except Exception as e:
            log(f'Ошибка синхронизации: {e}', 'error')