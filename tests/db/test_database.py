import allure
import pytest
from psycopg.errors import UniqueViolation, NotNullViolation


@allure.title("DB: Users. Get user by email")
def test_get_user_from_db_by_email(db_client, db_created_user):

    user = db_client.get_user_by_email(db_created_user["email"])

    with allure.step("Verify user info is correct"):
        assert user == db_created_user


@allure.title("DB: Users. Create new user")
def test_create_user_db(db_client, db_created_user):

    with allure.step("Verify new user info is correct"):
        assert db_created_user["name"] == "New User"
        assert db_created_user["email"] == "new@new.new"

    with allure.step("Verify new user is in the database"):
        user = db_client.get_user_by_email(db_created_user["email"])
        assert db_created_user == user


@pytest.mark.parametrize(
    "name, email, missing_field",
    [
        (None,"some@email.com", "Name"),
        ("Some name", None, "Email")
    ],
    ids=["No name", "No email"]
)
@allure.title("DB: Users. Create user without '{missing_field}' fails")
def test_create_user_without_mandatory_field_returns_exception(db_client, name, email, missing_field):
    with allure.step(f"Verify exception when creating user without '{missing_field}'"):
        with pytest.raises(NotNullViolation):
            db_client.create_user(name, email)


@allure.title("DB: Users. Create user with duplicate email fails")
def test_create_user_with_duplicate_email_returns_exception(db_client, db_created_user):
    with allure.step("Verify exception when creating user with duplicate email"):
        with pytest.raises(UniqueViolation):
            db_client.create_user("User with duplicated email", db_created_user["email"])


@allure.title("DB: Users. Delete user")
def test_delete_user_db(db_client, db_created_user):
    deleted_user = db_client.delete_user(db_created_user["id"])

    with allure.step("Verify that the right user was deleted"):
        assert db_created_user == deleted_user

    with allure.step("Verify user is no longer in the database"):
        assert db_client.get_user_by_email(deleted_user["email"]) is None


