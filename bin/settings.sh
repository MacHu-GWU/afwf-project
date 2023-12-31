#!/bin/bash
#
# Project specific settings value

if [ -n "${BASH_SOURCE}" ]
then
    dir_bin="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
else
    dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
fi
dir_project_root="$(dirname "${dir_bin}")"

#-----------------------------------------------------------------------------
# Change configuration here
#-----------------------------------------------------------------------------
# Your python alfred workflow has to be a package styled python library
# Put the package import name here
package_name="afwf"

# This is the directory absolute path of your Alfred Workflow
# Please update it manually, you can use this method to find it
# Right click your workflow in Alfred Workflow view, then click "open in finder"
dir_workflow="/Users/sanhehu/Documents/Alfred-Setting/Alfred.alfredpreferences/workflows/user.workflow.A909756D-ADA3-422B-A53F-B64D7E68445A"

# This is your development python virtual environment path
# It should have a "./bin" folder in it and "./bin/activate", "./bin/activate" files
dir_venv="${dir_project_root}/.venv"

# Don't touch this
package_version="$(python ${dir_project_root}/${package_name}/_version.py)"
