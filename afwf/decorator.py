# -*- coding: utf-8 -*-

"""
Decorators for Alfred workflow Script Filter functions.
"""

import functools
import logging
import logging.handlers
import traceback
import threading
from pathlib import Path
from typing import Callable

# Lazy logger cache: created on first exception, keyed by resolved log path.
# The mutex guards the dict during first-time initialisation.
_loggers: dict[Path, logging.Logger] = {}
_loggers_mutex = threading.Lock()


def _get_logger(
    path: Path,
    max_bytes: int,
    backup_count: int,
) -> logging.Logger:
    with _loggers_mutex:
        if path not in _loggers:
            path.parent.mkdir(parents=True, exist_ok=True)
            logger = logging.getLogger(f"afwf:{path}")
            logger.setLevel(logging.ERROR)
            logger.propagate = False  # don't bubble up to the root logger
            if not logger.handlers:  # guard against duplicate handlers on re-use
                handler = logging.handlers.RotatingFileHandler(
                    filename=path,
                    maxBytes=max_bytes,
                    backupCount=backup_count,
                    encoding="utf-8",
                )
                handler.setFormatter(
                    logging.Formatter(
                        fmt="[%(asctime)s]\n%(message)s\n" + "-" * 60,
                        datefmt="%Y-%m-%d %H:%M:%S",
                    )
                )
                logger.addHandler(handler)
            _loggers[path] = logger
        return _loggers[path]


def log_error(
    log_file: "str | Path | None" = None,
    tb_limit: "int | None" = None,
    max_bytes: int = 500_000,
    backup_count: int = 2,
):
    """
    Decorator factory that logs exception tracebacks to a rotating file.

    On success, the wrapped function behaves identically to the original.
    On error, the traceback is appended to ``log_file``, then re-raised.

    The logger is created lazily — zero file I/O on the happy path.
    ``RotatingFileHandler`` handles both rotation and thread safety.

    :param log_file: Path to the log file.  ``~`` is expanded.  Parent
        directories are created automatically.
        Defaults to ``~/.alfred-afwf/error.log``.
    :param tb_limit: Maximum number of stack frames.  ``None`` = full traceback.
    :param max_bytes: Rotate the file when it exceeds this size in bytes.
        Defaults to 500 000 (≈ 500 KB).
    :param backup_count: Number of rotated backup files to keep.
        Defaults to 2 (i.e. ``error.log``, ``error.log.1``, ``error.log.2``).

    Usage::

        import afwf.api as afwf

        @afwf.log_error()
        def main(query: str) -> afwf.ScriptFilter:
            ...

        @afwf.log_error(log_file="~/.alfred-afwf/search_bookmarks.log", max_bytes=200_000)
        def main(query: str) -> afwf.ScriptFilter:
            ...
    """
    if log_file is None:
        from .paths import path_enum
        _log_path = path_enum.dir_afwf / "error.log"
    else:
        _log_path = Path(log_file).expanduser()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                tb_msg = traceback.format_exc(limit=tb_limit).rstrip()
                _get_logger(_log_path, max_bytes, backup_count).error(tb_msg)
                raise

        return wrapper

    return decorator
