"""Base API client with typed request methods."""

from typing import TypeVar

import requests
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseAPIClient:
    """Base client for REST API interactions with Pydantic validation."""

    def __init__(self, base_url: str, session: requests.Session | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def get(self, path: str, response_model: type[T], **kwargs) -> T:
        """Perform GET request and validate response against Pydantic model."""
        response = self.session.get(f"{self.base_url}{path}", **kwargs)
        response.raise_for_status()
        return response_model.model_validate(response.json())

    def post(self, path: str, response_model: type[T], **kwargs) -> T:
        """Perform POST request and validate response against Pydantic model."""
        response = self.session.post(f"{self.base_url}{path}", **kwargs)
        response.raise_for_status()
        return response_model.model_validate(response.json())

    def get_raw(self, path: str, **kwargs) -> requests.Response:
        """Perform GET request and return raw response (for error cases)."""
        return self.session.get(f"{self.base_url}{path}", **kwargs)
