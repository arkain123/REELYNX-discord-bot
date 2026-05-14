import discord
from typing import Optional

class MessageManager:
    """Управление отправкой сообщений в Discord (обычные и embed-щитки)"""

    @staticmethod
    async def send_embed(
        channel: discord.TextChannel,
        title: str,
        description: str,
        color: discord.Color,
        timestamp: Optional[str] = None,
        footer: Optional[str] = None
    ):
        """Отправляет embed-сообщение (щиток)"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        if timestamp:
            embed.timestamp = discord.utils.utcnow()
            embed.add_field(name="🕒 Время", value=timestamp, inline=False)
        if footer:
            embed.set_footer(text=footer)
        await channel.send(embed=embed)

    @staticmethod
    async def send_simple(channel: discord.TextChannel, content: str):
        """Отправляет обычное текстовое сообщение"""
        await channel.send(content)

    @staticmethod
    async def send_error(channel: discord.TextChannel, error_text: str):
        """Отправляет сообщение об ошибке (красный щиток)"""
        embed = discord.Embed(
            title="❌ Ошибка",
            description=error_text,
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

    @staticmethod
    async def send_success(channel: discord.TextChannel, text: str):
        """Отправляет сообщение об успехе (зелёный щиток)"""
        embed = discord.Embed(
            title="✅ Успех",
            description=text,
            color=discord.Color.green()
        )
        await channel.send(embed=embed)

    @staticmethod
    async def send_warning(channel: discord.TextChannel, text: str):
        """Отправляет предупреждение (жёлтый щиток)"""
        embed = discord.Embed(
            title="⚠️ Внимание",
            description=text,
            color=discord.Color.yellow()
        )
        await channel.send(embed=embed)

    @staticmethod
    async def send_info(channel: discord.TextChannel, text: str):
        """Отправляет информационное сообщение (синий щиток)"""
        embed = discord.Embed(
            title="ℹ️ Информация",
            description=text,
            color=discord.Color.blue()
        )
        await channel.send(embed=embed)