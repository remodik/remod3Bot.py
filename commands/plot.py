import discord
import numpy as np
import matplotlib.pyplot as plt
from discord import File, Option
from discord.ext import commands
import os
import time


class PlotCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.folder_path = "plots"
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    @commands.slash_command(name="plot", description="Построить график функции")
    async def plot(self, ctx, func: str):
        """
        Построить график указанной функции.
        Пример: !plot x**2 или !plot np.sin(x)
        """
        await ctx.defer(ephemeral=True)
        try:
            # Создание безопасной строки для вычислений
            safe_func = func.replace("sin", "np.sin") \
                .replace("cos", "np.cos") \
                .replace("log", "np.log") \
                .replace("exp", "np.exp") \
                .replace("^", "**") \
                .replace("sqrt", "np.sqrt") \
                .replace("abs", "np.abs") \
                .replace("ceil", "np.ceil") \
                .replace("floor", "np.floor") \
                .replace("hypot", "np.hypot") \
                .replace("pi", "np.pi") \
                .replace("e", "np.e") \
                .replace("comb", "math.comb") \
                .replace("perm", "math.perm") \
                .replace("trunc", "math.trunc") \
                .replace("gcd", "math.gcd") \
                .replace("arcsin", "np.arcsin") \
                .replace("arccos", "np.arccos") \
                .replace("arctan", "np.arctan") \
                .replace("sinh", "np.sinh") \
                .replace("cosh", "np.cosh") \
                .replace("tanh", "np.tanh") \
                .replace("deg", "np.degrees") \
                .replace("rad", "np.radians") \
                .replace("mean", "np.mean") \
                .replace("median", "np.median")

            # Преобразование входного выражения
            x = np.linspace(-10, 10, 500)

            # Проверка и вычисление функции
            # Используем безопасный контекст для eval
            safe_dict = {"x": x, "np": np}
            y = eval(safe_func, {"__builtins__": None}, safe_dict)

            # Построение графика
            plt.figure()
            plt.plot(x, y, label=f"y = {func}")  # Используем исходный func для подписи
            plt.axhline(0, color='black', linewidth=0.5, linestyle="--")
            plt.axvline(0, color='black', linewidth=0.5, linestyle="--")
            plt.title("График функции")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(color='gray', linestyle='--', linewidth=0.5)
            plt.legend()

            # Генерация уникального имени файла с временной меткой
            timestamp = int(time.time())  # Используем количество секунд с эпохи
            file_path = os.path.join(self.folder_path, f"plot_{timestamp}.png")

            # Сохранение графика в файл
            plt.savefig(file_path)
            plt.close()

            # Отправка файла пользователю
            await ctx.followup.send(file=File(file_path), ephemeral=True)
            return

        except Exception as e:
            await ctx.followup.send(f"Произошла ошибка! Попробуйте чуть позже.", ephemeral=True)
            print(f"Произошла ошибка: {e}")
            return

def setup(bot):
    bot.add_cog(PlotCommand(bot))
