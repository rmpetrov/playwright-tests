from playwright.sync_api import Page, expect


class LoginPage:
    URL = "https://demo.applitools.com/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str, remember: bool = False):
        # Поля логина/пароля
        self.page.locator("#username").fill(username)
        self.page.locator("#password").fill(password)

        # Чекбокс "Remember Me" — через label, а не через id
        if remember:
            self.page.get_by_label("Remember Me").check()

        # Кнопка логина
        self.page.locator("#log-in").click()

    def assert_on_page(self):
        expect(self.page).to_have_url(self.URL)
