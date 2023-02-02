ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# export VENV=VENV_NAME ?
BIN_DIR := $$VENV/bin


# ------------ venv-pip --------------
create-venv: $(eval SHELL:=/bin/bash)
	@[[ -d $(VENV) ]] && echo "$(VENV) already exists" \
	|| (echo 'Creating virtual evnironment ...'; python3 -m venv $(VENV))

pip-install: $(eval SHELL:=/bin/bash)
	@(echo 'Updating pip ...'; $$VENV/bin/pip install -U pip) \
	&& (echo 'Installing requirements ...'; $$VENV/bin/pip install -r requirements.txt)

install: create-venv pip-install


# ------------- run ---------------
irun:
	@$(BIN_DIR)/python -i -Wall . $(word 2, $(MAKECMDGOALS))

run:
	@$(BIN_DIR)/python . $(word 2, $(MAKECMDGOALS))

wrun:
	@$(BIN_DIR)/python -Wall . $(word 2, $(MAKECMDGOALS))

# Run parser directly
# px: PARSER := ./parsers/user_parsers/{}.py
# px: parse
# parse:
# 	@time -vo $(shell dirname $(PARSER))/.time.log "$(BIN_DIR)/python" -i "$(PARSER)"


# ------------ template --------------
# Passing arguments to "make create_template" or "make new"
ifeq ($(filter $(new) $(create_template), $(firstword $(MAKECMDGOALS))),)
  # use the rest as arguments for "new"
  NEW_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(NEW_ARGS):;@:)
endif

create_template:
	@./scripts/create_parser_template $(NEW_ARGS)

# Usage:
#   make new <PARSER>
#   make -- new --help
new: create_template


# ------------ traceback --------------
# Usage:
#   make trace <PARSER>
#    - to generate traceback markdown file if fail
#   make trace <PARSER> [1|--new-window (i.e anything true)]
#    - to new VSCode instance with traceback's files directory if fail
trace:
	@./scripts/traceback $(word 2, $(MAKECMDGOALS)) $(word 3, $(MAKECMDGOALS))

birdseye:
	@nohup python -m $@ > ./log/$@_nohup.out 2>&1 &
	@echo http://localhost:7777

r: birdseye run
t: birdseye trace


# ------------ check --------------
flake8:
	@$(BIN_DIR)/$@

mypy:
	@$(BIN_DIR)/$@ --namespace-packages --explicit-package-bases --show-error-codes

check:
	make flake8 mypy

shellcheck:
	$@ ./scripts/*

versions: # Display the versions of Chrome, Chromedriver, Selenium
	@/usr/bin/google-chrome --version
	@"$(PWD)/parsers/request/driver/chrome/chromedriver" --version
	@printf 'Selenium '; "$(BIN_DIR)"/python -c "print(__import__('selenium').__version__)"


# ------------ files --------------
cloc:
	$@ --exclude-list-file=.clocignore .

recompile:
	@$(BIN_DIR)/python -m recompile ./parsers -q

# Press <Ctrl+D> to close stdin
note:
	python -c "import sys;\
	f=open(sys.argv[1],'a');\
	f.write(''.join([i for i in sys.stdin]));\
	f.close()" NOTE.tmp

diff:
	@$@ -u $(word 2, $(MAKECMDGOALS)) $(word 3, $(MAKECMDGOALS)) \
	| perl /usr/share/doc/git/contrib/diff-highlight/diff-highlight

lsvscfiles:
	ls -a ~/.vscode-server/extensions/ms-python.python-20[2-9][0-9].[0-9][0-9].[0-9]/pythonFiles/

head:
	echo ./data/$(word 3, $(MAKECMDGOALS))
	@$@ $(word 2, $(MAKECMDGOALS)) ./data/$(word 3, $(MAKECMDGOALS))/response.* | code -


# ------------ XServer --------------
check_xserver_process_exist:
	@powershell.exe get-process vcxsrv -ErrorAction SilentlyContinue \
	&& echo "success!" || { echo "failure!"; exit 1; }

# open XLaunch: Multiple windows -> Start no client -> Check 'Disable access control' -> Finish
XLAUNCH_CONFIG := '"$(PWD)/log/config.xlaunch"'
PROGRAM_DATA := /mnt/c/Progra~1
XLAUNCH := '"$(PROGRAM_DATA)/VcXsrv/xlaunch.exe"'
PARAMS := '-run', $(XLAUNCH_CONFIG)
NOHUP := $(PWD)/log/nohup.out

run_xlaunch:
	@nohup python3 -c "__import__('subprocess').call([$(XLAUNCH), $(PARAMS)])" > $(NOHUP) 2>&1 &
	@sleep 1; ps -o cmd | tail -4 | head -1

# NOTE: start terminal as admin
xlaunch:
	make check_xserver_process_exist || make run_xlaunch
