# -*- coding: utf-8 -*-

import dataclasses
import plistlib
from pathlib import Path
from functools import cached_property


@dataclasses.dataclass
class AlfredWorkflow:
    """
    Represents a single Alfred Workflow directory.

    The directory is typically located at::

        <Alfred.alfredpreferences>/workflows/user.workflow.<UUID>/

    and is expected to contain:

    - ``info.plist`` — workflow definition (name, version, bundle id, …)
    - ``icon.png``   — workflow icon
    - ``main.py``    — Python entry point (for afwf-based workflows)
    - ``lib/``       — installed Python dependencies

    All attributes are lazily evaluated and cached on first access.

    :param dir_workflow: Path to the workflow folder,
        e.g. ``…/workflows/user.workflow.76458317-…``.
    """

    dir_workflow: Path

    def __post_init__(self):
        self.dir_workflow = Path(self.dir_workflow)

    # ------------------------------------------------------------------
    # Directory / file paths
    # ------------------------------------------------------------------

    @cached_property
    def workflow_id(self) -> str:
        """UUID extracted from the folder name (``user.workflow.<UUID>``)."""
        return self.dir_workflow.name.removeprefix("user.workflow.")

    @cached_property
    def path_info_plist(self) -> Path:
        """``info.plist`` workflow definition file."""
        return self.dir_workflow / "info.plist"

    @cached_property
    def path_icon_png(self) -> Path:
        """``icon.png`` workflow icon."""
        return self.dir_workflow / "icon.png"

    # ------------------------------------------------------------------
    # Parsed info.plist fields
    # ------------------------------------------------------------------

    @cached_property
    def _plist_data(self) -> dict:
        """Raw dict parsed from ``info.plist``."""
        with self.path_info_plist.open("rb") as fh:
            return plistlib.load(fh)

    @cached_property
    def name(self) -> str:
        """Human-readable workflow name (``name`` key in ``info.plist``)."""
        return self._plist_data.get("name", "")

    @cached_property
    def bundle_id(self) -> str:
        """
        Reverse-DNS bundle identifier (``bundleid`` key in ``info.plist``),
        e.g. ``"MacHu-GWU.afwf_fts_anything"``.
        """
        return self._plist_data.get("bundleid", "")

    @cached_property
    def version(self) -> str:
        """Workflow version string (``version`` key in ``info.plist``)."""
        return self._plist_data.get("version", "")

    @cached_property
    def description(self) -> str:
        """Short description (``description`` key in ``info.plist``)."""
        return self._plist_data.get("description", "")

    @cached_property
    def created_by(self) -> str:
        """Author name (``createdby`` key in ``info.plist``)."""
        return self._plist_data.get("createdby", "")

    @cached_property
    def web_address(self) -> str:
        """Homepage / repo URL (``webaddress`` key in ``info.plist``)."""
        return self._plist_data.get("webaddress", "")

    @cached_property
    def readme(self) -> str:
        """Full readme text (``readme`` key in ``info.plist``)."""
        return self._plist_data.get("readme", "")

    @cached_property
    def disabled(self) -> bool:
        """Whether the workflow is currently disabled in Alfred."""
        return bool(self._plist_data.get("disabled", False))

    def __repr__(self) -> str:
        return f"AlfredWorkflow(name={self.name!r}, bundle_id={self.bundle_id!r}, version={self.version!r})"
