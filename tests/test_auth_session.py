import allure
import pytest

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, pytest.mark.auth, allure.feature("Auth Session")]


def _launch_persistent_page(playwright, browser_name: str, profile_dir):
    browser_type = getattr(playwright, browser_name)
    context = browser_type.launch_persistent_context(
        str(profile_dir),
        base_url=settings.base_url,
        headless=settings.headless,
        slow_mo=settings.slow_mo_ms,
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.set_default_timeout(settings.timeout_ms)
    return context, page


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_unauthenticated_dashboard_access_redirects_to_login(page):
    login_page = LoginPage(page)

    page.goto("/app.html")

    login_page.assert_loaded()
    login_page.assert_basic_ui_visible()


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_logout_revokes_dashboard_access(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login(settings.username, settings.password, remember=True)
    dashboard_page.assert_loaded()

    dashboard_page.logout()
    login_page.assert_loaded()

    page.goto("/app.html")
    login_page.assert_loaded()


@allure.severity(allure.severity_level.CRITICAL)
def test_remember_me_persists_auth_across_browser_restart(playwright, browser_name, tmp_path):
    profile_dir = tmp_path / "remember-me-profile"
    context, page = _launch_persistent_page(playwright, browser_name, profile_dir)

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login(settings.username, settings.password, remember=True)
    dashboard_page.assert_loaded()
    context.close()

    restored_context, restored_page = _launch_persistent_page(
        playwright,
        browser_name,
        profile_dir,
    )
    restored_dashboard = DashboardPage(restored_page)

    restored_page.goto("/app.html")
    restored_dashboard.assert_loaded()
    restored_dashboard.assert_signed_in_as(settings.username)

    restored_context.close()


@allure.severity(allure.severity_level.NORMAL)
def test_login_without_remember_me_does_not_persist_auth_across_browser_restart(
    playwright,
    browser_name,
    tmp_path,
):
    profile_dir = tmp_path / "session-only-profile"
    context, page = _launch_persistent_page(playwright, browser_name, profile_dir)

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login(settings.username, settings.password, remember=False)
    dashboard_page.assert_loaded()
    context.close()

    restored_context, restored_page = _launch_persistent_page(
        playwright,
        browser_name,
        profile_dir,
    )
    restored_login = LoginPage(restored_page)

    restored_page.goto("/app.html")
    restored_login.assert_loaded()

    restored_context.close()
