.. _Typed-Disk-Cache:

Typed Disk Cache: opt.cache
==============================================================================

Alfred invokes a Script Filter on every keystroke.  If your handler calls an
expensive operation — a network request, a disk scan, a slow computation —
the result should be cached between invocations so Alfred stays responsive.

:class:`~afwf.opt.cache.impl.TypedCache` provides a persistent, disk-backed
cache with a type-hint-safe memoize decorator.  It requires the ``afwf[cache]``
extra (``diskcache >= 5.4.0``).


Why TypedCache Instead of diskcache Directly
------------------------------------------------------------------------------

``diskcache.Cache`` ships its own ``memoize`` decorator, but applying it erases
the decorated function's type hints — IDE auto-complete and static analysis stop
working on the wrapped function.

:class:`~afwf.opt.cache.impl.TypedCache` inherits everything from
``diskcache.Cache`` and adds a single method,
:meth:`~afwf.opt.cache.impl.TypedCache.typed_memoize`, that wraps
``cache.memoize()`` in a way that preserves the original function's signature.
Everything else — cache location, eviction, expiry — is standard ``diskcache``.


Basic Usage
------------------------------------------------------------------------------

Create a ``TypedCache`` instance at module level (once per process) and
decorate the expensive function:

.. code-block:: python

    from afwf.opt.cache.api import TypedCache
    from afwf.paths import path_enum

    cache = TypedCache(path_enum.dir_afwf / ".cache")

    @cache.typed_memoize(expire=60)
    def fetch_results(query: str) -> list[str]:
        # slow network call or heavy computation here
        ...

The first call with a given ``query`` runs the function and stores the result.
Subsequent calls with the same ``query`` within 60 seconds return the cached
value without executing the function body.


typed_memoize() Parameters
------------------------------------------------------------------------------

``typed_memoize`` passes all arguments through to ``diskcache.Cache.memoize``.
The most commonly used ones:

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Parameter
     - Default
     - Meaning
   * - ``expire``
     - ``None``
     - Time-to-live in seconds.  ``None`` means the entry never expires.
   * - ``tag``
     - ``None``
     - String tag attached to every entry written by this decorator.
       Useful for bulk-invalidating a group of entries:
       ``cache.evict(tag="my_tag")``.
   * - ``name``
     - ``None``
     - Override the cache key prefix.  By default the function's qualified
       name is used.
   * - ``typed``
     - ``False``
     - When ``True``, ``f(1)`` and ``f(1.0)`` are cached separately.
   * - ``ignore``
     - ``()``
     - Tuple of argument names to exclude from the cache key — useful for
       arguments that change every call but do not affect the result
       (e.g. a logger or a request context).


The memoize.py Example
------------------------------------------------------------------------------

The ``memoize`` example generates a random integer for a given query key and
caches it for 5 seconds.  Repeated queries with the same key return the same
value until the TTL expires, demonstrating that the function body runs only
once per unique key per TTL window:

.. literalinclude:: ../../../../afwf/examples/memoize.py
   :language: python

Typing ``error`` as the query triggers a deliberate exception so you can
verify that :func:`~afwf.decorator.log_error` writes the traceback to the
log file even when the cached path is not taken.


Cache Location Convention
------------------------------------------------------------------------------

Store the cache directory inside ``path_enum.dir_afwf`` (``~/.alfred-afwf/``)
so all workflow-related state lives in one place and can be wiped cleanly:

.. code-block:: python

    cache = TypedCache(path_enum.dir_afwf / ".cache")

The directory is created automatically by ``diskcache`` on first use.


Cache Invalidation
------------------------------------------------------------------------------

``TypedCache`` inherits the full ``diskcache.Cache`` API.  The most useful
invalidation methods:

.. code-block:: python

    cache.clear()               # delete everything
    cache.evict(tag="my_tag")   # delete all entries with this tag
    cache.delete(key)           # delete one specific key

In tests, call ``cache.clear()`` in the test setup to start from a clean
state — see ``tests/opt/test_opt_cache.py`` for the pattern.


Installation
------------------------------------------------------------------------------

.. code-block:: bash

    pip install "afwf[cache]"
    # or with uv:
    uv add "afwf[cache]"
