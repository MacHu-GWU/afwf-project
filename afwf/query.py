# -*- coding: utf-8 -*-

"""
query utilities.
"""

import typing as T
import attr
from attrs_mate import AttrsClass


@attr.define
class Query(AttrsClass):
    """
    Structured query object.

    :param parts: the parts of query string split by delimiter
    :param trimmed_parts: similar to parts, but each part is white space stripped
    """
    parts: T.List[str] = AttrsClass.ib_list_of_str()
    trimmed_parts: T.List[str] = AttrsClass.ib_list_of_str()


SEP = "____"

class QueryParser:
    """
    Utility class that can parse string to query.
    """

    def __init__(
        self,
        delimiter: T.Union[str, T.List[str]] = " ",
    ):
        if isinstance(delimiter, str):
            self.delimiter = [delimiter,]
        else:
            self.delimiter = delimiter

    def parse(self, s: str) -> Query:
        """
        Convert string query to structured query object.
        """
        for sep in self.delimiter:
            s = s.replace(sep, SEP)
        parts = s.split(SEP)
        trimmed_parts = [c.strip() for c in parts if c.strip()]
        return Query(
            parts=parts,
            trimmed_parts=trimmed_parts,
        )
