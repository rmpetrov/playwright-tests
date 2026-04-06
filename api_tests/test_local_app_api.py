"""Deterministic local app API tests for negative and error-handling coverage."""

from __future__ import annotations

import json

import pytest
import requests

pytestmark = [pytest.mark.api, pytest.mark.integration]


def _assert_json_response(response: requests.Response, expected_status: int) -> dict:
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}. Body={response.text}"
    )
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type.lower(), (
        f"Expected JSON response content type, got: {content_type}"
    )
    return response.json()


def _assert_error_response(
    response: requests.Response,
    expected_status: int,
    expected_code: str,
) -> dict:
    body = _assert_json_response(response, expected_status)
    error = body.get("error")
    assert isinstance(error, dict), f"Expected structured error object, got: {body}"
    assert error.get("code") == expected_code, (
        f"Expected error code '{expected_code}', got: {error}"
    )
    assert error.get("message"), f"Expected non-empty error message, got: {error}"
    assert isinstance(error.get("details"), list), f"Expected error details list, got: {error}"
    return body


def _feedback_url(base_url: str) -> str:
    return f"{base_url}/api/feedback"


def _detail_for_field(details: list[dict], field: str) -> dict | None:
    for detail in details:
        if detail.get("field") == field:
            return detail
    return None


def test_feedback_submission_accepts_valid_payload(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        json={
            "subject": "Account access",
            "message": "Need help reviewing a recent transaction.",
        },
        timeout=5,
    )

    body = _assert_json_response(response, 201)
    assert body["id"] == "feedback-demo-001"
    assert body["status"] == "accepted"
    assert body["subject"] == "Account access"
    assert body["messagePreview"] == "Need help reviewing a recent transaction"


def test_feedback_submission_rejects_missing_required_fields(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        json={"subject": "Account access"},
        timeout=5,
    )

    body = _assert_error_response(response, 400, "validation_error")
    details = body["error"]["details"]
    message_error = _detail_for_field(details, "message")
    assert message_error is not None, f"Expected message field error, got: {details}"
    assert message_error["issue"] == "required"


def test_feedback_submission_rejects_empty_values(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        json={"subject": "   ", "message": ""},
        timeout=5,
    )

    body = _assert_error_response(response, 400, "validation_error")
    details = body["error"]["details"]
    assert _detail_for_field(details, "subject") == {
        "field": "subject",
        "issue": "must not be empty",
    }
    assert _detail_for_field(details, "message") == {
        "field": "message",
        "issue": "must not be empty",
    }


def test_feedback_submission_rejects_invalid_field_types(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        json={"subject": 123, "message": ["invalid"]},
        timeout=5,
    )

    body = _assert_error_response(response, 400, "validation_error")
    details = body["error"]["details"]
    assert _detail_for_field(details, "subject") == {
        "field": "subject",
        "issue": "must be a string",
    }
    assert _detail_for_field(details, "message") == {
        "field": "message",
        "issue": "must be a string",
    }


def test_feedback_submission_rejects_malformed_json(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        data='{"subject": "Broken payload"',
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    _assert_error_response(response, 400, "malformed_json")


def test_feedback_submission_rejects_non_json_content_type(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        data="subject=Account access&message=Please call back",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=5,
    )

    _assert_error_response(response, 415, "unsupported_media_type")


def test_feedback_submission_rejects_non_object_json(local_app_api_base_url: str):
    response = requests.post(
        _feedback_url(local_app_api_base_url),
        data=json.dumps(["unexpected", "payload"]),
        headers={"Content-Type": "application/json"},
        timeout=5,
    )

    body = _assert_error_response(response, 400, "validation_error")
    assert body["error"]["details"] == [
        {
            "field": "body",
            "issue": "must be a JSON object",
        }
    ]
