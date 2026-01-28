# CLAUDE.md

This document describes the project context, architecture, and development conventions.
It may also be used by AI-assisted tools (such as Claude Code) to better understand the codebase.

AI tools are treated as engineering assistants (review/refactor/help), not autonomous code authors.
All design decisions and final implementations are owned by the developer.

## Project Overview

Python + Pytest + Playwright test automation framework for https://demo.applitools.com banking demo app. Includes UI tests (Playwright) and API tests (requests library against reqres.in).

## Commands

```bash
# Run all tests
pytest -v

# Run UI tests only
pytest -m ui -v

# Run API tests only
pytest -m api -v

# Run single test file
pytest tests/test_login.py -v

# Run single test
pytest tests/test_login.py::test_successful_login -v

# Run with specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit

# Generate Allure report
pytest --alluredir=allure-results
allure serve allure-results

# Lint
ruff check .
ruff format .
```

## Architecture

### Page Object Model
- `pages/` — Page classes encapsulating UI interactions
- `LoginPage` — login form actions and assertions
- `DashboardPage` — dashboard page after login

### Test Structure
- `tests/` — UI tests (marked with `@pytest.mark.ui`)
- `api_tests/` — API tests (marked with `@pytest.mark.api`)

### Fixtures (conftest.py)
- `page` — Playwright page (from pytest-playwright)
- `authorized_page` — page with completed login
- `dashboard_page` — authorized page navigated to dashboard
- `screenshot_on_failure` — auto-captures screenshot on test failure

### Configuration
- `config.py` — Settings dataclass loaded from environment variables
- `.env` — local environment overrides (not committed)
- Environment variables: `PW_BASE_URL`, `PW_USERNAME`, `PW_PASSWORD`, `PW_TIMEOUT_MS`

## Dependency Management

This project uses `pip-tools` for reproducible dependency management.

### Source files (edit these)
- `requirements-api.in` — direct dependencies for API tests
- `requirements-ui.in` — direct dependencies for UI tests (includes API deps)
- `requirements-dev.txt` — dev tools (pip-tools, pre-commit, ruff)

### Compiled files (generated, do not edit manually)
- `requirements-api.txt` — pinned dependencies for API tests
- `requirements-ui.txt` — pinned dependencies for UI tests

### Updating dependencies
```bash
# Install pip-tools
pip install pip-tools

# Regenerate pinned requirements (API first, then UI)
python -m piptools compile --strip-extras -o requirements-api.txt requirements-api.in
python -m piptools compile --strip-extras -o requirements-ui.txt requirements-ui.in

# Upgrade all dependencies to latest versions
python -m piptools compile --upgrade --strip-extras -o requirements-api.txt requirements-api.in
python -m piptools compile --upgrade --strip-extras -o requirements-ui.txt requirements-ui.in
```

## Important Notes

- `.auth/` directory contains Playwright storage state with sensitive session data — never commit or modify
- `screenshots/` directory is auto-generated on test failures — gitignored
- Playwright CLI options (`--tracing`, `--video`, `--screenshot`) are set in CI workflow, not pytest.ini
