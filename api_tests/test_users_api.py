import pytest
import requests

BASE_URL = "https://reqres.in/api"

pytestmark = pytest.mark.api


def test_get_users_list():
    response = requests.get(f"{BASE_URL}/users", params={"page": 1})

    if response.status_code == 403:
        pytest.skip("Reqres.in returned 403 (blocked in this environment)")

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


def test_get_single_user():
    response = requests.get(f"{BASE_URL}/users/2")

    if response.status_code == 403:
        pytest.skip("Reqres.in returned 403 (blocked in this environment)")

    assert response.status_code == 200

    body = response.json()
    assert "data" in body
    user = body["data"]

    assert user["id"] == 2
    assert "email" in user
    assert "first_name" in user
    assert "last_name" in user


def test_get_single_user_not_found():
    response = requests.get(f"{BASE_URL}/users/23")

    if response.status_code == 403:
        pytest.skip("Reqres.in returned 403 (blocked in this environment)")

    assert response.status_code == 404


def test_create_user():
    payload = {"name": "Roman QA", "job": "QA Engineer"}

    response = requests.post(f"{BASE_URL}/users", json=payload)

    if response.status_code == 403:
        pytest.skip("Reqres.in returned 403 (blocked in this environment)")

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "id" in body
    assert "createdAt" in body
