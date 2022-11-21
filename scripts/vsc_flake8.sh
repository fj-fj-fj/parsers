#/bin/sh

# $(PROJECT_DIR)/scripts/vscode_flake8 [filename, ...]
$VENV/bin/python ~/.vscode-server/extensions/ms-python.python-20[2-9][0-9].[0-9][0-9].[0-9]/pythonFiles/linter.py \
    -m flake8 \
        --exclude=.git,.story,data,tests \
        --format='%(cyan)s%(path)s%(white)s:%(green)s%(row)d%(white)s:%(yellow)s%(col)s%(white)s: %(red)s%(code)s %(white)s%(text)s' \
        --ignore=E402,F841,F401,E302,E305 \
        --max-complexity=10 \
        --max-line-length=119 \
        $1 || .
