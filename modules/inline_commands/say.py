from discord import Interaction, app_commands
from .base import InlineCommand


class SayCommand(InlineCommand):
    @property
    def name(self) -> str:
        return "say"

    @property
    def description(self) -> str:
        return "Бот скажет текст"

    @app_commands.describe(
        text="Текст который скажет бот",
        ephemeral="Показать только вам"
    )
    async def callback(self, interaction: Interaction, text: str, ephemeral: bool = False) -> None:
        await interaction.response.send_message(text, ephemeral=ephemeral)