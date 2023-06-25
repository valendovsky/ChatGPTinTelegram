#!/usr/bin/env python3

from pydub import AudioSegment


async def ogg_to_mp3(input_file, output_file):
    """
    Конвертирует медиа файл формата .ogg в формат .mp3.
    """
    AudioSegment.from_ogg(input_file).export(output_file, format='mp3')


def _print_name(name):
    print(f'The module name is {name}')


if __name__ == '__main__':
    _print_name(__name__)
