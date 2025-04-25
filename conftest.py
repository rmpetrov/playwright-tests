import pytest
from playwright.sync_api import sync_playwright
import os

@pytest.fixture
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page

        # Скриншот при падении — только если test failed
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{request.node.name}.png"
            page.screenshot(path=screenshot_path)
            print(f"\n🧷 Скриншот сохранён: {screenshot_path}")

        browser.close()

# 🔄 Обязательный хук для фиксации статуса теста
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
