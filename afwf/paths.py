# -*- coding: utf-8 -*-

"""
Frequently used paths.
"""

from pathlib import Path

dir_here = Path(__file__).absolute().parent
PACKAGE_NAME = dir_here.name

dir_project_root = dir_here.parent

# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_pytest = dir_venv_bin / "pytest"

# test related
dir_htmlcov = dir_project_root / "htmlcov"
path_cov_index_html = dir_htmlcov / "index.html"
dir_unit_test = dir_project_root / "tests"

# ------------------------------------------------------------------------------
# Alfred
# ------------------------------------------------------------------------------
dir_lib = Path(dir_here.parent, "lib")
dir_home = Path.home()
dir_afwf = Path(dir_home, ".alfred-afwf")
p_last_error = Path(dir_afwf, "last-error.txt")
p_debug_log = Path(dir_afwf, "debug.txt")
