from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    create_profile_student,
)
from buttons import create_profile
from states.create_profiles import CreateProfileStudent

router = Router()


@router.callback_query(F.data.in_(["create_profiled_student", "disagree_fio_student"]))
async def selected_create_profiled_student(call: CallbackQuery):
    await call.message.edit_text(
        "Данные для Фамилии и Имени брать из... ?",
        reply_markup=create_profile.fio_student,
    )


@router.callback_query(F.data == "fio_from_account_student")
async def get_fio_for_student_profile_from_account(
    call: CallbackQuery, state: FSMContext
):
    last_name = call.from_user.last_name
    first_name = call.from_user.first_name
    if not last_name:
        last_name = "last_name (было взято last_name за отсутствием настоящего)"
        await state.update_data(last_name=last_name)
    else:
        await state.update_data(last_name=last_name)

    if not first_name:
        first_name = "first_name (было взято first_name за отсутствием настоящего)"
        await state.update_data(first_name=first_name)
    else:
        await state.update_data(first_name=first_name)
    await call.message.edit_text(
        f"Были взяты ваши: \nФамилия - {last_name} \nИмя - {first_name}",
        reply_markup=create_profile.y_n_fio_student,
    )


@router.callback_query(F.data == "get_fio_user_student")
async def get_fio_for_student_profile_from_user(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        f"Через пробел отправьте ваши Фаилия и Имя _ ",
    )
    await state.set_state(CreateProfileStudent.FIO)


@router.message(CreateProfileStudent.FIO)
async def get_fio_user(message: Message, state: FSMContext):
    first_name, last_name = message.text.split(" ")
    await state.update_data(first_name=first_name)
    await state.update_data(last_name=last_name)
    await message.answer(
        f"Ваши: \nФамилия - {last_name} \nИмя - {first_name}",
        reply_markup=create_profile.y_n_fio_student,
    )


@router.callback_query(F.data == "agree_fio_student")
async def set_fio_profile_create_profile_student(
    call: CallbackQuery, state: FSMContext
):
    await call.message.edit_text("Ваши данные приняты")
    data = await state.get_data()
    await call.message.bot.send_chat_action(
        chat_id=call.message.chat.id,
        action=ChatAction.TYPING,
    )
    await call.message.answer(
        text=f"{data["first_name"]} {data["last_name"]}",
    )
    async with session_factory() as session:
        await create_profile_student(
            session=session,
            first_name=data["first_name"],
            last_name=data["last_name"],
            tg_id=call.from_user.id,
        )
    await state.clear()
