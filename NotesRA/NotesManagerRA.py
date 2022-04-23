from typing import Iterable

from NotesRA.NoteRA import File
from NotesRA.Storage import AbstractStorage
from NotesRA.NoteRA import Folder


class FileManager:
    """
    Менеджер заметок. Управляет заметками определённой группы.
    """

    def __init__(self, name: str, storage: AbstractStorage):
        self.__name = name
        self.__storage = storage

    def get_notes(self) -> Iterable[Note]:
        return self.__storage.get_all()

    def get_file(self, file_id) -> File | None:
        return self.__storage.get_file(file_id)

    def get_folder(self, folder_id) -> Folder | None:
        return self.__storage.get_folder(Folder_id)


    def save_file(self, file: File):
        self.__storage.put_one(File)

    def delete_file(self, file_id: int):
        self.__storage.delete_one(file_id)

