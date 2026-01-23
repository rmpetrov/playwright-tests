# Execution modes

This project supports environment-based configuration for local development and CI.
All settings are centralized in `config.py`.

## Test suites

The project contains two independent test suites:

| Suite | Location | Dependencies | Playwright required |
|-------|----------|--------------|---------------------|
| UI tests | `tests/` | pytest, playwright | Yes |
| API tests | `api_tests/` | pytest, requests | No |

API tests do not depend on Playwright and can be executed without browser installation.

## Running tests locally

### API tests

```bash
pytest api_tests -v
```

No Playwright or browser installation required.

### UI tests

```bash
pytest tests -v
```

Runs with headed browser by default (`ENV=local`).

### UI tests in headless mode

```bash
ENV=ci pytest tests -v --browser=chromium
```

## Environment profiles

| Profile | Headless | Use case |
|---------|----------|----------|
| `ENV=local` (default) | No | Local development, debugging |
| `ENV=ci` | Yes | CI pipelines, headless execution |

## Configuration overrides

Individual settings can be overridden via environment variables:

| Variable | Description |
|----------|-------------|
| `PW_BASE_URL` | Application base URL |
| `PW_USERNAME` | Test user username |
| `PW_PASSWORD` | Test user password |
| `PW_TIMEOUT_MS` | Default timeout in milliseconds |
| `PW_HEADLESS` | Override headless mode (true/false) |
| `PW_SLOW_MO_MS` | Slow down execution for debugging |

Example:
```bash
PW_TIMEOUT_MS=60000 pytest tests -v
```

## CI job structure

GitHub Actions runs API and UI tests in separate parallel jobs:

| Job | Dependencies | Command |
|-----|--------------|---------|
| `api-tests` | `requirements-api.txt` | `pytest -v api_tests` |
| `ui-tests` | `requirements-ui.txt` + Playwright | `pytest -v tests --browser=<matrix>` |

- API tests run without Playwright installation
- UI tests run in headless mode with `ENV=ci`
- Each job uploads its own artifacts (HTML reports, Allure results)

## Timeouts

A global default timeout is applied to all Playwright pages via an autouse fixture.
Controlled by `PW_TIMEOUT_MS` (default: 30000ms).

## Authentication state

UI tests reuse authenticated storage state to avoid repeated logins:

- Generated once per test session
- Stored in `.auth/` (gitignored)
- Speeds up test execution
