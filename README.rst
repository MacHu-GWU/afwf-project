.. image:: https://readthedocs.org/projects/afwf/badge/?version=latest
    :target: https://afwf.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/afwf-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/afwf-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf-project

.. image:: https://img.shields.io/pypi/v/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/pypi/l/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/pypi/pyversions/afwf.svg
    :target: https://pypi.python.org/pypi/afwf

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/afwf-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/afwf-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://afwf.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/afwf#files


Welcome to ``afwf`` Documentation
==============================================================================
.. image:: https://afwf.readthedocs.io/en/latest/_static/afwf-logo.png
    :target: https://afwf.readthedocs.io/en/latest/

A powerful framework enables fast and elegant development of Alfred Workflows in Python.


What's New in 1.0.2 (2026-04-21)
------------------------------------------------------------------------------

Version 1.0.2 is a milestone release. It completely drops the old, complex workflow
development model in favour of modern Python practices: write pure functions, run them
locally, and they work in Alfred out of the box — no adapters, no scaffolding, no glue
code. Combined with ``uvx`` for zero-install deployment, the gap between a working Python
function and a shipping Alfred workflow has never been smaller.


Project Background
------------------------------------------------------------------------------
The `official Alfred Python library <https://www.deanishe.net/alfred-workflow/>`_ had not
been updated for years and only supported Python 2.7 — a version that reached end-of-life
in January 2020 and was removed from macOS in 2021. This left every workflow built on that
library broken on modern Macs. The library also suffered from heavy coupling: it bundled HTTP
clients, caching, and other concerns that belong in dedicated third-party packages, producing
layers of workarounds on top of outdated code.

At the same time, I personally maintain more than a dozen Alfred workflows across different
domains. Early on, each project contained large amounts of boilerplate unrelated to business
logic — Alfred integration glue, test scaffolding, and meta-programming code duplicated
across every repo. Extracting that into a reusable framework became the obvious next step.

``afwf`` provides:

- A clean Python data model for Alfred's Script Filter JSON protocol, built on Pydantic.
- A fluent ``Item`` API with action helpers (``open_url``, ``run_script``,
  ``send_notification``, …) that wire directly to Alfred's Conditional widget.
- Optional fuzzy-matching (``afwf[fuzzy]``) and disk-caching (``afwf[cache]``) extras.
- A deployment pattern — publish to PyPI, expose via ``fire`` CLI, invoke with ``uvx`` —
  that eliminates dependency management on the end-user machine.
- Best practices for development, testing, and release derived from building the official
  AWS internal Alfred Workflow (one of the largest Alfred workflow codebases in existence).

The library also ships ~50 bundled PNG icons commonly used in productivity workflows.
`Preview all icons <https://github.com/MacHu-GWU/afwf-project/blob/main/preview-icons.rst>`_.


Core Modules
------------------------------------------------------------------------------

Script Filter JSON Protocol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alfred Script Filters communicate via a `JSON protocol <https://www.alfredapp.com/help/workflows/inputs/script-filter/json/>`_. These modules implement it:

- ``afwf/script_filter_object.py`` — ``ScriptFilterObject``: Pydantic base class; ``to_script_filter()`` serialises to Alfred-compatible dict (handles None-omission, False-preservation, empty-object rules).
- ``afwf/item.py`` — ``Icon``, ``Text``, ``Item``: Alfred dropdown item model; ``Item`` has fluent ``set_*`` helpers (``open_url``, ``run_script``, ``open_file``, ``send_notification``, etc.) that set workflow variable pairs.
- ``afwf/script_filter.py`` — ``ScriptFilter``: Top-level response object; holds ``items`` list; ``send_feedback()`` dumps JSON to stdout.

Query Parsing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``afwf/query.py`` — ``Query``, ``QueryParser``: Utility for parsing the raw Alfred ``{query}`` string into structured tokens.

.. code-block:: python

    import afwf.api as afwf

    q = afwf.Query.from_str("  hello   world  ")
    q.trimmed_parts   # ['hello', 'world']
    q.n_trimmed_parts # 2

    parser = afwf.QueryParser.from_delimiter([" ", "/"])
    q = parser.parse("foo/bar baz")
    q.trimmed_parts   # ['foo', 'bar', 'baz']

Constants & Icons
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``afwf/constants.py`` — ``IconTypeEnum``, ``ItemTypeEnum``, ``ModEnum``, ``VarKeyEnum``, ``VarValueEnum``: All Alfred protocol string constants.
- ``afwf/icon.py`` — ``IconFileEnum``: Paths to ~50 bundled PNG icons (search, folder, star, git, error, …). `Preview all icons <https://github.com/MacHu-GWU/afwf-project/blob/main/preview-icons.rst>`_.

Error Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``afwf/decorator.py`` — ``log_error``: Decorator factory that silently logs exceptions to a rotating file so Alfred's UI never shows a raw Python traceback.

.. code-block:: python

    import afwf.api as afwf

    @afwf.log_error()
    def main(query: str) -> afwf.ScriptFilter:
        ...

    # Custom log file and size limit
    @afwf.log_error(log_file="~/.alfred-afwf/search.log", max_bytes=200_000)
    def main(query: str) -> afwf.ScriptFilter:
        ...

