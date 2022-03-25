# -*- coding: utf-8 -*-

from typing import List


def parse_query(query: str) -> List[str]:
    return [
        word.strip()
        for word in query.split(" ") if word.strip()
    ]
