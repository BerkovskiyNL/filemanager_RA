from __future__ import annotations

from typing import AsyncIterable, Dict

from FileRA.File import File, Folder

from FileRA.StorageAsync import AbstractStorage

import os

class MemoryStorage(AbstractStorage):

    def __init__(self):
        self.__storageFile: Dict[str, File] = {}
        self.__storageFolder: Dict[str, Folder] = {}
        self.__storage: Dict[int] = {}

    async def get_all(self) -> AsyncIterable[Folder]:
        for value in self.__storageFolder.values():
            yield value

    async def get_one(self, key: int) -> File | None:
        return self.__storageFile.get(key)

    async def put_one(self, file: File):
        self.__storageFile[file.name] = file

    async def create_folder(self, folder: Folder):
        self.__storageFolder[folder.name] = folder

    async def delete_one(self, filename: str):
        if filename in self.__storageFile:
            os.remove(self.__storageFile[filename].name)
            self.__storageFile.pop(filename)

    async def delete_folder(self, foldername: str):
        if foldername in self.__storageFolder:
            os.rmdir(self.__storageFolder[foldername].name)
            self.__storageFolder.pop(foldername)