import datetime
from datetime import (timedelta, date, datetime, timezone, time)
import discord
import logging

from discord.abc import GuildChannel, PrivateChannel
from discord.utils import get
from discord.ui import (View, Select, Button, Item, Modal, view)
from discord.ext import tasks, commands
from discord import (ui, SelectMenu, SelectOption, Interaction, Option, Color, Embed, ButtonStyle, InputTextStyle, Cog,
                     PartialEmoji, InputText, Colour, Emoji, Role, ApplicationContext, ApplicationCommand, ShardInfo,
                     SKUType,
                     AutocompleteContext, Forbidden, Button, Member, User, TextChannel, File, NotFound, HTTPException,
                     Sequence,
                     Game, Guild, guild, default_permissions, VideoQualityMode, Sequence, PrivilegedIntentsRequired,
                     SKUFlags,
                     WelcomeScreen,
                     Thread,
                     RawThreadUpdateEvent, RawThreadMembersUpdateEvent, RawThreadDeleteEvent, RawIntegrationDeleteEvent,
                     RawBulkMessageDeleteEvent, RawMessageDeleteEvent, RawReactionActionEvent,
                     PollAnswer, PollAnswerCount, ActionRow, RawReactionClearEmojiEvent, RawReactionClearEvent,
                     Iterable,
                     RawMemberRemoveEvent, RawScheduledEventSubscription, RawVoiceChannelStatusUpdateEvent, UserCommand,
                     RawAuditLogEntryEvent, AutoModKeywordPresetType, EntitlementOwnerType,
                     AuthorizingIntegrationOwners,
                     VoiceChannel, VoiceClient, VoiceState, VoiceRegion, PermissionOverwrite, EmbedMedia, Poll,
                     Enum, EmbedField, EmbedAuthor, EmbedFooter, EmbedProvider, Entitlement, EntitlementType,
                     ExtensionError,
                     ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, ExtensionAlreadyLoaded, ExpireBehavior,
                     TypeVar,
                     ExpireBehaviour, MessageType, EmbeddedActivity, Message, ActivityType, TYPE_CHECKING, ChannelType,
                     Asset,ForumChannel,DMChannel,StageChannel, CategoryChannel, GroupChannel, ChannelFlags,
                     SystemChannelFlags,
                     ScheduledEvent, ScheduledEventLocation, ScheduledEventStatus, ShardInfo, SKUType,
                     ScheduledEventLocationType, ScheduledEventPrivacyLevel, AutoModEventType,
                     AutoModActionExecutionEvent,
                     DiscordException, ClientException, Client, ClientUser, HTTPClient, UserFlags, PublicUserFlags,
                     UserCommand,ValidationError,NoEntryPointError,DiscordServerError,ApplicationCommandError,
                     InteractionType,ApplicationCommandInvokeError,Intents,MessageCommand,PartialMessage,
                     PartialMessageable,MessageCall,AppInfo,Team,
                     AuditLogEntry, AuditLogChanges, AuditLogActionCategory, Attachment, AttachmentFlags, RoleFlags,
                     Any, Activity, Asset, ApplicationFlags, ApplicationCommandMixin, ApplicationRoleConnectionMetadata,
                     AuditLogDiff, AuditLogAction, AutoModAction, AutoModActionType, AutoModTriggerType, ForumTag,
                     Object,
                     CogMixin, CogMeta, ComponentType, InteractionContextType, ContextMenuCommand, Component, Coroutine,
                     Invite,CheckFailure, CustomActivity, ConnectionClosed, ContentFilter, SlashCommand,
                     SlashCommandGroup, PCMAudio,GuildSticker, Sticker, StickerType, StickerFormatType,
                     SlashCommandOptionType, OptionChoice, PromptType,Route,
                     ReactionType, IntegrationType, InteractionResponseType, ApplicationRoleConnectionMetadataType,
                     Reaction, ReactionCountDetails, RoleTags, ThreadOption, InteractionResponse, MessageFlags,
                     DeletedReferencedMessage, InteractionResponded, InteractionMetadata, AutoModTriggerMetadata,Bot,
                     PollMedia,
                     InvalidData, InvalidArgument, ThreadMember, FFmpegAudio, FFmpegPCMAudio, FFmpegOpusAudio,
                     AudioSource,
                     AutoShardedBot, AutoShardedClient, AutoModActionMetadata, StandardSticker, PartialInviteGuild,
                     Spotify,
                     BaseActivity, StagePrivacyLevel, MaybeUnlock, Status, PollResults, LoginFailure,
                     PCMVolumeTransformer,
                     IntegrationAccount, Integration, BotIntegration, IntegrationApplication, StreamIntegration,
                     Streaming,
                     MemberFlags, MemberCacheFlags, TeamMember, TeamMembershipState, SpeakingState, Permissions,
                     StickerItem,
                     Onboarding, OnboardingMode, StickerPack, VersionInfo, API_VERSION, MessageReference,
                     InteractionMessage,
                     MessageInteraction, NoMoreItems, InviteTarget, PartialInviteChannel, VoiceProtocol, StageInstance,
                     Template, PromptOption, OnboardingPrompt, PartialAppInfo, NotificationLevel, VerificationLevel,
                     MISSING,
                     utils, asset, abc, audit_logs, application_command, application_role_connection, activity,
                     annotations, appinfo, automod, __author__, command, slash_command, user_command, message_command,
                     message,team, channel, flags, state, shard, integrations, warn_deprecated, threads, reaction,
                     raw_models, interactions, gateway, template, onboarding, partial_emoji, stage_instance,
                     context_managers,player, backoff, iterators, oggparse, monetization, __path__, __main__)
