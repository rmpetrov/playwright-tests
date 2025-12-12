import re
from playwright.sync_api import Page, expect


class DashboardPage:
    URL_PATTERN = re.compile(r".*/app\.html")

    def __init__(self, page: Page):
        self.page = page

    def assert_loaded(self):
        expect(self.page).to_have_url(self.URL_PATTERN)
        expect(self.page.get_by_text("Recent Transactions")).to_be_visible()

    def assert_overview_cards_present(self):
        expect(self.page.get_by_text("Total Balance")).to_be_visible()
        expect(self.page.get_by_text("Credit Available")).to_be_visible()
        expect(self.page.get_by_text("Financial Overview")).to_be_visible()

    def assert_has_transactions(self):
        rows = self.page.locator("table tbody tr")
        count = rows.count()
        assert count > 0, f"Expected at least 1 transaction row, got {count}"

    def get_transactions_headers_text(self):
        headers = self.page.locator("table thead th")
        return [headers.nth(i).inner_text().strip() for i in range(headers.count())]

    def get_amount_cells_text(self):
        rows = self.page.locator("table tbody tr")
        amount_texts = []
        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")
            last_cell = cells.nth(cells.count() - 1)
            amount_texts.append(last_cell.inner_text().strip())
        return amount_texts

    def assert_amounts_format(self):
        amount_texts = self.get_amount_cells_text()
        pattern = re.compile(r"^[+-]?\s?\d[\d,]*(?:\.\d{2})?\sUSD$")
        for value in amount_texts:
            assert pattern.match(value), f"Invalid amount format: {value}"


