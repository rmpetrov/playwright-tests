import allure
from playwright.sync_api import Page, expect

from config import settings


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Open login page")
    def open(self):
        self.page.goto(settings.base_url)

    @allure.step("Login as {username}")
    def login(self, username: str, password: str, remember: bool = False):
        self.page.locator("#username").fill(username)
        self.page.locator("#password").fill(password)

        if remember:
            self.page.get_by_label("Remember Me").check()

        self.page.locator("#log-in").click()

    @allure.step("Assert login form UI elements visible")
    def assert_basic_ui_visible(self):
        expect(self.page.get_by_text("Login Form")).to_be_visible()
        expect(self.page.get_by_placeholder("Enter your username")).to_be_visible()
        expect(self.page.get_by_placeholder("Enter your password")).to_be_visible()
        expect(self.page.get_by_label("Remember Me")).to_be_visible()
        expect(self.page.locator("#log-in")).to_be_visible()

    @allure.step("Check if Remember Me is checked")
    def is_remember_me_checked(self) -> bool:
        return self.page.get_by_label("Remember Me").is_checked()

    @allure.step("Click login button")
    def submit(self):
        self.page.locator("#log-in").click()

    @allure.step("Fill username: {username}")
    def fill_username(self, username: str):
        self.page.locator("#username").fill(username)

    @allure.step("Fill password")
    def fill_password(self, password: str):
        self.page.locator("#password").fill(password)
