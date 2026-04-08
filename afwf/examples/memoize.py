# -*- coding: utf-8 -*-

"""
Example: Memoize
================

**What it demonstrates**

Shows how to use :func:`afwf.opt.cache.api.TypedCache.typed_memoize` to cache
expensive function results across Alfred invocations.  The Script Filter
generates a random integer for a given query key and caches it for 5 seconds,
so repeated queries with the same key return the same value until the TTL
expires.  Type ``error`` as the query to trigger a simulated error and see how
:func:`afwf.log_error` writes a traceback to a log file.
"""

import random

import afwf.api as afwf
from afwf.opt.cache.api import TypedCache
from afwf.paths import path_enum

cache = TypedCache(path_enum.dir_afwf / ".cache")


@cache.typed_memoize(tag="memoize", expire=5)
def _get_value(key: str) -> int:
    return random.randint(1, 1000)


@afwf.log_error(log_file=path_enum.dir_afwf / "memoize.log")
def main(query: str) -> afwf.ScriptFilter:
    query = str(query)
    if query.strip() == "error":
        raise ValueError("This is a simulated Python error triggered by query='error'")

    value = _get_value(query)
    sf = afwf.ScriptFilter()
    sf.items.append(afwf.Item(title=f"value is {value}"))
    return sf
