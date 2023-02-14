ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

BIN_DIR := $$VENV/bin

##
.DEFAULT_GOAL:=help


## ------------ help-rules --------------
help-g:  ## Display '#\{2\}' descriptions
	@awk 'BEGIN {FS = ":.*##"; printf "\nShort help:\n  make \033[36m\033[0m\n"} \
	/^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
	/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
help: ## Same as 'help-g'
help:  help-g

help-d:  ## Make help via Docker (https://github.com/Xanders/make-help)
	@cat $(MAKEFILE_LIST) | docker run --rm -i xanders/make-help
h: ## Same as 'help-d'
h: help-d

help-3: ## Display '#\{3\}' descriptions
	@sed -e '/#\{3\}/!d; s/\\$$//; s/:[^#\t]*/:\t/; s/#\{3\} *//' $(MAKEFILE_LIST)
3: help-3
##


## ------------ venv-pip --------------
create-venv: $(eval SHELL:=/bin/bash)
	@[[ -d $(VENV) ]] && echo "$(VENV) already exists" \
	|| (echo 'Creating virtual evnironment ...'; python3 -m venv $(VENV))

pip-install: $(eval SHELL:=/bin/bash)
	@(echo 'Updating pip ...'; $$VENV/bin/pip install -U pip) \
	&& (echo 'Installing requirements ...'; $$VENV/bin/pip install -r requirements.txt)

# Create virtual-env and pip install requirements
install: create-venv pip-install

pip-update:
	@$(BIN_DIR)/pip install -U pip && $(BIN_DIR)/pip install -r <(pip freeze) --upgrade


## ------------ template --------------
# Passing arguments to "make create_template" or "make new"
ifeq ($(filter $(new) $(create_template), $(firstword $(MAKECMDGOALS))),)
  # use the rest as arguments for "new"
  NEW_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(NEW_ARGS):;@:)
endif

create_template:
	@./scripts/create_parser_template $(NEW_ARGS)

# Create new template
# make new <PARSER>
#   make -- new --help
new: ###
new: create_template


## ------------- run ---------------
# Start parser with interactive mode
# make irun <parser>
irun: ###
	@$(BIN_DIR)/python -i -Wall . $(word 2, $(MAKECMDGOALS))

# Start parser
# make run <parser>
run: ###
	@$(BIN_DIR)/python . $(word 2, $(MAKECMDGOALS))

# Start parser with warnings
# make wrun <parser>
wrun:
	@$(BIN_DIR)/python -Wall . $(word 2, $(MAKECMDGOALS))

# Run parser directly
# px: PARSER := ./parsers/user_parsers/{}.py
# px: parse
# parse:
# 	@time -vo $(shell dirname $(PARSER))/.time.log "$(BIN_DIR)/python" -i "$(PARSER)"


## ------------ traceback --------------
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


## ------------ check --------------
flake8:
	@$@ --max-line-length=119 --ignore=E402,F841,F401,E302,E305 --max-complexity=10

mypy:
	@$@ --namespace-packages --explicit-package-bases --show-error-codes

spell:
	@pyspelling

shellcheck:
	@$@ ./scripts/*

.PHONY: lint
lint:
	@make -j4 flake8 mypy spell shellcheck

bandit: ## Find common security issues in Python code
	@$@ --recursive .

safety: ## Check installed dependencies for known vulnerabilities
	@$@ check -r requirements/pip/local.txt --full-report

.PHONY: security
security: bandit safety ## Guard with Bandit and Safety

check: ## Check all
	make lint security

# Display versions of Chrome, Chromedriver, Selenium
versions:
	@/usr/bin/google-chrome --version
	@"$(PWD)/parsers/request/driver/chrome/chromedriver" --version
	@printf 'Selenium '; "$(BIN_DIR)"/python -c "print(__import__('selenium').__version__)"


## ------------ files --------------
recompile:
	@$(BIN_DIR)/python -m recompile ./parsers -q

# Press ^D to close stdin
note:
	python -c "import sys;\
	f=open(sys.argv[1],'a');\
	f.write(''.join([i for i in sys.stdin]));\
	f.close()" NOTE.tmp

diff:
	@$@ -u $(word 2, $(MAKECMDGOALS)) $(word 3, $(MAKECMDGOALS)) \
	| perl /usr/share/doc/git/contrib/diff-highlight/diff-highlight

ls-vsc-files:
	ls -a ~/.vscode-server/extensions/ms-python.python-20[2-9][0-9].[0-9][0-9].[0-9]/pythonFiles/

head:
	echo ./data/$(word 3, $(MAKECMDGOALS))
	@$@ $(word 2, $(MAKECMDGOALS)) ./data/$(word 3, $(MAKECMDGOALS))/response.* | code -

# Create temp files
tmp:
	@touch tmp.{TODO,g,notes,py,sh}


## ------------ XServer --------------
check_xserver_process_exist:
	@powershell.exe get-process vcxsrv -ErrorAction SilentlyContinue \
	&& echo "success!" || { echo "failure!"; exit 1; }

# open XLaunch: Multiple windows -> Start no client -> Check 'Disable access control' -> Finish
XLAUNCH_CONFIG := '"$(PWD)/.config/config.xlaunch"'
PROGRAM_DATA := /mnt/c/Progra~1
XLAUNCH := '"$(PROGRAM_DATA)/VcXsrv/xlaunch.exe"'
PARAMS := '-run', $(XLAUNCH_CONFIG)
NOHUP := $(PWD)/log/nohup.out

run_xlaunch:
	@nohup python3 -c "__import__('subprocess').call([$(XLAUNCH), $(PARAMS)])" > $(NOHUP) 2>&1 &
	@sleep 1; ps -o cmd | tail -4 | head -1

# Start XServer
# NOTE: start terminal as admin
xlaunch:
	make check_xserver_process_exist || make run_xlaunch
