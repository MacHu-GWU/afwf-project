# -*- coding: utf-8 -*-

"""
Example workflow instance — used as a framework integration test fixture.
"""

from afwf.workflow import Workflow

from .handlers import source_files

wf = Workflow()
wf.register(source_files.handler)
