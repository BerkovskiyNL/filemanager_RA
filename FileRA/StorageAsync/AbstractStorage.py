from abc import abstractmethod
from typing import AsyncIterable

from FileRA.File import Folder, File


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
    def create_folder(self) -> AsyncIterable[Folder]:
        raise NotImplementedError

    @abstractmethod
    def create_file(self) -> AsyncIterable[File]:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, key: int):
        raise NotImplementedError
