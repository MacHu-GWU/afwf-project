#!/bin/bash
#
# This shell script only re-build the main.py and aws_tools source code
# to Alfred Workflow preference directory, without install any dependencies
#
# It allows developer to quickly test the latest code with real Alfred UI
# You should run this script everything you update your source code

dir_bin="$( cd "$(dirname "$0")" ; pwd -P )"
dir_project_root="$(dirname "${dir_bin}")"

source "${dir_bin}/settings.sh"

bin_pip="${dir_venv}/bin/pip"

rm "${dir_workflow}/main.py"
rm -r "${dir_workflow}/lib/${package_name}"
rm -r "${dir_workflow}/lib/${package_name}-${package_version}.dist-info"

cp "${dir_project_root}/main.py" "${dir_workflow}/main.py"
${bin_pip} install "${dir_project_root}" --no-dependencies --target="${dir_workflow}/lib"
