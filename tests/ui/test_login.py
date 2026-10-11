import allure
import pytest
from playwright.sync_api import expect

from tests.ui.config import username, password

@allure.title("UI: Successful login")
def test_successful_login(login_page, base_url):
    login_page.open()

    with allure.step("Fill in username, password and login"):
        inventory_page = login_page.login(username, password)

    with allure.step("Check URL"):
        expect(inventory_page.page).to_have_url(f"{base_url}/inventory.html")

    with allure.step("Check page title"):
        title = inventory_page.title
        expect(title).to_be_visible()
        expect(title).to_have_text("Products")


@pytest.mark.parametrize(
    "username, password, missing_field",
    [
        ("", password, "Username"),
        (username, "", "Password"),
    ],
    ids=[
        "Empty login",
        "Empty password"
    ]
)
@allure.title("UI: Unsuccessful login with the missing field '{missing_field}'")
def test_login_with_empty_field_fails(login_page, base_url, username, password, missing_field):
    login_page.open()

    with allure.step(f"Don't fill in '{missing_field}' and login"):
        login_page.login(username, password)

    with allure.step("Check login error message"):
        expect(login_page.login_error).to_have_text(f"Epic sadface: {missing_field} is required")


@allure.title("UI: Unsuccessful login with a locked out user")
def test_login_with_locked_out_user_fails(login_page, base_url):
    login_page.open()

    with allure.step("Fill in locked out user credentials and login"):
        login_page.login("locked_out_user", password)

    with allure.step("Check login error message"):
        expect(login_page.login_error).to_have_text("Epic sadface: Sorry, this user has been locked out.")

