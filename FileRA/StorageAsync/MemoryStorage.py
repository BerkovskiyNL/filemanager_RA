from __future__ import annotations

from typing import AsyncIterable, Dict, Iterable

from FileRA.File import File, Folder

from FileRA.StorageAsync import AbstractStorage

import os

from pathlib import Path

class MemoryStorage(AbstractStorage):

    def __init__(self):
        self.__storageFile: Dict[str, File] = {}
        self.__storageFolder: Dict[str, Folder] = {}
        self.__storage: Dict[int] = {}

    async def get_all(self) -> AsyncIterable[Folder]:
        for value in self.__storageFolder.values():
            yield value

    async def get_folder(self, folder: str) -> Folder | None:
        self.list_folder(Path(folder))
        return self.__storageFolder.get(folder)

    async def get_file(self, file: str) -> File | None:
        f = self.__storageFile.get(Path(file))
        f.content = Path(file).open('r').read()
        return f

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

    async def list_folder(self, path: Path):
        self.__storageFolder = {}
        for folder in path.iterdir():
            if folder.is_dir():
                self.__storageFolder[folder] = Folder(folder, 0)
        for value in self.__storageFolder.values():
            yield value

    async def list_files(self, path: Path):
        self.__storageFile = {}
        for file in path.iterdir():
            if file.is_file():
                self.__storageFile[file] = File(file, file.stat().st_size, "")
        for value in self.__storageFile.values():
            yield value