from sqlalchemy import select, func, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from base.models.lessons import Lesson
from base.models.user import ProfileTeacher


async def create_lesson(
    session: AsyncSession,
    teacher_: ProfileTeacher,
    name: str,
    description: str,
) -> Lesson:
    lesson = Lesson(name=name, teacher_id=teacher_.id, description=description)
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


async def get_count_teacher_lessons(
    session: AsyncSession,
    teacher_: ProfileTeacher,
) -> int:
    count_teacher_lessons = await session.execute(
        select(func.count(Lesson.id)).where(Lesson.teacher_id == teacher_.id)
    )
    count_teacher_lessons = count_teacher_lessons.scalar_one()
    return count_teacher_lessons


async def get_teacher_lessons(
    session: AsyncSession,
    teacher_: ProfileTeacher,
    limit: int = 5,  # page size
    offset: int = 1,  # page number
) -> tuple[list[Lesson], int]:
    teacher_lessons = await session.scalars(
        select(Lesson)
        .limit(limit)
        .offset(offset=(limit * (offset - 1)))
        .where(Lesson.teacher_id == teacher_.id)
        .order_by(Lesson.created_at)
    )
    return list(teacher_lessons), await get_count_teacher_lessons(session, teacher_)


async def delete_lesson_by_id(session: AsyncSession, id_lesson: int) -> None:
    lesson = await get_lesson_by_id(session, id_lesson)
    await session.delete(lesson)
    await session.commit()


async def get_count_search_lessons(
    session: AsyncSession,
    search: str,
) -> int:
    count_teacher_lessons = await session.execute(
        select(func.count(Lesson.id)).filter(
            or_(
                Lesson.name.icontains(search),
                Lesson.description.icontains(search),
            )
        )
    )
    count_teacher_lessons = count_teacher_lessons.scalar_one()
    return count_teacher_lessons


async def search_lessons(
    session: AsyncSession,
    search: str,
    limit: int = 5,  # page size
    offset: int = 1,  # page number
) -> tuple[list[Lesson], int]:
    lessons = await session.scalars(
        select(Lesson)
        .options(joinedload(Lesson.teacher), selectinload(Lesson.tasks))
        .limit(limit)
        .offset(offset=(limit * (offset - 1)))
        .filter(
            or_(
                Lesson.name.icontains(search),
                Lesson.description.icontains(search),
            )
        )
    )
    return list(lessons), await get_count_search_lessons(session, search)
