import discord
from discord.ext import commands
from discord import InputTextStyle, Embed, Color, ui, ButtonStyle
import logging
logging.basicConfig(level=logging.DEBUG)
black_list = []



class UpdateBotCommand(ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Заявка на баг")
        self.add_item(ui.InputText(label="Суть улучшения", style=InputTextStyle.long,
                                   min_length=15, placeholder="Напишите суть улучшения", max_length=500))
        self.add_item(ui.InputText(label="Как с вами связаться", style=InputTextStyle.short,
                                   placeholder="Укажите ваши контактные данные", max_length=100))
        self.add_item(ui.InputText(label="Чем полезно", placeholder="Чем это улучшение будет полезно для бота?",
                                   max_length=250))

    async def callback(self, ctx):
        if ctx.user.id in black_list:
            await ctx.response.send_message("Вы находитесь в черном списке бота!", ephemeral=True)
            return
        answers = [item.value for item in self.children]
        news_channel = self.bot.get_channel(1315002924862148634)
        if not news_channel:
            await ctx.response.send_message("Канал для отправки предложений не найден. "
                                                    "Свяжитесь с разработчиком.", ephemeral=True)
            return
        embed = Embed(title="Заявка на улучшение бота", color=Color.embed_background())
        embed.add_field(name="Суть улучшения", value=answers[0], inline=False)
        embed.add_field(name="Данные пользователя", value=answers[1], inline=False)
        embed.add_field(name="Чем будет полезно", value=answers[2], inline=False)
        view = UpdateBotView(ctx.user)
        await news_channel.send(content=f"{ctx.user.mention} | `{ctx.user.name}` | "
                                       f"`{ctx.user.id}`", embed=embed, view=view)
        await ctx.response.send_message("Ваша заявка успешно отправлена!", ephemeral=True)


class UpdateBotView(ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, ui.Button): child.disabled = True

    @staticmethod
    def update_status(embed: Embed, status: str):
        status_field_index = None
        for i, field in enumerate(embed.fields):
            if field.name == "Статус:":
                status_field_index = i
                break
        if status_field_index is not None:
            embed.set_field_at(status_field_index, name="Статус:", value=status, inline=False)
        else:
            embed.add_field(name="Статус:", value=status, inline=False)

    @discord.ui.button(label="Принять", style=ButtonStyle.success, custom_id="accept_bug_button")
    async def accept_button_callback(self, button: discord.ui.Button, ctx):
        if ctx.user.guild_permissions.administrator:
            embed = ctx.message.embeds[0]
            self.update_status(embed, "Принята")
            self.disable_all_buttons()
            await ctx.message.edit(embed=embed, view=self)
            await ctx.response.send_message(f"{ctx.user.mention} принял заявку на улучшение от {self.member.mention} | "
                                            f"`{self.member.name}` | `{self.member.id}`")
            await self.member.send("Ваша заявка на улучшение бота была успешно одобрена!.\n"
                                   f"Рассматривал: {ctx.user.mention} | `{ctx.user.name}`")
        else:
            await ctx.response.send_message("У вас нет прав для принятия заявок.", ephemeral=True)

    @discord.ui.button(label="Отказать", style=ButtonStyle.danger, custom_id="decline_bug_button")
    async def deny_button_callback(self, button: discord.ui.Button, ctx):
        if ctx.user.guild_permissions.administrator:
            modal = UpdateBotReasonView(self.member, self)
            await ctx.response.send_modal(modal)
        else:
            await ctx.response.send_message("У вас нет прав для отклонения заявок.", ephemeral=True)

    @ui.button(label="На рассмотрении", style=discord.ButtonStyle.primary, custom_id="pending_bug_button")
    async def pending_button_callback(self, button: ui.Button, ctx):
        if ctx.user.guild_permissions.administrator:
            embed = ctx.message.embeds[0]
            self.update_status(embed, "На рассмотрении")
            await ctx.message.edit(embed=embed, view=self)
            await ctx.response.send_message(f"{ctx.user.mention} начал рассмотрение заявки на улучшение бота от "
                                            f"{self.member.mention} `{self.member.name}` | `{self.member.id}`")
            await self.member.send("Ваша заявка на улучшение бота находится на рассмотрении.")
        else:
            await ctx.response.send_message("У вас нет прав для изменения статуса заявок.", ephemeral=True)


class UpdateBotReasonView(ui.Modal):
    def __init__(self, member: discord.Member, view: UpdateBotView):
        super().__init__(title="Причина отказа")
        self.member = member
        self.view = view
        self.add_item(ui.InputText(label="Причина отказа", style=discord.InputTextStyle.long))

    async def callback(self, ctx):
        reason = self.children[0].value
        embed = ctx.message.embeds[0]
        self.view.update_status(embed, f"Отклонена: {reason}")
        self.view.disable_all_buttons()
        await ctx.message.edit(embed=embed, view=self.view)
        await ctx.response.send_message(f"{ctx.user.mention} отклонил заявку на улучшение от {self.member.mention} | "
                                        f"`{self.member.name}` | `{self.member.id}`")
        await self.member.send("Ваша заявка на улучшение бота была отклонена.\n"
                               f"Рассматривал: {ctx.user.mention} | `{ctx.user.name}`")


class UpdateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="предложение", description="Отправить предложение по улучшению бота")
    async def idea(self, ctx):
        modal = UpdateBotCommand(self.bot)
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(UpdateCommand(bot))
