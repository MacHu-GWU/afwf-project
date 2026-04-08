# -*- coding: utf-8 -*-

import sys
import dataclasses
from pathlib import Path
from functools import cached_property

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from ..alfred.workflow import AlfredWorkflow


@dataclasses.dataclass
class AfwfProject:
    """
    Represents a Python project built with the afwf framework.

    Binds together:

    - The **source project** (``dir_project_root``) — the git repo you develop in
    - The **Alfred Workflow folder** (``alfred_workflow``) — where Alfred runs the code

    Typical project layout::

        <dir_project_root>/
        ├── <package_name>/     ← Python package (same as [project] name in pyproject.toml)
        ├── main.py             ← entry point, copied to workflow folder on build
        ├── info.plist          ← synced back from Alfred for version control
        ├── icon.png            ← synced back from Alfred for version control
        └── pyproject.toml

    All attributes are lazily evaluated and cached on first access.

    :param dir_project_root: Root directory of the Python project.
    :param alfred_workflow: The Alfred Workflow this project deploys to.
    """

    dir_project_root: Path
    alfred_workflow: AlfredWorkflow

    def __post_init__(self):
        self.dir_project_root = Path(self.dir_project_root)

    # ------------------------------------------------------------------
    # Project-side paths
    # ------------------------------------------------------------------

    @cached_property
    def path_pyproject_toml(self) -> Path:
        """``pyproject.toml`` at the project root."""
        return self.dir_project_root / "pyproject.toml"

    @cached_property
    def _pyproject_data(self) -> dict:
        """Raw dict parsed from ``pyproject.toml``."""
        with self.path_pyproject_toml.open("rb") as fh:
            return tomllib.load(fh)

    @cached_property
    def package_name(self) -> str:
        """
        Python package name, read from the ``[project] name`` field in
        ``pyproject.toml``.
        """
        return self._pyproject_data["project"]["name"]

    @cached_property
    def dir_package(self) -> Path:
        """The main Python package directory (``<root>/<package_name>/``)."""
        return self.dir_project_root / self.package_name

    @cached_property
    def path_project_main_py(self) -> Path:
        """``main.py`` at the project root (source, copied to workflow on build)."""
        return self.dir_project_root / "main.py"

    @cached_property
    def path_project_info_plist(self) -> Path:
        """``info.plist`` at the project root (synced back from Alfred for VCS)."""
        return self.dir_project_root / "info.plist"

    @cached_property
    def path_project_icon_png(self) -> Path:
        """``icon.png`` at the project root (synced back from Alfred for VCS)."""
        return self.dir_project_root / "icon.png"

    # ------------------------------------------------------------------
    # Workflow-side paths (afwf convention on top of AlfredWorkflow)
    # ------------------------------------------------------------------

    @cached_property
    def path_workflow_main_py(self) -> Path:
        """``main.py`` inside the Alfred Workflow folder."""
        return self.alfred_workflow.dir_workflow / "main.py"

    @cached_property
    def dir_workflow_lib(self) -> Path:
        """``lib/`` inside the Alfred Workflow folder (pip install target)."""
        return self.alfred_workflow.dir_workflow / "lib"
