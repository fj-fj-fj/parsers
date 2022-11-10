PYTHON := ./.venv/bin/python3

PARSER_DIR := $(PWD)
PARSER := "$(PARSER_DIR)/parse_wikipedia.py"

TAIL_F := $(PARSER_DIR)/tail_f_logs.sh
TIME_LOG := $(PARSER_DIR)/.time.log

DATA := $(PARSER_DIR)/data
ANIMALS_LIST := $(DATA)/animals_list


wparse:
	@time -v -o "$(TIME_LOG)" "$(PYTHON)" -i "$(PARSER)" wiki


tail-f:
	$(TAIL_F)
# NOTE: to see logs: make wparse, CTRL + Z, make tail-f


count_animals:
	@date
	@python3 -c 'with open("$(ANIMALS_LIST)") as f:\
	print(sum((len(v) for v in eval(f.read()).values())))'
