import discord
from discord.ext import commands
from discord import Embed, ButtonStyle, Color
from discord.ui import View, Button
from commands.log import load_log_channel
from bot2 import get_prefix, bgac


class FaqCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="faq", description="Информация о боте")
    async def _faq(self, ctx):
        await ctx.defer()
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        version = "1.0"
        pref = get_prefix(self.bot, ctx) if ctx.guild is not None else "Вы не на сервере!"
        embed = Embed(title="remod3Bot",
                      description=(
                          "remod3Bot - это многофункциональный бот, предназначенный для крупных серверов "
                          "и более удобного управления ролями и сервером. Написав разработчику, вы можете заказать "
                          "команду/функционал для своего сервера."), color=Color.embed_background())
        try:
            embed.add_field(name="Основные команды",
                            value=f"</help:{bgac('help').id}> - Меню команд.\n"
                                  f"</предложение:{bgac('предложение').id}> - Написать идею для бота.\n"
                                  f"</bug_report:{bgac('bug_report').id}> - Сообщить о баге.\n"
                                  f"</update:{bgac('update').id}> - Последнее обновление.", inline=True)
        except Exception as e:
            print("Ошибка в faq: {e}".format(e=e))
            pass
        embed.add_field(name="Информация о боте",
                        value=f"Кол-во серверов: {len(self.bot.guilds)}\n"
                              f"Версия: {version}\n"
                              f"Дата создания: <t:1707598800:D> (<t:1707598800:R>)", inline=True)
        embed.add_field(name="Разработчики", value="1. `remodik` (`743864658951274528`)", inline=False)
        if ctx.user.guild_permissions.administrator or ctx.user.guild_permissions.manage_guild:
            log_channel_id = load_log_channel(ctx.guild.id)
            log_channel = f"<#{log_channel_id}>" if log_channel_id else "Не установлен"
            embed.add_field(name="Канал логов", value=f"{log_channel}", inline=True)
        embed.add_field(name="Префикс команд", value=f"`{pref}`", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        btn1 = discord.ui.Button(label="Информация о создателе", url='https://solo.to/remod3', style=ButtonStyle.link)
        btn2 = discord.ui.Button(label="Поддержать автора", url="https://www.donationalerts.com/r/remod3",
                         style=ButtonStyle.link)
        view = View()
        view.add_item(btn1)
        view.add_item(btn2)
        await ctx.followup.send(embed=embed, view=view)
        return


def setup(bot):
    bot.add_cog(FaqCommand(bot))
