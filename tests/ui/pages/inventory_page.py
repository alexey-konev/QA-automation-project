import allure

from tests.ui.components.header import Header
from tests.ui.pages.base_page import BasePage
from tests.ui.pages.cart_page import CartPage


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)

        self.header = Header(self.page)
        self.title = self.page.locator("[data-test='title']")

    @allure.step("Find '{product_name}'")
    def get_product_card(self, product_name):
        card = self.page.locator(".inventory_item").filter(has=self.page.get_by_text(product_name))

        return card

    @allure.step("Add product '{product_name}' to the cart")
    def add_product(self, product_name):
        card = self.get_product_card(product_name)

        card.get_by_role("button", name="Add to cart").click()

    @allure.step("Open cart")
    def open_cart(self):
        self.header.open_cart()

        return CartPage(self.page)