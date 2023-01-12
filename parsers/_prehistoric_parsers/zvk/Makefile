PARSER_DIR := $(PWD)
README := $(PARSER_DIR)/README.md
TIME_LOG := $(PARSER_DIR)/.time.log
DATA := $(PARSER_DIR)/data


parse_links:
	@time -v -o "$(PARSER_DIR)/.time.log" \
	./.venv/bin/python3 "$(PARSER_DIR)/links_parser.py" zvk


check_status_codes:
	bash "$(PARSER_DIR)/status_code_checker.sh"


check_correct_params:
	bash "$(PARSER_DIR)/correct_params_checker.sh" | tee $(PARSER_DIR)/check_correct_params.log


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


generate_urls:
	./.venv/bin/python3 "$(PARSER_DIR)/url_generator.py"


see_multi_params_files:
	python3 -c "from pathlib import Path;\
	print(*[fn.name for fn in Path('$(DATA)').glob('**/*') if fn.is_file() and fn.match('*_[0-9]')], sep='\n')"


clean_up:
	find "$(PARSER_DIR)" -name '*_[0-9]' -exec rm -f {} +


wc1:
	@wc -l `find $(DATA) -type f -iname "*" ! -iname "*_[0-9]" ! -iname "_all_parsed*"` | tail -1
	@wc -l `find $(DATA) -name "_all_parsed"`
wc2:
	@wc -l `find $(DATA) -type f -iname "*_2" ! -iname "_all_parsed_2"` | tail -1
	@wc -l `find $(DATA) -name "_all_parsed_2"`
wc3:
	@wc -l `find $(DATA) -type f -iname "*_3" ! -iname "_all_parsed_3"` | tail -1
	@wc -l `find $(DATA) -name "_all_parsed_3"`
wc9:
	@wc -l `find $(DATA) -type f -iname "*" ! -iname "_all_parsed*"` | tail -1
