# -*- coding: utf-8 -*-

"""
Enhancement for standard enum library.
"""

import enum
from typing import List


class BetterEnum(enum.Enum):
    """
    Provide additional method for enum.
    """

    @classmethod
    def has_name(cls, name: str) -> bool:
        """
        Check if a name is defined as enum.
        """
        try:
            _ = cls[name]
            return True
        except KeyError:
            return False

    @classmethod
    def has_value(cls, value) -> bool:
        """
        Check if a value is defined as enum.
        """
        try:
            _ = cls(value)
            return True
        except ValueError:
            return False

    @classmethod
    def to_names(cls) -> List[str]:
        """
        Get list of all defined names.
        """
        return [
            i.name
            for i in cls
        ]

    @classmethod
    def to_values(cls) -> list:
        """
        Get list of all defined values.
        """
        return [
            i.value
            for i in cls
        ]


special_char = ["!@#$%^&*()_+-=~`[]{}|,. "]


def snake_case(s) -> str: # pragma: no cover
    """
    convert string to snake case.
    """
    s = s.lower()
    for c in special_char:
        s = s.replace(c, "_")
    return s
