from typing import Optional

import sqlalchemy

from db.base import connect_db
from db.db_models import Post


class PostRepo:
    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        session = connect_db()
        post = session.query(Post).filter(Post.id == post_id).first()
        return post

    def get_all_user_posts(self, author_id) -> list[Optional[Post]]:
        session = connect_db()
        posts = session.query(Post).filter(Post.author_id == author_id).all()
        return posts

    def create_post(self, title: str, text: str, author_id: int) -> int:
        new_post = Post(
            title=title,
            text=text,
            author_id=author_id,
        )
        session = connect_db()
        try:
            session.add(new_post)
            session.commit()
        except sqlalchemy.exc.IntegrityError:  # нет такого автора
            return -1
        except Exception:  # ошибка соединения с бд
            return -2
        new_post_id = new_post.id
        return new_post_id

    def delete_post(self, post_id: int) -> Optional[int]:
        session = connect_db()
        post = session.query(Post).filter(Post.id == post_id).first()
        if post is not None:
            session.delete(post)
            session.commit()
            return post_id
        return None
