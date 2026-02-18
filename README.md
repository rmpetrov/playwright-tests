# Playwright Test Automation Portfolio

![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)

## 60-Second Evaluation Path
- Run locally:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-api.txt -r requirements-ui.txt && playwright install
make serve
# in another terminal:
make test-api test-ui-chromium
```
- CI results: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
- Published UI/API reports (GitHub Pages): https://rmpetrov.github.io/playwright-tests/
- Architecture + flaky policy: [`docs/architecture.md`](docs/architecture.md), [`docs/flaky_policy.md`](docs/flaky_policy.md)

## Scope
- UI + API automation in one repo (Playwright + pytest + requests)
- Deterministic suite with bundled local UI app, quarantine gates, and controlled retries
- CI artifacts (trace/video/screenshot, HTML + Allure)
- Reporting via GitHub Pages deployment

## Non-goals
- Testing production systems or live customer data
- Dependencies on unstable external services
- Long-running monitoring, load, or performance testing

## Quick Links
- Report portal: https://rmpetrov.github.io/playwright-tests/
- SDET showcase: https://github.com/rmpetrov/sdet-toolbox
- SDET toolbox reports: https://rmpetrov.github.io/sdet-toolbox/

## What to look at first
- CI pipeline and quality gates: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
- Stability governance (`flaky` + `quarantine`): [`docs/flaky_policy.md`](docs/flaky_policy.md)
- Framework design and boundaries: [`docs/architecture.md`](docs/architecture.md)

## Local UI App (Default)
- UI tests run against `http://127.0.0.1:8000` by default
- Routes:
  - `GET /` login page
  - `POST /login` credential validation (`302` to `/app.html` on success)
  - `GET /app.html` dashboard content for assertions
  - `GET /health` readiness endpoint (`ok`)
- To run against the old demo site without code changes:
```bash
PW_BASE_URL=https://demo.applitools.com/ make test-ui-chromium
```

## Proof
- Workflow runs: https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml
- GitHub Pages reports: https://rmpetrov.github.io/playwright-tests/
- PR history: https://github.com/rmpetrov/playwright-tests/pulls?q=is%3Apr

## Portfolio Summary
- Target role: SDET / QA Automation Engineer
- Focus: maintainable UI and API automation with CI/CD observability
- Tech stack: Playwright, Pytest, Requests, Responses, Pydantic, Allure, GitHub Actions
- Reliability controls: centralized timeouts, storage-state auth reuse, controlled UI retries, flaky governance

## Related Work
- SDET showcase: https://github.com/rmpetrov/sdet-toolbox
- SDET toolbox reports: https://rmpetrov.github.io/sdet-toolbox/

## CI Pipeline
The `Tests` workflow runs three stages:
1. `lint`: `ruff check` and `ruff format --check`
2. `api-tests`: API suite with HTML and Allure artifacts
3. `ui-tests`: Playwright suite on Chromium/Firefox/WebKit with retries, trace/video/screenshot artifacts, and GitHub Pages deployment

Pipeline behavior:
- UI stage depends on `api-tests`
- Quarantined tests are excluded from gating (`-m "not quarantine"`)
- UI retries are controlled (`--reruns=1 --reruns-delay=2`)

## Local Run
### 1. Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-api.txt -r requirements-ui.txt
playwright install
```

Optional (for exact retry parity with CI):
```bash
pip install "pytest-rerunfailures>=14,<17"
```

### 2. Use Make targets
```bash
make serve
# in another terminal:
make lint
make test-api
make test-ui-chromium
make test-ui-all
make report-allure
```

### 3. Equivalent raw commands
```bash
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest -v api_tests -m "not quarantine"
python3 -m local_app
ENV=ci PW_BASE_URL=http://127.0.0.1:8000 .venv/bin/pytest -v tests -m "not quarantine" --browser=chromium --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure --html=html-report/ui/index.html --self-contained-html --alluredir=allure-results-ui
ENV=ci PW_BASE_URL=http://127.0.0.1:8000 .venv/bin/pytest -v tests -m "not quarantine" --browser=chromium --reruns=1 --reruns-delay=2 --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure --html=html-report/ui/index.html --self-contained-html --alluredir=allure-results-ui
.venv/bin/pytest -v api_tests -m "not quarantine" --alluredir=allure-results
allure generate allure-results -o allure-report --clean
```

## Project Structure
```text
playwright-tests/
  local_app/             # Local deterministic UI app for test runs
  pages/                 # Playwright page objects
  tests/                 # UI tests and fixtures
  api_tests/             # API clients, schemas, and tests
  docs/                  # Architecture, execution, strategy, flaky policy
  .github/workflows/     # CI pipeline and report deployment
```

## Documentation
- [Execution modes and CI commands](docs/execution.md)
- [Architecture](docs/architecture.md)
- [Test strategy](docs/test_strategy.md)
- [Flaky test policy](docs/flaky_policy.md)
