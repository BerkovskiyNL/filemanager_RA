from dataclasses import dataclass


@dataclass
class File:
    file_id: int
    name: str
    size: int
    content: str


@dataclass
class Folder:
    folder_id: int
    file_id: int
    name: str
    size: int
    content: str