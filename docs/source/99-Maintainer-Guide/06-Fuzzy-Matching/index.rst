.. _Fuzzy-Matching:

Fuzzy Matching: opt.fuzzy and opt.fuzzy_item
==============================================================================

``afwf`` ships two optional modules for narrowing a list of items by fuzzy
string similarity.  They are layered: ``opt.fuzzy`` provides a generic
matcher for any Python type; ``opt.fuzzy_item`` specialises it for
:class:`~afwf.item.Item`.

Both require the ``afwf[fuzzy]`` extra (``rapidfuzz >= 3.0.0``).


opt.fuzzy — Generic Fuzzy Matching
------------------------------------------------------------------------------

:class:`~afwf.opt.fuzzy.impl.FuzzyMatcher` is a generic dataclass over an
arbitrary item type ``T``.  It builds an internal name→items map at
construction time and exposes a single :meth:`~afwf.opt.fuzzy.impl.FuzzyMatcher.match`
method.

**Subclassing**

To use it you must subclass and implement :meth:`~afwf.opt.fuzzy.impl.FuzzyMatcher.get_name`:

.. code-block:: python

    import dataclasses
    from afwf.opt.fuzzy.api import FuzzyMatcher

    @dataclasses.dataclass
    class Bookmark:
        title: str
        url: str

    class BookmarkMatcher(FuzzyMatcher[Bookmark]):
        def get_name(self, item: Bookmark) -> str | None:
            return item.title   # the string that gets fuzzy-matched

    bookmarks = [
        Bookmark("Alfred App", "https://www.alfredapp.com/"),
        Bookmark("Python Docs", "https://docs.python.org/"),
    ]
    matcher = BookmarkMatcher.from_items(bookmarks)
    results = matcher.match("alfred", threshold=0)
    # → [Bookmark("Alfred App", ...)]

If ``get_name()`` returns ``None`` for an item, that item is silently excluded
from the match index — useful for conditionally hiding items.


**Factory methods**

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Factory
     - When to use
   * - ``from_items(items)``
     - You have a flat list; ``get_name`` extracts the match key
   * - ``from_mapper(name_to_item_mapper)``
     - You already have a ``{name: [items]}`` dict; skips the ``get_name`` loop

**match() parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Default
     - Meaning
   * - ``name``
     - —
     - The search string to match against
   * - ``threshold``
     - ``70``
     - Minimum similarity score (0–100).  Results below this are discarded.
       Use ``threshold=0`` to return everything sorted by score.
   * - ``limit``
     - ``20``
     - Maximum number of results to return
   * - ``filter_func``
     - ``lambda x: True``
     - Extra callable applied after score filtering.  Receives a
       ``(name, score, index)`` tuple — the raw rapidfuzz result row.

Results are sorted by score, highest first.  If the best match falls below
``threshold``, an empty list is returned immediately.

**Duplicate names**

Multiple items can share the same name.  They are stored together under one
key in the internal mapper and all returned when that name matches.


opt.fuzzy_item — Fuzzy Matching for Alfred Items
------------------------------------------------------------------------------

:class:`~afwf.opt.fuzzy_item.impl.FuzzyItemMatcher` is a ready-made subclass
of ``FuzzyMatcher`` for :class:`~afwf.item.Item` objects.  It does not require
you to subclass anything — the match name is stored directly on the item.

**Item.set_fuzzy_match_name()**

The companion :class:`~afwf.opt.fuzzy_item.impl.Item` (a thin subclass of the
core ``Item``) stores the match name in ``item.variables["fuzzy_match_name"]``.
Storing it in ``variables`` means the name travels with the item through
Alfred's variable inheritance mechanism:

.. code-block:: python

    import afwf.opt.fuzzy_item.api as fuzzy_item

    item = fuzzy_item.Item(title="Alfred App", subtitle="https://www.alfredapp.com/")
    item.set_fuzzy_match_name("Alfred App")
    # item.variables == {"fuzzy_match_name": "Alfred App"}

    item.fuzzy_match_name   # → "Alfred App"  (read-back property)

**FuzzyItemMatcher**

.. code-block:: python

    matcher = fuzzy_item.FuzzyItemMatcher.from_items(items)
    matched = matcher.match("alfred", threshold=0)

``FuzzyItemMatcher.get_name()`` simply reads
``item.variables.get("fuzzy_match_name")``, so items that have not called
``set_fuzzy_match_name()`` are silently excluded from matching.


The Standard Script Filter Pattern
------------------------------------------------------------------------------

Almost every fuzzy Script Filter in ``afwf.examples`` follows this pattern:

1. Build the full item list unconditionally.
2. If the query is non-empty, run the matcher.
3. Fall back to the full list when there are no matches — the user always
   sees something.

.. literalinclude:: ../../../../afwf/examples/search_bookmarks.py
   :language: python
   :pyobject: main

The fall-back to ``items`` on no match (``matched if matched else items``) is
intentional: an empty result pane is confusing.  Showing the full list lets
the user see what is available even when their query does not hit anything.


When to Use opt.fuzzy vs opt.fuzzy_item
------------------------------------------------------------------------------

Use **opt.fuzzy_item** when your items are already :class:`~afwf.item.Item`
objects destined for Alfred — it requires the least boilerplate.

Use **opt.fuzzy** (base class) when you are matching over a domain type that
is not an ``Item`` — for example, a list of database records or file metadata
objects — and you want to keep the matching logic decoupled from the Alfred
presentation layer.


Installation
------------------------------------------------------------------------------

.. code-block:: bash

    pip install "afwf[fuzzy]"
    # or with uv:
    uv add "afwf[fuzzy]"
