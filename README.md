# Playwright + pytest quality validation project

![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)

This repository is a practical UI and API validation project built with Playwright and pytest. It is designed to show how automated checks can support software quality, regression confidence, reproducible execution, and failure troubleshooting, not just browser automation in isolation.

## Quick links
- CI workflow: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
- Published reports: https://rmpetrov.github.io/playwright-tests/

## Scope
- UI and API validation in one repository, focused on repeatable checks for critical workflows and response handling
- Quality-focused automation that emphasizes regression coverage, maintainable structure, and clear failure visibility

## What this project validates
- Login workflow behavior, including successful authentication, missing-field validation, password masking, Remember Me behavior, and keyboard submission
- Dashboard behavior, including overview cards, transaction table presence, header consistency, column structure, and amount formatting
- API client behavior for user endpoints, including GET and POST flows, status handling, and schema validation with Pydantic
- Negative and error-path handling, including 404 responses, 500 responses, and invalid API payloads

## Testing scope
- UI tests run against a bundled local app by default at `http://127.0.0.1:8000`
- API tests use mocked HTTP responses for deterministic execution
- CI runs linting, API checks, and UI checks across Chromium, Firefox, and WebKit
- Quarantine markers and controlled retries are used to keep gating runs practical and visible

## Why it matters
- The local app and mocked API flows make runs repeatable and easier to troubleshoot
- Published HTML reports, Allure results, and Playwright failure artifacts improve debugging visibility
- Page objects, fixtures, schemas, and supporting docs keep the suite maintainable and easier to extend
- The project demonstrates regression-oriented checks that support release readiness rather than one-off demo automation

## Tools used
- Python, pytest, Playwright
- Requests, Responses, Pydantic
- Ruff, Allure, pytest-html
- GitHub Actions, GitHub Pages

## CI and debugging visibility
- API jobs publish HTML and Allure artifacts
- UI jobs publish HTML reports plus Playwright traces, videos, and screenshots on failure
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
- [Test strategy](docs/test_strategy.md)
- [Flaky test policy](docs/flaky_policy.md)
- [Workflow runs](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml)
