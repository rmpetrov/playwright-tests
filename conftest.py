# conftest.py

"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pytest
from dotenv import load_dotenv

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

load_dotenv()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    yield

    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        try:
            page = request.getfixturevalue("page")
        except Exception:
            return

        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{request.node.name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        page.screenshot(path=filepath, full_page=True)
        print(f"\n🧷 Скриншот сохранён: {filepath}")


@pytest.fixture
def authorized_page(page):
    return page


@pytest.fixture
def dashboard_page(authorized_page) -> DashboardPage:
    authorized_page.goto("/app.html")
    dashboard = DashboardPage(authorized_page)
    dashboard.assert_loaded()
    return dashboard


AUTH_STATE_FILE = Path(".auth") / "storage_state.json"


@pytest.fixture(scope="session")
def auth_storage_state_path(playwright) -> str:
    """
    Creates an authenticated storage state once per test session.
    Tests will reuse it to avoid repeated UI logins.
    """
    AUTH_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Always regenerate for simplicity and to avoid stale sessions.
    browser = playwright.chromium.launch()
    context = browser.new_context(base_url=settings.base_url)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(settings.username, settings.password, remember=True)

    context.storage_state(path=str(AUTH_STATE_FILE))

    context.close()
    browser.close()

    return str(AUTH_STATE_FILE)


@pytest.fixture
def browser_context_args(auth_storage_state_path):
    return {
        "base_url": settings.base_url,
        "storage_state": auth_storage_state_path,
    }
