import discord
import aiohttp
from typing import Optional
from modules.handlers.exception_handler import log

class GuildManager:
    """Управление сервером (имя, иконка, уровень, приглашения, массовый кик)"""

    @staticmethod
    async def set_name(guild: discord.Guild, new_name: str) -> bool:
        try:
            old_name = guild.name
            await guild.edit(name=new_name)
            log(f"Сервер {old_name} переименован в {new_name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения имени сервера {guild.name}", "error")
            raise PermissionError("❌ Нет прав на изменение имени сервера")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def set_icon(guild: discord.Guild, icon_url: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(icon_url) as resp:
                    image_data = await resp.read()
            await guild.edit(icon=image_data)
            log(f"Иконка сервера {guild.name} обновлена", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения иконки сервера {guild.name}", "error")
            raise PermissionError("❌ Нет прав на изменение иконки")
        except Exception as e:
            log(f"Ошибка при загрузке/установке иконки: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def set_verification_level(guild: discord.Guild, level: discord.VerificationLevel) -> bool:
        try:
            await guild.edit(verification_level=level)
            log(f"Уровень верификации сервера {guild.name} изменён на {level}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения уровня верификации на {guild.name}", "error")
            raise PermissionError("❌ Нет прав на изменение уровня верификации")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def create_invite(
        channel: discord.TextChannel,
        max_age: int = 86400,
        max_uses: int = 0,
        temporary: bool = False
    ) -> str:
        try:
            invite = await channel.create_invite(max_age=max_age, max_uses=max_uses, temporary=temporary)
            log(f"Создано приглашение в канал {channel.name} на сервере {channel.guild.name}", "info")
            return invite.url
        except discord.Forbidden:
            log(f"Недостаточно прав для создания приглашения в канале {channel.name}", "error")
            raise PermissionError("❌ Нет прав на создание приглашения")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при создании приглашения: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def prune_members(guild: discord.Guild, days: int = 7, reason: str = None) -> int:
        try:
            pruned = await guild.prune_members(days=days, reason=reason, compute_prune_count=True)
            log(f"Выполнен массовый кик {pruned} участников (неактивны {days} дней) на сервере {guild.name}", "info")
            return pruned
        except discord.Forbidden:
            log(f"Недостаточно прав для массового кика на сервере {guild.name}", "error")
            raise PermissionError("❌ Нет прав на массовый кик")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при массовом кике: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")