def test_logout(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")
    page.click("button[id='react-burger-menu-btn']")
    page.wait_for_selector("a[id='logout_sidebar_link']")
    page.click("a[id='logout_sidebar_link']")
    assert page.is_visible("input[data-test='login-button']")
