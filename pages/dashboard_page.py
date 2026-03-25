import re

import allure
from playwright.sync_api import Page, expect


class DashboardPage:
    URL_PATTERN = re.compile(r".*/app\.html")

    def __init__(self, page: Page):
        self.page = page

    @allure.step("Assert dashboard page loaded")
    def assert_loaded(self):
        expect(self.page).to_have_url(self.URL_PATTERN)
        expect(self.page.locator("#dashboard-page")).to_be_visible()
        expect(self.page.locator("#dashboard-title")).to_be_visible()
        expect(self.page.get_by_text("Recent Transactions")).to_be_visible()

    @allure.step("Log out from dashboard")
    def logout(self):
        self.page.locator("#log-out").click()

    @allure.step("Assert session banner visible for {username}")
    def assert_signed_in_as(self, username: str):
        expect(self.page.locator("#session-banner")).to_have_text(f"Signed in as {username}")

    @allure.step("Assert overview card visible: {title}")
    def assert_overview_card_visible(self, title: str):
        expect(self.page.get_by_text(title)).to_be_visible()

    @allure.step("Assert transactions table has rows")
    def assert_has_transactions(self):
        rows = self.page.locator("table tbody tr")
        count = rows.count()
        assert count > 0, f"Expected at least 1 transaction row, got {count}"

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

    @allure.step("Get amount column values")
    def get_amount_cells_text(self):
        rows = self.page.locator("table tbody tr")
        amount_texts = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")
            last_cell = cells.nth(cells.count() - 1)
            amount_texts.append(last_cell.inner_text().strip())
        return amount_texts

    @allure.step("Assert transaction amounts format")
    def assert_amounts_format(self):
        amount_texts = self.get_amount_cells_text()
        pattern = re.compile(r"^[+-]?\s?\d[\d,]*(?:\.\d{2})?\sUSD$")
        for value in amount_texts:
            assert pattern.match(value), f"Invalid amount format: {value}"
