# Makefile search <Ctlr+F>
# ------------------------
# Parsers -------- # + 0
#  base .......... # + 01
#  proxy ......... # + 02
# Scripts -------- # + 1
#  ./scripts/* ... # + 11
#  makescripts ... # + 12
# Data ----------- # + 2
# Linting -------- # + 3
# Information ---- # + 4
# Updaing -------- # + 5
# Clean ---------- # + 6
# Configuration -- #`
#  XServer ....... #` + 1
#  makeconf ...... #` + 2


BIN_DIR := $$VENV/bin


#0 ------------------------- Parsers -------------------------

#01 -------------- base ----------------
# make run <PARSER_NAME>
irun:
	@$(BIN_DIR)/python -i -Wall . $(word 2, $(MAKECMDGOALS))

run:
	@$(BIN_DIR)/python . $(word 2, $(MAKECMDGOALS))

#02 -------------- proxy ----------------
px: PARSER := $(PWD)/parsers/request/proxy/core.py
px: parse


parse:
	@time -vo $(shell dirname $(PARSER))/.time.log "$(BIN_DIR)/python" -i "$(PARSER)"


#1 ------------------------- Scripts -------------------------

#11 --------- ./scrits/* ------------

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

#12 --------- makescripts ------------

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

#2 -------------------------- Data --------------------------

head:
	echo ./data/$(word 3, $(MAKECMDGOALS))
	@$@ $(word 2, $(MAKECMDGOALS)) ./data/$(word 3, $(MAKECMDGOALS))/response.* | code -


#3 -------------------------- Linting -------------------------

flake8:
	@$(BIN_DIR)/$@

mypy:
	@$(BIN_DIR)/$@ --namespace-packages --explicit-package-bases --show-error-codes

check:
	make flake8 mypy

shellcheck:
	$@ ./scripts/*


#4 --------------------------- files --------------------------

cloc:
	$@ --exclude-list-file=.clocignore .

recompile:
	@$(BIN_DIR)/python -m recompile ./parsers -q


#5 ------------------------- Updating -------------------------

versions: # Display the versions of Chrome, Chromedriver, Selenium
	@/usr/bin/google-chrome --version
	@"$(PWD)/src/driver/chrome/chromedriver" --version
	@printf 'Selenium '; $(PYTHON) -c "print(__import__('selenium').__version__)"


#6 -------------------------- Clean --------------------------


#` ---------------------- Configuration ----------------------

#`1 ------------ XServer --------------

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

#`2 ------------ makeconf --------------
ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif
