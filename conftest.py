# conftest.py
import os
from datetime import datetime

import pytest


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Хук, который сохраняет результат выполнения теста в атрибуты:
    rep_setup, rep_call, rep_teardown.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request):
    """
    Авто-фикстура: если тест упал на этапе call,
    берём Playwright-фикстуру `page` и делаем свой скриншот
    в папку screenshots/.
    """
    yield

    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        # пытаемся достать page — он есть во всех UI-тестах
        try:
            page = request.getfixturevalue("page")
        except Exception:
            # не UI-тест, page нет — просто выходим
            return

        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{request.node.name}_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)

        page.screenshot(path=filepath, full_page=True)
        print(f"\n🧷 Скриншот сохранён: {filepath}")
