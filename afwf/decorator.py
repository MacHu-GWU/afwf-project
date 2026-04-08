# -*- coding: utf-8 -*-

"""
Decorators for Alfred workflow Script Filter functions.
"""

import functools
import traceback
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable

# One lock per resolved log file path, shared across all decorators targeting
# the same file.  The mutex protects the dict itself during first-time creation.
_locks: dict[Path, threading.Lock] = {}
_locks_mutex = threading.Lock()


def _get_file_lock(path: Path) -> threading.Lock:
    with _locks_mutex:
        if path not in _locks:
            _locks[path] = threading.Lock()
        return _locks[path]


def safe_append_to_file(path: Path, content: str, lock: threading.Lock) -> None:
    """
    Append ``content`` to ``path`` under ``lock``.

    Uses EAFP: tries to open the file directly; only creates parent directories
    on the first ``FileNotFoundError``, avoiding ``mkdir`` overhead on every call.
    """
    with lock:
        try:
            with path.open("a", encoding="utf-8") as f:
                f.write(content)
        except FileNotFoundError:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as f:
                f.write(content)


def log_error(
    log_file: "str | Path | None" = None,
    tb_limit: "int | None" = None,
):
    """
    Decorator factory that appends exception tracebacks to a log file.

    On success, the wrapped function behaves identically to the original.
    On error, the traceback is appended to ``log_file`` with a timestamp,
    then the exception is re-raised so callers still see it.

    Thread-safe: writes to the same file are serialised by a per-file lock.

    :param log_file: Path to the append-only log file.  ``~`` is expanded.
        Parent directories are created automatically.
        Defaults to ``~/.alfred-afwf/error.log``.
    :param tb_limit: Maximum number of stack frames to include.
        ``None`` (default) means the full traceback.

    Usage::

        from afwf.decorator import log_error

        @log_error()  # writes to ~/.alfred-afwf/error.log
        def main(query: str) -> ScriptFilter:
            ...

        @log_error(log_file="~/.alfred-afwf/search_bookmarks.log")
        def main(query: str) -> ScriptFilter:
            ...
    """
    if log_file is None:
        from .paths import path_enum
        _log_path = path_enum.dir_afwf / "error.log"
    else:
        _log_path = Path(log_file).expanduser()

    _lock = _get_file_lock(_log_path)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                tb_msg = traceback.format_exc(limit=tb_limit)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                safe_append_to_file(
                    _log_path,
                    f"[{now}]\n{tb_msg}{'-' * 60}\n",
                    _lock,
                )
                raise

        return wrapper

    return decorator
