from playwright.sync_api import sync_playwright

def test_uniqlo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.uniqlo.com/us/en/")
        page.get_by_role("button", name="Membership / Order History").click()
        page.get_by_text("$10 Off Your $75+ Purchase*")
        page.get_by_role("button", name="Close dialog").click()
        page.get_by_role("link", name="UNIQLO home").click()
        page.get_by_role("tab", name="men", exact=True).click()
        page.get_by_role("button", name="Outerwear Outerwear").click()
        page.get_by_role("link", name="Blazers Blazers").click()
        page.get_by_role("link", name="AirSense Blazer | Wool-Like MEN, XXS-3XL AirSense Blazer | Wool-Like price is $").click()
        page.get_by_role("button", name="Add to cart").click()
        page.wait_for_timeout(5000)
        assert page.get_by_role("heading", name="Added to cart").is_visible()

        context.close()
        browser.close()