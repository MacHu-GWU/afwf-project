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
    warnings.warn("you have to install 'diskcache' to use 'afwf.opt.cache' feature!")
    raise error


def decohints(decorator: T.Callable) -> T.Callable:
    return decorator


class TypedCache(Cache):
    """
    The original ``diskcache.Cache.memoize`` method will mess up the type hint
    of the decorated function, this class fix this issue.

    Usage::

        cache = TypedCache("/path/to/cache/dir")

        @cache.typed_memoize()
        def very_slow_method() -> T.List[str]:
            pass
    """

    def typed_memoize(self, name=None, typed=False, expire=None, tag=None, ignore=()):
        """
        Memoizing cache decorator, with type hint reserved.
        """
        @decohints
        def decorator(func):
            return self.memoize(name, typed, expire, tag, ignore)(func)

        return decorator
