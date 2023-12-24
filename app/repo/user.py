from typing import Optional

import sqlalchemy

from db.base import connect_db
from db.db_models import User


class UserRepo:
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        session = connect_db()
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def get_user_by_email(self, user_email: str) -> Optional[User]:
        session = connect_db()
        user = session.query(User).filter(User.email == user_email).first()
        return user

    def create_user(
            self, username: str, password: str, email: str
    ) -> int:
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
        except Exception:  # ошибка соединения с бд
            return -2
        new_user_id = new_user.id
        return new_user_id

    def delete_user(self, user_id: int) -> Optional[int]:
        session = connect_db()
        user = (
            session.query(User)
            .filter(User.id == user_id)
            .first()
        )
        if user is not None:
            session.delete(user)
            session.commit()
            return user_id
        return None

    def update_user(self, user_id, username: str, password: str, email: str) -> Optional[int]:
        session = connect_db()
        user = (
            session.query(User)
            .filter(User.id == user_id)
            .first()
        )
        if user is not None:
            user.username = username
            user.password = password
            user.email = email
            try:
                session.add(user)
                session.commit()
            except Exception:
                return -2
            return user_id
        return None


# print(UserRepo().update_user(user_id=6, username='name', email='email', password='qwerty33'))
# print(UserRepo().delete_user(2))
