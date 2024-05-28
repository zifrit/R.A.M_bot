from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str


class DB(BaseSettings):
    DB_URL_FOR_SELECT: str = "sqlite+aiosqlite:///../../db.sqlite3"
    DB_URL_FOR_MIGRATE: str = "sqlite+aiosqlite:///../db.sqlite3"


settings = Settings()
db_settings = DB()
