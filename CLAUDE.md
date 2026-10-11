# Project context and development conventions

## Scope and architecture

This is an existing Python 3.13 / pytest / Playwright test project. Preserve its page objects,
fixtures, test intent, and negative-path coverage; make focused changes rather than rewrites.

- `local_app/`: deterministic standard-library HTTP application. Login, protected dashboard,
  logout, Remember Me cookies, three fixed transactions, and `?scenario=empty`.
  `POST /api/feedback` has real HTTP success and validation/error checks.
- `pages/`: `LoginPage` and `DashboardPage`, with reusable actions, assertions, and Allure steps.
- `tests/`: UI login, session persistence, populated and empty dashboard tests.
- `api_tests/clients/` and `api_tests/schemas/`: requests client and Pydantic models.
- `api_tests/test_users_api.py`: ReqRes-shaped responses intercepted by `responses`;
  no calls to the external ReqRes service.
- `api_tests/test_local_app_api.py`: real HTTP against an isolated local server started
  by the API session fixture on an OS-assigned port; no browser or manual server required.
- Root `conftest.py`: checks `flaky` metadata (`reason`, `issue`, `owner`).
- `pytest.ini`: repository import path, strict markers, and registered suite/selection markers.

The UI suite depends on the bundled app's DOM and session behavior. `PW_BASE_URL` can point
at another instance of that app; the old Applitools demo is not a compatible full-suite target.
The local application is a test fixture, not a production authentication implementation.

## Setup and commands

Use Python 3.13, matching CI and the compiled dependency files:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-api.txt -r requirements-ui.txt -r requirements-dev.txt
python -m playwright install
export PW_USERNAME=test_user PW_PASSWORD=test_password
LOCAL_APP_HOST=127.0.0.1 LOCAL_APP_PORT=8000 make serve
```

Keep the app running in one terminal and run checks in another activated terminal:

```bash
export PW_BASE_URL=http://127.0.0.1:8000
export PW_USERNAME=test_user PW_PASSWORD=test_password
make lint                         # lint and formatting validation, no formatting edits
make test-api                     # API tests, HTML report, Allure results
make test-ui-chromium              # headless UI; retains Playwright artifacts on failure
make test-ui-all                   # Chromium, Firefox, WebKit, sequentially
make test-ui-chromium EXTRA_PYTEST_ARGS=""  # disable retries during investigation
pytest -v tests/test_login.py --browser=chromium --headed
pytest -v tests -m auth --browser=firefox
pytest -v -m smoke                 # needs both dependency sets and a running UI app
```

`make test-ui` accepts `BROWSER`; all UI Make targets use `ENV=ci`. When installed,
`pytest-rerunfailures` enables one UI rerun with a two-second delay by default.
API tests have no retries. CLI artifact flags are set in the Makefile, not `pytest.ini`.

## Configuration

`config.py` loads `.env` before constructing immutable `settings`; exported environment
variables take precedence. An existing `.env` can redirect tests to another app unless
`PW_BASE_URL` is exported explicitly as in the commands above. The CLI server reads exported
variables rather than `.env`; use matching credentials in both terminals. Copy `.env.example`
only if no local `.env` needs preserving. Never commit `.env`
or authentication state.

- `ENV=local` (default): headed; `ENV=ci`: headless.
- `PW_BASE_URL`, `PW_USERNAME`, `PW_PASSWORD`, `PW_TIMEOUT_MS`, `PW_HEADLESS`, `PW_SLOW_MO_MS`.
- Playwright `--headed` and `--slowmo` override defaults for plugin-managed browser launches.
- `LOCAL_APP_HOST` and `LOCAL_APP_PORT` configure `python -m local_app`.
- `LOCAL_APP_SECRET` overrides the app's demonstration cookie-signing secret.

## UI fixtures and diagnostics

`tests/conftest.py` defines:

- `page`: unauthenticated pytest-playwright page, with base URL and default timeout.
- `auth_storage_state_path`: performs a Remember Me login once per browser per pytest session;
  rebuilds `.auth/storage_state_<browser>.json` each session.
- `authorized_page`: isolated authenticated context created through the plugin's `new_context`,
  so CLI trace/video/screenshot options apply.
- `dashboard_page` and `empty_dashboard_page`: navigate to populated/empty dashboard scenarios.
- Autouse fixtures: default timeout, browser console capture, and best-effort Allure screenshot,
  HTML, and URL attachments on test-body failures for standard/authorized pages.

Browser-restart tests deliberately launch persistent contexts directly. They currently do not
use the plugin artifact recorder or the standard-page Allure attachments; use a focused rerun
and browser inspection to investigate them.

## Dependencies

- Edit `requirements-api.in` and `requirements-ui.in` for direct test dependencies.
- UI requirements are constrained by the API lockfile; they do **not** include all API/reporting
  dependencies. Install both compiled files for UI or combined runs.
- Do not hand-edit generated `requirements-*.txt`. Compile with Python 3.13, API first:

```bash
python -m piptools compile --strip-extras -o requirements-api.txt requirements-api.in
python -m piptools compile --strip-extras -o requirements-ui.txt requirements-ui.in
```

Avoid blanket upgrades. Ruff is pinned consistently in `requirements-dev.txt`, pre-commit,
and CI; update those together. pip-tools and pre-commit themselves are developer tools.

## Reporting and CI

Lint, API, and the three UI browser jobs run independently. Each test job installs its own
dependencies; pip caching reuses downloads, not installed packages. UI jobs install only their
matrix browser. Failed tests remain failed even when artifacts are uploaded with `always()`.

Only a successful push to `main`, after lint, API, and all UI jobs pass, assembles and uploads the official
Pages artifact. A dependent `deploy-pages` job deploys through `configure-pages` and `deploy-pages`,
with only `pages: write` and `id-token: write` permissions and the `github-pages` environment.
Repository Pages Source must be **GitHub Actions**, not a publishing branch. PRs retain artifacts
without publishing. The report site includes API and all three UI browser reports.

Local outputs:

- `html-report/api/index.html`, `html-report/ui/index.html`
- `allure-results-api/`, `allure-results-ui/`
- `test-results/` for plugin-managed failures

Sequential local browser runs overwrite the UI HTML report and Playwright output;
Allure results accumulate. Use separate output directories when preserving multiple runs.
Allure CLI must be installed separately. `make report-allure` runs **API tests only** and
builds `allure-report/`; view UI results with `allure serve allure-results-ui`.

See [execution](docs/execution.md), [debugging](docs/debugging-guide.md),
[test data](docs/test-data.md), and [flaky policy](docs/flaky_policy.md).
