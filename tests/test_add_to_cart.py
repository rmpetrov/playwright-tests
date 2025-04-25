from playwright.sync_api import sync_playwright

def test_add_to_cart(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")
    page.wait_for_selector("span.title")
    page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("a.shopping_cart_link")
    page.wait_for_selector(".inventory_item_name")
    assert page.inner_text(".inventory_item_name") == "Sauce Labs Backpack"