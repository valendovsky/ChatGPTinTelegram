#!/usr/bin/env python3

# Названия команд бота
ACCESS = 'all_access'
SUBSCRIBERS = 'subscribers'
CHECK_ACCESS = 'check_access'
USER_CONTEXT = 'context'
ALL_CONTEXT = 'all_context'

# Сообщение о слишком большом контексте
TOO_LARGE_CONTEXT = 'В данный момент вы использовали максимум токенов в рамках контекста. Контекст очищен.'


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
