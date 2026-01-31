"""API tests configuration and fixtures."""

import pytest

from api_tests.clients.users_client import UsersClient

BASE_URL = "https://reqres.in/api"


@pytest.fixture
def users_client() -> UsersClient:
    """Create UsersClient instance for API tests."""
    return UsersClient(base_url=BASE_URL)
