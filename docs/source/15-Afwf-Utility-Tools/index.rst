afwf Utility Tools
==============================================================================

``afwf`` ships a small set of optional utilities that come up in nearly every workflow.
Unlike Alfred's official Python library — which bundles its own HTTP client, cache, etc.
from scratch using only the standard library — ``afwf`` delegates to well-maintained
third-party packages and keeps each utility in its own installable extra.


Disk Cache (``afwf.opt.cache``)
------------------------------------------------------------------------------

**Install:** ``pip install afwf[cache]``  (requires `diskcache <https://pypi.org/project/diskcache/>`_ ≥ 5.4)

Alfred Script Filters run on every keystroke. Any handler that calls an external API,
reads a large directory, or does heavy computation should cache its results between
invocations. ``TypedCache`` is a thin subclass of ``diskcache.Cache`` that preserves
the decorated function's type signature, keeping IDE completion intact.

.. code-block:: python

    from pathlib import Path
    from afwf.opt.cache.api import TypedCache

    cache = TypedCache(str(Path.home() / ".cache" / "my-workflow"))

    @cache.typed_memoize(expire=300)   # cache for 5 minutes
    def fetch_repos() -> list[str]:
        # expensive network call — only runs once per 5-minute window
        ...

``typed_memoize`` accepts the same arguments as ``diskcache.Cache.memoize``:

- ``expire`` — TTL in seconds (``None`` = never expires)
- ``name`` — override the cache key name
- ``typed`` — treat argument types as part of the key
- ``tag`` — group entries for bulk eviction
- ``ignore`` — argument positions / names to exclude from the cache key

Typical workflow pattern:

.. code-block:: python

    import afwf.api as afwf
    from afwf.opt.cache.api import TypedCache
    from pathlib import Path

    cache = TypedCache(str(Path.home() / ".cache" / "my-workflow"))

    @cache.typed_memoize(expire=300)
    def get_items() -> list[afwf.Item]:
        ...  # build items from a slow source

    def search(query: str = "") -> afwf.ScriptFilter:
        items = get_items()   # served from disk after the first call
        sf = afwf.ScriptFilter()
        sf.items.extend(items)
        return sf


Fuzzy Matching — Generic (``afwf.opt.fuzzy``)
------------------------------------------------------------------------------

**Install:** ``pip install afwf[fuzzy]``  (requires `rapidfuzz <https://pypi.org/project/rapidfuzz/>`_ ≥ 3.0)

``FuzzyMatcher`` is a generic, type-safe fuzzy matcher for any Python object.
Subclass it, implement ``get_name()``, and you get ranked results for any item type.

.. code-block:: python

    import dataclasses
    from afwf.opt.fuzzy.api import FuzzyMatcher

    @dataclasses.dataclass
    class Repo:
        id: int
        name: str

    class RepoMatcher(FuzzyMatcher[Repo]):
        def get_name(self, item: Repo) -> str | None:
            return item.name   # return None to silently skip an item

    repos = [
        Repo(id=1, name="apple and banana and cherry"),
        Repo(id=2, name="alice and bob and charlie"),
    ]

    matcher = RepoMatcher.from_items(repos)
    results = matcher.match("alice bob", threshold=0)
    # → [Repo(id=2, ...)]

**``match()`` parameters:**

- ``name`` — the search string
- ``threshold`` — minimum similarity score 0–100 (default ``70``); set to ``0`` to return all ranked results
- ``limit`` — maximum number of results (default ``20``)
- ``filter_func`` — optional callable ``(match_tuple) -> bool`` for extra filtering after scoring

**Factory methods:**

- ``FuzzyMatcher.from_items(items)`` — builds the internal name→item map by calling ``get_name()`` on each item
- ``FuzzyMatcher.from_mapper(name_to_item_mapper)`` — supply the map directly when you already have it


Fuzzy Item Matching (``afwf.opt.fuzzy_item``)
------------------------------------------------------------------------------

**Install:** ``pip install afwf[fuzzy]``

``afwf.opt.fuzzy_item`` wires ``FuzzyMatcher`` directly to Alfred
:class:`~afwf.item.Item` objects. It provides two classes:

- ``Item`` — an :class:`~afwf.item.Item` subclass with a ``set_fuzzy_match_name()`` method that stores the match name in ``variables``
- ``FuzzyItemMatcher`` — a ``FuzzyMatcher[Item]`` whose ``get_name()`` reads that variable

This is the pattern you will use in most Script Filters that rank a static list:

.. code-block:: python

    import afwf.api as afwf
    from afwf.opt.fuzzy_item.api import Item, FuzzyItemMatcher

    BOOKMARKS = [
        ("Alfred App",     "https://www.alfredapp.com/"),
        ("Python Docs",    "https://docs.python.org/"),
        ("GitHub",         "https://github.com/"),
        ("Stack Overflow", "https://stackoverflow.com/"),
    ]

    def search_bookmarks(query: str = "") -> afwf.ScriptFilter:
        items = [
            Item(title=title, subtitle=url, arg=url)
            .open_url(url)
            .set_fuzzy_match_name(title)
            for title, url in BOOKMARKS
        ]
        if query.strip():
            items = FuzzyItemMatcher.from_items(items).match(query, threshold=0) or items
        sf = afwf.ScriptFilter()
        sf.items.extend(items)
        return sf

When ``query`` is empty the full list is returned in its original order.
When ``query`` is non-empty the list is replaced with the fuzzy-ranked subset
(falling back to the full list if nothing scores above the threshold).
