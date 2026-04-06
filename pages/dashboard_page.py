import re

import allure
from playwright.sync_api import Page, expect


class DashboardPage:
    URL_PATTERN = re.compile(r".*/app\.html")
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    AMOUNT_PATTERN = re.compile(r"^[+-]?\s?\d[\d,]*(?:\.\d{2})?\sUSD$")

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Assert dashboard page loaded")
    def assert_loaded(self):
        expect(self.page).to_have_url(self.URL_PATTERN)
        expect(self.page.locator("#dashboard-page")).to_be_visible()
        expect(self.page.locator("#dashboard-title")).to_be_visible()
        expect(
            self.page.get_by_role("heading", name="Recent Transactions", exact=True)
        ).to_be_visible()

    @allure.step("Log out from dashboard")
    def logout(self):
        self.page.locator("#log-out").click()

    @allure.step("Assert session banner visible for {username}")
    def assert_signed_in_as(self, username: str):
        expect(self.page.locator("#session-banner")).to_have_text(f"Signed in as {username}")

    @allure.step("Assert overview card visible: {title}")
    def assert_overview_card_visible(self, title: str):
        expect(self.page.get_by_text(title)).to_be_visible()

    @allure.step("Assert transactions empty state visible")
    def assert_empty_state_visible(self):
        expect(self.page.locator("#transactions-empty-state")).to_have_text(
            "No recent transactions to display."
        )

    @allure.step("Assert transactions table has rows")
    def assert_has_transactions(self):
        count = self.get_transaction_row_count()
        assert count > 0, f"Expected at least 1 transaction row, got {count}"

    @allure.step("Assert transactions table has no rows")
    def assert_has_no_transactions(self):
        count = self.get_transaction_row_count()
        assert count == 0, f"Expected 0 transaction rows, got {count}"

    def _get_required_transaction_rows(self) -> list[dict[str, str]]:
        rows = self.get_transaction_rows_data()
        assert rows, "Expected transaction rows to be present"
        return rows

    @allure.step("Get transaction row count")
    def get_transaction_row_count(self) -> int:
        return self.page.locator("table tbody tr").count()

    @allure.step("Get transaction table headers")
    def get_transactions_headers_text(self):
        headers = self.page.locator("table thead th")
        return [headers.nth(i).inner_text().strip() for i in range(headers.count())]

    @allure.step("Get transaction header count")
    def get_transactions_header_count(self) -> int:
        return self.page.locator("table thead th").count()

    @allure.step("Get transaction row cell counts")
    def get_transaction_row_cell_counts(self, limit: int = 5) -> list[int]:
        rows = self.page.locator("table tbody tr")
        row_count = rows.count()
        take = min(row_count, limit)
        counts = []
        for i in range(take):
            counts.append(rows.nth(i).locator("td").count())
        return counts

    @allure.step("Get transaction rows data")
    def get_transaction_rows_data(self) -> list[dict[str, str]]:
        rows = self.page.locator("table tbody tr")
        row_data = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")
            row_data.append(
                {
                    "date": cells.nth(0).inner_text().strip(),
                    "description": cells.nth(1).inner_text().strip(),
                    "status": cells.nth(2).inner_text().strip(),
                    "amount": cells.nth(3).inner_text().strip(),
                }
            )
        return row_data

    @allure.step("Assert transaction rows include required values")
    def assert_transaction_rows_have_required_values(self):
        rows = self._get_required_transaction_rows()
        for row in rows:
            assert row["date"], f"Missing date value in row: {row}"
            assert row["description"], f"Missing description value in row: {row}"
            assert row["status"], f"Missing status value in row: {row}"
            assert row["amount"], f"Missing amount value in row: {row}"

    @allure.step("Assert transaction dates format")
    def assert_dates_format(self):
        rows = self._get_required_transaction_rows()
        for row in rows:
            assert self.DATE_PATTERN.match(row["date"]), f"Invalid date format: {row['date']}"

    @allure.step("Assert transaction amounts format")
    def assert_amounts_format(self):
        rows = self._get_required_transaction_rows()
        for row in rows:
            assert self.AMOUNT_PATTERN.match(row["amount"]), (
                f"Invalid amount format: {row['amount']}"
            )
