PARSER_DIR := "$(PWD)/parsers/zvk"


parse_links:
	@time -v -o "$(PARSER_DIR)/.parsers.log" \
	./.venv/bin/python3 "$(PARSER_DIR)/links_parser.py" zvk


check_status_codes:
	bash "$(PARSER_DIR)/status_code_checker.sh"
