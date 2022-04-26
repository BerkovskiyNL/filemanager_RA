from dataclasses import dataclass


@dataclass
class File:
    name: str
    size: int


@dataclass
class Folder:
    name: str
    size: int
