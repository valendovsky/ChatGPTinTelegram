#!/usr/bin/env python3

# Асинхронный Телеграмм-бот на основе aiogram с интегрированным ChatGPT

import asyncio
import logging
import contextlib

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode

from config import TG_API_KEY, ADMIN_ID
from middlewares.access_middleware import AccessMiddleware
from handlers import main_handlers, chatgpt_handlers


async def start_bot(bot: Bot):
    """
    Сообщает админу о запуске бота.
    """
    await bot.send_message(ADMIN_ID, text='Бот запущен!')


async def stop_bot(bot: Bot):
    """
    Сообщает админу об остановке бота.
    """
    await bot.send_message(ADMIN_ID, text='Бот остановлен!')


async def main():
    """
    Запускает Телеграмм бот.
    """
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )

    bot = Bot(token=TG_API_KEY, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Сообщения о запуске и остановке бота администратору
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Регистрация мидлвари ограничения доступа пользователей к боту
    dp.message.middleware.register(AccessMiddleware())

    # Регистрация роутеров
    dp.include_routers(main_handlers.router, chatgpt_handlers.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f'[!!! Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())

# by Valendovsky
