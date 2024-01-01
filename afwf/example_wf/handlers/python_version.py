# -*- coding: utf-8 -*-

import typing as T

import subprocess
from pathlib_mate import Path

import attr
import afwf

from ..cache import cache
from ... import paths


@attr.define
class Handler(afwf.Handler):
    @cache.memoize(expire=60)
    def get_all_python_version(self) -> T.List[str]:
        dir_pyenv = Path(paths.dir_project_root.joinpath("pyenv"))
        dir_pyenv.remove_if_exists()
        with Path(paths.dir_project_root).temp_cwd():
            args = ["git", "clone", "--depth", "1", "https://github.com/pyenv/pyenv"]
            subprocess.run(args, check=True)
            dir_python_build = paths.dir_project_root.joinpath(
                "pyenv", "plugins", "python-build", "share", "python-build"
            )
            versions = list()
            for p in dir_python_build.iterdir():
                if p.is_file():
                    version = p.name
                    versions.append(version)
            return versions

    def main(self, query: str) -> afwf.ScriptFilter:
        if query == "error":
            raise ValueError("query cannot be 'error'!")
        versions = self.get_all_python_version()
        filtered_versions = [version for version in versions if query in version]
        filtered_versions.sort()
        filtered_versions = filtered_versions[:50]
        sf = afwf.ScriptFilter()
        for version in filtered_versions:
            url = f"https://github.com/pyenv/pyenv/blob/master/plugins/python-build/share/python-build/{version}"
            item = afwf.Item(
                title=version,
                autocomplete=version,
                arg=url,
            )
            item.open_url(url=url)
            sf.items.append(item)
        if len(sf.items) == 0:
            url = "https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build"
            item = afwf.Item(
                title=f"{query!r} doesn't match any Python version!",
                subtitle=f"Open {url}",
                arg=url,
            )
            item.open_url(url=url)
            sf.items.append(item)
        return sf

    def parse_query(self, query: str) -> T.Dict[str, T.Any]:
        return dict(query=query)


handler = Handler(id="python_version")
