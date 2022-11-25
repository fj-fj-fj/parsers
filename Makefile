BIN_DIR := $$VENV/bin

# ------------------------- Parsers -------------------------

# -------------- proxy ----------------
px: PARSER := $(PWD)/src/parsers/proxy/__init__.py
px: parse


parse:
	@time -vo $(shell dirname $(PARSER))/.time.log "$(BIN_DIR)/python" -i "$(PARSER)"


# ------------------------- Scripts -------------------------

# --------- ./scrits/* ------------

# Passing arguments to "make create_template_structure" or "make new"
ifeq ($(filter $(new) $(create_template_structure), $(firstword $(MAKECMDGOALS))),)
  # use the rest as arguments for "new"
  NEW_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(NEW_ARGS):;@:)
endif

create_template_structure:
	@./scripts/create_parsers_template_structure $(NEW_ARGS)

# Usage:
#   make new <DIRECORY_NAME>
#   make -- new --help
new: create_template_structure


# --------- makescripts ------------

# Press <Ctrl+D> to close stdin
note:
	python -c "import sys;\
	f=open(sys.argv[1],'a');\
	f.write(''.join([i for i in sys.stdin]));\
	f.close()" NOTE.tmp


# -------------------------- Linting -------------------------

flake8:
	@$(BIN_DIR)/$@

mypy:
	@$(BIN_DIR)/$@ --show-error-codes

check:
	make flake8 mypy


# -------------------- Versions/Updating --------------------

versions: # Display the versions of Chrome, Chromedriver, Selenium
	@/usr/bin/google-chrome --version
	@"$(PWD)/src/driver/chrome/chromedriver" --version
	@printf 'Selenium '; $(PYTHON) -c "print(__import__('selenium').__version__)"


# --------------------- no-src execution ---------------------

cloc:
	$@ --exclude-list-file=.clocignore .


# ---------------------- Configuration ----------------------

# ------------ XServer --------------
check_xserver_process_exist:
	@powershell.exe get-process vcxsrv -ErrorAction SilentlyContinue \
	&& echo "success!" || { echo "failure!"; exit 1; }


NOHUP := $(PWD)/src/config/nohup.out
XLAUNCH_CONFIG := '"$(PWD)/src/config/config.xlaunch"'
PROGRAM_DATA := /mnt/c/Progra~1
XLAUNCH := '"$(PROGRAM_DATA)/VcXsrv/xlaunch.exe"'
PARAMS := '-run', $(XLAUNCH_CONFIG)

run_xlaunch:
	@nohup python3 -c "__import__('subprocess').call([$(XLAUNCH), $(PARAMS)])" > $(NOHUP) 2>&1 &
	@sleep 1; ps -o cmd | tail -4 | head -1

xlaunch:
	make check_xserver_process_exist || make run_xlaunch


ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif
