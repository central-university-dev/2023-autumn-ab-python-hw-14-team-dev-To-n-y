import uuid
from typing import Dict

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="session")
def client_cred(test_client: TestClient) -> Dict[str, str]:
    login = uuid.uuid4().hex.upper()[0:8]
    response = test_client.post(
        "/auth/register",
        json={
            "user": {
                "username": login,
                "password": "1234",
                "email": f"{login}@test.ru",
            }
        },
    )
    return {"jwt": response.json()['token'], "user_id": response.json()['id']}


@pytest.fixture(scope="session")
def post_cred(test_client: TestClient, client_cred: Dict[str, str]) -> int:
    response = test_client.post(
        "/post",
        json={"title": "test", "text": "yoo-hoo!"},
        headers={"Authorization": str(client_cred['jwt'])},
    )
    post_id = int(response.json())
    return post_id


def test_create_post_bad_cred(test_client: TestClient) -> None:
    response = test_client.post(
        "/post",
        json={"title": "test", "text": "yoo-hoo!"},
        headers={"Authorization": "bad-jwt"},
    )

    assert response.status_code == 401


def test_create_post_ok(test_client: TestClient, client_cred) -> None:
    response = test_client.post(
        "/post",
        json={"title": "test", "text": "yoo-hoo!"},
        headers={"Authorization": str(client_cred['jwt'])},
    )

    assert response.status_code == 200


def test_get_post_not_found(test_client: TestClient) -> None:
    response = test_client.get(
        "/post",
        params={
            "post_id": -1,
        },
    )

    assert response.status_code == 404


def test_get_post_ok(test_client: TestClient, post_cred: int) -> None:
    response = test_client.get(
        "/post",
        params={
            "post_id": str(post_cred),
        },
    )

    assert response.status_code == 200


def test_get_user_posts_ok(
    test_client: TestClient, client_cred: Dict[str, str]
) -> None:
    response = test_client.get(f"/post/user/{client_cred['user_id']}")

    assert response.status_code == 200


def test_delete_post_not_yours(
    test_client: TestClient, post_cred: int
) -> None:
    response = test_client.delete(
        "/post",
        params={
            "post_id": str(post_cred),
        },
    )

    assert response.status_code == 403


def test_delete_post_ok(
    test_client: TestClient, client_cred: Dict[str, str], post_cred: int
) -> None:
    response = test_client.delete(
        "/post",
        params={
            "post_id": str(post_cred),
        },
        headers={"Authorization": str(client_cred['jwt'])},
    )

    assert response.status_code == 200


def test_delete_post_not_found(
    test_client: TestClient, client_cred: Dict[str, str], post_cred: int
) -> None:
    response = test_client.delete(
        "/post",
        params={
            "post_id": str(post_cred),
        },
        headers={"Authorization": str(client_cred['jwt'])},
    )

    assert response.status_code == 404
