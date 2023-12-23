from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from config import config

engine = create_engine(config.POSTGRES_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)


class Comment(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    main_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # на кого подписался
    subscriber_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # подписчик


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    text = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
