# -*- coding: utf-8 -*-

import subprocess

from . import paths
from .nested_logger import logger

@logger.pretty_log()
def build_wf():
    """
    Build Alfred Workflow release from source code. Basically it creates:

    - user.workflow.../main.py
    - user.workflow.../lib
    - ${dir_project_root}/info.plist
    """
    # delete user.workflow.../main.py
    paths.path_workflow_main_py.remove_if_exists()
    # delete user.workflow.../lib
    paths.dir_workflow_lib.remove_if_exists()
    # delete ${dir_project_roo}/info.plist
    paths.path_git_repo_info_plist.remove_if_exists()

    # create user.workflow.../main.py
    paths.path_git_repo_main_py.copyto(paths.path_workflow_main_py)

    # create user.workflow.../lib/
    with paths.dir_project_root.temp_cwd():
        args = [
            f"{paths.bin_pip}",
            "install",
            f"{paths.dir_project_root}",
            f"--target={paths.dir_workflow_lib}",
        ]
        subprocess.run(args)

        args = [
            f"{paths.bin_pip}",
            "install",
            "-r",
            f"{paths.path_requirements_dev}",
            f"--target={paths.dir_workflow_lib}",
        ]
        subprocess.run(args)

    # create info.plist
    paths.path_workflow_info_plist.copyto(paths.path_git_repo_info_plist)


@logger.pretty_log()
def refresh_code():
    """
    This shell script only re-build the main.py and the source code
    to Alfred Workflow preference directory, without install any dependencies

    It allows developer to quickly test the latest code with real Alfred UI
    You should run this script everything you update your source code
    """
    # delete user.workflow.../main.py
    paths.path_workflow_main_py.remove_if_exists()
    # delete user.workflow.../lib/${PACKAGE_NAME}/
    paths.dir_workflow_lib.joinpath(paths.PACKAGE_NAME).remove_if_exists()
    # delete user.workflow.../lib/${PACKAGE_NAME}-${VERSION}.dist-info/
    for p in paths.dir_workflow_lib.iterdir():
        if p.basename.startswith(f"{paths.PACKAGE_NAME}-") and p.basename.endswith(
            ".dist-info"
        ):
            p.remove_if_exists()

    # create user.workflow.../main.py
    paths.path_git_repo_main_py.copyto(paths.path_workflow_main_py)
    with paths.dir_project_root.temp_cwd():
        args = [
            f"{paths.bin_pip}",
            "install",
            f"{paths.dir_project_root}",
            "--no-dependencies",
            f"--target={paths.dir_workflow_lib}",
        ]
        subprocess.run(args)
