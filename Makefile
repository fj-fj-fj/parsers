ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif


versions: # Chrome, Chromedriver, Selenium
	@/usr/bin/google-chrome --version
	@"$(PWD)/driver/chrome/chromedriver" --version
	@printf 'Selenium '; python3 -c "print(__import__('selenium').__version__)"

cloc:
	$@ --exclude-list-file=.clocignore .

list:
	@grep '^[^#[:space:]].*:' Makefile

# ------------------------------------ XSERVER ------------------------------------
check_xserver_process_exist:
	@powershell.exe get-process vcxsrv -ErrorAction SilentlyContinue \
	&& echo "success!" || { echo "failure!"; exit 1; }


NOHUP := $(PWD)/config/nohup.out
XLAUNCH_CONFIG := '"$(PWD)/config/config.xlaunch"'
PROGRAM_DATA := /mnt/c/Progra~1
XLAUNCH := '"$(PROGRAM_DATA)/VcXsrv/xlaunch.exe"'
PARAMS := '-run', $(XLAUNCH_CONFIG)
run_xlaunch:
	@nohup python3 -c "__import__('subprocess').call([$(XLAUNCH), $(PARAMS)])" > $(NOHUP) 2>&1 &
	@sleep 1; ps -o cmd | tail -4 | head -1

xlaunch:
	make check_xserver_process_exist || make run_xlaunch
# ----------------------------------------------------------------------------------

PYTHON := ./.venv/bin/python3

# ------------------------------------ PARSERS ------------------------------------

# -------------- proxy ----------------

PROXY_DIR := $(PWD)/request/proxy
px: PARSER := $(PROXY_DIR)/parser.py
checkpx: PARSER := $(PROXY_DIR)/checker.py
px: parse
checkpx: parse

# -------------------------------------

parse:
	@time -vo $(shell dirname $(PARSER))/log/.time.log "$(PYTHON)" -i "$(PARSER)"


include ./parsers/zvk/Makefile

ZVK_TARGET := $(filter $(firstword $(MAKECMDGOALS)), zparse readme check_status_codes check_correct_params generate_urls see_multi_params_files clean_up wc1 wc2 wc3 wc9)
# ifeq ($(firstword $(MAKECMDGOALS)),$(filter $(firstword $(MAKECMDGOALS)),\
# 	zparse readme check_status_codes check_correct_params generate_urls see_multi_params_files clean_up wc1 wc2 wc3 wc9))
# ifdef $(ZVK_TARGET)
ifeq ($(firstword $(MAKECMDGOALS)),$(filter $(firstword $(MAKECMDGOALS)),check_correct_params))
	PYTHON := ./.venv/bin/python3

	PARSER_DIR := $(PWD)/parsers/zvk
	DATA := $(PARSER_DIR)/data
	README := $(PARSER_DIR)/README.md
	TIME_LOG := $(PARSER_DIR)/.time.log
endif

zparse:
	@time -v -o "$(TIME_LOG)" ./.venv/bin/python3 . zvk

readme:

check_status_codes: # `sudo make check_status_codes`
check_correct_params: # `sudo make check_status_codes`

generate_urls:

see_multi_params_files:

clean_up:

wc1:
wc2:
wc3:
wc9:


# --------------- wiki ---------------

include ./parsers/wiki/Makefile

# ifeq ($(firstword $(MAKECMDGOALS)),$(filter $(firstword $(MAKECMDGOALS)),wparse))
WIKI_TARGET := $(filter $(firstword $(MAKECMDGOALS)),wparse tail-f wt count_animals)
ifdef $(WIKI_TARGET)
	PYTHON := ./.venv/bin/python3

	PARSER_DIR := $(PWD)/parsers/wiki
	PARSER := "$(PARSER_DIR)/parse_wikipedia.py"

	TAIL_F := $(PARSER_DIR)/tail_f_logs.sh
	TIME_LOG := $(PARSER_DIR)/.time.log

	DATA := $(PARSER_DIR)/data
	ANIMALS_LIST := $(DATA)/animals_list
endif

wparse:

tail-f:

wt:
	nohup make wparse > "$(PARSER_DIR)/nohup.out" 2>&1 &
	sleep 2; make --ignore-errors tail-f

count_animals:
