from .base import BaseCommand
from typing import Dict, Any


class HelloCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "hello"

    @property
    def aliases(self) -> list:
        return ["hi", "привет"]

    @property
    def description(self) -> str:
        return "Поприветствовать бота"

    async def execute(self, context: Dict[str, Any]) -> None:
        message = context['message']
        await message.channel.send(f'Привет, {message.author.name}! 👋')