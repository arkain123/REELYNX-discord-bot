import discord
from typing import Dict, Optional
from modules.handlers.exception_handler import log
from .channel_manager import ChannelManager
from .user_manager import UserManager
from .permission_manager import PermissionManager

class PrivateVoiceManager:
    """
    Менеджер приватных голосовых каналов.
    При заходе в определённый канал создаётся личная комната для пользователя.
    При выходе всех участников канал удаляется.
    """
    _instance = None
    _private_channels: Dict[int, int] = {}  # {channel_id: owner_id}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.trigger_channel_ids = []
            self._load_config()
            self._initialized = True

    def _load_config(self):
        import os
        ids_str = os.getenv('PRIVATE_VOICE_CHANNEL_IDS', '')
        if ids_str:
            self.trigger_channel_ids = [int(x.strip()) for x in ids_str.split(',') if x.strip()]
        log(f"Загружены каналы-триггеры для приватных комнат: {self.trigger_channel_ids}", "info")

    def is_trigger_channel(self, channel_id: int) -> bool:
        return channel_id in self.trigger_channel_ids

    async def handle_voice_state(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild = member.guild

        if after.channel and self.is_trigger_channel(after.channel.id):
            existing = self._get_user_private_channel(member)
            if existing:
                if after.channel != existing:
                    await UserManager.move_to_voice(member, existing)
                return

            await self._create_private_channel(member, after.channel.category, after.channel)

        elif before.channel and before.channel.id in self._private_channels:
            owner_id = self._private_channels[before.channel.id]
            if member.id == owner_id:
                remaining = [m for m in before.channel.members if not m.bot]
                if not remaining:
                    await self._delete_private_channel(before.channel)
                else:
                    log(f"Владелец {member.display_name} вышел, но канал не пуст", "debug")
            else:
                log(f"Участник {member.display_name} вышел из чужого приватного канала", "debug")

    async def _create_private_channel(self, member: discord.Member, category: Optional[discord.CategoryChannel], position_anchor: discord.VoiceChannel):
        guild = member.guild
        channel_name = f"🔒 {member.display_name}'s room"

        try:
            new_channel = await ChannelManager.create_voice(
                guild=guild,
                name=channel_name,
                category=category,
                bitrate=position_anchor.bitrate,
                user_limit=0
            )
            await ChannelManager.set_position(new_channel, position_anchor.position + 1)

            owner_perms = discord.Permissions()
            owner_perms.update(manage_channels=True, mute_members=True, deafen_members=True, move_members=True)
            await PermissionManager.set_user_permissions(new_channel, member, allow=owner_perms)

            self._private_channels[new_channel.id] = member.id
            await UserManager.move_to_voice(member, new_channel)

            log(f"Создан приватный канал {new_channel.name} для {member.display_name}", "success")
        except Exception as e:
            log(f"Ошибка создания приватного канала для {member.display_name}: {e}", "error")
            raise

    async def _delete_private_channel(self, channel: discord.VoiceChannel):
        if channel.id not in self._private_channels:
            return
        owner_id = self._private_channels.pop(channel.id)
        log(f"Удаление приватного канала {channel.name} (владелец ID: {owner_id})", "info")
        try:
            await ChannelManager.delete(channel)
        except Exception as e:
            log(f"Ошибка удаления канала {channel.name}: {e}", "error")

    def _get_user_private_channel(self, member: discord.Member) -> Optional[discord.VoiceChannel]:
        for channel_id, owner_id in self._private_channels.items():
            if owner_id == member.id:
                channel = member.guild.get_channel(channel_id)
                if channel:
                    return channel
                else:
                    del self._private_channels[channel_id]
        return None