import ast
import datetime
import logging
import math
import operator
import os
import sys
import time
from datetime import (timedelta, datetime)

import aiohttp
import discord
import re
import requests
from discord import (Color, Embed, User, TextChannel, NotFound, VoiceChannel, ForumChannel, DMChannel, StageChannel,
                     CategoryChannel, GroupChannel, Status, Forbidden, Option, Role, Member, utils, AutocompleteContext,
                     abc, Thread, Intents)
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import tasks, commands
from discord.utils import get
import json

block_users = []
if os.path.exists("json/prefixes.json"):
    with open("json/prefixes.json", "r") as f:
        prefixes = json.load(f)
else:
    prefixes = {}

def get_prefix(bot, message):
    guild_id = str(message.guild.id)
    return prefixes.get(guild_id, "r!")

logging.basicConfig(level=logging.INFO, format="[%(levelname)s]%(asctime)s - %(message)s", stream=sys.stdout)
logging.info("Бот запущен.")
bot = commands.Bot(command_prefix=get_prefix,intents=Intents.all(),auto_sync_commands=True,sync_commands_debug=True)
rcm = discord.SlashCommandGroup("role", "description")
bgac = bot.get_application_command
for filename in os.listdir("C:\\Users\\slend\\OneDrive\\OneDrive\\bot\\commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

bot.add_application_command(rcm)
log = bot.get_cog("SendLog")
if log is None:
    print("Ког SendLog не загружен.")
bot.remove_command("help")
""" Префиксы бота"""
@bot.command(name="prefix")
async def set_prefix(ctx, new_prefix=None):
    if ctx.author.guild_permissions.administrator:
        if new_prefix is None:
            await ctx.reply(f"Текущий префикс: `{get_prefix(bot, ctx)}`")
            return
        guild_id = str(ctx.guild.id)
        prefixes[guild_id] = new_prefix
        with open("json/prefixes.json", "w") as f:
            json.dump(prefixes, f)
        await ctx.send(f"Префикс изменён на: {new_prefix}")
""" Обработчик ошибок префиксных команд """
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("У вас нет необходимых прав для использования этой команды.")
    elif isinstance(error, AttributeError):
        await ctx.reply("Для использования этой команды добавьте меня на сервер!")
    elif isinstance(error, Forbidden):
        await ctx.reply("У меня нет необходимых прав для использования этой команды.")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print(f"Произошла ошибка: {error}")
""""""

""""""
class BugCommand(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Заявка на баг")
        self.add_item(discord.ui.InputText(label="Что за баг?", style=discord.InputTextStyle.long,
                                   min_length=15, placeholder="Напишите суть бага", max_length=500))
        self.add_item(discord.ui.InputText(label="Как с вами связаться", style=discord.InputTextStyle.short,
                                   placeholder="Укажите ваши контактные данные", max_length=100))
        self.add_item(discord.ui.InputText(label="Доказательства", placeholder="Укажите ссылку на видео/фото",
                                   max_length=250))

    async def callback(self, interaction: discord.Interaction):
        answers = [item.value for item in self.children]
        bug_channel = bot.get_channel(1315002924862148635)

        if not bug_channel:
            await interaction.response.send_message("Канал для отправки багов не найден. Свяжитесь с разработчиком.",
                                                    ephemeral=True)
            return
        embed = Embed(title="Заявка на баг", color=Color.embed_background())
        embed.add_field(name="Суть бага", value=answers[0], inline=False)
        embed.add_field(name="Данные пользователя", value=answers[1], inline=False)
        embed.add_field(name="Доказательства", value=answers[2], inline=False)
        view = BugReportView(interaction.user)
        await bug_channel.send(content=f"{interaction.user.mention} | `{interaction.user.name}` | "
                                       f"`{interaction.user.id}`", embed=embed, view=view)
        await interaction.response.send_message("Ваша заявка успешно отправлена!", ephemeral=True)
class BugReportView(discord.ui.View):
    def __init__(self, member: Member):
        super().__init__(timeout=None)
        self.member = member

    def disable_all_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button): child.disabled = True

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
class ReasonModal(discord.ui.Modal):
    def __init__(self, member: Member, view: BugReportView):
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
""""""
def get_id_ac(ctx: AutocompleteContext):
    if bot.application_commands:
        return [command.name for command in bot.application_commands if hasattr(command, 'id')]
    else:
        return ["Нет доступных команд"]


@bot.slash_command(name="get_id", guild_ids=[1148996038363975800, 1214617864863219732, 1315002924048318506],
                   default_member_permissions=discord.Permissions(administrator=True))
async def get_id(ctx, arg: Option(str, autocomplete=get_id_ac)):
    try:
        command = get(bot.application_commands, name=arg)
        if command:
            await ctx.respond(f"ID команды '{arg}': {command.id}", ephemeral=True)
        else:
            await ctx.respond(f"Команда '{arg}' не найдена.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"Произошла ошибка: {str(e)}", ephemeral=True)
""""""
class HelpSelect(discord.ui.Select):
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
            category_title = "Команды управления ролями"
        elif selected_value == "Развлечения":
            category_title = "Развлекательные команды"
        elif selected_value == "Другое":
            category_title = "Прочие команды"
        else:
            category_title = "Список команд"

        embed = Embed(title=category_title, color=Color.blue())

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
                    'description': f'</set_system:{bgac("set_system").id}> - Установить канал для уведомлений о '
                                   f'входах/выходах.',
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
                    'description': f'</kick:{bgac("kick").id}> - Выгнать пользователя с сервера.',
                    'requires_permission': True
                },
                'clear': {
                    'permission': 'manage_messages',
                    'description': f'</clear:{bgac("clear").id}> - Удалить сообщения в чате.',
                    'requires_permission': True
                },
                'delchat': {
                    'permission': 'manage_channels',
                    'description': f'</delchat:{bgac("delchat").id}> - Удалить текстовый чат.',
                    'requires_permission': True
                },
                'delvoice': {
                    'permission': 'manage_channels',
                    'description': f'</delvoice:{bgac("rcm").id}delvoice> - Удалить голосовой чат.',
                    'requires_permission': True
                },
                'nick': {
                    'permission': 'manage_nicknames',
                    'description': f'</nick:{bgac("nick").id}> - Изменить ник пользователя.',
                    'requires_permission': True
                },
                'presence': {
                    'permission': 'manage_guild',
                    'description': f'</presence:{bgac("presence").id}> - Поиск людей с определённой активностью.',
                    'requires_permission': True
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Роли":
            commands_permissions = {
                'add': {
                    'permission': 'manage_roles',
                    'description': f'</role add:{bgac("role").id}> - Выдать пользователю роль.',
                    'requires_permission': True
                },
                'create': {
                    'permission': 'manage_roles',
                    'description': f'</role create:{bgac("role").id}> - Создать роль.',
                    'requires_permission': True
                },
                'delperm': {
                    'permission': 'administrator',
                    'description': f'</role delperm:{bgac("role").id}> - Забрать право у роли.',
                    'requires_permission': True
                },
                'do': {
                    'permission': 'manage_roles',
                    'description': f'</role do:{bgac("role").id}> - Понизить роль пользователя на 1 уровень.',
                    'requires_permission': True
                },
                'delete': {
                    'permission': 'manage_roles',
                    'description': f'</role delete:{bgac("role").id}> - Удалить роль.',
                    'requires_permission': True
                },
                'pre': {
                    'permission': 'administrator',
                    'description': f'</role pre:{bgac("role").id}> - Изменить приоритет роли.',
                    'requires_permission': True
                },
                'clear': {
                    'permission': 'administrator',
                    'description': f'</role clear:{bgac("role").id}> - Забрать все роли у пользователя.',
                    'requires_permission': True
                },
                'color': {
                    'permission': 'manage_roles',
                    'description': f'</role color:{bgac("role").id}> - Изменить цвет роли.',
                    'requires_permission': True
                },
                'remove': {
                    'permission': 'manage_roles',
                    'description': f'</role delete:{bgac("role").id}> - Забрать роль у пользователя.',
                    'requires_permission': True
                },
                'replace': {
                    'permission': 'manage_roles',
                    'description': f'</role replace:{bgac("role").id}> - Заменить роль у пользователя.',
                    'requires_permission': True
                },
                'name': {
                    'permission': 'manage_roles',
                    'description': f'</role rename:{bgac("role").id}> - Переименовать роль.',
                    'requires_permission': True
                },
                'list': {
                    'permission': 'manage_roles',
                    'description': f'</role list:{bgac("role").id}> - Список ролей сервера.',
                    'requires_permission': True
                },
                'setperm': {
                    'permission': 'administrator',
                    'description': f'</role setperm:{bgac("role").id}> - Установить право для роли.',
                    'requires_permission': True
                },
                'up': {
                    'permission': 'manage_roles',
                    'description': f'</role up:{bgac("role").id}> - Повысить роль пользователя на 1 уровень.',
                    'requires_permission': True
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Развлечения":
            commands_permissions = {
                # 'giveaway': {
                #     'permission': 'administrator',
                #     'description': '</giveaway:1306213844909297686> - Сделать розыгрыш на сервере.',
                #     'requires_permission': True
                # },
                'anime': {
                    'permission': '',
                    'description': f'</anime:{bgac("anime").id}> - Посмотреть информацию об аниме.',
                    'requires_permission': False
                }
            }
            embed = add_commands_to_embed(commands_permissions)
        elif selected_value == "Другое":
            commands_permissions = {
                'embed': {
                    'permission': 'manage_messages',
                    'description': f'</embed:{bgac("embed").id}> - Создание embed-сообщений.',
                    'requires_permission': True,
                },
                'mserver': {
                    'permission': 'administrator',
                    'description': f'</mserver:{bgac("mserver").id}> - Посмотреть информацию о Minecraft сервере.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'avatar': {
                    'permission': 'administrator',
                    'description': f'</avatar:{bgac("avatar").id}> Получить пользователя или сервера.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'calculate': {
                    'permission': 'administrator',
                    'description': f'</calculate:{bgac("calculate").id}> - Посчитать выражение.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'faq': {
                    'permission': 'administrator',
                    'description': f'</faq:{bgac("faq").id}> - Информация о боте.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'предложение': {
                    'permission': 'administrator',
                    'description': f'</предложение:{bgac("предложение").id}> - Предложить улучшить бота.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'bug_report': {
                    'permission': None,
                    'description': f'</bug_report:{bgac("bug_report").id}> - Сообщить о баге в боте.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'caps': {
                    'permission': 'manage_messages',
                    'description': f'</caps:{bgac("caps").id}> - Узнать % верхнего регистра.',
                    'requires_permission': False,
                    'guild_access': None,
                    'role_access': None,
                    'user_access': None
                },
                'send_stat': {
                    'permission': 'administrator',
                    'description': f'</send_stat:{bgac("send_stat").id}> - Назначить канал для статистики сервера.',
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

@bot.slash_command(name="help", description="Информация о моих командах")
async def _help(ctx, channel: Option(abc.GuildChannel,"Куда отправить?", required=False)):
    view = HelpView()
    if isinstance(channel, (DMChannel, StageChannel, ForumChannel, GroupChannel, CategoryChannel)):
        await ctx.respond("Нельзя туда такое отправлять!", ephemeral=True)
        return
    if channel is None:
        await ctx.response.send_message(ephemeral=True, view=view, content="Помощь по моим командам")
    else:
        if (not channel.permissions_for(ctx.author).send_messages and not channel.permissions_for(ctx.author).
                read_messages):
            await ctx.respond("У вас нет прав для отправки сообщений в этом канале.", ephemeral=True)
            return
        else:
            await channel.send(view=view, content="Помощь по моим командам")
            await ctx.respond("Успешно!", ephemeral=True)
""" Ивент для сервера FieryBlaze"""
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    server_id = 1138400553081253948
    if message.guild and message.guild.id == server_id:
        # Проверка упоминания специальных пользователей
        special_users = {863326185451028521, 835874448779247688}
        if any(user.id in special_users for user in message.mentions):
            await message.delete()
            await message.channel.send(f'{message.author.mention}, :shushing_face:')
            return

        # Проверка триггерных слов
        trigger_words = {"сервер запущен", "серв работает", "серв запущен", "сервер работает"}
        if any(word in message.content.lower() for word in trigger_words):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, сервер закрыт на переработку. Подробнее: "
                "https://discord.com/channels/1138400553081253948/1138400553995604070")
            return

    await bot.process_commands(message)
""" Функции для статистики """
def save_message_id(channel_id, message_id):
    try:
        # Убедитесь, что директория существует
        if not os.path.exists("json"):
            os.makedirs("json")
        # Считайте существующий файл или создайте пустой объект
        try:
            with open('json/message_cache.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        # Добавьте данные и сохраните файл
        data[str(channel_id)] = message_id
        with open('json/message_cache.json', 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Ошибка при сохранении ID сообщения: {e}")

def get_message_id(channel_id):
    try:
        with open('json/message_cache.json', 'r') as file:
            data = json.load(file)
        return data.get(str(channel_id))
    except FileNotFoundError:
        return None
""" Статистика сервера """
@bot.slash_command(name="send_stat", description='Чат для отправки статистики сервера')
async def send_stat(ctx, channel: discord.abc.GuildChannel = None):
    try:
        if isinstance(channel, (VoiceChannel, StageChannel, DMChannel, CategoryChannel, GroupChannel, ForumChannel)):
            await ctx.response.send_message("Пожалуйста, выберите текстовый канал для отправки статистики.",
                                            ephemeral=True)
            return

        if not channel.permissions_for(ctx.guild.me).send_messages:
            await ctx.response.send_message(f"У меня нет прав на отправку сообщений в канал {channel.mention}.",
                                            ephemeral=True)
            return

        if not ctx.author.guild_permissions.manage_guild:
            await ctx.response.send_message("У вас нет прав для настройки канала статистики.", ephemeral=True)
            return

        channel_id = channel.id
        embed = await get_server_info(ctx.guild)
        message = await channel.send(embed=embed)
        save_message_id(channel_id, message.id)
        await ctx.response.send_message(f"Статистика будет отправляться каждую минуту в канал {channel.mention}")
        embed_log = Embed(title="Канал статистики настроен", color=0x7b68ee)
        embed_log.add_field(name="Автор", value=ctx.author.mention, inline=True)
        embed_log.add_field(name="Канал", value=channel.mention)
        await log.send_log(ctx.guild.id, embed=embed_log)
        emb = Embed(title='Инструкция по использованию команды send_stat', color=0x5a357f,
                    description="Эта команда позволяет настроить канал для отправки статистики сервера каждую минуту.")
        emb.add_field(name="Как использовать:",
                      value="1. Убедитесь, что у вас есть права на управление сервером.\n"
                            "2. Выберите текстовый канал, куда будет отправляться статистика.\n"
                            "3. Команда будет отправлять информацию каждые 5 минут.", inline=False)
        emb.add_field(name="Важно!", value="Убедитесь, что у бота есть права на отправку сообщений в "
                                           "выбранный канал.", inline=False)
        if channel is None:
            await ctx.respond(embed=embed, ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} "
              f"| {ctx.author.id}\nКоманда: send_stat")

async def update_old_messages():
    try:
        with open('json/message_cache.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return

    for channel_id, message_id in data.items():
        channel = bot.get_channel(int(channel_id))
        if channel:
            try:
                message = await channel.fetch_message(message_id)
                embed = await get_server_info(channel.guild)
                await message.edit(embed=embed)
            except discord.NotFound:
                embed = await get_server_info(channel.guild)
                message = await channel.send(embed=embed)
                save_message_id(channel.id, message.id)


@tasks.loop(minutes=1)
async def send_statistics():
    with open('json/message_cache.json', 'r') as file:
        data = json.load(file)
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
""" Функция для статистики сервера """
async def get_server_info(guild):
    embed = Embed(title=f'Статистика сервера Discord', color=Color.embed_background())
    roles = len(guild.roles)
    voice_members = sum(1 for member in guild.members if member.voice)
    emojis = len(guild.emojis)
    members = guild.member_count
    bots = sum(1 for member in guild.members if member.bot)
    humans = members - bots
    online = sum(1 for member in guild.members if member.status == Status.online)
    idle = sum(1 for member in guild.members if member.status == Status.idle)
    do_not_disturb = sum(1 for member in guild.members if member.status == Status.do_not_disturb)
    offline = sum(1 for member in guild.members if member.status == Status.offline)
    embed.add_field(name='Общее', value=f"<:icon_edm:1269748398068727829> Кол-во ролей: **{roles}**\n"
                                        f"<:icon_prm:1269748753045393510> Голосовой онлайн: "
                                        f"**{voice_members}**\n"
                                        f"<:icon_emj:1269748064961433631> Кол-во эмодзи: **{emojis}**",inline=True)
    embed.add_field(name=f'Участников [{members}]', value=f"Людей: **{humans}**\n"
                                                          f"Ботов: **{bots}**", inline=True)
    embed.add_field(name='По статусам', value=f'<a:icon_onl:1269732534552498226> В сети: {online}\n'
                                              f'<a:icon_inct:1269732551384105060> Не активен: {idle}\n'
                                              f'<a:icon_nbs:1269732558300778566> Не беспокоить: {do_not_disturb}\n'
                                              f'<a:icon_ofl:1269742137331941508> Не в сети: {offline}',
                    inline=True)
    text_channels = sum(1 for channel in guild.channels if isinstance(channel, TextChannel))
    voice_channels = sum(1 for channel in guild.channels if isinstance(channel, VoiceChannel))
    stage_channels = sum(1 for channel in guild.channels if isinstance(channel, StageChannel))
    categories = sum(1 for channel in guild.channels if isinstance(channel, CategoryChannel))
    embed.add_field(name='Каналов', value=f"<:icon_cht:1269750004663324786> Текстовые: {text_channels}\n"
                                          f"<:icon_vc:1269746265185587220> Голосовые: {voice_channels}\n"
                                          f"<:icon_stg:1269746018086555869> Трибуны: {stage_channels}\n"
                                          f"<:icon_ctg:1269751898458685535> Категории: {categories}", inline=True)
    boost_level = guild.premium_tier
    boosters = len(guild.premium_subscribers)
    boosts = guild.premium_subscription_count
    embed.add_field(name='Буст сервера', value=f'<:boost_lvl:1269747700325285989> Уровень буста: {boost_level}\n'
                                               f'<:boosts:1269747791194751086> Кол-во бустеров: {boosters}\n'
                                               f'<a:boosters:1269746647139881133> Кол-во бустов: {boosts}', inline=True)
    timestamp = 60
    current_time = time.time()
    target_time = current_time + timestamp
    unix_time = int(target_time)
    embed.add_field(name="", value=f"Следующее обновление: <t:{unix_time}:R>", inline=False)
    return embed


def load_warnings():
    try:
        with open('json/user_warns.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'user_warns': {}, 'total': 0}


def save_warnings(data):
    with open('json/user_warns.json', 'w') as f:
        json.dump(data, f, indent=4)
""" Наказания """
@bot.command(name='warn')
async def warn(ctx, target: User = None, duration: str = None, *, reason: str = ''):
    global expiry_time
    if ctx.author.guild_permissions.administrator:
        pref = get_prefix(bot, ctx)
        if target is None and ctx.message.reference:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            target = referenced_message.author
        if target is None:
            await ctx.reply(embed=Embed(title="", description=f'Команда "{pref}warn"\nВыдает указанному участнику '
                                                              f'вечное или временное предупреждение.',
                                        color=Color.embed_background()))
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
                await ctx.reply('Неверный формат времени. Используйте дни (d), часы (h) или минуты (m).')
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
        embed = Embed(title='', description=f'Участник {target.mention} получил предупреждение `#{warning_id}` '
                                            f'`(случай #{total_warning_id})`.', color=0x5a357f)
        embed.add_field(name='Причина', value=reason if reason else 'Не указана')
        if expiry_time_str:
            embed.add_field(name='Истекает', value=f'<t:{int(expiry_time.timestamp())}:F> '
                                                   f'(<t:{int(expiry_time.timestamp())}:R>)')
        else:
            pass
        await ctx.send(embed=embed)

@bot.command(name='unwarn')
async def unwarn(ctx, case_id: int = None):
    if ctx.author.guild_permissions.administrator:
        if case_id is None:
            await ctx.reply(embed=Embed(title="Снять предупреждение участнику",
                                        description='Снимает с участника предупреждение по номеру случая из команды '
                                                    '".warns".\n\n**Использование**\n`.unwarn <номер случая>`\n\n'
                                                    '**Пример**\n`.unwarn 1`\n┗ Снимет предупреждение с номером случая'
                                                    ' #1.', color=Color.embed_background()))
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
                    embed = Embed(title='', description=f'Предупреждение `#{case_id}` было снято.', color=0x5a357f)
                    await ctx.send(embed=embed)
                    break
            if found: break
        if not found: await ctx.send(f'Предупреждение с общим случаем `#{case_id}` не найдено.')

@bot.command(name='warns')
async def warns(ctx, user: User = None):
    if ctx.author.guild_permissions.administrator:
        data = load_warnings()
        if user is None:
            user_id = str(ctx.author.id)
            user_mention = ctx.author.name
        else:
            user_id = str(user.id)
            user_mention = user.name
        if user_id in data['user_warns']:
            user_warnings = data['user_warns'][user_id]
            embed = Embed(title=f'Предупреждения участника {user_mention}', color=0x5a357f)
            if user_warnings:
                for w in user_warnings:
                    warning_id = w['id']
                    reason = w['reason']
                    issued_at = datetime.fromisoformat(w['issued_at'])
                    expires = datetime.fromisoformat(w['expires']) if w['expires'] else None
                    issuer = w.get('issuer', 'Неизвестен')
                    expires_text = f'<t:{int(expires.timestamp())}:F> (<t:{int(expires.timestamp())}:R>)' if expires \
                        else 'Никогда'
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
            embed = Embed(title='', description=f'У {user_mention} нет предупреждений.', color=0x5a357f)
            await ctx.send(embed=embed)

""" Операторы калькулятора"""
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
""" Функции калькулятора """
FUNCTIONS = {
    'abs': abs,
    'max': max, 'min': min,
    'round': round,
    'pow': pow, '**': pow,
    'sqrt': math.sqrt, 'isqrt': math.isqrt,
    'log': math.log,
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'cot': lambda x: 1 / math.tan(math.radians(x)),
    '!': math.factorial,
    'exp': math.exp,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'deg': math.degrees, 'rad': math.radians,
    'ceil': math.ceil, 'floor': math.floor,
    'hypot': math.hypot,
    'pi': math.pi, 'e': math.e,
    'comb': math.comb, 'perm': math.perm,
    'trunc': math.trunc,
    'gcd': math.gcd,
    'len': len,
    'real': lambda z: z.real, 'imag': lambda z: z.imag,
    'mean': lambda data: sum(data) / len(data),
    'median': lambda data: sorted(data)[len(data) // 2]
}

""" Функция для замены операторов калькулятора"""
def safe_eval(expression):
    expression = expression.replace(" ", "")
    expression = re.sub(r"(?<!\w)\^(?!\w)", "**", expression)
    expression = re.sub(r"!(\d+)", r"math.factorial(\1)", expression)
    expression = re.sub(r"(\d+)!", r"math.factorial(\1)", expression)
    try:
        tree = ast.parse(expression, mode='eval')
        return _eval(tree.body)
    except Exception as e:
        raise ValueError(f"Ошибка при обработке выражения: {e}")
""" Функция для вычислений """
def _eval(node):
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        return OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS:
            args = [_eval(arg) for arg in node.args]
            return FUNCTIONS[node.func.id](*args)
        elif isinstance(node.func, ast.Attribute):
            obj = _eval(node.func.value)
            if isinstance(obj, type(math)) and hasattr(obj, node.func.attr):
                func = getattr(obj, node.func.attr)
                args = [_eval(arg) for arg in node.args]
                return func(*args)
        else:
            raise ValueError(f"Недопустимая функция: {node.func}")
    elif isinstance(node, ast.Attribute):
        value = _eval(node.value)
        if isinstance(value, type(math)) and hasattr(value, node.attr):
            return getattr(value, node.attr)
    elif isinstance(node, ast.Name):
        if node.id in FUNCTIONS:
            return FUNCTIONS[node.id]
        elif node.id == 'math':
            return math
        else:
            raise ValueError(f"Недопустимое имя: {node.id}")
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.List):
        return [_eval(elem) for elem in node.elts]
    elif isinstance(node, ast.Tuple):
        return tuple(_eval(elem) for elem in node.elts)
    else:
        raise ValueError(f"Недопустимая операция: {type(node)}")
""""""
""""""
class UpdateView(discord.ui.View):
    def __init__(self, updates, cur_page=0):
        super().__init__()
        self.updates = updates
        self.cur_page = cur_page
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        if len(self.updates) > 1:
            if self.cur_page > 0:
                self.add_item(discord.ui.Button(label="В начало", style=discord.ButtonStyle.primary, custom_id="start",
                                     emoji=discord.PartialEmoji(name="previous_pages", id=989035748424568832)))
                self.add_item(discord.ui.Button(label="Назад", style=discord.ButtonStyle.primary, custom_id="previous",
                                     emoji=discord.PartialEmoji(name="prev_page", id=684354640019587112)))
            if self.cur_page < len(self.updates) - 1:
                self.add_item(discord.ui.Button(label="Вперёд", style=discord.ButtonStyle.primary, custom_id="next",
                                     emoji=discord.PartialEmoji(name="next_page", id=684354639973318817)))
                self.add_item(discord.ui.Button(label="В конец", style=discord.ButtonStyle.primary, custom_id="end",
                                     emoji=discord.PartialEmoji(name="next_pages", id=989035746885246986)))

    async def on_button_click(self, interaction: discord.Interaction):
        if interaction.user.id != interaction.message.interaction.user.id:
            return await interaction.response.send_message("Это не ваша команда!", ephemeral=True)
        if interaction.custom_id == "start":
            self.cur_page = 0
        elif interaction.custom_id == "previous":
            self.cur_page = max(0, self.cur_page - 1)
        elif interaction.custom_id == "next":
            self.cur_page = min(len(self.updates) - 1, self.cur_page + 1)
        elif interaction.custom_id == "end":
            self.cur_page = len(self.updates) - 1
        self.update_buttons()
        embed = Embed(title="История обновлений", description=self.updates[self.cur_page],
                      color=Color.embed_background())
        await interaction.response.edit_message(embed=embed, view=self)


@bot.slash_command(name="update", description="Последнее обновление")
async def обновление(ctx):
    cur = (f"**07.12.2024** Обновлена команда `</clear:1317429027711221764>`.\n"
           f"Теперь сохраняет удалённые сообщения в лог-файл.")
    embed = Embed(title="", description=cur, color=Color.embed_background())
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
        "Использование: `/role {{command}}`\n\n"
        "**27.11.2024** Команда `giveaway` временно отключена.\n\n"
        "**05.12.2024** Команда `8ball` была удалена.\n\n"
        "**07.12.2024** Обновлена команда `clear`.\n"
        "Теперь сохраняет удалённые сообщения в лог-файл."
        "\n\n\n**В разработке**\nСистема управления модерацией"
    ]
    embed = Embed(title="История обновлений", description=updates[0].format(pref=pref), color=Color.embed_background())
    view = UpdateView(updates)
    await ctx.response.send_message(embed=embed, view=view, ephemeral=True)
""""""
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
async def set_system(ctx, channel: abc.GuildChannel):
    if isinstance(channel, (CategoryChannel, GroupChannel, VoiceChannel, StageChannel, DMChannel)):
        await ctx.respond("Сюда нельзя отправлять сообщения!", ephemeral=True)
        return
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if not channel.permissions_for(ctx.author).view_channel:
        await ctx.respond("У вас нет доступа к этому каналу.", ephemeral=True)
        return
    if not channel.permissions_for(ctx.guild.me).send_messages:
        await ctx.respond("У меня нет прав отправлять сообщения в этот канал.", ephemeral=True)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Эта команда только для администраторов.", ephemeral=True)
        return
    data_members = load_data()
    data_members[str(ctx.guild.id)] = channel.id
    save_data(data_members)
    await ctx.respond(f"Системный канал установлен: {channel.mention}")


@bot.event
async def on_member_join(member):
    data_members = load_data()
    channel_id = data_members.get(str(member.guild.id))
    if channel_id:
        member_channel = bot.get_channel(channel_id)
        if member_channel:
            embed = Embed(title="Пользователь присоединился к серверу", color=Color.green())
            embed.add_field(name="Тег", value=member.mention, inline=False)
            embed.add_field(name="Имя пользователя", value=member.name, inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            await member_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    data_members = load_data()
    channel_id = data_members.get(str(member.guild.id))
    if channel_id:
        channel: GuildChannel | Thread | PrivateChannel | None = bot.get_channel(channel_id)
        if channel:
            embed = Embed(title="Пользователь покинул сервер", color=Color.red())
            embed.add_field(name="Тег", value=member.mention, inline=False)
            embed.add_field(name="Имя пользователя", value=member.name, inline=False)
            embed.add_field(name="ID", value=member.id, inline=False)
            await channel.send(embed=embed)

@bot.event
async def on_interaction(inter):
    admin = await bot.fetch_channel(1315003234561036380)
    blocked_users = load_blocked_users()
    if inter.user.id in blocked_users:
        await inter.response.send_message("Вы находитесь в чёрном списке!", ephemeral=True)
    else:
        if inter.type == discord.InteractionType.application_command:
            command_name = inter.data.get('name')
            command_id = inter.data.get('id')
            await admin.send(embed=Embed(
                description=f"Команда {command_name} с ID: {command_id}, сервер: {inter.guild.name}, пользователь: "
                            f"{inter.user.mention} | `{inter.user.id}`", color=Color.embed_background()))
        await bot.process_application_commands(interaction=inter)
""" Роли """
@rcm.command(name="color", description="Изменить цвет роли")
async def role_color(ctx, role: discord.Option(discord.Role, description="Какой роли изменить цвет"),
                     color: discord.Option(input_type=discord.Color,
                                           description="Цветовой код (например #fe3a3 или 0xfe3a3)")):
    try:
        if ctx.author.guild_permissions.manage_roles:
            if ctx.guild is None:
                await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
                return
            if role:
                if ctx.author.top_role > role:
                    try:
                        embed = discord.Embed(title="Цвет роли изменен", color=0x7b68ee)
                        old_color = role.color
                        await role.edit(color=color)
                        embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                        embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=True)
                        embed.add_field(name="Прошлый цвет", value=str(old_color), inline=False)
                        embed.add_field(name="Новый цвет", value=str(color))
                        await ctx.response.send_message(f"Цвет роли «{role.name}» изменен на «{color}»", ephemeral=True)
                        await log.send_log(ctx.guild.id, embed=embed)
                    except discord.Forbidden:
                        await ctx.response.send_message("У меня нет прав на изменение цвета этой роли", ephemeral=True)
                    except discord.ext.commands.errors.BadColourArgument:
                        await ctx.respond("Неверный цвет. Пожалуйста, введите цвет в формате HEX "
                                          "(например, `#32a852` или `0x32a852`)", ephemeral=True)
                else:await ctx.respond("Вы не можете изменить цвет роли, которая выше Вашей.", ephemeral=True)
            else:await ctx.respond(f"Роль «{role.name}» не найдена", ephemeral=True)
        else:await ctx.respond(embed=Embed(description="У вас недостаточно прав!",color=0x7b68ee),ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: rcolor")
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)
@rcm.command(name="pre", description="Изменить приоритет роли")
async def _pre(ctx, role: discord.Option(discord.Role, description="Какую роль переместить"),
               pos: discord.Option(int, description="На какую позицию переместить роль")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.top_role >= role:
            if not role:
                await ctx.response.send_message('Роль не найдена', ephemeral=True)
                return
            try:
                embed = Embed(title="Приоритет роли изменён", color=0x7b68ee)
                embed.add_field(name="Автор", value=f"{ctx.author.mention} (`{ctx.author.name}`)", inline=True)
                embed.add_field(name="Роль", value=f"{role.mention} (`{role.name}`)", inline=False)
                embed.add_field(name="Старая позиция", value=role.position, inline=True)
                embed.add_field(name="Новая позиция", value="`pos`", inline=True)
                embed.set_footer(text=f"role id: {role.id}")
                if role.icon:
                    embed.set_thumbnail(url=role.icon.url)
                await log.send_log(ctx.guild.id, embed=embed)
                await role.edit(position=pos)
                await ctx.response.send_message(f'«{role.name}» перемещена на позицию `{pos}`.')
            except Forbidden:
                await ctx.respond('У меня нет прав для изменения приоритета для этой роли', ephemeral=True)
        else:
            await ctx.response.send_message("Вы не можете переместить роль, которая выше Вашей роли.", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)
        return
@rcm.command(name="add", description="Выдать роль пользователю")
async def _give_role(ctx, user: discord.Option(discord.Member, description="Кому выдать роль"),
                     role: discord.Option(Role, description="Какую роль выдать")):
    try:
        if ctx.guild is not None:
            if ctx.author.guild_permissions.manage_roles:
                if ctx.author.top_role >= role:
                    if role:
                        try:
                            emb = discord.Embed(title="Пользователю выдана роль", color=0x7b68ee)
                            emb.add_field(name="Автор",value=f"{ctx.author.mention} (`{ctx.author.name}`)",inline=False)
                            emb.add_field(name="Роль", value=f"{role.mention} (`{role.name}`)")
                            emb.add_field(name="Пользователь", value=f"{user.mention} (`{user.name}`)")
                            await user.add_roles(role)
                            await ctx.respond(f"Роль «{role.name}» выдана пользователю: {user.mention}", ephemeral=True)
                            await log.send_log(ctx.guild.id, embed=emb)
                        except discord.Forbidden:
                            await ctx.response.send_message("У меня нет прав для выдачи этой роли", ephemeral=True)
                    else: await ctx.response.send_message(f"Роль «{role.name}» не найдена.", ephemeral=True)
                else: await ctx.respond(f"Вы не можете выдать роль, которая выше вашей роли.", ephemeral=True)
            else: await ctx.respond("У вас недостаточно прав!", ephemeral=True)
        else: await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)
@rcm.command(name="remove", description="Удалить роль у пользователя")
async def _remove_role(ctx, user: discord.Option(discord.Member, description="У кого нужно забрать роль"),
                       role: discord.Option(discord.Role, description="Какую забрать роль")):
    try:
        if user == ctx.author:
            await ctx.respond("Вы не можете удалять свои роли!", ephemeral=True)
            return
        if not role:
            await ctx.respond("Роль не найдена", ephemeral=True)
            return
        if not user:
            await ctx.respond("Пользователь не найден", ephemeral=True)
        if ctx.guild is not None:
            if ctx.author.guild_permissions.manage_roles:
                if ctx.author.top_role > role:
                    try:
                        embed = Embed(title="У пользователя забрана роль", color=0x7b68ee)
                        embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
                        embed.add_field(name="Роль", value=f"{role.mention} (`{role.name}`)")
                        embed.add_field(name="Пользователь", value=f"{user.mention} (`{user.name}`)")
                        await user.remove_roles(role)
                        await ctx.respond(f"Роль «{role.name}» удалена у {user.mention}", ephemeral=True)
                        await log.send_log(ctx.guild.id, embed=embed)
                    except discord.Forbidden:
                        await ctx.respond("У меня нет прав для удаления этой роли", ephemeral=True)
                else:
                    await ctx.respond(f"У вас недостаточно прав!", ephemeral=True)
            else:
                await ctx.respond("У вас недостаточно прав!", ephemeral=True)
        else:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав!", ephemeral=True)
@rcm.command(name="up", description='Повысить роль пользователя на 1 уровень')
async def _uprole(ctx, member: Option(Member, "Кому повысить роль")):
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
                new_role = utils.get(guild.roles, position=highest_role.position + 1)
                await member.add_roles(new_role)
                await member.remove_roles(highest_role)
                await ctx.response.send_message(f'Пользователю {member.mention} ({member.id}) повышен ранг '
                                                f'до: {new_role.name} ({new_role.id})', ephemeral=True)
                embed = Embed(title="Пользователю повышен ранг", color=0x7b68ee)
                embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
                embed.add_field(name="Прошлая роль", value=f"{highest_role.mention} ({highest_role.name})", inline=True)
                embed.add_field(name="Новая роль", value=f"{new_role.mention} ({new_role.name})", inline=True)
                embed.add_field(name="Пользователь", value=f"{member.mention} ({member.name})")
                await log.send_log(ctx.guild.id, embed=embed)
            else:
                await ctx.response.send_message(f"Вы не можете повысить роль которая вышей вашей роли.", ephemeral=True)
        else:
            await ctx.respond("У вас недостаточно прав!", ephemeral=True)
    except PermissionError:
        await ctx.response.send_message("У меня недостаточно прав!", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: uprole")
@rcm.command(name="do", description="Понизить роль пользователя на 1 уровень")
async def _do(ctx, member: Option(Member, description="Кому понизить роль")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if member == ctx.author:
            await ctx.respond(embed=Embed(description="Вы не можете понижать свою роль!", color=0x7b68ee),ephemeral=True)
            return

        if ctx.author.top_role > member.top_role:
            highest_role = member.top_role
            roles = ctx.guild.roles
            new_role_position = highest_role.position - 1
            new_role = utils.get(roles, position=new_role_position)
            await member.add_roles(new_role)
            await member.remove_roles(highest_role)
            await ctx.respond(f'Пользователю {member.mention} понижен ранг до: {new_role.name}')
        else:
            await ctx.response.send_message(f"Вы не можете понизить роль которая выше вашей.", ephemeral=True)
    except PermissionError:
        await ctx.response.send_message("У меня недостаточно прав!", ephemeral=True)
@rcm.command(name="clear", description="Удалить все роли пользователя")
async def clear_roles(ctx, member: Option(Member, description="У кого очистить роли")):
    try:
        if not ctx.guild:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if member == ctx.author:
            await ctx.respond(embed=Embed(description="Вы не можете удалять свои роли!", color=0x7b68ee),
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
            embed.add_field(name="Пользователь", value=f"{member.mention} ({member.name})")
            await ctx.respond(f"Все роли пользователя {member.display_name} удалены", ephemeral=True)
            await log.send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond(f"Вы не можете очистить роли этого пользователя.", ephemeral=True)
    except PermissionError:
        await ctx.respond("У меня недостаточно прав для удаления ролей!", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
@rcm.command(name="create", description="Создать роль")
async def createrole(ctx, role: Option(str, description="Название роли"),
                     color: Option(input_type=Color, description="Цвет для роли", required=False)):
    if bot.user in [member for member in ctx.guild.members if member.bot]:
        if ctx.author.guild_permissions.manage_roles:
            guild = ctx.guild
            created_role = await guild.create_role(name=role, colour=color if color else Color.embed_background())
            await ctx.response.send_message(f'Роль «{role}» создана.')
            embed = Embed(title="Роль создана", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            embed.add_field(name="Роль", value=f"{created_role.mention} ({created_role.name})", inline=False)
            embed.set_footer(text=f"role id: {created_role.id}")
            await log.send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond(embed=Embed(title="", description="У вас нет прав!", color=0x7b68ee), ephemeral=True)
    else:
        await ctx.respond(embed=Embed(title="", description="Для использования этой команды добавьте меня на сервер!",
                                      color=Color.embed_background()))
def perm_ac(ctx: AutocompleteContext):
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
@rcm.command(name='delperm', description='Забрать право для роли')
async def delperm(ctx, role: Option(Role, description="У какой роли забрать разрешение"),
                  perm: Option(description="Разрешение для установки", autocomplete=perm_ac)):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.administrator:
            return
        if ctx.author.top_role > role:
            perms = role.permissions
            perms.update(**{perm: False})
            await role.edit(permissions=perms)
            await ctx.response.send_message(f"Разрешение {perm} забрано для роли {role.name}")
            embed = Embed(title="Разрешение у роли забрано", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
            embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=True)
            embed.add_field(name="Разрешение", value=perm, inline=False)
            await log.send_log(ctx.guild.id, embed=embed)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: setperm")
@rcm.command(name='setperm', description='Установить право для роли')
async def setperm(ctx, role: Option(Role, description="Какой роли выдать разрешение"),
                  perm: Option(str, description="Разрешение для установки", autocomplete=perm_ac)):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.administrator:
            return
        if ctx.author.top_role > role:
            perms = role.permissions
            perms.update(**{perm: True})
            await role.edit(permissions=perms)
            await ctx.response.send_message(f"Разрешение {perm} забрано у роли {role.name}")
            embed = Embed(title="Разрешение у роли забрано", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
            embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=True)
            embed.add_field(name="Разрешение", value=perm, inline=False)
            await log.send_log(ctx.guild.id, embed=embed)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: setperm")
@rcm.command(name="replace", description='Заменить роль у пользователя')
async def replace(ctx, member: Option(Member, "У кого заменить роль"),
                  prev_role: Option(Role, "Предыдущая роль пользователя"),
                  new_role: Option(Role, "Новая роль пользователя")):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.top_role > new_role:
            if prev_role not in member.roles:
                await ctx.respond(f"{member.mention} не имеет роли {prev_role.name}")
                return
            if member == ctx.author:
                await ctx.response.send_message("Вы не можете заменять свои же роли!", ephemeral=True)
                return
            await member.remove_roles(prev_role)
            await member.add_roles(new_role)
            await ctx.respond(f"Роль пользователя {member.mention} заменена с «{prev_role.mention}» на новую роль "
                              f"«{new_role.mention}»")
            embed = Embed(title="Роль пользователя заменена")
            embed.add_field(name="Автор", value=f"{ctx.author.mention} ({ctx.author.name})", inline=True)
            embed.add_field(name="Пользователь", value=f"{member.mention} ({member.name})", inline=False)
            embed.add_field(name="Предыдущая роль", value=f"{prev_role.mention} ({prev_role.name})", inline=True)
            embed.add_field(name="Новая роль", value=f"{new_role.mention} ({new_role.name})", inline=True)
            await log.send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond(f"Вы не можете заменить роль, которая выше вашей.", ephemeral=True)
    except Exception as e:
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: "
              f"{ctx.author.mention} | `{ctx.author.id}`\nКоманда: replace")
@rcm.command(name="list", description="Список ролей сервера")
async def role_list(ctx):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.guild_permissions.manage_roles:
            discord_roles = ctx.guild.roles
            discord_role_list = Embed(title="Список ролей сервера", color=Color.blue())
            max_roles_per_page = 15
            start_index = 0
            end_index = min(start_index + max_roles_per_page, len(discord_roles))
            for index, role in enumerate(discord_roles[start_index:end_index], start=0):
                if role.name != "@everyone":
                    discord_role_list.add_field(name=f"", value=f"{role.mention} `{role.id}` - `id:` {index}",
                                                inline=False)
                    discord_role_list.set_footer(text=f"Кол-во ролей: {len(ctx.guild.roles) - 1}")
            role_list_view = RoleView(ctx,discord_roles, start_index, end_index, len(discord_roles), max_roles_per_page)
            await log.send_log(ctx.guild.id, embed=Embed(description=f"{ctx.author.mention} вызвал список ролей через "
                                                                     f"</role list:{bgac('role').id}>",
                                                         color=0x7b68ee))
            await ctx.response.send_message(embed=discord_role_list, view=role_list_view)
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
        role_list = Embed(title="Список ролей сервера", color=Color.blue())
        for index, role in enumerate(reversed(self.roles[self.start_index:self.end_index]), start=self.start_index + 1):
            if role.name != "@everyone":
                role_list.add_field(name="", value=f"{role.mention} `{role.id}` - index: {index}", inline=False)
                role_list.set_footer(text=f"Кол-во ролей: {len(ctx.guild.roles)}")
        await ctx.response.edit_message(embed=role_list, view=self)
@rcm.command(name="delete", description="Удалить роль")
async def delrole(ctx, *, role: Option(Role, description="Какую роль удалить")):
    if ctx.guild is None:
        await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
        return
    if ctx.author.guild_permissions.manage_roles:
        if ctx.author.top_role > role:
            if role:
                embed = Embed(title="Роль удалена", color=0x7b68ee)
                embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                embed.add_field(name="Роль", value=f"{role.mention} ({role.name})")
                embed.set_footer(text=f"user id: {ctx.author.id}")
                await log.send_log(ctx.guild.id, embed=embed)
                await ctx.response.send_message(f"Роль «{role.name}» удалена", ephemeral=True)
                await role.delete()
            else:
                await ctx.response.send_message(f'Роль «{role.name}» не найдена', ephemeral=True)
        else:
            await ctx.response.send_message("У вас недостаточно прав!", ephemreal=True)
    else:
        await ctx.response.send_message(f"У вас нет прав на использование этой команды!", ephemeral=True)
class HelpRolesView(discord.ui.View):
    def __init__(self, embeds, page=0):
        super().__init__()
        self.embeds = embeds
        self.page = page

    async def update_message(self, interaction: discord.Interaction):
        embed = self.embeds[self.page]
        self.update_buttons()
        await interaction.response.edit_message(embed=embed, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.page == 0
        self.children[1].disabled = self.page == len(self.embeds) - 1

    @discord.ui.button(label="Назад", style=discord.ButtonStyle.primary)
    async def back_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page > 0:
            self.page -= 1
            await self.update_message(interaction)

    @discord.ui.button(label="Вперед", style=discord.ButtonStyle.primary)
    async def forward_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.page < len(self.embeds) - 1:
            self.page += 1
            await self.update_message(interaction)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
@rcm.command(name="perms", description="Информация о разрешениях ролей")
async def role_perms(ctx: discord.Interaction):
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
    help_roles_view = HelpRolesView(embeds)
    await ctx.response.send_message(embed=embeds[0], view=help_roles_view)
@rcm.command(name="pin", description="Переключить видимость роли в списке участников.")
async def pin_role(ctx, role: Role):
    try:
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if ctx.author.guild_permissions.manage_roles:
            if ctx.author.top_role > role:
                if role not in ctx.guild.roles:
                    await ctx.response.send_message("Роль не найдена.", ephemeral=True)
                    return
                hoist_status = role.hoist
                await role.edit(hoist=not hoist_status)
                embed = Embed(title="Параметры роли изменены",color=0x7b68ee,
                              description="`Показывать участников с ролью отдельно от остальных участников в сети`")
                embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
                if hoist_status:
                    embed.add_field(name="Новое состояние", value="Выключено")
                    await ctx.respond(f"Роль **{role.name}** больше не будет отображаться отдельно.", ephemeral=True)
                else:
                    embed.add_field(name="Новое состояние", value="Включено")
                    await ctx.respond(f"Роль **{role.name}** теперь будет отображаться отдельно.", ephemeral=True)
                embed.set_footer(text=f"channel: {ctx.channel.mention}")
                await log.send_log(ctx.guild.id, embed=embed)
            else:
                await ctx.response.send_message("У вас недостаточно прав!", ephemeral=True)
        else:
            await ctx.response.send_message("У вас недостаточно прав!", ephemeral=True)
    except Forbidden:
        await ctx.respond("Недостаточно прав для изменения параметров этой роли.", ephemeral=True)
@rcm.command(name="mention", description="Переключить упоминание (тег) роли.")
async def mentions_cmd(ctx, role: Role, enable: Option(bool, choices=[True, False])):
    if role not in ctx.guild.roles:
        await ctx.response.send_message("Эта роль не существует на этом сервере.", ephemeral=True)
        return
    if ctx.author.guild_permissions.manage_roles and ctx.author.top_role >= role:
        enable_bool = enable is True
        await role.edit(mentionable=enable_bool)
        if ctx.author.top_role <= role:
            await ctx.respond(embed=Embed(description="Вы не можете настраивать свою наивысшую роль!"), ephemeral=True)
            return
        if enable_bool:
            param = "Включено"
            await ctx.response.send_message(f"Роль {role.name} теперь может быть упомянута.", ephemeral=True)
        else:
            param = "Выключено"
            await ctx.response.send_message(f"Роль {role.name} больше не может быть упомянута.", ephemeral=True)
        embed = Embed(title="Параметры роли изменены", color=0x7b68ee)
        embed.add_field(name="Автор", value=ctx.author.mention, inline=True)
        embed.add_field(name="Роль", value=f"{role.mention} ({role.name})", inline=False)
        embed.add_field(name="Параметр", value=f"`Позволить всем @упоминать эту роль.`, теперь {param}`")
        await log.send_log(ctx.guild.id, embed=embed)
    else:
        await ctx.respond(embed=Embed(description="У вас нет прав для использования этой команды!",
                                      color=Color.embed_background()), ephemeral=True)
""" Калькулятор """
@bot.slash_command(name="calculate", description="Вычисляет математическое выражение")
async def _calculate(ctx, expression=None):
    try:
        if expression is None:
            embed = Embed(title="Доступные математические функции",
                          description="Вот список доступных функций и примеры их использования.", color=0x5a357f)
            embed.add_field(name="Основные арифметические", value=(
                "`abs(x)` - модуль числа, пример: `abs(-5) → 5`\n"
                "`max(a, b, ...)` - максимум, пример: `max(3, 7, 1) → 7`\n"
                "`min(a, b, ...)` - минимум, пример: `min(3, 7, 1) → 1`\n"
                "`round(x, n)` - округление до `n` знаков, пример: `round(3.14159, 2) → 3.14`\n"
                "`pow(a, b)` или `a**b` - возведение в степень, пример: `pow(2, 3) → 8`\n"
                "`sqrt(x)` - квадратный корень, пример: `sqrt(16) → 4`\n"
                "`len(a)` - длина строки, пример: `len(\"Hello\") → 5`"), inline=False)
            embed.add_field(name="Логарифмы и экспоненты", value=(
                "`log(x, base)` - логарифм числа `x` по основанию `base`, пример: `log(8, 2) → 3`\n"
                "`exp(x)` - e^x, пример: `exp(1) → 2.71828`"), inline=False)
            embed.add_field(name="Тригонометрия", value=(
                "`sin(x)` - синус угла в радианах, пример: `sin(pi/2) → 1`\n"
                "`cos(x)` - косинус угла, пример: `cos(0) → 1`\n"
                "`tan(x)` - тангенс угла, пример: `tan(pi/4) → 1`\n"
                "`cot(x)` - котангенс угла в градусах, пример: `cot(45) → 1`"), inline=False)
            embed.add_field(name="Углы", value=("`deg(x)` - перевод из радиан в градусы, пример: `deg(pi) → 180`\n"
                                                "`rad(x)` - перевод из градусов в радианы, пример: `rad(180) → 3.14`"),
                            inline=False)
            embed.add_field(name="Округление", value=("`ceil(x)` - округление вверх, пример: `ceil(2.3) → 3`\n"
                                                      "`floor(x)` - округление вниз, пример: `floor(2.7) → 2`\n"
                                                      "`trunc(x)` - усечение дробной части, пример: `trunc(2.7) → 2`"),
                            inline=False)
            embed.add_field(name="Специальные значения", value=("`pi` - число π, пример: `pi → 3.14159`\n"
                                                                "`e` - число e, пример: `e → 2.71828`"), inline=False)
            embed.add_field(name="Факторизация и комбинаторика",
                            value=("`!n` - факториал числа, пример: `!5 → 120`\n"
                                   "`comb(n, k)` - сочетания, пример: `comb(5, 2) → 10`\n"
                                   "`perm(n, k)` - перестановки, пример: `perm(5, 2) → 20`"), inline=False)
            embed.add_field(name="Геометрия", value=("`hypot(a, b)` - гипотенуза, пример: `hypot(3, 4) → 5`\n"
                                                     "`gcd(a, b)` - НОД, пример: `gcd(12, 15) → 3`"), inline=False)
            embed.add_field(name="Комплексные числа",
                            value=("`real(z)` - действительная часть, пример: `real(3+4j) → 3`\n"
                                   "`imag(z)` - мнимая часть, пример: `imag(3+4j) → 4`"), inline=False)
            embed.add_field(name="Статистика",
                            value=("`mean(data)` - среднее значение, пример: `mean([1, 2, 3]) -> 2`\n"
                                   "`median(data)` - медиана, пример: `median([1, 3, 2]) → 2`"),
                            inline=False)
            embed.set_footer(text="Используйте функции с правильным синтаксисом и аргументами для успешных расчетов!")
            await ctx.respond(embed=embed, ephemeral=True)
            return
        if len(expression) > 100:
            await ctx.respond("Выражение слишком длинное.", ephemeral=True)
            return
        if expression is not None:
            expression = expression.replace("^", "**")
            result = safe_eval(expression)
            if isinstance(result, (int, float)):
                max_value = 10 ** 35
                if abs(result) > max_value:
                    await ctx.respond("Результат слишком велик. Попробуйте другое выражение.", ephemeral=True)
                    return
            embed = Embed(description=f"Результат выражения `{expression}`", color=0x5a357f)
            embed.add_field(name="Ответ", value=f"`{result}`")
            await ctx.respond(embed=embed)
            return
    except SyntaxError:
        await ctx.respond("Ошибка синтаксиса в выражении. Проверьте ввод!", ephemeral=True)
    except ValueError:
        await ctx.respond(f"Ошибка при обработке выражения. Проверьте синтаксис и попробуйте ещё раз.",ephemeral=True)
    except Exception as e:
        print(f"Ошибка: {e}")
        await ctx.respond("Произошла ошибка при выполнении вычислений.", ephemeral=True)

BLOCKED_USERS = "json/blocked_users.json"

if not os.path.exists(BLOCKED_USERS):
    with open(BLOCKED_USERS, "w") as file:
        json.dump([], file)


def load_blocked_users():
    with open(BLOCKED_USERS, "r") as file:
        return json.load(file)


def save_blocked_users(data):
    with open(BLOCKED_USERS, "w") as file:
        json.dump(data, file, indent=4)
""" Блок-лист """
@bot.command(name="block")
async def block(ctx, action: str, user: User = None):
    """
    Управление блок-листом.
    Пример: r!block add @пользователь или r!block remove @пользователь
    """
    if ctx.author.id != 743864658951274528:
        return
    blocked_users = load_blocked_users()

    if action.lower() == "add":
        if not user:
            await ctx.reply(embed=Embed(title="", description="Укажите пользователя", color=0x5a357f))
        if user.id not in blocked_users:
            blocked_users.append(user.id)
            save_blocked_users(blocked_users)
            await ctx.reply(embed=Embed(title="", description=f"Пользователь {user} добавлен в блок-лист.",
                                       color=Color.embed_background()))
        else:
            await ctx.reply(embed=Embed(title="", description=f"Пользователь {user} уже находится в блок-листе.",
                                       color=Color.embed_background()))
    elif action.lower() in ["remove","del","delete","rem"]:
        if user.id in blocked_users:
            blocked_users.remove(user.id)
            save_blocked_users(blocked_users)
            await ctx.reply(embed=Embed(title="", description=f"Пользователь {user} удалён из блок-листа.",
                                       color=Color.embed_background()))
        else:
            await ctx.reply(embed=Embed(title="", description=f"Пользователя {user} нет в блок-листе.",
                                       color=Color.embed_background()))
    elif action.lower() in ["list", "l"]:
        embed = Embed(title="ЧС бота", color=Color.embed_background())
        for user in blocked_users:
            embed.add_field(name="", value=f"<@{user}> (`{user}`)", inline=False)
        await ctx.reply(embed=embed)

    else:
        return
""" Принудительная остановка бота """
@bot.slash_command(name="stop")
@commands.is_owner()
async def _stop(ctx):
    await ctx.response.send_message("+", ephemeral=True)
    await bot.close()

""" Изменение ника пользователя """
@bot.slash_command(name="nick", description="Изменить ник пользователю")
async def _nick(ctx, user: Option(Member, "Кому изменить ник"),
                nick: Option(str, "Новый ник пользователя")):
    try:
        if not ctx.channel.permissions_for(ctx.guild.me).manage_nicknames:
            await ctx.respond("У меня нет прав на управление никнеймами.", ephemeral=True)
            return
        if ctx.guild is None:
            await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
            return
        if not ctx.author.guild_permissions.manage_nicknames:
            await ctx.respond("У вас недостаточно прав!", ephemeral=True)
            return
        if ctx.author.top_role > user.top_role:
            embed = Embed(title="Пользователю изменён ник", color=0x7b68ee)
            embed.add_field(name="Автор", value=ctx.author.mention, inline=False)
            embed.add_field(name="Пользователь", value=f"{user.mention} ({user.name})")
            embed.add_field(name="Прошлый ник", value=user.nick, inline=True)
            embed.add_field(name="Новый ник", value=nick)
            await user.edit(nick=nick)
            await ctx.response.send_message(f"Пользователю {user.name} изменён ник на: {nick}", ephemeral=True)
            await log.send_log(ctx.guild.id, embed=embed)
    except PermissionError:
        await ctx.response.send_message("У меня нет прав на изменение ника этого пользователя", ephemeral=True)
        return
""" Пинг бота """
@bot.slash_command(name='ping')
@commands.is_owner()
async def ping(ctx):
    bot_ping = bot.latency
    await ctx.response.send_message(f"The bot ping is: {round(bot_ping * 1000)}ms!")

with open('json/config.json', 'r') as f:
    data_as = json.load(f)
@bot.slash_command(name="mserver", description="Получить информацию о сервере")
async def _mserver(ctx: discord.Interaction, ip_address: Option(str, "IP адрес сервера")):
    await ctx.defer(ephemeral=True)
    url = f"https://api.mcsrvstat.us/2/{ip_address}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
    try:
        if data.get('online'):
            players_online = data.get('players', {}).get('online', 'Не известно')
            server_name = data.get("hostname", "Не известно")
            server_version = data.get('version', "Не известно")
            software_n = data.get('software', "Не известно")
            info_n = ' '.join(data.get('motd', {}).get('clean', ["Не известно"]))
            embed = Embed(title=f"Информация о сервере {ip_address}", color=Color.embed_background())
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
@bot.event
async def on_ready():
    try:
        await bot.sync_commands()
        on_ready_channel = bot.get_channel(1317407756881235988)
        extensions = []
        api_status = requests.get("https://discordstatus.com/api").status_code
        for extension in bot.extensions:
            if extension.startswith("commands."):
                extensions.append(extension.replace("commands.", ""))
        await on_ready_channel.send(embed=Embed(
            title="Бот запущен", color=0x7b68ee,
            description=f"Время запуска: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
                        f"Мой айди: {bot.user.id}\n"
                        f"Подключён к серверам: {len(bot.guilds)}\n\n"
                        f"--- Модули ---\n\n"
                        f"Загружено расширений: {len(bot.extensions)}\n"
                        f"Расширения: {', '.join(extensions)}\n\n"
                        f"--- Команды ---\n\n"
                        f"Загружено команд: {len(bot.commands) + len(bot.application_commands)}\n"
                        f"Команды: {len(bot.commands)}\n"
                        f"[{', '.join(command.name for command in bot.commands)}]\n"
                        f"Слеш команды: {len(bot.application_commands)}\n"
                        f"[{', '.join(app_command.callback.__name__ for app_command in bot.application_commands if hasattr(app_command, 'callback'))}]\n\n"
                        f"--- Версии ---\n\n"
                        f"Версия Py-cord.py: {discord.__version__}\n"
                        f"Версия Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n\n"
                        f"--- API ---\n\n"
                        f"Статус API: {api_status}\n"))
        print(f"Бот {bot.user.name} запущен")
        await update_old_messages()
        if not send_statistics.is_running():
            send_statistics.start()
        # bot.add_view(HelpView())
        await bot.change_presence(activity=discord.Game(name="/help"))
    except NotFound:
        print(" Сообщение не найдено")

bot.run(data_as["token"])
#for guild in bot.guilds:
        #    try:
        #        await bot.sync_commands()
        #        logging.info(f"Команды синхронизированы для серверов: {guild.name} (ID: {guild.id})")
        #    except Exception as e:
        #        logging.error(f"Ошибка синхронизации команд на серверах: {guild.name} (ID: {guild.id}): {e}")
        # commands_ = [send_stat, _calculate,clear_messages,_kick,_nick,
        #              ping,roles,_stop,guilds,anime,_avatar,set_system,
        #              plot,role_perms,_delchat,_delvoice,_staff_m,get_id,bug_report,bot_idea,log,_ban,_faq,inform,
        #              _mserver, обновление,история, _help]
        # await bot.register_commands(commands=commands_)