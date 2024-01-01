.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


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
