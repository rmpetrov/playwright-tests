"""
API tests for user endpoints.

These tests use mocked HTTP responses for deterministic execution.
They validate request handling, status codes, and response schema via Pydantic.
"""

import pytest
import responses

from api_tests.clients.users_client import UsersClient
from api_tests.schemas.users import CreateUserRequest

BASE_URL = "https://reqres.in/api"

pytestmark = pytest.mark.api


@responses.activate
def test_get_users_list(users_client: UsersClient):
    """Test GET /users returns paginated user list with validated schema."""
    mock_response = {
        "page": 1,
        "per_page": 6,
        "total": 12,
        "total_pages": 2,
        "data": [
            {
                "id": 1,
                "email": "george.bluth@reqres.in",
                "first_name": "George",
                "last_name": "Bluth",
            },
            {
                "id": 2,
                "email": "janet.weaver@reqres.in",
                "first_name": "Janet",
                "last_name": "Weaver",
            },
        ],
    }
    responses.add(
        responses.GET,
        f"{BASE_URL}/users",
        json=mock_response,
        status=200,
    )

    result = users_client.get_users(page=1)

    assert result.page == 1
    assert result.per_page == 6
    assert result.total == 12
    assert len(result.data) == 2

    first_user = result.data[0]
    assert first_user.id == 1
    assert first_user.email == "george.bluth@reqres.in"
    assert first_user.first_name == "George"
    assert first_user.last_name == "Bluth"


@responses.activate
def test_get_single_user(users_client: UsersClient):
    """Test GET /users/{id} returns single user with validated schema."""
    mock_response = {
        "data": {
            "id": 2,
            "email": "janet.weaver@reqres.in",
            "first_name": "Janet",
            "last_name": "Weaver",
        }
    }
    responses.add(
        responses.GET,
        f"{BASE_URL}/users/2",
        json=mock_response,
        status=200,
    )

    result = users_client.get_user(user_id=2)

    assert result.data.id == 2
    assert result.data.email == "janet.weaver@reqres.in"
    assert result.data.first_name == "Janet"
    assert result.data.last_name == "Weaver"


@responses.activate
def test_get_single_user_not_found(users_client: UsersClient):
    """Test GET /users/{id} returns 404 for non-existent user."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/users/23",
        json={},
        status=404,
    )

    response = users_client.get_raw("/users/23")

    assert response.status_code == 404


@responses.activate
def test_create_user(users_client: UsersClient):
    """Test POST /users creates user and returns validated response."""
    mock_response = {
        "name": "Roman QA",
        "job": "QA Engineer",
        "id": "123",
        "createdAt": "2024-01-15T10:30:00.000Z",
    }
    responses.add(
        responses.POST,
        f"{BASE_URL}/users",
        json=mock_response,
        status=201,
    )

    request = CreateUserRequest(name="Roman QA", job="QA Engineer")
    result = users_client.create_user(request)

    assert result.name == "Roman QA"
    assert result.job == "QA Engineer"
    assert result.id == "123"
    assert result.createdAt == "2024-01-15T10:30:00.000Z"
