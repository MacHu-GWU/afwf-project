# -*- coding: utf-8 -*-

import subprocess
import dataclasses

from pathlib_mate import T_PATH_ARG, Path

from .compat import cached_property
from .logger import logger


@dataclasses.dataclass
class WorkflowContext:
    """
    Represent a specific Alfred Workflow folder in the fAlfred Preference folder.
    Usually, the path is like
    ``/path/to/Alfred.alfredpreferences/workflows/user.workflow.ABCD1234-A1B2-C3D4-E5F6-A1B2C3D4E5F6/``

    It should have the following files / folders:

    - a ``lib`` folder which contains the Python dependencies.
    - a ``main.py`` file which is the entry point of the workflow.
    - a ``info.plist`` file which is an XML file that contains your workflow
        widgets and settings.
    - a ``icon.png`` file which is the icon of the workflow.
    """

    dir_workflow: T_PATH_ARG = dataclasses.field()

    def __post_init__(self):
        self.dir_workflow = Path(self.dir_workflow)

    @property
    def dir_workflow_lib(self) -> Path:
        return self.dir_workflow.joinpath("lib")

    @property
    def path_workflow_main_py(self) -> Path:
        return self.dir_workflow.joinpath("main.py")

    @property
    def path_workflow_info_plist(self) -> Path:
        return self.dir_workflow.joinpath("info.plist")

    @property
    def path_workflow_icon_png(self) -> Path:
        return self.dir_workflow.joinpath("icon.png")

    def pre_build(self):
        self.dir_workflow_lib.remove_if_exists()
        self.path_workflow_main_py.remove_if_exists()


@dataclasses.dataclass
class ProjectContext:
    """
    Represent a specific Alfred Workflow Python project
    """

    dir_project_root: T_PATH_ARG = dataclasses.field()

    def __post_init__(self):
        self.dir_project_root = Path(self.dir_project_root)

    @cached_property
    def package_name(self) -> str:
        for path in self.dir_project_root.select_dir(recursive=False):
            if path.joinpath("_version.py").exists():
                return path.basename
        raise FileNotFoundError

    @property
    def dir_project_lib(self) -> Path:
        return self.dir_project_root.joinpath(self.package_name)

    @property
    def path_project_main_py(self) -> Path:
        return self.dir_project_root.joinpath("main.py")

    @property
    def path_project_info_plist(self) -> Path:
        return self.dir_project_root.joinpath("info.plist")

    @property
    def path_project_icon_png(self) -> Path:
        return self.dir_project_root.joinpath("icon.png")

    def pre_build(self):
        self.path_project_info_plist.remove_if_exists()
        self.path_project_icon_png.remove_if_exists()


@logger.emoji_block(
    msg="Build Workflow",
    emoji="🔨",
)
def build_wf(
    path_bin_pip: T_PATH_ARG,
    wf_ctx: WorkflowContext,
    proj_ctx: ProjectContext,
):
    """
    Build Alfred Workflow from source code. Basically it does the following:

    - Install dependencies and source code to ``/path/to/Alfred.alfredpreferences/workflows/user.workflow.../lib``
    - Copy the main.py from source code to ``/path/to/Alfred.alfredpreferences/workflows/user.workflow.../main.py``
    - Copy the ``info.plist`` from Alfred Workflow to source code
    - Copy the ``icon.png`` from Alfred Workflow to source code
    """
    wf_ctx.pre_build()
    proj_ctx.pre_build()

    logger.info(f"copy main.py to {wf_ctx.path_workflow_main_py}")
    proj_ctx.path_project_main_py.copyto(wf_ctx.path_workflow_main_py)

    logger.info(f"install dependencies to {wf_ctx.dir_workflow_lib}")
    with proj_ctx.dir_project_root.temp_cwd():
        args = [
            f"{path_bin_pip}",
            "install",
            f"{proj_ctx.dir_project_root}",
            f"--target={wf_ctx.dir_workflow_lib}",
            # "--quiet",
        ]
        subprocess.run(args)

    logger.info(f"copy info.plist to {proj_ctx.path_project_info_plist}")
    wf_ctx.path_workflow_info_plist.copyto(proj_ctx.path_project_info_plist)
    logger.info(f"copy icon.png to {proj_ctx.path_project_icon_png}")
    wf_ctx.path_workflow_icon_png.copyto(proj_ctx.path_project_icon_png)


@logger.emoji_block(
    msg="Refresh Code",
    emoji="🔄",
)
def refresh_code(
    path_bin_pip: T_PATH_ARG,
    wf_ctx: WorkflowContext,
    proj_ctx: ProjectContext,
):
    """
    Similar to :func:`build_wf`, but it does not install dependencies.

    It allows developer to quickly test the latest code with real Alfred UI
    You should run this script everytime you update your source code.
    """
    wf_ctx.path_workflow_main_py.remove_if_exists()
    wf_ctx.dir_workflow_lib.joinpath(proj_ctx.package_name).remove_if_exists()

    for p in wf_ctx.dir_workflow_lib.iterdir():
        if p.basename.startswith(f"{proj_ctx.package_name}-") and p.basename.endswith(
            ".dist-info"
        ):
            p.remove_if_exists()

    logger.info(f"copy main.py to {wf_ctx.path_workflow_main_py}")
    proj_ctx.path_project_main_py.copyto(wf_ctx.path_workflow_main_py)

    logger.info(f"install {proj_ctx.package_name!r} to {wf_ctx.dir_workflow_lib}")
    with proj_ctx.dir_project_root.temp_cwd():
        args = [
            f"{path_bin_pip}",
            "install",
            f"{proj_ctx.dir_project_root}",
            "--no-dependencies",
            f"--target={wf_ctx.dir_workflow_lib}",
            # "--quiet",
        ]
        subprocess.run(args)
