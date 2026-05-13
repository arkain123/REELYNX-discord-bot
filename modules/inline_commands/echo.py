from discord import Interaction, app_commands
from .base import InlineCommand


class EchoCommand(InlineCommand):
    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Повторяет ваш текст"

    @app_commands.describe(text="Текст для повтора")
    async def callback(self, interaction: Interaction, text: str) -> None:
        await interaction.response.send_message(text)