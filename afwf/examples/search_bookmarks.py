# -*- coding: utf-8 -*-

from afwf.script_filter import ScriptFilter
from afwf.opt.fuzzy_item.api import Item, FuzzyItemMatcher

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


def main(query: str) -> ScriptFilter:
    items = []
    for title, url in BOOKMARKS:
        item = Item(title=title, subtitle=url, arg=url)
        item.set_fuzzy_match_name(title)
        items.append(item)

    if query.strip():
        matcher = FuzzyItemMatcher.from_items(items)
        matched = matcher.match(query, threshold=0)
        result_items = matched if matched else items
    else:
        result_items = items

    sf = ScriptFilter()
    sf.items.extend(result_items)
    return sf
