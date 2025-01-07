from discord import Embed, Color
from discord import Interaction


class PresenceCommand:
    def __init__(self, bot):
        self.bot = bot
        self.setup()

    def setup(self):
        @self.bot.slash_command(name="presence")
        async def find_presence(ctx: Interaction, text: str):
            text = text.lower()
            embed = Embed(title="Поиск активности",
                          description=f"Пользователи с активностью, содержащей '{text}'",
                          color=Color.embed_background())
            if ctx.guild is None:
                await ctx.response.send_message("Для использования этой команды добавьте меня на сервер!",
                                                ephemeral=True)
                return
            if self.bot.user not in ctx.guild.members:
                await ctx.response.send_message("Бот не найден среди участников этого сервера.", ephemeral=True)
                return
            for member in ctx.guild.members:
                if member.activity and member.activity.name:
                    activity_name = member.activity.name.lower()
                    if text in activity_name:
                        embed.add_field(name="", value=f"user: {member.mention}\n{member.activity.name}", inline=False)
            await ctx.response.send_message(embed=embed)


def setup(bot):
    PresenceCommand(bot)
