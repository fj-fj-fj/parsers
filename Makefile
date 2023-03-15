include ./.config/makefile-settings.mk

## --------------- help -------------------
help: ## Display docstring

## ------------ build --------------
include ./.config/makefile-build.mk

install-core: ## Install build dependencies (to build Python from source)
apt-install-all: ## Install ./requirements/apt/*.txt
install-pyenv: ## Install pyenv & add config lines to .bashrc
del-pyenv: ## Delete pyenv from $HOME & (optional) config lines from .bashrc
create-venv: ## Create v.environment with pyenv (make 'create-venv v=PY_VERSION')
del-venv: ## Delete v.environment (see 'revenv' rule)
revenv: ## Return v.environment from the previous 'upgrade-venv'
upgrade-python: ## Install latest Python version with pyenv
upgrade-venv: ## Create v.environmet with latest Python (with backup to ~/bak)
upgrade: ## make upgrade-python upgrade-venv
pip-install: ## Install requirements.txt
pip-upgrade: ## Upgrade pip & requirements.txt
setup: ## Download latest Python, create v.environment, install reqs
setup-full: ## make install-core setup

## ------------ template --------------
.PHONY: create_template new

# Passing arguments to "make create_template" or "make new"
ifeq ($(filter $(new) $(create_template), $(RULE_NAME)),)
  # use the rest as arguments for "new"
  CREATE_TEMPLATE_ARG := $(ARGS)
  # ...and turn them into do-nothing targets
  $(eval $(CREATE_TEMPLATE_ARG):;@:)
endif

create_template:  ## Create new template
	@./scripts/create_parser_template $(CREATE_TEMPLATE_ARG)

new: create_template  ## make new PARSER (or make --new --help)

## ------------- parse ---------------
.PHONY: irun run wrun px

irun:  ## make irun PARSER (start with -i mode)
	@$(BIN_DIR)/python -i . $(FIRST_ARG)

run: ## make run PARSER (start PARSER()
	@$(BIN_DIR)/python . $(FIRST_ARG)

wrun: ## make wrun PARSER (start with -w mode)
	@$(BIN_DIR)/python -Wall . $(FIRST_ARG)

px: PARSER := $$CURPARSER
px: _px  ## Start exported CURPARSER (make [PYTHON_FLAG(S)] px)
_px:
	@time -vo $(shell dirname $(PARSER))/.time.log \
	"$(BIN_DIR)/python" $(FIRST_ARG) "$(PARSER)"

## ------------ debug --------------
.PHONY: trace birdseye r test

# Usage:
#   make trace PARSER
#    - to generate traceback markdown file if fail
#   make trace PARSER [1 | --new-window]
#    - to new VSCode instance with traceback's files directory if fail
trace:  ## Generate .md error file(s) if fail
	@./scripts/traceback $(FIRST_ARG) $(SECOND_ARG)

birdseye:  ## Debug with Birdseye (https://github.com/alexmojaki/birdseye)
	@nohup python -m $@ > ./log/$@_nohup.out 2>&1 &
	@echo http://localhost:7777

r: birdseye run  ## Start parser with Birdseye
test: birdseye trace  ## Start parser with Birdseye and `trace`

## ------------ check --------------
.PHONY: flake 8 mypy pyspelling spell shellcheck lint
.PHONY: bandit safety security gitleaks warnings
.PHONY: check ch all

makecheck: ## Lint makefile (require Go, checkmake)

flake: ## Check style FILE or recursively (https://github.com/PyCQA/flake8)
	${INFO} "Flake8 starting..."
	@$(BIN_DIR)/$@8 \
	--ignore=E402,F841,F401,E302,E305 \
	--exclude=.git,.story,data,log,tests,_prehistoric*,tmp.py \
	--format='%(cyan)s%(path)s%(white)s:%(green)s%(row)d%(white)s:%(yellow)s%(col)s%(white)s: %(red)s%(code)s %(white)s%(text)s' \
	--max-line-length=119 \
	--max-complexity=10 \
	$(FIRST_ARG_OR_CURRENT_DIR)
	${SUCCESS} "Flake8: style check succeeded"

8: ## ./scripts/flake8_vscode.sh FILE
	@./scripts/flake8_vscode.sh $(FIRST_ARG)

shellcheck: ## Lint sh/bash scripts (https://github.com/koalaman/shellcheck)
	${INFO} "Shellcheck starting..."
	-@ $@ ./scripts/*

mypy: ## Check types FILE or recursively (https://github.com/python/mypy)
	${INFO} "Mypy starting..."
	@$(BIN_DIR)/$@ \
	--namespace-packages \
	--explicit-package-bases \
	--show-error-codes \
	--exclude 'log/*' \
	--exclude 'data/*' \
	--exclude '_prehistoric*/*' \
	--no-warn-no-return \
	--show-column-numbers \
	--show-error-context \
	--no-error-summary \
	--pretty \
	$(FIRST_ARG_OR_CURRENT_DIR)
	${SUCCESS} "Mypy: no issues found"

pyspelling: ## Spell check recursively (https://github.com/facelessuser/pyspelling)
	${INFO} "Pyspelling starting..."
	@ $@

spell: ## Check FILE with pyspelling
	${INFO} "Pyspelling starting..."
	@printf "matrix:\
	\n- name: tmp\
	\n  sources:\
	\n  - $(FIRST_ARG)\
	\n  dictionary:\
	\n    wordlists:\
	\n    - .config/.vocabulary\
	\n    - .config/.vocabulary-python\
	\n  pipeline:\
	\n  - pyspelling.filters.python:\
	\n      string_types: bfur" > ./log/make-spell.yml
	@pyspelling --config ./log/make-spell.yml \
	&& rm ./log/make-spell.yml dictionary.dic

