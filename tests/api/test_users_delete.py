import allure


@allure.title("API: Users. Delete user")
def test_delete_user_success(api_client_with_valid_auth, db_client, db_created_user):
    with allure.step("Get id of the user"):
        user_id = db_created_user["id"]

    with allure.step("Send DELETE request"):
        response_delete = api_client_with_valid_auth.delete(f"users/{user_id}")

    with allure.step("Verify response status code = 204 and body is empty"):
        assert response_delete.status_code == 204
        assert response_delete.content == b""

    with allure.step("Verify deleted user no longer exists"):
        response_get = api_client_with_valid_auth.get(f"users/{user_id}")
        assert response_get.status_code == 404

        assert db_client.get_user_by_id(user_id) is None


@allure.title("API: Users. Delete user without authorization returns 401")
def test_delete_user_without_authorization_returns_401(api_client_without_auth):
    with allure.step("Send DELETE request"):
        response = api_client_without_auth.delete("users/1")
        data = response.json()

    with allure.step("Verify response status code: 401 Unauthorized"):
        assert response.status_code == 401
        assert data["detail"] == "Unauthorized"


@allure.title("API: Users. Delete user with invalid authorization returns 401")
def test_delete_user_with_invalid_authorization_returns_401(api_client_with_invalid_auth):
    with allure.step("Send DELETE request"):
        response = api_client_with_invalid_auth.delete("users/1")
        data = response.json()

    with allure.step("Verify response status code: 401 Unauthorized"):
        assert response.status_code == 401
        assert data["detail"] == "Unauthorized"


@allure.title("API: Users. Delete nonexisting user returns 404")
def test_delete_nonexisting_user_returns_404(api_client_with_valid_auth):
    with allure.step("Send DELETE request"):
        response = api_client_with_valid_auth.delete("users/1234567")
        data = response.json()

    with allure.step("Verify response status code: 404 User not found"):
        assert response.status_code == 404
        assert data["detail"] == "User not found"