# -*- coding: utf-8 -*-

"""
A sample workflow built on top of the afwf library. It is used as an integration
test case for the library.
"""

import afwf
from .handlers import python_version

wf = afwf.Workflow()
wf.register(python_version.handler)