import discord.ext.commands.errors as error
from discord.commands import permissions
import asyncio, ast, aiohttp
from asyncio import sleep
import hashlib
from pypresence import Presence
import math
import io
import numpy as np
import matplotlib.pyplot as plt
import json
import sqlite3
import os, operator
import textwrap, time
import subprocess
from statistics import mean, median
import requests, random, re
from art import tprint
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix="r!", intents=discord.Intents.all())
roles = discord.SlashCommandGroup("role", "description")
bot.remove_command("help")
bgac = bot.get_application_command
log = bot.get_cog("SendLog")
with open('json/config.json', 'r') as f:
    data_as = json.load(f)
os.system('color a')
os.system('title Discord Bot')
print("\n")
tprint("remod3")


@bot.slash_command(name="system")
@commands.is_owner()
async def _system(ctx, command: str):
    os.system(f"{command}")
    await ctx.response.send_message("+")

@bot.slash_command(name="guilds", guild_ids=[1214617864863219732, 1148996038363975800])
@commands.is_owner()
async def guilds(ctx: Interaction):
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
            SelectOption(
                label=f"{anime['russian'][:97]}..." if len(anime['russian']) > 100 else anime['russian'],
                value=str(anime['id'])) for anime in anime_results[:25]]
        super().__init__(placeholder="Выберите аниме", options=options, min_values=1, max_values=1)

    async def callback(self, ctx: Interaction):
        anime_id = self.values[0]
        anime_details = self.get_anime_details(anime_id)
        if anime_details and isinstance(anime_details, dict):
            image_url = "https://shikimori.one" + anime_details['image']['original']
            description = anime_details.get('description', 'Описание недоступно')
            cleaned_description = clean_description(description) if description else 'Описание недоступно'
            embed = Embed(title=f"{anime_details.get('russian', 'Без названия')} "
                                f"({anime_details.get('name', 'Без ориг. названия')})",
                          description=cleaned_description, color=Color.embed_background())
            embed.add_field(name="Год выхода", value=anime_details.get('aired_on', 'Неизвестно'))
            embed.add_field(name="Статус", value=anime_details.get('status', 'Неизвестно'))
            embed.add_field(name="Количество эпизодов", value=anime_details.get('episodes', 'Неизвестно'))
            embed.set_thumbnail(url=image_url)
            view = ui.View()
            await ctx.response.edit_message(content="Информация о выбранном аниме:", embed=embed, view=view)
        else:
            await ctx.respond(f"Не удалось получить информацию о выбранном аниме. ({anime_id})", ephemeral=True)

    @staticmethod
    async def on_error(error: Exception, ctx: Interaction) -> None:
        await ctx.response.send_message(f"Произошла ошибка! Свяжитесь с разработчиком: `remodik`")
        print(error)

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

class AnimeSelectView(View):
    def __init__(self, anime_results):
        super().__init__(timeout=None)
        self.add_item(AnimeSelect(anime_results))


@bot.slash_command(name="anime", description="Поиск информации об аниме")
async def anime(ctx, name: Option(str, description="Название аниме")):
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
        print(f"Произошла ошибка:\n{e}\nСервер: {ctx.guild.name}\nПользователь: {ctx.author.mention} | "
              f"`{ctx.author.id}`\nКоманда: anime")


