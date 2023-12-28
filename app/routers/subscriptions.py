from typing import Any, List

from fastapi import APIRouter

from ..repo.subscription import SubscriptionRepo

router = APIRouter(
    prefix="/sub",
    tags=["Subscriptions"],
)


@router.get("/{owner_id}")
async def get_subs(owner_id: int) -> List[Any]:
    subscribes = SubscriptionRepo.get_all_owners(owner_id)
    return subscribes


@router.get("/owner/{subscriber_id}")
async def get_owners(subscriber_id: int) -> List[Any]:
    followers = SubscriptionRepo.get_all_subscribers(subscriber_id)
    return followers


@router.post("/")
async def create_sub(owner_id: int, subscriber_id: int) -> int | None:
    new_sub_id = SubscriptionRepo.create_subscription(owner_id, subscriber_id)
    return new_sub_id


@router.delete("/")
async def delete_sub(owner_id: int, subscriber_id: int) -> bool:
    sub = SubscriptionRepo.delete_subscription(owner_id, subscriber_id)
    return bool(sub)
