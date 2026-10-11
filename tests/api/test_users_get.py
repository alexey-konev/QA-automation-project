import pytest


# /users
def test_get_users_returns_list(get_users_response):
    response = get_users_response
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)


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
    data = get_users_response.json()

    for user in data:
        assert field in user
        assert isinstance(user[field], field_type)


# /users/{id}
def test_get_existing_user_returns_correct_user(api_client_without_auth, db_created_user):
    user_id = db_created_user["id"]

    response = api_client_without_auth.get(f"users/{user_id}")
    user = response.json()

    assert response.status_code == 200
    assert user == db_created_user


def test_get_nonexistent_user_by_id_returns_404(api_client_without_auth):
    response = api_client_without_auth.get("users/1234567")
    data = response.json()

    assert response.status_code == 404
    assert data["detail"] == "User not found"


def test_get_user_by_id_returns_422_for_invalid_id(api_client_without_auth):
    response = api_client_without_auth.get("users/asd")
    data = response.json()

    assert response.status_code == 422
    assert data["detail"][0]["loc"] == ["path", "user_id"]
