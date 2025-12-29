"""Centralized project configuration.

Override via env vars:
- PW_BASE_URL
- PW_USERNAME
- PW_PASSWORD
- PW_TIMEOUT_MS
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _getenv(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None or value.strip() == "" else value


def _getenv_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str
    password: str
    timeout_ms: int


settings = Settings(
    base_url=_getenv("PW_BASE_URL", "https://demo.applitools.com/"),
    username=_getenv("PW_USERNAME", "test_user"),
    password=_getenv("PW_PASSWORD", "test_password"),
    timeout_ms=_getenv_int("PW_TIMEOUT_MS", 30_000),
)
