import re
from playwright.sync_api import Page, expect


class DashboardPage:
    URL_PATTERN = re.compile(r".*/app\.html")

    def __init__(self, page: Page):
        self.page = page

    def assert_loaded(self):
        # урл после логина
        expect(self.page).to_have_url(self.URL_PATTERN)
        # заголовок секции дашборда
        expect(self.page.get_by_text("Recent Transactions")).to_be_visible()

    def assert_overview_cards_present(self):
        # пару ключевых метрик на дашборде
        expect(self.page.get_by_text("Total Balance")).to_be_visible()
        expect(self.page.get_by_text("Credit Available")).to_be_visible()
        expect(self.page.get_by_text("Financial Overview")).to_be_visible()

    def assert_has_transactions(self):
        rows = self.page.locator("table tbody tr")
        # просто проверим, что таблица не пустая
        count = rows.count()
        assert count > 0, f"Expected at least 1 transaction row, got {count}"
