import discord
from discord.ext import commands
from discord import Embed, abc, ForumChannel, StageChannel, DMChannel, GroupChannel, CategoryChannel, VoiceChannel
import json
import os

LOG_CHANNEL_FILE = 'C:\\Users\\slend\\OneDrive\\OneDrive\\bot\\json\\log_channels.json'


def load_log_channel(guild_id):
    """Загрузка канала для конкретного сервера из JSON файла."""
    try:
        if os.path.exists(LOG_CHANNEL_FILE):
            with open(LOG_CHANNEL_FILE, 'r') as f:
                data = json.load(f)
                return data.get(str(guild_id), {}).get('channel_id')
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка при загрузке канала логов: {e}")
    return None


def save_log_channel(guild_id, channel_id):
    """Сохранение канала для конкретного сервера в JSON файл."""
    try:
        data = {}
        if os.path.exists(LOG_CHANNEL_FILE):
            with open(LOG_CHANNEL_FILE, 'r') as f:
                data = json.load(f)
        data[str(guild_id)] = {'channel_id': channel_id}
        with open(LOG_CHANNEL_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Ошибка при сохранении канала логов: {e}")


class LogCommand(commands.Cog):
    """Ког для управления настройками логирования."""
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="log", description="Установить канал для логирования.")
    async def log(self, ctx, channel: abc.GuildChannel = None):
        """Команда для установки канала для логирования."""
        if isinstance(channel, (StageChannel, DMChannel, GroupChannel, CategoryChannel, VoiceChannel, ForumChannel)):
            await ctx.respond("Сюда нельзя отправлять логи!", ephemeral=True)
            return

        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return

        if ctx.author.guild_permissions.administrator:
            if channel is None:
                current_channel_id = load_log_channel(ctx.guild.id)
                if current_channel_id:
                    await ctx.respond(f"Текущий канал логов: <#{current_channel_id}>", ephemeral=True)
                else:
                    await ctx.respond("Канал для логов не установлен.", ephemeral=True)
                return

            save_log_channel(ctx.guild.id, channel.id)
            await ctx.respond(f"Канал для логов установлен: <#{channel.id}>")
        else:
            await ctx.respond(embed=Embed(description="У вас нет прав для использования этой команды!", color=0x7b68ee),
                              ephemeral=True)


def setup(bot):
    bot.add_cog(LogCommand(bot))
