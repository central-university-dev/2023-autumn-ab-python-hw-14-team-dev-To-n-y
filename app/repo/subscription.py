from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.base import connect_db
from db.db_models import Subscription, User


class SubscriptionRepo:
    @staticmethod
    def get_all_subscribers(
        owner_id: int,
    ) -> list[User]:  # все подписчики
        session = connect_db()
        users = (
            session.query(User)
            .join(Subscription, Subscription.subscriber_id == User.id)
            .filter(Subscription.owner_id == owner_id)
            .distinct()
            .all()
        )
        return users

    @staticmethod
    def get_all_owners(
        subscriber_id: int,
    ) -> list[User]:  # все на кого он подписан
        session = connect_db()
        users = (
            session.query(User)
            .join(Subscription, Subscription.owner_id == User.id)
            .filter(Subscription.subscriber_id == subscriber_id)
            .distinct()
            .all()
        )
        return users

    @staticmethod
    def create_subscription(
        owner_id: int, subscriber_id: int
    ) -> Optional[int]:
        if owner_id == subscriber_id:
            raise ValueError("Attempt to subscribe on itself")
        session = connect_db()
        try:
            subscription = (
                session.query(Subscription)
                .filter(Subscription.owner_id == owner_id)
                .filter(Subscription.subscriber_id == subscriber_id)
                .first()
            )
        except ConnectionError as exc:  # ошибка соединения с бд
            raise ConnectionError("Error while connecting to db") from exc
        if subscription is not None:
            raise ValueError("Subscription already exists")
        new_subscription = Subscription(
            owner_id=owner_id, subscriber_id=subscriber_id
        )

        try:
            session.add(new_subscription)
            session.commit()
            new_subscription_id = int(new_subscription.id)
            return new_subscription_id
        except IntegrityError:
            raise ValueError("No such user")
        except ConnectionError as exc:
            raise ConnectionError("Error while connecting to db") from exc

    @staticmethod
    def delete_subscription(
        owner_id: int, subscriber_id: int
    ) -> Optional[int]:
        session = connect_db()
        subscription = (
            session.query(Subscription)
            .filter(Subscription.owner_id == owner_id)
            .filter(Subscription.subscriber_id == subscriber_id)
            .first()
        )
        if subscription is not None:
            session.delete(subscription)
            session.commit()
            deleted_subscription_id = subscription.id
            return deleted_subscription_id
        return None
