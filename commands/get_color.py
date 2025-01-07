from discord import Embed, Option, File
from discord.ext import commands
from PIL import Image, ImageDraw
import io

class ColorCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="get_color", description="Показывает указанный цвет.")
    async def get_color(self, ctx, color: Option(str, "Введите цвет в формате HEX (#RRGGBB или RRGGBB)")):
        try:
            if color.startswith("#"):
                color = color[1:]

            if len(color) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color):
                await ctx.respond("Неверный формат цвета. Укажите цвет в формате HEX (#RRGGBB).", ephemeral=True)
                return

            r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)

            image = Image.new("RGBA", (128, 128), (255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            draw.ellipse((16, 16, 112, 112), fill=(r, g, b))
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            embed = Embed(
                title=f"Ваш цвет: #{color.upper()}",
                description=f"HEX: `#{color.upper()}`\nRGB: `({r}, {g}, {b})`",
                color=int(color, 16))
            embed.set_image(url="attachment://color_circle.png")
            file = File(buffer, filename="color_circle.png")
            await ctx.respond(embed=embed, file=file, ephemeral=True)
        except Exception as e:
            await ctx.respond(f"Произошла ошибка!", ephemeral=True)
            print("Ошибка в get_color", e)


def setup(bot):
    bot.add_cog(ColorCommand(bot))
