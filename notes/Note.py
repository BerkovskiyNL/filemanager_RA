from dataclasses import dataclass


@dataclass
class Note:
    note_id: int
    author: str
    message: str
