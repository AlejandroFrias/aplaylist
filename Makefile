.PHONY: help
help:
	@echo 'Usage:'
	@echo
	@echo '    make [target]'
	@echo
	@echo 'Targets:'
	@echo
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/^/    /' -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

.PHONY: lint
lint: venv  ## Run linter
	@source venv/bin/activate && flake8 --exclude venv --max-line-length 100 .

.PHONY: server
server: venv  ## Run django server
	@source venv/bin/activate && ./manage.py runserver

.PHONY: shell_plus
shell_plus: venv  ## Run django shell_plus
	@source venv/bin/activate && ./manage.py shell_plus

.PHONY: clean
clean:  ## Delete compiled python files
	find . -name "__pycache__" -delete

.PHONY: teardown
teardown: clean  ## Delete virtual environment
	test -d venv && rm -fr venv

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || python -m venv venv
	venv/bin/pip install -Ur requirements.txt
	touch venv/bin/activate
