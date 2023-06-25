#!/usr/bin/env python3

"""
Инлайн-клавиатура для операции создания рассылки.
"""

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup

from constants import ADD_BUTTON_TEXT, ADD_BUTTON_CALLBACK, NO_BUTTON_TEXT, NO_BUTTON_CALLBACK,\
    CONFIRM_TEXT, CONFIRM_CALLBACK, CANCEL_TEXT, CANCEL_CALLBACK


def get_confirm_button_keyboard():
    """
    Клавиатура создания рекламной инлайн-кнопки.
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=ADD_BUTTON_TEXT, callback_data=ADD_BUTTON_CALLBACK)
    keyboard_builder.button(text=NO_BUTTON_TEXT, callback_data=NO_BUTTON_CALLBACK)
    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def get_confirm_sender_keyboard():
    """
    Клавиатура для подтверждения и отмены рассылки.
    """
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text=CONFIRM_TEXT, callback_data=CONFIRM_CALLBACK)
    keyboard_builder.button(text=CANCEL_TEXT, callback_data=CANCEL_CALLBACK)
    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup()


def get_campaign_keyboard(text_button: str, url_button: str):
    """
    Формирует клавиатуру для рекламного сообщения.
    """
    campaign_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=text_button,
                url=url_button
            )
        ]
    ])

    return campaign_keyboard


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
