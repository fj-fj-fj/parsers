# phony rules to [un]installs,update,upgrade apt,pip requirements,virtual environment, etc.

.PHONY: install-core
install-core: ## Install build dependencies (to build Python from source)
	@xargs -a <(sed 's/#.*//' "$$PROJECT_DIR"/requirements/apt/base.txt) sudo apt install

.PHONY: apt-install-all
apt-install-all: ## Install ./requirements/apt/*.txt
	@xargs -a <(sed 's/#.*//' "$$PROJECT_DIR"/requirements/apt/*.txt) sudo apt install

.PHONY: install-pyenv
install-pyenv: ## Install pyenv & add config lines to .bashrc
	${INFO} "Trying to install pyenv..."
	@curl --silent \
	--location https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
	${INFO} "pyenv installed successfully."
	${INFO} "Adding the commands to ~/.bashrc..."
	@echo -e "\n# Pyenv" >> ~/.bashrc \
	&& echo 'export PYENV_ROOT="$$HOME/.pyenv"' >> ~/.bashrc \
	&& echo 'command -v pyenv >/dev/null || export PATH="$$PYENV_ROOT/bin:$$PATH"' >> ~/.bashrc \
	&& echo 'if which pyenv > /dev/null; then eval "$$(pyenv init --path)"; fi' >> ~/.bashrc \
	&& echo 'if which pyenv > /dev/null; then eval "$$(pyenv virtualenv-init -)"; fi' >> ~/.bashrc
	${INFO} "pyenv versions:" && pyenv versions
	${INFO} "If you manually configure the environment:"
	${INFO} "- use 'make install-core' to install all the build dependencies."
	${INFO} "  * pyenv builds Python from source, which means you'll need build dependencies."
	${INFO} "- to install python use 'pyenv install <python_version>"
	${INFO} "- to exercise most global setting use: 'pyenv global <python_version>'"

.PHONY: del-pyenv
del-pyenv: ## Delete pyenv from $HOME & (optional) config lines from .bashrc
	@if read -t 10 -p "Delete pyenv configuration lines from .bashrc? (y/[n]) " response; then \
		if [[ "$${response}" =~ ^[yY]([eE][sS])*$$ ]]; then \
			sed -i.bak '\^# Pyenv^d' "$$HOME/.bashrc" \
			&& sed -i '\^export PYENV_ROOT="$$HOME/.pyenv"^d' "$$HOME/.bashrc" \
			&& sed -i '\^command -v pyenv >/dev/null || export PATH="$$PYENV_ROOT/bin:$$PATH"^d' "$$HOME/.bashrc" \
			&& sed -i '\^if which pyenv > /dev/null; then eval "$$(pyenv init --path)"; fi^d' "$$HOME/.bashrc" \
			&& sed -i '\^if which pyenv > /dev/null; then eval "$$(pyenv virtualenv-init -)"; fi^d' "$$HOME/.bashrc"; \
			printf "\e[1;33mpyenv entries from .bashrc deleted (.bashrc.bak created)\n\e[0m"; \
		fi \
	else \
		echo -e "\nInput timed out"; \
		exit 1; \
	fi
	@[[ -d "$$HOME/.pyenv" ]] && rm -rf "$$HOME/.pyenv"
	${SUCCESS} "pyenv deleted."

.PHONY: create-venv
create-venv:  ## Create v.environment with pyenv (make 'create-venv v=PY_VERSION')
	@[[ "$$v" ]] && pyenv virtualenv "$$v" ".$$PROJECT_NAME" \
	&& pyenv local ".$$PROJECT_NAME" \
	|| ( echo -en "\a"; ${ERROR} "Usage: make create-venv v=3.x.x"; exit 1; )
	${SUCCESS} "Virtual environment created."
	${INFO} "Local Python version: $$(pyenv virtualenv-prefix)"
	${INFO} "Current virtual environment: $$(pyenv prefix)"
	${INFO} "To install requirements.txt use 'make pip-install'"
	${INFO} "To upgrade requirements.txt use 'make pip-upgrade'"

.PHONY: upgrade-python
upgrade-python: ## Install latest Python version with pyenv
	${INFO} "pyenv updating..."
	@pyenv update
	${INFO} "Installing latest Python version..."
	@pyenv install 3:latest
	${SUCCESS} "Latest versions: ($$(pyenv --version) | python $$(pyenv latest 3))"
	@pyenv versions

.PHONY: upgrade-venv
upgrade-venv: ## Create v.environmet with latest Python (with backup to ~/bak)
	${INFO} "Virtual environment creating..."
	@mkdir --parents ~/bak/pyenv/versions \
	&& cp --recursive "$$VENV" ~/bak/pyenv/versions \
	&& rm --recursive --force "$$VENV" \
	&& pyenv virtualenv $$(pyenv latest 3) ".$$PROJECT_NAME" \
	#                   ^^^^^^^^^^^^^^^^^^                   \
	# if desired version not found, try replacing it manually \
	# if wanted version not known, replace it with <wanted> \
	&& pyenv local ".$$PROJECT_NAME"
	${SUCCESS} "Virtual environment created."
	${INFO} "Local Python version: $$(pyenv virtualenv-prefix)"
	${INFO} "Current virtual environment: $$(pyenv prefix)"

.PHONY: del-venv
del-venv: ## Delete v.environment (see 'revenv' rule)
	${INFO} "Deleting $$(pyenv virtualenv-prefix)"
	@pyenv virtualenv-delete $$(pyenv prefix) && rm .python-version
	${SUCCESS} "Virtual environment deleted."

.PHONY: revenv
revenv: ## Return v.environment from the previous 'upgrade-venv'
	${INFO} "Reinitializing virtual environment (previous 'upgrade-venv')..."
	@py_version="$$( \
		~/bak/pyenv/versions/."$$PROJECT_NAME"/bin/python -c \
		'from platform import python_version; print(python_version())' \
	)" \
	&& cp -R ~/bak/pyenv/versions/."$$PROJECT_NAME" $$(pyenv prefix) \
	&& pyenv virtualenv $$py_version ".$$PROJECT_NAME"
	${SUCCESS} "Virtual environment created."

.PHONY: upgrade
upgrade: upgrade-python upgrade-venv ## make upgrade-python upgrade-venv

.PHONY: pip-install
pip-install: ## Install requirements.txt
	${INFO} "Updating pip..."
	@$$(pyenv prefix)/bin/pip install -U pip
	${INFO} "Installing requirements..."
	@$$(pyenv prefix)/bin/pip install -r requirements.txt
	${SUCCESS} "$$($$VENV/bin/pip --version)"

.PHONY: pip-upgrade
pip-upgrade: ## Upgrade pip & requirements.txt
	${INFO} "Upgrading pip..."
	@$$VENV/bin/pip install -U pip
	${INFO} "Upgrading requirements..."
	@$$VENV/bin/pip install -r <(pip freeze) --upgrade
	${SUCCESS} "$$($$VENV/bin/pip --version)"

.PHONY: setup
setup: install-pyenv ## Download latest Python, create v.environment, install reqs
	@latest_py_version=$$(pyenv latest --known 3) \
	&& pyenv install $$latest_py_version \
	&& pyenv local $$latest_py_version \
	make create-venv v=$$latest_py_version \
	pip-install
	${SUCCESS} "Setup finished."

.PHONY: setup-full
setup-full: install-core setup ## make install-core setup

.PHONY: all test clean
