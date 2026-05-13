from discord import Interaction, app_commands
from .base import InlineCommand


class MultiplyCommand(InlineCommand):
    @property
    def name(self) -> str:
        return "multiply"

    @property
    def description(self) -> str:
        return "Умножает два числа"

    @app_commands.describe(
        a="Первое число",
        b="Второе число"
    )
    async def callback(self, interaction: Interaction, a: int, b: int) -> None:
        result = a * b
        await interaction.response.send_message(f"{a} × {b} = {result}")