.. _Pattern-Read-Only-Script-Filters:

Pattern: Read-Only Script Filters
==============================================================================

A *read-only* Script Filter returns items for the user to inspect or act on,
but the action is performed by Alfred's built-in widgets (open a URL, open a
file) rather than by running additional Python code.  The ``main()`` function
only *builds* the response; it never writes to disk or makes network calls at
action time.

The example workflow contains four read-only Script Filters, each illustrating
a distinct sub-pattern.


search-bookmarks: Python-Side Fuzzy Filtering
------------------------------------------------------------------------------

**Keyword:** ``afwf-search-bookmarks``

**Script:** ``afwf-examples search-bookmarks --query '{query}'``

**What it does:** Maintains a static bookmark list.  On every keystroke Alfred
passes the current query to Python, which narrows the list with
:class:`~afwf.opt.fuzzy_item.impl.FuzzyItemMatcher` and returns the filtered
items.  Selecting an item opens the URL in the default browser.

.. literalinclude:: ../../../../afwf/examples/search_bookmarks.py
   :language: python

Key points:

- Each item calls ``item.open_url(url)`` to set the ``open_url`` / ``open_url_arg``
  variable pair (see :doc:`../03-Item-Variables-Conditional-Widget/index`).
- ``argumenttype: 1`` (required) in ``info.plist`` — Alfred always passes the
  query, even when empty.
- When no fuzzy match is found, the full list is returned so the pane is never
  empty.
- Typing ``error`` raises a deliberate exception to demonstrate
  :func:`~afwf.decorator.log_error`.

**Downstream widgets** (from ``info.plist``)::

    Script Filter ──► Conditional (open_url=y)  ──► Open URL  {var:open_url_arg}
                  └──► Conditional (_open_log_file=y) ──► Open File  {var:_open_log_file_path}


open-file: Alfred-Side Filtering via the match Field
------------------------------------------------------------------------------

**Keyword:** ``afwf-open-file``

**Script:** ``afwf-examples open-file``  *(no query argument)*

**What it does:** Lists every ``.py`` file in ``afwf/examples/`` and lets
Alfred filter the list interactively as the user types.  Selecting an item
opens the file with the system default application.

.. literalinclude:: ../../../../afwf/examples/open_file.py
   :language: python

Key points:

- ``argumenttype: 2`` (no argument) in ``info.plist`` — the script receives no
  query string.  It always returns the full file list.
- Each item sets ``item.match = p.basename`` and ``item.autocomplete = p.basename``.
  Alfred uses the ``match`` field for its own client-side filtering, narrowing
  the displayed list as the user types without re-invoking the script.
- Each item calls ``item.open_file(path=p.abspath)`` to set the ``open_file`` /
  ``open_file_path`` variable pair.

**When to choose Alfred-side filtering:** Use it when the full item list is
small, static, or cheap to produce, and you do not need Python-side logic to
decide what to show.  The script runs once; Alfred handles the rest.

**Downstream widgets** (from ``info.plist``)::

    Script Filter ──► Conditional (open_file=y) ──► Open File  {var:open_file_path}


read-file: Conditional Item Display
------------------------------------------------------------------------------

**Keyword:** ``afwf-read-file``

**Script:** ``afwf-examples read-file``  *(no query argument)*

**What it does:** Reads ``~/.alfred-afwf/file.txt`` and displays its content as
a subtitle.  If the file does not exist, an error item with the error icon is
shown instead.

.. literalinclude:: ../../../../afwf/examples/read_file.py
   :language: python

Key points:

- The handler branches on a file-existence condition and returns a different
  item in each case — a common pattern for Script Filters that depend on
  external state that may not yet exist.
- :func:`~afwf.icon.IconFileEnum` provides bundled icons; ``IconFileEnum.error``
  gives a consistent visual cue for failure states.
- This Script Filter is intentionally read-only — it has no downstream action
  widget.  The item is for display only; pressing Enter does nothing meaningful.
- Designed to work alongside ``write-file``: write something with
  ``afwf-write-file``, then confirm with ``afwf-read-file``.


memoize: Disk-Cached Computation
------------------------------------------------------------------------------

**Keyword:** ``afwf-memoize``

**Script:** ``afwf-examples memoize --query '{query}'``

**What it does:** Generates a random integer for the given query key and caches
it for 5 seconds.  Repeated queries with the same key return the cached value
without re-running the function.

.. literalinclude:: ../../../../afwf/examples/memoize.py
   :language: python

Key points:

- ``cache = TypedCache(path_enum.dir_afwf / ".cache")`` is a module-level
  singleton.  It is created once when the module is imported and reused across
  Alfred invocations (each ``uvx`` call is a fresh process, so the cache
  persists on disk between calls).
- ``@cache.typed_memoize(tag="memoize", expire=5)`` decorates the inner
  function, not ``main()``.  Only the expensive computation is cached; the
  ``ScriptFilter`` assembly runs on every call.
- This Script Filter has no downstream action widget.  It demonstrates caching
  behaviour, not a user-facing action.

**Observing the cache:** Call ``afwf-memoize hello`` twice within 5 seconds —
the integer stays the same.  Wait 6 seconds — it changes.
