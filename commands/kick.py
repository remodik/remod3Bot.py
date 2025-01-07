import discord
from discord.ext import commands
from discord import Option, Embed, Color, Forbidden, Member


class KickCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="kick", description="Кикнуть пользователя")
    async def _kick(self, ctx, user: Option(Member, description="Кого кикнуть"),
                    reason: Option(str, description="Причина кика", default=False)):
        log = self.bot.get_cog("SendLog")
        if not ctx.author.guild_permissions.kick_members:
            return
        if user == ctx.author:
            await ctx.respond(embed=Embed(title="",
                                          description="Вы не можете кикнуть себя!", color=Color.red()), ephemeral=True)
        else:
            try:
                if ctx.author.top_role > user.top_role or ctx.author.id == ctx.guild.owner_id:
                    try:
                        embed = Embed(title="", color=Color.embed_background(),
                                      description=f"Пользователь {user.mention} был кикнут с сервера.", )
                        embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
                        embed_log = Embed(title="Пользователь кикнут", color=0x7b68ee)
                        embed_log.add_field(name="Автор", value=ctx.author.mention, inline=True)
                        embed_log.add_field(name="Пользователь", value=f"{user.mention} ({user.name})", inline=True)
                        if reason:
                            embed.add_field(name="Причина", value=reason)
                            embed_log.add_field(name="Причина", value=reason, inline=False)
                        else:
                            pass
                        await ctx.respond(embed=embed)
                        await log.send_log(ctx.guild.id, embed=embed_log)
                        await user.kick(reason=reason)
                    except Forbidden:
                        await ctx.respond("У меня нет прав на кик этого пользователя!", ephemeral=True)
                else:
                    await ctx.respond(f"Вы не можете кикнуть этого пользователя!", ephemeral=True)
            except AttributeError:
                await ctx.respond("Пользователь не найден", ephemeral=True)
            except Exception as e:
                print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
                      f"`{ctx.author.id}`\nКоманда: kick")


def setup(bot):
    bot.add_cog(KickCommand(bot))
