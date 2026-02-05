import allure
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

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

    @allure.step("Set Remember Me: {value}")
    def set_remember_me(self, value: bool):
        checkbox = self.page.get_by_label("Remember Me")
        if value:
            checkbox.check()
        else:
            checkbox.uncheck()

    @allure.step("Click login button")
    def submit(self):
        self.page.locator("#log-in").click()

    @allure.step("Submit login via Enter")
    def submit_via_enter(self):
        self.page.locator("#password").press("Enter")

    @allure.step("Fill username: {username}")
    def fill_username(self, username: str):
        self.page.locator("#username").fill(username)

    @allure.step("Fill password")
    def fill_password(self, password: str):
        self.page.locator("#password").fill(password)

    @allure.step("Assert still on login page")
    def assert_still_on_login(self):
        expect(self.page).not_to_have_url("**/app.html")
        expect(self.page.get_by_text("Login Form")).to_be_visible()

    @allure.step("Check if current page is login page")
    def is_login_page(self) -> bool:
        if "/app.html" in self.page.url:
            return False
        return self.page.locator("#log-in").count() > 0

    @allure.step("Get login error message text")
    def get_error_message_text(self, timeout_ms: int = 1000) -> str:
        alert = self.page.locator("#alert")
        try:
            alert.wait_for(state="visible", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            return ""
        return alert.inner_text().strip()

    @allure.step("Assert error contains (if present): {expected_substring}")
    def assert_error_contains_if_present(self, expected_substring: str):
        text = self.get_error_message_text()
        if not text:
            return
        assert expected_substring.lower() in text.lower(), (
            f"Expected error to contain '{expected_substring}', got: {text}"
        )

    @allure.step("Assert password field is masked")
    def assert_password_field_masked(self):
        input_type = self.page.locator("#password").get_attribute("type")
        assert input_type == "password", f"Expected password input type, got {input_type}"