Alfred Introspection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``afwf/alfred/workflow.py`` — ``AlfredWorkflow``: Represents a single Alfred Workflow directory; lazily reads ``info.plist`` to expose ``name``, ``bundle_id``, ``version``, ``description``, and more.
- ``afwf/alfred/prefs.py`` — ``AlfredPreferences``: Locates the Alfred preferences folder and enumerates installed workflows.
- ``afwf/project/project.py`` — ``AfwfProject``: Binds a Python source project to its corresponding Alfred Workflow folder; exposes paths for ``main.py``, ``lib/``, ``info.plist``, and ``icon.png`` on both sides.

Optional Utilities (``afwf/opt/``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``afwf/opt/cache/`` — ``TypedCache``: ``diskcache``-backed disk cache with a type-hint-safe ``typed_memoize()`` decorator. Install with ``afwf[cache]``.
- ``afwf/opt/fuzzy/`` — ``FuzzyMatcher``: Generic fuzzy matcher over any item type using ``rapidfuzz``; subclass and implement ``get_name()``. Install with ``afwf[fuzzy]``.
- ``afwf/opt/fuzzy_item/`` — ``Item``, ``FuzzyItemMatcher``: ``Item`` subclass that stores a fuzzy-match name in ``variables``; wires directly to ``FuzzyMatcher``.


Quickstart
------------------------------------------------------------------------------

A minimal Script Filter handler:

.. code-block:: python

    import afwf.api as afwf

    @afwf.log_error()
    def main(query: str) -> afwf.ScriptFilter:
        q = afwf.Query.from_str(query)
        sf = afwf.ScriptFilter()
        item = afwf.Item(title="Hello", subtitle=f"You typed: {q.raw}")
        item.open_url(url="https://example.com")
        sf.items.append(item)
        return sf

    if __name__ == "__main__":
        import fire
        fire.Fire({"search": lambda query="": main(query).send_feedback()})

Deployment Pattern (Best Practice)
------------------------------------------------------------------------------

Publish your workflow logic as a Python package on PyPI, expose it as a CLI using `fire <https://github.com/google-deepmind/python-fire>`_, then invoke it from Alfred's Script Filter via ``uvx``:

.. code-block:: bash

    # Development / local
    ~/Documents/GitHub/my-workflow-project/.venv/bin/my-workflow search --query '{query}'

    # Production (no install required on end-user machine)
    ~/.local/bin/uvx --from my-workflow==1.0.0 my-workflow search --query '{query}'

The ``afwf-examples`` CLI bundled in this repo demonstrates all built-in example handlers:

.. code-block:: bash

    afwf-examples search-bookmarks --query 'git'
    afwf-examples open-file
    afwf-examples read-file
    afwf-examples write-file --query 'hello'
    afwf-examples view-settings
    afwf-examples set-settings --query 'theme'
    afwf-examples memoize --query 'test'


AI-Assisted Development (Claude Code Agent Skill)
------------------------------------------------------------------------------

This repo ships a **Claude Code Agent Skill** under ``.claude/skills/afwf/``.

The Skill is a self-contained reference guide written for AI assistants. Hand it to any
AI that supports the Skill mechanism (such as Claude Code) and the AI instantly knows how
to build Alfred workflows with ``afwf``, covering:

- How to write a Script Filter handler (``main(query) → ScriptFilter``)
- Mapping CLI entry points (``fire.Fire``) to Alfred's Script field
- Every ``Item`` action method (``open_url``, ``run_script``, ``send_notification``, …)
- Query parsing, fuzzy matching (``afwf[fuzzy]``), and disk caching (``afwf[cache]``)
- The two-phase write-action pattern (run_script + send_notification)
- Unit testing patterns — no Alfred required, plain pytest
- Local dev and ``uvx`` production deployment

**Directory layout:**

.. code-block:: text

    .claude/skills/afwf/
    ├── SKILL.md                          # Main Skill file — the AI reference manual
    └── ref/
        ├── script-filter-json-format.md  # Alfred Script Filter JSON protocol spec
        └── script-filter-input.md        # Alfred Script Filter input format reference

**Activating in Claude Code:**

Type ``/afwf`` in the conversation. Claude Code loads the Skill and from that point on
you can describe what you want in plain English — the AI will generate complete,
ready-to-run ``afwf`` code following best practices.

.. code-block:: text

    You:    /afwf Write a Script Filter that fuzzy-searches a hardcoded list of bookmarks
    Claude: [Skill loaded → generates complete afwf-idiomatic code]

.. note::

    The Skill file is plain Markdown and does **not** require Claude Code. Paste the
    contents of ``SKILL.md`` into the system prompt (or first message) of any AI chat
    and it will understand and correctly use ``afwf`` in the same way.


.. _install:

Install
------------------------------------------------------------------------------
``afwf`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install afwf

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade afwf

Optional extras:

.. code-block:: console

    # Fuzzy matching (rapidfuzz)
    $ pip install "afwf[fuzzy]"

    # Disk caching (diskcache)
    $ pip install "afwf[cache]"

    # Both
    $ pip install "afwf[fuzzy,cache]"
