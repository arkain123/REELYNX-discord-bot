import discord
from typing import Union
from modules.handlers.exception_handler import log

class PermissionManager:
    """Управление правами (overwrites) на каналах"""

    @staticmethod
    async def set_user_permissions(
        channel: Union[discord.VoiceChannel, discord.TextChannel],
        user: discord.Member,
        allow: discord.Permissions = None,
        deny: discord.Permissions = None
    ) -> bool:
        try:
            overwrite = channel.overwrites_for(user)
            if allow:
                for perm, value in allow:
                    if value is True:
                        setattr(overwrite, perm, True)
            if deny:
                for perm, value in deny:
                    if value is True:
                        setattr(overwrite, perm, False)
            await channel.set_permissions(user, overwrite=overwrite)
            log(f"Установлены права для пользователя {user.display_name} на канале {channel.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения прав пользователя {user.display_name} на канале {channel.name}", "error")
            raise PermissionError("❌ Нет прав на изменение прав пользователя")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка установки прав: {e}")

    @staticmethod
    async def set_role_permissions(
        channel: Union[discord.VoiceChannel, discord.TextChannel],
        role: discord.Role,
        allow: discord.Permissions = None,
        deny: discord.Permissions = None
    ) -> bool:
        try:
            overwrite = channel.overwrites_for(role)
            if allow:
                for perm, value in allow:
                    if value is True:
                        setattr(overwrite, perm, True)
            if deny:
                for perm, value in deny:
                    if value is True:
                        setattr(overwrite, perm, False)
            await channel.set_permissions(role, overwrite=overwrite)
            log(f"Установлены права для роли {role.name} на канале {channel.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения прав роли {role.name} на канале {channel.name}", "error")
            raise PermissionError("❌ Нет прав на изменение прав роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка установки прав: {e}")

    @staticmethod
    async def clear_permissions(
        channel: Union[discord.VoiceChannel, discord.TextChannel],
        target: Union[discord.Member, discord.Role]
    ) -> bool:
        try:
            await channel.set_permissions(target, overwrite=None)
            log(f"Очищены права для {target} на канале {channel.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для очистки прав для {target} на канале {channel.name}", "error")
            raise PermissionError("❌ Нет прав на очистку прав")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка очистки прав: {e}")