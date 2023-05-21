#!/usr/bin/env python3

# Хендлеры для работы с ChatGPT

import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from utils.chatgpt_req import get_chatgpt_response
from middlewares.chat_action_middleware import ChatActionMiddleware
from constants import USER_CONTEXT, ALL_CONTEXT, TOO_LARGE_CONTEXT


# Контекст всех пользователей
USERS_MESSAGES = {}

router = Router()
# Подключаем мидлвари для оповещения о длительной операции
router.message.middleware(ChatActionMiddleware())


def update_context(user_id, role, content):
    """
    Добавляет сообщение к контексту пользователя.
    """
    if user_id in USERS_MESSAGES:
        USERS_MESSAGES[user_id].append({'role': role, 'content': content})
    else:
        USERS_MESSAGES[user_id] = [{'role': role, 'content': content}]


def reset_context(user_id):
    """
    Сбрасывает контекст конкретного пользователя.
    """
    USERS_MESSAGES.pop(user_id, 'clear')  # на случай, если контекст отсутствует


@router.message(Command(USER_CONTEXT))
async def reset_user_context(message: Message):
    """
    Хендлер сброса контекста конкретного пользователя.
    """
    reset_context(message.from_user.id)
    await message.answer(text='Контекст очищен.')


@router.message(Command(ALL_CONTEXT))
async def reset_all_context(message: Message):
    """
    Очищает весь контекст всех пользователей.
    """
    USERS_MESSAGES.clear()
    await message.answer(text='Контекст всех чатов удалён.')


@router.message(F.text, flags={'long_operation': 'typing'})
async def get_chatgpt(message: Message):
    """
    Пересылает сообщение пользователя ChatGPT и возвращает пользователю его ответ.
    """
    # Минимальная задержка для срабатывания 'typing'
    await asyncio.sleep(0.3)

    user_id = message.from_user.id

    # Обновляем контекст пользователя
    update_context(user_id, 'user', message.text)

    # Получаем ответ ChatGPT
    message_for_user = await get_chatgpt_response(message_for_openai=USERS_MESSAGES[user_id])

    # Если контекст превысил допустимый размер, очищаем его
    if message_for_user == TOO_LARGE_CONTEXT:
        reset_context(user_id)

    # Отправляем ответ ChatGPT пользователю
    await message.answer(text=message_for_user)


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
