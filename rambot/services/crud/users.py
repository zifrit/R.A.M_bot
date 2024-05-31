from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from base.models import User


async def create_users(
    session: AsyncSession,
    username: str,
    tg_id: int,
) -> None:
    user = User(username=username, tg_id=tg_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)


async def get_user_by_tg_id(
    session: AsyncSession,
    tg_id: int,
) -> User:
    stmt = select(User).where(User.tg_id == tg_id)
    user = await session.scalar(stmt)
    return user
