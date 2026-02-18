"""Centralized project configuration.

Profiles: local (default), ci
Select via ENV env var: ENV=local or ENV=ci

Override individual values via env vars:
- PW_BASE_URL
- PW_USERNAME
- PW_PASSWORD
- PW_TIMEOUT_MS
- PW_HEADLESS (true/false)
- PW_SLOW_MO_MS
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


def _getenv_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in ("true", "1", "yes", "y", "on")


# Profile-specific defaults (only for fields that differ between environments)
_PROFILES = {
    "local": {
        "headless": False,
        "slow_mo_ms": 0,
    },
    "ci": {
        "headless": True,
        "slow_mo_ms": 0,
    },
}

_env = _getenv("ENV", "local").strip().lower()
_profile = _PROFILES.get(_env, _PROFILES["local"])


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str
    password: str
    timeout_ms: int
    headless: bool
    slow_mo_ms: int


settings = Settings(
    base_url=_getenv("PW_BASE_URL", "http://127.0.0.1:8000"),
    username=_getenv("PW_USERNAME", "test_user"),
    password=_getenv("PW_PASSWORD", "test_password"),
    timeout_ms=_getenv_int("PW_TIMEOUT_MS", 30_000),
    headless=_getenv_bool("PW_HEADLESS", _profile["headless"]),
    slow_mo_ms=_getenv_int("PW_SLOW_MO_MS", _profile["slow_mo_ms"]),
)
