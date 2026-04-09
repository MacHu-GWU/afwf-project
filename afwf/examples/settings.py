# -*- coding: utf-8 -*-

"""
Shared settings store for the afwf examples.

Provides :data:`settings` — a lightweight JSON-backed key-value store — and
:class:`SettingsKeyEnum` which enumerates the valid setting keys.  Both are
used by ``set_settings.py`` and ``view_settings.py``.

The store is intentionally simple (a single JSON file) so that the examples
have no extra dependencies beyond the standard library.
"""

import enum
import json
from pathlib import Path

from afwf.paths import path_enum

path_settings_json = path_enum.dir_afwf / "settings.json"


class SettingsKeyEnum(enum.Enum):
    username = "username"
    theme = "theme"
    language = "language"


class _JsonSettings:
    """Minimal dict-like wrapper around a JSON file."""

    def __init__(self, path: Path) -> None:
        self._path = Path(path)

    def _load(self) -> dict:
        if self._path.exists():
            return json.loads(self._path.read_text(encoding="utf-8"))
        return {}

    def get(self, key: str, default=None):
        return self._load().get(key, default)

    def __getitem__(self, key: str):
        return self._load()[key]

    def __setitem__(self, key: str, value: str) -> None:
        data = self._load()
        data[key] = value
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def __contains__(self, key: str) -> bool:
        return key in self._load()


settings = _JsonSettings(path_settings_json)
