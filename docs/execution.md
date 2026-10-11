# Execution Modes

Use Python 3.13, matching the lockfile compiler, CI, and Ruff target version.

## Dependencies

| Suite | Installation | Server setup | Browser binaries |
|---|---|---|---|
| API | `python -m pip install -r requirements-api.txt` | Automatic fixture on a free loopback port | None |
| UI | `python -m pip install -r requirements-api.txt -r requirements-ui.txt` | `make serve` in another terminal | `python -m playwright install` |
| Development | `python -m pip install -r requirements-dev.txt` | None | None |

The UI source file constrains shared packages against the API lockfile; it does not include
API/reporting packages. Both lockfiles are required for UI tests. Retry support is pinned in
the UI lockfile. On Linux, use `python -m playwright install --with-deps` for OS libraries.

To regenerate locks, use an activated Python 3.13 environment with pip-tools, API first:

```bash
python -m piptools compile --strip-extras -o requirements-api.txt requirements-api.in
python -m piptools compile --strip-extras -o requirements-ui.txt requirements-ui.in
```

## Local Commands

```bash
make lint
make test-api
export PW_USERNAME=test_user PW_PASSWORD=test_password
LOCAL_APP_HOST=127.0.0.1 LOCAL_APP_PORT=8000 make serve  # keep running for UI tests
```

In another activated terminal (exports apply only to that shell):

```bash
export PW_BASE_URL=http://127.0.0.1:8000
export PW_USERNAME=test_user PW_PASSWORD=test_password
make test-ui-chromium
make test-ui-firefox
make test-ui-webkit
make test-ui-all
make test-ui BROWSER=firefox
```

All UI Make targets use `ENV=ci` and retain plugin-managed trace/video/screenshot artifacts
on failure. They enable one rerun with a two-second delay if the retry plugin is installed.
Disable retries during investigation:

```bash
make test-ui-chromium EXTRA_PYTEST_ARGS=""
```

Direct pytest selection (without automatic report/artifact flags):

```bash
pytest -v tests --browser=chromium --headed
ENV=ci pytest -v tests -m auth --browser=firefox
ENV=ci pytest -v tests/test_auth_session.py --browser=webkit
pytest -v api_tests
ENV=ci pytest -v -m smoke
```

Combined and smoke runs need both dependency sets and a running UI app. The API fixture
owns a separate server, so it can run while `make serve` is active. `PW_BASE_URL` can target
another instance of the bundled app; the legacy Applitools demo lacks required DOM/session
behavior and is not a supported full-suite target.

## Reports

- API Make target: `html-report/api/index.html`, `allure-results-api/`.
- UI Make targets: `html-report/ui/index.html`, `allure-results-ui/`, `test-results/`.
- Local sequential browser runs overwrite UI HTML/Playwright output; Allure results accumulate.
  To preserve separate runs, pass explicit `--html`, `--output`, and `--alluredir` paths to pytest.
- Allure CLI is separate from the Python plugin. `allure serve allure-results-ui` opens UI results;
  `make report-allure` runs API tests only and generates `allure-report/`.

## CI (`.github/workflows/tests.yml`)

1. `lint`, `api-tests`, and `ui-tests` run independently. Each job installs its dependencies;
   pip caching saves downloads rather than sharing an installed environment.
2. UI uses a fail-fast-disabled Chromium/Firefox/WebKit matrix. Each job installs only its
   browser, starts the bundled app, verifies `/health`, and runs the corresponding Make target.
3. Test jobs upload HTML and Allure artifacts even after failures. UI also uploads available
   Playwright outputs and `local-app.log`, and records readiness/artifact names in its summary.
4. `publish-reports` waits for successful lint, API, and every browser job, then downloads
   reports into distinct browser directories, checks non-empty files, and uploads the official
   Pages artifact. It runs only after successful checks on pushes to `main`, never PRs, with
   read-only repository permissions.
5. `deploy-pages` depends on that completed artifact job. It uses `configure-pages`,
   `deploy-pages`, and the `github-pages` environment, with only `pages: write` and
   `id-token: write`. No personal access token or report-branch push is used.
6. Workflow concurrency cancels superseded runs for the same ref. Matrix artifact names
   include the browser, preventing collisions.

The public report site shows the last successful main run. A failed run does not replace it;
inspect Actions artifacts and the workflow result for current failure evidence. Repository
GitHub Pages **Settings → Pages → Build and deployment → Source** must be **GitHub Actions**.
This is a one-time repository setting when migrating from branch publishing. Restrict the
`github-pages` deployment environment to `main`; any configured environment approval rules
still apply. Token-authenticated pushes do not trigger branch-based Pages builds, so the
workflow deploys the artifact directly.

## Configuration

`config.py` loads `.env` before building settings; exported values take precedence.
Copy `.env.example` for local overrides only if you do not already have a `.env` to preserve.
An existing `.env` with `PW_BASE_URL` pointing elsewhere redirects pytest to that site when no
export is present. The local command exports above force the bundled app URL and demo credentials
without changing your file. New terminals need those exports again. The CLI app reads exported environment variables;
when changing credentials for tests, export the same values in the server terminal.

| Variable | Purpose |
|---|---|
| `ENV` | `local` (headed default) or `ci` (headless default) |
| `PW_BASE_URL` | UI application URL; default `http://127.0.0.1:8000` |
| `PW_USERNAME`, `PW_PASSWORD` | Demo login credentials |
| `PW_TIMEOUT_MS` | Default timeout for UI actions |
| `PW_HEADLESS`, `PW_SLOW_MO_MS` | Browser launch defaults |
| `LOCAL_APP_HOST`, `LOCAL_APP_PORT` | CLI server bind address/port |
| `LOCAL_APP_SECRET` | Demo cookie-signing secret override |

Playwright `--headed` and `--slowmo` override plugin-managed browser defaults. Persistent
browser-restart tests use settings directly. `make test-ui` sets `ENV=ci` even when invoked
from a local profile; use direct pytest or `--headed` for headed investigation.

Markers: `ui`, `api`, `auth`, `smoke`, `integration`, `flaky`, `quarantine`.
Gating Make/CI runs exclude `quarantine`; see [flaky policy](flaky_policy.md) for metadata
and remediation rules. API tests are not retried.
