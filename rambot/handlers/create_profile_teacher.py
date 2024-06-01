from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    create_profile_teacher,
)
from buttons import start
from states.create_profiles import CreateProfileTeacher

router = Router()


@router.callback_query(F.data.in_(["create_profiled_teacher", "disagree_fio"]))
async def create_profiled_teacher(call: CallbackQuery):
    await call.message.edit_text(
        "Данные для Фамилии и Имени брать из... ?", reply_markup=start.fio
    )


@router.callback_query(F.data == "fio_from_account")
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
        reply_markup=start.y_n_fio,
    )


@router.callback_query(F.data == "get_fio_user")
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
        f"Ваши: \nФамилия - {last_name} \nИмя - {first_name}",
        reply_markup=start.y_n_fio,
    )


@router.callback_query(F.data == "agree_fio")
async def set_fio_profile(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Ваши данные приняты")
    await call.message.answer("Отправьте фото для вашего профиля")
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
    await message.answer_photo(
        photo=data["image"],
        caption=f"{data["first_name"]} {data["last_name"]} \n\n\n\n{data["bio"]}",
    )
    async with session_factory() as session:
        await create_profile_teacher(
            session=session,
            first_name=data["first_name"],
            last_name=data["last_name"],
            bio=data["bio"],
            tg_id=message.from_user.id,
            image=data["image"],
        )
    await state.clear()