lint: ## Check recursively whth flake8, shellcheck
	@make -j2 flake shellcheck

bandit: ## Find security issues in FILE or recursively (https://github.com/PyCQA/bandit)
	${INFO} "Bandit starting..."
	@$(BIN_DIR)/$@ $(FIRST_ARG_OR_CURRENT_DIR) \
	--exclude ./.story,./parsers/_prehistoric* \
	--recursive \
	--silent \
	--skip B101 \
	2> log/make-bandit.log
	${SUCCESS} "Bandit: no issues identified"

safety: ## Check installed for known vulnerabilities (https://github.com/pyupio/safety)
	${INFO} "Safety starting..."
	@$(BIN_DIR)/$@ check \
	--file requirements/pip/local.txt \
	--full-report \
	1> ./log/make-safety.log \
	&& { printf "\033[32m  Safety: no known security vulnerabilities found\033[0m\n"; \
	$(call remove_esc_secs,./log/make-safety.log); } \
	|| { rc=$$?; printf "\033[31m  Safety: check ./log/make-safety.log\033[0m\n"; \
	$(call remove_esc_secs,./log/make-safety.log); exit $$rc; }

gitleaks: ## Check secrets (https://github.com/zricethezav/gitleaks)
	${INFO} "Gitleaks starting..."
	-@gitleaks detect --path=. --report=./log/gitleaks-report.json  --verbose

security: ## Guard with Bandit and Safety recursively
	make j2 bandit safety

warnings: ## Find temporary fixes, possible issues, etc
	${INFO} "Warnings checking..."
	@grep --color="always" \
	--exclude-dir=.direnv \
	--exclude-dir=.git \
	--exclude-dir=.mypy_cache \
	--exclude-dir=.story \
	--exclude-dir=data \
	--exclude-dir=log \
	--exclude=".vocabulary*" \
	--exclude=Makefile \
	--exclude="tmp.*" \
	--exclude="notes.*" \
	--exclude="*.md" \
	--ignore-case \
	--line-number \
	--recursive \
	--with-filename \
	--word-regexp \
	. \
	--regexp '#\s*chmod -w .envrc\|fixme\|issue\|problem\|nosec\|refactorme'
	@python -c "input(' everything is fine? ')"

check: ## Full check recursively
	make pyspelling lint mypy security warnings

ifeq (ch, $(RULE_NAME))
	PY_FILE := $(ARGS)
	$(eval $(PY_FILE):;@true)
endif
ch: flake mypy spell bandit $(PY_FILE) ## Full check PY_FILE
	@make safety warnings

all: makecheck shellcheck gitleaks check ## Extra full check recursively

## ------------ versions --------------
.PHONY: versions

versions: ## Display versions of Chrome, Chromedriver, Selenium
	@	# Windows Chrome:
	-${INFO} "(Windows) Chrome $(shell ls "/mnt/c/Program Files (x86)/Google/Chrome/Application/" | head -1)"
	@	# Linux Chrome:
	-${INFO} "(Linus) $(shell /usr/bin/google-chrome --version)"

	-${INFO} "$(shell "$(CURDIR)/parsers/request/driver/chrome/chromedriver" --version)"
	-${INFO} "Selenium $(shell "$(BIN_DIR)"/python -c "print(__import__('selenium').__version__)")"

## ------------ files --------------
.PHONY: diff note tmp recompile clean

diff: ## git/contrib/diff-highlight FILE1 FILE2
	@ $@ -u $(FIRST_ARG) $(SECOND_ARG) \
	| perl /usr/share/doc/git/contrib/diff-highlight/diff-highlight

note: ## Write notes to ./NOTE.tmp (press ^D to close stdin)
	@python -c "import sys;\
	f=open(sys.argv[1],'a');\
	f.write(''.join([i for i in sys.stdin]));\
	f.close()" NOTE.tmp

tmp: ## Create temp files
	@touch tmp.{TODO,g,notes,py,sh}

recompile: ## Recompile ./parsers/*
	@$(BIN_DIR)/python -m recompile ./parsers -q

clean: ## Remove Python cache
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

## ------------ WSL --------------
.PHONY: check_xserver_process_exist run_xlaunch xlaunch

check_xserver_process_exist:
	@powershell.exe get-process vcxsrv -ErrorAction SilentlyContinue \
	&& echo "success!" || { echo "failure!"; exit 1; }

# open XLaunch: Multiple windows -> Start no client -> Check 'Disable access control' -> Finish
XLAUNCH_CONFIG := '"$(PWD)/.config/config.xlaunch"'
PROGRAM_DATA := /mnt/c/Progra~1
# https://sourceforge.net/projects/vcxsrv/
XLAUNCH := '"$(PROGRAM_DATA)/VcXsrv/xlaunch.exe"'
PARAMS := '-run', $(XLAUNCH_CONFIG)
NOHUP := $(PWD)/log/nohup.out

run_xlaunch:
	@nohup python3 -c "__import__('subprocess').call([$(XLAUNCH), $(PARAMS)])" > $(NOHUP) 2>&1 &
	@sleep 1; ps -o cmd | tail -4 | head -1

xlaunch: ## Start XServer (NOTE: start terminal as admin)
	make check_xserver_process_exist || make run_xlaunch


## ------------ local making --------------
# Override the project's Makefile tasks in local envirioment.
#
#   https://www.gnu.org/software/make/manual/html_node/Overriding-Makefiles.html
#   There can only be one recipe to be executed for a file.
#   If more than one rule gives a recipe for the same file,
#   make uses the last one given and prints an error message.
-include [Mm]akefile.local
# .gitignore already contains this.
