# pylint: disable=missing-module-docstring
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator


@contextmanager
def named_temporary_file() -> Generator[Path, None, None]:
    """Required as tempfile.NamedTemporaryFile does not work on windows"""
    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        temp_file = temp_dir / "temporary_file"
        temp_file.touch()
        yield temp_file
