from abc import abstractmethod
from typing import AsyncIterable

from FileRA.File import Folder, File
#from notes.Note import Note


class AbstractStorage(object):
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_folder(self) -> AsyncIterable[Folder]:
        raise NotImplementedError

    @abstractmethod
    def get_file(self) -> AsyncIterable[File]:
        raise NotImplementedError

    @abstractmethod
    async def put_one(self, note: Note):
        raise NotImplementedError

    @abstractmethod
    async def delete_file(self, key: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_folder(self, key: int):
        raise NotImplementedError

    @abstractmethod
    async def get_folder(self, key: int) -> Folder:
        raise NotImplementedError