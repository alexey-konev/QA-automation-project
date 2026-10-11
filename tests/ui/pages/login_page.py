from tests.ui.pages.base_page import BasePage
from tests.ui.pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)

        self.username_input = self.page.get_by_placeholder("Username")
        self.password_input = self.page.get_by_placeholder("Password")
        self.login_button = self.page.locator("[data-test='login-button']")
        self.login_error = self.page.locator("[data-test='error']")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

        return InventoryPage(self.page)
