# -*- coding: utf-8 -*-

"""
query utilities.
"""

from typing import List
import attr
from attrs_mate import AttrsClass


@attr.define
class Query(AttrsClass):
    """
    Structured query object.
    """
    parts: List[str] = AttrsClass.ib_list_of_str()
    trimmed_parts: List[str] = AttrsClass.ib_list_of_str()


class QueryParser:
    """
    Utility class that can parse string to query.
    """

    def __init__(
        self,
        delimiter: str = " ",
    ):
        self.delimiter = delimiter

    def parse(self, s: str) -> Query:
        parts = s.split(self.delimiter)
        trimmed_parts = [c.strip() for c in parts if c.strip()]
        return Query(
            parts=parts,
            trimmed_parts=trimmed_parts,
        )
