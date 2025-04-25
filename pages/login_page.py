class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = "input[data-test='username']"
        self.password_input = "input[data-test='password']"
        self.login_button = "input[data-test='login-button']"
        self.title = "span.title"

    def goto(self):
        self.page.goto("https://www.saucedemo.com/")

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)
        self.page.wait_for_selector(self.title)
