#!/usr/bin/env python3

# Основные хендлеры бота

from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from config import ADMIN_ID, change_access_status, get_access_status, change_subscribers_status, get_subscribers_status
from constants import ACCESS, SUBSCRIBERS, CHECK_ACCESS
from utils.menu_commands import set_admin_commands, set_members_commands


router = Router()


@router.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    """
    Команда запуска бота /start, создание меню бота.
    """
    if message.chat.id == int(ADMIN_ID):
        # Формируем меню для админов
        await set_admin_commands(bot)
    else:
        # Формируем меню для пользователей
        await set_members_commands(bot)

    await message.answer(f'Привет, {message.from_user.first_name}!\r\n'
                         'Задай мне вопрос, и я попрошу ChatGPT ответить на него.')


@router.message(Command(ACCESS), (F.from_user.id == int(ADMIN_ID)))
async def change_access(message: Message):
    """
    Команда изменения общих прав доступа к боту /all_access, только для админа.
    """
    change_access_status()
    if get_access_status():
        msg = 'открыт общий доступ'
    else:
        msg = 'общий доступ закрыт'
    await message.answer(f'Права общего доступа к боту изменены, <b>{msg}</b>.')


@router.message(Command(SUBSCRIBERS), (F.from_user.id == int(ADMIN_ID)))
async def change_subscribers_access(message: Message):
    """
    Команда изменения прав доступа к боту подписчиков /subscribers, только для админа.
    """
    change_subscribers_status()
    if get_subscribers_status():
        msg = 'доступен'
    else:
        msg = 'НЕ доступен'
    await message.answer(f'Права доступа подписчиков к боту изменены, теперь бот <b>{msg}</b> подписчикам.')


@router.message(Command(CHECK_ACCESS), (F.from_user.id == int(ADMIN_ID)))
async def check_access(message: Message):
    """
    Команда проверки прав доступа к боту /check_access, только для админа.
    """
    if get_access_status():
        msg = 'Бот доступен всем пользователям.'
    else:
        if get_subscribers_status():
            msg = 'Бот доступен только подписчикам.'
        else:
            msg = 'Бот доступен только администратору.'
    await message.answer(msg)


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
