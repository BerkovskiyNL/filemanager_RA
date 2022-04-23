from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from FileRA.File import File, Folder
from FileRA.StorageAsync import AbstractStorage


class FileManager:
    """
    Менеджер заметок. Управляет заметками определённой группы.
    """

    def __init__(self, name: str, storage: AbstractStorage):
        self.__name = name
        self.__storage = storage

    def get_all(self) -> Iterable[Folder, File]:
        return self.__storage.get_all()

    def get_file(self, file_id) -> File | None:
        return self.__storage.get_file(file_id)

    def create_folder(self) -> Folder:
        return self.__storage.create_folder()

    def put_one(self, file: File):
        self.__storage.put_one(file)

    def delete_one(self, file_id: int):
        self.__storage.delete_one(file_id)

    def put_folder(self, folder: Folder):
        self.__storage.put_one(folder)
