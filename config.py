#!/usr/bin/env python3

"""
Файл настроек.
"""

import os

from dotenv import load_dotenv


load_dotenv()

TG_API_KEY = os.getenv('TG_API_KEY')
ADMIN_ID: int = int(os.getenv('ADMIN_ID'))
ACCESS_STATUS = False
SUBSCRIBERS_STATUS = True
SUBSCRIBERS_LIST = (os.getenv('SUBSCRIBERS_LIST').split(','))
SUBSCRIBERS = [int(subscriber) for subscriber in SUBSCRIBERS_LIST if SUBSCRIBERS_LIST != ['']] or []
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = 'gpt-3.5-turbo'
MAX_TOTAL_TOKENS = 4096


def change_access_status():
    """
    Изменяет права доступа к боту.
    """
    global ACCESS_STATUS
    ACCESS_STATUS = not ACCESS_STATUS


def get_access_status():
    """
    Возвращает значение переменной ACCESS_STATUS.
    False - доступ только администратора, True - доступ открыт для всех.
    """
    return ACCESS_STATUS


def change_subscribers_status():
    """
    Изменяет права доступа всех подписчиков к боту.
    """
    global SUBSCRIBERS_STATUS
    SUBSCRIBERS_STATUS = not SUBSCRIBERS_STATUS


def get_subscribers_status():
    """
    Возвращает значение переменной SUBSCRIBERS_STATUS.
    False - доступ подписчикам закрыт, True - доступ подписчикам открыт.
    """
    return SUBSCRIBERS_STATUS


def get_subscribers():
    """
    Возвращает список подписчиков.
    """
    return SUBSCRIBERS


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
