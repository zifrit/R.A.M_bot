from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from base.models import User
from base.models.lessons import Lesson
from config.settings import encryption_settings
from utils.tokens import decrypt_token


async def create_lesson(
    session: AsyncSession,
    name: str,
) -> Lesson:
    lesson = Lesson(name=name)
    session.add(lesson)
    await session.commit()
    return lesson


async def get_lesson_by_id(
    session: AsyncSession,
    id_lesson: int,
) -> Lesson:
    stmt = select(Lesson).where(Lesson.id == id_lesson)
    lesson = await session.scalar(stmt)
    return lesson


async def update_lesson(
    session: AsyncSession,
    id_lesson: int,
    new_name: str,
) -> None:
    lesson = await get_lesson_by_id(session, id_lesson)
    lesson.name = new_name
    await session.commit()
