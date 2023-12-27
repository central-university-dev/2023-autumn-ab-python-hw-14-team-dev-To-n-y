from typing import Optional

import sqlalchemy

from db.base import connect_db
from db.db_models import User


class UserRepo:
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        session = connect_db()
        user = session.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def get_user_by_email(user_email: str) -> Optional[User]:
        session = connect_db()
        user = session.query(User).filter(User.email == user_email).first()
        return user

    @staticmethod
    def create_user(username: str, password: str, email: str) -> int:
        new_user = User(
            username=username,
            password=password,
            email=email,
        )
        session = connect_db()
        try:
            session.add(new_user)
            session.commit()
        except sqlalchemy.exc.IntegrityError:  # уже есть такой юзер
            return -1
        except ConnectionError as exc:  # ошибка соединения с бд
            raise ConnectionError("Error while connecting to db") from exc
        new_user_id = int(new_user.id)
        return new_user_id

    @staticmethod
    def delete_user(user_id: int) -> Optional[int]:
        session = connect_db()
        user = session.query(User).filter(User.id == user_id).first()
        if user is not None:
            session.delete(user)
            session.commit()
            return user_id
        return None

    @staticmethod
    def update_user(
        user_id, username: str, password: str, email: str
    ) -> Optional[int]:
        session = connect_db()
        user = session.query(User).filter(User.id == user_id).first()
        if user is not None:
            user.username = username
            user.password = password
            user.email = email
            try:
                session.add(user)
                session.commit()
                return user_id
            except ConnectionError as exc:
                raise ConnectionError("Error while connecting to db") from exc

        raise ValueError(f"User with id {user_id} does not exist")
