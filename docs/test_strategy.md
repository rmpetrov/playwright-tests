# Test Strategy

## Purpose
This document describes the test strategy for this Playwright and Pytest portfolio project. It is written for SDET and QA Automation roles and focuses on maintainability, reliability, and CI readiness.

## Goals
- Validate critical user flows in the UI
- Verify API responses against schemas
- Keep tests deterministic and fast to run in CI
- Provide actionable artifacts for debugging failures

## Scope
In scope:
- UI smoke and regression checks for login and dashboard flows
- API contract checks with schema validation
- Negative checks for validation and error handling

Out of scope (for this portfolio version):
- Performance and load testing
- Security testing
- Accessibility audits
- Visual regression testing

## Test Types
- UI smoke: fast checks of the main user path
- UI regression: functional checks on dashboard data and formatting
- API contract: schema validation using Pydantic models
- Negative tests: invalid inputs and not found scenarios

## Coverage Focus
- Authentication flow and session behavior
- Dashboard visibility and core data presentation
- API request and response structure
- Error handling for missing or invalid resources

## Data Strategy
- UI tests use the demo site credentials from environment config
- API tests use mocked responses with deterministic data
- Shared config is centralized in `config.py`

## Environments
- Local: headed browser for fast debugging
- CI: headless browser with artifacts for traceability

## Reliability Practices
- Global Playwright timeout applied via autouse fixture
- Auth storage state reuse to reduce flaky logins
- Console logs, screenshots, video, and trace on failure
- Controlled UI retries in CI to mitigate transient browser issues
- Flaky handling governed by `docs/flaky_policy.md`

## Reporting
- HTML reports published to GitHub Pages
- Allure results captured with attachments
- CI artifacts include videos, traces, and screenshots

## Quality Gates
- Ruff lint and format checks
- API tests must pass before UI tests
- UI tests run on Chromium, Firefox, and WebKit

## Future Enhancements
- Add retry policy with explicit flaky marker
- Add integration tests against real APIs
- Add data builders for more complex test setup
