VENV_BIN ?= .venv/bin
PYTEST ?= $(VENV_BIN)/pytest
RUFF ?= $(VENV_BIN)/ruff
ALLURE ?= allure
RERUN_ARGS := $(shell $(PYTEST) --help 2>/dev/null | grep -q -- '--reruns' && echo '--reruns=1 --reruns-delay=2')

.PHONY: lint test-api test-ui-chromium test-ui-all report-allure

lint:
	$(RUFF) check .
	$(RUFF) format --check .

test-api:
	$(PYTEST) -v api_tests -m "not quarantine"

test-ui-chromium:
	ENV=ci $(PYTEST) -v tests -m "not quarantine" --browser=chromium $(RERUN_ARGS) --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure

test-ui-all:
	@for browser in chromium firefox webkit; do \
		echo "Running UI tests on $$browser"; \
		ENV=ci $(PYTEST) -v tests -m "not quarantine" --browser=$$browser $(RERUN_ARGS) --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure || exit $$?; \
	done

report-allure:
	$(PYTEST) -v api_tests -m "not quarantine" --alluredir=allure-results
	$(ALLURE) generate allure-results -o allure-report --clean
