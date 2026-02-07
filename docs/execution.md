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

### API tests
```bash
pytest -v api_tests -m "not quarantine"
```

### UI tests (single browser)
```bash
ENV=ci pytest -v tests -m "not quarantine" --browser=chromium --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure
```

UI test command with retry flags (same as CI):
```bash
ENV=ci pytest -v tests -m "not quarantine" --browser=chromium --reruns=1 --reruns-delay=2 --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure
```

### UI tests (all browsers)
```bash
for browser in chromium firefox webkit; do
  ENV=ci pytest -v tests -m "not quarantine" --browser="$browser" --tracing=retain-on-failure --video=retain-on-failure --screenshot=only-on-failure
done
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
- Runs `pytest -v tests -m "not quarantine" --browser=<matrix> --reruns=1 --reruns-delay=2 ...`
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
