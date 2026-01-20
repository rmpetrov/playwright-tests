# Playwright UI Testing Project

![Tests](https://github.com/rmpetrov/playwright-tests/actions/workflows/tests.yml/badge.svg)

---
## Project highlights
- ✅ UI automation with Playwright + Pytest (Page Object Model)
- ✅ Environment-based configuration (`ENV=local | ci`)
- ✅ CI-ready execution (headless runs in GitHub Actions)
- ✅ Auth reuse via Playwright storage state (fast, stable tests)
- ✅ Consistent timeouts applied via autouse fixture
- ✅ UI + API tests in a single test framework
- ✅ HTML reports published via GitHub Pages
- ✅ Allure reporting with artifacts (screenshots, video, trace)
- ✅ Code quality enforced via pre-commit (ruff: lint + format)

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
Lightweight API suite using `requests` and public API `reqres.in`.

### Automatic screenshots, video & trace
All failures generate:
- Screenshots  
- Playwright videos  
- Playwright trace files  

### HTML report (pytest-html)
Latest report auto-published via GitHub Pages:

**https://rmpetrov.github.io/playwright-tests/**

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
    test_login.py
    test_dashboard.py

  api_tests/
    test_users_api.py

  screenshots/             
  test-results/            
  allure-results/          

  conftest.py
  pytest.ini
  requirements.txt
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

```bash
pip install -r requirements.txt
playwright install
```

### 3. Run tests

Local execution (default, headed):
```bash
pytest -v
```
CI-like execution (headless):
```bash
ENV=ci pytest -v
```

### 4. Run only UI tests

```bash
pytest tests/ -v
```

### 5. Run only API tests

```bash
pytest api_tests/ -v
```

### 6. Generate Allure report

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

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