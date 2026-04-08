# -*- coding: utf-8 -*-

"""
Example: Search Bookmarks
=========================

**What it demonstrates**

Shows how to build a fuzzy-search Script Filter using
:mod:`afwf.opt.fuzzy_item`.  A static list of bookmarks is turned into
:class:`afwf.opt.fuzzy_item.Item` objects; when the user types a query the
list is narrowed with :class:`afwf.opt.fuzzy_item.FuzzyItemMatcher`.  If no
fuzzy match is found the full list is returned so the user always sees
results.  Selecting an item opens the URL in the default browser via the
``open_url`` variable pair.  Type ``error`` as the query to trigger a
simulated error and see how :func:`afwf.log_error` writes a traceback to a
log file.

**Alfred Workflow setup**

+---------------------------+----------------------------------------------------+
| Field                     | Value                                              |
+===========================+====================================================+
| Keyword                   | ``afwf-example-search-bookmarks``                  |
|                           | (Argument Optional)                                |
+---------------------------+----------------------------------------------------+
| Language                  | ``/bin/bash``                                      |
+---------------------------+----------------------------------------------------+
| Script                    | ``python main.py 'search_bookmarks {query}'``      |
+---------------------------+----------------------------------------------------+
| Alfred filters results    | unchecked (filtering is done in Python)            |
+---------------------------+----------------------------------------------------+
"""

import afwf.api as afwf
import afwf.opt.fuzzy_item.api as fuzzy_item

BOOKMARKS = [
    ("Alfred App", "https://www.alfredapp.com/"),
    ("Python", "https://www.python.org/"),
    ("GitHub", "https://github.com/"),
    ("Stack Overflow", "https://stackoverflow.com/"),
    ("MDN Web Docs", "https://developer.mozilla.org/"),
    ("PyPI", "https://pypi.org/"),
    ("Read the Docs", "https://readthedocs.org/"),
    ("Hacker News", "https://news.ycombinator.com/"),
    ("Wikipedia", "https://www.wikipedia.org/"),
    ("Google", "https://www.google.com/"),
    ("YouTube", "https://www.youtube.com/"),
    ("Twitter / X", "https://twitter.com/"),
    ("Reddit", "https://www.reddit.com/"),
    ("AWS Console", "https://console.aws.amazon.com/"),
    ("Docker Hub", "https://hub.docker.com/"),
    ("Homebrew", "https://brew.sh/"),
    ("VS Code Docs", "https://code.visualstudio.com/docs"),
    ("Real Python", "https://realpython.com/"),
    ("Anthropic Claude", "https://claude.ai/"),
    ("OpenAI", "https://openai.com/"),
]


@afwf.log_error(
    log_file=afwf.path_enum.dir_home.joinpath(
        ".alfred-afwf/search_bookmarks.log"
    ),  # or just @log_error()
)
def main(query: str) -> afwf.ScriptFilter:
    if query.strip() == "error":
        raise ValueError("This is a simulated Python error triggered by query='error'")

    items = []
    for title, url in BOOKMARKS:
        item = fuzzy_item.Item(title=title, subtitle=url, arg=url)
        item.set_fuzzy_match_name(title)
        item.open_url(url)
        items.append(item)

    if query.strip():
        matcher = fuzzy_item.FuzzyItemMatcher.from_items(items)
        matched = matcher.match(query, threshold=0)
        result_items = matched if matched else items
    else:
        result_items = items

    sf = afwf.ScriptFilter()
    sf.items.extend(result_items)
    return sf
