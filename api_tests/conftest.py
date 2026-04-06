"""API tests configuration and fixtures."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

from api_tests.clients.users_client import UsersClient
from local_app.server import DEFAULT_HOST, DEFAULT_PORT

USERS_API_BASE_URL = "https://reqres.in/api"
LOCAL_APP_API_BASE_URL = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def users_client() -> UsersClient:
    """Create UsersClient instance for API tests."""
    return UsersClient(base_url=USERS_API_BASE_URL)


@pytest.fixture(scope="session")
def local_app_server(tmp_path_factory):
    """Start the bundled local app for deterministic local API checks."""
    log_dir = tmp_path_factory.mktemp("local-app-api")
    with (log_dir / "local-app.log").open("w", encoding="utf-8") as log_file:
        process = subprocess.Popen(
            [sys.executable, "-m", "local_app"],
            cwd=PROJECT_ROOT,
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )

        try:
            for _ in range(30):
                try:
                    response = requests.get(f"{LOCAL_APP_API_BASE_URL}/health", timeout=1)
                    if response.status_code == 200 and response.text.strip() == "ok":
                        yield LOCAL_APP_API_BASE_URL
                        break
                except requests.RequestException:
                    pass
                time.sleep(0.5)
            else:
                raise RuntimeError("Local app did not become ready for API tests.")
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


@pytest.fixture
def local_app_api_base_url(local_app_server) -> str:
    return local_app_server
