import discord
from discord.ext import commands
from commands.log import load_log_channel, save_log_channel


class SendLog(commands.Cog):
    """Ког для отправки логов в указанный канал."""
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, guild_id, message=None, embed=None, log_file_path=None):
        """Отправка логов в заданный канал для конкретного сервера."""
        log_channel_id = load_log_channel(guild_id)
        if log_channel_id is not None:
            channel = self.bot.get_channel(log_channel_id)
            if channel is None:
                print(f"Канал с ID {log_channel_id} не найден.")
                return

            file = None
            if log_file_path:
                try:
                    file = discord.File(log_file_path, filename=f"log_{guild_id}.log")
                except FileNotFoundError:
                    print(f"Файл {log_file_path} не найден.")

            try:
                if message and embed:
                    await channel.send(content=message, embed=embed, file=file)
                elif embed:
                    await channel.send(embed=embed, file=file)
                elif message:
                    await channel.send(content=message, file=file)
            except discord.Forbidden:
                print(f"Недостаточно прав для отправки сообщения в канал {channel.id}.")
            except discord.HTTPException as e:
                print(f"Ошибка HTTP при отправке логов: {e}")
        else:
            print(f"Канал для логов для сервера {guild_id} не установлен.")


def setup(bot):
    bot.add_cog(SendLog(bot))
