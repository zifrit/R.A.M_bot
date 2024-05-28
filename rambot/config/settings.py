from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file="../.env")


class DB(BaseSettings):
    DB_URL_FOR_SELECT: str = "sqlite+aiosqlite:///../../db.sqlite3"
    DB_URL_FOR_MIGRATE: str = "sqlite+aiosqlite:///../db.sqlite3"

    model_config = SettingsConfigDict(env_file="../.env")


class Postgres(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = "5432"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "r_a_m_bot"

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
postgres_settings = Postgres()
db_settings = DB()
