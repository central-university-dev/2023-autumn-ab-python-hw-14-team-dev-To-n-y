from typing import Any, List

from fastapi import APIRouter

from ..models.post import Post
from ..repo.post import PostRepo

router = APIRouter(
    prefix="/post",
    tags=["Posts"],
)


@router.get("/")
async def get_post(post_id: int) -> Any:
    post = PostRepo.get_post_by_id(post_id)
    return post


@router.get("/user/{user_id}")
async def get_posts(user_id: int) -> List[Any]:
    posts = PostRepo.get_all_user_posts(user_id)
    return posts


@router.post("/")
async def create_post(post: Post) -> int:
    new_post_id = PostRepo.create_post(post.title, post.text, post.author_id)
    return new_post_id


@router.delete("/")
async def delete_post(post_id: int) -> bool:
    posts = PostRepo.delete_post(post_id)
    return bool(posts)
