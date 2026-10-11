import allure
from playwright.sync_api import expect

from tests.ui.data.customers import VALID_CUSTOMER
from tests.ui.data.products import PRODUCTS
from tests.ui.config import username, password


@allure.title("UI: Products. Add to cart")
def test_add_product_to_cart(inventory_page):
    inventory_page.open()
    inventory_page.add_product(PRODUCTS["backpack"])

    with allure.step("Verify cart has a '1' badge"):
        expect(inventory_page.header.cart_badge).to_have_text("1")


@allure.title("UI: Products. Add multiple to cart")
def test_add_multiple_products_to_cart(inventory_page):
    product_list = [PRODUCTS["backpack"], PRODUCTS["bike_light"], PRODUCTS["tshirt"]]

    inventory_page.open()

    with allure.step("Add 3 products to the cart"):
        for item in product_list:
            inventory_page.add_product(item)

    with allure.step("Verify cart has a '3' badge"):
        expect(inventory_page.header.cart_badge).to_have_text("3")

    cart_page = inventory_page.open_cart()

    with allure.step("Verify all product are in the cart"):
        for item in product_list:
            expect(cart_page.get_product_card(item)).to_be_visible()


@allure.title("UI: Products. Remove from cart")
def test_remove_single_product_from_cart(inventory_page):
    inventory_page.open()
    inventory_page.add_product(PRODUCTS["backpack"])
    cart_page = inventory_page.open_cart()

    expect(cart_page.get_product_card(PRODUCTS["backpack"])).to_be_visible()

    cart_page.remove_product(PRODUCTS["backpack"])

    with allure.step("Verify no products are in the cart"):
        expect(cart_page.get_product_card(PRODUCTS["backpack"])).to_have_count(0)
        expect(cart_page.header.cart_badge).to_be_hidden()


@allure.title("UI: Products. Remove one of multiple products")
def test_remove_one_out_of_two_products_from_cart(inventory_page):
    inventory_page.open()
    inventory_page.add_product(PRODUCTS["backpack"])
    inventory_page.add_product(PRODUCTS["bike_light"])
    cart_page = inventory_page.open_cart()

    with allure.step("Verify 2 products are in the cart"):
        expect(cart_page.get_product_card(PRODUCTS["backpack"])).to_be_visible()
        expect(cart_page.get_product_card(PRODUCTS["bike_light"])).to_be_visible()

    cart_page.remove_product(PRODUCTS["backpack"])

    with allure.step("Verify only 1 product left in the cart"):
        expect(cart_page.get_product_card(PRODUCTS["backpack"])).to_have_count(0)
        expect(cart_page.get_product_card(PRODUCTS["bike_light"])).to_have_count(1)
        expect(cart_page.header.cart_badge).to_have_text("1")


@allure.title("UI: Products. Successful purchase")
@allure.description("User adds one product to the cart, proceeds to checkout, and completes the purchase successfully.")
def test_successful_purchase(login_page, base_url):
    login_page.open()

    with allure.step("Fill in username, password and login"):
        inventory_page = login_page.login(username, password)

    inventory_page.add_product(PRODUCTS["backpack"])

    with allure.step("Verify cart has a '1' badge"):
        expect(inventory_page.header.cart_badge).to_have_text("1")

    cart_page = inventory_page.open_cart()

    expect(cart_page.get_product_card(PRODUCTS["backpack"])).to_be_visible()

    with allure.step("Complete checkout"):
        checkout_page = cart_page.start_checkout()
        checkout_page.fill_customer_info(VALID_CUSTOMER["firstname"], VALID_CUSTOMER["lastname"], VALID_CUSTOMER["postal_code"])

        checkout_overview_page = checkout_page.continue_checkout()
        expect(checkout_overview_page.get_product_card(PRODUCTS["backpack"])).to_be_visible()

        order_complete_page = checkout_overview_page.finish_checkout()

    with allure.step("Verify purchase is successful"):
        expect(order_complete_page.page).to_have_url(f"{base_url}/checkout-complete.html")
        expect(order_complete_page.complete_message).to_be_visible()
