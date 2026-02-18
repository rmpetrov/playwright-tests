# Execution Modes

This repository supports local and CI execution with shared config from `config.py`.

## Test Suites
| Suite | Location | Main dependencies | Playwright required |
|---|---|---|---|
| UI | `tests/` | `pytest`, `playwright`, `pytest-playwright` | Yes |
| API | `api_tests/` | `pytest`, `requests`, `responses`, `pydantic` | No |

## Environment Profiles
| Profile | Headless | Typical use |
|---|---|---|
| `ENV=local` | No | local debugging |
| `ENV=ci` | Yes | CI-like execution |

## Local Commands
Install optional CI retry plugin for parity:
```bash
pip install "pytest-rerunfailures>=14,<17"
```

Start the bundled local UI app (default UI target):
```bash
make serve
```

### API tests
```bash
pytest -v api_tests -m "not quarantine"
```

### UI tests (single browser)
```bash
ENV=ci make test-ui-chromium
```

UI test command with retry flags (same as CI):
```bash
ENV=ci make test-ui-chromium EXTRA_PYTEST_ARGS="--reruns=1 --reruns-delay=2"
```

### UI tests (all browsers)
```bash
ENV=ci make test-ui-all
```

To run against the legacy external demo target without code changes:
```bash
PW_BASE_URL=https://demo.applitools.com/ make test-ui-chromium
```

## CI Stages (`.github/workflows/tests.yml`)
1. `lint`
- Runs `ruff check .`
- Runs `ruff format --check .`

2. `api-tests`
- Installs API dependencies
- Runs `pytest -v api_tests -m "not quarantine" --html=... --alluredir=...`
- Uploads HTML and Allure artifacts (`if: always()`)

3. `ui-tests`
- Depends on `api-tests`
- Runs matrix on `chromium`, `firefox`, `webkit`
- Starts `python3 -m local_app` and waits for `GET /health == ok`
- Runs `make test-ui-<matrix> EXTRA_PYTEST_ARGS="--reruns=1 --reruns-delay=2"`
- Uploads artifacts (`if: always()`)
- Validates report structure and deploys `html-report` to `gh-pages` from Chromium job

## Flaky Handling
- `flaky` marker: known unstable test under investigation
- `quarantine` marker: non-blocking test excluded from gating runs
- Retry scope: UI stage only, one rerun with 2-second delay
- Governance details: `docs/flaky_policy.md`

## Configuration Overrides
| Variable | Purpose |
|---|---|
| `PW_BASE_URL` | application base URL |
| `PW_USERNAME` | login username |
| `PW_PASSWORD` | login password |
| `PW_TIMEOUT_MS` | default Playwright timeout |
| `PW_HEADLESS` | force headless mode |
| `PW_SLOW_MO_MS` | add Playwright slow motion |
