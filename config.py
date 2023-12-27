import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "docker", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME")
    POSTGRES_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@127.0.0.1/{POSTGRES_DB_NAME}"


config = Config()
