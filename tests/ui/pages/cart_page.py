import allure

from tests.ui.components.header import Header
from tests.ui.pages.base_page import BasePage
from tests.ui.pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    path = "/cart.html"

    def __init__(self, page):
        super().__init__(page)

        self.header = Header(self.page)
        self.checkout_button = self.page.get_by_role("button", name="Checkout")

    @allure.step("Find '{product_name}'")
    def get_product_card(self, product_name):
        card = self.page.locator(".cart_item").filter(has=self.page.get_by_text(product_name))

        return card

    @allure.step("Remove '{product_name}' from the cart")
    def remove_product(self, product_name):
        card = self.get_product_card(product_name)

        card.get_by_role("button", name="Remove").click()

    @allure.step("Click the Checkout button'")
    def start_checkout(self):
        self.checkout_button.click()

        return CheckoutPage(self.page)