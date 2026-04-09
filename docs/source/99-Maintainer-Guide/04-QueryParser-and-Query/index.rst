.. _QueryParser-and-Query:

QueryParser and Query
==============================================================================

Alfred passes the Script Filter a single raw string — whatever the user has
typed after the keyword trigger. For simple handlers this string can be used
directly. For multi-step interactions, where the meaning of the input depends
on how many words have been typed, you need to tokenise it first.

:class:`~afwf.query.QueryParser` and :class:`~afwf.query.Query` handle this
tokenisation.


Basic Usage
------------------------------------------------------------------------------

The quickest way to parse a query string is :meth:`~afwf.query.Query.from_str`,
which uses the default space-delimited parser:

.. code-block:: python

    import afwf.api as afwf

    q = afwf.Query.from_str("  hello   world  ")
    q.parts           # ["", "", "hello", "", "", "world", "", ""]  (raw split)
    q.trimmed_parts   # ["hello", "world"]                          (empty parts removed)
    q.n_trimmed_parts # 2


``parts`` vs ``trimmed_parts``
------------------------------------------------------------------------------

``parts`` is the direct result of splitting on the delimiter — it preserves
empty strings produced by leading, trailing, or consecutive delimiters.

``trimmed_parts`` strips whitespace from each part and removes empty strings.
This is what you almost always want when branching on the number of tokens:

.. code-block:: python

    q = afwf.Query.from_str("")
    q.n_trimmed_parts   # 0  → show default list

    q = afwf.Query.from_str("username")
    q.n_trimmed_parts   # 1  → fuzzy-filter by key

    q = afwf.Query.from_str("username alice")
    q.n_trimmed_parts   # 2  → show confirmation item


Custom Delimiters
------------------------------------------------------------------------------

Use :meth:`~afwf.query.QueryParser.from_delimiter` when you need to split on
something other than a space, or on multiple delimiters at once:

.. code-block:: python

    parser = afwf.QueryParser.from_delimiter("/")
    q = parser.parse("2026/04/08")
    q.trimmed_parts   # ["2026", "04", "08"]

    parser = afwf.QueryParser.from_delimiter([" ", ","])
    q = parser.parse("a, b, c")
    q.trimmed_parts   # ["a", "b", "c"]


The Multi-Step Interaction Pattern
------------------------------------------------------------------------------

The most common use of ``Query`` is branching a Script Filter's behaviour on
``n_trimmed_parts``. The ``set_settings`` example demonstrates the three
states a two-word handler typically has:

.. literalinclude:: ../../../../afwf/examples/set_settings.py
   :language: python
   :pyobject: main

The branch logic reads naturally:

- **0 words** — the user has not typed anything; show all available options.
- **1 word** — the user is narrowing down; fuzzy-filter the option list.
- **2+ words** — the user has selected a key and is entering a value;
  show a confirmation item with the action pre-built.

This pattern keeps each Script Filter invocation stateless: the full context
(key and value) is re-parsed from the query string on every keystroke.


``trimmed_parts`` Index Access
------------------------------------------------------------------------------

After checking ``n_trimmed_parts``, index into ``trimmed_parts`` directly:

.. code-block:: python

    q = afwf.Query.from_str("username alice bob")

    key   = q.trimmed_parts[0]          # "username"
    value = " ".join(q.trimmed_parts[1:])  # "alice bob"

This is safe because you have already verified ``n_trimmed_parts >= 2`` before
reaching this branch.
