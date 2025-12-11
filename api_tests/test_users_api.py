import requests
import pytest

BASE_URL = "https://reqres.in/api"


def test_get_users_list():
    """GET /users - список пользователей возвращается и не пустой."""
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
    """GET /users/2 - существующий пользователь возвращается корректно."""
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
    """GET /users/23 - несуществующий пользователь -> 404."""
    response = requests.get(f"{BASE_URL}/users/23")

    if response.status_code == 403:
        pytest.skip("Reqres.in returned 403 (blocked in this environment)")

    assert response.status_code == 404
    # для 404 reqres.in возвращает пустое тело {}


def test_create_user():
    """POST /users - успешное создание пользователя."""
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
