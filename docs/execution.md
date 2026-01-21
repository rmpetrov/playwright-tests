# Execution modes

This project supports multiple execution profiles designed for local development and CI environments.
All defaults and overrides are centralized in `config.py`.

## Test types

The project contains two independent test types:

- **UI tests** — Playwright-based browser tests (`tests/`)
- **API tests** — HTTP-level tests using `requests` (`api_tests/`)

API tests do not depend on Playwright or browser execution and can be run independently.

## ENV=local (default)

Use this mode for local development and debugging.

- Browser typically runs **headed** (UI visible)
- Best for test development and investigation

Run:
```bash
pytest -q
```

## ENV=ci

Use this mode in CI environments where no display server is available.

- Runs **headless** for stability and performance
- Matches GitHub Actions configuration

Run:
```bash
ENV=ci pytest -q
```

## UI tests

Run UI tests locally:
```bash
pytest tests -v
```

Run UI tests in CI mode:
```bash
ENV=ci pytest tests -v --browser=chromium
```

## API tests

Run API tests:
```bash
pytest api_tests -v
```

API tests run without browser context and do not require Playwright.

## Configuration overrides

Individual settings can be overridden via environment variables:

- `PW_BASE_URL`
- `PW_USERNAME`
- `PW_PASSWORD`
- `PW_TIMEOUT_MS`
- `PW_HEADLESS`
- `PW_SLOW_MO_MS`

Example:
```bash
PW_TIMEOUT_MS=60000 PW_HEADLESS=true pytest -q
```

## Timeouts

A global default timeout is applied to all Playwright pages via an autouse fixture:

- Ensures consistent behavior across tests
- Avoids relying on Playwright defaults

The value is controlled by `PW_TIMEOUT_MS`.

## Authentication state

Authentication storage state is generated once and reused:

- Avoids repeated UI logins
- Speeds up test execution
- Keeps tests focused on application behavior

## CI execution

In CI environments:
- UI tests run in headless mode
- Execution uses the `ENV=ci` profile
- Test reports and artifacts are collected for post-run analysis
