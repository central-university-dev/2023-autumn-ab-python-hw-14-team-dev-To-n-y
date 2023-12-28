import pytest
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from app.repo.user import UserRepo
from db.base import engine
from db.db_models import Base, User

if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine)


@pytest.fixture(name="user_data")
def user_data_tuple() -> tuple[str, str, str]:
    return "username", "password", "username@gmail.com"


def test_create_user(user_data: tuple[str, str, str]) -> None:
    new_user: User | None = UserRepo.get_user_by_id(
        UserRepo.create_user(*user_data)
    )
    assert new_user is not None
    assert (
        new_user.username == user_data[0]
        and new_user.password == user_data[1]
        and new_user.email == user_data[2]
    )
    UserRepo.delete_user(int(new_user.id))


def test_delete_user(user_data: tuple[str, str, str]) -> None:
    UserRepo.create_user(*user_data)
    new_user: User | None = UserRepo.get_user_by_email(user_data[2])
    assert new_user is not None
    assert (
        new_user.username == user_data[0]
        and new_user.password == user_data[1]
        and new_user.email == user_data[2]
    )
    UserRepo.delete_user(int(new_user.id))


def test_update_user(user_data: tuple[str, str, str]) -> None:
    updated_user_data = list(map(lambda x: x + "1", user_data))
    user_id = UserRepo.create_user(*user_data)
    UserRepo.update_user(user_id, *updated_user_data)
    new_user: User | None = UserRepo.get_user_by_id(user_id)
    assert new_user is not None
    assert (
        new_user.username == updated_user_data[0]
        and new_user.password == updated_user_data[1]
        and new_user.email == updated_user_data[2]
    )
    UserRepo.delete_user(int(new_user.id))
