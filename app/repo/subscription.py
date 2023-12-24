from typing import Optional

from db.base import connect_db
from db.db_models import Subscription, User


class SubscriptionRepo:
    def get_all_subscribers(self, owner_id: int) -> list[Optional[User]]:  # все подписчики
        session = connect_db()
        users = session.query(User).join(Subscription, Subscription.subscriber_id == User.id).filter(
            Subscription.owner_id == owner_id).distinct().all()
        return users

    def get_all_owners(self, subscriber_id: int) -> list[Optional[User]]:  # все на кого он подписан
        session = connect_db()
        users = session.query(User).join(Subscription, Subscription.owner_id == User.id).filter(
            Subscription.subscriber_id == subscriber_id).distinct().all()
        return users

    def create_subscription(
            self, owner_id: int, subscriber_id: int
    ) -> int:
        new_subscription = Subscription(
            owner_id=owner_id,
            subscriber_id=subscriber_id
        )
        session = connect_db()
        try:
            session.add(new_subscription)
            session.commit()
        except Exception:  # ошибка соединения с бд
            return -2
        new_subscription_id = new_subscription.id
        return new_subscription_id

    def delete_subscription(self, owner_id: int, subscriber_id: int) -> Optional[int]:
        session = connect_db()
        subscriptions = (
            session.query(Subscription)
            .filter(Subscription.owner_id == owner_id).filter(Subscription.subscriber_id == subscriber_id)
            .all()
        )
        if len(subscriptions) > 0:
            for subscription in subscriptions:
                session.delete(subscription)
            session.commit()
            return len(subscriptions)
        return None

# print(SubscriptionRepo().delete_subscription(owner_id=1, subscriber_id=6))
# print(SubscriptionRepo().get_all_owners(6)[0].id)
# print(SubscriptionRepo().create_subscription(owner_id=1, subscriber_id=1))