@bot.slash_command(name="avatar", description="Получить аватар пользователя или сервера")
async def _avatar(ctx: ApplicationContext,
                  user: Option(Member, description="Выберите пользователя", required=False),
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


@bot.slash_command(name="delchat", description="Удалить текстовый канал")
async def _delchat(ctx, name: Option(TextChannel, "Какой чат удалить")):
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
            await log.send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond("У вас нет прав на использование этой команды!", ephemeral=True)
    except Forbidden:
        await ctx.response.send_message(f"Недостаточно прав для удаления канала «{name.name}».", ephemeral=True)
    except NotFound:
        await ctx.response.send_message(f"Чат с именем «{name.name}» не найден.", ephemeral=True)


@bot.slash_command(name="delvoice", description="Удалить голосовой канал")
async def _delvoice(ctx, name: Option(VoiceChannel, "Какой чат удалить")):
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
            await log.send_log(ctx.guild.id, embed=embed)
        else:
            await ctx.respond("У вас нет прав на использование этой команды!", ephemeral=True)
    except Forbidden:
        await ctx.response.send_message(f"Недостаточно прав для удаления этого канала.", ephemeral=True)
    except NotFound:
        await ctx.response.send_message(f"Канал «{name.name}» не найден.", ephemeral=True)


@bot.slash_command(name="embed", description="Создать Embed сообщение")
async def _staff_m(ctx, channel: Option(TextChannel | DMChannel | VoiceChannel,
                                        description="Куда отправить", required=False),
                   message: Option(str, "Дополнительное сообщение (перед Embed)", required=False),
                   title: Option(str, description="Название заголовка", required=False),
                   description: Option(str, description="Описание Embed", required=False),
                   field_name: Option(str, description="Заголовок поля", required=False),
                   field_desc: Option(str, description="Описание поля", required=False),
                   thumbnail: Option(str, description="Ссылка на фото", required=False),
                   image: Option(str, description="Ссылка на фото", required=False),
                   footer: Option(str, description="Доп. инфа в самом низу", required=False)):
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
        await ctx.respond("У вас недостаточно прав!", ephemeral=True)
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
        if not text: return text
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
                        if dt_method:
                            value = dt_method(*eval(format_str)) if format_str else dt_method()
                        else:
                            value = f"Ошибка: неизвестный метод '{obj_type}.{method}'"
                elif obj_type == "date":
                    if method == "today":
                        format_str = format_str if format_str else "%d.%m.%Y"
                        value = date.today().strftime(format_str)
                    else:
                        date_method = getattr(date, method, None)
                        if date_method:
                            value = date_method(*eval(format_str)) if format_str else date_method()
                        else:
                            value = f"Ошибка: неизвестный метод '{obj_type}.{method}'"
                elif obj_type == "time":
                    if method == "now":
                        format_str = format_str if format_str else "%H:%M:%S"
                        value = datetime.now().strftime(format_str).split()[1]
                    else:
                        time_method = getattr(time, method, None)
                        if time_method:
                            value = time_method(*eval(format_str)) if format_str else time_method()
                        else:
                            value = f"Ошибка: неизвестный метод '{obj_type}.{method}'"
                else:
                    value = f"Ошибка: неизвестный объект '{obj_type}'"
                return str(value)
            except Exception as e:
                print(f"Ошибка: {e}")

        return re.sub(pattern, replace_placeholder, text)

    message = process_placeholders(message)
    title = process_placeholders(title)
    description = process_placeholders(description)
    field_name = process_placeholders(field_name)
    field_desc = process_placeholders(field_desc)
    footer = process_placeholders(footer)
    embed = Embed(title=title if title else "", description=description if description else "",
                  color=Color.embed_background())
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
    else:
        pass
    if channel is None:
        if message:
            await ctx.respond(content=message, embed=embed)
        else:
            await ctx.respond(embed=embed)
    else:
        if isinstance(channel, abc.Messageable):
            await channel.send(content=message, embed=embed)
    if ctx.guild is not None:
        await log.send_log(ctx.guild.id, message=f"{ctx.author.mention} отправил Embed!")
        if message:
            await log.send_log(ctx.guild.id, message=message)
        elif embed:
            await log.send_log(ctx.guild.id, embed=embed)
        elif message and embed:
            await log.send_log(ctx.guild.id, message=message, embed=embed)
    await ctx.respond("Успешно!", ephemeral=True)

@bot.event
async def on_connect():
    try:
        print("ok")
    except ConnectionAbortedError:
        print("[WinError 1236] Подключение к сети было разорвано локальной системой")


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


# class GiveawayView(View):
#     def __init__(self, seconds, prize, description, winners_count, participants_limit):
#         super().__init__(timeout=seconds)
#         self.prize = prize
#         self.description = description
#         self.winners_count = int(winners_count)
#         self.participants_limit = int(participants_limit)
#         self.participants = []
#
#     @ui.button(label="Записаться", style=ButtonStyle.green)
#     async def join_button(self, button: ui.Button, interaction: Interaction):
#         if len(self.participants) < self.participants_limit:
#             if interaction.user not in self.participants:
#                 self.participants.append(interaction.user)
#                 await interaction.response.send_message(f"Теперь вы участвуете в розыгрыше!", ephemeral=True)
#                 self.update_embed(interaction)
#             else:
#                 await interaction.response.send_message("Вы уже участвуете в этом розыгрыше.", ephemeral=True)
#         else:
#             await interaction.response.send_message("Лимит участников уже достигнут.", ephemeral=True)
#
#     @ui.button(label="Отказаться", style=ButtonStyle.red)
#     async def leave_button(self, button: ui.Button, interaction: Interaction):
#         if interaction.user in self.participants:
#             self.participants.remove(interaction.user)
#             await interaction.response.send_message(f"Вы успешно отказались от участия в розыгрыше.", ephemeral=True)
#             self.update_embed(interaction)
#         else:
#             await interaction.response.send_message("Вы не участвуете в этом розыгрыше.", ephemeral=True)
#
#     def update_embed(self, interaction):
#         embed = Embed(title='🎉 Розыгрыш!', description=self.description or "", color=0x42f57b)
#         embed.add_field(name="Приз", value=self.prize)
#         embed.add_field(name="", value=f"Участников: {str(len(self.participants))}", inline=False)
#         embed.add_field(name="Максимальное кол-во участников", value=str(self.participants_limit))
#         embed.set_author(name=interaction.author.name, url=interaction.author.avatar.url)
#         asyncio.create_task(interaction.message.edit(embed=embed, view=self))
#
#     async def on_timeout(self):
#         embed = Embed(title='🎉 Розыгрыш завершен! 🎉', description="Время вышло, вот и результаты!",
#                       color=0x42f57b)
#         if len(self.participants) >= self.winners_count:
#             winners = random.sample(self.participants, self.winners_count)
#             winners_mentions = ', '.join([winner.mention for winner in winners])
#             embed.add_field(name="🏆 Победители", value=winners_mentions, inline=False)
#             embed.add_field(name="🎁 Приз", value=self.prize, inline=False)
#             embed.add_field(name="📜 Описание", value=self.description or "Описание отсутствует", inline=False)
#             embed.add_field(name="👥 Количество участников", value=str(len(self.participants)), inline=False)
#             embed.set_footer(text="Спасибо всем за участие!")
#             await self.message.channel.send(embed=embed)
#         else:
#             embed.description += "\nК сожалению, в розыгрыше не было достаточно участников."
#             await self.message.channel.send(embed=embed)


# @bot.slash_command(name="giveaway", description="Создать розыгрыш")
# async def giveaway(ctx, seconds, prize: Option(str, description="Приз который получит победитель"),
#                    winners_count: Option(int, description="Макс кол-во победителей"),
#                    participants_limit: Option(int, description="Макс кол-во участников"),
#                    description: Option(str, description="Описание розыгрыша", default=False)):
#     try:
#         if ctx.guild is None:
#             await ctx.respond("Для использования этой команды добавьте меня на сервер!", ephemeral=True)
#             return
#         if not ctx.author.guild_permissions.administrator:
#             return
#         seconds = giveaway_parse_time(seconds)
#         formatted_time = giveaway_format_time(seconds)
#         embed = Embed(title="🎉 Розыгрыш!", description=description or "Описание отсутствует", color=0x42f57b)
#         embed.add_field(name="Приз", value=prize, inline=False)
#         embed.add_field(name="Продолжительность", value=formatted_time, inline=False)
#         embed.add_field(name="Кол-во победителей", value=str(winners_count), inline=False)
#         embed.add_field(name="Максимальное кол-во участников", value=str(participants_limit), inline=False)
#         view = GiveawayView(seconds, prize, description, winners_count, participants_limit)
#         giveaway_message = await ctx.response.send_message(embed=embed, view=view)
#         view.message = giveaway_message
#     except Exception as e:
#         print(f"Произошла ошибка:\n{e}")
#

ban_data_file = "json/ban_data.json"


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
    if isinstance(target, Member):
        return target
    try:
        user_id = int(target)
        member = await ctx.guild.fetch_member(user_id)
        return member
    except (ValueError, NotFound):
        pass
    if ctx.message.reference:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        return message.author
    await ctx.reply(embed=Embed(
        title="", description="Пользователь не найден. Используйте упоминание, ID или ответ на сообщение."))
    return None


def parse_time(time_str: str) -> timedelta | None:
    time_str = time_str.lower()
    time_re = re.compile(r'(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?')
    match = time_re.match(time_str)
    if not match:
        return None
    days = int(match.group(1)) if match.group(1) else 0
    hours = int(match.group(2)) if match.group(2) else 0
    minutes = int(match.group(3)) if match.group(3) else 0
    return timedelta(days=days, hours=hours, minutes=minutes)


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
    member = utils.get(ctx.guild.members, name=arg)
    if member:
        return member
    # Поиск по полному имени (никнейму)
    member = utils.get(ctx.guild.members, nick=arg)
    return member


@bot.command(name="mute")
async def mute(ctx, target: str, duration: str, *, reason: str = None):
    if ctx.author.guild_permissions.moderate_members:
        member = await get_user(ctx, target)
        if not member:
            await ctx.reply(Embed(title="", description="Пользователь не найден."))
            return
        mute_role = utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted", permissions=Permissions(send_messages=False,
                                                                                          add_reactions=False))
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False, add_reactions=False)
        time_delta = parse_time(duration)
        if not time_delta:
            await ctx.reply("Неверный формат времени. Используйте, например, 1d, 1h, 1m, 1h30m и т.д.")
            return
        embed = Embed(title="", description=f":white_check_mark: Участник {member.mention} замьючен! 🙊")
        if duration: embed.add_field(name="Срок", value=f"{duration}")
        if reason: embed.add_field(name="Причина", value=reason, inline=False)
        await member.add_roles(mute_role)
        await member.timeout_for(time_delta)
        await ctx.reply(embed=embed)
        await asyncio.sleep(time_delta.total_seconds())
        await member.remove_roles(mute_role)


