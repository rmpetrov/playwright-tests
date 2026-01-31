"""Pydantic models for Users API responses."""

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str


class UsersListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[User]


class SingleUserResponse(BaseModel):
    data: User


class CreateUserRequest(BaseModel):
    name: str
    job: str


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str
