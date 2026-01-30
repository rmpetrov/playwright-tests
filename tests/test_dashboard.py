import allure
import pytest

from pages.dashboard_page import DashboardPage

pytestmark = [pytest.mark.ui, allure.feature("Dashboard")]


@allure.severity(allure.severity_level.NORMAL)
def test_dashboard_overview_cards_visible(dashboard_page: DashboardPage):
    dashboard_page.assert_overview_cards_present()


@allure.severity(allure.severity_level.NORMAL)
def test_dashboard_has_transactions(dashboard_page: DashboardPage):
    dashboard_page.assert_has_transactions()


@allure.severity(allure.severity_level.MINOR)
def test_dashboard_transactions_have_amount_column(dashboard_page: DashboardPage):
    headers = dashboard_page.get_transactions_headers_text()
    assert any("amount" in h.lower() for h in headers), (
        f"No 'Amount' column found in headers: {headers}"
    )


@allure.severity(allure.severity_level.NORMAL)
def test_dashboard_transaction_amounts_formatted(dashboard_page: DashboardPage):
    dashboard_page.assert_amounts_format()


@allure.severity(allure.severity_level.MINOR)
def test_dashboard_headers_count_reasonable(dashboard_page: DashboardPage):
    headers = dashboard_page.get_transactions_headers_text()
    assert len(headers) >= 3, f"Expected at least 3 headers, got {len(headers)}"
