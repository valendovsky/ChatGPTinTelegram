#!/usr/bin/env python3

"""
Обработка запросов к ChatGPT.
"""

import openai

from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOTAL_TOKENS
from constants import TOO_LARGE_CONTEXT


async def get_chatgpt_response(message_for_openai: str):
    """
    Возвращает ответ ChatGPT на запросы пользователей.
    """
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(model=OPENAI_MODEL,
                                            messages=message_for_openai)

    # Превышение максимального размера контекста
    if response['usage']['total_tokens'] >= int(MAX_TOTAL_TOKENS):
        return TOO_LARGE_CONTEXT

    return response.choices[0].message.content


async def transcript_voice(file_path):
    """
    Транскрибирует голосовую аудио дорожку в текст.
    """
    audio_file = open(file_path, 'rb')
    transcript = openai.Audio.transcribe('whisper-1', audio_file)

    return transcript['text']


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
