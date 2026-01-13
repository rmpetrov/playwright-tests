# conftest.py
from __future__ import annotations

import os
from datetime import datetime

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
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(settings.username, settings.password, remember=True)
    return page


@pytest.fixture
def dashboard_page(authorized_page) -> DashboardPage:
    dashboard = DashboardPage(authorized_page)
    dashboard.assert_loaded()
    return dashboard
