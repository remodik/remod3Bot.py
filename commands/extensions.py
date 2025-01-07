import discord
from discord.ext import commands
from discord import Option, ExtensionNotFound, ExtensionFailed
import os

def get_all_extensions():
    """Возвращает список всех расширений в папке commands."""
    extensions = []
    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            extensions.append(f"commands.{filename[:-3]}")
    return extensions

async def ext_ac_load(ctx: discord.AutocompleteContext):
    """Автодополнение для команды /load_extension: показывает только незагруженные расширения."""
    all_extensions = get_all_extensions()
    loaded_extensions = ctx.bot.extensions.keys()
    return [ext for ext in all_extensions if ext not in loaded_extensions]

async def ext_ac(ctx: discord.AutocompleteContext):
    """Автодополнение для команд /unload_extension и /reload_extension: показывает только загруженные расширения."""
    loaded_extensions = list(ctx.bot.extensions.keys())
    if ctx.value:
        loaded_extensions = [ext for ext in loaded_extensions if ext.lower().startswith(ctx.value.lower())]
    return loaded_extensions[:25]



class ExtensionManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="load_extension", description="Загрузить расширение.", guild_ids=[1315002924048318506])
    @commands.is_owner()
    async def load_extension(self, ctx, extension: Option(str, "Выберите расширение", autocomplete=ext_ac_load)):
        await ctx.defer(ephemeral=True)
        try:
            if extension in self.bot.extensions:
                await ctx.followup.send(f"Расширение `{extension}` уже загружено.", ephemeral=True)
                return

            self.bot.load_extension(extension)
            await ctx.followup.send(f"Расширение `{extension}` успешно загружено.", ephemeral=True)
        except ExtensionNotFound:
            await ctx.followup.send(f"Расширение `{extension}` не найдено.", ephemeral=True)
        except ExtensionFailed as e:
            await ctx.followup.send(f"Ошибка при загрузке расширения `{extension}`: {e}", ephemeral=True)

    @commands.slash_command(name="unload_extension", description="Выгрузить расширение.", guild_ids=[1315002924048318506])
    @commands.is_owner()
    async def unload_extension(self, ctx, extension: Option(str, "Выберите расширение", autocomplete=ext_ac)):
        await ctx.defer(ephemeral=True)
        try:
            if extension not in self.bot.extensions:
                await ctx.followup.send(f"Расширение `{extension}` не загружено.", ephemeral=True)
                return

            self.bot.unload_extension(extension)
            await ctx.followup.send(f"Расширение `{extension}` успешно выгружено.", ephemeral=True)
        except ExtensionNotFound:
            await ctx.followup.send(f"Расширение `{extension}` не найдено.", ephemeral=True)

    @commands.slash_command(name="reload_extension", description="Перезагрузить расширение.",
                       guild_ids=[1315002924048318506])
    @commands.is_owner()
    async def reload_extension(self, ctx, extension: Option(str, "Выберите расширение", autocomplete=ext_ac)):
        await ctx.defer(ephemeral=True)
        try:
            if extension not in self.bot.extensions:
                await ctx.followup.send(f"Расширение `{extension}` не загружено.", ephemeral=True)
                return

            self.bot.reload_extension(extension)
            await ctx.followup.send(f"Расширение `{extension}` успешно перезагружено.", ephemeral=True)
        except ExtensionNotFound:
            await ctx.followup.send(f"Расширение `{extension}` не найдено.", ephemeral=True)
        except ExtensionFailed as e:
            await ctx.followup.send(f"Ошибка при перезагрузке расширения `{extension}`: {e}", ephemeral=True)


def setup(bot):
    bot.add_cog(ExtensionManagement(bot))
