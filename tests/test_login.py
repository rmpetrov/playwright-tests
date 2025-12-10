from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def test_successful_login(page):
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login("test_user", "test_password", remember=True)

    dashboard_page.assert_loaded()