@bot.command(name="unmute")
async def unmute(ctx, target):
    if ctx.author.guild_permissions.moderate_members:
        member = await get_user(ctx, target)
        if target is None:
            pref = get_prefix(bot, ctx.message)
            await ctx.reply(embed=Embed(title="", description=f"Использование команды: {pref}unmute ID|mention"))
        if not member:
            await ctx.reply(embed=Embed(title="", description="Пользователь не найден."))
            return
        mute_role = utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await member.timeout_for(0)
        await ctx.reply(embed=Embed(title="",description=f":white_check_mark: Участник {member.name} размьючен! 😊"))


@bot.command(name="mutes")
async def mutes(ctx):
    if ctx.author.guild_permissions.moderate_members:
        mute_role = utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            await ctx.reply(Embed(title="", description="Роль мута не найдена"))
            return
        muted_members = [member.mention for member in ctx.guild.members
                         if
                         mute_role in member.roles or (hasattr(member, 'timed_out_until') and member.timed_out_until)]
        mutes_em = Embed(title="", description=f"Замученные пользователи: {', '.join(muted_members)}")
        if muted_members:
            await ctx.reply(embed=mutes_em)
        else:
            await ctx.reply(embed=Embed(title="", description="Нет замученных пользователей."))


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
        ban = Embed(title="",
                    description=f"{member.mention} был забанен {'на ' + str(days) + ' дней' if days > 0 else ''}.")
        await ctx.reply(embed=ban)


