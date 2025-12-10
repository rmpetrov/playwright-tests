# Playwright UI Testing Project

This repository contains automated UI tests for the demo banking application  
👉 https://demo.applitools.com  
using **Python**, **Pytest**, and **Playwright**.

The goal of the project is to demonstrate clean test structure, Page Object Model (POM) usage, and basic reporting - similar to what is expected in real automation frameworks.

---

## Tech Stack

- Python 3.13+
- Playwright (synchronous API)
- Pytest
- Page Object Model (POM)
- Automatic screenshots on failure
- HTML reports via `pytest-html`

---

## Project Structure

```text
my-playwright-tests/
  pages/
    login_page.py        # POM for the login page
    dashboard_page.py    # POM for the main dashboard after login

  tests/
    test_login.py        # Smoke test for successful login
    test_dashboard.py    # Tests for dashboard widgets and transactions

  screenshots/           # Screenshots saved on test failures
  conftest.py            # Pytest & Playwright configuration
  pytest.ini
  requirements.txt
```

---

## How to Run Tests

### 1. Create and activate virtual environment (optional but recommended)

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.\.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 3. Run all tests

```bash
pytest -v
```

### 4. Generate HTML report

```bash
pytest --html=report.html --self-contained-html
```

The report will be saved as `report.html` in the project root.

---

## Future Improvements

- Negative login scenarios (empty fields, invalid credentials)
- Additional dashboard checks (filters, amounts, widgets)
- API test suite using a public API (e.g., reqres.in)
- GitHub Actions CI to run tests on each push

---

**Author:** Roman Petrov  
**GitHub:** https://github.com/rmpetrov