PARSER_DIR := $(PWD)
README := $(PARSER_DIR)/README.md
TIME_LOG := $(PARSER_DIR)/.time.log
DATA := $(PARSER_DIR)/data


parse_links:
	@time -v -o "$(PARSER_DIR)/.time.log" \
	./.venv/bin/python3 "$(PARSER_DIR)/links_parser.py" zvk


check_status_codes:
	bash "$(PARSER_DIR)/status_code_checker.sh"


readme:
	@echo '```sh' > $(README) && \
	echo 'parsers/zvk/data/' >> $(README) && \
	tree $(DATA) | tail -n +2 >> $(README) && \
	echo '```' >> $(README) && \
	echo '#' >> $(README) && \
	echo '```sh' >> $(README) && \
	cat $(TIME_LOG) >> $(README) && \
	echo '```' >> $(README)


test:
	python3 -m doctest -v "$(PARSER_DIR)/_test_combinatorics.py"
