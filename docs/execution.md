# Execution modes

This project supports multiple execution profiles controlled via environment variables.
All defaults and overrides are centralized in `config.py`.

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
