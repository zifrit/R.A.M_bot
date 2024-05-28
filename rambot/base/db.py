import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from base.models import User
from base.models.user import ProfileTeacher
from config.settings import db_settings


engine = create_async_engine(db_settings.DB_URL_FOR_SELECT, echo=True, future=True)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_users(
    session: AsyncSession,
    first_name: str,
    last_name: str,
) -> ProfileTeacher:
    user = ProfileTeacher(first_name=first_name, last_name=last_name)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def main():
    async with session_factory() as session:
        await create_users(session=session, first_name="user4", last_name="last_name")
    # a = await get_users(session=session, user_id=1)
    # print(a.username)
    # async with engine.begin() as conn:
    # await conn.run_sync(Base.metadata.drop_all)
    # await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(main())
