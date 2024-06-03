from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    create_profile_teacher,
    get_teacher_by_tg_id,
    update_profile_teacher,
)
from buttons import create_profile
from states.create_profiles import CreateProfileTeacher

router = Router()


@router.callback_query(
    F.data.in_(
        [
            "create_profiled_teacher",
            "disagree_fio_teacher",
        ]
    )
)
async def create_profiled_teacher(call: CallbackQuery):
    await call.message.edit_text(
        "Данные для Фамилии и Имени брать из... ?",
        reply_markup=create_profile.fio_teacher,
    )


@router.callback_query(
    F.data.in_(
        [
            "re_register_teacher_profile",
        ]
    )
)
async def create_profiled_teacher(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        "Данные для Фамилии и Имени брать из... ?",
        reply_markup=create_profile.fio_teacher,
    )


@router.callback_query(F.data == "fio_from_account_teacher")
async def create_profiled_teacher(call: CallbackQuery, state: FSMContext):
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
        reply_markup=create_profile.y_n_fio_teacher,
    )


@router.callback_query(F.data == "get_fio_user_teacher")
async def create_profiled_teacher(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        f"Через пробел отправьте ваши Фаилия и Имя",
    )
    await state.set_state(CreateProfileTeacher.FIO)


@router.message(CreateProfileTeacher.FIO)
async def get_fio_user(message: Message, state: FSMContext):
    first_name, last_name = message.text.split(" ")
    await state.update_data(first_name=first_name)
    await state.update_data(last_name=last_name)
    await message.answer(
        f"Ваши: \nФамилия - {first_name} \nИмя - {last_name}",
        reply_markup=create_profile.y_n_fio_teacher,
    )


@router.callback_query(F.data == "agree_fio_teacher")
async def set_fio_profile(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Отправьте фото для вашего профиля")
    await state.set_state(CreateProfileTeacher.image)


@router.message(~F.photo, CreateProfileTeacher.image)
async def process_image_invalid(message: Message):
    await message.reply("Это не фото. Пожалуйста, отправь фото.")


@router.message(CreateProfileTeacher.image)
async def get_image_user(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer(
        f"Ведите информацию о себе",
    )
    await state.set_state(CreateProfileTeacher.bio)


@router.message(CreateProfileTeacher.bio)
async def get_fio_user(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    data = await state.get_data()
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(
            session=session, tg_id=message.from_user.id
        )
        if teacher:
            teacher_ = await update_profile_teacher(
                session=session,
                first_name=data["first_name"],
                last_name=data["last_name"],
                bio=data["bio"],
                image=data["image"],
                teacher_=teacher,
            )
        else:
            teacher_ = await create_profile_teacher(
                session=session,
                first_name=data["first_name"],
                last_name=data["last_name"],
                bio=data["bio"],
                tg_id=message.from_user.id,
                image=data["image"],
            )
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.answer("Ваши профиль")
    await message.answer_photo(
        photo=teacher_.image,
        caption=f"{teacher_.first_name} {teacher_.last_name} \n\n\n\n{teacher_.bio}",
    )
    await state.clear()
