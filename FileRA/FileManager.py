from typing import Iterable

from FileRA.File import File, Folder
from FileRA.StorageAsync import AbstractStorage


class FileManager:
    """
    Файлменеджер
    """

    def __init__(self, name: str, storage: AbstractStorage):
        self.__name = name
        self.__storage = storage

    def get_all(self) -> Iterable[Folder]:
        return self.__storage.get_all()

    def create_folder(self) -> Folder:
        return self.__storage.create_folder()

    def put_one(self, file: File):
        self.__storage.put_one(file)

    def delete_one(self, file_id: int):
        self.__storage.delete_one(file_id)

    def delete_folder(self, folder_id: int):
        self.__storage.delete_folder(folder_id)

    def list_dir (self, folder: str, file: str):
        self.__storage.list_dir(folder, file)