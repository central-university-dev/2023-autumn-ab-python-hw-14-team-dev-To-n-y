from typing import Optional

import sqlalchemy

from db.base import connect_db
from db.db_models import Post


class PostRepo:
    @staticmethod
    def get_post_by_id(post_id: int) -> Optional[Post]:
        session = connect_db()
        post = session.query(Post).filter(Post.id == post_id).first()
        return post

    @staticmethod
    def get_all_user_posts(author_id) -> list[Optional[Post]]:
        session = connect_db()
        posts = session.query(Post).filter(Post.author_id == author_id).all()
        return posts

    @staticmethod
    def create_post(title: str, text: str, author_id: int) -> int:
        new_post = Post(
            title=title,
            text=text,
            author_id=author_id,
        )
        session = connect_db()
        try:
            session.add(new_post)
            session.commit()
            new_post_id = int(new_post.id)
            return new_post_id
        except sqlalchemy.exc.IntegrityError as e:
            raise ValueError(f"user with id {author_id} doesn't exist") from e
        except ConnectionError as exc:
            raise ConnectionError("Error while connecting to db") from exc

    @staticmethod
    def delete_post(post_id: int) -> Optional[int]:
        session = connect_db()
        post = session.query(Post).filter(Post.id == post_id).first()
        if post is not None:
            session.delete(post)
            session.commit()
            return post_id
        return None


# PostRepo.create_post("some_post", "some text", 1)
