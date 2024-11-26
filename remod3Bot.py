import datetime
from datetime import (timedelta, date, datetime, timezone, time, tzinfo)
from typing import Type
from collections import (defaultdict, Counter)
import colorama, contextlib
import discord
from discord.utils import get
from discord.ui import (View, Select, Button, Item, Modal, view)
from discord.ext import tasks, commands
from discord import (ui, SelectMenu, SelectOption, Interaction, guild_only, Option, Color, Embed,
                     ButtonStyle, InputTextStyle, PartialEmoji, InputText, Colour)
import discord.ext.commands.errors as error
from discord.commands import permissions
from discord.abc import *
import asyncio, ast, aiohttp
from asyncio import sleep
import hashlib
#from pypresence import Presence
import math
import io
import json
import sqlite3
import os, openai, operator
import textwrap, time
import subprocess
import requests, random, re
from art import tprint
from bs4 import BeautifulSoup

block_users = []
if os.path.exists("json/prefixes.json"):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
else:
    prefixes = {}


def get_prefix(bot, message):
    guild_id = str(message.guild.id)
    return prefixes.get(guild_id, "r!")


bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), enable_debug_events=True)
roles = discord.SlashCommandGroup("role", "description", guild_only=True)
bot.remove_command("help")


@bot.command(name="prefix")
async def set_prefix(ctx, new_prefix=None):
    if ctx.author.guild_permissions.administrator:
        if new_prefix is None:
            await ctx.reply(f"Текущий префикс: {get_prefix(bot, ctx)}")
            return
        guild_id = str(ctx.guild.id)
        prefixes[guild_id] = new_prefix
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f)
        await ctx.send(f"Префикс изменён на: {new_prefix}")


premium_guild = [1241732478020878469]
with open('json/config.json', 'r') as f:
    data_as = json.load(f)


class CapsModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label='Введите текст', style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        text = self.children[0].value
        filtered_text = [c for c in text if c.isalpha()]
        caps_count = sum(1 for c in filtered_text if c.isupper())
        caps_percentage = (caps_count / len(filtered_text)) * 100 if filtered_text else 0
        view = CapsView(text=text, author=interaction.user, caps_percentage=caps_percentage)
        await interaction.response.send_message(f'В сообщении {caps_percentage:.2f}% капса\n'
                                                f'Ваш текст: `{text}`', view=view)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message(
            f"Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: `remodik`\n\n{error}")


class CapsView(View):
    def __init__(self, text, caps_percentage, author):
        super().__init__()
        self.text = text
        self.caps_percentage = caps_percentage
        self.author = author
        self.is_hidden = False

    @discord.ui.button(label="Скрыть содержимое", style=discord.ButtonStyle.primary)
    async def toggle_visibility(self, button: Button, interaction: Interaction):
        if interaction.user != self.author:
            return await interaction.response.send_message("Вы не можете использовать эту кнопку.", ephemeral=True)
        self.is_hidden = not self.is_hidden
        if self.is_hidden:
            button.label = "Показать содержимое"
            await interaction.response.edit_message(content=f'В вашем сообщении {self.caps_percentage:.2f}% капса',
                                                    view=self)
        else:
            button.label = "Скрыть содержимое"
            await interaction.response.edit_message(content=f'В вашем сообщении {self.caps_percentage:.2f}% капса\n'
                                                            f'Ваш текст: `{self.text}`', view=self)


@bot.slash_command(name="restart", guild_ids=[1241732478020878469,1148996038363975800, 1214617864863219732])
@commands.is_owner()
async def restart_bot(ctx: discord.Interaction):
    await ctx.response.send_message("Успешно", ephemeral=True)
    os.system('cls')
    os.system('python.exe C:\\Users\\slend\\OneDrive\\OneDrive\\bot\\remod3Bot.py')


@bot.slash_command(name="caps")
async def caps(ctx: commands.Context):
    modal = CapsModal(title='Введите текст (Учитываются только буквы)')
    await ctx.send_modal(modal)
    print(f"caps: {ctx.command.id}")


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    server_id = 1138400553081253948
    special_user_1 = 863326185451028521
    special_user_2 = 835874448779247688
    if message.author.bot or message.guild.id != server_id or message.author.id == 743864658951274528: return
    await bot.process_commands(message)
    mentions_ids = [user.id for user in message.mentions]
    if message.author.id in [special_user_1, special_user_2]: return
    await bot.process_commands(message)
    if special_user_1 in mentions_ids or special_user_2 in mentions_ids:
        await message.delete()
        await message.channel.send(content=f'{message.author.mention}, :shushing_face:')
    await bot.process_commands(message)
    if message.guild.id == 1138400553081253948:
        trigger_words = ["сервер запущен", "серв работает", "серв запущен", "сервер работает"]
        message_content_lower = message.content.lower()
        if any(word in message_content_lower for word in trigger_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, На данный момент сервер закрыт на переработку. "
                                       f"Планируется переделать сервер с Грифа на Анархию. Подробности можно узнать "
                                       f"тут: https://discord.com/channels/1138400553081253948/1138400553995604070")
    await bot.process_commands(message)


def save_message_id(channel_id, message_id):
    try:
        with open('json/message_cache.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[str(channel_id)] = message_id
    with open('json/message_cache.json', 'w') as file:
        json.dump(data, file)


def get_message_id(channel_id):
    try:
        with open('json/message_cache.json', 'r') as file:
            data = json.load(file)
        return data.get(str(channel_id))
    except FileNotFoundError:
        return None


@bot.slash_command(name="send_stat", description='Чат для отправки статистики сервера')
async def send_stat(ctx, channel: discord.abc.GuildChannel):
    try:
        if ctx.author.guild_permissions.manage_roles:
            channel_id = channel.id
            embed = await get_server_info(ctx.guild)
            message = await channel.send(embed=embed)
            save_message_id(channel_id, message.id)
            await ctx.response.send_message(f"Статистика будет отправляться каждые 5 минут в канал {channel.mention}")
            embed_log = Embed(title="Канал статистики настроен", color=0x7b68ee)
            embed_log.add_field(name="Автор", value=ctx.author.mention, inline=True)
            embed_log.add_field(name="Канал", value=channel.mention)
            await send_log(ctx.guild.id, embed=embed_log)
            print(f"send_stat: {ctx.command.id}")
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} "
              f"| {ctx.author.id}\nКоманда: send_stat")


async def update_old_messages():
    try:
        with open('json/message_cache.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    except Exception as e:
        return
    for channel_id, message_id in data.items():
        channel = bot.get_channel(int(channel_id))
        if channel is not None:
            embed = await get_server_info(channel.guild)
            if message_id:
                try:
                    message = await channel.fetch_message(message_id)
                    await message.edit(embed=embed)
                except discord.ext.commands.errors.MessageNotFound:
                    message = await channel.send(embed=embed)
                    save_message_id(channel_id, message.id)
            else:
                message = await channel.send(embed=embed)
                save_message_id(channel_id, message.id)


@tasks.loop(minutes=1)
async def send_statistics():
    try:
        with open('json/message_cache.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    except Exception as e:
        return
    for channel_id, message_id in data.items():
        channel = bot.get_channel(int(channel_id))
        if channel is not None:
            embed = await get_server_info(channel.guild)
            if message_id:
                try:
                    message = await channel.fetch_message(message_id)
                    await message.edit(embed=embed)
                except discord.ext.commands.errors.MessageNotFound:
                    message = await channel.send(embed=embed)
                    save_message_id(channel_id, message.id)
            else:
                message = await channel.send(embed=embed)
                save_message_id(channel_id, message.id)


async def get_server_info(guild):
    embed = Embed(title=f'Статистика сервера Discord', color=Color.default())
    roles = len(guild.roles)
    voice_members = sum(1 for member in guild.members if member.voice)
    emojis = len(guild.emojis)
    members = guild.member_count
    bots = sum(1 for member in guild.members if member.bot)
    humans = members - bots
    online = sum(1 for member in guild.members if member.status == discord.Status.online)
    idle = sum(1 for member in guild.members if member.status == discord.Status.idle)
    do_not_disturb = sum(1 for member in guild.members if member.status == discord.Status.do_not_disturb)
    offline = sum(1 for member in guild.members if member.status == discord.Status.offline)
    embed.add_field(name='Общее', value=f"<:adminicon:1269748398068727829> Кол-во ролей: **{roles}**\n"
                                        f"<:Default_Role_Permissions:1269748753045393510> Голосовой онлайн: "
                                        f"**{voice_members}**\n"
                                        f"<:1630spotifywarning:1269748064961433631> Кол-во эмодзи: **{emojis}**",
                    inline=True)
    embed.add_field(name=f'Участников [{members}]', value=f"Людей: **{humans}**\n"
                                                          f"Ботов: **{bots}**", inline=True)
    embed.add_field(name='По статусам', value=f'<a:6209loadingonlinecircle:1269732534552498226> В сети: {online}\n'
                                              f'<a:7278loadingidlecircle:1269732551384105060> Не активен: {idle}\n'
                                              f'<a:7278loadingdonotdisturbcircle:1269732558300778566> Не беспокоить: '
                                              f'{do_not_disturb}\n'
                                              f'<a:2390offlineinvisible:1269742137331941508> Не в сети: {offline}',
                    inline=True)
    text_channels = sum(1 for channel in guild.channels if isinstance(channel, discord.TextChannel))
    voice_channels = sum(1 for channel in guild.channels if isinstance(channel, discord.VoiceChannel))
    stage_channels = sum(1 for channel in guild.channels if isinstance(channel, discord.StageChannel))
    categories = sum(1 for channel in guild.channels if isinstance(channel, discord.CategoryChannel))
    embed.add_field(name='Каналов', value=f"<:5413blurplechat:1269750004663324786> Текстовые: {text_channels}\n"
                                          f"<:2911voicebadge:1269746265185587220> Голосовые: {voice_channels}\n"
                                          f"<:5508discordstagechannel:1269746018086555869> Трибуны: {stage_channels}\n"
                                          f"<:xz:1269751898458685535> Категории: {categories}", inline=True)
    boost_level = guild.premium_tier
    boosters = len(guild.premium_subscribers)
    boosts = guild.premium_subscription_count
    embed.add_field(name='Буст сервера', value=f'<:4989boostheart:1269747700325285989> Уровень буста: {boost_level}\n'
                                               f'<:3370utilityboost:1269747791194751086> Кол-во бустеров: {boosters}\n'
                                               f'<a:21025boosterbadgerolling:1269746647139881133> Кол-во бустов: '
                                               f'{boosts}', inline=True)
    timestamp = 60
    current_time = time.time()
    target_time = current_time + timestamp
    unix_time = int(target_time)
    embed.add_field(name="", value=f"Следующее обновление: <t:{unix_time}:R>", inline=False)
    return embed


def get_hwid():
    cpu_info = subprocess.check_output("wmic cpu get processorid", shell=True).decode().strip().split("\n")[1]
    hdd_info = (subprocess.check_output("wmic diskdrive get serialnumber", shell=True).decode().strip().split("\n")[1])
    hwide = cpu_info + hdd_info
    hwide = hwide.encode()
    hwide = hashlib.sha256(hwide).hexdigest()
    return hwide


os.system('color a')
os.system('title Discord Bot')
print("\n")
tprint("remod3")


@bot.slash_command(name='staff_d',description="Список администрации проекта",
                   guild_ids=[1138204059397005352,1263854530445971671])
async def _staff_ds(ctx):
    if not ctx.author.guild_permissions.administrator:
        return 
    Vlad = 1138210426002362559
    tex = 1219875518178922546
    men = 1258410711483420802
    sov = 1240156648715325540
    team = 1228304126782210068
    cur = 1138212488123514970
    mlc = 1236331609192398948
    embed = discord.Embed(title="Администрация HightMine", color=discord.Color.default())
    embed.add_field(name="", value=f"<@&{Vlad}> [Saha_Hightmine](https://vk.com/saha_hightmine) | "
                                   f"<@1131618591251370215> (`its_saha`)", inline=False)
    embed.add_field(name="", value=f"<@&{tex}> [FrayerLT](http://vk.com/artemalladin) | "
                                   "<@748978241305313445> (`iwantpepper`)", inline=False)
    embed.add_field(name="", value=f"<@&{men}> [Raydex__](http://vk.com/raydexgrief) | "
                                   "<@1097064973328453704> (`raydexov`)", inline=False)
    embed.add_field(name="", value=f"<@&{sov}> [MrWenDeTTa](https://vk.com/wendett1) | <@1162321198143782932>"
                                   " (`wendett1`)", inline=False)
    embed.add_field(name="", value=f"<@&{team}> [DoSheG](https://vk.com/rakhimov_usman) | <@637309157997019136>"
                                   " (`dosheg`)", inline=False)
    embed.add_field(name="", value=f"<@&{team}> [remod3](https://vk.com/remod3) | <@743864658951274528> "
                                   "(`remodik`)", inline=False)
    embed.add_field(name="", value=f"<@&{team}> [xFallenAngell_](http://vk.com/miamurov) | "
                                   "<@433592572754132993> (`xfallenangel_`)", inline=False)
    embed.add_field(name="", value=f"<@&{team}> [DedGeroinov](https://vk.com/freegerokn) | "
                                   "<@931585084312670219> (`dedgeroinov`)", inline=False)
    embed.add_field(name="", value=f"<@&{team}> [medium_abaje](https://vk.com/vilstor) | <@613729038422507530>"
                                   " (`ychastnik`)", inline=False)
    embed.add_field(name="", value=f"<@&{cur}> [ceves](https://vk.com/id481239721) | <@332182810662010881>"
                                   " (`g26444`)", inline=False)
    embed.add_field(name="", value=f"<@&{mlc}> [PoliceRW](https://vk.com/aristokrat_6_6_6) | "
                                   "<@1114643268202926090> (`policerw`)", inline=False)
    embed.add_field(name="", value=f"<@&{mlc}> [faffaf](http://vk.com/faffaf12) | <@891589636097450034> "
                                   "(`faffaf`)", inline=False)
    embed.add_field(name="", value=f"<@&{cur}> [toxic_allen](http://vk.com/yalinger) | <@1140748293853433866>"
                                   " (`alipuska`)", inline=False)
    embed.add_field(name="", value=f"<@&{mlc}> [EllezarGreen](https://vk.com/id797728158) | "
                                   "<@1198683837966852228> (`ellezargreen`)", inline=False)
    await ctx.response.send_message("+", ephemeral=True)
    await ctx.send(embed=embed)


def load_warnings():
    try:
        with open('json/user_warns.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'user_warns': {}, 'total': 0}


def save_warnings(data):
    with open('json/user_warns.json', 'w') as f:
        json.dump(data, f, indent=4)


@bot.command(name='warn')
async def warn(ctx, target: discord.User = None, duration: str = None, *, reason: str = ''):
    if ctx.author.guild_permissions.administrator:
        pref = get_prefix(bot, ctx)
        if target is None and ctx.message.reference:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            target = referenced_message.author
        if target is None:
            await ctx.reply(embed=discord.Embed(title="", description=f'Команда "{pref}warn"\nВыдает указанному участнику '
                                                                      f'вечное или временное предупреждение.'))
            return
        data = load_warnings()
        user_id = str(target.id)
        if user_id not in data['user_warns']:
            data['user_warns'][user_id] = []
        if duration:
            if duration.endswith('d'):
                expiry_time = datetime.now() + timedelta(days=int(duration[:-1]))
            elif duration.endswith('h'):
                expiry_time = datetime.now() + timedelta(hours=int(duration[:-1]))
            elif duration.endswith('m'):
                expiry_time = datetime.now() + timedelta(minutes=int(duration[:-1]))
            else:
                await ctx.send('Неверный формат времени. Используйте дни (d), часы (h) или минуты (m).')
                return
            expiry_time_str = expiry_time.isoformat()
        else:
            expiry_time_str = None
        warning_id = len(data['user_warns'][user_id]) + 1
        total_warning_id = data['total'] + 1
        issuer = ctx.author.name
        data['user_warns'][user_id].append({
            'id': warning_id,
            'reason': reason,
            'expires': expiry_time_str,
            'issued_at': datetime.now().isoformat(),
            'issuer': issuer
        })
        data['total'] = total_warning_id
        save_warnings(data)
        embed = discord.Embed(title='', description=f'Участник {target.mention} получил предупреждение `#{warning_id}` '
                                                    f'`(случай #{total_warning_id})`.', color=0x5a357f)
        embed.add_field(name='Причина', value=reason if reason else 'Не указана')
        if expiry_time_str:
            embed.add_field(name='Истекает', value=f'<t:{int(expiry_time.timestamp())}:F> '
                                                   f'(<t:{int(expiry_time.timestamp())}:R>)')
        else:
            embed.add_field(name='Истекает', value='Никогда (предупреждение выдано навсегда)')
        await ctx.send(embed=embed)
        print(f"caps: {ctx.command.id}")


@bot.command(name='unwarn')
async def unwarn(ctx, case_id: int = None):
    if ctx.author.guild_permissions.administrator:
        if case_id is None:
            await ctx.reply(embed=discord.Embed(title="Снять предупреждение участнику",
                                                description='Снимает с участника предупреждение по номеру случая из '
                                                            'команды ".warns".\n\n'
                                                            '**Использование**\n'
                                                            '`.unwarn <номер случая>`\n\n'
                                                            '**Пример**\n'
                                                            '`.unwarn 1`\n┗ Снимет предупреждение с номером случая #1.'))
            return
        data = load_warnings()
        found = False
        for user_id, warnings in data['user_warns'].items():
            for warning in warnings:
                if warning.get('id') == case_id:
                    warnings.remove(warning)
                    found = True
                    data['total'] -= 1
                    save_warnings(data)
                    embed = discord.Embed(title='', description=f'Предупреждение `#{case_id}` было снято.', color=0x5a357f)
                    await ctx.send(embed=embed)
                    break
            if found: break
        if not found: await ctx.send(f'Предупреждение с общим случаем `#{case_id}` не найдено.')


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
    ast.BitAnd: operator.and_,
    ast.BitOr: operator.or_,
    ast.BitXor: operator.xor,
    ast.LShift: operator.lshift,
    ast.RShift: operator.rshift,
}
FUNCTIONS = {
    'abs': abs,
    'max': max,
    'min': min,
    'round': round,
    'pow': pow,
    'sqrt': math.sqrt,
    'log': math.log,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'exp': math.exp,
}


def safe_eval(expression):
    tree = ast.parse(expression, mode='eval')
    return _eval(tree.body)


def _eval(node):
    if isinstance(node, ast.BinOp):
        if type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        raise ValueError("Unsupported operator")
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS:
            args = [_eval(arg) for arg in node.args]
            return FUNCTIONS[node.func.id](*args)
        raise ValueError("Unsupported function")
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Expression):
        return _eval(node.body)
    else:
        raise TypeError("Unsupported expression")


@bot.slash_command(name="calculate", description="Вычисляет математическое выражение")
async def _calculate(ctx, expression: str):
    try:
        result = safe_eval(expression)
        embed = discord.Embed(description=f"Результат выражения `{expression}`", color=0x5a357f)
        embed.add_field(name="Результат", value=f"`{result}`")
        await ctx.response.send_message(embed=embed)
    except TypeError:
        await ctx.response.send_message("Оператор не поддерживается!", ephemeral=True)
    except Exception as e:
        await print(f"Ошибка: {e}")


@bot.command(name='warns')
async def warns(ctx, user: discord.User = None):
        data = load_warnings()
        if user is None:
            user_id = str(ctx.author.id)
            user_mention = ctx.author.name
        else:
            user_id = str(user.id)
            user_mention = user.name
        if user_id in data['user_warns']:
            user_warnings = data['user_warns'][user_id]
            embed = discord.Embed(title=f'Предупреждения участника {user_mention}', color=0x5a357f)
            if user_warnings:
                for w in user_warnings:
                    warning_id = w['id']
                    reason = w['reason']
                    issued_at = datetime.fromisoformat(w['issued_at'])
                    expires = datetime.fromisoformat(w['expires']) if w['expires'] else None
                    issuer = w.get('issuer', 'Неизвестен')
                    expires_text = f'<t:{int(expires.timestamp())}:F> (<t:{int(expires.timestamp())}:R>)' if expires else \
                        'Никогда'
                    embed.add_field(name=f'',
                                    value=f'`Случай #{warning_id}` **<t:{int(issued_at.timestamp())}> {issuer}**\n'
                                          f'**Причина:** {reason}\n'
                                          f'**Действует до:** {expires_text}',
                                    inline=False)
                    embed.set_footer(text=f"Запросил {ctx.author.name}")
                await ctx.send(embed=embed)
            else:
                embed.description = f'У участника {user_mention} нет предупреждений.'
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='',
                                  description=f'У {user_mention} нет предупреждений.',
                                  color=0x5a357f)
            await ctx.send(embed=embed)


