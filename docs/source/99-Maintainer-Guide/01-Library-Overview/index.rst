.. _Library-Overview:

Library Overview
==============================================================================

``afwf`` is a Python framework for building Alfred Workflows. This document gives a high-level picture of what the library does. Each point is covered in depth in a dedicated document.


Script Filter JSON Data Model
------------------------------------------------------------------------------

Alfred's Script Filter expects a specific JSON structure. ``afwf`` provides typed Python classes — :class:`~afwf.item.Item`, :class:`~afwf.item.Icon`, :class:`~afwf.item.Text`, :class:`~afwf.script_filter.ScriptFilter` — that map directly onto that spec. You build the response as objects and call ``to_script_filter()`` to serialize, instead of constructing raw dicts by hand.


Semantic Variables for Follow-up Actions
------------------------------------------------------------------------------

Alfred's `Conditional widget <https://www.alfredapp.com/help/workflows/utilities/conditional/>`_ can branch on item variables. ``afwf`` defines a set of semantic variable keys and values (see :class:`~afwf.constants.VarKeyEnum`, :class:`~afwf.constants.VarValueEnum`) so that each :class:`~afwf.item.Item` can declare its intended follow-up action — open a URL, open a file, run a script, etc. — directly in code. The Conditional widget in Alfred reads those variables and routes accordingly, keeping the Workflow diagram static while the behavior is controlled entirely from Python.


Developer-Friendly Utilities
------------------------------------------------------------------------------

The library ships a small set of helpers that reduce boilerplate in common situations:

- :func:`~afwf.decorator.log_error` — a decorator that catches exceptions inside a handler, writes the traceback to ``~/.alfred-afwf/last-error.txt``, and returns a fallback :class:`~afwf.script_filter.ScriptFilter` with debug items instead of crashing silently.
- :class:`~afwf.query.QueryParser` — a configurable tokenizer for parsing Alfred's raw query string into structured parts.
- :class:`~afwf.workflow.Workflow` — a multi-handler entry point with built-in error handling and invocation logging (pre-uvx deployment model).


Optional Workflow Utilities
------------------------------------------------------------------------------

``afwf.opt`` contains modules that are useful in many workflows but not required by the core:

- **Fuzzy item matching** (``afwf.opt.fuzzy_item``) — ranks a list of :class:`~afwf.item.Item` objects against a query string using `rapidfuzz <https://pypi.org/project/rapidfuzz/>`_.
- **Typed disk cache** (``afwf.opt.cache``) — a thin wrapper around `diskcache <https://pypi.org/project/diskcache/>`_ for persisting results between Alfred invocations.

These are installed via extras (``pip install afwf[fuzzy]``, ``pip install afwf[cache]``).


Built-in Examples
------------------------------------------------------------------------------

``afwf.examples`` contains working Script Filter implementations built with this framework. They serve as reference code for workflow developers learning the patterns. Each example is also wired into a CLI entry point so it can be run and inspected directly without Alfred.


Deployment Model: fire + uvx
------------------------------------------------------------------------------

The recommended deployment model avoids placing any Python source or virtualenv inside the Alfred workflow directory. Instead:

1. Workflow logic is published as a normal PyPI package.
2. Each Script Filter is exposed as a subcommand of a `fire <https://github.com/google/python-fire>`_ CLI.
3. Alfred's Script field calls the package via `uvx <https://docs.astral.sh/uv/guides/tools/>`_, which downloads, caches, and runs the pinned version on demand.

This means no virtualenv to maintain, no path hardcoding, and no per-machine setup. Upgrading a workflow is a version bump in PyPI and a one-line change in Alfred.
