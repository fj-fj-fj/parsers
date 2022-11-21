#!/bin/bash
# Update Pyenv, download latest Python, update venv

[ -x "$(command -v pyenv)" ] || exit 1

VENV_BASENAME=".$PROJECT_NAME"
# pyenv-virtualenv: Plugin for pyenv and virtual environments
pyenv_venv="$(pyenv root)/plugins/pyenv-virtualenv"
# pyenv-update: Plugin for updating pyenv
pyenv_update="$(pyenv root)/plugins/pyenv-update"
# pyenv-doctor: Plugin to verify that pyenv and build dependencies are installed
pyenv_doctor="$(pyenv root)/plugins/pyenv-doctor"
# pyenv-which-ext: Plugin to automatically lookup system commands
pyenv_which_ext="$(pyenv root)/plugins/pyenv-which-ext"

[ -d $pyenv_venv ] || git clone https://github.com/pyenv/pyenv-virtualenv.git $pyenv_venv
[ -d $pyenv_update ] || git clone https://github.com/pyenv/pyenv-update.git $pyenv_update
[ -d $pyenv_doctor ] || git clone https://github.com/pyenv/pyenv-doctor.git $pyenv_doctor
[ -d $pyenv_which_ext ] || git clone https://github.com/pyenv/pyenv-which-ext.git $pyenv_which_ext

pyenv update
pyenv install $(PYTHON_VERSION):latest

rm -rf $VENV
pyenv virtualenv "$VENV_BASENAME"
pyenv local "$VENV_BASENAME"

$VENV/bin/python -m test
$VENV/bin/python -m pip install --upgrade pip
$VENV/bin/pip install -r requirements.txt
