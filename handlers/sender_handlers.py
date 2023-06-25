#!/usr/bin/env python3

"""
Хендлеры для создания рассылки.
"""

import asyncio
import logging

from aiogram import Bot, Router, html, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramRetryAfter

from constants import SENDER, ADD_BUTTON_CALLBACK, NO_BUTTON_CALLBACK, CONFIRM_CALLBACK, CANCEL_CALLBACK, CANCEL
from config import SUBSCRIBERS, ADMIN_ID, get_subscribers
from utils.sender_state import Steps
from keyboards.sender_keyboard import get_confirm_button_keyboard, get_confirm_sender_keyboard, get_campaign_keyboard


router = Router()
# Включаем фильтрацию выполнения только для админа
router.message.filter(F.from_user.id == ADMIN_ID)


@router.message(Command(SENDER))
async def get_sender(message: Message, command: CommandObject, state: FSMContext):
    """
    Хендлер создания рассылки по подписчикам.
    """
    # Если подписчиков нет
    if not SUBSCRIBERS:
        await message.answer('Нет подписчиков для рассылки рекламных сообщений')
        return

    # Проверка наличия имени рассылки
    if not command.args:
        await message.answer('Для создания рассылки введите команду /sender и имя рассылки')
        return

    # Сохранение в машину состояний названия кампании
    await state.update_data(name_camp=command.args)
    # Переходим в состояние создания рекламного сообщения
    await state.set_state(Steps.get_message)

    await message.answer(f'Создание рассылки: {html.bold(command.args)}.\r\n\r\n'
                         'Отправьте рекламное сообщение.\r\n'
                         f'Чтобы выйти наберите /{CANCEL}')


@router.message(Command(CANCEL))
async def cancel_sender(message: Message, state: FSMContext):
    """
    Прерывает процесс создания рассылки.
    """
    # Очистка машины состояний
    await state.clear()

    await message.answer('Отмена кампании рассылки.')


@router.message(Steps.get_message)
async def get_message(message: Message, state: FSMContext):
    """
    Получает рекламное сообщение.
    """
    # Сохраняем в машину состояний идентификаторы рекламного сообщения
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    # Переходим в состояние запроса инлайн-кнопки
    await state.set_state(Steps.get_button)

    await message.answer('Сообщение для рассылки создано.\r\n'
                         'Добавить кнопку к сообщению?',
                         reply_markup=get_confirm_button_keyboard())


