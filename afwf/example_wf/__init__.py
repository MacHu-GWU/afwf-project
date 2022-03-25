# -*- coding: utf-8 -*-

import afwf
from .handlers import python_version

wf = afwf.Workflow()
wf.register(python_version.handler)
