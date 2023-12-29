from typing import Any, List

import sqlalchemy
from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
from jose import JWTError
from jwt import DecodeError
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_502_BAD_GATEWAY,
)

from ..models.post import Post
from ..models.token import Token
from ..repo.post import PostRepo
from ..security import decode_token

router = APIRouter(
    prefix="/post",
    tags=["Posts"],
)

api_key_header = APIKeyHeader(name="Authorization")

@router.get("/")
async def get_post(post_id: int) -> Any:
    post = PostRepo.get_post_by_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Post not found!",
        )
    return Post(title=str(post.title), text=str(post.text))


@router.get("/user/{user_id}")
async def get_posts(user_id: int) -> List[Any]:
    posts = PostRepo.get_all_user_posts(user_id)
    ret_posts = [
        Post(title=str(post.title), text=str(post.text)) for post in posts
    ]
    return ret_posts


@router.post("/")
async def create_post(
    post: Post, token: str = Security(api_key_header)
) -> int:
    try:
        payload = decode_token(token)
        token_data = Token(**payload)
    except (JWTError, DecodeError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials!",
        )
    try:
        new_post_id = PostRepo().create_post(
            title=post.title, text=post.text, author_id=token_data.id
        )
        return new_post_id
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found!"
        )
    except ConnectionError:
        raise HTTPException(
            status_code=HTTP_502_BAD_GATEWAY, detail="Database error!"
        )


@router.delete("/")
async def delete_post(post_id: int, token: str = Security(api_key_header)):
    try:
        payload = decode_token(token)
        token_data = Token(**payload)
    except JWTError:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials!",
        )
    post = PostRepo().get_post_by_id(post_id)
    if post is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Post not found!",
        )
    if post.author_id != token_data.id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not your post!"
        )
    del_res = PostRepo.delete_post(post_id)
    return bool(del_res)
