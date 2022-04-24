from typing import AsyncIterable, Dict

from FileRA.File import File, Folder

from FileRA.StorageAsync import AbstractStorage


class MemoryStorage(AbstractStorage):
    def __init__(self):
        self.__storageFile: Dict[int, File] = {}
        self.__storageFolder: Dict[int, Folder] = {}
        self.__storage: Dict[int] = {}

    async def get_all(self) -> AsyncIterable[Folder]:
        for value in self.__storageFolder.values():
            yield value

    async def get_one(self, key: int) -> File | None:
        return self.__storageFile.get(key)

    async def put_one(self, file: File):
        self.__storageFile[file.file_id] = file

    async def delete_one(self, key: int):
        if key in self.__storage:
            self.__storage.pop(key)
