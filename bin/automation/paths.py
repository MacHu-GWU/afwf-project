# -*- coding: utf-8 -*-

"""
Enum important path on the local file systems for this project.
"""

from pathlib_mate import Path

dir_project_root = Path(__file__).absolute().parent.parent.parent

dir_python_lib = None
for p in dir_project_root.iterdir():
    if p.joinpath("_version.py").exists():
        dir_python_lib = p

PACKAGE_NAME = dir_python_lib.basename

dir_home = Path.home()
# ------------------------------------------------------------------------------
# Virtual Environment Related
# ------------------------------------------------------------------------------
dir_venv = dir_project_root / ".venv"
dir_venv_bin = dir_venv / "bin"

# virtualenv executable paths
bin_python = dir_venv_bin / "python"
bin_pip = dir_venv_bin / "pip"
bin_pytest = dir_venv_bin / "pytest"

# ------------------------------------------------------------------------------
# Test Related
# ------------------------------------------------------------------------------
dir_tests = dir_project_root / "tests"

dir_htmlcov = dir_project_root / "htmlcov"

# ------------------------------------------------------------------------------
# Poetry Related
# ------------------------------------------------------------------------------
path_requirements_main = dir_project_root / "requirements-main.txt"
path_requirements_dev = dir_project_root / "requirements-dev.txt"
path_requirements_test = dir_project_root / "requirements-test.txt"
path_requirements_doc = dir_project_root / "requirements-doc.txt"
path_requirements_automation = dir_project_root / "requirements-automation.txt"

# ------------------------------------------------------------------------------
# Build Related
# ------------------------------------------------------------------------------
dir_build = dir_project_root / "build"
dir_dist = dir_project_root / "dist"

path_pyenv_bin_python = dir_home.joinpath(
    ".pyenv",
    "versions",
    "3.8.13",
    "bin",
    "python",
)

# ------------------------------------------------------------------------------
# Alfred Related
# ------------------------------------------------------------------------------
path_git_repo_info_plist = dir_project_root / "info.plist"
path_git_repo_main_py = dir_project_root / "main.py"

dir_workflow = dir_home.joinpath(
    "Documents",
    "Alfred-Setting",
    "Alfred.alfredpreferences",
    "workflows",
    "user.workflow.A909756D-ADA3-422B-A53F-B64D7E68445A",
)
path_workflow_info_plist = dir_workflow / "info.plist"
path_workflow_main_py = dir_workflow / "main.py"
dir_workflow_lib = dir_workflow / "lib"