@bot.slash_command(name="ban", description="Забанить пользователя")
async def _ban(ctx, member: Option(Member, "Кого забанить"),
               reason: Option(str, "Причина бана", required=False)):
    if ctx.author.guild_permissions.ban_members or ctx.author.id == ctx.guild.owner_id:
        if member.guild_permissions <= ctx.author.guild_permissions:
            embed = Embed(title="Пользователь забанен", color=0x7b68ee)
            embed.add_field(name="Автор", value=f"{ctx.author.mention} ({ctx.author.name})", inline=True)
            embed.add_field(name="Пользователь", value=f"{member.mention} ({member.name})", inline=True)
            if reason:
                embed.add_field(name="Причина", value=reason, inline=False)
            await log.send_log(ctx.guild.id, embed=embed)
            emb = Embed(description=f"Пользователь {member.mention} был забанен!", color=Color.red())
            emb.add_field(name="Модератор", value=ctx.author.mention, inline=True)
            if reason:
                emb.add_field(name="Причина", value=reason, inline=False)
            await member.ban(reason=reason if reason else None)


@bot.command(name="unban")
async def unban(ctx, target: User):
    if ctx.author.guild_permissions.ban_members:
        await ctx.guild.unban(target)
        if str(target.id) in ban_data:
            del ban_data[str(target.id)]
            save_ban_data(ban_data)
        await ctx.reply(embed=Embed(title="", description=f"{target.mention} был разбанен."))


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


