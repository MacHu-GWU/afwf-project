# -*- coding: utf-8 -*-

import enum
from typing import Optional, List


class BetterEnum(enum.Enum):
    @classmethod
    def has_name(cls, name: str) -> bool:
        try:
            _ = cls[name]
            return True
        except KeyError:
            return False

    @classmethod
    def has_value(cls, value) -> bool:
        try:
            _ = cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def to_names(cls) -> List[str]:
        return [
            i.name
            for i in cls
        ]

    @classmethod
    def to_values(cls) -> list:
        return [
            i.value
            for i in cls
        ]


special_char = [":"]


def snake_case(s):
    """
    convert string to snake case.
    """
    s = s.lower()
    for c in special_char:
        s = s.replace(c, "_")
    return s


class StrEnum(enum.Enum):
    """
    Special enum that value are all string or None.

    The ``key`` has to be the same as ``snake_case(value)``, with all
    special characters become "_"

    Example::

        class Color(StrEnum):
            red = "Red"
            green = "green"
            none = None

    """

    @classmethod
    def get_by_value(cls, v: Optional[str]) -> 'StrEnum':
        return cls[snake_case(str(v).lower())]
