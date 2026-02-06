# Flaky Test Policy

## Purpose
This policy defines how flaky tests are handled in this repository to keep CI reliable without hiding product or test issues.

## Principles
- Flakiness is treated as a defect, not a normal state.
- Retries are a short-term mitigation, not a fix.
- Every flaky test must have ownership and a tracked remediation task.

## CI Retry Configuration
- Scope: UI test job only (`tests/` with Playwright)
- Reruns: `1`
- Delay between reruns: `2` seconds
- API tests do not use retries to preserve strict contract validation

## Marker Usage
- `@pytest.mark.flaky`: test is known unstable and under active investigation
- `@pytest.mark.quarantine`: test is excluded from blocking gates until fixed

## Workflow
1. Detect flaky behavior from CI history or repeated non-deterministic failures.
2. Open an issue and assign an owner.
3. Mark the test as `flaky` only if root cause is not yet fixed.
4. Stabilize and remove the marker after verification.
5. If impact is high and fix is not immediate, move test to `quarantine` with a follow-up issue.

## Exit Criteria
A flaky test is considered resolved when:
- it passes consistently in repeated local runs;
- it passes across all CI browsers without retry-triggered failures;
- the `flaky` or `quarantine` marker is removed.

## Anti-Patterns
- Increasing retry counts to make pipelines appear green
- Leaving flaky markers without a tracked issue
- Using quarantine as permanent storage for failing tests
