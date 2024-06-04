from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    get_teacher_by_tg_id,
)
from services.crud.lessons import (
    create_lesson,
    update_lesson,
    get_lesson_by_id,
)
from buttons import profiles, start
from states.create_lessons_task import CreateLesson

router = Router()


@router.message(F.text == "/create_lesson")
async def create_lessons(message: Message, state: FSMContext):
    await state.clear()
    async with session_factory(state) as session:
        teacher = await get_teacher_by_tg_id(
            session=session, tg_id=message.from_user.tg_id
        )
        if not teacher:
            await message.answer(
                'Вы не можете создавать "Урок".\nНужно иметь профиль преподавателя'
            )
        else:
            await message.answer("Введите название Урока")
            await state.set_state(CreateLesson.name_lesson)


@router.message(CreateLesson.name_lesson)
async def get_create_lesson_name(message: Message, state: FSMContext):
    name_lesson = message.text
    async with session_factory() as session:
        lesson = await create_lesson(session=session, name=name_lesson)
        await message.answer(f"Урок с название {lesson.name}, был создан")
        await state.clear()
