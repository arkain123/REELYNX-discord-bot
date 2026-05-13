import discord
from typing import Optional
from modules.handlers.exception_handler import log

class RoleManager:
    """Управление ролями (создание, удаление, редактирование, выдача/снятие)"""

    @staticmethod
    async def create(
        guild: discord.Guild,
        name: str,
        color: discord.Color = discord.Color.default(),
        permissions: discord.Permissions = None,
        hoist: bool = False,
        mentionable: bool = False,
        reason: str = None
    ) -> discord.Role:
        try:
            role = await guild.create_role(
                name=name,
                color=color,
                permissions=permissions,
                hoist=hoist,
                mentionable=mentionable,
                reason=reason
            )
            log(f"Создана роль {role.name} на сервере {guild.name}", "info")
            return role
        except discord.Forbidden:
            log(f"Недостаточно прав для создания роли на сервере {guild.name}", "error")
            raise PermissionError("❌ Нет прав на создание роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при создании роли: {e}", "error")
            raise RuntimeError(f"❌ Ошибка создания роли: {e}")

    @staticmethod
    async def delete(role: discord.Role, reason: str = None) -> bool:
        guild_name = role.guild.name
        try:
            await role.delete(reason=reason)
            log(f"Роль {role.name} удалена на сервере {guild_name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для удаления роли {role.name} на сервере {guild_name}", "error")
            raise PermissionError("❌ Нет прав на удаление роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при удалении роли: {e}", "error")
            raise RuntimeError(f"❌ Ошибка удаления: {e}")

    @staticmethod
    async def rename(role: discord.Role, new_name: str, reason: str = None) -> bool:
        old_name = role.name
        guild_name = role.guild.name
        try:
            await role.edit(name=new_name, reason=reason)
            log(f"Роль {old_name} переименована в {new_name} на сервере {guild_name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для переименования роли {old_name}", "error")
            raise PermissionError("❌ Нет прав на переименование роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при переименовании роли: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def set_color(role: discord.Role, color: discord.Color, reason: str = None) -> bool:
        try:
            await role.edit(color=color, reason=reason)
            log(f"Цвет роли {role.name} изменён на {color} на сервере {role.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения цвета роли {role.name}", "error")
            raise PermissionError("❌ Нет прав на изменение цвета")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def set_permissions(role: discord.Role, permissions: discord.Permissions, reason: str = None) -> bool:
        try:
            await role.edit(permissions=permissions, reason=reason)
            log(f"Права роли {role.name} обновлены на сервере {role.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения прав роли {role.name}", "error")
            raise PermissionError("❌ Нет прав на изменение прав роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def set_position(role: discord.Role, position: int, reason: str = None) -> bool:
        try:
            await role.edit(position=position, reason=reason)
            log(f"Позиция роли {role.name} изменена на {position} на сервере {role.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для изменения позиции роли {role.name}", "error")
            raise PermissionError("❌ Нет прав на изменение позиции")
        except discord.HTTPException as e:
            log(f"Ошибка Discord: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")