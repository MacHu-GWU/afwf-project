# -*- coding: utf-8 -*-

import typing as T
import os
import contextlib
from pathlib import Path

__version__ = "0.1.1"

@contextlib.contextmanager
def temp_cwd(path: T.Union[str, Path]):
    """
    Temporarily set the current working directory (CWD) and automatically
    switch back when it's done.

    Example:

    .. code-block:: python

        with temp_cwd(Path("/path/to/target/working/directory")):
            # do something
    """
    path = Path(path).absolute()
    if not path.is_dir():
        raise NotADirectoryError(f"{path} is not a dir!")
    cwd = os.getcwd()
    os.chdir(str(path))
    try:
        yield path
    finally:
        os.chdir(cwd)


def get_dir_here(file_var: str) -> Path:
    """
    Get the directory of the current file.

    Example:

    .. code-block:: python

        get_dir_here(__file__)
    """
    return Path(file_var).absolute().parent
