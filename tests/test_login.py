from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_successful_login(page):
    """Позитивный сценарий: логин с любыми непустыми данными."""
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login("test_user", "test_password", remember=True)

    dashboard_page.assert_loaded()


def test_login_page_ui_elements(page):
    """Проверяем, что на странице логина видны все базовые элементы."""
    login_page = LoginPage(page)

    login_page.open()
    login_page.assert_basic_ui_visible()


def test_remember_me_unchecked_by_default(page):
    """Чекбокс Remember Me по умолчанию должен быть не отмечен."""
    login_page = LoginPage(page)

    login_page.open()
    assert login_page.is_remember_me_checked() is False
