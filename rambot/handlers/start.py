from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    create_users,
    get_user_by_tg_id,
    get_student_by_tg_id,
    get_teacher_by_tg_id,
)
from buttons import profiles, start

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    async with session_factory() as session:
        user = await get_user_by_tg_id(session=session, tg_id=message.from_user.id)
        if user:
            pass
        else:
            user = await create_users(
                session=session,
                username=message.from_user.username,
                tg_id=message.from_user.id,
            )
        if user.is_teacher and user.is_student:
            await message.answer(
                "Это система помощи работы с учениками для преподавателей.",
            )
        elif user.is_teacher:
            await message.answer(
                "Это система помощи работы с учениками для преподавателей."
                "\nВыберите способ регистрации вашего профиля ⬇️",
                reply_markup=profiles.create_profiles_student_inline,
            )
        elif user.is_student:
            await message.answer(
                "Это система помощи работы с учениками для преподавателей."
                "\nВыберите способ регистрации вашего профиля ⬇️",
                reply_markup=profiles.create_profile_teacher_inline,
            )
        else:
            await message.answer(
                "Это система помощи работы с учениками для преподавателей."
                "\nВыберите способ регистрации вашего профиля ⬇️",
                reply_markup=profiles.create_profiles_inline,
            )


@router.message(F.text == "/profiles")
async def profile(message: Message, state: FSMContext):
    await state.clear()
    async with session_factory() as session:
        user = await get_user_by_tg_id(session=session, tg_id=message.from_user.id)
        if user.is_teacher and user.is_student:
            await message.answer(
                f"Какой профиль хотите посмотреть ?",
                reply_markup=start.profiles,
            )
        elif user.is_teacher:
            teacher = await get_teacher_by_tg_id(
                session=session, tg_id=message.from_user.id
            )
            await message.answer_photo(
                photo=teacher.image,
                caption=f"{teacher.first_name} {teacher.last_name} \n\n\n\n{teacher.bio}",
                reply_markup=profiles.view_profile(
                    callback_data="re_register_teacher_profile", is_teacher=True
                ),
            )
        elif user.is_student:
            student = await get_student_by_tg_id(
                session=session, tg_id=message.from_user.id
            )
            await message.answer(
                text=f"{student.first_name} {student.last_name}",
                reply_markup=profiles.view_profile(
                    callback_data="re_register_student_profile"
                ),
            )


@router.callback_query(F.data == "back_choice_profile")
async def profile(call: CallbackQuery):
    async with session_factory() as session:
        await call.message.delete()
        user = await get_user_by_tg_id(session=session, tg_id=call.from_user.id)
        if user.is_teacher and user.is_student:
            await call.message.answer(
                f"Какой профиль хотите посмотреть ?",
                reply_markup=start.profiles,
            )
        elif user.is_teacher:
            teacher = await get_teacher_by_tg_id(
                session=session, tg_id=call.from_user.id
            )
            await call.message.answer_photo(
                photo=teacher.image,
                caption=f"{teacher.first_name} {teacher.last_name} \n\n\n\n{teacher.bio}",
                reply_markup=profiles.view_profile(
                    callback_data="re_register_teacher_profile", is_teacher=True
                ),
            )
        elif user.is_student:
            student = await get_student_by_tg_id(
                session=session, tg_id=call.from_user.id
            )
            await call.message.answer(
                text=f"{student.first_name} {student.last_name}",
                reply_markup=profiles.view_profile(
                    callback_data="re_register_student_profile"
                ),
            )


@router.callback_query(F.data == "profiled_student")
async def profiled_student(call: CallbackQuery):
    async with session_factory() as session:
        student = await get_student_by_tg_id(session=session, tg_id=call.from_user.id)
        await call.message.edit_text(
            text=f"{student.first_name} {student.last_name}",
            reply_markup=profiles.view_profile(
                callback_data="re_register_student_profile"
            ),
        )


@router.callback_query(F.data == "profiled_teacher")
async def profiled_teacher(call: CallbackQuery):
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(session=session, tg_id=call.from_user.id)
        await call.message.delete()
        await call.message.answer_photo(
            photo=teacher.image,
            caption=f"{teacher.first_name} {teacher.last_name} \n\n\n\n{teacher.bio}",
            reply_markup=profiles.view_profile(
                callback_data="re_register_teacher_profile", is_teacher=True
            ),
        )
