"""API tests configuration and fixtures."""

from __future__ import annotations

from http.server import ThreadingHTTPServer
from threading import Thread

import pytest

from api_tests.clients.users_client import UsersClient
from local_app.server import DEFAULT_HOST, _Handler

USERS_API_BASE_URL = "https://reqres.in/api"


@pytest.fixture
def users_client():
    """Create UsersClient instance for API tests."""
    client = UsersClient(base_url=USERS_API_BASE_URL)
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def local_app_server():
    """Use an isolated port so API checks cannot hit an existing UI app."""
    server = ThreadingHTTPServer((DEFAULT_HOST, 0), _Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://{DEFAULT_HOST}:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.fixture
def local_app_api_base_url(local_app_server) -> str:
    return local_app_server
