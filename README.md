# Playwright Test Automation Portfolio

![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)

## 60-Second Evaluation Path
- Run locally:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-api.txt -r requirements-ui.txt && playwright install
make test-api test-ui-chromium
```
- CI results: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
- Published UI/API reports (GitHub Pages): https://rmpetrov.github.io/playwright-tests/
- Architecture + flaky policy: [`docs/architecture.md`](docs/architecture.md), [`docs/flaky_policy.md`](docs/flaky_policy.md)

## Scope
- UI + API automation in one repo (Playwright + pytest + requests)
- Deterministic suite with quarantine gates and controlled retries
- CI artifacts (trace/video/screenshot, HTML + Allure)
- Reporting via GitHub Pages deployment

## Non-goals
- Testing production systems or live customer data
- Dependencies on unstable external services
- Long-running monitoring, load, or performance testing

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

## Local Run (Detailed)
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

Use Make targets:
```bash
make lint
make test-api
make test-ui-chromium
make test-ui-all
make report-allure
```

## Project Structure
```text
playwright-tests/
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
