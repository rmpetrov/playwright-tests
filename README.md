# Playwright + pytest quality validation project

![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)

This repository is a practical UI and API validation project built with Playwright and pytest. It is designed to show how automated checks can support software quality, regression confidence, reproducible execution, and failure troubleshooting, not just browser automation in isolation.

## Quick links
- CI workflow: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
- Published reports: https://rmpetrov.github.io/playwright-tests/

## Scope
- UI and API validation in one repository, focused on repeatable checks for critical workflows and response handling
- Quality-focused automation with a bundled local app for realistic auth/session checks

## What this project validates
- Login and session workflow behavior, including protected dashboard access, logout, Remember Me persistence, validation, and keyboard submission
- Dashboard behavior, including overview cards, populated and empty transaction states, row consistency, and amount formatting
- API client behavior for user endpoints, including GET and POST flows, status handling, and schema validation with Pydantic
- Negative and error-path handling, including 404 responses, 500 responses, malformed JSON, and validation errors

## Testing scope
- UI tests run against a bundled local app by default at `http://127.0.0.1:8000`
- The local app includes deterministic auth/session, empty-dashboard, and local API validation scenarios
- API tests use mocked HTTP responses for deterministic execution
- CI runs linting, API checks, and UI checks across Chromium, Firefox, and WebKit
- Marker-based selection (`ui`, `api`, `auth`, `smoke`) and controlled retries keep runs practical and easy to target

## Why it matters
- Deterministic local UI and mocked API flows keep runs repeatable and easier to troubleshoot
- Reports, Allure results, and Playwright failure artifacts improve debugging
- Page objects, fixtures, schemas, and supporting docs keep the suite maintainable and easier to extend
- The project demonstrates regression-oriented checks that support release readiness rather than one-off demo automation

## Tools used
- Python, pytest, Playwright
- Requests, Responses, Pydantic
- Ruff, Allure, pytest-html
- GitHub Actions, GitHub Pages

## CI and debugging visibility
- API jobs publish HTML and Allure artifacts
- UI jobs publish HTML reports, Playwright artifacts, and `local-app.log` for every browser job
- UI jobs add a compact summary with the browser under test, local app readiness, and artifact names
- GitHub Pages exposes the generated report site from successful CI runs
- The workflow validates report output before deployment to keep report publishing reliable

## How to run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-api.txt -r requirements-ui.txt
playwright install
make serve
```

In another terminal:

```bash
make test-api
make test-ui-chromium
```

Useful alternatives:

```bash
make lint
make test-ui-all
make report-allure
pytest -v tests -m auth --browser=chromium
pytest -v -m smoke
```

Optional alternate target: `PW_BASE_URL=https://demo.applitools.com/ make test-ui-chromium`

## Project structure
```text
playwright-tests/
  local_app/             # Deterministic local UI app used for repeatable runs
  pages/                 # Playwright page objects
  tests/                 # UI tests and fixtures
  api_tests/             # API clients, schemas, and tests
  docs/                  # Architecture, strategy, execution, flaky policy
  .github/workflows/     # CI pipeline and report publishing
```

## Documentation and proof
- [Execution modes and CI commands](docs/execution.md)
- [Architecture](docs/architecture.md)
- [Debugging guide](docs/debugging-guide.md)
- [Local app test data](docs/test-data.md)
- [Test strategy](docs/test_strategy.md)
- [Flaky test policy](docs/flaky_policy.md)
- [Workflow runs](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml)
