# -*- coding: utf-8 -*-

import json
import dataclasses
from pathlib import Path
from functools import cached_property

from .workflow import AlfredWorkflow


@dataclasses.dataclass
class AlfredPreferences:
    """
    Reads Alfred's ``prefs.json`` to locate the active Alfred preferences
    folder and its nested workflow directories.

    All attributes are lazily evaluated and cached on first access.

    ``~/Library/Application Support/Alfred/prefs.json`` example::

        {
          "current": "/Users/you/Documents/Alfred-Settings/Alfred.alfredpreferences",
          "localhash": "eca048243db0aaa88c88989d699c5ff94a75b844",
          "syncfolders": {
            "5": "~/Documents/Alfred-Settings"
          }
        }
    """

    @cached_property
    def path_prefs_json(self) -> Path:
        """Path to ``~/Library/Application Support/Alfred/prefs.json``."""
        return Path.home() / "Library" / "Application Support" / "Alfred" / "prefs.json"

    @cached_property
    def _prefs_data(self) -> dict:
        """Raw parsed content of ``prefs.json``."""
        return json.loads(self.path_prefs_json.read_text(encoding="utf-8"))

    @cached_property
    def dir_alfred_preferences(self) -> Path:
        """
        The active Alfred preferences folder (``Alfred.alfredpreferences``).

        Resolved from the ``current`` key in ``prefs.json``.
        """
        return Path(self._prefs_data["current"]).expanduser().resolve()

    @cached_property
    def dir_workflows(self) -> Path:
        """
        The ``workflows/`` directory inside the active Alfred preferences folder.

        All user workflows live here as sub-folders named
        ``user.workflow.<UUID>``.
        """
        return self.dir_alfred_preferences / "workflows"

    def get_workflow(self, workflow_id: str) -> "AlfredWorkflow":
        """
        Return an :class:`~afwf.alfred.workflow.AlfredWorkflow` for the given UUID.

        :param workflow_id: The workflow UUID, e.g.
            ``"76458317-5B0A-40E7-A328-DC6C900EC1B9"``.
        """
        dir_workflow = self.dir_workflows / f"user.workflow.{workflow_id}"
        return AlfredWorkflow(dir_workflow=dir_workflow)

    def list_workflows(self) -> list:
        """
        Return a list of :class:`~afwf.alfred.workflow.AlfredWorkflow` objects
        for every workflow folder found in :attr:`dir_workflows`.
        """
        return [
            AlfredWorkflow(dir_workflow=p)
            for p in sorted(self.dir_workflows.iterdir())
            if p.is_dir() and p.name.startswith("user.workflow.")
        ]
