import sqlite3

from abc import abstractmethod
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Tuple

from FileRA.File import File
from FileRA.File import Folder

class AbstractStorage(object):
    """
    Определяет интерфейс хранилища заметок.
    """
    @abstractmethod
    def get_all(self) -> Iterable[Folder, File]:
        raise NotImplemented

    @abstractmethod
    def get_file(self, file_id) -> File | None:
        raise NotImplemented

    @abstractmethod
    def get_folder(self, folder_id) -> Folder | None:
        raise NotImplemented

    @abstractmethod
    def put_one(self, file: File):
        raise NotImplemented

    @abstractmethod
    def delete_file(self, file_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_folder(self, folder_id: int):
        raise NotImplemented

class BaseStorage(object):
    """
    Базовый класс хранилища заметок (содержит только данные).
    """
    def __init__(self):
        self._files = {}
        self._folders = {}

class ReadOnlyStorage(BaseStorage):
    """
    Хранилище заметок с возможностью только читать (добавляет методы выгрузки данных).
    """
    def get_all(self) -> Iterable[Folder]:
        return self._folders.values()

    def get_folder(self, folder_id) -> Folder | None:
        return self._folders.get(folder_id)

    def get_file(self, file_id) -> File | None:
        return self._files.get(file_id)

class WriteOnlyStorage(BaseStorage):
    """
    Хранилище заметок с возможностью только (добавляет методы редактирования данных).
    """
    def put_one(self, file: File):
        self._files[file.file_id] = file

    def delete_one(self, file_id: int):
        del self._files[file_id]


class ReadWriteStorage(ReadOnlyStorage, WriteOnlyStorage, AbstractStorage):
    """
    Хранилище заметок в оперативной памяти.
    """
    pass


class FileStorage(AbstractStorage):
    """
    Реализация хранилища в файле.
    """
    def __init__(self, path: Path, delimiter=';;'):
        self.__path = path
        self.__delimiter = delimiter

        # если файла хранилища нет по указанному пути, создадим его
        if not self.__path.exists():
            self.__path.touch()

    def get_all(self) -> Iterable[Folder]:
        # открываем файл хранилища на чтение
        with self.__path.open('r') as f:
            # читаем файл построчно и для каждой строки формируем заметку
            yield from (self.__make_note(line.removesuffix('\n')) for line in f)

    def get_one(self, note_id) -> Note | None:
        # перебираем все заметки в поисках нужной, если находим - возвращаем
        for note in self.get_all():
            if note.note_id == note_id:
                return note

        return None

    def put_one(self, note: Note):
        # читаем заметки, фильтруем, перезаписываем с новыми данными
        lines = [self.__make_line(x) for x in self.get_all() if x.note_id != note.note_id] + [self.__make_line(note)]
        self.__path.write_text('\n'.join(lines))

    def delete_one(self, note_id: int):
        # читаем заметки, фильтруем, перезаписываем без удалённой
        lines = [self.__make_line(note) for note in self.get_all() if note.note_id != note_id]
        self.__path.write_text('\n'.join(lines))

    def __make_line(self, note: Note) -> str:
        return self.__delimiter.join([str(note.note_id), note.author, note.message])

    def __make_note(self, line: str):
        note_id, author, message = line.split(self.__delimiter)
        return Note(int(note_id), author, message)


class DatabaseStorage(AbstractStorage):
    """
    Реализация хранилища в базе данных sqlite.
    """
    def __init__(self, path: Path):
        self.__connection = sqlite3.Connection(path)
        self.__cursor = self.__connection.cursor()

        # создаём таблицу "notes", если таковой ещё нет
        self.__cursor.execute(
            'CREATE TABLE IF NOT EXISTS notes (id int PRIMARY KEY, author text, message text)'
        )

    def get_all(self) -> Iterable[Note]:
        # формируем заметки из всех записей таблицы
        yield from (self.__make_note(row) for row in self.__cursor.execute('SELECT * FROM notes'))

    def get_one(self, note_id) -> Note | None:
        # запрашиваем нужную запись по id
        rows = self.__cursor.execute('SELECT * FROM notes WHERE id=:id', {'id': note_id})

        # формируем заметку из первого (и единственного, вероятно) элемента rows, если таковой имеется
        try:
            return self.__make_note(next(rows))
        except StopIteration:
            return None

    def put_one(self, note: Note):
        # обновляем существующую запись в таблице или вставляем новую
        self.__cursor.execute(
            'INSERT INTO notes VALUES (:note_id, :author, :message) '
            '  ON CONFLICT (id) DO UPDATE SET id=:note_id, author=:author, message=:message',
            asdict(note)
        )

        self.__connection.commit()

    def delete_one(self, note_id: int):
        # обновляем указанную запись из таблицы
        self.__cursor.execute('DELETE FROM notes WHERE id=:id', {'id': note_id})
        self.__connection.commit()

    @staticmethod
    def __make_note(row: Tuple[int, str, str]) -> Note:
        return Note(row[0], row[1], row[2])
