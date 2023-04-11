# -*- coding: utf-8 -*-

"""
Disk cache for Alfred Workflow.
"""

import typing as T
import warnings

try:  # pragma: no cover
    from diskcache import Cache

    has_diskcache = True
except ImportError as e:  # pragma: no cover
    error = e
    has_diskcache = False

if has_diskcache is False:  # pragma: no cover
    warnings.warn("you have to install 'fuzzywuzzy' to use 'afwf.opt.fuzzy' feature!")
    raise error


def decohints(decorator: T.Callable) -> T.Callable:
    return decorator


class TypedCache(Cache):
    def typed_memoize(
        self,
        name=None,
        typed=False,
        expire=None,
        tag=None,
        ignore=(),
    ):
        @decohints
        def decorator(func):
            return self.memoize(name, typed, expire, tag, ignore)(func)

        return decorator
