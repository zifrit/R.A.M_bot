from sqlalchemy import select, func, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from base.models.lessons import Lesson, InProgressLesson, InProgressTasks, Tasks
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


async def get_lesson_by_id_full(
    session: AsyncSession,
    id_lesson: int,
) -> Lesson:

    lesson = await session.scalar(
        select(Lesson)
        .options(joinedload(Lesson.teacher), selectinload(Lesson.tasks))
        .where(Lesson.id == id_lesson)
    )
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


async def start_lesson(
    session: AsyncSession,
    id_lesson: int,
    id_student: int,
) -> tuple[InProgressLesson, bool]:
    lesson = await get_lesson_by_id_full(session, id_lesson)
    in_progress_lesson = await session.scalar(
        select(InProgressLesson).where(
            InProgressLesson.name == lesson.name,
            InProgressLesson.student_id == id_student,
        )
    )
    if in_progress_lesson:
        return in_progress_lesson, False
    in_progress_lesson = InProgressLesson(
        name=lesson.name,
        teacher_id=lesson.teacher_id,
        description=lesson.description,
        student_id=id_student,
    )
    session.add(in_progress_lesson)
    await session.commit()

    prev_lesson_task = await session.scalar(
        select(Tasks).where(
            Tasks.lesson_id == id_lesson,
            Tasks.previous_task_id == None,
        )
    )
    prev_lesson_progress_tasks = InProgressTasks(
        task_type_id=prev_lesson_task.task_type_id,
        in_progress_lessons_id=in_progress_lesson.id,
        img=prev_lesson_task.img,
        question=prev_lesson_task.question,
        answer=prev_lesson_task.answer,
        right_answer=prev_lesson_task.right_answer,
    )
    session.add(prev_lesson_progress_tasks)
    await session.commit()
    while True:
        if not prev_lesson_task.next_task_id:
            break
        next_lesson_task = await session.scalar(
            select(Tasks).where(
                Tasks.id == prev_lesson_task.next_task_id,
            )
        )
        next_lesson_progress_tasks = InProgressTasks(
            task_type_id=next_lesson_task.task_type_id,
            in_progress_lessons_id=in_progress_lesson.id,
            img=next_lesson_task.img,
            previous_task_id=prev_lesson_progress_tasks.id,
            question=next_lesson_task.question,
            answer=next_lesson_task.answer,
            right_answer=next_lesson_task.right_answer,
        )
        session.add(next_lesson_progress_tasks)
        await session.commit()
        prev_lesson_progress_tasks.next_task_id = next_lesson_progress_tasks.id
        await session.commit()
        prev_lesson_task = next_lesson_task
        prev_lesson_progress_tasks = next_lesson_progress_tasks
    return in_progress_lesson, True


async def get_in_progress_lesson(
    session: AsyncSession, id_lesson: int
) -> InProgressLesson:
    stmt = select(InProgressLesson).where(InProgressLesson.id == id_lesson)
    lesson = await session.scalar(stmt)
    return lesson
