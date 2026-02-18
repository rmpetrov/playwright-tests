VENV_BIN ?= .venv/bin
PYTHON ?= python3
PYTEST ?= pytest
RUFF ?= ruff
ALLURE ?= allure
RERUN_ARGS := $(shell $(PYTEST) --help 2>/dev/null | grep -q -- '--reruns' && echo '--reruns=1 --reruns-delay=2')
BROWSER ?= chromium
EXTRA_PYTEST_ARGS ?= $(RERUN_ARGS)

.PHONY: serve lint test-api test-ui test-ui-chromium test-ui-firefox test-ui-webkit test-ui-all report-allure

serve:
	$(PYTHON) -m local_app

lint:
	$(RUFF) check .
	$(RUFF) format --check .

test-api:
	$(PYTEST) -v api_tests -m "not quarantine"

test-ui:
	ENV=ci $(PYTEST) -v tests -m "not quarantine" --browser=$(BROWSER) --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure --html=html-report/ui/index.html --self-contained-html --alluredir=allure-results-ui $(EXTRA_PYTEST_ARGS)

test-ui-chromium:
	$(MAKE) test-ui BROWSER=chromium EXTRA_PYTEST_ARGS="$(EXTRA_PYTEST_ARGS)"

test-ui-firefox:
	$(MAKE) test-ui BROWSER=firefox EXTRA_PYTEST_ARGS="$(EXTRA_PYTEST_ARGS)"

test-ui-webkit:
	$(MAKE) test-ui BROWSER=webkit EXTRA_PYTEST_ARGS="$(EXTRA_PYTEST_ARGS)"

test-ui-all:
	$(MAKE) test-ui-chromium EXTRA_PYTEST_ARGS="$(EXTRA_PYTEST_ARGS)"
	$(MAKE) test-ui-firefox EXTRA_PYTEST_ARGS="$(EXTRA_PYTEST_ARGS)"
	$(MAKE) test-ui-webkit EXTRA_PYTEST_ARGS="$(EXTRA_PYTEST_ARGS)"

report-allure:
	$(PYTEST) -v api_tests -m "not quarantine" --alluredir=allure-results
	$(ALLURE) generate allure-results -o allure-report --clean
