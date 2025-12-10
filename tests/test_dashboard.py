from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


def _login_and_open_dashboard(page) -> DashboardPage:
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.open()
    login_page.login("test_user", "test_password", remember=True)
    dashboard_page.assert_loaded()
    return dashboard_page


def test_dashboard_overview_cards_visible(page):
    """Проверяем, что основные блоки дашборда отображаются."""
    dashboard_page = _login_and_open_dashboard(page)
    dashboard_page.assert_overview_cards_present()


def test_dashboard_has_transactions(page):
    """Проверяем, что в таблице есть хотя бы одна транзакция."""
    dashboard_page = _login_and_open_dashboard(page)
    dashboard_page.assert_has_transactions()
