# Debugging Guide

## Failing UI Run Locally
- Start the bundled app with `make serve`.
- Re-run a focused UI slice first, for example `ENV=ci pytest -v tests/test_dashboard.py --browser=chromium`.
- Open the HTML report in `html-report/ui/index.html`.
- Check Playwright artifacts in `test-results/` for the failing test:
  - `trace.zip`
  - `video.webm`
  - `*.png` screenshots
- Review `local-app.log` when the failure looks data- or routing-related.

## Failing CI Run
- Download the uploaded artifacts from the failed workflow run.
- Review the UI HTML report artifact first for test-level context.
- Inspect `test-results-<browser>` for Playwright traces, videos, and screenshots.
- Inspect `local-app-log-<browser>` to confirm whether the app started correctly and served the expected scenario.
- Use the UI job summary in GitHub Actions to confirm browser, readiness state, and artifact names.

## Report and Artifact Locations
- Local UI HTML report: `html-report/ui/index.html`
- Local API HTML report: `html-report/api/index.html`
- Allure input directories: `allure-results-ui/`, `allure-results-api/`
- Playwright artifacts on failure: `test-results/`
- Local app log in CI: uploaded as `local-app-log-<browser>`

## Using `local-app.log`
- Use it to confirm the local app started and remained healthy during a run.
- Check it when tests fail on redirects, protected routes, empty dashboard scenarios, or local API validation cases.
- If the app never became ready, inspect the readiness step and the last log lines first before looking at selectors.

## App Issue vs Test Issue
- Suspect an app issue when the route, response body, empty-state message, or API error payload is wrong in both the browser and the log.
- Suspect a fixture issue when failures happen before navigation or only in setup/teardown.
- Suspect a selector/assertion issue when the page is clearly loaded but the test expects stale text, row counts, or artifact paths.
- For dashboard scenarios, confirm whether the URL includes the intended switch such as `?scenario=empty` before changing assertions.
