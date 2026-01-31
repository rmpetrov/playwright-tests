"""Users API client with typed methods."""

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
