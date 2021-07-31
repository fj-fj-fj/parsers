PARSER = ./discontinued_tech/parser.py

parse:
	python3 -i $(PARSER)

html:
	python3 $(PARSER) --save
