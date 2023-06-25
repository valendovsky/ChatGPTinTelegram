#!/usr/bin/env python3

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update, TelegramObject

from config import ADMIN_ID, get_access_status, get_subscribers, get_subscribers_status


class AccessMiddleware(BaseMiddleware):
    """
    Класс для ограничения доступа к боту.
    """
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update,
                       data: Dict[str, Any]
                       ) -> Any:
        # Проверяем права пользователя на доступ к боту
        if event.from_user.id == ADMIN_ID \
                or get_access_status() \
                or ((event.from_user.id in get_subscribers()) and get_subscribers_status()):
            return await handler(event, data)

        return


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
