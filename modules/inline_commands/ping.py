from discord import Interaction
from .base import InlineCommand
import time


class PingCommand(InlineCommand):
    @property
    def name(self) -> str:
        return "ping"

    @property
    def description(self) -> str:
        return "Проверить задержку бота"

    async def callback(self, interaction: Interaction) -> None:
        start = time.perf_counter()
        await interaction.response.send_message("Понг!")
        end = time.perf_counter()
        await interaction.edit_original_response(
            content=f"Понг! ⏱️ {round((end - start) * 1000)}ms"
        )