# -*- coding: utf-8 -*-

import random

import afwf.api as afwf
from afwf.opt.cache.api import TypedCache
from afwf.paths import path_enum

cache = TypedCache(path_enum.dir_afwf / ".cache")


@cache.typed_memoize(tag="memorize_cache", expire=5)
def _get_value(key: str) -> int:
    return random.randint(1, 1000)


@afwf.log_error(log_file=path_enum.dir_afwf / "memorize_cache.log")
def main(query: str) -> afwf.ScriptFilter:
    query = str(query)
    if query.strip() == "error":
        raise ValueError("This is a simulated Python error triggered by query='error'")

    value = _get_value(query)
    sf = afwf.ScriptFilter()
    sf.items.append(afwf.Item(title=f"value is {value}"))
    return sf
