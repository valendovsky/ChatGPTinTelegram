#!/usr/bin/env python3

"""
Основные общие хендлеры бота.
"""

from aiogram import Bot, Router, html
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import ADMIN_ID
from keyboards.menu_commands import set_admin_commands, set_members_commands


router = Router()


@router.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    """
    Команда запуска бота /start, создание меню бота.
    """
    if message.chat.id == ADMIN_ID:
        # Формируем меню для админов
        await set_admin_commands(bot)
    else:
        # Формируем меню для пользователей
        await set_members_commands(bot)

    await message.answer(f'Привет, {html.quote(message.from_user.first_name)}!\r\n'
                         'Задай мне вопрос, и я попрошу ChatGPT ответить на него.')


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
