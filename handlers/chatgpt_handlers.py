#!/usr/bin/env python3

"""
Хендлеры для работы с ChatGPT.
"""

import asyncio
import os

from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command

from utils.chatgpt_req import get_chatgpt_response, transcript_voice
from middlewares.chat_action_middleware import ChatActionMiddleware
from constants import USER_CONTEXT, ALL_CONTEXT, TOO_LARGE_CONTEXT
from utils.audio_converter import ogg_to_mp3


# Контексты всех пользователей
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


async def get_message_for_user(user_id, message_for_openai):
    """
    Пересылает сообщение пользователя ChatGPT и возвращает пользователю его ответ.
    """
    # Обновляем контекст пользователя
    update_context(user_id, 'user', message_for_openai)

    # Получаем ответ ChatGPT
    message_for_user = await get_chatgpt_response(message_for_openai=USERS_MESSAGES[user_id])

    # Если контекст превысил допустимый размер, очищаем его
    if message_for_user == TOO_LARGE_CONTEXT:
        reset_context(user_id)

    return message_for_user


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
async def get_text_chatgpt(message: Message):
    """
    Даёт ответ ChatGPT на текстовый запрос пользователя.
    """
    # Минимальная задержка для срабатывания 'typing'
    await asyncio.sleep(0.3)

    # Делаем запрос к ChatGPT
    message_for_user = await get_message_for_user(message.from_user.id, message.text)

    # Отправляем ответ ChatGPT пользователю
    await message.answer(text=message_for_user)


@router.message(F.voice, flags={'long_operation': 'typing'})
async def get_voice_chatgpt(message: Message, bot: Bot):
    """
    Даёт ответ ChatGPT на голосовой запрос пользователя.
    """
    # Минимальная задержка для срабатывания 'typing'
    await asyncio.sleep(0.3)

    # Голосовые файлы пользователя
    ogg_file_path = f'./tmp/{message.voice.file_id}.ogg'
    mp3_file_path = f'./tmp/mp3_{message.voice.file_id}.mp3'

    # Скачиваем голосовое пользователя
    await bot.download(message.voice, destination=ogg_file_path)
    # Конвертируем ogg файл в mp3 формат
    await ogg_to_mp3(ogg_file_path, mp3_file_path)
    # Транскрибируем голосовое сообщение в текст
    text = await transcript_voice(mp3_file_path)

    if not text:
        message_from_openai = 'Очень неразборчиво, пожалуйста, повторите вопрос.'
    else:
        # Делаем запрос к ChatGPT
        message_from_openai = await get_message_for_user(message.from_user.id, text)

    # Формируем ответ пользователю
    message_for_user = f'Ваш вопрос: {text}\r\n' + message_from_openai

    # Отправляем ответ ChatGPT пользователю
    await message.answer(text=message_for_user)

    # Удаление голосовых файлов
    os.remove(ogg_file_path)
    os.remove(mp3_file_path)


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
