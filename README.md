# Playwright UI Testing Project

![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)

---
## Portfolio summary
- Target role: SDET / QA Automation
- Focus: scalable UI + API automation, CI readiness, reporting, stability
- Stack: Playwright (Python), Pytest, Allure, GitHub Actions

---
## Why this project
I built this framework to demonstrate how I approach automation as an engineer, not just a test writer. It shows architecture decisions, reliability practices, and CI-ready execution with rich reporting.

## Test strategy summary
- Test levels: UI smoke/regression and API contract checks
- Coverage intent: critical user flows, UI stability, and API schema validation
- Data strategy: deterministic API responses via mocks for repeatable runs
- Execution: local headed runs for debugging, headless CI for reproducibility
- Observability: HTML reports, Allure, screenshots, video, trace on failure

## Quality gates (CI)
- Lint and format checks via Ruff
- API tests run independently before UI tests
- UI tests run in a 3-browser matrix (Chromium, Firefox, WebKit)
- HTML reports and Allure results published as artifacts
- Report validation step ensures deployable GitHub Pages output

## Design decisions
- Page Object Model to keep tests readable and maintainable
- Centralized fixtures for timeouts and auth state reuse
- Environment-based config to keep local and CI runs consistent
- Typed API client with Pydantic for schema-level validation

---
## Project highlights
-  UI automation with Playwright + Pytest (Page Object Model)
-  Environment-based configuration (`ENV=local | ci`)
-  CI-ready execution (headless runs in GitHub Actions)
-  Auth reuse via Playwright storage state (fast, stable tests)
-  Consistent timeouts applied via autouse fixture
-  UI + API tests in a single test framework
-  HTML reports published via GitHub Pages
-  Allure reporting with artifacts (screenshots, video, trace)
-  Code quality enforced via pre-commit (ruff: lint + format)

---

## What this framework demonstrates
This project demonstrates how I design and evolve a maintainable automation framework:

- **Test architecture**: clear separation of tests, page objects (POM), and fixtures
- **Stability & reliability**: centralized timeouts, deterministic auth setup, reduced flakiness
- **Configuration & portability**: same test suite runs locally and in CI with minimal changes
- **CI readiness**: headless execution, reproducible environment, test artifacts
- **Scalability mindset**: UI and API tests share the same tooling and conventions

---

## Features

### Cross-browser UI automation
Tests run in 3 browsers via CI matrix:
- **Chromium**
- **Firefox**
- **WebKit**

### Page Object Model (POM)
Clear separation of UI interactions into reusable page classes.

### API Tests
Lightweight API suite using `requests` with mocked HTTP responses for deterministic execution.

### Automatic screenshots, video & trace
All failures generate:
- Screenshots  
- Playwright videos  
- Playwright trace files  

### HTML report (pytest-html)
Latest reports auto-published via GitHub Pages:

- **Landing page:** https://rmpetrov.github.io/playwright-tests/
- **UI report:** https://rmpetrov.github.io/playwright-tests/ui/
- **API report:** https://rmpetrov.github.io/playwright-tests/api/

### Allure reporting
Local Allure report generation with full metadata:

```bash
pytest -v --alluredir=allure-results
allure serve allure-results
```

CI also uploads **allure-results** as artifacts for every browser.

---

## Project Structure

```text
my-playwright-tests/
  pages/
    login_page.py
    dashboard_page.py

  tests/
    conftest.py           # UI fixtures (Playwright)
    test_login.py
    test_dashboard.py

  api_tests/
    test_users_api.py     # Mocked HTTP tests

  config.py               # Environment-based settings
  pytest.ini
  requirements-api.in     # API deps source (pip-compile input)
  requirements-api.txt    # API deps pinned (pip-compile output)
  requirements-ui.in      # UI deps source (pip-compile input)
  requirements-ui.txt     # UI deps pinned (pip-compile output)
```
---

## Test Reporting Stack

### Pytest + pytest-html  
Generates static HTML reports.  
In CI, Chromium report is auto-deployed to GitHub Pages.

### Allure Framework  
Enterprise-grade reporting: steps, attachments, categories, timelines.

Local usage:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### GitHub Actions CI  
Pipeline includes:

- Python & Playwright installation  
- Matrix execution in 3 browsers  
- Storage of:
  - HTML reports  
  - Videos  
  - Traces  
  - Screenshots  
  - Allure results  
- Auto-deploy of HTML report

---

## How to Run Tests Locally

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

**For API tests only** (no Playwright required):
```bash
pip install -r requirements-api.txt
```

**For UI tests** (includes Playwright):
```bash
pip install -r requirements-api.txt -r requirements-ui.txt
playwright install
```

### 3. Run API tests

```bash
pytest -v api_tests
```

API tests use mocked HTTP responses and run without external dependencies.

### 4. Run UI tests

Local execution (headed browser):
```bash
pytest -v tests
```

CI-like execution (headless):
```bash
ENV=ci pytest -v tests
```

### 5. Generate Allure report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```
---
## Docs
- [Execution modes (local vs CI)](docs/execution.md)
- [Test strategy](docs/test_strategy.md)
- [Architecture](docs/architecture.md)
---
## Screenshots

### HTML Test Report (GitHub Pages)
![HTML Report Screenshot](docs/images/html_report_example.png)

### Allure Report Dashboard
![Allure Report Screenshot](docs/images/allure_report_example.png)

### Playwright Trace Viewer
![Trace Viewer Screenshot](docs/images/dashboard_example.png)


---

## 📈 Future Enhancements

- More negative UI scenarios  
- API client layer abstraction  
- Allure step decorators & severity tags  
- Dockerized test environment  


---

**Author:** Roman Petrov  
**GitHub:** https://github.com/rmpetrov
