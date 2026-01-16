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

## Important Notes

- `.auth/` directory contains Playwright storage state with sensitive session data — never commit or modify
- `screenshots/` directory is auto-generated on test failures — gitignored
- pytest.ini configures `--tracing=retain-on-failure`, `--video=retain-on-failure`, `--screenshot=only-on-failure`
