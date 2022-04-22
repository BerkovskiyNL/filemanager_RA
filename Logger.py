import logging
import sys

from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

from pathlib import Path
from typing import List


# храним файлы логов в этой папке
def __logs_directory() -> Path:
    path = Path.home().joinpath('.logs', 'RA_Python')

    if not path.exists():
        path.mkdir(parents=True)

    return path


# определяем формат имени файлов логов
def __log_file(application: str) -> Path:
    return __logs_directory().joinpath(f'{application}.log')


# определяем формат сообщений в логах
def __record_format() -> str:
    return '[%(levelname)s] %(asctime)s: %(message)s'


# определяем формат даты/времени в соощениях
def __datetime_format() -> str:
    return '%d.%m.%Y %H:%M:%S'


# обработчики сообщений
def __handlers(application: str) -> List[logging.Handler]:
    return [
        # запись в файлы
        TimedRotatingFileHandler(filename=__log_file(application), when='M', backupCount=3),

        # вывод в консоль
        StreamHandler(stream=sys.stdout),
    ]


def configure_logger(application: str):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for handler in __handlers(application):
        handler.setFormatter(logging.Formatter(__record_format(), __datetime_format()))
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
