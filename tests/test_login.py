from pages.login_page import LoginPage

def test_valid_login(page):
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "secret_sauce")
    assert page.inner_text("span.title") == "Products"

def test_invalid_login(page):
    login = LoginPage(page)
    login.goto()
    login.login("standard_user", "wrong_password")
    error = page.inner_text("h3[data-test='error']")
    assert "Username and password do not match" in error
