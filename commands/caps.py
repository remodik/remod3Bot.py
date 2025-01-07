import discord
from discord.ext import commands


class CapsModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label='Введите текст', style=discord.InputTextStyle.long))

    async def callback(self, ctx):
        text = self.children[0].value
        filtered_text = [c for c in text if c.isalpha()]
        caps_count = sum(1 for c in filtered_text if c.isupper())
        caps_percentage = (caps_count / len(filtered_text)) * 100 if filtered_text else 0
        view = CapsView(text=text, author=ctx.user, caps_percentage=caps_percentage)
        await ctx.response.send_message(f'В сообщении {caps_percentage:.2f}% капса\nВаш текст:\n`{text}`', view=view)


class CapsView(discord.ui.View):
    def __init__(self, text, caps_percentage, author):
        super().__init__()
        self.text = text
        self.caps_percentage = caps_percentage
        self.author = author
        self.is_hidden = False

    @discord.ui.button(label="Скрыть содержимое", style=discord.ButtonStyle.primary)
    async def toggle_visibility(self, button: discord.ui.Button, ctx):
        if ctx.user != self.author:
            return await ctx.response.send_message("Вы не можете использовать эту кнопку.", ephemeral=True)
        self.is_hidden = not self.is_hidden
        if self.is_hidden:
            button.label = "Показать содержимое"
            await ctx.response.edit_message(content=f'В вашем сообщении {self.caps_percentage:.2f}% капса',view=self)
        else:
            button.label = "Скрыть содержимое"
            await ctx.response.edit_message(content=f'В вашем сообщении {self.caps_percentage:.2f}% капса\n'
                                                            f'Ваш текст: `{self.text}`', view=self)


class CapsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="caps")
    async def caps(self, ctx):
        modal = CapsModal(title='Введите текст (Учитываются только буквы)')
        await ctx.send_modal(modal)
        return


def setup(bot):
    bot.add_cog(CapsCommand(bot))
