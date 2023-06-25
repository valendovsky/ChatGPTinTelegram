#!/usr/bin/env python3

"""
Хендлеры для команд администраторов.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from config import ADMIN_ID, change_access_status, get_access_status, change_subscribers_status, get_subscribers_status
from constants import ACCESS, SUBSCRIBERS, CHECK_ACCESS


router = Router()
# Включаем фильтрацию выполнения только для админа
router.message.filter(F.from_user.id == ADMIN_ID)


@router.message(Command(ACCESS))
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


@router.message(Command(SUBSCRIBERS))
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


@router.message(Command(CHECK_ACCESS))
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
