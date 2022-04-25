import asyncio
import json
import logging
import os
import pathlib
from abc import abstractmethod
from asyncio.streams import StreamReader, StreamWriter
from operator import index
from typing import Any

import Logger

from FileRA.StorageAsync import AbstractStorage, MemoryStorage
from FileRA.File import File, Folder


class AbstractCommand(object):
    """
    Базовый класс команды.
    В рамках одной команды читаем данные, ведём обработку и пишем результат в ответ.
    """

    def __init__(self, storage: AbstractStorage, reader: StreamReader, writer: StreamWriter):
        self._storage = storage
        self._reader = reader
        self._writer = writer

    @abstractmethod
    async def execute(self):
        pass

    async def _readline(self):
        return (await self._reader.readline()).decode().strip()

    def _writeline(self, line: str):
        self._writer.write((line + '\n').encode())


class InfoFolderCommand(AbstractCommand):
    async def execute(self):
        self._writeline('OK')
        self._writeline(';;'.join([str(folder) async for folder in self._storage.get_all()]))


class InfoFileCommand(AbstractCommand):
    async def execute(self):
        try:
            file_id = int(await self._readline())

            if file := await self._storage.get_file(file_id):
                self._writeline('OK')
                self._writeline(str(file))
            else:
                self._writeline(f'ERROR: file "{file_id}" not found')
        except ValueError as error:
            self._writeline(f'ERROR: {error}')


class GetFolderCommand(AbstractCommand):
    async def execute(self):
        try:
            folder_id = int(await self._readline())

            if folder := await self._storage.get_folder(folder_id):
                self._writeline('OK')
                self._writeline(str(folder))
            else:
                self._writeline(f'ERROR: note "{folder_id}" not found')
        except ValueError as error:
            self._writeline(f'ERROR: {error}')


class CreateFileCommand(AbstractCommand):
    async def execute(self):
        try:
            file = input('Введите имя файла')
            open(file, 'w')
            await self._storage.put_one()
            self._writeline('Cоздан')
            file.close()
        except (TypeError, ValueError) as error:
            self._writeline(f'ERROR: {error}')


class CreateFolderCommand(AbstractCommand):
    async def execute(self):
        try:
            folder = input('Введите имя папки')
            os.mkdir(folder)
            await self._storage.put_two(folder)
            self._writeline('OK')
        except (TypeError, ValueError) as error:
            self._writeline(f'ERROR: {error}')


class DeleteFileCommand(AbstractCommand):
    async def execute(self):
        file_id = int(await self._readline())
        await self._storage.delete_one(file_id)
        self._writeline('OK')


class DeleteFolderCommand(AbstractCommand):
    async def execute(self):
        folder_id = int(await self._readline())
        await self._storage.delete_one(folder_id)
        self._writeline('OK')


class CommandFactory(object):
    """
    Фабрика команд. Позволяет получать нужный класс команды по имени.
    """

    class __UnknownCommand(AbstractCommand):
        async def execute(self):
            self._writeline('Error: "Unknown command"')
            logging.error('Error: "Unknown command"')

    # регистрируем команды, которые будет поддерживать сервер
    _commands = {

        'CREATE_FOLDER': CreateFolderCommand,
        'CREATE_FILE': CreateFileCommand,
        'DELETE_FOLDER': DeleteFolderCommand,
        'DELETE_FILE': DeleteFileCommand,
        'INFO_FOLDER': InfoFolderCommand,
        'INFO_FILE': InfoFileCommand
    }

    def __init__(self, storage: AbstractStorage, reader: StreamReader, writer: StreamWriter):
        self.__storage = storage
        self.__reader = reader
        self.__writer = writer

    def get_command(self, command: str) -> AbstractCommand:
        return self._commands.get(command, self.__UnknownCommand)(
            self.__storage, self.__reader, self.__writer
        )


class CommandProcessor(object):
    """
    Класс логики сервера (обработчик команд).
    """

    def __init__(self, storage: AbstractStorage):
        # внедряем зависимости (нам нужен только storage)
        self.__storage = storage

    # превращаем экземпляры класса Callable, чтобы завернуть в asyncio.start_server()
    async def __call__(self, reader: StreamReader, writer: StreamWriter):
        # получаем информацию о созданном соединении
        host, port = writer.transport.get_extra_info('peername')
        logging.info(f'Connected to: {host}:{port}')

        factory = CommandFactory(self.__storage, reader, writer)

        while not writer.is_closing():
            # построчно читаем команды и выполняем их
            line = (await reader.readline()).decode().strip()
            command = factory.get_command(line)
            await command.execute()

        logging.info(f'Disconnected from {host}:{port}')


async def main():
    processor = CommandProcessor(MemoryStorage())

    # запускаем сервер на localhost:3333
    server = await asyncio.start_server(processor, 'localhost', 3333)
    logging.info('Server started')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    Logger.configure_logger('tcp_server_example')

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Server stopped')
