from dataclasses import dataclass


@dataclass
class Note:
    note_id: int
    author: str
    message: str


@dataclass
class File:
    name: str
    size: int
    content: str


@dataclass
class Folder:
    name: str
    size: int
    content: str