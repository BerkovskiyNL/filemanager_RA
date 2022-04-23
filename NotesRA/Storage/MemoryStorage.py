from typing import AsyncIterable, Dict

from notes.Note import Note

from notes.StorageAsync import AbstractStorage


class MemoryStorage(AbstractStorage):
    def __init__(self):
        self.__storage: Dict[int, Note] = {}

    async def get_all(self) -> AsyncIterable[Note]:
        for value in self.__storage.values():
            yield value

    async def get_one(self, key: int) -> Note | None:
        return self.__storage.get(key)

    async def put_one(self, note: Note):
        self.__storage[note.note_id] = note

    async def delete_one(self, key: int):
        if key in self.__storage:
            self.__storage.pop(key)
