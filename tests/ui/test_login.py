import pytest
from playwright.sync_api import expect

from tests.ui.config import username, password


def test_successful_login(login_page, base_url):

    login_page.open()
    inventory_page = login_page.login(username, password)

    expect(inventory_page.page).to_have_url(f"{base_url}/inventory.html")

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
def test_login_with_empty_field_fails(login_page, base_url, username, password, missing_field):

    login_page.open()
    login_page.login(username, password)

    expect(login_page.login_error).to_have_text(f"Epic sadface: {missing_field} is required")


def test_login_with_locked_out_user_fails(login_page, base_url):

    login_page.open()
    login_page.login("locked_out_user", password)

    expect(login_page.login_error).to_have_text("Epic sadface: Sorry, this user has been locked out.")