try:
    with open('json/warnings.json', 'r') as file:
        warnings = json.load(file)
except FileNotFoundError:
    warnings = {}


@bot.slash_command(name='warn',description='Выдать выговор модератору',guild_ids=[1263854530445971671])
async def _warn(ctx, member: discord.Option(discord.Member, description="Кому выдать выговор"),
                reason: discord.Option(str, description="Причина выговора", required=False)):
    try:
        if ctx.author.guild_permissions.administrator:
            ob_channel = bot.get_channel(1263869130705076305)
            if member.id not in warnings:
                warnings[member.id] = {'count': 1, 'reasons': [reason]}
            else:
                warnings[member.id]['count'] += 1
                warnings[member.id]['reasons'].append(reason)
    
            embed = discord.Embed(title='', description=f'{member.mention} выдан выговор.',
                                  color=discord.Color.default())
            embed.add_field(name='Причина', value=reason if reason else 'Не указана', inline=False)
            embed.add_field(name='Количество выговоров', value=warnings[member.id]['count'], inline=False)
            await ob_channel.send(embed=embed)
            await ctx.response.send_message("+", ephemeral=True)
            guild = ctx.guild
            role1 = "Выговор 1/3"
            role2 = "Выговор 2/3"
            xz = discord.utils.get(guild.roles, name=role1)
            xz2 = discord.utils.get(guild.roles, name=role2)
            if warnings[member.id]['count'] == 1:
                await member.add_roles(xz)
            elif warnings[member.id]['count'] == 2:
                await member.add_roles(xz2)
                await member.remove_roles(xz)
            elif warnings[member.id]['count'] == 3:
                warnings[member.id]['count'] -= 3
                member = ctx.guild.get_member(member.id)
                if member:
                    embed = discord.Embed(title="", description=f"Новости персонала HightMine за {date.today()}\n",
                                          color=discord.Color.default())
                    if member.top_role.id == 1263854684787970122:
                        embed.add_field(name="Снят с должности «Руководителя проекта»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263854773023543428:
                        embed.add_field(name="Снят с должности «Менеджера персонала»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263854774156132372:
                        embed.add_field(name="Снят с должности «Менеджера медиа»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263854775309570169:
                        embed.add_field(name="Снят с должности «Главы Тех.Поддержки»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263854774625898658:
                        embed.add_field(name="Снят с должности «Команды проекта»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263863292254748692:
                        embed.add_field(name="Снят с должности «Администратора»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263854775900835904:
                        embed.add_field(name="Снят с должности «Куратора Модерации»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263854783639326794:
                        embed.add_field(name="Снят с должности «Мл.Куратора Модерации»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263867829623460042:
                        embed.add_field(name="Снят с должности «ГС Секции»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263867759524188161:
                        embed.add_field(name="Снят с должности «ЗГС Секции»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856989499424818:
                        embed.add_field(name="Снят с должности «Tech Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856995828760690:
                        embed.add_field(name="Снят с должности «Method Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856994750697635:
                        embed.add_field(name="Снят с должности «Forum Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856995157545043:
                        embed.add_field(name="Снят с должности «Support Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263863513693032459:
                        embed.add_field(name="Снят с должности «Media Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263854784969183303:
                        embed.add_field(name="Снят с должности «Build Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856988937261076:
                        embed.add_field(name="Снят с должности «Event Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263867286901751818:
                        embed.add_field(name="Снят с должности «GP Section»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856996692656140:
                        embed.add_field(name="Снят с должности «Главного Модератора»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263856996965159002:
                        embed.add_field(name="Снят с должности «Старшего Модератора»", value=f"{member.mention}",
                                        inline=False)
                    elif member.top_role.id == 1263856997737037904:
                        embed.add_field(name="Снят с должности «Модератора»", value=f"{member.mention}", inline=False)
                    elif member.top_role.id == 1263856998005477467:
                        embed.add_field(name="Снят с должности «Хелпера»", value=f"{member.mention}", inline=False)
                    embed.add_field(name="", value="причина: 3/3 выговоров.")
                    await ob_channel.send(embed=embed)
                    roles_to_remove = [role for role in member.roles if
                                       role.name in ["Менеджер персонала", "Менеджер медиа",
                                                     "Глава Тех.Поддержки", "Команда Проекта", "Администратор",
                                                     "Куратор модерации", "Мл.Куратор Модерации", "ГС Секции", "ЗГС Секции",
                                                     "Teaching Section", "Method Section", "Forum Section",
                                                     "Support Section",
                                                     "Media Section", "Build Section", "Event Section", "GP Section",
                                                     "Главный Модератор", "Старший Модератор", "Модератор", "Хелпер",
                                                     "Выговор 2/3", "Выговор 1/3", "Устный 2/3", "Устный 1/3", "1st Group",
                                                     "2nd Group", "3rd Group"]]
                    await member.remove_roles(*roles_to_remove)
        with open('json/warnings.json', 'w') as file:
            json.dump(warnings, file)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: /warn")


@bot.slash_command(name='unwarn',description='Снять последний выговор у модератора',guild_ids=[1263854530445971671])
async def unwarn(ctx, user: discord.Member):
    try:
        if not ctx.author.guild_permissions.administrator:
            return 
        if user.id in warnings and warnings[user.id]['count'] > 0:
            warnings[user.id]['count'] -= 1
            last_reason = warnings[user.id]['reasons'].pop()
            embed = discord.Embed(title=f'Выговор снят у {user.name}',
                                  description=f'Причина последнего выговора: {last_reason}\nКоличество выговоров: '
                                              f'{warnings[user.id]["count"]}', color=discord.Color.default())
            await ctx.response.send_message(embed=embed)
            with open('json/warnings.json', 'w') as file:
                json.dump(warnings, file)
        else:
            embed = discord.Embed(title='', description=f'{user.name} не имеет выговоров.',
                                  color=discord.Color.default())
            await ctx.response.send_message(embed=embed)
        with open('json/warnings.json', 'w') as file:
            json.dump(warnings, file)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: /unwarn")


@bot.slash_command(name='warns',description='Выговоры модератора',guild_ids=[1263854530445971671])
async def _warns(ctx, user: discord.Member):
    try:
        if not ctx.author.guild_permissions.administrator:
            return 
        if user.id in warnings:
            embed = discord.Embed(title=f'', description=f'Выговоры у {user.name}',
                                  color=discord.Color.default())
            for idx, reason in enumerate(warnings[user.id]['reasons']):
                embed.add_field(name=f'Выговор {idx + 1}', value=reason, inline=False)
            embed.add_field(name='Количество выговоров', value=warnings[user.id]['count'], inline=False)
        else:
            embed = discord.Embed(title='Информация о выговорах', description=f'{user.mention} не имеет выговоров.',
                                  color=discord.Color.default())
        await ctx.response.send_message(embed=embed)
        with open('json/warnings.json', 'w') as file:
            json.dump(warnings, file)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: /warns")


@bot.slash_command(name='warnlist',description='Список пользователей с выговорами',guild_ids=[1263854530445971671])
async def warnlist(ctx):
    try:
        if not ctx.author.guild_permissions.administrator:
            return 
        if warnings:
            embed = discord.Embed(title='Список пользователей с выговорами', color=discord.Color.default())
            for user_id, data in warnings.items():
                if data["count"] == 0: continue
                user = ctx.guild.get_member(user_id)
                if user:
                    embed.add_field(name='Пользователь', value=f'<@{user_id}>', inline=True)
                    embed.add_field(name='Выговоры', value=data["count"], inline=True)
            if not embed.fields:
                embed = discord.Embed(title='Список пользователей с выговорами',
                                      description='Нет пользователей с выговорами.',
                                      color=discord.Color.default())
            await ctx.response.send_message(embed=embed)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: /warnlist")


def get_message_declension(count):
    """Функция для склонения слова 'сообщение' в зависимости от количества."""
    if 11 <= count % 100 <= 19:
        return "сообщений"
    else:
        cases = {1: "сообщение", 2: "сообщения", 3: "сообщения", 4: "сообщения"}
        return cases.get(count % 10, "сообщений")


def get_time_declension(amount, unit):
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


def parse_time_string(time_string):
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
        unit_plural = get_time_declension(amount, unit)
        time_description.append(f"{amount} {unit_plural}")
        total_delta += timedelta(**{time_units[unit]: amount})

    return total_delta, " и ".join(time_description)


@bot.slash_command(name="clear", description="Удаляет сообщения в чате")
async def clear_messages(ctx: discord.ApplicationContext,
                         amount: discord.Option(int, "Количество сообщений", required=False),
                         time: discord.Option(str, "За какое время удалить (1s|m|h|d|w и т.д.)", required=False),
                         user: discord.Option(discord.User, "Пользователь", required=False)):
    channel = ctx.channel
    await ctx.defer(ephemeral=True)
    if amount:
        deleted_count = 0
        async for message in channel.history(limit=150):
            if user and message.author != user:
                continue
            try:
                await message.delete()
                deleted_count += 1
                if deleted_count >= amount:
                    break
            except discord.Forbidden:
                continue
        declension = get_message_declension(deleted_count)
        if user and amount:
            await ctx.followup.send(f"Удалено {deleted_count} {declension} от {user.mention}.", ephemeral=True)
            embed = Embed(title="Сообщение удалено", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            embed.add_field(name="Жертва", value=user.mention, inline=True)
            embed.add_field(name="Количество", value=deleted_count)
            await send_log(ctx.guild.id, embed=embed)
        elif amount:
            await ctx.followup.send(f"Удалено {deleted_count} {declension}.", ephemeral=True)
            embed = Embed(title="Сообщение удалено", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            embed.add_field(name="Количество", value=deleted_count)
            await send_log(ctx.guild.id, embed=embed)
        return
    if time:
        time_delta, time_description = parse_time_string(time)
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
            await message.delete()
            deleted_count += 1
        except discord.Forbidden:
            continue
    declension = get_message_declension(deleted_count)
    await ctx.followup.send(f"Удалено {deleted_count} {declension} за посл. {time_description}.", ephemeral=True)
    embed = Embed(title="Сообщение удалено", color=0x7b68ee)
    embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
    embed.add_field(name="Количество", value=deleted_count, inline=False)
    embed.add_field(name="Время", value=time_description)
    await send_log(ctx.guild.id, embed=embed)


@bot.slash_command(name="kick", description="Кикнуть пользователя")
async def _kick(ctx,user: discord.Option(discord.Member, description="Участник сервера, которого нужно кикнуть"),
                причина: discord.Option(str, description="Причина кика", default=False)):
    if not ctx.author.guild_permissions.kick_members:
        return
    if user == ctx.author:
        await ctx.respond(embed=Embed(title="",
                                      description="Вы не можете кикнуть себя!", color=Color.red()), ephemeral=True)
    else:
        try:
            if ctx.author.top_role > user.top_role:
                try:
                    embed = Embed(title="", color=Color.default(),
                                  description=f"Пользователь {user.mention} был кикнут с сервера.", )
                    embed.add_field(name="Модератор", value=ctx.author.mention, inline=True)
                    embed_log = Embed(title="Пользователь кикнут", color=0x7b68ee)
                    embed_log.add_field(name="Автор", value=ctx.author.mention, inline=True)
                    if причина:
                        embed.add_field(name="Причина", value=причина)
                        embed_log.add_field(name="Причина", value=причина)
                    else:
                        pass
                    await ctx.respond(embed=embed)
                    await send_log(ctx.guild.id, embed=embed_log)
                    await user.kick(reason=причина)
                except discord.Forbidden:
                    await ctx.respond("У меня нет прав на кик этого пользователя!", ephemeral=True)
            else:
                await ctx.respond(f"Вы не можете кикнуть этого пользователя!", ephemeral=True)
        except Exception as e:
            print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
                  f"`{ctx.author.id}`\nКоманда: kick")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас нет необходимых прав для использования этой команды.", ephemeral=True)
    elif isinstance(error, AttributeError):
        await ctx.response.send_message("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
    else:
        await ctx.send(f"Произошла ошибка: {str(error)}")
        raise error


@roles.command(name="color", description="Изменить цвет роли")
async def _change_role_color(ctx, роль: discord.Option(discord.Role, description="Какой роли изменить цвет"),
                             цвет: discord.Option(
                                 discord.Color,description="Цветовой код в формате HEX (например #fe3a3 или 0xfe3a3)")):
    try:
        if ctx.author.guild_permissions.manage_roles:
            if ctx.guild is None:
                await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
                return
            if роль:
                if ctx.author.top_role > роль:
                    try:
                        embed = Embed(title="Цвет роли изменен", color=0x7b68ee)
                        old_color = роль.color
                        await роль.edit(color=цвет)
                        embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                        embed.add_field(name="Роль", value=f"{роль.mention} ({роль.name})", inline=True)
                        embed.add_field(name="Прошлый цвет", value=str(old_color), inline=False)
                        embed.add_field(name="Новый цвет", value=str(цвет))
                        await ctx.response.send_message(f"Цвет роли «{роль.name}» изменен на «{цвет}»", ephemeral=True)
                        await send_log(ctx.guild.id, embed=embed)
                    except discord.Forbidden:
                        await ctx.response.send_message("У меня нет прав на изменение цвета этой роли", ephemeral=True)
                    except discord.ext.commands.errors.BadColourArgument:
                        await ctx.response.send_message("Неверный цвет. Пожалуйста, введите цвет в формате "
                                                        "HEX (например, `#32a852`)", ephemeral=True)
                else:
                    await ctx.response.send_message(
                        f"{ctx.author.mention}, Вы не можете изменить цвет роли, которая выше Вашей.", ephemeral=True)
            else:
                await ctx.response.send_message(f"Роль с именем «{роль.name}» не найдена", ephemeral=True)
        else:
            await ctx.respond(embed=Embed(description="У вас нет прав управлять ролями!",color=0x7b68ee),ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: rcolor")
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)


@roles.command(name="pre", description="Изменить приоритет роли")
async def _pre(ctx, роль: discord.Option(discord.Role, description="Какую роль переместить"),
               pos: discord.Option(int, description="На какую позицию переместить роль")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.top_role >= роль:
            if not роль:
                await ctx.response.send_message('Роль не найдена', ephemeral=True)
                return
            try:
                await роль.edit(position=pos)
                await ctx.response.send_message(f'«{роль.name}» перемещена на позицию {pos}.')
            except discord.Forbidden:
                await ctx.response.send_message('У меня нет прав для изменения приоритета для этой роли',
                                                ephemeral=True)
        else:
            await ctx.response.send_message(
                f"{ctx.author.mention}, Вы не можете переместить роль, которая выше Вашей роли.", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)
        return


@roles.command(name="add", description="Выдать роль пользователю")
async def _give_role(ctx, user: discord.Option(discord.Member, description="Кому выдать роль"),
                     роль: discord.Option(discord.Role, description="Какую роль выдать")):
    try:
        if ctx.guild is not None:
            if ctx.author.guild_permissions.manage_roles:
                if ctx.author.top_role >= роль:
                    if роль:
                        try:
                            embed = Embed(title="Пользователю выдана роль", color=0x7b68ee)
                            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
                            embed.add_field(name="Роль", value=f"{роль.mention} ({роль.name})")
                            await user.add_roles(роль)
                            await ctx.response.send_message(f'Роль «{роль.name}» выдана пользователю: {user.mention}',
                                                            ephemeral=True)
                            await send_log(ctx.guild.id, embed=embed)
                        except discord.Forbidden:
                            await ctx.response.send_message('У меня нет прав для выдачи этой роли', ephemeral=True)
                    else:
                        await ctx.response.send_message(f'Роль с именем «{роль.name}» не найдена.', ephemeral=True)
                else:
                    await ctx.respond(f'{ctx.author.mention}, Вы не можете выдать роль, которая выше вашей роли.',
                                      ephemeral=True)
            else:
                await ctx.respond("У вас недостаточно прав!", ephemeral=True)
        else:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)


@roles.command(name="remove", description="Удалить роль у пользователя")
async def _remove_role(ctx, user: discord.Option(discord.Member, description="У кого нужно забрать роль"),
                       роль: discord.Option(discord.Role, description="Какую забрать роль")):
    try:
        if user == ctx.author:
            await ctx.respond("Вы не можете удалять свои же роли!", ephemeral=True)
            return
        if ctx.guild is not None:
            if ctx.author.guild_permissions.manage_roles:
                if ctx.author.top_role > роль:
                    if user and роль:
                        if роль:
                            try:
                                embed = Embed(title="У пользователя забрана роль", color=0x7b68ee)
                                embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
                                embed.add_field(name="Роль", value=f"{роль.mention} ({роль.name})")
                                await user.remove_roles(роль)
                                await ctx.respond(f'Роль «{роль.name}» удалена у {user.mention}', ephemeral=True)
                                await send_log(ctx.guild.id, embed=embed)
                            except discord.Forbidden:
                                await ctx.respond('У меня нет прав для удаления этой роли', ephemeral=True)
                        else:
                            await ctx.respond("Роль не найдена", ephemeral=True)
                    else:
                        await ctx.respond("Роль или пользователь не найдены", ephemeral=True)
                else:
                    await ctx.respond(f"{ctx.author.mention}, Вы не можете забрать роль, которая выше вашей роли.",
                                      ephemeral=True)
            else:
                await ctx.respond("У вас недостаточно прав!", ephemeral=True)
        else:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)


@bot.slash_command(name="nick", description="Изменить ник пользователю")
async def _nick(ctx, user: discord.Option(discord.Member, "Кому изменить ник"),
                ник: discord.Option(str, "Новый ник пользователя")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.manage_nicknames:
            return 
        if ctx.author.top_role > user.top_role:
            embed = Embed(title="Пользователю изменён ник", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            embed.add_field(name="Прошлый ник", value=user.nick, inline=True)
            embed.add_field(name="Новый ник", value=ник)
            await user.edit(nick=ник)
            await ctx.response.send_message(f"Пользователю {user.name} изменён ник на: {ник}", ephemeral=True)
            await send_log(ctx.guild.id, embed=embed)
    except discord.Forbidden:
        await ctx.response.send_message("У меня нет прав на изменение ника этого пользователя", ephemeral=True)


@roles.command(name="up", description='Повысить роль пользователя на 1 уровень')
async def _uprole(ctx, member: discord.Option(discord.Member, "Кому повысить роль")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return

        if member == ctx.author:
            await ctx.response.send_message(embed=Embed(description="Вы не можете повышать свою роль!", color=0x7b68ee),
                                            ephemeral=True)
            return

        if ctx.author.guild_permissions.manage_roles:
            if ctx.author.top_role > member.top_role:
                guild = ctx.guild
                roles = [role for role in member.roles if role != guild.default_role]
                highest_role = max(roles, key=lambda x: x.position)
                new_role = discord.utils.get(guild.roles, position=highest_role.position + 1)
                await member.add_roles(new_role)
                await member.remove_roles(highest_role)
                await ctx.response.send_message(f'Пользователю {member.mention} ({member.id}) повышен ранг '
                                                f'до: {new_role.name} ({new_role.id})', ephemeral=True)
                embed = Embed(title="Пользователю повышен ранг", color=0x7b68ee)
                embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
                embed.add_field(name="Прошлая роль", value=highest_role.mention, inline=True)
                embed.add_field(name="Новая роль", value=new_role.mention, inline=True)
                await send_log(ctx.guild.id, embed=embed)
            else:
                await ctx.response.send_message(f"Вы не можете повысить роль которая вышей вашей роли.", ephemeral=True)
        else:
            await ctx.respond("У вас недостаточно прав!", ephemeral=True)
    except PermissionError:
        await ctx.response.send_message("У меня недостаточно прав!", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: uprole")


@roles.command(name="do", description="Понизить роль пользователя на 1 уровень")
async def _do(ctx, member: discord.Option(discord.Member, description="Кому понизить роль")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if member == ctx.author:
            await ctx.response.send_message(embed=Embed(description="Вы не можете понижать свою роль!", color=0x7b68ee),
                                            ephemeral=True)
            return

        if ctx.author.top_role > member.top_role:
            highest_role = member.top_role
            roles = ctx.guild.roles
            new_role_position = highest_role.position - 1
            new_role = discord.utils.get(roles, position=new_role_position)
            await member.add_roles(new_role)
            await member.remove_roles(highest_role)
            await ctx.response.send_message(f'Пользователю {member.mention} ({member.id}) понижен ранг '
                                            f'до: {new_role.name} ({new_role.id})')
        else:
            await ctx.response.send_message(f"Вы не можете понизить роль которая выше вашей.", ephemeral=True)
    except PermissionError:
        await ctx.response.send_message("У меня недостаточно прав!", ephemeral=True)


@roles.command(name="clear", description="Удалить все роли пользователя")
async def _rclear(ctx, member: discord.Option(discord.Member, description="У кого очистить роли")):
    try:
        if not ctx.guild:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if member == ctx.author:
            await ctx.response.send_message(embed=Embed(description="Вы не можете удалять свои роли!", color=0x7b68ee),
                                            ephemeral=True)
            return
        if ctx.author.top_role >= member.top_role:
            roles = member.roles
            embed = Embed(title="Роли пользователя очищены", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            roles.reverse()
            role_names = []
            for role in roles:
                if role != ctx.guild.default_role:
                    role_names.append(role.name)
                    await member.remove_roles(role)
            embed.add_field(name="Роли пользователя", value=', '.join(role_names), inline=False)
            await ctx.respond(f"Все роли пользователя {member.display_name} удалены", ephemeral=True)
            await send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond(f"Вы не можете очистить роли этого пользователя.", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав для удаления ролей!", ephemeral=True)
    except Exception as e:
        await print(f"Произошла ошибка: {str(e)}")


@bot.slash_command(name="jn")
@commands.is_owner()
async def _jn(ctx):
    author_voice_state = ctx.author.voice
    if author_voice_state:
        voice_channel = author_voice_state.channel
        await voice_channel.connect()
        await ctx.response.send_message(f'Joined voice channel: {voice_channel}', ephemeral=True)
    else:
        await ctx.response.send_message('You are not connected to a voice channel.', ephemeral=True)


@bot.slash_command(name='ping')
@commands.is_owner()
async def ping(ctx):
    ping = bot.latency
    await ctx.response.send_message(f"The bot ping is: {round(ping * 1000)}ms!")


@bot.slash_command(name="system")
@commands.is_owner()
async def _system(ctx, command: str):
    os.system(f"{command}")
    await ctx.response.send_message("+")


ds_roles = {
    "× Мл.Модератор Дискорда": "× Модератор Дискорда",
    "× Модератор Дискорда": "× Ст.Модератор Дискорда",
    "× Ст.Модератор Дискорда": "× Гл.Модератор Дискорда",
    "× Гл.Модератор Дискорда": "× Мл.Администратор Дискорда",
    "× Мл.Администратор Дискорда": "× Администратор Дискорда",
    "× Администратор Дискорда": "× Гл.Администратор Дискорда"
}


@bot.slash_command(
    name="dsup",
    guild_ids=[1138204059397005352]
)
async def dsup(ctx: discord.Interaction, user: discord.Member,
               d_role: discord.Option(str, choices=list(ds_roles.keys()))):
    current_role = None
    for role in user.roles:
        if role.name in ds_roles:
            current_role = role
            break

    if current_role:
        if ds_roles[current_role.name] == d_role:
            action = "повышен(а) до"
        elif current_role.name == d_role:
            await ctx.response.send_message(f"{user.mention} уже имеет роль {d_role}.", ephemeral=True)
            return
        else:
            action = "понижен(а) до"
        next_role = discord.utils.get(ctx.guild.roles, name=d_role)
        await user.remove_roles(current_role)
        await user.add_roles(next_role)
        embed = discord.Embed(
            title=f"Новости Дискорд персонала HightMine за {date.today().strftime('%d.%m.%Y')}",
            description="", color=0x7b68ee)
        embed.add_field(name="", value=f"{user.mention} {action} должности {next_role.name}", inline=False)
        embed.add_field(name="", value=f"-# *Предыдущая должность: {current_role.name}", inline=False)
        embed.add_field(name="", value="", inline=False)
        embed.add_field(name="Желаем успехов в развитии!", value="", inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.response.send_message(embed=embed)
    else:
        await ctx.response.send_message(f"{user.mention} не имеет подходящей текущей роли.", ephemeral=True)


@bot.slash_command(name="stop")
@commands.is_owner()
async def _stop(ctx):
    await ctx.response.send_message("+", ephemeral=True)
    await bot.close()


@bot.slash_command(name="munreg", guild_ids=[1138204059397005352])
async def munreg_command(ctx, member: discord.Member, reason=None):
    admin_roles = [1219899085855789056, 1228593717586427987, 1220095527547437116]
    for admin_role in ctx.author.roles:
        if admin_role.id in admin_roles:
            try:
                channel = bot.get_channel(1225454618763595997)
                channel2 = bot.get_channel(1282715295995138129)
                role_mapping = {
                    1223995125487632486: "× Мл.Модератор Дискорда",
                    1223995222086651914: "× Модератор Дискорда",
                    1223995448793108632: "× Ст.Модератор Дискорда",
                    1223995309651263524: "× Гл.Модератор Дискорда",
                    1220095527547437116: "× Мл.Администратор Дискорда",
                    1228593717586427987: "× Администратор Дискорда",
                    1219899085855789056: "× Гл.Администратор Дискорда"}
                embed = discord.Embed(title="", description=f"Новости дискорд персонала HightMine за {date.today()}\n",
                                      color=discord.Color.default())
                embed2 = discord.Embed(title="", description=f"Пользователь: {member.mention} | `{member.id}`",
                                       color=discord.Color.default())
                for role in member.roles:
                    if role.id in role_mapping:
                        role_name = role_mapping[role.id]
                        embed.add_field(name=f"Снят с должности «{role_name}»", value=f"{member.mention}", inline=False)
                        embed2.add_field(name="", value=f"Должность: <@&{role.id}> | `{role.id}`", inline=False)
                embed2.add_field(name="", value=f"Причина ухода: {reason if reason else 'По решению ВА'}")
                embed.add_field(name="", value=f"Причина: {reason}" if reason else "Причина: Не указана")
                embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
                embed.set_thumbnail(url=member.avatar.url)
                await channel.send("||<@&1220265238083928176>||", embed=embed)
                await channel2.send(embed=embed2)
                await ctx.response.send_message("Успешно!", ephemeral=True)
                roles = [1219596842698801193, 1223995125487632486, 1223995222086651914, 1223995448793108632,
                         1223995309651263524,
                         1220095527547437116, 1228593717586427987]
                highest_role = None
                for role in roles:
                    role_obj = ctx.guild.get_role(role)
                    if role_obj in member.roles:
                        if highest_role is None or role_obj.position > highest_role.position: highest_role = role_obj
                if highest_role is not None:
                    for role in roles:
                        role_obj = ctx.guild.get_role(role)
                        await member.remove_roles(role_obj)
            except Exception as e:
                print(f"Произошла ошибка:\n{e}\n"
                      f"Сервер: {ctx.guild.name}\n"
                      f"Пользователь: {ctx.author.mention} | "
                      f"`{ctx.author.id}`\nКоманда: munreg")


def check_access(ctx):
    return (any(role.id in data_as['allowed_roles'] for role in ctx.author.roles) or ctx.author.id in
            data_as['allowed_users'])


@bot.slash_command(name="unreg", guild_ids=[1263854530445971671], description="Снять с должности")
@commands.check(check_access)
async def _unreg(ctx, member: discord.Option(discord.Member, description="Кого снять"),
                 reason: discord.Option(str, description="Причина снятия", default=False)):
    try:
        channel = bot.get_channel(1263869130705076305)
        embed = Embed(title="", description=f"Новости персонала HightMine за "
                                            f"{date.today().strftime('%d.%m.%Y')}\n",color=Color.default())
        sections = {
            1263856989499424818: "Tech Section", 1264230599733018656: "Recruiting Section",
            1263856995828760690: "Method Section", 1264230586013323366: "Teaching Section",
            1263856994750697635: "Forum Section", 1263856995157545043: "Support Section",
            1263863513693032459: "Media Section", 1264641554287427656: "Resource Section",
            1263854784969183303: "Build Section", 1263856988937261076: "Event Section",
            1263867286901751818: "GP Section"}
        highest_role = max([role for role in member.roles if role != ctx.guild.default_role], key=lambda r: r.position)
        embed.add_field(name=f"Снят с должности «{highest_role.name}»", value=f"{member.mention}", inline=False)
        user_roles = [role for role in member.roles if role != ctx.guild.default_role]
        if user_roles:
            embed.add_field(name="Роли", value=", ".join([role.name for role in user_roles]), inline=False)
        user_sections = [sections[role.id] for role in member.roles if role.id in sections]
        if user_sections:
            embed.add_field(name="Секции", value=", ".join(user_sections), inline=False)
        embed.add_field(name="", value=f"Причина: {reason}" if reason else "Причина: Не указана")
        embed.set_footer(text=f"@{ctx.author.name}", icon_url=ctx.author.avatar.url)
        await channel.send(embed=embed)
        await ctx.response.send_message("Успешно!", ephemeral=True)
        await member.remove_roles(*[role for role in member.roles if role != ctx.guild.default_role])
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"{ctx.author.id}\nКоманда: /unreg")


@roles.command(name="create", description="Создать роль")
async def createrole(ctx, роль: discord.Option(str, description="Название роли"),
                     цвет: discord.Option(discord.Color, description="Цвет для роли", required=False)):
    if bot.user in [member for member in ctx.guild.members if member.bot]:
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            created_role = await guild.create_role(name=роль, colour=цвет if цвет else Color.default())
            await ctx.response.send_message(f"Роль «{роль}» создана.")
            embed = Embed(title="Роль создана", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            embed.add_field(name="Роль", value=f"{created_role.mention} ({created_role.name})", inline=False)
            embed.set_footer(text=f"role id: {created_role.id}")
            await send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond(embed=Embed(title="",description="У вас недостаточно прав",color=0x7b68ee),ephemeral=True)
    else:
        await ctx.respond(embed=Embed(title="",description="Для использования этой команды добавьте меня на сервер!",
                                      color=Color.default()))


@bot.slash_command(name="reg", description="Сообщение о принятии на должность", guild_ids=[1263854530445971671])
@commands.check(check_access)
async def _reg(ctx, member: discord.Option(discord.Member, description="Укажите участника"),
               выдать_роли: discord.Option(discord.Role, description="Выдать роль на основании должности"),
               комментарий: discord.Option(str, description="Комментарий к сообщению")):
    try:
        channel = bot.get_channel(1263855526798692392)
        embed = Embed(title="", description=f"Новости персонала HightMine за {date.today().strftime('%d.%m.%Y')}",
                      color=Color.default())
        embed.add_field(name="", value=f"{member.mention} принят на должность «{выдать_роли.name}»")
        if комментарий: embed.add_field(name="Комментарий", value=комментарий, inline=False)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await channel.send(embed=embed)
        await member.add_roles(выдать_роли)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: mute")


@bot.slash_command(name="guilds", guild_ids=[1214617864863219732, 1148996038363975800])
@commands.is_owner()
async def guilds(ctx: discord.Interaction):
    try:
        for guild in bot.guilds:
            if guild.get_member(ctx.author.id) is None:
                channel = guild.system_channel or next(
                    (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
                if channel:
                    invite = await channel.create_invite(max_age=3600)
                    await ctx.send(f"Sending invite to {guild.name} | `{guild.owner.name}({guild.owner_id})`: "
                                   f"\n{invite.url}")
                else:
                    await ctx.response.send_message(f"Cannot send invite to {guild.name} (no suitable channel)")
    except Exception as e:
        print(f"Произошла ошибка:\n{e}")


last_used = {}


@bot.slash_command(name="8ball", description='Сыграть в игру на кик с сервера', guild_only=True)
async def eight_ball(ctx):
    user_id = ctx.author.id
    current_time = time.time()
    one_day = 86400
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if user_id in last_used and current_time - last_used[user_id] < one_day:
        next_use_time = last_used[user_id] + one_day
        await ctx.response.send_message(f"До следующего использования команды осталось: <t:{int(next_use_time)}:R>")
        return
    last_used[user_id] = current_time
    if not ctx.guild.me.guild_permissions.kick_members:
        await send_log(ctx.guild.id,
                       f"У меня нет прав чтобы кикнуть проигравшего пользователя в 8ball! ({ctx.author.mention})")
        return
    if random.randint(1, 10) == 1:
        try:
            await ctx.response.send_message(f"{ctx.author.mention}, Не повезло и он кикнут с сервера!")
            await ctx.author.kick(reason="Проиграл в 8ball")
            await ctx.author.send("Вы проиграли в игре 8ball и были кикнуты с сервера!")
        except discord.Forbidden:
            await ctx.response.send_message(f"У меня нет прав чтобы кикнуть проигравшего "
                                            f"пользователя в 8ball! ({ctx.author.mention})")
    else:
        await ctx.response.send_message("Вам повезло!")


data = {
    "BASE_URL": "https://shikimori.one/api"
}


def get_characters_from_html(anime_id):
    url = f"https://shikimori.one/animes/{anime_id}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; DiscordBot/1.0)"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        characters_div = soup.find('div', class_='cc-characters')
        characters = []
        if characters_div:
            character_elements = characters_div.find_all('article')
            for char in character_elements:
                name_ru = char.find('span', class_='name-ru')
                name_ru = name_ru.get_text(strip=True) if name_ru else "Неизвестно"
                name_en = char.find('span', class_='name-en')
                name_en = name_en.get_text(strip=True) if name_en else "Неизвестно"
                image = char.find('meta', itemprop='image')
                image_url = image['content'] if image else None
                characters.append({
                    'name_ru': name_ru,
                    'name_en': name_en,
                    'image': image_url
                })
        return characters
    else:
        print(f"Ошибка получения данных: {response.status_code}")
        return None


def search_anime_by_title(title):
    url = f"{data_as['BASE_URL']}/animes"
    params = {"search": title, "limit": 25}
    headers = {"User-Agent": "remod3 (slenderzet@gmail.com)"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка поиска аниме по названию: {response.status_code}, {response.text}")
        return None


def clean_description(description):
    cleaned_description = re.sub(r'\[.*?\]', '', description)
    return cleaned_description


class AnimeSelect(Select):
    def __init__(self, anime_results):
        options = [
            discord.SelectOption(
                label=f"{anime['russian'][:97]}..." if len(anime['russian']) > 100 else anime['russian'],
                value=str(anime['id'])) for anime in anime_results[:25]]
        super().__init__(placeholder="Выберите аниме", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        anime_id = self.values[0]
        anime_details = self.get_anime_details(anime_id)
        if anime_details and isinstance(anime_details, dict):
            image_url = "https://shikimori.one" + anime_details['image']['original']
            description = anime_details.get('description', 'Описание недоступно')
            cleaned_description = clean_description(description) if description else 'Описание недоступно'
            embed = discord.Embed(title=f"{anime_details.get('russian', 'Без названия')} "
                                        f"({anime_details.get('name', 'Без ориг. названия')})",
                                  description=cleaned_description, color=discord.Color.default())
            embed.add_field(name="Год выхода", value=anime_details.get('aired_on', 'Неизвестно'))
            embed.add_field(name="Статус", value=anime_details.get('status', 'Неизвестно'))
            embed.add_field(name="Количество эпизодов", value=anime_details.get('episodes', 'Неизвестно'))
            embed.set_thumbnail(url=image_url)
            button = discord.ui.Button(label="Главные герои", style=discord.ButtonStyle.primary)
            button.callback = lambda inter: self.show_characters(inter, anime_id)
            view = discord.ui.View()
            view.add_item(button)
            await interaction.response.edit_message(content="Информация о выбранном аниме:", embed=embed, view=view)
        else:
            await interaction.response.send_message(f"Не удалось получить информацию о выбранном аниме. "
                                                    f"({anime_id})", ephemeral=True)

    @staticmethod
    async def on_error(error: Exception, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                f"`remodik`\n\n{error}")

    async def show_characters(self, interaction, anime_id):
        characters = get_characters_from_html(anime_id)
        if characters and len(characters) > 0:
            embed = discord.Embed(title="Главные герои", color=discord.Color.blue())
            view = discord.ui.View()
            for char in characters:
                name = f"{char['name_ru']} ({char['name_en']})"
                embed.add_field(name=name, value="Персонаж", inline=True)
                button = discord.ui.Button(label=char['name_ru'], style=discord.ButtonStyle.secondary)
                button.callback = lambda inter, char_info=char: self.show_character_info(inter, char_info)
                view.add_item(button)
            await interaction.response.send_message(content="Главные герои:", embed=embed, view=view, ephemeral=True)
        else:
            await interaction.response.send_message("Не удалось получить героев. Данные отсутствуют.", ephemeral=True)

    @staticmethod
    async def show_character_info(interaction, char_info):
        embed = discord.Embed(title=char_info['name_ru'], color=discord.Color.default())
        embed.add_field(name="Имя на английском", value=char_info['name_en'], inline=False)
        if char_info['image']:
            embed.set_thumbnail(url=char_info['image'])
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @staticmethod
    def get_animation_characters(anime_id):
        url = f"{data_as['BASE_URL']}/animes/{anime_id}/characters"
        headers = {"User-Agent": "remod3 (slenderzet@gmail.com)"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return response.json()
        return None

    @staticmethod
    def get_anime_details(anime_id):
        url = f"{data_as['BASE_URL']}/animes/{anime_id}"
        headers = {"User-Agent": "remod3 (slenderzet@gmail.com)"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200: return response.json()
        return None


def l_mod_data():
    if os.path.exists("json/mod_data.json"):
        with open("json/mod_data.json", "r") as f:
            return json.load(f)


def s_mod_data(m_data):
    with open("json/mod_data.json", "w") as f:
        json.dump(m_data, f, indent=4)


mod_com = discord.SlashCommandGroup(name="mod", description="", guild_only=True)


@mod_com.command(name="add", description="Добавить модерацию")
async def add_mod(ctx: discord.ApplicationContext, member: discord.Member = None, role: discord.Role = None):
    guild_id = str(ctx.guild.id)
    if member:
        member_id = str(member.id)
    if role:
        role_id = str(role.id)
    mod_data = l_mod_data()
    if guild_id not in mod_data:
        mod_data[guild_id] = []
    mod_data[guild_id].append({
        "member_id": member_id,
        "role_id": role_id
    })
    s_mod_data(mod_data)
    await ctx.response.defer()
    try:
        if ctx.author.id == ctx.guild.owner_id:
            embed = Embed(title="Обновление участников модерации",
                          color=0x7b68ee)
            if member:
                embed.add_field(name="Модератор", value=f"{member.mention} ({member.name})", inline=True)
            if role:
                embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=False)
            await ctx.followup.send(embed=embed)
    except Exception as e:
        print(f"Ошибка в mod add\n\n\n{e}")


class AnimeSelectView(View):
    def __init__(self, anime_results):
        super().__init__(timeout=None)
        self.add_item(AnimeSelect(anime_results))

        async def on_error(self, error: Exception, interaction: discord.Interaction) -> None:
            await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                    f"`remodik`\n\n{error}")


@bot.slash_command(name="anime", description="Поиск информации об аниме")
async def anime(ctx, name: discord.Option(str, description="Название аниме")):
    try:
        await ctx.response.defer(ephemeral=True)
        anime_results = search_anime_by_title(name)
        if anime_results and isinstance(anime_results, list) and len(anime_results) > 0:
            view = AnimeSelectView(anime_results)
            await ctx.followup.send("Выберите аниме из списка:", view=view, ephemeral=True)
        else:
            await ctx.followup.send("Аниме не найдено или произошла ошибка.", ephemeral=True)
    except Exception as e:
        await ctx.followup.send("Произошла неизвестная ошибка!", ephemeral=True)
        await admin.send(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
                         f"`{ctx.author.id}`\nКоманда: anime")


@bot.slash_command(name="avatar", description="Получить аватар пользователя или сервера")
async def _avatar(ctx: discord.ApplicationContext,
                  user: Option(discord.Member, description="Выберите пользователя", required=False),
                  guild: Option(description="Аватар сервера", choices=["guild"], required=False)):
    if user: avatar_url = user.avatar.url if user.avatar else "У пользователя нет аватара."
    if user:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        else:
            avatar_url = user.avatar.url
    elif guild:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        else:
            avatar_url = ctx.guild.icon.url if ctx.guild.icon else "У сервера нет аватара."
    else:
        avatar_url = ctx.author.avatar.url if ctx.author.avatar else "У вас нет аватара."
    await ctx.response.send_message(avatar_url)


@roles.command(name="replace", description='Заменить роль у пользователя')
async def replace(ctx, member: discord.Option(discord.Member, "У кого заменить роль"),
                  prev_role: discord.Option(discord.Role, "Предыдущая роль пользователя"),
                  new_role: discord.Option(discord.Role, "Новая роль пользователя")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.top_role > new_role:
            if prev_role not in member.roles:
                await ctx.respond(f'{member.mention} не имеет роли {prev_role.name}')
                return
            if member == ctx.author:
                await ctx.response.send_message("Вы не можете заменять свои же роли!", ephemeral=True)
                return
            await member.remove_roles(prev_role)
            await member.add_roles(new_role)
            await ctx.respond(f'Вы заменили роль пользователя {member.mention} с '
                              f'«{prev_role.mention}» на роль «{new_role.mention}»')
            await send_log(ctx.guild.id, f"{ctx.author.mention} Заменил роль пользователя {member.mention} с "
                                         f"«{prev_role.mention}» на роль «{new_role.mention}».")
        else:
            await ctx.respond(f"Вы не можете заменить роль, которая выше вашей.", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: "
              f"{ctx.author.mention} | `{ctx.author.id}`\nКоманда: replace")


class MyRep(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label='Ник', style=discord.InputTextStyle.short,
                                           placeholder='Ваш ник на сервере', custom_id="nickname"))
        self.add_item(discord.ui.InputText(label='Ник нарушителя', style=discord.InputTextStyle.short, max_length=40,
                                           custom_id="black_nick"))
        self.add_item(discord.ui.InputText(label='Правило', style=discord.InputTextStyle.short,
                                           placeholder="Пункт правил который нарушил игрок", max_length=300,
                                           custom_id="rules"))
        self.add_item(
            discord.ui.InputText(label='Описание нарушения', style=discord.InputTextStyle.long, max_length=300))
        self.add_item(discord.ui.InputText(label='Ссылка на доказательство', style=discord.InputTextStyle.short,
                                           max_length=300, custom_id="description_label"))

    async def callback(self, interaction: discord.Interaction):
        answers = [item.value for item in self.children]
        embed = discord.Embed(title=f"Новая жалоба от пользователя: {interaction.user}",
                              color=discord.Color.brand_green())
        embed.add_field(name='Его ник:', value=answers[0], inline=False)
        embed.add_field(name='Ник нарушителя:', value=answers[1], inline=False)
        embed.add_field(name='Нарушенный Пункт правил', value=answers[2], inline=False)
        embed.add_field(name='Описание нарушения:', value=answers[3], inline=False)
        embed.add_field(name='Ссылка на доказательство:', value=answers[4], inline=False)
        embed.add_field(name='', value=f'User: {interaction.user.mention}\nID: {interaction.user.id}', inline=False)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        channel = bot.get_channel(1236274747910783057)
        await channel.send(embed=embed)
        await interaction.response.send_message("Ваша жалоба успешно отправлена!", ephemeral=True)

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                f"`remodik`\n\n{error}")


@bot.slash_command(name="report", description='Отправить жалобу на игрока', guild_ids=[1138204059397005352])
async def _report_(ctx):
    reps = MyRep(title="Жалоба")
    await ctx.send_modal(reps)


last_mention_time = 0
mention_cooldown = 120


@bot.slash_command(name="ru", guild_ids=[1138204059397005352])
async def _send_r(ctx):
    if not ctx.author.guild_permissions.administrator:
        return
    embed = discord.Embed(title="Правила сервера Discord",
                          description="> Наш сервер придерживается правил Discord Terms of Service и Discord Community "
                                      "Guidelines, поэтому настоятельно советуем вам с ними ознакомиться.\n\n"
                                      "- [Условия предоставления услуг Discord](https://discord.com/terms)\n"
                                      "- [Правила сообщества Discord](https://discord.com/guidelines)",
                          color=discord.Color.default(), type="rich")
    view_rule = RuleView()
    embed.set_image(
        url="https://sun9-78.userapi.com/impf/gMIhKf4uPQHEDtCrB4Ek4OJFrKodmk7yn-Z4LQ/5dGftKsMKZ8.jpg?size=1590x530"
            "&quality=95&crop=262,0,1200,400&sign=07f3df3002e602c971c6ae8d6c90826a&type=cover_group")
    await ctx.send(embed=embed, view=view_rule)


class RuleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.custom_id = "rule"

    @discord.ui.select(
        placeholder="Выбери нужный свод правил",
        min_values=1,
        max_values=1,
        custom_id="rule",
        options=[
            discord.SelectOption(
                label="Общее положение",
                emoji=discord.PartialEmoji(
                    name="3709rulesbook",
                    id=1199732396208164864
                )
            ),
            discord.SelectOption(
                label="Правила Текстовых каналов",
                emoji=discord.PartialEmoji(
                    name="3709rulesbook",
                    id=1199732396208164864
                )
            ),
            discord.SelectOption(
                label="Правила Голосовых каналов",
                emoji=discord.PartialEmoji(
                    name="3709rulesbook",
                    id=1199732396208164864
                )
            ),
            discord.SelectOption(
                label="Дополнительная информация",
                emoji=discord.PartialEmoji(
                    name="3709rulesbook",
                    id=1199732396208164864
                )
            )
        ]
    )
    async def select_callback(self, select, interaction):
        embed1 = discord.Embed(title="", color=discord.Color.default(), type="rich")
        embed1.add_field(name="",
                         value='**Общее положение**\n\n'
                               '``1.1`` Находясь в дискорд сервере вы автоматически соглашаетесь с '
                               'правилами.\n'
                               '``1.2`` Незнание правил не освобождает вас от ответственности.\n'
                               '``1.3`` Если вы не согласны с выданным вам наказанием, то можете попробовать обжаловать'
                               ' ему в лс - <@743864658951274528>\n'
                               '``1.4`` Администрация дискорда в праве выдать наказания без объяснения '
                               'причин.\n'
                               '``1.5`` Все наказания могут суммироваться и складываться.\n'
                               '``1.6`` — Если игрок нарушил правило в дискорде, то модератор может выдать '
                               'предупреждение вместо мута. 3 предупреждения - мут на 4 часа. Предупреждения снимаются '
                               'через 7 дней.\n'
                               '``1.7`` — Попытка нарушения правил, тоже наказуема.\n'
                               '``1.8`` — Этот свод правил является не финальной версией и может меняться в любой '
                               'момент, без уведомления участников Discord\n\n', inline=False)
        embed1.add_field(name="",
                         value="``2.1`` Запрещается продажа/передача аккаунтов.\n"
                               "**Наказание: Бан навсегда**\n"
                               "> Дополнение: Взлом/Попытка взлома чужих аккаунтов, а также привязка этих аккаунтов, "
                               "тоже наказуема.\n\n"
                               "``2.2`` Запрещается использование/распространение запрещенного ПО.\n"
                               "Запрещены материалы (скриншоты/фото/видео) с наличием запрещенного ПО\n"
                               "**Наказание: мут 2 часа | мут на 1 день | бан 30 дней | бан навсегда**\n"
                               "> Дополнение: Фото/Видео где есть ЗПО: мут 1 день.\n"
                               "> Продажа ЗПО: бан 30 дней\n", inline=False)
        embed1.add_field(name="",
                         value="```2.3``` Запрещена коммерческая деятельность (продажа чего-либо за реальные"
                               "деньги/аметисты/игровую валюту)\n"
                               "**Наказание: Бан навсегда**\n"
                               "> Дополнение: Торговля за валюты и предметы других проектов также наказуема.\n\n"
                               "``2.4`` Запрещено обходить мут/бан путем перехода на другой аккаунт.\n"
                               "**Наказание: бан навсегда основного аккаунта, а так же твинка**\n\n"
                               "``2.5`` Запрещено ставить ники/автарки/описание аккаунта которые нарушают"
                               "правила Discord сервера\n\n"
                               "**Наказание: Просьба сменить ник/Аватарку/Описание - В случае отказа/игнора бан 5 "
                               "дней**\n"
                               "``2.6`` Провокация участников сервера на нарушение пользовательского "
                               "соглашения Discord.\n"
                               "**Наказание: бан: 30 дней**\n"
                               "> Пример: (Пацаны напишите что вам 11 лет)\n"
                               "> Дополнение:\n"
                               "> Признание своего возраста меньше 13 лет также будет караться вечным баном.",
                         inline=False)
        dop = discord.Embed(title="",
                            color=discord.Color.default())
        dop.add_field(name="", value="**Дополнительная информация**\n\n"
                                     "``1`` Наказание оспаривается 3 дня.\n"
                                     "``2`` Модератор по своему усмотрению может занизить норму наказания\n"
                                     "``3`` Если игрок находится в бане более 45 дней, его уровень/голосова активность "
                                     "может быть сброшена к 0. Без возможности восстановления\n"
                                     "``4`` Жалобы на модерацию от 3-тьих лиц не принимаются\n"
                                     "``5`` В случае бана аккаунта за 2.4, разбан требуется покупать на ВСЕ аккаунты.\n"
                                     "``6`` Если вы намеренно громко говорите, кричите, орете матом или неадекватно "
                                     "себя ведете или просто мешаете другим учатником в голосовом канале, модератор "
                                     "имеет полное право отключить вам микрофон на неопределенное время.\n",
                      inline=False)
        dop.add_field(name="",
                      value='``1.4.1`` Умышленное причинение вреда проекту или составу проекта | бан навсегда.\n'
                            '``1.4.2`` Администрация имеет право выдавать наказание за нарушения не указанных в своде '
                            'правил, если посчитает, что ваши действия приносят вред игрокам и/или проекту в целом.\n'
                            '``1.4.3`` Администрация имеет право самостоятельно устанавливать время и тяжесть наказания'
                            ', отличающееся от того, что указано в правиле, исходя из индивидуальной ситуации, а также '
                            'тяжести и частоты нарушений конкретного игрока или группы лиц, в первую очередь '
                            'руководствуясь здравым смыслом.', inline=False)
        embed2 = discord.Embed(title="Правила текстовых чатов", color=discord.Color.default(), type="rich")
        embed2.add_field(name="", value="``3.1`` Запрещено оскорбление/провокация участников/модерацию Discord/"
                                        "Модерацию сервера/Оскорбление проекта.\n"
                                        "**Наказание: warn 7d/мут 3/12 часов/бан 3 дня**\n"
                                        "> Дополнение:\n"
                                        "> Завуалированное оскорбление тоже является оскорблением.\n"
                                        "> Гифки с оскорблением так же наказуемы.\n"
                                        "> Целенаправленное оскорбление модерации Discord в личные сообщения |\n"
                                        "> мут 4 дня.\n"
                                        "> Запрещено оскорбление/упоминание проекта/Discord проекта в негативном "
                                        "контексте | мут 5 дней.\n"
                                        "> Запрещены угрозы в сторону участников дискорд сервера. | мут 3 часа. "
                                        "(Исключения игровые угрозы)\n"
                                        "> Оскорбление кого либо | 3 часа мута.\n"
                                        "> Оскорбление модерации сервера/Модерации Discord | 12 часов мута.\n\n",
                         inline=False)
        embed2.add_field(name="", value="``3.2`` Запрещено оскорбление/упоминание родных.\n"
                                        "**Наказание: мут 3 дня**\n"
                                        "> Дополнение\n"
                                        "> Гифки с оскорблением/упоминанием так же наказуемы.\n"
                                        "> Завуалированное оскорбление тоже является оскорблением.\n\n"
                                        "``3.3`` Запрещён флуд.\n"
                                        "**Наказание: warn 7d/мут 1 час**\n"
                                        "> Дополнение\n"
                                        "> От 3-ёх схожих по смыслу сообщений в 4 минуты.\n"
                                        "> Флуд символами | От 7 символов.\n"
                                        "> Смех: ахахахахах | От 14 символов.\n"
                                        "> От 4-ёх Больших/Маленьких смайликов в 1 сообщении.\n"
                                        "> Флуд гифками/смайликами/эмодзи/видео/фото тоже наказуем.", inline=False)
        embed2.add_field(name="", value="> Если на 1 скриншоте видно все 3 сообщения и даже если есть промежуток 4 "
                                        "минуты = Всё равно мут.\n"
                                        "> В 1 сообщении можно отправлять до 10 фотографий, но 2 подобных сообщения в "
                                        "течении 5 минут = мут.\n\n"
                                        "``3.4`` Запрещён тег администрации проекта.\n"
                                        "> К правилу относятся: люди с ролью Куратор и выше. Упом. роли - тоже мут.\n"
                                        "**Наказание: мут 3 дня.**\n\n", inline=False)
        embed2_1 = discord.Embed(title="", description="", color=discord.Color.default(), type="rich")
        embed2_1.add_field(name="", value="``3.5`` Запрещена реклама чего-либо, не относящегося к проекту.\n"
                                          "**Наказание: мут 1 день/бан 30 дней/бан навсегда**\n"
                                          "> Дополнение:\n"
                                          "> Запрещены ссылки на группы/сайты/Ютуб/телеграм каналы и т.д. | бан "
                                          "навсегда.\n"
                                          "> Запрещено упоминание серверов/не официальных ютуберов/телеграм каналов/"
                                          "сайтов и т.д. | мут 1 день.\n"
                                          "> Любая реклама/упоминание серверов копирующие механики HightMine | бан "
                                          "навсегда\n> Исключение: Hypixel.\n"
                                          "> Закрытые проекты обсуждать разрешено.\n"
                                          "> Ссылки на свои соц. сети разрешены.\n\n",
                           inline=False)
        embed2_1.add_field(name="", value="``3.6`` Запрещена выдача себя за администрацию|модерацию сервера/дискорда.\n"
                                          "**Наказание: warn 7d/мут 2 часа**\n"
                                          "> Дополнение:\n"
                                          "> Использование команд модерации | warn 7d/мут 2 часа\n\n"
                                          "``3.7`` Запрещена организация флуда.\n"
                                          "**Наказание: мут 2 часа**\n"
                                          "> Пример: Парни кто видел собаку пишите +\n\n", inline=False)
        embed2_1.add_field(name="", value="``3.8`` Запрещён капс.\n"
                                          "**Наказание: warn 7d/мут 1 час**\n"
                                          "> Дополнение:\n"
                                          "> От 50% сообщения капсом, а так же от 7 символов. Запрещено писать текста "
                                          "большими шрифтами и заголовками.\n"
                                          "> Не распространяется на игровые ники\n\n"
                                          "``3.9`` Запрещены сообщения не по теме канала/оффтоп.\n"
                                          "**Наказание: warn 7d/мут 30 минут/мут 12 часов.**\n"
                                          "> Дополнение:\n"
                                          "> Картинки, которые не относятся к теме канала.\n"
                                          "> Попрошайничество чего-либо | warn 7d\n"
                                          "> Попрошайничество не внутриигровых ресурсов/денег | мут 12 часов",
                           inline=False)
        embed2_1.add_field(name="", value="``3.10`` Запрещено отправлять скриншоты/фото/видео, содержащие информацию "
                                          "эротического/шокирующего характера и другой 18+ контент.\n"
                                          "**Наказание: warn 7d/мут 2 часа/мут 6 часов/бан 5d-15d**\n"
                                          "> Дополнение:\n"
                                          "> Аморальное поведение | warn 7d / Мут 1 час.\n"
                                          "> Сообщения сексуального/аморального характера | мут 2 часа\n"
                                          "> Запрещено отправлять фото/видео/гиф где есть скример | мут 6 часов.\n"
                                          "> Корректность сообщения определяется модератором\n\n"
                                          "``3.11`` Запрещено распространять информацию, которая вводит в заблуждение "
                                          "или обман/клевета/Информацию об игроках/Дюпах.\n"
                                          "**Наказание: warn 7d/мут 1 час/бан навсегда**\n"
                                          "> Дополнение:\n"
                                          "> Распространение/Продажа информации о дюпах | мут 3 часа\n"
                                          "> Слив личных данных участников Discord | бан навсегда", inline=False)
        embed2_1.add_field(name="", value="``3.12`` Запрещена пропаганда или агитация, возбуждающая социальную, расовую"
                                          ", национальную или религиозную ненависть и вражду.\n"
                                          "**Наказание: мут 8 часов**\n> Дополнение:\n"
                                          "> Запрещён нацизм, его символика и всё, что с ним связано;\n"
                                          "> Если сообщение содержит: Слава Украине/Слава (тп стран) - карается мутом "
                                          "(Исключение Слава Мерлоу)\n"
                                          "> Если сообщение содержит: Негр, хач, хохол, чурка - также карается мутом;\n"
                                          "> Все, что касается религии (кроме праздников) также наказуемо в зависимости"
                                          " от контекста сообщения игрока.\n"
                                          "> Так же запрещается призывать людей к суициду, или к любым другим опасным/"
                                          "нелегальным действиям\n"
                                          "> Упоминание психотропных веществ\n\n", inline=False)
        embed_voice = discord.Embed(title="Правила Голосовых каналов", description="",
                                    color=discord.Color.default(), type="rich")
        embed_voice.add_field(name="", value="``4.1`` Запрещено включать резкие, громкие звуки, кричать в микрофон или "
                                             "использовать Soundpad а так-же подключатся и отключатся от войса с целью "
                                             "создания громких звуков подключения и отключения. Спам звуковой панелью "
                                             "Так-же наказуемо.\n"
                                             "**Наказание: мут 12 часов**\n\n"
                                             "``4.2`` Запрещено транслировать контент с игры, на котором изображены "
                                             "читы.\n"
                                             "**Наказание: бан 30 дней**\n\n"
                                             "``4.3`` Запрещено транслировать сексуальный/шокирующий и другой 18+\n"
                                             "контент.\n"
                                             "**Наказание: бан 30 дней**\n\n"
                                             "**На войс распространяются все правила текстовых чатов**")
        if select.values[0] == "Общее положение":
            await interaction.response.send_message(embed=embed1, ephemeral=True)
        elif select.values[0] == "Правила Текстовых каналов":
            await interaction.response.send_message(embed=embed2, ephemeral=True)
            await interaction.followup.send(embed=embed2_1, ephemeral=True)
        elif select.values[0] == "Правила Голосовых каналов":
            await interaction.response.send_message(embed=embed_voice, ephemeral=True)
        elif select.values[0] == "Дополнительная информация":
            await interaction.response.send_message(embed=dop, ephemeral=True)


async def setup_views():
    view_rule = RuleView()
    bot.add_view(view_rule)


bot.loop.create_task(setup_views())


@bot.command(name='sos')
async def _sos(ctx):
    if ctx.guild.id in [1138204059397005352 or 1138400553081253948]:
        global last_mention_time
        cur_time = time.time()
        if ctx.guild.id == 1138400553081253948:
            role_id = 1285618374394511394
        elif ctx.guild.id == 1138204059397005352:
            role_id = 1219596842698801193
        time_since_last_mention = cur_time - last_mention_time
        embed = discord.Embed(title="", description="", color=discord.Color.green())
        if time_since_last_mention >= mention_cooldown:
            embed.add_field(name="",
                            value=f"{ctx.author.mention}, Вы вызвали модерацию! Ожидайте, скоро Вам помогут.")
            await ctx.reply(f"<@&{role_id}>\n", embed=embed)
            last_mention_time = cur_time
        else:
            time_remaining = mention_cooldown - time_since_last_mention
            unix_time = int(cur_time + time_remaining)
            await ctx.reply(f"{ctx.author.mention}, Вы сможете вызвать модерацию через <t:{unix_time}:R>.")


DATA_FILE_SYSTEM_CHANNELS = 'json/system_channels.json'


def load_data():
    if os.path.exists(DATA_FILE_SYSTEM_CHANNELS):
        with open(DATA_FILE_SYSTEM_CHANNELS, 'r+') as f: return json.load(f)
    return {}


def save_data(data):
    try:
        with open(DATA_FILE_SYSTEM_CHANNELS, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")


@bot.slash_command(name='set_system', description="Назначить канал для сообщений о входе/выходе игроков")
async def set_system(ctx, channel: discord.abc.GuildChannel):
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if not ctx.author.guild_permissions.administrator:
        return
    data = load_data()
    data[str(ctx.guild.id)] = channel.id
    save_data(data)
    await ctx.respond(f"Системный канал установлен: {channel.mention}")


@bot.event
async def on_member_join(member):
    data = load_data()
    channel_id = data.get(str(member.guild.id))
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(title="Пользователь присоединился к серверу", color=discord.Color.green())
            embed.add_field(name="Тег", value=member.mention, inline=False)
            embed.add_field(name="Имя пользователя", value=member.name, inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            await channel.send(f"{member.mention}, Добро пожаловать!", embed=embed)


@bot.event
async def on_member_remove(member):
    data = load_data()
    channel_id = data.get(str(member.guild.id))
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(title="Пользователь покинул сервер", color=discord.Color.red())
            embed.add_field(name="Тег", value=member.mention, inline=False)
            embed.add_field(name="Имя пользователя", value=member.name, inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            await channel.send(f"{member.mention} покинул сервер.", embed=embed)


def perm_ac(ctx: discord.AutocompleteContext):
    return [
        "create_instant_invite", "kick_members", "ban_members", "administrator", "manage_channels", "manage_guild",
        "view_audit_log", "view_guild_insights", "manage_roles", "manage_webhooks", "manage_emojis_and_stickers",
        "manage_events", "moderate_members", "read_messages", "send_messages", "send_tts_messages", "manage_messages",
        "embed_links", "attach_files", "read_message_history", "mention_everyone", "use_external_emojis",
        "use_external_stickers", "add_reactions", "connect", "speak", "stream", "use_vad", "priority_speaker",
        "mute_members",
        "deafen_members", "move_members", "request_to_speak", "manage_threads", "create_public_threads",
        "manage_emojis",
        "create_private_threads", "send_messages_in_threads", "use_embedded_activities", "use_application_commands"]


@roles.command(name='delperm', description='Забрать право для роли')
async def _delperm(ctx, роль: discord.Option(discord.Role, description="У какой роли забрать разрешение"),
                   perm: discord.Option(description="Разрешение для установки", autocomplete=perm_ac)):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.administrator:
            return 
        if ctx.author.top_role > роль:
            permissions = роль.permissions
            permissions.update(**{perm: False})
            await роль.edit(permissions=permissions)
            await ctx.response.send_message(f"Разрешение {perm} забрано для роли {роль.name}")
            await send_log(ctx.guild.id, f"{ctx.author.mention} забрал право `{perm}` у роли {роль.mention}")
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: setperm")


@roles.command(name='setperm', description='Установить право для роли')
async def _setperm(ctx, роль: discord.Option(discord.Role, description="Какой роли выдать разрешение"),
                   perm: discord.Option(str, description="Разрешение для установки", autocomplete=perm_ac)):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.administrator:
            return 
        if ctx.author.top_role > роль:
            permissions = роль.permissions
            permissions.update(**{perm: True})
            await роль.edit(permissions=permissions)
            await ctx.response.send_message(f"Разрешение {perm} установлено для роли {роль.name}")
            await send_log(ctx.guild.id, f"{ctx.author.mention} выдал право `{perm}` для роли {роль.mention}")
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: setperm")


class HelpRolesView(View):
    def __init__(self, embeds, page=0):
        super().__init__()
        self.embeds = embeds
        self.page = page

    async def update_message(self, interaction: Interaction):
        embed = self.embeds[self.page]
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.page == 0
        self.children[1].disabled = self.page == len(self.embeds) - 1

    @ui.button(label="Назад", style=discord.ButtonStyle.primary)
    async def back_button(self, button: Button, interaction: Interaction):
        if self.page > 0:
            self.page -= 1
            await self.update_message(interaction)

    @ui.button(label="Вперед", style=discord.ButtonStyle.primary)
    async def forward_button(self, button: Button, interaction: Interaction):
        if self.page < len(self.embeds) - 1:
            self.page += 1
            await self.update_message(interaction)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


@bot.slash_command(name="perms", description="Информация о разрешениях ролей")
async def help_roles(ctx: Interaction):
    embeds = [
        Embed(
            title="Информация о разрешениях ролей",
            description="**view_channels** - Позволяет участникам просматривать каналы (кроме приватных) по "
                        "умолчанию.\n"
                        "**manage_channels** - Позволяет участникам создавать, редактировать и удалять каналы.\n"
                        "**manage_roles** - Позволяет участникам создавать новые роли и редактировать или удалять "
                        "роли, которые ниже их самой высокой роли. Также позволяет участникам изменять права отдельных "
                        "каналов, к которым у них есть доступ.\n"
                        "**manage_emojis** - Позволяет участникам редактировать и удалять пользовательские "
                        "эмодзи, стикеры и звуки на этом сервере.\n"
                        "**view_audit_log** - Позволяет участникам просматривать историю изменений этого сервера.\n"
                        "**view_server_insights** - Позволяет участникам просматривать аналитику сервера.\n"
                        "**manage_webhooks** - Позволяет участникам создавать, редактировать и удалять вебхуки, "
                        "которые публикуют на этом сервере сообщения из других приложений и с сайтов.\n"
                        "**manage_server** - Даёт участникам право переименовывать этот сервер, менять регионы, "
                        "просматривать все приглашения, добавлять на этот сервер приложения или создавать и "
                        "обновлять правила Автомода.\n"
                        "**create_invite** - Позволяет участникам приглашать на этот сервер других участников."),
        Embed(
            title="",
            description="**kick_members** - Позволяет участникам удалять с этого сервера других участников. "
                        "Выгнанные участники смогут вернуться, только получив новое приглашение.\n"
                        "**ban_members** - Позволяет участникам навсегда банить на этом сервере других участников "
                        "и удалять историю сообщений.\n"
                        "**moderate_members** - Те, кого отправили думать о своём поведении, делают это молча. "
                        "Они не смогут отправлять сообщения в чат, отвечать в ветках, реагировать на сообщения и "
                        "говорить в голосовом чате или на трибуне.\n"
                        "**send_messages** - Позволяет участникам отправлять сообщения в текстовых каналах."
                        "**send_messages_in_threads** - Разрешить участникам отправлять сообщения в ветках.\n"
                        "**create_public_threads** - Разрешить участникам создавать ветки, которые смогут видеть "
                        "все, кто присутствует в канале.\n"
                        "**create_private_threads** - Разрешить участникам создавать ветки, с доступом только по "
                        "приглашению.\n"
                        "**embed_links** - Позволяет отображать на текстовых каналах контент ссылок, которыми "
                        "делятся участники.\n"
                        "**attach_files** - Позволяет участникам загружать на текстовые каналы файлы или "
                        "медиаконтент.\n"
                        "**add_reactions** - Позволяет участникам добавлять к сообщениям новые реакции-эмодзи. Если"
                        "отключить это право, участники смогут реагировать на сообщения только с помощью уже "
                        "существующих реакций."
        )
    ]
    view = HelpRolesView(embeds)
    await ctx.response.send_message(embed=embeds[0], view=view)


def load_roles():
    if os.path.exists('roles.json'):
        with open('roles.json', 'r') as file: return json.load(file)
    return {"role_1": {}, "role_2": {}, "role_3": {}}


def save_roles(data):
    with open('roles.json', 'w') as file: json.dump(data, file)


class RoleButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.custom_id = "role_buttons"
        self.data = load_roles()

    @discord.ui.button(label="Новости розыгрышей", style=discord.ButtonStyle.primary, custom_id="role_1")
    async def role_1_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(data_as['ROLE_ID_1'])
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            self.data["role_1"][str(interaction.user.id)] = True
            await interaction.response.send_message(f'Роль "{role.name}" успешно выдана!', ephemeral=True)
        else:
            await interaction.user.remove_roles(role)
            self.data["role_1"][str(interaction.user.id)] = False
            await interaction.response.send_message(f'Роль "{role.name}" успешно забрана!', ephemeral=True)
        save_roles(self.data)

    @discord.ui.button(label="Новости персонала", style=discord.ButtonStyle.primary, custom_id="role_2")
    async def role_2_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(data_as['ROLE_ID_2'])
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            self.data["role_2"][str(interaction.user.id)] = True
            await interaction.response.send_message(f'Роль "{role.name}" успешно выдана!', ephemeral=True)
        else:
            await interaction.user.remove_roles(role)
            self.data["role_2"][str(interaction.user.id)] = False
            await interaction.response.send_message(f'Роль "{role.name}" успешно забрана!', ephemeral=True)
        save_roles(self.data)

    @discord.ui.button(label="Новости медиа", style=discord.ButtonStyle.primary, custom_id="role_3")
    async def role_3_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(data_as['ROLE_ID_3'])
        if role not in interaction.user.roles:
            await interaction.user.add_roles(role)
            self.data["role_3"][str(interaction.user.id)] = True
            await interaction.response.send_message(f'Роль "{role.name}" успешно выдана!', ephemeral=True)
        else:
            await interaction.user.remove_roles(role)
            self.data["role_3"][str(interaction.user.id)] = False
            await interaction.response.send_message(f'Роль "{role.name}" успешно забрана!', ephemeral=True)
        save_roles(self.data)

        async def on_error(self, error: Exception, interaction: Interaction) -> None:
            await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                    f"`remodik`\n\n{error}")


async def setup_button():
    button_view = RoleButtons()
    bot.add_view(button_view)


bot.loop.create_task(setup_button())


class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Не выбрано",
                emoji=discord.PartialEmoji(id=877264845366517770, name="No_Check")
            ),
            discord.SelectOption(
                label="Настройки",
                emoji=discord.PartialEmoji(name="43a63c2b9c4e96dc7a6a", id=1305791881791406151)
            ),
            discord.SelectOption(
                label="Модерация",
                emoji=discord.PartialEmoji(
                    name="Ban_Hammer_7437",
                    id=1303576542273863701
                )
            ),
            discord.SelectOption(
                label="Роли",
                emoji=discord.PartialEmoji(
                    name="Owner_7437",
                    id=1303575461154132018
                )
            ),
            discord.SelectOption(
                label="Развлечения",
                emoji=discord.PartialEmoji(name="controller", id=1107789264135139509)
            ),
            discord.SelectOption(
                label="Другое",
                emoji=discord.PartialEmoji(name="VisionAnemo", id=725173419133370390)
            )
        ]
        super().__init__(placeholder="Выберите категорию", options=options, custom_id="help_command")

    async def callback(self, ctx: discord.Interaction):
        pref = get_prefix(bot, ctx)
        selected_value = self.values[0]
        if selected_value == "Настройки":
            category_title = "Команды для настройки бота"
        elif selected_value == "Модерация":
            category_title = "Команды для модерации сервера"
        elif selected_value == "Роли":
            category_title = "Команды управления ролями. (/role *arg)"
        elif selected_value == "Развлечения":
            category_title = "Развлекательные команды"
        elif selected_value == "Другое":
            category_title = "Прочие команды"
        else:
            category_title = "Список команд"

        embed = discord.Embed(title=category_title, color=discord.Color.blue())

        def add_commands_to_embed(commands_permissions):
            for cmd, info in commands_permissions.items():
                if info.get('requires_permission') and not getattr(ctx.user.guild_permissions, info['permission'],
                                                                   False):
                    continue
                if info.get('guild_access') and ctx.guild.id not in info['guild_access']:
                    continue
                if info.get('role_access') and not any(role.id in info['role_access'] for role in ctx.user.roles):
                    continue
                if info.get('user_access') and ctx.user.id not in info['user_access']:
                    continue
                embed.add_field(name="", value=info['description'], inline=False)
            return embed

        if selected_value == "Настройки":
            commands_permissions = {
                'prefix': {
                    'permission': 'administrator',
                    'description': f'`prefix` - Установить префикс команд бота. **Использование:** `{pref}prefix '
                                   f'prefix`',
                    'requires_permission': True,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'set_system': {
                    'permission': 'administrator',
                    'description': '</set_system:1306213844712030262> - Установить канал для уведомлений о '
                                   'входах/выходах.',
                    'requires_permission': True,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Модерация":
            commands_permissions = {
                'kick': {
                    'permission': 'kick_members',
                    'description': '</kick:1306213844363907137> - Выгнать пользователя с сервера.',
                    'requires_permission': True
                },
                'clear': {
                    'permission': 'manage_messages',
                    'description': '</clear:1306213844363907136> - Удалить сообщения в чате.',
                    'requires_permission': True
                },
                'delchat': {
                    'permission': 'manage_channels',
                    'description': '</delchat:1306213844712030265> - Удалить текстовый чат.',
                    'requires_permission': True
                },
                'delvoice': {
                    'permission': 'manage_channels',
                    'description': '</delvoice:1306213844712030267> - Удалить голосовой чат.',
                    'requires_permission': True
                },
                'nick': {
                    'permission': 'manage_nicknames',
                    'description': '</nick:1306213844363907138> - Изменить ник пользователя.',
                    'requires_permission': True
                },
                'presence': {
                    'permission': 'kick_members',
                    'description': '</presence:1306578580699877466> - Поиск людей с определённой активностью.',
                    'requires_permission': True
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Роли":
            commands_permissions = {
                'add': {
                    'permission': 'manage_roles',
                    'description': '</role add:1307242710674968667> - Выдать пользователю роль.',
                    'requires_permission': True
                },
                'create': {
                    'permission': 'manage_roles',
                    'description': "</role create:1307242710674968667> - Создать роль.",
                    'requires_permission': True
                },
                'delperm': {
                    'permission': 'administrator',
                    'description': "</role delperm:1307242710674968667> - Забрать право у роли.",
                    'requires_permission': True
                },
                'do': {
                    'permission': 'manage_roles',
                    'description': "</role do:1307242710674968667> - Повысить роль пользователя на 1 уровень.",
                    'requires_permission': True
                },
                'delete': {
                    'permission': 'manage_roles',
                    'description': "</role delete:1307242710674968667> - Удалить роль.",
                    'requires_permission': True
                },
                'pre': {
                    'permission': 'administrator',
                    'description': "</role pre:1307242710674968667> - Изменить приоритет роли.",
                    'requires_permission': True
                },
                'clear': {
                    'permission': 'administrator',
                    'description': "</role clear:1307242710674968667> - Забрать все роли у пользователя.",
                    'requires_permission': True
                },
                'color': {
                    'permission': 'manage_roles',
                    'description': "</role color:1307242710674968667> - Изменить цвет роли.",
                    'requires_permission': True
                },
                'remove': {
                    'permission': 'manage_roles',
                    'description': "</role delete:1307242710674968667> - Забрать роль у пользователя.",
                    'requires_permission': True
                },
                'replace': {
                    'permission': 'manage_roles',
                    'description': "</role replace:1307242710674968667> - Заменить роль у пользователя.",
                    'requires_permission': True
                },
                'name': {
                    'permission': 'manage_roles',
                    'description': "</role rename:1307242710674968667> - Переименовать роль.",
                    'requires_permission': True
                },
                'list': {
                    'permission': 'manage_roles',
                    'description': "</role list:1307242710674968667> - Список ролей сервера.",
                    'requires_permission': True
                },
                'setperm': {
                    'permission': 'administrator',
                    'description': "</role setperm:1307242710674968667> - Установить право для роли.",
                    'requires_permission': True
                },
                'up': {
                    'permission': 'manage_roles',
                    'description': "</role up:1307242710674968667> - Повысить роль пользователя на 1 уровень.",
                    'requires_permission': True
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Развлечения":
            commands_permissions = {
                '8ball': {
                    'permission': '',
                    'description': '</8ball:1306213844712030261> - Игра на кик с сервера, шанс проиграть 10%.',
                    'requires_permission': False
                },
                'giveaway': {
                    'permission': 'administrator',
                    'description': '</giveaway:1306213844909297686> - Сделать розыгрыш на сервере.',
                    'requires_permission': True
                },
                'anime': {
                    'permission': '',
                    'description': '</anime:1306578580699877463> - Посмотреть информацию об аниме.',
                    'requires_permission': False
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Другое":
            commands_permissions = {
                'mserver': {
                    'permission': 'administrator',
                    'description': '</mserver:1306625242516557869> - Посмотреть информацию о Minecraft сервере.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'avatar': {
                    'permission': 'administrator',
                    'description': '</avatar:1306578580699877464> Получить пользователя или сервера.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'calculate': {
                    'permission': 'administrator',
                    'description': '</calculate:1306213844363907135> - Посчитать выражение.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'faq': {
                    'permission': 'administrator',
                    'description': '</faq:1306213844909297689> - Информация о боте.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'предложение': {
                    'permission': 'administrator',
                    'description': '</предложение:1306213844909297685> - Предложить улучшить бота.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'bug_report': {
                    'permission': None,
                    'description': '</bug_report:1306213844909297684> - Сообщить о баге в боте.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'unreg': {
                    'permission': 'administrator',
                    'description': '</unreg:1265212320234209375> - Снять модератора с должности.',
                    'requires_permission': True,
                    'guild_access': [1263854530445971671],
                    'role_access': [1263854775900835904],
                    'user_access': [931585084312670219, 933020119783858247, 1097064973328453704, 743864658951274528]
                },
                'reg': {
                    'permission': 'administrator',
                    'description': '</reg:1265212320234209376> - Принять пользователя на должность.',
                    'requires_permission': True,
                    'guild_access': [1263854530445971671],
                    'role_access': [1263854775900835904],
                    'user_access': [931585084312670219, 933020119783858247, 1097064973328453704, 743864658951274528]
                },
                'dsup': {
                    'permission': 'administrator',
                    'description': '<dsup:1279065730620592148> - Повысить модератора Discord в должности.',
                    'requires_permission': True,
                    'guild_access': [1138204059397005352],
                    'role_access': [1219899085855789056, 1250430571252023397, 1228593717586427987],
                    'user_access': None
                },
                'munreg': {
                    'permission': 'administrator',
                    'description': '`munreg` - Снять модератора Discord с должности.',
                    'requires_permission': True,
                    'guild_access': [1138204059397005352],
                    'role_access': [1219899085855789056, 1250430571252023397, 1228593717586427987],
                    'user_access': [990180688504434688]
                },
                'report': {
                    'permission': 'administrator',
                    'description': '</report:1268277034992537603> - Отправить жалобу на игрока.',
                    'requires_permission': False,
                    'guild_access': [1138204059397005352],
                    'role_access': None,
                    'user_access': None
                },
                'hmb': {
                    'permission': 'administrator',
                    'description': '`hmb` - Вызвать сообщение с выбором ролей уведомлений HightMine. '
                                   f'**Использование:** `{pref}hmb`',
                    'requires_permission': True,
                    'guild_access': [1138204059397005352],
                    'role_access': None,
                    'user_access': None
                },
                'caps': {
                    'permission': 'manage_messages',
                    'description': '</caps:1306213844363907133> - Узнать % верхнего регистра.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'send_stat': {
                    'permission': 'administrator',
                    'description': '</send_stat:1306213844363907134> - Назначить канал для статистики сервера.',
                    'requires_permission': True
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        if self.values[0] == "Не выбрано":
            await ctx.response.defer(invisible=True)
            return
        if not embed.fields:
            await ctx.response.send_message("Нет прав на использование команд в этой категории.", ephemeral=True)
        else:
            await ctx.response.send_message(embed=embed, ephemeral=True)


class HelpView(discord.ui.View):
    def __init__(self):
        self.custom_id = "help_view"
        super().__init__(timeout=None)
        self.add_item(HelpSelect())

        async def on_error(self, error: Exception, interaction: Interaction) -> None:
            await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                    f"`remodik`\n\n{error}")


@bot.slash_command(name="help", description="Информация о моих командах")
async def _help(ctx: Interaction):
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    view = HelpView()
    await ctx.response.send_message(ephemeral=True, content="+")
    await ctx.send("Помощь по моим командам", view=view)


@bot.command(name="hmb")
@commands.is_owner()
async def hmb(ctx):
    view = RoleButtons()
    button_channel = bot.get_channel(1225384797648719945)
    async for message in button_channel.history(limit=1): await message.delete()
    await ctx.send("Нажмите на реакцию для получения соответствующих уведомлений", view=view)


@roles.command(name="list", description="Список ролей сервера")
async def role_list(ctx):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.guild_permissions.manage_roles:
            roles = ctx.guild.roles
            role_list = discord.Embed(title="Список ролей сервера", color=discord.Color.blue())
            MAX_ROLES_PER_PAGE = 15
            start_index = 0
            end_index = min(start_index + MAX_ROLES_PER_PAGE, len(roles))
            for index, role in enumerate(roles[start_index:end_index], start=0):
                if role.name != "@everyone":
                    role_list.add_field(name=f"", value=f"{role.mention} `{role.id}` - `id:` {index}", inline=False)
                    role_list.set_footer(text=f"Кол-во ролей: {len(ctx.guild.roles)}")
            view = RoleView(ctx, roles, start_index, end_index, len(roles), MAX_ROLES_PER_PAGE)
            await ctx.response.send_message(embed=role_list, view=view)
            await send_log(ctx.guild.id, embed=Embed(description=f"{ctx.author.mention} вызвал список ролей через "
                                                                 f"</role list:1307242710674968667>", color=0x7b68ee))
        else:
            await ctx.response.send_message("У вас недостаточно прав!", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.user.mention} | "
              f"`{ctx.user.id}`\nКоманда: roles")


class RoleView(discord.ui.View):
    def __init__(self, ctx, roles, start_index, end_index, total_roles, max_roles_per_page):
        super().__init__(timeout=None)
        self.interaction = ctx
        self.roles = roles
        self.start_index = start_index
        self.end_index = end_index
        self.total_roles = total_roles
        self.max_roles_per_page = max_roles_per_page
        self.update_buttons()

    def update_buttons(self):
        self.children[0].disabled = self.start_index == 0
        self.children[1].disabled = self.end_index >= self.total_roles

    @discord.ui.button(label='Назад', style=discord.ButtonStyle.red)
    async def previous_button(self, button: discord.ui.Button, ctx: discord.Interaction):
        if self.start_index > 0:
            self.start_index -= self.max_roles_per_page
            self.end_index = min(self.start_index + self.max_roles_per_page, self.total_roles)
            self.update_buttons()
            await self.update_message(ctx)

    @discord.ui.button(label='Вперёд', style=discord.ButtonStyle.green)
    async def next_button(self, button: discord.ui.Button, ctx: discord.Interaction):
        if self.end_index < self.total_roles:
            self.start_index += self.max_roles_per_page
            self.end_index = min(self.start_index + self.max_roles_per_page, self.total_roles)
            self.update_buttons()
            await self.update_message(ctx)

    async def update_message(self, ctx):
        role_list = discord.Embed(title="Список ролей сервера", color=discord.Color.blue())
        for index, role in enumerate(reversed(self.roles[self.start_index:self.end_index]), start=self.start_index + 1):
            if role.name != "@everyone":
                role_list.add_field(name="", value=f"{role.mention} `{role.id}` - index: {index}", inline=False)
                role_list.set_footer(text=f"Кол-во ролей: {len(ctx.guild.roles)}")
        await ctx.response.edit_message(embed=role_list, view=self)


@roles.command(name="delete", description="Удалить роль")
async def _delrole(ctx, *, роль: discord.Option(discord.Role, description="Какую роль удалить")):
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if ctx.author.guild_permissions.manage_roles:
        if ctx.author.top_role > роль:
            if роль:
                embed = Embed(title="Роль удалена", color=0x7b68ee)
                embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                embed.add_field(name="Роль", value=f"{роль.mention} ({роль.name})")
                embed.set_footer(text=f"user id: {ctx.author.id}")
                await send_log(ctx.guild.id, embed=embed)
                await ctx.response.send_message(f"Роль «{роль.name}» удалена", ephemeral=True)
                await роль.delete()
            else:
                await ctx.response.send_message(f'Роль «{роль.name}» не найдена', ephemeral=True)
        else:
            await ctx.response.send_message("У вас недостаточно прав!", ephemreal=True)
    else:
        await ctx.response.send_message(f"У вас нет прав на использование этой команды!", ephemeral=True)


@bot.slash_command(name="delchat", description="Удалить текстовый канал")
async def _delchat(ctx, name: discord.Option(discord.TextChannel, "Какой чат удалить")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.guild_permissions.manage_channels:
            embed = Embed(title="Текстовый чат удалён", color=0x7b68ee)
            embed.add_field(name="Название", value=name, inline=True)
            embed.add_field(name="Автор", value=ctx.author.mention)
            embed.set_footer(text=f"user id: {ctx.author.id}")
            await name.delete()
            await ctx.response.send_message(f"Текстовый канал «{name.name}» был удален.")
            await send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond("У вас нет прав на использование этой команды!", ephemeral=True)
    except discord.Forbidden:
        await ctx.response.send_message(f"Недостаточно прав для удаления канала «{name.name}».", ephemeral=True)
    except discord.NotFound:
        await ctx.response.send_message(f"Чат с именем «{name.name}» не найден.", ephemeral=True)


@bot.slash_command(name="delvoice", description="Удалить голосовой канал")
async def _delvoice(ctx, name: discord.Option(discord.VoiceChannel, "Какой чат удалить")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.guild_permissions.manage_channels:
            embed = Embed(title="Голосовой канал удалён", color=0x7b68ee)
            embed.add_field(name="Название", value=name, inline=True)
            embed.add_field(name="Автор", value=ctx.author.mention)
            embed.set_footer(text=f"user id: {ctx.author.id}")
            await name.delete()
            await ctx.response.send_message(f'Голосовой канал «{name.name}» был удален.', ephemeral=True)
            await send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond("У вас нет прав на использование этой команды!", ephemeral=True)
    except discord.Forbidden:
        await ctx.response.send_message(f"Недостаточно прав для удаления этого канала.", ephemeral=True)
    except discord.NotFound:
        await ctx.response.send_message(f"Канал «{name.name}» не найден.", ephemeral=True)


@roles.command(name="pin", description="Переключить видимость роли в списке участников.")
async def pin_role(ctx, role: discord.Role):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.guild_permissions.manage_roles:
            if ctx.author.top_role > role:
                if role not in ctx.guild.roles:
                    await ctx.response.send_message("Данная роль не существует на этом сервере.", ephemeral=True)
                    return
                hoist_status = role.hoist
                await role.edit(hoist=not hoist_status)
                if hoist_status:
                    embed = Embed(title="Параметры роли изменены",
                                  description="`Показывать участников с ролью отдельно от остальных участников в сети`",
                                  color=0x7b68ee)
                    embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                    embed.add_field(name="Новое состояние", value="Выключено")
                    embed.set_footer(text=f"channel: {ctx.channel.mention}")
                    await ctx.respond(f'Роль **{role.name}** больше не будет отображаться отдельно.', ephemeral=True)
                    await send_log(ctx.guild.id, embed=embed)
                else:
                    embed = Embed(title="Параметры роли изменены",
                                  description="`Показывать участников с ролью отдельно от остальных участников в сети`",
                                  color=0x7b68ee)
                    embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                    embed.add_field(name="Новое состояние", value="Включено")
                    embed.set_footer(text=f"channel: {ctx.channel.mention}")
                    await ctx.respond(f"Роль **{role.name}** теперь будет отображаться отдельно.", ephemeral=True)
                    await send_log(ctx.guild.id, embed=embed)
            else:
                await ctx.response.send_message("У вас недостаточно прав!", ephemeral=True)
        else:
            await ctx.response.send_message("У вас недостаточно прав!", ephemeral=True)
    except discord.Forbidden:
        await ctx.respond("Недостаточно прав для изменения параметров этой роли.", ephemeral=True)


@bot.event
async def on_interaction(interaction):
    if interaction.user.id in block_users:
        await interaction.response.send_message("Вы находитесь в чёрном списке!", ephemeral=True)
    else:
        if interaction.type == discord.InteractionType.application_command:
            command_name = interaction.data.get('name')
            command_id = interaction.data.get('id')
            print(f"Команда {command_name} с ID: {command_id}")
        await bot.process_application_commands(interaction=interaction)


@bot.slash_command(name="embed", description="Создать Embed сообщение")
async def _staff_m(ctx, channel: discord.Option(discord.TextChannel | discord.DMChannel | discord.VoiceChannel,
                                                description="Куда отправить", default=None),
                   message: Option(str, "Дополнительное сообщение (перед Embed)", default=None),
                   title: Option(str, description="Название заголовка", default=None),
                   description: Option(str,description="Описание Embed",default=None),
                   field_name: Option(str, description="Заголовок поля", default=None),
                   field_desc: Option(str, description="Описание поля", default=None),
                   thumbnail: Option(str, description="Ссылка на фото", default=None),
                   image: Option(str, description="Ссылка на фото", default=None),
                   footer: Option(str, description="Доп. инфа в самом низу", default=None)):
    if not any([channel, message, title, description, field_name, field_desc, thumbnail, image, footer]):
        embeds = Embed(title="Помощь по Embed", color=0x7b68ee)
        embeds.add_field(name="channel *(Куда отправить)*",
                         value=f"Описание: Укажите канал, куда нужно отправить Embed сообщение. Если не указано, "
                               f"сообщение будет отправлено в текущий канал.", inline=False)

        embeds.add_field(name="message *(Дополнительное сообщение перед Embed)*",
                         value="Описание: Текст, который будет отображаться перед Embed сообщением. Полезно, если вы "
                               "хотите добавить какое-то пояснение или приветствие.", inline=False)

        embeds.add_field(name="title *(Название заголовка)*",
                         value="Описание: Заголовок Embed сообщения. Этот текст будет выделен жирным шрифтом вверху "
                               "сообщения.", inline=False)

        embeds.add_field(name="description *(Описание)*",
                         value="Описание: Основной текст сообщения. Поддерживает переносы строк, а также форматирование"
                               " (например, жирный, курсив, зачеркнутый).", inline=False)

        embeds.add_field(name="field_name *(Заголовок поля)*",
                         value="Описание: Название дополнительного поля. Поля позволяют добавить структурированную "
                               "информацию в виде пар «Заголовок — Значение».", inline=False)

        embeds.add_field(name="field_desc *(Описание поля)*", inline=False,
                         value="Описание: Значение для поля. Обычно используется для дополнительных данных.", )

        embeds.add_field(name="thumbnail *(Ссылка на фото)*",
                         value="Описание: Ссылка на изображение, которое будет отображаться в виде миниатюры "
                               "(слева вверху).", inline=False)

        embeds.add_field(name="footer *(Доп. инфа в самом низу)*",
                         value="Описание: Дополнительная информация, которая отображается внизу Embed сообщения. "
                               "Например, вы можете указать дату или свой текст.", inline=False)
        embeds.add_field(name="\nШаблоны",
                         value=f"Для перехода на новую строку используйте \\n\n"
                               f"Шаблоны времени: Начинаются и заканчиваются знаком %\n"
                               f"\nПримеры:\n"
                               f"- %datetime.now('%d.%m.%Y')% — текущая дата в формате 16.11.2024\n"
                               f"- %datetime.now('%A, %d %B %Y')% — текущая дата в формате Saturday, 16 November 2024\n"
                               f"- %datetime.now('%H:%M:%S')% — текущее время в формате 14:30:00\n"
                               f"- %datetime.today()% — текущая дата в формате 2024-11-16\n"
                               f"\nВы можете комбинировать шаблоны с текстом для динамичных сообщений.", inline=False)
        await ctx.respond(embed=embeds, ephemeral=True)
        return
    if not ctx.author.guild_permissions.manage_messages:
        return
    if message:
        message = message.replace("\\n", "\n")
    if title:
        title = title.replace("\\n", "\n")
    if description:
        description = description.replace("\\n", "\n")
    if field_name:
        field_name = field_name.replace("\\n", "\n")
    if field_desc:
        field_desc = field_desc.replace("\\n", "\n")
    if footer:
        footer = footer.replace("\\n", "\n")

    def process_placeholders(text: str) -> str:
        if not text:return text
        pattern = r"%([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\((.*?)\)%"

        def replace_placeholder(match):
            obj_type = match.group(1)
            method = match.group(2)
            format_str = match.group(3).strip("'\"")
            try:
                if obj_type == "datetime":
                    if method == "now":
                        format_str = format_str if format_str else "%d.%m.%Y %H:%M:%S"
                        value = datetime.now().strftime(format_str)
                    elif method == "timestamp":
                        time_delta = eval(format_str)
                        value = (datetime.now() + time_delta).timestamp()
                    else:
                        dt_method = getattr(datetime, method, None)
                        if dt_method:value = dt_method(*eval(format_str)) if format_str else dt_method()
                        else:value = f"[Ошибка: неизвестный метод '{obj_type}.{method}']"
                elif obj_type == "date":
                    if method == "today":
                        format_str = format_str if format_str else "%d.%m.%Y"
                        value = date.today().strftime(format_str)
                    else:
                        date_method = getattr(date, method, None)
                        if date_method:value = date_method(*eval(format_str)) if format_str else date_method()
                        else:value = f"[Ошибка: неизвестный метод '{obj_type}.{method}']"
                elif obj_type == "time":
                    if method == "now":
                        format_str = format_str if format_str else "%H:%M:%S"
                        value = datetime.now().strftime(format_str).split()[1]
                    else:
                        time_method = getattr(time, method, None)
                        if time_method:value = time_method(*eval(format_str)) if format_str else time_method()
                        else:value = f"[Ошибка: неизвестный метод '{obj_type}.{method}']"
                else:value = f"[Ошибка: неизвестный объект '{obj_type}']"
                return str(value)
            except Exception as e:return f"[Ошибка: {e}]"
        return re.sub(pattern, replace_placeholder, text)
    message = process_placeholders(message)
    title = process_placeholders(title)
    description = process_placeholders(description)
    field_name = process_placeholders(field_name)
    field_desc = process_placeholders(field_desc)
    footer = process_placeholders(footer)
    embed = Embed(title=title if title else "", description=description if description else "", color=Color.default())
    if ctx.guild is not None:
        member = ctx.guild.get_member(ctx.author.id)
        nick = member.display_name
        embed.set_author(name=nick, icon_url=ctx.author.avatar.url)
    if field_name:
        embed.add_field(name=field_name, value=field_desc if field_desc else "")
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    if footer:
        embed.set_footer(text=footer)
    if channel is None:
        if message:
            await ctx.respond(content=message, embed=embed)
        else:
            await ctx.respond(embed=embed)
    else:
        if isinstance(channel, discord.abc.Messageable):
            await channel.send(content=message, embed=embed)
    if ctx.guild is not None:
        await send_log(ctx.guild.id, message=f"{ctx.author.mention} отправил Embed!")
        if message or embed:
            await send_log(ctx.guild.id, message=message, embed=embed)
    await ctx.respond("Успешно!", ephemeral=True)


async def mentions_def(ctx: discord.AutocompleteContext):
    return [True, False]


@roles.command(name="mention", description="Управлять упоминаниями роли.")
async def mentions_cmd(ctx, role: discord.Role, enable: bool = discord.Option(autocomplete=mentions_def)):
    if role not in ctx.guild.roles:
        await ctx.response.send_message("Эта роль не существует на этом сервере.", ephemeral=True)
        return
    if ctx.author.guild_permissions.manage_roles:
        enable_bool = enable is True
        await role.edit(mentionable=enable_bool)
        if ctx.author.top_role <= role:
            await ctx.respond(embed=Embed(description="Вы не можете настраивать свою наивысшую роль!"), ephemeral=True)
            return
        if enable_bool:
            embed = Embed(title="Параметры роли изменены", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
            embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=False)
            embed.add_field(name="Параметр", value="`Позволить всем @упоминать эту роль.`, теперь включено`")
            await ctx.response.send_message(f"Роль {role.name} теперь может быть упомянута.", ephemeral=True)
            await send_log(ctx.guild.id, embed=embed)
        else:
            embed = Embed(title="Параметры роли изменены", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
            embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=False)
            embed.add_field(name="Параметр", value="`Позволить всем @упоминать эту роль.`, теперь выключено`")
            await ctx.response.send_message(f"Роль {role.name} больше не может быть упомянута.", ephemeral=True)
            await send_log(ctx.guild.id, embed=embed)
    else:
        await ctx.respond(embed=Embed(description="У вас нет прав для использования этой команды!",
                                      color=Color.default()), ephemeral=True)


message_to_update = None
persistent_views_added = False


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    global persistent_views_added
    global message_to_update
    if not persistent_views_added:
        persistent_views_added = True
    channel = bot.get_channel(1270854193900687412)
    if channel is None: return
    async for message in channel.history(limit=1):
        if message.author == bot.user:
            await message.delete()
            break
    embed = await create_embed()
    message_to_update = await channel.send(embed=embed)
    await update_old_messages()
    if not send_statistics.is_running():
        send_statistics.start()
    if update_message.is_running():
        update_message.stop()
    update_message.start()
    bot.add_view(HelpView())
    await bot.change_presence(activity=discord.Game(name="/help (От администратора)"))
    await setup_views()
    commands_ = [restart_bot, caps, send_stat, _staff_ds, _calculate, _warn, unwarn, _warns, warnlist, clear_messages,
                 _kick, log, _nick, ping, dsup, _stop, munreg_command, _unreg, _reg, guilds, eight_ball, _report_,
                 _send_r, _help, set_system, help_roles, _delchat, _delvoice, bug_report, bot_idea, anime, _faq,
                 giveaway, _avatar, find_presence, _staff_m, _mserver, обновление, история, inform]
    # await bot.register_commands(commands=commands_)
    for command in commands_:
        print(f"{command.name} - {command.id}")
    print("\n\n")
    for command_g in roles.subcommands:
        print(command_g.id)


TARGET_ROLES = ["× Гл.Администратор Дискорда", "× Администратор Дискорда", "× Мл.Администратор Дискорда",
                "× Гл.Модератор Дискорда", "× Ст.Модератор Дискорда", "× Модератор Дискорда", "× Мл.Модератор Дискорда"]


@tasks.loop(seconds=5)
async def update_message():
    global message_to_update
    if message_to_update is not None:
        embed = await create_embed()
        await message_to_update.edit(embed=embed)


async def create_embed():
    guild = bot.get_guild(1138204059397005352)
    if guild is None:
        return discord.Embed(title="Error", description="Guild not found", color=discord.Color.default())
    embed = discord.Embed(title="Персонал дискорда", color=discord.Color.default())
    members_with_roles = []
    for member in guild.members:
        max_role = get_max_role(member)
        if max_role: members_with_roles.append((member, max_role))
    members_with_roles.sort(key=lambda x: x[1].position, reverse=True)
    for member, max_role in members_with_roles:
        embed.add_field(name='', value=f'{member.mention} × {max_role.mention}', inline=False)
    return embed


def get_max_role(member):
    roles = [role for role in member.roles if role.name in TARGET_ROLES]
    if roles: return max(roles, key=lambda role: role.position)
    return None


@roles.command(name="rename", description="Изменить имя роли")
async def _rname(ctx, роль: Option(discord.Role, description="Какую роль переименовать"),
                 new_name: Option(str, description="Новое имя роли")):
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if ctx.author.guild_permissions.manage_roles:
        if ctx.author.top_role > роль:
            try:
                await ctx.response.send_message(f"Роль {роль.name} переименована в {new_name}", ephemeral=True)
                embed = Embed(title="Роль переименована", color=0x7b68ee)
                embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
                embed.add_field(name=f"Роль", value=f"{роль.mention} ({роль.name})", inline=True)
                embed.add_field(name="Новое имя", value=new_name)
                await send_log(ctx.guild.id, embed=embed)
                await роль.edit(name=new_name)
            except discord.Forbidden:
                await ctx.response.send_message("У меня нет прав для изменения роли.", ephemeral=True)
            except discord.HTTPException:
                await ctx.response.send_message("Произошла ошибка при попытке изменить имя роли.", ephemeral=True)
        else:
            await ctx.response.send_message("Вы не можете изменять эту роль!", ephemeral=True)
    else:
        await ctx.response.send_message("У вас нет прав!", ephemeral=True)


class DeclineModal(Modal):
    def __init__(self, member: discord.Member, view: 'AcceptDeclineView', *args, **kwargs):
        super().__init__(*args, **kwargs, title="Причина отказа")
        self.member = member
        self.view = view
        self.add_item(discord.ui.InputText(label='Укажите причину отказа', style=discord.InputTextStyle.long,
                                           placeholder='Напишите причину отказа от заявки', max_length=500))

    async def on_error(self, error: Exception, interaction: Interaction) -> None:
        await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                f"`remodik`\n\n{error}")

    async def callback(self, interaction: discord.Interaction):
        reason = self.children[0].value
        if interaction.guild.id == 1138204059397005352:
            text = "Мл.Модератор дискорда"
        elif interaction.guild.id == 1138400553081253948:
            text = 'Хелпер Discord'
        await self.member.send(f"Ваша заявка на должность '{text}' отклонена.\nПричина: {reason}\n"
                               f"Проверяющий: {interaction.user.mention} | {interaction.user.id}")
        await interaction.response.send_message(f"{interaction.user.mention} отклонил заявку на должность пользователя:"
                                                f" {self.member.mention}\nПричина отказа: {reason}")
        await self.view.decline_action_completed(interaction, True)


class ApplyButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.custom_id = "accept_button"

    @discord.ui.button(label="Подать заявку", style=discord.ButtonStyle.green, custom_id="apply_button")
    async def apply_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = MyModal(title="Анкета")
        await interaction.response.send_modal(modal)


class BugCommand(Modal):
    def __init__(self):
        super().__init__(title="Заявка на баг")
        self.add_item(discord.ui.InputText(label="Суть бага", style=discord.InputTextStyle.long,
                                           min_length=15, placeholder="Напишите суть бага", max_length=500))
        self.add_item(discord.ui.InputText(label="Как с вами связаться", style=discord.InputTextStyle.short,
                                           placeholder="Укажите ваши контактные данные", max_length=100))
        self.add_item(discord.ui.InputText(label="Доказательства", placeholder="Укажите ссылку на видео/фото",
                                           max_length=250))

    async def callback(self, interaction: discord.Interaction):
        чс_обращений = []
        if interaction.user.id in чс_обращений:
            await interaction.response.send_message("Вы находитесь в черном списке бота!", ephemeral=True)
            return
        answers = [item.value for item in self.children]
        bug_channel = bot.get_channel(1291806519909941362)

        if not bug_channel:
            await interaction.response.send_message("Канал для отправки багов не найден. Свяжитесь с разработчиком.",
                                                    ephemeral=True)
            return
        embed = discord.Embed(title="Заявка на баг", color=discord.Color.default())
        embed.add_field(name="Суть бага", value=answers[0], inline=False)
        embed.add_field(name="Данные пользователя", value=answers[1], inline=False)
        embed.add_field(name="Доказательства", value=answers[2], inline=False)
        view = BugReportView(interaction.user)
        await bug_channel.send(content=f"{interaction.user.mention} | `{interaction.user.name}` | "
                                       f"`{interaction.user.id}`", embed=embed, view=view)
        await interaction.response.send_message("Ваша заявка успешно отправлена!", ephemeral=True)


class BugReportView(View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button): child.disabled = True

    @staticmethod
    def update_status(embed: discord.Embed, status: str):
        status_field_index = None
        for i, field in enumerate(embed.fields):
            if field.name == "Статус:":
                status_field_index = i
                break
        if status_field_index is not None:
            embed.set_field_at(status_field_index, name="Статус:", value=status, inline=False)
        else:
            embed.add_field(name="Статус:", value=status, inline=False)

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.success, custom_id="accept_bug_button")
    async def accept_button_callback(self, button: discord.ui.Button, ctx: discord.Interaction):
        if ctx.user.guild_permissions.administrator:
            embed = ctx.message.embeds[0]
            self.update_status(embed, "Принята")
            self.disable_all_buttons()
            await ctx.message.edit(embed=embed, view=self)
            await ctx.response.send_message(f"{ctx.user.mention} принял заявку на баг от {self.member.mention} | "
                                            f"`{self.member.name}` | `{self.member.id}`")
            await self.member.send("Ваша заявка на баг была успешно одобрена!.\n"
                                   f"Рассматривал: {ctx.user.mention} | `{ctx.user.name}`")
        else:
            await ctx.response.send_message("У вас нет прав для принятия заявок.", ephemeral=True)

    @discord.ui.button(label="Отказать", style=discord.ButtonStyle.danger, custom_id="decline_bug_button")
    async def deny_button_callback(self, button: discord.ui.Button, ctx: discord.Interaction):
        if ctx.user.guild_permissions.administrator:
            modal = ReasonModal(self.member, self)
            await ctx.response.send_modal(modal)
        else:
            await ctx.response.send_message("У вас нет прав для отклонения заявок.", ephemeral=True)

    @discord.ui.button(label="На рассмотрении", style=discord.ButtonStyle.primary, custom_id="pending_bug_button")
    async def pending_button_callback(self, button: discord.ui.Button, ctx: discord.Interaction):
        if ctx.user.guild_permissions.administrator:
            embed = ctx.message.embeds[0]
            self.update_status(embed, "На рассмотрении")
            await ctx.message.edit(embed=embed, view=self)
            await ctx.response.send_message(f"{ctx.user.mention} начал рассмотрение заявки на баг от "
                                            f"{self.member.mention} `{self.member.name}` | `{self.member.id}`")
            await self.member.send("Ваша заявка на баг находится на рассмотрении.")
        else:
            await ctx.response.send_message("У вас нет прав для изменения статуса заявок.", ephemeral=True)


class ReasonModal(Modal):
    def __init__(self, member: discord.Member, view: BugReportView):
        super().__init__(title="Причина отказа")
        self.member = member
        self.view = view
        self.add_item(discord.ui.InputText(label="Причина отказа", style=discord.InputTextStyle.long))

    async def callback(self, ctx: discord.Interaction):
        reason = self.children[0].value
        embed = ctx.message.embeds[0]
        self.view.update_status(embed, f"Отклонена: {reason}")
        self.view.disable_all_buttons()
        await ctx.message.edit(embed=embed, view=self.view)
        await ctx.response.send_message(f"{ctx.user.mention} отклонил заявку на баг от {self.member.mention} | "
                                        f"`{self.member.name}` | `{self.member.id}`")
        await self.member.send("Ваша заявка на баг была отклонена.\n"
                               f"Рассматривал: {ctx.user.mention} | `{ctx.user.name}`")


@bot.slash_command(name="bug_report", description="Отправить сообщение о баге")
async def bug_report(ctx: discord.ApplicationContext):
    modal = BugCommand()
    await ctx.send_modal(modal)


class UpdateBotCommand(Modal):
    def __init__(self):
        super().__init__(title="Заявка на баг")
        self.add_item(discord.ui.InputText(label="Суть улучшения", style=discord.InputTextStyle.long,
                                           min_length=15, placeholder="Напишите суть улучшения", max_length=500))
        self.add_item(discord.ui.InputText(label="Как с вами связаться", style=discord.InputTextStyle.short,
                                           placeholder="Укажите ваши контактные данные", max_length=100))
        self.add_item(discord.ui.InputText(label="Чем полезно", placeholder="Чем это улучшение будет полезно для бота?",
                                           max_length=250))

    async def callback(self, interaction: discord.Interaction):
        чс_обращений = []
        if interaction.user.id in чс_обращений:
            await interaction.response.send_message("Вы находитесь в черном списке бота!", ephemeral=True)
            return
        answers = [item.value for item in self.children]
        bug_channel = bot.get_channel(1290988742492033087)
        if not bug_channel:
            await interaction.response.send_message("Канал для отправки предложений не найден. "
                                                    "Свяжитесь с разработчиком.", ephemeral=True)
            return
        embed = discord.Embed(title="Заявка на улучшение бота", color=discord.Color.default())
        embed.add_field(name="Суть улучшения", value=answers[0], inline=False)
        embed.add_field(name="Данные пользователя", value=answers[1], inline=False)
        embed.add_field(name="Чем будет полезно", value=answers[2], inline=False)
        view = UpdateBotView(interaction.user)
        await bug_channel.send(content=f"{interaction.user.mention} | `{interaction.user.name}` | "
                                       f"`{interaction.user.id}`", embed=embed, view=view)
        await interaction.response.send_message("Ваша заявка успешно отправлена!", ephemeral=True)


class UpdateBotView(View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=None)
        self.member = member

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button): child.disabled = True

    @staticmethod
    def update_status(embed: discord.Embed, status: str):
        status_field_index = None
        for i, field in enumerate(embed.fields):
            if field.name == "Статус:":
                status_field_index = i
                break
        if status_field_index is not None:
            embed.set_field_at(status_field_index, name="Статус:", value=status, inline=False)
        else:
            embed.add_field(name="Статус:", value=status, inline=False)

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.success, custom_id="accept_bug_button")
    async def accept_button_callback(self, button: discord.ui.Button, ctx: discord.Interaction):
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

    @discord.ui.button(label="Отказать", style=discord.ButtonStyle.danger, custom_id="decline_bug_button")
    async def deny_button_callback(self, button: discord.ui.Button, ctx: discord.Interaction):
        if ctx.user.guild_permissions.administrator:
            modal = UpdateBotReasonView(self.member, self)
            await ctx.response.send_modal(modal)
        else:
            await ctx.response.send_message("У вас нет прав для отклонения заявок.", ephemeral=True)

    @discord.ui.button(label="На рассмотрении", style=discord.ButtonStyle.primary, custom_id="pending_bug_button")
    async def pending_button_callback(self, button: discord.ui.Button, ctx: discord.Interaction):
        if ctx.user.guild_permissions.administrator:
            embed = ctx.message.embeds[0]
            self.update_status(embed, "На рассмотрении")
            await ctx.message.edit(embed=embed, view=self)
            await ctx.response.send_message(f"{ctx.user.mention} начал рассмотрение заявки на улучшение бота от "
                                            f"{self.member.mention} `{self.member.name}` | `{self.member.id}`")
            await self.member.send("Ваша заявка на улучшение бота находится на рассмотрении.")
        else:
            await ctx.response.send_message("У вас нет прав для изменения статуса заявок.", ephemeral=True)


class UpdateBotReasonView(Modal):
    def __init__(self, member: discord.Member, view: BugReportView):
        super().__init__(title="Причина отказа")
        self.member = member
        self.view = view
        self.add_item(discord.ui.InputText(label="Причина отказа", style=discord.InputTextStyle.long))

    async def callback(self, ctx: discord.Interaction):
        reason = self.children[0].value
        embed = ctx.message.embeds[0]
        self.view.update_status(embed, f"Отклонена: {reason}")
        self.view.disable_all_buttons()
        await ctx.message.edit(embed=embed, view=self.view)
        await ctx.response.send_message(f"{ctx.user.mention} отклонил заявку на улучшение от {self.member.mention} | "
                                        f"`{self.member.name}` | `{self.member.id}`")
        await self.member.send("Ваша заявка на улучшение бота была отклонена.\n"
                               f"Рассматривал: {ctx.user.mention} | `{ctx.user.name}`")


@bot.slash_command(name="предложение", description="Отправить предложение по улучшению бота")
async def bot_idea(ctx: discord.ApplicationContext):
    modal = UpdateBotCommand()
    await ctx.send_modal(modal)


class MyModal(Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)
        self.add_item(
            discord.ui.InputText(label='Укажите ваш вк', style=discord.InputTextStyle.short, value="vk.com/",
                                 max_length=20))
        self.add_item(
            discord.ui.InputText(label="Расскажите немного о себе", style=discord.InputTextStyle.long,
                                 placeholder="Имя, возраст, чем увлекаетесь и т.д.", min_length=50, max_length=300))
        self.add_item(
            discord.ui.InputText(label='Почему именно в нашем дискорде?', style=discord.InputTextStyle.long,
                                 placeholder='От 50 символов', min_length=50, max_length=300))
        self.add_item(
            discord.ui.InputText(label='Есть ли опыт работы в модерировании',
                                 style=discord.InputTextStyle.short,
                                 placeholder='Да/Нет. Если да, то где и кем были', max_length=250))
        self.add_item(
            discord.ui.InputText(label='Сколько времени готовы уделять должности',
                                 style=discord.InputTextStyle.short,
                                 placeholder='Время по МСК', max_length=100))

    async def callback(self, interaction: discord.Interaction):
        answers = [item.value for item in self.children]
        embed = discord.Embed(title=f"Новая заявка от пользователя: {interaction.user.name}",
                              color=discord.Color.brand_green())
        embed.add_field(name='Вк:', value=answers[0], inline=False)
        embed.add_field(name='О себе', value=answers[1], inline=False)
        embed.add_field(name='Почему именно в нашем дискорде?', value=answers[2], inline=False)
        embed.add_field(name='Опыт работы:', value=answers[3], inline=False)
        embed.add_field(name='Время для должности:', value=answers[4], inline=False)
        embed.add_field(name='', value=f'User: {interaction.user.mention}\nID: {interaction.user.id}', inline=False)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        if interaction.guild.id == 1138204059397005352:
            channel = bot.get_channel(1239561061846351873)
            xz_role = [1223995125487632486, 1219596842698801193]
        elif interaction.guild.id == 1138400553081253948:
            channel = bot.get_channel(1285617433125716030)
            xz_role = [1285618374394511394, 1285599502216204328]
        view = AcceptDeclineView(member=interaction.user, role_ids=xz_role)
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message("Ваша заявка успешно отправлена!", ephemeral=True)


class AcceptDeclineView(View):
    def __init__(self, member: discord.Member, role_ids: list, *args, **kwargs):
        super().__init__(*args, **kwargs, timeout=None)
        self.member = member
        self.role_ids = role_ids
        self.action_taken = False

    @discord.ui.button(label="Принять", style=discord.ButtonStyle.success, custom_id="accept_moder_button")
    async def accept_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.action_taken:
            await interaction.response.send_message("Действие недоступно", ephemeral=True)
            return
        roles = [interaction.guild.get_role(role_id) for role_id in self.role_ids]
        await self.member.add_roles(*roles)
        if interaction.guild.id == 1138204059397005352:
            m_roles = "Мл.Модератора Дискорда"
        elif interaction.guild.id == 1138400553081253948:
            m_roles = "Хелпер` Discord"
        await self.member.send(f"Вы приняты на должность {m_roles}")
        await interaction.response.send_message(
            f"{interaction.user.mention} принял на должность {self.member.mention}.")
        self.disable_buttons()
        self.action_taken = True
        await interaction.message.edit(view=self)

    @discord.ui.button(label="Отказать", style=discord.ButtonStyle.danger, custom_id="decline_moder_button")
    async def decline_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.action_taken:
            await interaction.response.send_message("Действие недоступно", ephemeral=True)
            return
        modal = DeclineModal(member=self.member, view=self)
        await interaction.response.send_modal(modal)

    async def decline_action_completed(self, interaction: discord.Interaction, success: bool):
        if success:
            self.disable_buttons()
            self.action_taken = True
            await interaction.message.edit(view=self)

    def disable_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button): child.disabled = True


@bot.command(name="set_modal")
async def set_modal(ctx):
    view = ApplyButtonView()
    if ctx.guild.id == 1138400553081253948:
        roles = "Хелпера Discord"
    elif ctx.guild.id == 1138204059397005352:
        roles = "Модератора Дискорда"
    embed = discord.Embed(title=f"Заявка на должность {roles}",
                          description="**Привет!** Если ты хочешь **стать Модератором** нашего Discord-сервера,"
                                      "\nто ознакомься с информацией ниже:\n"
                                      "— В случае отказа, причину вы получите в личные сообщения Discord.\n"
                                      "**Возможные причины отказа:**\n"
                                      "<:1017023806101004360:1282781539247329413>Ваш возраст менее 15 лет (возможны "
                                      "исключения)\n"
                                      "<:1017023806101004360:1282781539247329413>Слишком много нарушений на сервере.\n"
                                      "<:1017023806101004360:1282781539247329413>Некачественная заявка.\n"
                                      "<:1017023806101004360:1282781539247329413>Был получен Мут/Бан за последние 15 "
                                      "дней.\n"
                                      "<:1017023806101004360:1282781539247329413>Был плохой опыт работы с вами.\n"
                                      "<:1017023806101004360:1282781539247329413>Недостаточная активность на "
                                      "сервере.\n\n"
                                      "**[!]** Убедитесь, что у вас **включены Личные Сообщения в Discord**, чтобы мы "
                                      "могли с вами связаться.\n\n"
                                      "**Для подачи заявки нажмите на кнопку ниже и заполните форму.**",
                          color=0x5a357f)
    await ctx.send(embed=embed, view=view)


async def accept_moder_button():
    moder_view = ApplyButtonView()
    bot.add_view(moder_view)


bot.loop.create_task(accept_moder_button())


async def accept_moder_button():
    moder_view = ApplyButtonView()
    bot.add_view(moder_view)


bot.loop.create_task(accept_moder_button())


def giveaway_parse_time(time_str):
    total_seconds = 0
    matches = re.findall(r'(\d+)([hms])', time_str)

    for value, unit in matches:
        value = int(value)
        if unit == 'h':
            total_seconds += value * 3600
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 's':
            total_seconds += value
    return total_seconds


def giveaway_format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    time_parts = []
    if hours > 0:
        hour_label = "час" if hours == 1 else "часа" if hours < 5 else "часов"
        time_parts.append(f"{hours} {hour_label}")
    if minutes > 0:
        minute_label = "минута" if minutes == 1 else "минуты" if minutes < 5 else "минут"
        time_parts.append(f"{minutes} {minute_label}")
    return " ".join(time_parts)


class GiveawayView(View):
    def __init__(self, seconds, prize, description, winners_count, participants_limit):
        super().__init__(timeout=seconds)
        self.prize = prize
        self.description = description
        self.winners_count = int(winners_count)
        self.participants_limit = int(participants_limit)
        self.participants = []

    @discord.ui.button(label="Записаться", style=discord.ButtonStyle.green)
    async def join_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if len(self.participants) < self.participants_limit:
            if interaction.user not in self.participants:
                self.participants.append(interaction.user)
                await interaction.response.send_message(f"Теперь вы участвуете в розыгрыше!", ephemeral=True)
                self.update_embed(interaction)
            else:
                await interaction.response.send_message("Вы уже участвуете в этом розыгрыше.", ephemeral=True)
        else:
            await interaction.response.send_message("Лимит участников уже достигнут.", ephemeral=True)

    @discord.ui.button(label="Отказаться", style=discord.ButtonStyle.red)
    async def leave_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user in self.participants:
            self.participants.remove(interaction.user)
            await interaction.response.send_message(f"Вы успешно отказались от участия в розыгрыше.", ephemeral=True)
            self.update_embed(interaction)
        else:
            await interaction.response.send_message("Вы не участвуете в этом розыгрыше.", ephemeral=True)

    def update_embed(self, interaction):
        embed = discord.Embed(title='🎉 Розыгрыш!', description=self.description or "", color=0x42f57b)
        embed.add_field(name="Приз", value=self.prize)
        embed.add_field(name="", value=f"Участников: {str(len(self.participants))}", inline=False)
        embed.add_field(name="Максимальное кол-во участников", value=str(self.participants_limit))
        embed.set_author(name=interaction.author.name, url=interaction.author.avatar.url)
        asyncio.create_task(interaction.message.edit(embed=embed, view=self))

    async def on_timeout(self):
        embed = discord.Embed(title='🎉 Розыгрыш завершен! 🎉', description="Время вышло, вот и результаты!",
                              color=0x42f57b)
        if len(self.participants) >= self.winners_count:
            winners = random.sample(self.participants, self.winners_count)
            winners_mentions = ', '.join([winner.mention for winner in winners])
            embed.add_field(name="🏆 Победители", value=winners_mentions, inline=False)
            embed.add_field(name="🎁 Приз", value=self.prize, inline=False)
            embed.add_field(name="📜 Описание", value=self.description or "Описание отсутствует", inline=False)
            embed.add_field(name="👥 Количество участников", value=str(len(self.participants)), inline=False)
            embed.set_footer(text="Спасибо всем за участие!")
            await self.message.channel.send(embed=embed)
        else:
            embed.description += "\nК сожалению, в розыгрыше не было достаточно участников."
            await self.message.channel.send(embed=embed)


@bot.slash_command(name="giveaway", description="Создать розыгрыш")
async def giveaway(ctx, seconds, prize: discord.Option(str, description="Приз который получит победитель"),
                   winners_count: discord.Option(int, description="Макс кол-во победителей"),
                   participants_limit: discord.Option(int, description="Макс кол-во участников"),
                   description: discord.Option(str, description="Описание розыгрыша", default=False)):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.administrator:
            return 
        seconds = giveaway_parse_time(seconds)
        formatted_time = giveaway_format_time(seconds)
        embed = discord.Embed(title="🎉 Розыгрыш!", description=description or "Описание отсутствует", color=0x42f57b)
        embed.add_field(name="Приз", value=prize, inline=False)
        embed.add_field(name="Продолжительность", value=formatted_time, inline=False)
        embed.add_field(name="Кол-во победителей", value=str(winners_count), inline=False)
        embed.add_field(name="Максимальное кол-во участников", value=str(participants_limit), inline=False)
        view = GiveawayView(seconds, prize, description, winners_count, participants_limit)
        giveaway_message = await ctx.response.send_message(embed=embed, view=view)
        view.message = giveaway_message
    except Exception as e:
        print(f"Произошла ошибка:\n{e}")


# @bot.slash_command(name="find", description="Найти искомые слова в тексте")
# async def find(ctx, words: str):
#     modal = FindBanWords(words)
#     await ctx.send_modal(modal)
#
#
# class FindBanWords(discord.ui.Modal):
#     def __init__(self, words):
#         super().__init__(title="Введите текст")
#         self.words = [word.strip() for word in words.split(',')]
#         self.input = discord.ui.InputText(label="Введите текст для поиска:", style=discord.InputTextStyle.multiline)
#         self.add_item(self.input)
#
#     async def callback(self, interaction: discord.Interaction):
#         text = self.input.value
#         found_terms = [word for word in self.words if word in text]
#         await interaction.response.send_message(f"Найденные слова: {found_terms}", ephemeral=True)


ban_data_file = "ban_data.json"


def load_ban_data():
    if os.path.exists(ban_data_file):
        with open(ban_data_file, 'r') as f:
            return json.load(f)
    return {}


def save_ban_data(data):
    with open(ban_data_file, 'w') as f:
        json.dump(data, f, indent=4)


ban_data = load_ban_data()


async def get_member(ctx, target):
    if isinstance(target, discord.Member):
        return target
    try:
        user_id = int(target)
        member = await ctx.guild.fetch_member(user_id)
        return member
    except (ValueError, discord.NotFound):
        pass
    if ctx.message.reference:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        return message.author
    await ctx.reply(embed=discord.Embed(
        title="", description="Пользователь не найден. Используйте упоминание, ID или ответ на сообщение."))
    return None


def parse_time(time_str: str) -> timedelta:
    time_str = time_str.lower()
    time_re = re.compile(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?')
    match = time_re.match(time_str)
    if not match:
        return None
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    return timedelta(days=days, hours=hours, minutes=minutes)


LOG_CHANNEL_FILE = 'json/log_channel.json'


def load_log_channel(guild_id):
    """Загрузка канала для конкретного сервера из JSON файла."""
    if os.path.exists(LOG_CHANNEL_FILE):
        with open(LOG_CHANNEL_FILE, 'r') as f:
            data = json.load(f)
            return data.get(str(guild_id), {}).get('channel_id')
    return None


def save_log_channel(guild_id, channel_id):
    """Сохранение канала для конкретного сервера в JSON файл."""
    data = {}
    if os.path.exists(LOG_CHANNEL_FILE):
        with open(LOG_CHANNEL_FILE, 'r') as f:
            data = json.load(f)
    data[str(guild_id)] = {'channel_id': channel_id}
    with open(LOG_CHANNEL_FILE, 'w') as f:
        json.dump(data, f)


@bot.slash_command(name="log", description="Установить канал для логирования.")
async def log(ctx, channel: discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.Thread |
                            discord.DMChannel = None):
    """Команда для установки канала для логирования."""
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if ctx.author.guild_permissions.administrator:
        if channel is None:
            current_channel_id = load_log_channel(ctx.guild.id)
            if current_channel_id:
                await ctx.respond(f"Текущий канал логов: <#{current_channel_id}>", ephemeral=True)
            else:
                await ctx.respond("Канал для логов не установлен.", ephemeral=True)
            return
        save_log_channel(ctx.guild.id, channel.id)
        await ctx.respond(f"Канал для логов установлен: <#{channel.id}>")
    else:
        await ctx.respond(embed=Embed(description="У вас нет прав для использования этой команды!",color=0x7b68ee),
                          ephemeral=True)
        return


async def send_log(guild_id, message=None, embed=None):
    """Отправка логов в заданный канал для конкретного сервера."""
    log_channel_id = load_log_channel(guild_id)
    if log_channel_id is not None:
        channel = bot.get_channel(log_channel_id)
        if channel is not None:
            if message and embed:
                await channel.send(content=message, embed=embed)
            elif embed:
                await channel.send(embed=embed)
            elif message:
                await channel.send(content=message)


async def get_user(ctx, arg):
    if ctx.message.reference:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        return message.author
    # Проверка на упоминание
    mention_match = re.match(r"<@!?(\d+)>", arg)
    if mention_match:
        user_id = int(mention_match.group(1))
        member = await ctx.guild.fetch_member(user_id)
        return member
    # Проверка на ID
    try:
        user_id = int(arg)
        member = await ctx.guild.fetch_member(user_id)
        return member
    except ValueError:
        pass
    # Поиск по имени пользователя
    member = discord.utils.get(ctx.guild.members, name=arg)
    if member:
        return member
    # Поиск по полному имени (никнейму)
    member = discord.utils.get(ctx.guild.members, nick=arg)
    return member


@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, target: str, duration: str, *, reason: str = None):
    member = await get_user(ctx, target)
    if not member:
        await ctx.reply(discord.Embed(title="", description="Пользователь не найден."))
        return
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False,
                                                                                              add_reactions=False))
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(mute_role, send_messages=False, add_reactions=False)
    time_delta = parse_time(duration)
    if not time_delta:
        await ctx.reply("Неверный формат времени. Используйте, например, 1d, 1h, 1m, 1h30m и т.д.")
        return
    embed = discord.Embed(title="", description=f":white_check_mark: Участник {member.mention} замьючен! 🙊")
    if duration: embed.add_field(name="Срок", value=f"{duration}")
    if reason: embed.add_field(name="Причина", value=reason, inline=False)
    await member.add_roles(mute_role)
    await member.timeout_for(time_delta)
    await ctx.reply(embed=embed)
    await asyncio.sleep(time_delta.total_seconds())
    await member.remove_roles(mute_role)


@bot.command(name="unmute", aliaces=["размут"])
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, *, target):
    member = await get_user(ctx, target)
    if target is None:
        pref = get_prefix(bot, ctx.message)
        await ctx.reply(embed=discord.Embed(title="", description=f"Использование команды: {pref}unmute ID|mention"))
    if not member:
        await ctx.reply(embed=discord.Embed(title="", description="Пользователь не найден."))
        return
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await member.timeout_for(0)
    await ctx.reply(embed=discord.Embed(title="",
                                        description=f":white_check_mark: Участник {member.name} размьючен! 😊"))


@bot.command(name="mutes")
async def mutes(ctx):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        await ctx.reply(discord.Embed(title="", description="Роль мута не найдена"))
        return
    muted_members = [member.mention for member in ctx.guild.members
                     if mute_role in member.roles or (hasattr(member, 'timed_out_until') and member.timed_out_until)]
    mutes_em = discord.Embed(title="", description=f"Замученные пользователи: {', '.join(muted_members)}")
    if muted_members:
        await ctx.reply(embed=mutes_em)
    else:
        await ctx.reply(embed=discord.Embed(title="", description="Нет замученных пользователей."))


@bot.command(name="ban")
async def ban(ctx, target, days: int = 0, reason: str = ""):
    if ctx.author.guild_permissions.ban_members:
        member = await get_member(ctx, target)
        if not member:
            return
        await member.ban(reason=f"{reason if reason else None}")
        if days > 0:
            unban_time = (datetime.now() + timedelta(days=days)).isoformat()
            ban_data[str(member.id)] = unban_time
            save_ban_data(ban_data)
        ban = discord.Embed(title="",
                            description=f"{member.mention} был забанен {'на ' + str(days) + ' дней' if days > 0 else ''}.")
        await ctx.reply(embed=ban)


@bot.command(name="unban")
async def unban(ctx, target: discord.User):
    if ctx.author.guild_permissions.ban_members:
        await ctx.guild.unban(target)
        if str(target.id) in ban_data:
            del ban_data[str(target.id)]
            save_ban_data(ban_data)
        await ctx.reply(embed=discord.Embed(title="", description=f"{target.mention} был разбанен."))


@tasks.loop(minutes=1)
async def check_unban():
    current_time = datetime.now().isoformat()
    for guild in bot.guilds:
        for user_id, unban_time in list(ban_data.items()):
            if current_time > unban_time:
                user = await bot.fetch_user(int(user_id))
                await guild.unban(user)
                del ban_data[user_id]
                save_ban_data(ban_data)


@bot.slash_command(name="faq", description="Информация о боте")
async def _faq(ctx):
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    version = "1.0"
    pref = get_prefix(bot, ctx) if ctx.guild is not None else "Вы не на сервере!"
    embed = discord.Embed(title="remod3Bot",
                          description=(
                              "remod3Bot - это многофункциональный бот, предназначенный для крупных серверов "
                              "и более удобного управления ролями и сервером. Написав разработчику, вы можете заказать "
                              "команду/функционал для своего сервера."), color=discord.Color.default())
    embed.add_field(name="Основные команды",
                    value="`/help` - Меню команд.\n`/предложение` - Написать идею для бота.\n`/bug_report` - Сообщить "
                          "о баге.\n`/update` - Последние обновления.", inline=True)
    embed.add_field(name="Информация о боте",
                    value=f"Кол-во серверов: {len(bot.guilds)}\n"
                          f"Версия: {version}\n"
                          f"Дата создания: <t:1707598800:D> (<t:1707598800:R>)", inline=True)
    embed.add_field(name="Разработчики", value="1. `remodik` (`743864658951274528`)", inline=False)
    if ctx.user.guild_permissions.administrator or ctx.user.guild_permissions.manage_guild:
        log_channel_id = load_log_channel(ctx.guild.id)
        log_channel = f"<#{log_channel_id}>" if log_channel_id else "Не установлен"
        embed.add_field(name="Канал логов", value=f"{log_channel}", inline=True)
    embed.add_field(name="Префикс команд", value=f"`{pref}`", inline=True)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
    btn1 = Button(style=ButtonStyle.grey, label="Информация о создателе", url='https://solo.to/remod3')
    btn2 = Button(style=ButtonStyle.green, label="Поддержать автора", url="https://www.donationalerts.com/r/remod3")
    view = View()
    view.add_item(btn1)
    view.add_item(btn2)
    await ctx.response.send_message(embed=embed, view=view)


@bot.slash_command(name="inform", description="Информация о боте (сокращенно)")
async def inform(ctx):
    version = "1.0"
    embed = discord.Embed(
        title="Информация о боте",
        description="remod3Bot - это многофункциональный бот, предназначенный для крупных серверов "
                    "и более удобного управления ролями и сервером. Написав разработчику, вы можете заказать "
                    "команду/функционал для своего сервера",
        color=discord.Color.default())
    embed.add_field(
        name="Информация о боте",
        value=f"Версия: {version}\n"
              f"Дата создания: <t:1697887295:D> (<t:1697887295:R>)",
        inline=False)
    embed.add_field(
        name='Разработчики',
        value='1. `remodik` (`743864658951274528`)')
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/yzJCZz-vGE8Gmd1x-AqmGaDRA"
                            "-TOvD5ObRi__IMen2Y/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/120"
                            "6275841395392552/a_1b9fe156b57bf2f57b054a27c0fe4f73.gif?width=575&heig"
                            "ht=575")
    embed.set_author(name="remod3Bot", icon_url="https://images-ext-1.discordapp.net/external/yzJCZz-vGE8Gmd1x-AqmGaDRA"
                                                "-TOvD5ObRi__IMen2Y/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/120"
                                                "6275841395392552/a_1b9fe156b57bf2f57b054a27c0fe4f73.gif?width=575&heig"
                                                "ht=575")

    btn1 = Button(
        style=discord.ButtonStyle.grey,
        label="Информация о создателе",
        url='https://solo.to/remod3')
    btn2 = Button(
        style=discord.ButtonStyle.green,
        label="Поддержать автора",
        url="https://www.donationalerts.com/r/remod3")
    view = View()
    view.add_item(btn1)
    view.add_item(btn2)
    await ctx.response.send_message(embed=embed, view=view)


@bot.slash_command(name="mserver", description="Получить информацию о сервере")
async def _mserver(ctx: Interaction, ip_address: discord.Option(str, "IP адрес сервера")):
    await ctx.defer(ephemeral=True)
    url = f"https://api.mcsrvstat.us/2/{ip_address}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
    try:
        if data.get('online'):
            players_online = data.get('players', {}).get('online', 'Хз')
            server_name = data.get("hostname", "Хз")
            server_version = data.get('version', "Хз")
            software_n = data.get('software', "Хз")
            info_n = ' '.join(data.get('motd', {}).get('clean', ["Хз"]))
            embed = discord.Embed(title=f"Информация о сервере {ip_address}", color=discord.Color.default())
            embed.add_field(name="Игроков онлайн", value=f"{players_online} онлайн", inline=True)
            embed.add_field(name="Имя хоста", value=server_name, inline=True)
            embed.add_field(name="Версия сервера", value=server_version, inline=True)
            embed.add_field(name="ПО сервера", value=software_n, inline=True)
            embed.add_field(name="Описание", value=info_n, inline=True)
            await ctx.followup.send(embed=embed, ephemeral=True)
        else:
            await ctx.followup.send(content=f"Сервер {ip_address} не отвечает или не найден.", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: mserver")


class UpdateView(View):
    def __init__(self, updates, current_page=0):
        super().__init__()
        self.updates = updates
        self.current_page = current_page
        self.update_buttons()

        async def on_error(self, error: Exception, interaction: Interaction) -> None:
            await interaction.response.send_message("Произошла ошибка! Свяжитесь с разработчиком для решения проблемы: "
                                                    f"`remodik`\n\n{error}")

    def update_buttons(self):
        self.clear_items()
        if len(self.updates) > 1:
            if self.current_page > 0:
                self.add_item(Button(label="В начало", style=ButtonStyle.primary, custom_id="start",
                                     emoji=PartialEmoji(name="previous_pages", id=989035748424568832)))
                self.add_item(Button(label="Назад", style=ButtonStyle.primary, custom_id="previous",
                                     emoji=PartialEmoji(name="prev_page", id=684354640019587112)))
            if self.current_page < len(self.updates) - 1:
                self.add_item(Button(label="Вперёд", style=ButtonStyle.primary, custom_id="next",
                                     emoji=PartialEmoji(name="next_page", id=684354639973318817)))
                self.add_item(Button(label="В конец", style=ButtonStyle.primary, custom_id="end",
                                     emoji=PartialEmoji(name="next_pages", id=989035746885246986)))

    async def on_button_click(self, interaction: Interaction):
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("Это не ваша команда!", ephemeral=True)
        if interaction.custom_id == "start":
            self.current_page = 0
        elif interaction.custom_id == "previous":
            self.current_page = max(0, self.current_page - 1)
        elif interaction.custom_id == "next":
            self.current_page = min(len(self.updates) - 1, self.current_page + 1)
        elif interaction.custom_id == "end":
            self.current_page = len(self.updates) - 1
        self.update_buttons()
        embed = Embed(title="История обновлений", description=self.updates[self.current_page], color=Color.default())
        await interaction.response.edit_message(embed=embed, view=self)


@bot.slash_command(name="update", description="Последнее обновление")
async def обновление(ctx):
    current_update = ("**10.11.2024** Команды управления ролями были сгруппированы.\n"
                      "Использование: `/role {command}`")
    embed = Embed(title="", description=current_update, color=Color.default())
    await ctx.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command(name="hist_update", description="История обновлений бота")
async def история(ctx):
    pref = get_prefix(bot, ctx) if ctx.guild else "r!"
    updates = [
        "**17.09.2024:** Добавлена команда - `anime`.\n"
        "Посмотреть информацию о каком либо аниме теперь стало ещё проще!\n"
        "Использование команды: `/anime {{name}}`, где {{name}} - это название аниме, "
        "информацию о котором вы хотите получить.\n\n"
        "**23.09.2024**: Добавлена команда - `set_system`.\n"
        "Предназначена для установки канала, в который бот будет отправлять сообщения о входе/выходе "
        "игроков с сервера.\n"
        "Использование команды: `/set_system {{channel}}`, где {{channel}} - это текстовый канал.\n\n"
        "**30.09.2024:** Доработана команда `anime`\n"
        "Теперь выбор конкретного аниме стал гораздо легче.\n"
        "После ввода команды бот выдаст список аниме, в названиях которых есть слово, которое вы ввели\n\n"
        "**05.10.2024:** Добавлена команда - `предложение`\n"
        "Есть идеи по улучшению бота? Напишите её разработчику, и он её обязательно рассмотрит!\n"
        "Использование команды: `/предложение`\n\n"
        "**05.10.2024:** Добавлена команда - `bug_report`\n"
        "Нашли баг в боте? Сообщите о нём разработчику!\n"
        "Использование команды: `/bug_report`\n\n"
        "**06.10.2024:** Добавлена команда `prefix`\n"
        "Для изменений префикса команд. (По умолчанию `r!{{command}}`)\n"
        "Использование команды: `{pref}prefix {{prefix}}`\n\n"
        "**06.11.2024** Добавлена команда - `log`.\n"
        "Для оправки логирования действий.\n"
        "Использование команды: `/log {{channel}}`\n\n"
        "**06.11.2024** Обновлена команда - `faq`.\n"
        "Теперь показывает текущий префикс на сервере.\n\n"
        "**06.11.2024** Добавлена команда `caps`.\n"
        "Подсчитывает % верхнего регистра в вашем сообщении.\n"
        "Использование команды: `/caps`\n\n"
        "**06.11.2024** Добавлена команда `pin`.\n"
        "Переключает параметр `Показывать участников с ролью отдельно от остальных участников в сети`\n"
        "Использование команды: `/role pin {{role}}`\n\n"
        "**06.11.2024** Добавлена команда - `mentions`.\n"
        "Переключает параметр `Позволить всем @упоминать эту роль`\n"
        "Использование команды: `/mentions {{role}} {{True|False}}`\n\n"
        "**10.11.2024** Команды управления ролями были сгруппированы.\n"
        "Использование: `/role {{command}}`\n\n\n"
        "**В разработке**\nСистема управления модерацией"
    ]
    embed = Embed(title="История обновлений", description=updates[0].format(pref=pref), color=Color.default())
    view = UpdateView(updates)
    await ctx.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.slash_command(name="presence")
async def find_presence(ctx: discord.Interaction, text: str):
    text = text.lower()
    embed = discord.Embed(title=f"Поиск активности",
                          description=f"Пользователи с активностью, содержащей '{text}'",
                          color=discord.Color.default())
    if ctx.guild is None:
        await ctx.response.send_message("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if bot.user not in ctx.guild.members:
        await ctx.response.send_message("Бот не найден среди участников этого сервера.", ephemeral=True)
        return
    for member in ctx.guild.members:
        if member.activity and member.activity.name:
            activity_name = member.activity.name.lower()
            if text in activity_name:
                embed.add_field(name=f"", value=f"user: {member.mention}\n{member.activity.name}", inline=False)
    await ctx.response.send_message(embed=embed)


bot.add_application_command(roles)
bot.add_application_command(mod_com)
bot.run(data_as['token'])
#match input("Connect RPC? >> "):
#    case 'y' | 'Y' | '+' | 'да' | 'Да' | 'Yes' | 'yes':
#        rpc = Presence("1206275841395392552")
#        rpc.connect()
#        rpc.update(state="Author: remodik", details="Version: 1.0", start=timedelta(days=500).total_seconds(),
#                   large_image="a_1b9fe156b57bf2f57b054a27c0fe4f73_1_",
#                   buttons=[{"label": "User Install",
#                             "url": "https://discord.com/oauth2/authorize?client_id=1206275841395392552&integration"
#                                    "_type=1&scope=applications.commands"},
#                            {"label": "Guild Install",
#                             "url": "https://discord.com/oauth2/authorize?client_id=1206275841395392552&permissions"
#                                    "=8&integration_type=0&scope=bot+applications.commands"}])
#        bot.run(data_as['token'])

        # async def start_bot():
        #     await bot.start(data_as['token'])
        #
        # if __name__ == "__main__":
        #     asyncio.run(start_bot())
#    case 'n' | 'N' | '-' | 'нет' | 'Нет' | 'no' | 'No':
        # bot.run("MTIwNjI3NTg0MTM5NTM5MjU1Mg.GHQNw8.OXoM0SCc-U0ZbMg1pOfDqDIxEhjYV15olb9D0Y")
#        bot.run(data_as['token'])
        # async def start_bot():
        #     await bot.start(data_as['token'])
        #
        # if __name__ == "__main__":
        #     asyncio.run(start_bot())
