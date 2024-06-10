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
