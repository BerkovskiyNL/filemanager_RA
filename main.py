from pathlib import Path

from notes.Note import Note
from notes.Storage import FileStorage, DatabaseStorage


if __name__ == '__main__':
    storage = DatabaseStorage(Path('storage.db'))
    storage.put_one(Note(1, 'a_1', 'm_1'))
    storage.put_one(Note(2, 'a_2', 'm_2'))
    storage.delete_one(1)
    print([note for note in storage.get_all()])
    print(storage.get_one(2))
