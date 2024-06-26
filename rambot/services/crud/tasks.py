from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from base.models.lessons import Tasks, InProgressTasks, TasksTypes


async def get_task_types(session: AsyncSession) -> list[TasksTypes]:
    stmt = select(TasksTypes)
    task_types = await session.scalars(stmt)
    return list(task_types)


async def get_task(session: AsyncSession, id_task: int) -> Tasks:
    stmt = select(Tasks).where(Tasks.id == id_task)
    task = await session.scalar(stmt)
    return task


async def get_lessons_tasks(
    session: AsyncSession, id_lesson: int, limit: int = 1, offset: int = 1
) -> tuple[list[Tasks], int]:
    stmt = (
        select(Tasks)
        .limit(limit=limit)
        .offset(offset=(limit * (offset - 1)))
        .where(Tasks.lesson_id == id_lesson)
        .order_by(Tasks.id)
    )
    task = await session.scalars(stmt)
    return list(task), await get_count_lessons_tasks(session, id_lesson)


async def get_count_lessons_tasks(
    session: AsyncSession,
    id_lesson: int,
) -> int:
    count_lessons_tasks = await session.execute(
        select(func.count(Tasks.id)).where(Tasks.lesson_id == id_lesson)
    )
    count_lessons_tasks = count_lessons_tasks.scalar_one()
    return count_lessons_tasks


async def get_last_lessons_task(session: AsyncSession, id_lesson: int) -> Tasks:
    stmt = select(Tasks).filter(
        Tasks.lesson_id == id_lesson, Tasks.next_task_id == None
    )
    task = await session.scalar(stmt)
    return task


async def create_lessons_task(
    session: AsyncSession,
    id_lesson: int,
    question: str,
    answer: list,
    right_answer: str,
    task_type_id: int,
    previous: int | None = None,
    img: str | None = None,
) -> Tasks:
    task = Tasks(
        lesson_id=id_lesson,
        task_type_id=task_type_id,
        question=question,
        answer=answer,
        right_answer=right_answer,
        previous_task_id=previous,
        img=img,
    )
    session.add(task)
    await session.flush()
    if previous:
        previous_task = await get_task(session, previous)
        previous_task.next_task_id = task.id
        await session.flush()
    await session.commit()
    return task


async def get_first_in_progress_task(
    session: AsyncSession,
    id_progress_lesson: int,
) -> InProgressTasks:
    task = await session.scalar(
        select(InProgressTasks).where(
            InProgressTasks.in_progress_lessons_id == id_progress_lesson,
            InProgressTasks.previous_task_id == None,
        )
    )
    return task


async def get_in_progress_task(
    session: AsyncSession,
    id_task: int,
) -> InProgressTasks:
    task = await session.scalar(
        select(InProgressTasks).where(InProgressTasks.id == id_task)
    )
    return task


async def continue_lesson(
    session: AsyncSession,
    id_progress_lesson: int,
) -> InProgressTasks:
    task = await session.scalar(
        select(InProgressTasks).where(
            id_progress_lesson == InProgressTasks.in_progress_lessons_id,
            "now" == InProgressTasks.progress,
        )
    )
    return task


async def get_count_completed_lessons_task(
    session: AsyncSession, id_lesson: int
) -> int:
    count_completed_lessons_task = await session.execute(
        select(func.count(InProgressTasks.id)).where(
            InProgressTasks.in_progress_lessons_id == id_lesson,
            InProgressTasks.student_answer != None,
        )
    )
    count_completed_lessons_task = count_completed_lessons_task.scalar_one()
    return count_completed_lessons_task


async def get_count_verify_tasks(session: AsyncSession, id_lesson: int) -> int:
    count_completed_lessons_task = await session.execute(
        select(func.count(InProgressTasks.id)).where(
            InProgressTasks.in_progress_lessons_id == id_lesson,
        )
    )
    count_completed_lessons_task = count_completed_lessons_task.scalar_one()
    return count_completed_lessons_task


async def get_verify_tasks(
    session: AsyncSession,
    id_lesson: int,
    limit: int = 1,
    offset: int = 1,
) -> tuple[list[InProgressTasks], int]:
    stmt = (
        select(InProgressTasks)
        .limit(limit=limit)
        .offset(offset=(limit * (offset - 1)))
        .where(InProgressTasks.in_progress_lessons_id == id_lesson)
        .order_by(InProgressTasks.id)
    )
    tasks = await session.scalars(stmt)
    return list(tasks), await get_count_verify_tasks(session, id_lesson)


async def get_first_not_verify_lessons_task(
    session: AsyncSession, id_lesson: int
) -> InProgressTasks:
    task = await session.scalar(
        select(InProgressTasks)
        .where(
            InProgressTasks.in_progress_lessons_id == id_lesson,
            InProgressTasks.teacher_verify == False,
        )
        .order_by(InProgressTasks.id)
    )
    return task
