import os
import pytest

from clients.api_client import ApiClient
from clients.db_client import DatabaseClient
from tests.data import CREATE_USER_PAYLOAD


# api_clients
@pytest.fixture(scope="module")
def api_client_without_auth():
    api_client = ApiClient()
    yield api_client
    api_client.close()

@pytest.fixture(scope="module")
def api_client_with_valid_auth():
    api_client = ApiClient(token=os.getenv("API_ACCESS_TOKEN"))
    yield api_client
    api_client.close()

@pytest.fixture(scope="module")
def api_client_with_invalid_auth():
    api_client = ApiClient(token="wrong-token")
    yield api_client
    api_client.close()


# get users
@pytest.fixture()
def get_users_response(api_client_without_auth):
    return api_client_without_auth.get("users")


# create user
@pytest.fixture()
def create_new_user(api_client_with_valid_auth):
    response = api_client_with_valid_auth.post("users", json = CREATE_USER_PAYLOAD)

    assert response.status_code == 201

    user = response.json()

    yield user

    cleanup_response = api_client_with_valid_auth.delete(f"users/{user['id']}")

    if cleanup_response.status_code not in (204, 404):
        raise AssertionError(
            f"Cleanup failed: {cleanup_response.status_code}"
        )


#database
@pytest.fixture(scope="module")
def db_client():
    db_client = DatabaseClient()

    yield db_client

    db_client.close()

@pytest.fixture()
def db_created_user(db_client):
    user = db_client.create_user("New User", "new@new.new")

    yield user

    if db_client.get_user_by_id(user["id"]):
        db_client.delete_user(user["id"])

#hooks
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        print(f"{item.name} -> {report.outcome}")