import discord
from discord.ext import commands
from discord import Embed, ButtonStyle, Color, ui, InteractionType, Forbidden, Message, File, HTTPException, TextChannel
from discord import ApplicationContext,Option

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_message_declension(self, count):
        """Функция для склонения слова 'сообщение' в зависимости от количества."""
        if 11 <= count % 100 <= 19:
            return "сообщений"
        else:
            cases = {1: "сообщение", 2: "сообщения", 3: "сообщения", 4: "сообщения"}
            return cases.get(count % 10, "сообщений")

    def get_time_declension(self, amount, unit):
        """Возвращает слово с правильным склонением для единицы времени."""
        declensions = {
            "s": ["секунда", "секунды", "секунд"],
            "m": ["минута", "минуты", "минут"],
            "h": ["час", "часа", "часов"],
            "d": ["день", "дня", "дней"],
            "w": ["неделя", "недели", "недель"]
        }
        if 11 <= amount % 100 <= 19:
            return declensions[unit][2]
        elif amount % 10 == 1:
            return declensions[unit][0]
        elif 2 <= amount % 10 <= 4:
            return declensions[unit][1]
        else:
            return declensions[unit][2]

    def parse_time_string(self, time_string):
        """Разбирает строку времени и возвращает timedelta и описание времени."""
        time_matches = re.findall(r"(\d+)([smhdw])", time_string)
        total_delta = timedelta()
        time_description = []

        time_units = {
            "s": "seconds",
            "m": "minutes",
            "h": "hours",
            "d": "days",
            "w": "weeks",
        }

        for amount, unit in time_matches:
            amount = int(amount)
            unit_plural = self.get_time_declension(amount, unit)
            time_description.append(f"{amount} {unit_plural}")
            total_delta += timedelta(**{time_units[unit]: amount})

        return total_delta, " и ".join(time_description)

    @commands.slash_command(name="clear", description="Удаляет сообщения в чате")
    async def clear_messages(self,
                             ctx: ApplicationContext,
                             user: Option(discord.User, "Пользователь", required=False),
                             amount: Option(int, "Количество сообщений (Макс. 150)", required=False, max_value=150),
                             time: Option(str, "За какое время удалить (1s|m|h|d|w и т.д.)", required=False)):
        if not (ctx.author.guild_permissions.manage_messages or ctx.author.id == ctx.guild.owner_id):
            await ctx.respond("У вас нет прав на удаление сообщений.", ephemeral=True)
            return
        log = self.bot.get_cog("SendLog")
        channel = ctx.channel
        await ctx.defer(ephemeral=True)

        log_lines = []  # Хранилище для логов удалённых сообщений

        if amount:
            deleted_count = 0
            async for message in channel.history(limit=150):
                if user and message.author != user:
                    continue
                try:
                    log_lines.append(
                        f"{message.author} | {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} | {message.content}\n")
                    await message.delete()
                    deleted_count += 1
                    if deleted_count >= amount:
                        break
                except Forbidden:
                    continue

            declension = self.get_message_declension(deleted_count)
            if deleted_count > 0:
                log_file_path = f"log_messages/message_{channel.id}.log"
                with open(log_file_path, "w", encoding="utf-8") as log_file:
                    log_file.writelines(log_lines)

                embed = Embed(title="Сообщения удалены", color=0x7b68ee)
                embed.add_field(name="Автор команды", value=ctx.author.mention, inline=False)
                embed.add_field(name="Канал", value=channel.mention, inline=True)
                embed.add_field(name="Количество", value=deleted_count, inline=True)

                if user:
                    embed.add_field(name="Пользователь", value=user.mention, inline=False)

                await log.send_log(ctx.guild.id, embed=embed, log_file_path=log_file_path)

            await ctx.followup.send(f"Удалено {deleted_count} {declension}.", ephemeral=True)
            return

        if time:
            time_delta, time_description = self.parse_time_string(time)
            cutoff_time = datetime.now(timezone.utc) - time_delta
        else:
            time_description = "за последние 7 дней"
            cutoff_time = datetime.now(timezone.utc) - timedelta(days=7)

        messages = await channel.history(limit=100).flatten()
        filtered_messages = []
        for message in messages:
            if message.created_at >= cutoff_time:
                if user and message.author != user:
                    continue
                filtered_messages.append(message)

        deleted_count = 0
        for message in filtered_messages:
            try:
                log_lines.append(
                    f"{message.author} | {message.created_at.strftime('%Y-%m-%d %H:%M:%S')} | {message.content}\n")
                await message.delete()
                deleted_count += 1
            except Forbidden:
                continue

        declension = self.get_message_declension(deleted_count)

        if deleted_count > 0:
            log_file_path = f"../log_messages/message_{channel.id}.log"
            with open(log_file_path, "w", encoding="utf-8") as log_file:
                log_file.writelines(log_lines)

            embed = Embed(title="Сообщения удалены", color=0x7b68ee)
            embed.add_field(name="Автор команды", value=ctx.author.mention, inline=False)
            embed.add_field(name="Канал", value=channel.mention, inline=True)
            embed.add_field(name="Количество", value=deleted_count, inline=True)
            embed.add_field(name="Период", value=time_description, inline=True)

            if user:
                embed.add_field(name="Пользователь", value=user.mention, inline=False)

            await log.send_log(ctx.guild.id, embed=embed, log_file_path=log_file_path)

        await ctx.followup.send(f"Удалено {deleted_count} {declension} за {time_description}.", ephemeral=True)

def setup(bot):
    bot.add_cog(Clear(bot))