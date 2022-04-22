from pathlib import Path


class Files(object):
    _folder_prefix = 'RA_'
    _file_extension = 'txt'

    @classmethod
    def get_all(cls, path: Path) -> tuple:
        for folder in path.iterdir():
            if folder.is_dir() and folder.name.startswith(cls._folder_prefix):
                yield from (
                    (f, f.stat())
                    for f in folder.iterdir()
                    if f.is_file() and f.suffix == f'.{cls._file_extension}'
                )


if __name__ == '__main__':
    pass
