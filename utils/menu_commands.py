#!/usr/bin/env python3

# Команды для меню

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

from constants import ACCESS, SUBSCRIBERS, CHECK_ACCESS, USER_CONTEXT, ALL_CONTEXT
from config import ADMIN_ID


async def set_admin_commands(bot: Bot):
    """
    Формирует меню команд для админов.
    """
    admin_commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command=USER_CONTEXT,
            description='Сбросить контекст'
        ),
        BotCommand(
            command=ALL_CONTEXT,
            description='Сбросить контекст для всех пользователей'
        ),
        BotCommand(
            command=ACCESS,
            description='Изменить общие права доступа'
        ),
        BotCommand(
            command=SUBSCRIBERS,
            description='Изменить права доступа для подписчиков'
        ),
        BotCommand(
            command=CHECK_ACCESS,
            description='Проверить права доступа'
        )
    ]
    await bot.set_my_commands(admin_commands, BotCommandScopeChat(chat_id=ADMIN_ID))


async def set_members_commands(bot: Bot):
    """
    Формирует меню для обычных пользователей.
    """
    user_commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command=USER_CONTEXT,
            description='Сбросить контекст'
        )
    ]
    await bot.set_my_commands(user_commands, BotCommandScopeAllPrivateChats())
