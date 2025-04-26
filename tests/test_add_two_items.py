def test_add_two_items_to_cart(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")
    page.click("button[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("button[data-test='add-to-cart-sauce-labs-bike-light']")
    page.click("a[class='shopping_cart_link']")
    assert page.locator(".cart_item").count() == 2
