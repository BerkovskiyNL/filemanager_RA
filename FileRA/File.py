from dataclasses import dataclass


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