from pathlib import Path
from zipfile import ZipFile

if __name__ == '__main__':
    source_directory = Path(__file__).parent
    source_files = [entry for entry in source_directory.iterdir() if entry.is_file() and entry.name.endswith('.py')]

    with ZipFile(source_directory.joinpath('sources.zip'), 'w') as zip_file:
        for file in source_files:
            zip_file.write(file.relative_to(source_directory))
