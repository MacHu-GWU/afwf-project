# -*- coding: utf-8 -*-

"""
query utilities.
"""

import dataclasses

_SEP = "____"


@dataclasses.dataclass
class QueryParser:
    """
    Utility class that can parse string to :class:`Query`. Naturally, it is
    just a tokenizer.

    :param delimiter: list of delimiter strings to split the query string.

    Use the :meth:`from_delimiter` factory to construct with a single string
    or a list of strings.
    """

    delimiter: list[str] = dataclasses.field(default_factory=lambda: [" "])

    @classmethod
    def from_delimiter(cls, delimiter: str | list[str] = " ") -> "QueryParser":
        """
        Create a :class:`QueryParser` from a single delimiter string or a list.
        """
        if isinstance(delimiter, str):
            return cls(delimiter=[delimiter])
        return cls(delimiter=delimiter)

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


@dataclasses.dataclass
class Query:
    """
    Structured query object. This is very useful to parse the input of UI handler.

    :param raw: the raw query string after delimiter normalization.
    :param parts: the parts of query string split by delimiter. For example,
        if the user input is ``"hello world!"``, then ``parts`` is
        ``["hello", "world!"]``.
    :param trimmed_parts: similar to parts, but each part is white-space stripped.
        For example, if the user input is ``" hello world "``, then ``parts`` is
        ``["", "hello", "world", ""]``, and ``trimmed_parts`` is ``["hello", "world"]``.

    Usage::

        >>> q = Query.from_str("  a   b   c  ")
        >>> q.trimmed_parts
        ['a', 'b', 'c']
        >>> q.n_trimmed_parts
        3
    """

    raw: str
    parts: list[str]
    trimmed_parts: list[str]

    @classmethod
    def from_str(cls, s: str, parser: QueryParser = DEFAULT_QUERY_PARSER) -> "Query":
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
