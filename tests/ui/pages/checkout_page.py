import allure

from tests.ui.components.header import Header
from tests.ui.pages.base_page import BasePage
from tests.ui.pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)

        self.header = Header(self.page)
        self.first_name_input = self.page.locator("#first-name")
        self.last_name_input = self.page.locator("#last-name")
        self.postal_code_input = self.page.locator("#postal-code")
        self.continue_button = self.page.locator("#continue")

    @allure.step("Fill in customer info")
    def fill_customer_info(self, first_name, last_name, postal_code):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    @allure.step("Click the Continue button")
    def continue_checkout(self):
        self.continue_button.click()

        return CheckoutOverviewPage(self.page)


