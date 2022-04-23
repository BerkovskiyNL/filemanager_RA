from abc import abstractmethod
from typing import AsyncIterable

from FileRA.File import Folder, File


class AbstractStorage(object):
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_all(self) -> AsyncIterable[Folder]:
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, key: int) -> File:
        raise NotImplementedError

    @abstractmethod
    async def get_folder(self, key: int) -> Folder:
        raise NotImplementedError

    @abstractmethod
    async def create_folder(self, folder: Folder):
        raise NotImplementedError

    @abstractmethod
    async def put_one(self, file: File):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, key: int):
        raise NotImplementedError
