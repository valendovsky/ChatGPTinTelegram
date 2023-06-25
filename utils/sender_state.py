#!/usr/bin/env python3

"""
Состояния при создании кампании рассылки.
"""

from aiogram.fsm.state import State, StatesGroup


class Steps(StatesGroup):
    get_message = State()
    get_button = State()
    get_text_button = State()
    get_url_button = State()
