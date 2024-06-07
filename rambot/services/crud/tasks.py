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


async def get_last_task(session: AsyncSession, id_lesson: int) -> Tasks:
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
) -> Tasks:
    task = Tasks(
        lesson_id=id_lesson,
        task_type_id=task_type_id,
        question=question,
        answer=answer,
        right_answer=right_answer,
        previous_task_id=previous,
    )
    session.add(task)
    await session.flush()
    if previous:
        previous_task = await get_task(session, previous)
        previous_task.next_task_id = task.id
        await session.flush()
    await session.commit()
    return task
