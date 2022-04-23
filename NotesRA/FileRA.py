from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from NotesRA.NoteRA import File
from NotesRA.Storage import AbstractStorage

class FileManager:
    """
    Менеджер заметок. Управляет заметками определённой группы.
    """

    def __init__(self, name: str, storage: AbstractStorage):
        self.__name = name
        self.__storage = storage

    def get_notes(self) -> Iterable[Note]:
        return self.__storage.get_all()

    def get_note(self, note_id) -> Note | None:
        return self.__storage.get_one(note_id)

    def save_note(self, note: Note):
        self.__storage.put_one(note)

    def delete_note(self, note_id: int):
        self.__storage.delete_one(note_id)