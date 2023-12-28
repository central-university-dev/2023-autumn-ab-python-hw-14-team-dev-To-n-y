from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings

engine = create_engine(settings.DATABASE_URL_psycopg)


def connect_db():
    with Session(bind=engine.connect()) as session:
        return session
