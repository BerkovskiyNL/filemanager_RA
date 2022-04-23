from typing import AsyncIterable, Dict

from FileRA.File import File, Folder

from FileRA.StorageAsync import AbstractStorage


class MemoryStorage(AbstractStorage):
    def __init__(self):
        self.__storage: Dict[int, File] = {}
        self.__storage: Dict[int, Folder] = {}

    async def get_all(self) -> AsyncIterable[Folder]:
        for value in self.__storage.values():
            yield value

    async def get_one(self, key: int) -> File | None:
        return self.__storage.get(key)

    async def put_one(self, file: File):
        self.__storage[file.file_id] = File

    async def delete_one(self, key: int):
        if key in self.__storage:
            self.__storage.pop(key)
