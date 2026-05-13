import discord
from typing import Optional, Union
from modules.handlers.exception_handler import log

class ChannelManager:
    """Управление каналами (текстовыми, голосовыми, категориями)"""

    # ---------- СОЗДАНИЕ ----------
    @staticmethod
    async def create_text(
        guild: discord.Guild,
        name: str,
        category: Optional[discord.CategoryChannel] = None,
        topic: str = None,
        slowmode_delay: int = 0,
        nsfw: bool = False
    ) -> discord.TextChannel:
        try:
            channel = await guild.create_text_channel(
                name=name,
                category=category,
                topic=topic,
                slowmode_delay=slowmode_delay,
                nsfw=nsfw
            )
            log(f"Создан текстовый канал #{channel.name} на сервере {guild.name}", "info")
            return channel
        except discord.Forbidden:
            log(f"Недостаточно прав для создания текстового канала на сервере {guild.name}", "error")
            raise PermissionError("❌ Нет прав на создание текстового канала")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при создании канала: {e}", "error")
            raise RuntimeError(f"❌ Ошибка создания канала: {e}")

    @staticmethod
    async def create_voice(
        guild: discord.Guild,
        name: str,
        category: Optional[discord.CategoryChannel] = None,
        bitrate: int = 64000,
        user_limit: int = 0
    ) -> discord.VoiceChannel:
        try:
            channel = await guild.create_voice_channel(
                name=name,
                category=category,
                bitrate=bitrate,
                user_limit=user_limit
            )
            log(f"Создан голосовой канал {channel.name} на сервере {guild.name}", "info")
            return channel
        except discord.Forbidden:
            log(f"Недостаточно прав для создания голосового канала на сервере {guild.name}", "error")
            raise PermissionError("❌ Нет прав на создание голосового канала")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при создании голосового канала: {e}", "error")
            raise RuntimeError(f"❌ Ошибка создания канала: {e}")

    @staticmethod
    async def create_category(
        guild: discord.Guild,
        name: str,
        position: Optional[int] = None
    ) -> discord.CategoryChannel:
        try:
            category = await guild.create_category(name=name)
            if position is not None:
                await category.edit(position=position)
            log(f"Создана категория {category.name} на сервере {guild.name}", "info")
            return category
        except discord.Forbidden:
            log(f"Недостаточно прав для создания категории на сервере {guild.name}", "error")
            raise PermissionError("❌ Нет прав на создание категории")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при создании категории: {e}", "error")
            raise RuntimeError(f"❌ Ошибка создания категории: {e}")

    # ---------- УДАЛЕНИЕ ----------
    @staticmethod
    async def delete(channel: Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]) -> bool:
        guild_name = channel.guild.name if channel.guild else "Unknown"
        try:
            await channel.delete()
            log(f"Удалён канал {channel.name} на сервере {guild_name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для удаления канала {channel.name} на сервере {guild_name}", "error")
            raise PermissionError("❌ Нет прав на удаление канала")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при удалении канала: {e}", "error")
            raise RuntimeError(f"❌ Ошибка удаления: {e}")

    # ---------- РЕДАКТИРОВАНИЕ ----------
    @staticmethod
    async def rename(channel: Union[discord.TextChannel, discord.VoiceChannel], new_name: str) -> bool:
        old_name = channel.name
        guild_name = channel.guild.name if channel.guild else "Unknown"
        try:
            await channel.edit(name=new_name)
            log(f"Канал {old_name} переименован в {new_name} на сервере {guild_name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для переименования канала {old_name} на сервере {guild_name}", "error")
            raise PermissionError("❌ Нет прав на переименование")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при переименовании: {e}", "error")
            raise RuntimeError(f"❌ Ошибка переименования: {e}")

    @staticmethod
    async def set_category(
        channel: Union[discord.TextChannel, discord.VoiceChannel],
        category: Optional[discord.CategoryChannel]
    ) -> bool:
        guild_name = channel.guild.name if channel.guild else "Unknown"
        try:
            await channel.edit(category=category)
            log(f"Канал {channel.name} перемещён в категорию {category.name if category else 'None'} на сервере {guild_name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения категории канала {channel.name}", "error")
            raise PermissionError("❌ Нет прав на перемещение в категорию")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def set_position(channel: Union[discord.TextChannel, discord.VoiceChannel], position: int) -> bool:
        try:
            await channel.edit(position=position)
            log(f"Позиция канала {channel.name} изменена на {position}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения позиции канала {channel.name}", "error")
            raise PermissionError("❌ Нет прав на изменение позиции")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")