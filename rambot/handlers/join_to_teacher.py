from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    get_student_by_tg_id,
    get_teacher_by_tg_id,
    join_to_teacher,
)
from config.settings import encryption_settings
from states.join_to_teacher import JoinToTeacher
from utils.tokens import create_token

router = Router()


@router.callback_query(F.data == "create_join_token")
async def create_join_token(call: CallbackQuery):
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(session=session, tg_id=call.from_user.id)
        data = {
            "id": teacher.id,
        }
    token = create_token(data=data, key=encryption_settings.ENCRYPTION_TOKEN)
    await call.message.answer(f"```token\n{token}```", parse_mode=ParseMode.MARKDOWN)


@router.message(F.text == "/join_to_teacher")
async def get_join_to_teacher_token(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Отправьте ключ присоединения полученный от преподавателя")
    await state.set_state(JoinToTeacher.join_token)


@router.message(JoinToTeacher.join_token)
async def verify_join_to_teacher_and_join(message: Message, state: FSMContext):
    token = message.text
    async with session_factory() as session:
        student = await get_student_by_tg_id(
            session=session, tg_id=message.from_user.id
        )
        text = await join_to_teacher(session=session, token=token, student_=student)
        if text == "Вы подписались на преподавателя":
            await message.answer(text)
            await state.clear()
        else:
            await message.answer(text)
