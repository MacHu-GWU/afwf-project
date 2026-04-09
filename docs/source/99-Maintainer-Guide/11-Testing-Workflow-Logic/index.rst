.. _Testing-Workflow-Logic:

Testing Workflow Logic
==============================================================================

Every example in ``afwf/examples/`` has a corresponding test file in
``tests/examples/``.  Because the Python layer is cleanly separated from
Alfred, all tests run with plain ``pytest`` — no Alfred installation required.

This document covers the four patterns used throughout the test suite.


Pattern 1 — run_cov_test: Standalone File Execution with Coverage
------------------------------------------------------------------------------

Every test file ends with an ``if __name__ == "__main__":`` block that runs
the file directly and generates a coverage report for exactly one module:

.. code-block:: python

    if __name__ == "__main__":
        from afwf.tests import run_cov_test

        run_cov_test(
            __file__,
            "afwf.examples.search_bookmarks",
            preview=False,
        )

Running the file as a script (``python tests/examples/test_examples_search_bookmarks.py``)
invokes ``pytest`` as a subprocess, measures coverage for the target module,
and writes ``htmlcov/``.  Setting ``preview=True`` opens the HTML report in a
browser immediately after.

This pattern enables quick iteration: fix a bug in one module, run its test
file directly, see the coverage diff — without running the full suite.

The full suite is run via ``mise run cov``, which collects all test files
and aggregates coverage.


Pattern 2 — Monkeypatching Module-Level State
------------------------------------------------------------------------------

Several modules keep mutable state at module level — a file path, a settings
object, a cache instance.  Tests replace these with ``tmp_path`` variants
using ``monkeypatch.setattr``:

.. code-block:: python

    import afwf.examples.write_file as mod

    def test_creates_file(self, tmp_path, monkeypatch):
        p = tmp_path / "file.txt"
        monkeypatch.setattr(mod, "path_file", p)   # redirect writes to tmp

        mod.write_request("hello")
        assert p.read_text() == "hello"

The key is to patch the attribute *on the module object* (``mod.path_file``),
not on the imported ``Path`` class.  ``monkeypatch.setattr`` restores the
original value automatically after each test.

**Settings store** — ``test_examples_set_settings.py`` patches both the
``settings_mod.settings`` and ``mod.settings`` attributes because the
``settings`` singleton is imported into ``set_settings.py`` at import time:

.. code-block:: python

    def _patch_settings(tmp_path, monkeypatch):
        import afwf.examples.settings as settings_mod

        patched = _JsonSettings(tmp_path / "settings.json")
        monkeypatch.setattr(settings_mod, "settings", patched)
        monkeypatch.setattr(mod, "settings", patched)
        return patched

**Cache instance** — ``test_examples_memoize.py`` replaces both the cache
object and the memoized function (because the decorator was already applied
at import time with the real cache):

.. code-block:: python

    def test_same_key_returns_cached_value(self, tmp_path):
        import afwf.examples.memoize as mod
        from afwf.opt.cache.api import TypedCache

        mod.cache = TypedCache(tmp_path / ".cache")
        mod._get_value = mod.cache.typed_memoize(tag="memoize", expire=5)(
            lambda key: __import__("random").randint(1, 1000)
        )

        v1 = mod._get_value("same_key")
        v2 = mod._get_value("same_key")
        assert v1 == v2


Pattern 3 — Testing log_error via __wrapped__
------------------------------------------------------------------------------

:func:`~afwf.decorator.log_error` uses ``@functools.wraps``, which stores the
original function on ``__wrapped__``.  Tests access this to re-decorate with a
temporary log path, so they can assert that the log file is written without
touching ``~/.alfred-afwf/``:

.. code-block:: python

    def test_error_query_raises_and_logs(self, tmp_path):
        import afwf.examples.search_bookmarks as mod
        from afwf.decorator import log_error

        log_file = tmp_path / "test_error.log"
        patched_main = log_error(log_file=log_file)(mod.main.__wrapped__)

        with pytest.raises(ValueError, match="simulated Python error"):
            patched_main(query="error")

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "ValueError" in content
        assert "simulated Python error" in content

The three assertions check: the log file was created, it contains the
exception type, and it contains the message.  This is sufficient to verify
that the decorator wrote the traceback correctly.


Pattern 4 — Asserting Variables, Not JSON
------------------------------------------------------------------------------

Tests assert on Python object state — ``item.variables``, ``item.arg``,
``item.icon`` — rather than on the serialised JSON string.  This is more
readable and decoupled from serialisation details:

.. code-block:: python

    # Good — assert on the model
    item = sf.items[0]
    assert item.variables["run_script"] == "y"
    assert "write-file-request" in item.arg

    # Avoid — brittle, couples tests to JSON format
    raw = json.dumps(sf.to_script_filter())
    assert '"run_script": "y"' in raw

The serialisation rules are tested separately in
``tests/test_script_filter_object.py``; example tests do not need to re-test them.


What Not to Test
------------------------------------------------------------------------------

- **Alfred widget routing** — Conditional branches, Open URL config, Run Script
  field values — are workflow *configuration*, not Python code.  They are
  verified by running the workflow in Alfred, not by unit tests.
- **``to_script_filter()`` output format** — already covered by
  ``tests/test_script_filter_object.py``.  Example tests should assert on the
  model, not on the raw dict.
- **``uvx`` or Alfred invocation** — integration with Alfred is an end-to-end
  concern.  Unit tests only cover the Python logic layer.
