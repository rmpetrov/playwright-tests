"""Users API client with typed methods."""

import requests

from api_tests.clients.base_client import BaseAPIClient
from api_tests.schemas.users import (
    CreateUserRequest,
    CreateUserResponse,
    SingleUserResponse,
    UsersListResponse,
)


class UsersClient(BaseAPIClient):
    """Client for Users API endpoints."""

    def get_users(self, page: int = 1) -> UsersListResponse:
        """Get paginated list of users."""
        return self.get("/users", UsersListResponse, params={"page": page})

    def get_user(self, user_id: int) -> SingleUserResponse:
        """Get single user by ID."""
        return self.get(f"/users/{user_id}", SingleUserResponse)

    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        """Create a new user."""
        return self.post("/users", CreateUserResponse, json=request.model_dump())

    def get_user_raw(self, user_id: int) -> requests.Response:
        """Return raw response for GET /users/{id} (for status-code assertions)."""
        return self.get_raw(f"/users/{user_id}")
