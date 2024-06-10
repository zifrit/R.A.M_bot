from aiogram import F, Router
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    get_teacher_by_tg_id,
)
from services.crud.lessons import (
    create_lesson,
    update_lesson,
    get_count_teacher_lessons,
    delete_lesson_by_id,
    get_lesson_by_id,
    get_teacher_lessons,
)
from buttons import profiles, start, lessons, pagination
from states.create_lessons_task import UpdateLessonName, CreateLesson

router = Router()


@router.message(F.text == "/create_lesson")
async def create_lessons(message: Message, state: FSMContext):
    await state.clear()
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(
            session=session, tg_id=message.from_user.id
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
        teacher = await get_teacher_by_tg_id(
            session=session, tg_id=message.from_user.id
        )
        lesson = await create_lesson(
            session=session, name=name_lesson, teacher_=teacher
        )
        await message.answer(f"Урок с название {lesson.name}, был создан")
        await state.clear()


@router.callback_query(F.data.in_(["back_list_lessons", "view_my_lessons"]))
async def view_lessons_teacher(call: CallbackQuery):
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(session=session, tg_id=call.from_user.id)
        teacher_lessons, count_lessons = await get_teacher_lessons(
            session=session, teacher_=teacher, limit=2
        )
        count_page = (
            count_lessons // 2 + 1 if count_lessons % 2 != 0 else count_lessons // 3
        )
    if 0 < count_lessons <= 2:
        text = []
        for lesson in teacher_lessons:
            text.append(f"""📝 {lesson.name}\n/info_lesson_{lesson.id}""")
        await call.message.delete()
        await call.message.answer(
            text="\n\n".join(text), reply_markup=pagination.back_teacher_profile
        )
    elif count_lessons > 2:
        text = []
        for lesson in teacher_lessons:
            text.append(f"""📝 {lesson.name}\n/info_lesson_{lesson.id}""")
        await call.message.delete()
        await call.message.answer(
            text="\n\n".join(text),
            reply_markup=pagination.pagination(
                back_callback="profiled_teacher",
                name_nex_action="next_page_lessons",
                count_page=count_page,
            ),
        )
    else:
        await call.message.answer(text="Уроки еще не был созданы")


@router.callback_query(
    pagination.Pagination.filter(
        F.action.in_(["prev_page_lessons", "next_page_lessons"])
    )
)
async def paginator_service(call: CallbackQuery, callback_data: pagination.Pagination):
    left = "prev_page_lessons"
    right = "next_page_lessons"
    if callback_data.action == "prev_page_lessons":
        if callback_data.page > 1:
            page = callback_data.page - 1
            if page <= 1:
                left = None
                right = "next_page_lessons"
        else:
            page = callback_data.page
            left = None
            right = "next_page_lessons"
    elif callback_data.action == "next_page_lessons":
        if callback_data.page < callback_data.count_page:
            page = callback_data.page + 1
            if page >= callback_data.count_page:
                left = "prev_page_lessons"
                right = None
        else:
            page = callback_data.page
            left = "prev_page_lessons"
            right = None
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(session=session, tg_id=call.from_user.id)
        teacher_lessons, count_lessons = await get_teacher_lessons(
            session=session, teacher_=teacher, offset=page, limit=2
        )
        count_page = (
            count_lessons // 2 + 1 if count_lessons % 2 != 0 else count_lessons // 3
        )
    text = []
    for lesson in teacher_lessons:
        text.append(f"""📝 {lesson.name}\n/info_lesson_{lesson.id}""")
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            reply_markup=pagination.pagination(
                count_page=count_page,
                page=page,
                name_prev_action=left,
                name_nex_action=right,
                back_callback="profiled_teacher",
            ),
            text="\n\n".join(text),
        )


@router.message(F.text.startswith("/info_lesson"))
async def info_lesson(message: Message):
    id_lesson = int(message.text.split("_")[-1])
    async with session_factory() as session:
        lesson = await get_lesson_by_id(session=session, id_lesson=id_lesson)
        text = f"📝{lesson.name}\nКоличество задач / \n✍🏻Количество проходящих / \n🥇Количество пройденных /"
        await message.answer(
            text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
        )


@router.callback_query(F.data.startswith("delete_lesson"))
async def delete_lesson(call: CallbackQuery):
    id_lesson = int(call.data.split("_")[-1])
    async with session_factory() as session:
        await delete_lesson_by_id(session=session, id_lesson=id_lesson)
    await call.message.edit_text("Урок удален")


@router.callback_query(F.data.startswith("update_lesson_name"))
async def update_lesson_name(call: CallbackQuery, state: FSMContext):
    id_lesson = int(call.data.split("_")[-1])
    await call.message.edit_text("Введите новое название урока")
    await state.update_data(id_lesson=id_lesson)
    await state.set_state(UpdateLessonName.new_name)


@router.message(UpdateLessonName.new_name)
async def set_name_lesson(message: Message, state: FSMContext):
    data = await state.get_data()
    id_lesson = int(data["id_lesson"])
    async with session_factory() as session:
        await update_lesson(session=session, id_lesson=id_lesson, new_name=message.text)
        lesson = await get_lesson_by_id(session=session, id_lesson=id_lesson)
        text = f"📝{lesson.name}\nКоличество задач / \n✍🏻Количество проходящих / \n🥇Количество пройденных /"
        await message.answer(
            text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
        )
        await state.clear()


@router.callback_query(F.data == "stop_create_task")
async def back_view_lesson(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    id_lesson = data["id_lesson"]
    await state.clear()
    async with session_factory() as session:
        lesson = await get_lesson_by_id(session=session, id_lesson=id_lesson)
        text = f"📝{lesson.name}\nКоличество задач / \n✍🏻Количество проходящих / \n🥇Количество пройденных /"
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(
                text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
            )
        else:
            await call.message.edit_text(
                text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
            )
