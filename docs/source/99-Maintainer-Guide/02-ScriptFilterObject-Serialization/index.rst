.. _ScriptFilterObject-Serialization:

ScriptFilterObject: Serialization Rules
==============================================================================

Every object in an Alfred Script Filter JSON payload — :class:`~afwf.item.Item`,
:class:`~afwf.item.Icon`, :class:`~afwf.item.Text`, :class:`~afwf.script_filter.ScriptFilter`
— inherits from :class:`~afwf.script_filter_object.ScriptFilterObject`.

The base class provides a single method: :meth:`~afwf.script_filter_object.ScriptFilterObject.to_script_filter`.
This method serialises the object to a plain ``dict`` that Alfred can consume.
It exists because Alfred's JSON protocol differs from standard Python serialisation
in several ways that a naïve ``model_dump()`` or ``asdict()`` call would get wrong.


Why Not model_dump()
------------------------------------------------------------------------------

Pydantic's ``model_dump()`` emits ``null`` for ``None`` fields, collapses
``False`` / ``0`` / ``""`` identically to absent keys when
``exclude_none=True`` is used, and recurses uniformly into all nested objects.
Alfred's protocol requires different treatment for each of these cases.
``to_script_filter()`` implements the exact rules Alfred expects.


The Six Rules
------------------------------------------------------------------------------

Rule 1 — ``None`` means absent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alfred interprets a *missing* key as "use default behaviour". Sending
``"subtitle": null`` is not equivalent — it is an unexpected value that some
Alfred versions may mishandle. Every field whose Python value is ``None``
is simply omitted from the output dict.

.. code-block:: python

    item = Item(title="hello")          # subtitle is None
    item.to_script_filter()
    # → {"title": "hello", "valid": True}
    # "subtitle" key is absent entirely


Rule 2 — Falsy primitives are preserved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``False``, ``0``, and ``""`` are falsy in Python but carry real meaning in
Alfred's protocol. The most important case: if ``valid`` is absent, Alfred
defaults to ``True``. Sending ``valid=False`` **must** appear in the output.
A naïve ``if v:`` falsy-filter would silently drop it — a hard-to-diagnose bug.

.. code-block:: python

    item = Item(title="disabled", valid=False)
    item.to_script_filter()
    # → {"title": "disabled", "valid": False}   ← False preserved


Rule 3 — Empty nested objects are absent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A :class:`~afwf.item.Text` with no fields set serialises to ``{}``.
Sending ``"text": {}`` to Alfred is noise and may confuse some Alfred versions.
``to_script_filter()`` calls itself recursively on nested
``ScriptFilterObject`` instances and omits the key when the result is empty.

.. code-block:: python

    item = Item(title="hello", text=Text())     # Text() → {}
    item.to_script_filter()
    # → {"title": "hello", "valid": True}
    # "text" key is absent


Rule 4 — Empty top-level ``dict`` fields are absent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``variables: dict = {}`` on an ``Item`` means "no variables" — identical to
the key being absent. Alfred ignores both. An empty top-level ``dict`` is omitted.

.. code-block:: python

    item = Item(title="hello")                  # variables defaults to {}
    item.to_script_filter()
    # → {"title": "hello", "valid": True}
    # "variables" key is absent


Rule 5 — ``variables: {}`` *inside* ``mods`` is preserved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Alfred distinguishes between a mod entry *without* a ``variables`` key
(the mod inherits the item's variables) and a mod *with* ``"variables": {}``
(the mod explicitly clears that inheritance). This matters when you want a
modifier key to have a completely independent action.

Rule 4 therefore applies **only** to top-level ``ScriptFilterObject`` fields.
Plain ``dict`` values — such as the entries inside ``mods`` — are passed
through as-is without any recursive stripping.

.. code-block:: python

    item = Item(title="hello")
    item.mods = {"cmd": {"variables": {}}}      # intentional empty variables
    item.to_script_filter()
    # → {"title": "hello", "valid": True, "mods": {"cmd": {"variables": {}}}}
    # "variables": {} inside mods is preserved


Rule 6 — ``list`` fields are always preserved
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`~afwf.script_filter.ScriptFilter` must always return an ``items``
array — even ``[]`` — because Alfred expects the key to be present.
List fields are never omitted regardless of their content.

.. code-block:: python

    sf = ScriptFilter()                         # items defaults to []
    sf.to_script_filter()
    # → {"items": []}                           ← empty list preserved


Alias Handling
------------------------------------------------------------------------------

Some fields use a Pydantic alias because their natural Alfred JSON key is a
Python reserved word. :class:`~afwf.item.Text` stores the clipboard-copy text
as ``copy_text`` in Python (``alias="copy"``).
``to_script_filter()`` writes the *alias* as the JSON key:

.. code-block:: python

    text = Text(copy_text="copy me")
    text.to_script_filter()
    # → {"copy": "copy me"}


Summary Table
------------------------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Python value
     - Output
   * - ``None``
     - Field omitted (Rule 1)
   * - ``False`` / ``0`` / ``""``
     - Value preserved as-is (Rule 2)
   * - Nested ``ScriptFilterObject`` → ``{}``
     - Field omitted (Rule 3)
   * - Top-level ``dict`` that is ``{}``
     - Field omitted (Rule 4)
   * - ``dict`` nested inside another ``dict`` (e.g. inside ``mods``)
     - Passed through unchanged (Rule 5)
   * - ``list`` (any length)
     - Value preserved as-is (Rule 6)


Tests
------------------------------------------------------------------------------

Each rule has a dedicated test case in ``tests/test_script_filter_object.py``.
Running that file standalone also generates a coverage report for
``afwf.script_filter_object``:

.. code-block:: bash

    python tests/test_script_filter_object.py
