#!/usr/bin/env python3

"""
Команды для меню бота.
"""

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

import constants
from config import ADMIN_ID


async def set_admin_commands(bot: Bot):
    """
    Формирует меню команд для админов.
    """
    admin_commands = [
        BotCommand(
            command='start',
            description=constants.START_DESCRIPTION
        ),
        BotCommand(
            command=constants.USER_CONTEXT,
            description=constants.USER_CONTEXT_DESCRIPTION
        ),
        BotCommand(
            command=constants.ALL_CONTEXT,
            description=constants.ALL_CONTEXT_DESCRIPTION
        ),
        BotCommand(
            command=constants.CHECK_ACCESS,
            description=constants.CHECK_ACCESS_DESCRIPTION
        ),
        BotCommand(
            command=constants.ACCESS,
            description=constants.ACCESS_DESCRIPTION
        ),
        BotCommand(
            command=constants.SUBSCRIBERS,
            description=constants.SUBSCRIBERS_DESCRIPTION
        ),
        BotCommand(
            command=constants.SENDER,
            description=constants.SENDER_DESCRIPTION
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
            description=constants.START_DESCRIPTION
        ),
        BotCommand(
            command=constants.USER_CONTEXT,
            description=constants.USER_CONTEXT_DESCRIPTION
        )
    ]
    await bot.set_my_commands(user_commands, BotCommandScopeAllPrivateChats())


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
