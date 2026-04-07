# -*- coding: utf-8 -*-

"""
Example handler: fuzzy-search Python source files in the afwf package.

Used as a self-contained integration test fixture — no network access required.
Each item represents one ``.py`` file; its title is the path relative to the
project root using ``/`` separators (e.g. ``afwf/handler.py``).
"""

from pathlib import Path

from afwf.handler import Handler as BaseHandler
from afwf.script_filter import ScriptFilter
from afwf.item import Item
from afwf.paths import path_enum


def _collect_source_files() -> list[str]:
    """
    Return sorted list of all ``.py`` file paths inside the ``afwf`` package,
    relative to the project root, using ``/`` as the separator.

    Example output entries::

        afwf/__init__.py
        afwf/handler.py
        afwf/item.py
        afwf/opt/fuzzy/impl.py
    """
    root = path_enum.dir_project_root
    pkg = root / "afwf"
    files = []
    for p in sorted(pkg.rglob("*.py")):
        if "__pycache__" not in p.parts:
            rel = p.relative_to(root)
            files.append("/".join(rel.parts))
    return files


class Handler(BaseHandler):
    def get_all_files(self) -> list[str]:
        """
        Return all ``.py`` source file paths in the afwf package.
        """
        return _collect_source_files()

    def main(
        self,
        query: str,
    ) -> ScriptFilter:
        files = self.get_all_files()
        matched = [f for f in files if query in f] if query else files
        matched = matched[:50]
        sf = ScriptFilter()
        for rel_path in matched:
            abs_path = str(path_enum.dir_project_root / Path(rel_path))
            item = Item(
                title=rel_path,
                subtitle=abs_path,
                arg=abs_path,
                autocomplete=rel_path,
            )
            item.open_file(path=abs_path)
            sf.items.append(item)
        if not sf.items:
            item = Item(
                title=f"{query!r} did not match any source file",
                subtitle="Try a different query",
            )
            sf.items.append(item)
        return sf

    def parse_query(
        self,
        query: str,
    ) -> dict:
        return {"query": query.strip()}

    def encode_query(
        self,
        query: str,
    ) -> str:
        return query


handler = Handler(id="source_files")
