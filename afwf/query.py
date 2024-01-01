# -*- coding: utf-8 -*-

"""
query utilities.
"""

import typing as T
import attrs
from attrs_mate import AttrsClass

_SEP = "____"


class QueryParser:
    """
    Utility class that can parse string to :class:`Query`. Naturally, it is
    just a tokenizer.

    :param delimiter: the delimiter to split the query string.
    """

    def __init__(
        self,
        delimiter: T.Union[str, T.List[str]] = " ",
    ):
        if isinstance(delimiter, str):
            self.delimiter = [delimiter]
        else:
            self.delimiter = delimiter

    def parse(self, s: str) -> "Query":
        """
        Convert string query to structured :class:`Query` object.

        :param s: a string.
        """
        non_underscore_sep_list = []
        for sep in self.delimiter:
            if "_" in sep:
                s = s.replace(sep, _SEP)
            else:
                non_underscore_sep_list.append(sep)
        for sep in non_underscore_sep_list:
            s = s.replace(sep, _SEP)
        parts = s.split(_SEP)
        trimmed_parts = [c.strip() for c in parts if c.strip()]
        return Query(
            raw=s,
            parts=parts,
            trimmed_parts=trimmed_parts,
        )


DEFAULT_QUERY_PARSER = QueryParser()


@attrs.define
class Query(AttrsClass):
    """
    Structured query object. This is very useful to parse the input of UI handler.

    :param parts: the parts of query string split by delimiter. For example,
        if the user input is ``"hello world!"``, then ``parts`` is
        ``["hello", "world!"]``.
    :param trimmed_parts: similar to parts, but each part is white-space stripped
        For example, if the user input is ``" hello world "``, then ``parts`` is
        ``["", "hello", "world", ""]``, and ``trimmed_parts`` is ``["hello", "world"]``.

    Usage::

        >>> q = Query.from_str("  a   b   c  ")
        >>> q.trimmed_parts
        ['a', 'b', 'c']
        >>> q.n_trimmed_parts
        3
    """

    raw: str = AttrsClass.ib_str(nullable=False)
    parts: T.List[str] = AttrsClass.ib_list_of_str(nullable=False)
    trimmed_parts: T.List[str] = AttrsClass.ib_list_of_str(nullable=False)

    @classmethod
    def from_str(cls, s: str, parser=DEFAULT_QUERY_PARSER):
        """
        Parse query from string using the given parser.
        """
        return parser.parse(s)

    @property
    def n_parts(self) -> int:
        """
        The number of items in the ``parts``.
        """
        return len(self.parts)

    @property
    def n_trimmed_parts(self) -> int:
        """
        The number of items in the ``trimmed_parts``.
        """
        return len(self.trimmed_parts)
