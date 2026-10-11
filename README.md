# Playwright + pytest UI and API validation

[![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml)

A Python 3.13 test project with a bundled deterministic HTTP application, Playwright page
objects, and requests clients validated with Pydantic. UI tests exercise real browser/session
behavior; API tests combine mocked user responses with real HTTP checks of the local app.
No external application or API service is required.

| Validation | Implemented checks |
|---|---|
| Login and sessions | Required fields, keyboard submission, protected routes, logout, Remember Me across browser restart |
| Dashboard | Overview cards, transaction headers/values/date and amount formats, populated and empty states |
| Mocked users API | GET/POST, 404, HTTP 500, missing fields and invalid response types |
| Local feedback API | 201 success, missing/empty/invalid fields, non-object and malformed JSON, unsupported content type |

**CI:** Ruff lint/format, API tests, and independent Chromium/Firefox/WebKit jobs.
Each browser job retains failure diagnostics and reports. See [workflow runs](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml)
and [published HTML reports](https://rmpetrov.github.io/playwright-tests/).
Published reports represent the latest successful `main` run; failed runs and PR evidence
remain in Actions artifacts.

## Run locally

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-api.txt -r requirements-ui.txt -r requirements-dev.txt
python -m playwright install
export PW_USERNAME=test_user PW_PASSWORD=test_password
LOCAL_APP_HOST=127.0.0.1 LOCAL_APP_PORT=8000 make serve
```

In another terminal, activate the same environment:

```bash
source .venv/bin/activate
export PW_BASE_URL=http://127.0.0.1:8000
export PW_USERNAME=test_user PW_PASSWORD=test_password
make lint
make test-api
make test-ui-chromium
make test-ui-all
```

API-only setup needs just `requirements-api.txt`; `make test-api` starts its own isolated
local server. The exports above target the bundled app even if an existing `.env` sets
`PW_BASE_URL` to another site: exported variables take precedence. Without the exports,
pytest loads that `.env` value and tests the other site. The server reads exported variables,
not `.env`; use matching credentials in both terminals. The external Applitools demo is
not a compatible full-suite target.
On Linux, install browser OS dependencies with `python -m playwright install --with-deps`.
See [execution modes](docs/execution.md) for profiles, markers, and overrides.

## Deterministic data and failure investigation

The dashboard has three fixed transactions; `?scenario=empty` renders the empty state.
User API tests intercept HTTP through `responses`; feedback tests call a fixture-owned
server on a free loopback port. Neither suite depends on third-party service availability.

`make test-ui-chromium` produces `html-report/ui/index.html` and `allure-results-ui/`.
Plugin-managed pages retain traces, videos, and screenshots in `test-results/` on failure.
For an empty-state failure, check the URL and rendered rows in the trace, then rerun with
`EXTRA_PYTEST_ARGS=""` to disable retries. Browser-restart tests use manual persistent
contexts and currently lack automatic plugin artifacts. See the [debugging guide](docs/debugging-guide.md).

## Structure and documentation

```text
local_app/        # Bundled HTTP app, session cookies, dashboard, feedback endpoint
pages/            # Login and dashboard page objects with Allure steps
tests/            # UI tests and browser/auth fixtures
api_tests/        # HTTP clients, Pydantic schemas, mocks and local integration tests
docs/             # Execution, architecture, strategy, data and debugging
.github/workflows/ # Independent quality checks and gated report publishing
```

- [Architecture](docs/architecture.md)
- [Execution and dependency management](docs/execution.md)
- [Debugging guide](docs/debugging-guide.md)
- [Local app test data](docs/test-data.md)
- [Test strategy](docs/test_strategy.md)
- [Flaky test policy](docs/flaky_policy.md)

Test dependencies are pinned in compiled lockfiles; UI runs require both API and UI files.
Ruff is shared across CI and pre-commit. Allure results are collected by pytest; viewing them
requires a separately installed Allure CLI. The local app is a test fixture; performance,
security, accessibility, and visual regression audits are outside this suite's scope.

For report deployment, set **Settings → Pages → Build and deployment → Source** to
**GitHub Actions**. The workflow uses official Pages deployment actions and the `github-pages`
environment; it does not push report commits to a publishing branch.
