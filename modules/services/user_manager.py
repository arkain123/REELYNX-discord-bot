import discord
from datetime import timedelta, datetime
from modules.handlers.exception_handler import log

class UserManager:
    """Управление участниками (перемещение, кик, бан, тайм-аут)"""

    @staticmethod
    async def move_to_voice(member: discord.Member, target_channel: discord.VoiceChannel) -> bool:
        try:
            await member.move_to(target_channel)
            log(f"Участник {member.display_name} перемещён в голосовой канал {target_channel.name} на сервере {member.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для перемещения {member.display_name} на сервере {member.guild.name}", "error")
            raise PermissionError("❌ Нет прав для перемещения участника")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при перемещении {member.display_name}: {e}", "error")
            raise RuntimeError(f"❌ Ошибка Discord: {e}")

    @staticmethod
    async def kick(member: discord.Member, reason: str = None) -> bool:
        try:
            await member.kick(reason=reason)
            log(f"Участник {member.display_name} кикнут с сервера {member.guild.name} (причина: {reason})", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для кика {member.display_name}", "error")
            raise PermissionError("❌ Нет прав на кик")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при кике: {e}", "error")
            raise RuntimeError(f"❌ Ошибка кика: {e}")

    @staticmethod
    async def ban(member: discord.Member, reason: str = None, delete_message_days: int = 0) -> bool:
        try:
            await member.ban(reason=reason, delete_message_days=delete_message_days)
            log(f"Участник {member.display_name} забанен на сервере {member.guild.name} (причина: {reason})", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для бана {member.display_name}", "error")
            raise PermissionError("❌ Нет прав на бан")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при бане: {e}", "error")
            raise RuntimeError(f"❌ Ошибка бана: {e}")

    @staticmethod
    async def unban(guild: discord.Guild, user_id: int, reason: str = None) -> bool:
        try:
            ban_entry = await guild.fetch_ban(discord.Object(id=user_id))
            await guild.unban(ban_entry.user, reason=reason)
            log(f"Пользователь {ban_entry.user} разбанен на сервере {guild.name}", "info")
            return True
        except discord.NotFound:
            log(f"Пользователь с ID {user_id} не найден в банах на сервере {guild.name}", "warning")
            raise ValueError("❌ Пользователь не в бане")
        except discord.Forbidden:
            log(f"Недостаточно прав для разбана на сервере {guild.name}", "error")
            raise PermissionError("❌ Нет прав на разбан")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при разбане: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def timeout(member: discord.Member, duration_seconds: int, reason: str = None) -> bool:
        try:
            until = datetime.utcnow() + timedelta(seconds=duration_seconds) if duration_seconds > 0 else None
            await member.timeout(until, reason=reason)
            if duration_seconds > 0:
                log(f"Участнику {member.display_name} выдан тайм-аут на {duration_seconds} сек на сервере {member.guild.name}", "info")
            else:
                log(f"Тайм-аут снят с {member.display_name} на сервере {member.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для тайм-аута {member.display_name}", "error")
            raise PermissionError("❌ Нет прав на тайм-аут")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при тайм-ауте: {e}", "error")
            raise RuntimeError(f"❌ Ошибка тайм-аута: {e}")

    @staticmethod
    async def add_role(member: discord.Member, role: discord.Role, reason: str = None) -> bool:
        try:
            await member.add_roles(role, reason=reason)
            log(f"Роль {role.name} выдана участнику {member.display_name} на сервере {member.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для выдачи роли {role.name} участнику {member.display_name}", "error")
            raise PermissionError("❌ Нет прав на выдачу роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при выдаче роли: {e}", "error")
            raise RuntimeError(f"❌ Ошибка выдачи роли: {e}")

    @staticmethod
    async def remove_role(member: discord.Member, role: discord.Role, reason: str = None) -> bool:
        try:
            await member.remove_roles(role, reason=reason)
            log(f"Роль {role.name} снята с участника {member.display_name} на сервере {member.guild.name}", "info")
            return True
        except discord.Forbidden:
            log(f"Недостаточно прав для снятия роли {role.name} с {member.display_name}", "error")
            raise PermissionError("❌ Нет прав на снятие роли")
        except discord.HTTPException as e:
            log(f"Ошибка Discord при снятии роли: {e}", "error")
            raise RuntimeError(f"❌ Ошибка снятия роли: {e}")

    # Можно добавить массовую выдачу/снятие
    @staticmethod
    async def add_roles(member: discord.Member, roles: list[discord.Role], reason: str = None) -> bool:
        try:
            await member.add_roles(*roles, reason=reason)
            log(f"Роли {[r.name for r in roles]} выданы участнику {member.display_name}", "info")
            return True
        except Exception as e:
            log(f"Ошибка массовой выдачи ролей: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")

    @staticmethod
    async def remove_roles(member: discord.Member, roles: list[discord.Role], reason: str = None) -> bool:
        try:
            await member.remove_roles(*roles, reason=reason)
            log(f"Роли {[r.name for r in roles]} сняты с участника {member.display_name}", "info")
            return True
        except Exception as e:
            log(f"Ошибка массового снятия ролей: {e}", "error")
            raise RuntimeError(f"❌ Ошибка: {e}")