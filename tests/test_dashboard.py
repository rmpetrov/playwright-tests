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
    """Проверяем, что основные виджеты дашборда отображаются."""
    dashboard_page = _login_and_open_dashboard(page)
    dashboard_page.assert_overview_cards_present()


def test_dashboard_has_transactions(page):
    """Проверяем, что таблица транзакций не пустая."""
    dashboard_page = _login_and_open_dashboard(page)
    dashboard_page.assert_has_transactions()


def test_dashboard_transactions_have_amount_column(page):
    """Проверяем, что в таблице есть колонка Amount (по названию)."""
    dashboard_page = _login_and_open_dashboard(page)
    headers = dashboard_page.get_transactions_headers_text()
    assert any("amount" in h.lower() for h in headers), \
        f"No 'Amount' column found in headers: {headers}"


def test_dashboard_transaction_amounts_formatted(page):
    dashboard_page = _login_and_open_dashboard(page)
    dashboard_page.assert_amounts_format()


def test_dashboard_headers_count_reasonable(page):
    dashboard_page = _login_and_open_dashboard(page)
    headers = dashboard_page.get_transactions_headers_text()
    assert len(headers) >= 3, f"Expected at least 3 headers, got {len(headers)}"
