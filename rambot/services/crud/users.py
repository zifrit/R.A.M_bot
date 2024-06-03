from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload

from base.models import User
from base.models.user import ProfileTeacher, ProfileStudent
from config.settings import encryption_settings
from utils.tokens import decrypt_token


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
) -> ProfileTeacher:
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
    return teacher


async def create_profile_student(
    session: AsyncSession,
    first_name: str,
    last_name: str,
    tg_id: int,
) -> ProfileStudent:
    user = await get_user_by_tg_id(session, tg_id)
    student = ProfileStudent(
        user_id=user.id,
        first_name=first_name,
        last_name=last_name,
    )
    setattr(user, "is_student", True)
    session.add(student)
    await session.commit()
    return student


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
) -> ProfileStudent:
    user = await get_user_by_tg_id(session, tg_id)
    stmt = select(ProfileStudent).where(ProfileStudent.user_id == user.id)
    student = await session.scalar(stmt)
    return student


async def update_profile_teacher(
    session: AsyncSession,
    first_name: str,
    last_name: str,
    image: str,
    bio: str,
    teacher_: ProfileTeacher,
) -> ProfileTeacher:
    teacher_.image = image
    teacher_.bio = bio
    teacher_.last_name = last_name
    teacher_.first_name = first_name
    await session.commit()
    return teacher_


async def update_profile_student(
    session: AsyncSession,
    first_name: str,
    last_name: str,
    student_: ProfileStudent,
) -> ProfileStudent:
    student_.last_name = last_name
    student_.first_name = first_name
    await session.commit()
    return student_


async def join_to_teacher(
    session: AsyncSession,
    token: str,
    student_: ProfileStudent,
):
    key = encryption_settings.ENCRYPTION_TOKEN
    data = decrypt_token(token=token, key=key)
    if data == "Token invalid token":
        return "Такой ключ не существует"
    elif data == "Token has expired":
        return "Ключ уже не работает"
    else:
        teacher_ = await session.scalar(
            select(ProfileTeacher)
            .options(selectinload(ProfileTeacher.students))
            .where(ProfileTeacher.id == data["id"])
        )
        if student_ in teacher_.students:
            return "Вы уже подписались на этого преподавателя"
        else:
            teacher_.students.append(student_)
            await session.commit()
            return "Вы подписались на преподавателя"
