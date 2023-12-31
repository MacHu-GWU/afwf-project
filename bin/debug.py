# -*- coding: utf-8 -*-

import subprocess

from automation import paths

args = [
    f"{paths.path_pyenv_bin_python}",
    f"{paths.path_workflow_main_py}",
    'python_version 3.7',
]
print(" ".join(args))
subprocess.run(args, check=True)