@bot.slash_command(name="inform", description="Информация о боте (сокращенно)")
async def inform(ctx):
    embed = Embed(
        title="Информация о боте",
        description="remod3Bot - это многофункциональный бот, предназначенный для крупных серверов "
                    "и более удобного управления ролями и сервером. Написав разработчику, вы можете заказать "
                    "команду/функционал для своего сервера",
        color=Color.embed_background())
    embed.add_field(name="Информация о боте",value=f"Версия: 1.0\n"
                                                   f"Дата создания: <t:1697887295:D> (<t:1697887295:R>)",inline=False)
    embed.add_field(name='Разработчики',value='1. `remodik` (`743864658951274528`)')
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/yzJCZz-vGE8Gmd1x-AqmGaDRA"
                            "-TOvD5ObRi__IMen2Y/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/120"
                            "6275841395392552/a_1b9fe156b57bf2f57b054a27c0fe4f73.gif?width=575&heig"
                            "ht=575")
    embed.set_author(name="remod3Bot", icon_url="https://images-ext-1.discordapp.net/external/yzJCZz-vGE8Gmd1x-AqmGaDRA"
                                                "-TOvD5ObRi__IMen2Y/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/120"
                                                "6275841395392552/a_1b9fe156b57bf2f57b054a27c0fe4f73.gif?width=575&heig"
                                                "ht=575")

    btn1 = ui.Button(style=ButtonStyle.grey,label="Информация о создателе",url='https://solo.to/remod3')
    btn2 = ui.Button(style=ButtonStyle.green,label="Поддержать автора",url="https://www.donationalerts.com/r/remod3")
    view = View()
    view.add_item(btn1)
    view.add_item(btn2)
    await ctx.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    try:
        cc = bot.get_channel(1317407756881235988)
        await bot.sync_commands()
        #for guild in bot.guilds:
        #    try:
        #        await bot.sync_commands()
        #        logging.info(f"Команды синхронизированы для серверов: {guild.name} (ID: {guild.id})")
        #    except Exception as e:
        #        logging.error(f"Ошибка синхронизации команд на серверах: {guild.name} (ID: {guild.id}): {e}")
        # commands_ = [send_stat, _staff_ds, _calculate,clear_messages,_kick,_nick,
        #              ping,roles,_stop,guilds,anime,_avatar,set_system,
        #              plot,role_perms,_delchat,_delvoice,_staff_m,get_id,bug_report,bot_idea,log,_ban,_faq,inform,
        #              _mserver, обновление,история, _help]
        # await bot.register_commands(commands=commands_)
        print(f'Logged in as {bot.user}')
        commands_1 = await bot.http.get_guild_commands(bot.user.id, next(guild.id for guild in bot.guilds))
        for comma in commands_1:
            print(f"Команда: {comma['name']}, ID: {comma['id']}")
        er = (", ".join(app_command.callback.__name__
                        for app_command in bot.application_commands if hasattr(app_command, 'callback')))
        await cc.send(embed=Embed(title="", description=f"{er if er else '-'}", color=Color.embed_background()))
        # bot.add_view(HelpView())
        await bot.change_presence(activity=discord.Game(name="/help"))
    except NotFound:
        print("Сообщение не найдено")


bot.add_application_command(roles)
bot.run(data_as['token'])
# match input("Connect RPC? >> "):
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
#
#
#    case 'n' | 'N' | '-' | 'нет' | 'Нет' | 'no' | 'No':
# bot.run("MTIwNjI3NTg0MTM5NTM5MjU1Mg.GHQNw8.OXoM0SCc-U0ZbMg1pOfDqDIxEhjYV15olb9D0Y")
#        bot.run(data_as['token'])
