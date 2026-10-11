import re

import pytest
from psycopg.errors import UniqueViolation, NotNullViolation


def test_get_user_from_db_by_email(db_client, db_created_user):
    user = db_client.get_user_by_email(db_created_user["email"])

    assert user == db_created_user


def test_create_user_db(db_client, db_created_user):

    assert db_created_user["name"] == "New User"
    assert db_created_user["email"] == "new@new.new"

    user = db_client.get_user_by_email(db_created_user["email"])

    assert db_created_user == user


@pytest.mark.parametrize(
    "name, email",
    [
        (None,"some@email.com"),
        ("Some name", None)
    ],
    ids=["No name", "No email"]
)
def test_create_user_without_mandatory_field_fails(db_client, name, email):
    with pytest.raises(NotNullViolation, match=r"NOT NULL"):
        db_client.create_user(name, email)


def test_create_user_with_duplicate_email_fails(db_client, db_created_user):
    with pytest.raises(UniqueViolation, match=re.escape('Ключ "(email)=(new@new.new)" уже существует.')):
        db_client.create_user("User with duplicated email", db_created_user["email"])


def test_delete_user_db(db_client, db_created_user):
    deleted_user = db_client.delete_user(db_created_user["id"])

    assert db_created_user == deleted_user
    assert db_client.get_user_by_email(deleted_user["email"]) is None


