ifndef VERBOSE
    MAKEFLAGS += --no-print-directory
endif

SHELL = /bin/bash

# Terminal output
GREEN := "\e[32m"
YELLOW := "\e[1;33m"
RED := "\e[1;31m"
NC := "\e[0m"
INFO := @bash -c 'printf $(YELLOW); echo "$$1"; printf $(NC)' MESSAGE
SUCCESS := @bash -c 'printf $(GREEN); echo "  $$1"; printf $(NC)' MESSAGE
ERROR := bash -c 'printf $(RED); echo "$$1"; printf $(NC)' MESSAGE

# Rule arguments
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
FIRST_ARG := $(word 2,$(MAKECMDGOALS))
FIRST_ARG_OR_CURRENT_DIR := $(word 2,$(MAKECMDGOALS) .)
SECOND_ARG := $(word 3,$(MAKECMDGOALS))
RULE_NAME := $(firstword $(MAKECMDGOALS))

# Function to remove escape sequences
# $(call remove_esc_secs,<path/to/file>)
define remove_esc_secs
	cat $(1) | sed -Ee 's/\x1b\[[0-9;]+m//g' > $(1)
endef


.DEFAULT_GOAL := _help

_help: #- Display helpers
	@sed -e '/#\{1\}-/!d; s/\\$$//; s/:[^#\t]*/:\t/; s/#\{1\}- *//' $(MAKEFILE_LIST)
	${INFO} "Use \`make help\` to see others"

# TODO: help: rule(blue) args(green) doccomment(white)
help: #- Display docstring
	@ awk 'BEGIN {FS = ":.*##"; printf "\nShort help:\n  make \033[36m<rule>\033[0m\n"} \
	/^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
	/^##/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

hlp: #- Display docstring with Docker (https://github.com/Xanders/make-help)
	@ cat $(MAKEFILE_LIST) | docker run --rm -i xanders/make-help


# makecheck requires Go and checkmake
# - https://go.dev/doc/install
# - https://github.com/mrtazz/checkmake#installation
makecheck: ## Lint makefile with Go,checkmake
	-@go run ~/go/src/github.com/mrtazz/checkmake --config=./.config/checkmake.ini .config/makefile-settings.mk
	-@go run ~/go/src/github.com/mrtazz/checkmake --config=./.config/checkmake.ini .config/makefile-build.mk
	-@go run ~/go/src/github.com/mrtazz/checkmake --config=./.config/checkmake.ini Makefile

.PHONY: _help help hlp makecheck all test clean
