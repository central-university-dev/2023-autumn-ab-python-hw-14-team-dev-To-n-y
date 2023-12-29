import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def client_cred() -> str:
    login = uuid.uuid4().hex.upper()[0:8]
    return login


def test_reg_ok(test_client: TestClient, client_cred: str) -> None:
    response = test_client.post(
        "/auth/register",
        json={
            "user": {
                "username": client_cred,
                "password": "1234",
                "email": f"{client_cred}@test.ru",
            }
        },
    )

    assert response.status_code == 200


def test_reg_user_exists(test_client: TestClient, client_cred: str) -> None:
    response = test_client.post(
        "/auth/register",
        json={
            "user": {
                "username": client_cred,
                "password": "1234",
                "email": f"{client_cred}@test.ru",
            }
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists!"}


def test_login_ok(test_client: TestClient, client_cred: str) -> None:
    response = test_client.post(
        "/auth/login",
        json={"user": {"password": "1234", "email": f"{client_cred}@test.ru"}},
    )

    assert response.status_code == 200


def test_login_invalid(test_client: TestClient, client_cred: str) -> None:
    response = test_client.post(
        "/auth/login",
        json={
            "user": {
                "password": "invalid-password",
                "email": f"{client_cred}@test.ru",
            }
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid login or password"}


def test_login_not_found(test_client: TestClient, client_cred: str) -> None:
    response = test_client.post(
        "/auth/login",
        json={
            "user": {
                "password": "1234",
                "email": f"{client_cred}non-exist-user@test.ru",
            }
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found!"}
