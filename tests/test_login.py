import allure
import pytest

from config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.feature("Authentication")]


@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login(settings.username, settings.password, remember=True)

    dashboard_page.assert_loaded()


@allure.severity(allure.severity_level.NORMAL)
def test_login_page_ui_elements(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.assert_basic_ui_visible()


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("", settings.password, "username"),
        (settings.username, "", "password"),
        ("", "", "username"),
    ],
)
def test_login_validation_missing_fields(page, username, password, expected_error):
    login_page = LoginPage(page)

    login_page.open()
    login_page.fill_username(username)
    login_page.fill_password(password)
    login_page.submit()

    login_page.assert_still_on_login()
    login_page.assert_error_contains_if_present(expected_error)


@allure.severity(allure.severity_level.MINOR)
def test_login_password_field_is_masked(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.assert_password_field_masked()


@allure.severity(allure.severity_level.MINOR)
def test_login_remember_me_toggle(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.set_remember_me(True)
    assert login_page.is_remember_me_checked() is True

    login_page.set_remember_me(False)
    assert login_page.is_remember_me_checked() is False


@allure.severity(allure.severity_level.NORMAL)
def test_login_submit_via_enter(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.fill_username(settings.username)
    login_page.fill_password(settings.password)
    login_page.submit_via_enter()

    dashboard_page.assert_loaded()


@allure.severity(allure.severity_level.MINOR)
def test_remember_me_unchecked_by_default(page):
    login_page = LoginPage(page)

    login_page.open()
    assert login_page.is_remember_me_checked() is False
