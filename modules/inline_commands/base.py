from abc import ABC, abstractmethod
from discord import Interaction


class InlineCommand(ABC):
    """Базовый класс для слеш-команд"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    async def callback(self, interaction: Interaction) -> None:
        """Метод который будет вызван. У параметров будут декораторы!"""
        pass