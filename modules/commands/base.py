from typing import List, Dict, Any
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

load_dotenv()


class BaseCommand(ABC):
    """Базовый класс для всех префиксных команд"""

    @property
    def prefix(self) -> str:
        """Префикс из .env"""
        return os.getenv('PREFIX', '!')

    @property
    @abstractmethod
    def name(self) -> str:
        """Имя команды"""
        pass

    @property
    def aliases(self) -> List[str]:
        """Алиасы команды"""
        return []

    @property
    def description(self) -> str:
        """Описание команды"""
        return "Нет описания"

    @property
    def usage(self) -> str:
        """Пример использования"""
        return f"{self.prefix}{self.name}"

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> None:
        """Выполнение команды"""
        pass