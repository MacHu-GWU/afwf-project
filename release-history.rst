.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.2 (2026-04-21)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Exposed ``AlfredWorkflow``, ``AlfredPreferences``, and ``AfwfProject`` in the top-level ``afwf.api`` module so they are accessible via ``import afwf.api as afwf``.
- Reorganised documentation structure: renamed and renumbered doc chapters for better clarity.

**Bugfixes**

- Fix missing ``afwf/icons/`` PNG files in the published package by adding ``[tool.setuptools.package-data]`` to ``pyproject.toml``.


1.0.1 (2026-04-07)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**💥 Breaking Change**

- Removed ``attrs`` / ``attrs_mate`` as dependencies. All core models (``Item``, ``Text``, ``Icon``, ``ScriptFilter``, ``Handler``, ``Workflow``) have been fully rewritten using **Pydantic v2**.
- ``Item.copy`` field renamed to ``copy_text`` (serialized as ``"copy"`` via field alias) to avoid shadowing Pydantic's ``BaseModel.copy`` method.

**Features and Improvements**

- Introduced :mod:`afwf.constants` module that centralises all Alfred Script Filter protocol string constants (``IconTypeEnum``, ``ItemTypeEnum``, ``ModEnum``, ``VarKeyEnum``, ``VarValueEnum``).
- Added ``enum-mate`` as a core dependency to power the new enum utilities.
- Fuzzy matching (``afwf.opt.fuzzy``) migrated to ``rapidfuzz``; fuzzy-item now stores the match name in ``variables`` under ``FUZZY_MATCH_NAME_VAR_KEY`` for cleaner downstream handling.
- ``ScriptFilterObject.to_script_filter()`` now respects field aliases when serialising to JSON, so aliased fields round-trip correctly.
- Replaced the network-dependent ``python_version`` example handler with a self-contained ``source_files`` example that works offline.
- ``fuzzy`` and ``cache`` optional dependency groups are now declared in ``pyproject.toml`` (``pip install afwf[fuzzy]``, ``pip install afwf[cache]``).
- Switched project toolchain to **mise** + **uv**; legacy ``requirements*.txt`` / ``setup.py`` / ``tox.ini`` removed.

**Minor Improvements**

- Enriched docstrings and type annotations across ``item.py``, ``handler.py``, ``workflow.py``, and ``script_filter.py``.
- Added ``tests/opt/test_opt_api.py`` smoke test for the optional-extras public API.
- Sphinx API reference pages auto-generated for all public modules under ``docs/source/api/``.

**Miscellaneous**

- Added ``mise`` task runner configuration (``mise.toml``) with tasks for install, test, coverage, doc-build, and release.


0.6.1 (2024-01-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Improve the :class:`afwf.query.QueryParser` and :class:`afwf.query.Query`

**Minor Improvements**

- Improve the ``Afwf Framework Overview`` document.

**Miscellaneous**

- Use ``afwf_ops`` for DevOps automation.


0.5.2 (2023-12-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix bug that 0.5.1 forget to include icons in the package release.


0.5.1 (2023-12-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**💥 Breaking Change**

- Drop support for Python < 3.7 due to the attrs now only support 3.7+.

**Minor Improvements**

- use version range in ``requirements.txt``.
- add maintainer guide document.
- use ``pyproject_ops`` code skeleton.
- use ``attrs`` modern API.


0.4.1 (2023-04-10)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add the ``afwf.opt`` modules. It stores lots of optional utility tools
- add the :mod:`afwf.opt.cache` module.
- add the :mod:`afwf.opt.fuzzy` module.
- add the :mod:`afwf.opt.fuzzy_item` module.

**Minor Improvements**

- now all of :meth:`afwf.item.Item.open_file`, :meth:`afwf.item.Item.open_url`, ..., method returns the :class:`afwf.item.Item` object itself, so you can chain them together.


0.3.2 (2023-04-08)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Miscellaneous**

- add lot more icons.


0.3.1 (2023-04-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add tons of doc string and unit test.

**Minor Improvements**

- Add documentation website.


0.2.2 (2023-01-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix a bug that ``run_script()`` and ``terminal_command()`` should set the command to item arguments.


0.2.1 (2023-01-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add more abstract method to ``Handler`` class.
- add public API to unit test.


0.1.1 (2023-01-29)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Determine the list of public API.


0.0.4 (2022-07-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- fix a bug that in ``workflow.py``, the ``mkdir_if_not_exist()`` method not exists.


0.0.3 (2022-04-13)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- The first working version


0.0.2 (2022-03-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Prepare for pip installable


0.0.1 (2022-02-24)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Place Holder Release
