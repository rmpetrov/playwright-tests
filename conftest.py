"""Global pytest hooks shared across UI and API suites."""

from __future__ import annotations

import pytest

_REQUIRED_FLAKY_FIELDS = ("reason", "issue", "owner")


def pytest_collection_modifyitems(session, config, items):
    """Validate flaky marker metadata for governance and traceability."""
    errors: list[str] = []

    for item in items:
        for marker in item.iter_markers(name="flaky"):
            missing = [field for field in _REQUIRED_FLAKY_FIELDS if not marker.kwargs.get(field)]
            if not missing:
                continue
            errors.append(f"{item.nodeid}: missing flaky metadata fields: {', '.join(missing)}")

    if errors:
        formatted = "\n".join(f"- {error}" for error in errors)
        raise pytest.UsageError(
            "Invalid flaky marker usage. Each flaky marker must include "
            "reason, issue, and owner.\n"
            f"{formatted}"
        )
