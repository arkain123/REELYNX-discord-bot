from .base import BaseCommand
from typing import Dict, Any
import time


class PingCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "ping"

    @property
    def description(self) -> str:
        return "Проверить задержку бота"

    async def execute(self, context: Dict[str, Any]) -> None:
        message = context['message']
        start = time.perf_counter()
        await message.channel.send("Понг!")
        end = time.perf_counter()
        await message.channel.send(f"⏱️ {round((end - start) * 1000)}ms")