from typing import Optional

from db.base import connect_db
from db.db_models import Subscription, User


class SubscriptionRepo:
    def get_all_subscribers(
        self, owner_id: int
    ) -> list[Optional[User]]:  # все подписчики
        session = connect_db()
        users = (
            session.query(User)
            .join(Subscription, Subscription.subscriber_id == User.id)
            .filter(Subscription.owner_id == owner_id)
            .distinct()
            .all()
        )
        return users

    def get_all_owners(
        self, subscriber_id: int
    ) -> list[Optional[User]]:  # все на кого он подписан
        session = connect_db()
        users = (
            session.query(User)
            .join(Subscription, Subscription.owner_id == User.id)
            .filter(Subscription.subscriber_id == subscriber_id)
            .distinct()
            .all()
        )
        return users

    def create_subscription(self, owner_id: int, subscriber_id: int) -> int:
        if owner_id == subscriber_id:
            return -3  # нельзя подписаться на себя
        session = connect_db()
        try:
            subscription = (
                session.query(Subscription)
                .filter(Subscription.owner_id == owner_id)
                .filter(Subscription.subscriber_id == subscriber_id)
                .first()
            )
        except Exception:
            return -2
        if subscription is not None:
            return -1
        new_subscription = Subscription(
            owner_id=owner_id, subscriber_id=subscriber_id
        )

        try:
            session.add(new_subscription)
            session.commit()
        except Exception:  # ошибка соединения с бд
            return -2
        new_subscription_id = new_subscription.id
        return new_subscription_id

    def delete_subscription(
        self, owner_id: int, subscriber_id: int
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
