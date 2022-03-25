# -*- coding: utf-8 -*-

from typing import List

import attr
import afwf
import requests
from bs4 import BeautifulSoup

from ..cache import cache


@attr.define
class Handler(afwf.Handler):
    @cache.memoize(expire=60)
    def get_all_python_version(self) -> List[str]:
        invalid_versions = ["patches", "."]
        url = "https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        div = soup.find("div", class_="Box mb-3")
        versions = list()
        for a in div.find_all("a", class_="js-navigation-open Link--primary"):
            version = a.text
            if version not in invalid_versions:
                versions.append(version)
        return versions

    def lower_level_api(self, query: str) -> afwf.ScriptFilter:
        versions = self.get_all_python_version()
        filtered_versions = [
            version
            for version in versions
            if query in version
        ]
        filtered_versions.sort()
        filtered_versions = filtered_versions[:50]
        sf = afwf.ScriptFilter()
        for version in filtered_versions:
            item = afwf.Item(
                title=version,
                autocomplete=version,
                arg=f"https://github.com/pyenv/pyenv/blob/master/plugins/python-build/share/python-build/{version}",
            )
            sf.items.append(item)
        if len(sf.items) == 0:
            sf.items.append(afwf.Item(
                title=f"{query!r} doesn't match any Python version!",
                subtitle="Open https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build",
                arg="https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build",
            ))
        return sf

    def handler(self, query: str) -> afwf.ScriptFilter:
        return self.lower_level_api(query=query)


handler = Handler(id="python_version")
