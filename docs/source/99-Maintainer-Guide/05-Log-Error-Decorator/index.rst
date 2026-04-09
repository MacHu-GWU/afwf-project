.. _log_error-Decorator:

log_error  Decorator
==============================================================================

:func:`~afwf.decorator.log_error` catches any exception raised by the decorated
``main`` function, writes a timestamped traceback to a rotating log file, then
re-raises the exception unchanged.  On the happy path the decorator is fully
transparent — the return value and behaviour of the function are identical to
the unwrapped version.


Why You Need This
------------------------------------------------------------------------------
Alfred Script Filters run inside Alfred's own process.  When your Python code
raises an exception Alfred silently swallows it — the Drop Down Menu goes blank
and there is no traceback visible anywhere.  :func:`~afwf.decorator.log_error`
gives you a persistent, on-disk record of every error so you can open the log
file and see exactly which line failed.


Usage
------------------------------------------------------------------------------

Minimal — write to the default log file ``~/.alfred-afwf/error.log``:

.. code-block:: python

    import afwf.api as afwf

    @afwf.log_error()
    def main(query: str) -> afwf.ScriptFilter:
        ...

Custom log file — useful when a workflow has multiple Script Filters and you
want to keep their error logs separate:

.. code-block:: python

    import afwf.api as afwf

    @afwf.log_error(log_file="~/.alfred-afwf/search_bookmarks.log")
    def main(query: str) -> afwf.ScriptFilter:
        ...

Limit traceback depth — keeps the log compact when call stacks are deep:

.. code-block:: python

    import afwf.api as afwf

    @afwf.log_error(log_file="~/.alfred-afwf/my_workflow.log", tb_limit=5)
    def main(query: str) -> afwf.ScriptFilter:
        ...

Control log rotation — lower ``max_bytes`` for tighter disk budgets:

.. code-block:: python

    import afwf.api as afwf

    @afwf.log_error(
        log_file="~/.alfred-afwf/search_bookmarks.log",
        max_bytes=200_000,
        backup_count=1,
    )
    def main(query: str) -> afwf.ScriptFilter:
        ...


Log Format
------------------------------------------------------------------------------
Each exception appends one entry to the log file::

    [2026-04-08 10:23:45]
    Traceback (most recent call last):
      File ".../search_bookmarks.py", line 33, in main
        raise ValueError("This is a simulated Python error triggered by query='error'")
    ValueError: This is a simulated Python error triggered by query='error'
    ------------------------------------------------------------

The timestamp ``[YYYY-MM-DD HH:MM:SS]`` is followed by the full Python
traceback, and a 60-character separator line is appended so multiple entries
remain easy to tell apart.


Log Rotation
------------------------------------------------------------------------------
:func:`~afwf.decorator.log_error` uses ``logging.handlers.RotatingFileHandler``
under the hood.  Once the active log file exceeds ``max_bytes`` (default
500 000 bytes ≈ 500 KB) it is rotated: the current file is renamed to ``.1``,
the previous ``.1`` becomes ``.2``, and so on.  Files beyond ``backup_count``
(default 2) are deleted automatically.  Total disk usage is bounded at
``max_bytes × (backup_count + 1)``, roughly 1.5 MB with the defaults::

    ~/.alfred-afwf/search_bookmarks.log     ← current (newest)
    ~/.alfred-afwf/search_bookmarks.log.1
    ~/.alfred-afwf/search_bookmarks.log.2   ← oldest, deleted on next rotation

The handler is thread-safe and initialised lazily — no file I/O occurs on the
happy path, so there is no measurable overhead per ``uvx`` invocation.


Full Example
------------------------------------------------------------------------------
The following is the complete ``afwf/examples/search_bookmarks.py``.  Passing
``query="error"`` deliberately raises an exception so you can verify that the
log file is written correctly:

.. literalinclude:: ../../../../afwf/examples/search_bookmarks.py
   :language: python
