from .base import BaseCommand
from typing import Dict, Any


class HelpCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "help"

    @property
    def aliases(self) -> list:
        return ["commands", "команды"]

    @property
    def description(self) -> str:
        return "Показать список команд"

    async def execute(self, context: Dict[str, Any]) -> None:
        message = context['message']
        handler = context['handler']

        # Собираем уникальные команды
        unique_commands = {}
        for cmd_name, cmd_func in handler.commands.items():
            if hasattr(cmd_func, '__self__'):
                cmd = cmd_func.__self__
                if cmd.name not in unique_commands:
                    unique_commands[cmd.name] = cmd

        # Формируем ответ
        prefix = self.prefix
        help_text = f"**📚 Доступные команды (префикс: `{prefix}`):**\n\n"

        for cmd in sorted(unique_commands.values(), key=lambda x: x.name):
            aliases_str = f" (алиасы: {', '.join(cmd.aliases)})" if cmd.aliases else ""
            help_text += f"**{prefix}{cmd.name}**{aliases_str}\n"
            help_text += f"└ {cmd.description}\n"
            help_text += f"└ Использование: `{cmd.usage}`\n\n"

        await message.channel.send(help_text)