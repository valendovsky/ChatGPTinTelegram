#!/usr/bin/env python3

"""
Константные значения.
"""

# Названия команд бота
START_DESCRIPTION = 'Начало работы'
ACCESS = 'all_access'
ACCESS_DESCRIPTION = 'Изменить права доступа для всех'
SUBSCRIBERS = 'subscribers'
SUBSCRIBERS_DESCRIPTION = 'Изменить права доступа для подписчиков'
CHECK_ACCESS = 'check_access'
CHECK_ACCESS_DESCRIPTION = 'Проверить права доступа'
USER_CONTEXT = 'context'
USER_CONTEXT_DESCRIPTION = 'Сбросить контекст'
ALL_CONTEXT = 'all_context'
ALL_CONTEXT_DESCRIPTION = 'Сбросить контекст для всех пользователей'
SENDER = 'sender'
SENDER_DESCRIPTION = 'Начать рассылку (укажите название рассылки)'
CANCEL = 'cancel'

# Клавиатура создания рассылки
ADD_BUTTON_TEXT = 'Добавить кнопку'
ADD_BUTTON_CALLBACK = 'add_button'
NO_BUTTON_TEXT = 'Продолжить без кнопки'
NO_BUTTON_CALLBACK = 'no_button'

# Клавиатура подтверждения рассылки
CONFIRM_TEXT = 'Подтвердить'
CONFIRM_CALLBACK = 'confirm_sender'
CANCEL_TEXT = 'Отменить'
CANCEL_CALLBACK = 'cancel_sender'

# Сообщение о слишком большом контексте
TOO_LARGE_CONTEXT = 'В данный момент вы использовали максимум токенов в рамках контекста. Контекст очищен.'


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
