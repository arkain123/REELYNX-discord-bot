import discord
from typing import Optional, Union

class Utils:
    """Вспомогательные функции для поиска объектов"""

    @staticmethod
    async def find_channel(guild: discord.Guild, name: str) -> Optional[Union[discord.TextChannel, discord.VoiceChannel]]:
        return discord.utils.get(guild.channels, name=name)

    @staticmethod
    async def find_role(guild: discord.Guild, name: str) -> Optional[discord.Role]:
        return discord.utils.get(guild.roles, name=name)

    @staticmethod
    async def find_member(guild: discord.Guild, name: str) -> Optional[discord.Member]:
        return discord.utils.get(guild.members, name=name)

    @staticmethod
    async def find_category(guild: discord.Guild, name: str) -> Optional[discord.CategoryChannel]:
        return discord.utils.get(guild.categories, name=name)