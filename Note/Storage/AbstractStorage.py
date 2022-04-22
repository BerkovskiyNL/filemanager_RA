from abc import abstractmethod
from typing import AsyncIterable

from notes.Note import Note


class AbstractStorage(object):
    async def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_all(self) -> AsyncIterable[Note]:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, key: int) -> Note:
        raise NotImplementedError

    @abstractmethod
    async def put_one(self, note: Note):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, key: int):
        raise NotImplementedError
