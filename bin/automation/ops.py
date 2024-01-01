# -*- coding: utf-8 -*-

from pathlib_mate import Path

from .afwf_ops import api as afwf_ops

path_bin_python = Path.home().joinpath(".pyenv/shims/python3.8")
path_bin_pip = Path.home().joinpath(".pyenv/shims/pip3.8")
dir_workflow = Path.home().joinpath(
    "Documents/Alfred-Setting/Alfred.alfredpreferences/workflows/user.workflow.A909756D-ADA3-422B-A53F-B64D7E68445A"
)
dir_project_root = Path.dir_here(__file__).parent.parent
wf_ctx = afwf_ops.WorkflowContext(dir_workflow=dir_workflow)
proj_ctx = afwf_ops.ProjectContext(dir_project_root=dir_project_root)


def build_wf():
    afwf_ops.build_wf(
        path_bin_pip=path_bin_pip,
        wf_ctx=wf_ctx,
        proj_ctx=proj_ctx,
    )


def refresh_code():
    afwf_ops.refresh_code(
        path_bin_pip=path_bin_pip,
        wf_ctx=wf_ctx,
        proj_ctx=proj_ctx,
    )
