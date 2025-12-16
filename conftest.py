# conftest.py
import os
from datetime import datetime

import pytest


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
