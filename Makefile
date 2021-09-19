ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif


versions:
	@/usr/bin/google-chrome --version
	@"$(PWD)/driver/chrome/chromedriver" --version
	@printf 'Selenium '; python3 -c "print(__import__('selenium').__version__)"

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

# ------------------------------------ PARSERS ------------------------------------

# ---------------- zvk ----------------

include ./parsers/zvk/Makefile

zparse:
	@time -v -o "$(PARSER_DIR)/.parsers.log" ./.venv/bin/python3 . zvk

test:
	sudo make check_status_codes
