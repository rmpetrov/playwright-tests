import allure
import pytest

from pages.dashboard_page import DashboardPage

pytestmark = [pytest.mark.ui, allure.feature("Dashboard")]


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize(
    "card_title",
    [
        "Total Balance",
        "Credit Available",
        "Financial Overview",
    ],
)
def test_dashboard_overview_card_visible(dashboard_page: DashboardPage, card_title: str):
    dashboard_page.assert_overview_card_visible(card_title)


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


@allure.severity(allure.severity_level.NORMAL)
def test_dashboard_header_texts_not_empty(dashboard_page: DashboardPage):
    headers = dashboard_page.get_transactions_headers_text()
    assert headers, "Expected at least one table header"
    assert all(h.strip() for h in headers), f"Empty header found: {headers}"


@allure.severity(allure.severity_level.NORMAL)
def test_dashboard_transactions_rows_have_consistent_columns(
    dashboard_page: DashboardPage,
):
    header_count = dashboard_page.get_transactions_header_count()
    row_counts = dashboard_page.get_transaction_row_cell_counts(limit=5)

    assert header_count > 0, "Expected table headers to be present"
    assert row_counts, "Expected at least one transaction row"
    assert all(count == header_count for count in row_counts), (
        f"Row column counts do not match headers. headers={header_count}, rows={row_counts}"
    )
