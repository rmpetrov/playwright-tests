import requests

def test_get_users():
    response = requests.get("https://reqres.in/api/users?page=2")
    assert response.status_code == 200

    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

def test_create_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "Hello",
        "body": "This is an API test",
        "userId": 1
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Hello"
    assert "id" in data

def test_update_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    payload = {
        "id": 1,
        "title": "Updated title",
        "body": "Updated content",
        "userId": 1
    }

    response = requests.put(url, json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated title"
    assert data["body"] == "Updated content"

def test_delete_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.delete(url)
    assert response.status_code == 200 or response.status_code == 204