@router.callback_query(Steps.get_button)
async def get_button(call: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Обрабатывает выбор создания кнопки для рекламного сообщения.
    """
    if call.data == ADD_BUTTON_CALLBACK:
        # Создание инлайн-кнопки для сообщения
        await state.set_state(Steps.get_text_button)
        await call.message.answer('Отправьте текст для кнопки.', reply_markup=None)
    elif call.data == NO_BUTTON_CALLBACK:
        # Продолжить без создания инлайн-кнопки
        await call.message.edit_reply_markup(reply_markup=None)

        # Получаем элементы рекламного сообщения из машины состояний
        data = await state.get_data()
        message_id = int(data.get('message_id'))
        chat_id = int(data.get('chat_id'))

        # Переходим в состояние одобрения рекламного объявления
        await state.set_state(Steps.get_url_button)

        # Отправляем рекламное сообщение без кнопки (reply_markup=None) на подтверждение
        await confirm(call.message, bot, message_id, chat_id)

    # Отвечаем на callbackquery событие
    await call.answer()


@router.message(Steps.get_text_button)
async def get_text_button(message: Message, state: FSMContext):
    """
    Сохраняет текст кнопки для рекламного сообщения.
    """
    # Сохраняем данные и переходим в следующее состояние
    await state.update_data(text_button=message.text)
    await state.set_state(Steps.get_url_button)

    await message.answer('Теперь отправьте ссылку для кнопки.')


@router.message(Steps.get_url_button, F.text)
async def get_url_button(message: Message, bot: Bot, state: FSMContext):
    """
    Сохраняет ссылку для кнопки рекламного сообщения.
    Завершает процесс формирования рекламного объявления.
    """
    await state.update_data(url_button=message.text)

    # Формируем клавиатуру для рекламного объявления
    campaign_keyboard = get_campaign_keyboard((await state.get_data()).get('text_button'), message.text)

    # Получаем рекламное сообщение
    data = await state.get_data()
    message_id = int(data.get('message_id'))
    chat_id = int(data.get('chat_id'))

    # Отправляем рекламное сообщение на подтверждение
    await confirm(message, bot, message_id, chat_id, campaign_keyboard)


async def confirm(message: Message,
                  bot: Bot,
                  message_id: int,
                  chat_id: int,
                  reply_markup: InlineKeyboardMarkup = None):
    """
    Отправляет рекламный пост пользователю на подтверждение.
    Клавиатуры может не быть (None).
    """
    # Копируем в чат рекламное сообщение с инлайн-клавиатурой и запрашиваем подтверждение
    await bot.copy_message(chat_id, chat_id, message_id, reply_markup=reply_markup)

    await message.answer('Это сообщение для рассылки.',
                         reply_markup=get_confirm_sender_keyboard())


@router.callback_query(Steps.get_url_button, F.data.in_([CONFIRM_CALLBACK, CANCEL_CALLBACK]))
async def sender_decide(call: CallbackQuery, bot: Bot, state: FSMContext):
    """
    Хендлер обработки отмены или подтверждения рассылки.
    """
    if call.data == CONFIRM_CALLBACK:
        await call.message.edit_text('Начинаем рассылку сообщений.', reply_markup=None)

        # Получение данных рекламного объявления
        data = await state.get_data()
        message_id = data.get('message_id')
        chat_id = data.get('chat_id')
        text_button = data.get('text_button')
        url_button = data.get('url_button')
        name_camp = data.get('name_camp')

        count = await broadcaster(bot, name_camp, chat_id, message_id, text_button, url_button)

        await call.message.answer(f'Рекламное сообщение успешно разослано [{count}] пользователям.')
    elif call.data == CANCEL_CALLBACK:
        await call.message.edit_text('Рассылка отменена.', reply_markup=None)

    # Очистка машины состояний
    await state.clear()


async def send_message(bot: Bot,
                       name_camp: str,
                       user_id: int,
                       from_chat_id: int,
                       message_id: int,
                       keyboard: InlineKeyboardMarkup = None):
    """
    Отправляет сообщения, обрабатывая исключения.
    """
    try:
        await bot.copy_message(user_id, from_chat_id, message_id, reply_markup=keyboard)
    except TelegramRetryAfter as ex:
        # Ограничение по лимитам
        await asyncio.sleep(ex.retry_after)
        # Рекурсивно повторяем рассылку
        return await send_message(bot, user_id, from_chat_id, message_id, keyboard)
    except Exception as ex:
        # Прочие исключения
        logging.warning(f'Exception: {name_camp} - {user_id} - {ex}')
    else:
        return True

    return False


async def broadcaster(bot: Bot,
                      name_camp: str,
                      from_chat_id: int,
                      message_id: int,
                      text_button: str = None,
                      url_button: str = None):
    """
    Рассылает рекламные сообщения подписчикам.
    """
    # Создаём клавиатуру, если существует
    if text_button and url_button:
        keyboard = get_campaign_keyboard(text_button, url_button)
    else:
        keyboard = None

    # Получаем список подписчиков
    subscribers = get_subscribers()

    # Рассылаем сообщения
    count = 0
    for subscriber in subscribers:
        if await send_message(bot, name_camp, int(subscriber), from_chat_id, message_id, keyboard):
            count += 1
            # Задержка для лимитов
            await asyncio.sleep(.05)

    return count


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
