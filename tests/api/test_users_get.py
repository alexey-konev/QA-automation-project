import allure
import pytest


# /users
@allure.title("API: GET Users returns list")
def test_get_users_returns_list(get_users_response):
    with allure.step("Send GET request"):
        response = get_users_response
        data = response.json()

    with allure.step("Verify response status code: 200"):
        assert response.status_code == 200

    with allure.step("Verify response body is a list"):
        assert isinstance(data, list)


@allure.title("API: GET Users returns valid user structure")
@pytest.mark.parametrize(
    "field, field_type",
    [
        ("id", int),
        ("name", str),
        ("email", str)
    ],
    ids=[
        "id in user",
        "name in user",
        "email in user"
    ]
)
def test_get_users_returns_valid_user_structure(field, field_type, get_users_response):
    with allure.step("Send GET request"):
        data = get_users_response.json()

    for user in data:
        with allure.step(f"Verify user has the field: '{field}'"):
            assert field in user
        with allure.step(f"Verify '{field}' field type is '{field_type}'"):
            assert isinstance(user[field], field_type)


# /users/{id}
@allure.title("API: GET User returns correct user")
def test_get_existing_user_returns_correct_user(api_client_without_auth, db_created_user):
    with allure.step("Get user id"):
        user_id = db_created_user["id"]

    with allure.step("Send GET request"):
        response = api_client_without_auth.get(f"users/{user_id}")
        user = response.json()

    with allure.step("Verify response status code: 200"):
        assert response.status_code == 200

    with allure.step("Verify response contains correct user"):
        assert user == db_created_user


@allure.title("API: GET nonexistent User returns 404")
def test_get_nonexistent_user_returns_404(api_client_without_auth):
    with allure.step("Send GET request"):
        response = api_client_without_auth.get("users/1234567")
        data = response.json()

    with allure.step("Verify response status code: 404 User not found"):
        assert response.status_code == 404
        assert data["detail"] == "User not found"


@allure.title("API: GET User by invalid id returns 422")
def test_get_user_by_invalid_id_returns_422(api_client_without_auth):
    with allure.step("Send GET request"):
        response = api_client_without_auth.get("users/asd")
        data = response.json()

    with allure.step("Verify response status code: 422"):
        assert response.status_code == 422
        assert data["detail"][0]["loc"] == ["path", "user_id"]
