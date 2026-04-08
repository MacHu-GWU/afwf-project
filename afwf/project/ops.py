# -*- coding: utf-8 -*-

import shutil
import subprocess
from pathlib import Path

from .project import AfwfProject


# TODO: 计划将以下两个函数的依赖安装方式从 pip --target 迁移到 uv:
#   在 workflow 目录下直接用 `uv venv .venv` 创建虚拟环境，
#   再用 `uv pip install` 安装依赖，速度更快、环境更标准。
#   届时 path_bin_pip 参数可替换为 path_bin_uv，dir_workflow_lib 也不再需要。


def build_wf(
    path_bin_pip: Path,
    proj: AfwfProject,
) -> None:
    """
    Full build: install all dependencies and source code into the Alfred
    Workflow folder, then sync ``info.plist`` and ``icon.png`` back to the
    project for version control.

    Steps:

    1. Remove ``<workflow>/lib/`` and ``<workflow>/main.py``
    2. Copy ``main.py`` from the project into the workflow folder
    3. ``pip install <project_root> --target=<workflow>/lib``
    4. Copy ``info.plist`` from Alfred back to the project root
    5. Copy ``icon.png`` from Alfred back to the project root

    :param path_bin_pip: Path to the ``pip`` executable to use.
    :param proj: The afwf project to build.
    """
    # Clean workflow targets
    if proj.dir_workflow_lib.exists():
        shutil.rmtree(proj.dir_workflow_lib)
    if proj.path_workflow_main_py.exists():
        proj.path_workflow_main_py.unlink()

    # Clean project sync targets
    if proj.path_project_info_plist.exists():
        proj.path_project_info_plist.unlink()
    if proj.path_project_icon_png.exists():
        proj.path_project_icon_png.unlink()

    print(f"Copying main.py -> {proj.path_workflow_main_py}")
    shutil.copy2(proj.path_project_main_py, proj.path_workflow_main_py)

    print(f"Installing dependencies -> {proj.dir_workflow_lib}")
    subprocess.run(
        [
            str(path_bin_pip),
            "install",
            str(proj.dir_project_root),
            f"--target={proj.dir_workflow_lib}",
        ],
        cwd=proj.dir_project_root,
        check=True,
    )

    print(f"Syncing info.plist -> {proj.path_project_info_plist}")
    shutil.copy2(proj.alfred_workflow.path_info_plist, proj.path_project_info_plist)

    print(f"Syncing icon.png -> {proj.path_project_icon_png}")
    shutil.copy2(proj.alfred_workflow.path_icon_png, proj.path_project_icon_png)


def refresh_code(
    path_bin_pip: Path,
    proj: AfwfProject,
) -> None:
    """
    Fast refresh: reinstall only the project's own package (no dependencies).

    Use this during development after every source code change to make Alfred
    pick up the latest code without the slow full dependency installation.

    Steps:

    1. Remove ``<workflow>/main.py``
    2. Remove ``<workflow>/lib/<package_name>/`` and its ``.dist-info``
    3. Copy ``main.py`` from the project into the workflow folder
    4. ``pip install <project_root> --no-dependencies --target=<workflow>/lib``

    :param path_bin_pip: Path to the ``pip`` executable to use.
    :param proj: The afwf project to refresh.
    """
    if proj.path_workflow_main_py.exists():
        proj.path_workflow_main_py.unlink()

    pkg_dir = proj.dir_workflow_lib / proj.package_name
    if pkg_dir.exists():
        shutil.rmtree(pkg_dir)

    for p in proj.dir_workflow_lib.iterdir():
        if p.name.startswith(f"{proj.package_name}-") and p.name.endswith(".dist-info"):
            shutil.rmtree(p)

    print(f"Copying main.py -> {proj.path_workflow_main_py}")
    shutil.copy2(proj.path_project_main_py, proj.path_workflow_main_py)

    print(f"Installing {proj.package_name!r} -> {proj.dir_workflow_lib}")
    subprocess.run(
        [
            str(path_bin_pip),
            "install",
            str(proj.dir_project_root),
            "--no-dependencies",
            f"--target={proj.dir_workflow_lib}",
        ],
        cwd=proj.dir_project_root,
        check=True,
    )
