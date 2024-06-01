from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from base.models import User
from base.models.user import ProfileTeacher, ProfileStudent


async def create_users(
    session: AsyncSession,
    username: str,
    tg_id: int,
) -> User:
    user = User(username=username, tg_id=tg_id)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_tg_id(
    session: AsyncSession,
    tg_id: int,
) -> User:
    stmt = select(User).where(User.tg_id == tg_id)
    user = await session.scalar(stmt)
    return user


async def create_profile_teacher(
    session: AsyncSession,
    first_name: str,
    last_name: str,
    image: str,
    bio: str,
    tg_id: int,
) -> None:
    user = await get_user_by_tg_id(session, tg_id)
    teacher = ProfileTeacher(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
        image=image,
        bio=bio,
    )
    setattr(user, "is_teacher", True)
    session.add(teacher)
    await session.commit()


async def create_profile_student(
    session: AsyncSession,
    first_name: str,
    last_name: str,
    tg_id: int,
) -> None:
    user = await get_user_by_tg_id(session, tg_id)
    teacher = ProfileStudent(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
    )
    setattr(user, "is_student", True)
    session.add(teacher)
    await session.commit()


async def get_teacher_by_tg_id(
    session: AsyncSession,
    tg_id: int,
) -> ProfileTeacher:
    user = await get_user_by_tg_id(session, tg_id)
    stmt = select(ProfileTeacher).where(ProfileTeacher.user_id == user.id)
    teacher = await session.scalar(stmt)
    return teacher


async def get_student_by_tg_id(
    session: AsyncSession,
    tg_id: int,
) -> ProfileTeacher:
    user = await get_user_by_tg_id(session, tg_id)
    stmt = select(ProfileStudent).where(ProfileStudent.user_id == user.id)
    teacher = await session.scalar(stmt)
    return teacher
