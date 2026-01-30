# conftest.py

"""Pytest configuration and shared fixtures."""

from __future__ import annotations

from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

load_dotenv()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the item for access in fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def apply_default_timeout(request):
    """Apply consistent timeout from settings to all UI test pages."""
    if "page" not in request.fixturenames:
        return
    page = request.getfixturevalue("page")
    page.set_default_timeout(settings.timeout_ms)


@pytest.fixture(autouse=True)
def capture_console_logs(request):
    """Capture browser console logs for UI tests and attach on failure."""
    if "page" not in request.fixturenames:
        yield
        return

    console_messages: list[str] = []

    def handle_console(msg):
        console_messages.append(f"[{msg.type}] {msg.text}")

    page = request.getfixturevalue("page")
    page.on("console", handle_console)

    yield

    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed and console_messages:
        log_text = "\n".join(console_messages[-100:])  # Limit to last 100 messages
        allure.attach(
            log_text,
            name="browser_console",
            attachment_type=allure.attachment_type.TEXT,
        )


@pytest.fixture(autouse=True)
def allure_attach_on_failure(request):
    """Attach screenshot, page HTML, and URL to Allure on UI test failure."""
    yield

    if "page" not in request.fixturenames:
        return

    rep = getattr(request.node, "rep_call", None)
    if not rep or not rep.failed:
        return

    try:
        page = request.getfixturevalue("page")
    except Exception:
        return

    # Attach screenshot
    try:
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass

    # Attach page HTML (truncate if too large)
    try:
        html_content = page.content()
        if len(html_content) > 500_000:  # 500KB limit
            html_content = html_content[:500_000] + "\n<!-- truncated -->"
        allure.attach(
            html_content,
            name="page_html",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception:
        pass

    # Attach current URL
    try:
        allure.attach(
            page.url,
            name="page_url",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception:
        pass


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
    browser = playwright.chromium.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo_ms,
    )
    context = browser.new_context(base_url=settings.base_url)
    page = context.new_page()
    page.set_default_timeout(settings.timeout_ms)

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
