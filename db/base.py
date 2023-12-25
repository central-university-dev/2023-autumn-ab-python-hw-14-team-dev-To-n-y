from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import config

engine = create_engine(config.POSTGRES_URL)


def connect_db():
    session = Session(bind=engine.connect())
    with Session(bind=engine.connect()) as session:
        return session
