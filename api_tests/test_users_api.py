"""
API tests for user endpoints.

These tests use mocked HTTP responses for deterministic execution.
They validate request handling, status codes, and response schema.
"""

import pytest
import requests
import responses

BASE_URL = "https://reqres.in/api"

pytestmark = pytest.mark.api


@responses.activate
def test_get_users_list():
    """Test GET /users returns paginated user list with expected schema."""
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

    response = requests.get(f"{BASE_URL}/users", params={"page": 1})

    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    assert isinstance(body["data"], list)
    assert len(body["data"]) > 0

    first_user = body["data"][0]
    assert "id" in first_user
    assert "email" in first_user
    assert "first_name" in first_user
    assert "last_name" in first_user


@responses.activate
def test_get_single_user():
    """Test GET /users/{id} returns single user with expected fields."""
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

    response = requests.get(f"{BASE_URL}/users/2")

    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    user = body["data"]

    assert user["id"] == 2
    assert "email" in user
    assert "first_name" in user
    assert "last_name" in user


@responses.activate
def test_get_single_user_not_found():
    """Test GET /users/{id} returns 404 for non-existent user."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/users/23",
        json={},
        status=404,
    )

    response = requests.get(f"{BASE_URL}/users/23")

    assert response.status_code == 404


@responses.activate
def test_create_user():
    """Test POST /users creates user and returns expected fields."""
    payload = {"name": "Roman QA", "job": "QA Engineer"}
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

    response = requests.post(f"{BASE_URL}/users", json=payload)

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "id" in body
    assert "createdAt" in body
