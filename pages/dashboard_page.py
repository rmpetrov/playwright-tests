from playwright.sync_api import Page, expect
import re


class DashboardPage:
    def __init__(self, page: Page):
        self.page = page

    def assert_loaded(self):
        # урл
        expect(self.page).to_have_url(re.compile(r".*demo\.applitools\.com.*app\.html"))
        # заголовок / элемент дашборда
        expect(self.page.get_by_text("ACME")).to_be_visible()
