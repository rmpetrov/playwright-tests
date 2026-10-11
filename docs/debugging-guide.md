# Debugging Guide

## Failing UI Run Locally

Start the bundled app and export the local URL and matching demo credentials as shown in
[execution commands](execution.md#local-commands). This overrides a stale external target in
`.env`. Reproduce without retries and with the Make target's
report/artifact flags:

```bash
make test-ui-chromium EXTRA_PYTEST_ARGS="-k empty_state"
```

Inspect `html-report/ui/index.html`, then open a retained trace:

```bash
python -m playwright show-trace test-results/<test-directory>/trace.zip
```

For an empty-dashboard failure, check that navigation used `/app.html?scenario=empty`, the
empty-state message is visible, and the table has no rows. For authentication failures, inspect
redirects and cookies; `.auth/storage_state_<browser>.json` is regenerated each pytest session.
Do not change expectations simply to make a failure pass.

The plugin records standard `page` and `authorized_page` contexts. The two browser-restart
tests launch persistent contexts manually and currently lack automatic traces/videos/screenshots
and standard-page Allure attachments. Re-run these directly with headed settings:

```bash
ENV=local PW_HEADLESS=false pytest -v tests/test_auth_session.py -k restart --browser=chromium
```

## Failing CI Run

- Download `html-report-ui-<browser>` and inspect test/setup errors.
- Inspect `test-results-<browser>` for available traces, videos, and screenshots.
- Allure results include best-effort screenshot, page HTML, URL, and console logs for failures
  in test bodies using standard/authorized pages.
- Check `local-app-log-<browser>` and the readiness step when the app cannot start.
- The job summary records browser, readiness state, and artifact names.
- API failures have `html-report-api` and `allure-results-api` artifacts; local feedback tests
  start their own isolated server without Playwright.

Artifacts may be absent when installation/setup fails before tests run. The public Pages site
contains only the last fully successful `main` run, so use the failed workflow's artifacts.

## Local Output Locations

| Output | Path |
|---|---|
| API HTML report (`make test-api`) | `html-report/api/index.html` |
| UI HTML report (UI Make targets) | `html-report/ui/index.html` |
| Allure input | `allure-results-api/`, `allure-results-ui/` |
| Playwright failure artifacts | `test-results/` |

Direct pytest commands require explicit report/artifact flags. Sequential local browser runs
replace UI HTML and Playwright output; preserve evidence before another run. Allure results
accumulate across runs.

## App Issue vs Fixture or Assertion Issue

`local-app.log` is created by CI shell redirection and contains startup output and exceptions.
The bundled server suppresses per-request access logs, so it cannot show response bodies or
prove which routes were served. Locally, capture startup output with
`python -m local_app > local-app.log 2>&1` when needed.

Compare browser/network evidence and actual API response bodies with the deterministic
[test data](test-data.md). Setup/teardown-only failures suggest fixture or environment issues;
a loaded page with mismatched expected text suggests an assertion/data discrepancy.
