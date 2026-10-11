import allure

from tests.ui.components.header import Header
from tests.ui.pages.base_page import BasePage
from tests.ui.pages.order_complete_page import OrderCompletePage


class CheckoutOverviewPage(BasePage):
    path = "/checkout-step-two.html"

    def __init__(self, page):
        super().__init__(page)

        self.header = Header(self.page)
        self.finish_button = self.page.get_by_role("button", name="Finish")

    @allure.step("Find '{product_name}'")
    def get_product_card(self, product_name):
        card = self.page.locator(".cart_item").filter(has=self.page.get_by_text(product_name))

        return card

    @allure.step("Click the Finish button")
    def finish_checkout(self):
        self.finish_button.click()

        return OrderCompletePage(self.page)

