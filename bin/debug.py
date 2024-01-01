# -*- coding: utf-8 -*-

import json
from automation.ops import path_bin_python, dir_workflow
from afwf.example_wf.handlers import python_version
from rich import print as rprint

# verbose = True
verbose = False

handler = python_version.handler
query = ""
# query = "3.7"

res = handler.run_script_command(path_bin_python, dir_workflow, query, verbose=verbose)
if res is None:
    print(f"res = {res}")
else:
    rprint(json.loads(res))
