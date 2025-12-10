from playwright.sync_api import expect
import re

from pages.login_page import LoginPage


def test_successful_login(page):
    login_page = LoginPage(page)

    # открываем страницу логина
    login_page.open()

    # логинимся любым не пустым логином/паролем —
    # у demo.applitools этого достаточно
    login_page.login("test_user", "test_password", remember=True)

    # проверяем, что мы попали на дашборд
    expect(page).to_have_url(re.compile(r".*demo\.applitools\.com.*app.*"))
    # и, например, что есть какой-то элемент дашборда
    expect(page.get_by_text("ACME")).to_be_visible()
