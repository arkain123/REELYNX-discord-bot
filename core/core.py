import discord
import os
from dotenv import load_dotenv
from modules.handlers.exception_handler import log, set_bot
from modules.handlers.command_handler import CommandHandler
from modules.handlers.inline_handler import InlineCommandHandler
from modules.loaders.command_loader import CommandLoader
from modules.loaders.inline_loader import InlineCommandLoader
from modules.services.private_voice_manager import PrivateVoiceManager

load_dotenv()


class Core(discord.Client):
    def __init__(self, **options):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, **options)
        set_bot(self)

        # Инициализация компонентов
        self.prefix = os.getenv('PREFIX', '!')
        self.tree = discord.app_commands.CommandTree(self)
        self.command_handler = None
        self.inline_handler = None
        self.private_voice_manager = PrivateVoiceManager()
        self._initialize()

    def _initialize(self):
        """Инициализация бота"""
        # Создаем обработчик команд
        self.command_handler = CommandHandler(prefix=self.prefix)
        self.inline_handler = InlineCommandHandler(self)

        # Загружаем префиксные команды
        loader = CommandLoader()
        commands = loader.load_commands()
        self.command_handler.register_all(commands)

        # Загружаем слеш-команды
        inline_loader = InlineCommandLoader()
        inline_commands = inline_loader.load_commands()
        self.inline_handler.register_all(inline_commands)

        log(f'Ядро инициализировано. Префикс: {self.prefix}', 'info')

    async def on_ready(self):
        """По готовности"""
        log(f'Бот запущен: {self.user}', 'success')
        log(f'Загружено всего команд: {len(self.command_handler.commands)}', 'info')
        await self.inline_handler.sync()

    async def on_message(self, message):
        """Обработка сообщений"""
        if message.author == self.user:
            return

        if self.command_handler:
            await self.command_handler.handle(message)

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        """Обработка изменений голосового состояния — делегируем менеджеру приватных каналов"""
        await self.private_voice_manager.handle_voice_state(member, before, after)

    def run(self, **kwargs):
        """Запуск бота"""
        token = os.getenv('TOKEN')
        if not token:
            log('TOKEN не найден в .env файле', 'critical')
            return
        super().run(token)