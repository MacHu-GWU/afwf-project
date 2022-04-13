# -*- coding: utf-8 -*-

from typing import List


def parse_query(
    query: str,
    delimiter: str = " ",
) -> List[str]:
    """
    Parse query string using delimiter.
    """
    return [
        word.strip()
        for word in query.split(delimiter) if word.strip()
    ]
