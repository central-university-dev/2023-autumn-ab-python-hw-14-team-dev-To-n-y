from typing import Any, List

from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from jose import JWTError
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_502_BAD_GATEWAY,
)

from ..models.token import Token
from ..models.user import UserPerf
from ..repo.subscription import SubscriptionRepo
from ..security import decode_token

router = APIRouter(
    prefix="/sub",
    tags=["Subscriptions"],
)

api_key_header = APIKeyHeader(name="rpc-auth-key")


@router.get("/{owner_id}")
async def get_subs(owner_id: int) -> List[Any]:
    subscribers = SubscriptionRepo.get_all_subscribers(owner_id)
    ret_subscribers = [
        UserPerf(username=str(user.username), email=str(user.email))
        for user in subscribers
    ]
    return ret_subscribers


@router.get("/owner/{subscriber_id}")
async def get_owners(subscriber_id: int) -> List[Any]:
    owners = SubscriptionRepo.get_all_owners(subscriber_id)
    ret_owners = [
        UserPerf(username=str(user.username), email=str(user.email))
        for user in owners
    ]
    return ret_owners


@router.post("/")
async def create_sub(
    owner_id: int, token: str = Security(api_key_header)
) -> int | None:
    try:
        payload = decode_token(token)
        token_data = Token(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials!",
        )
    try:
        new_sub_id = SubscriptionRepo.create_subscription(
            owner_id, token_data.id
        )
    except ValueError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Subscription already exists!",
        )
    except ConnectionError:
        raise HTTPException(
            status_code=HTTP_502_BAD_GATEWAY, detail="Database error!"
        )
    return new_sub_id


@router.delete("/")
async def delete_sub(
    owner_id: int, token: str = Security(api_key_header)
) -> bool:
    try:
        payload = decode_token(token)
        token_data = Token(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials!",
        )

    del_res = SubscriptionRepo.delete_subscription(
        owner_id=owner_id, subscriber_id=token_data.id
    )
    return bool(del_res)
