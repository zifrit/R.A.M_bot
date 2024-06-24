from aiogram import F, Router
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.users import (
    get_teacher_by_tg_id,
    get_student_by_tg_id,
)
from services.crud.lessons import (
    create_lesson,
    update_lesson,
    search_lessons,
    delete_lesson_by_id,
    get_lesson_by_id,
    get_teacher_lessons,
    get_lesson_by_id_full,
    start_lesson,
    get_student_lessons,
    get_in_progress_lesson_full,
    delete_student_lesson_by_id,
    get_count_complete_lesson,
)
from buttons import profiles, start, lessons, pagination
from states.lessons_task import UpdateLessonName, CreateLesson, SearchLesson

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
    await state.update_data(name_lesson=name_lesson)
    await state.set_state(CreateLesson.description)
    await message.answer(f"В видите описание для урока")


@router.message(CreateLesson.description)
async def get_create_lesson_name(message: Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(
            session=session, tg_id=message.from_user.id
        )
        await create_lesson(
            session=session,
            name=data["name_lesson"],
            teacher_=teacher,
            description=description,
        )
        await message.answer(f"Урок был создан")
        await state.clear()


@router.callback_query(F.data.in_(["back_list_lessons", "view_teacher_lessons"]))
async def view_lessons_teacher(call: CallbackQuery):
    async with session_factory() as session:
        teacher = await get_teacher_by_tg_id(session=session, tg_id=call.from_user.id)
        teacher_lessons, count_lessons = await get_teacher_lessons(
            session=session, teacher_=teacher, limit=2
        )
        count_page = (
            count_lessons // 2 + 1 if count_lessons % 2 != 0 else count_lessons // 2
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
            count_lessons // 2 + 1 if count_lessons % 2 != 0 else count_lessons // 2
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
async def info_lesson(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    id_lesson = int(message.text.split("_")[-1])
    async with session_factory() as session:
        if data.get("search", False):
            lesson = await get_lesson_by_id_full(session=session, id_lesson=id_lesson)
            text = (
                f"📝{lesson.name}\n\n"
                f"Преподаватель: {lesson.teacher.first_name} {lesson.teacher.last_name}\n"
                f"Количество задач: {len(lesson.tasks)}\n"
                f"Описание: {lesson.description}\n\n"
            )
            have_tasks = True if len(lesson.tasks) > 0 else False
            await message.answer(
                text=text,
                reply_markup=lessons.info_lesson(
                    id_lesson=id_lesson,
                    search=True,
                    have_tasks=have_tasks,
                ),
            )
        else:
            lesson = await get_lesson_by_id_full(session=session, id_lesson=id_lesson)
            teacher = await get_teacher_by_tg_id(
                session=session, tg_id=message.from_user.id
            )
            count_complete_lesson = await get_count_complete_lesson(
                session=session, id_lesson=id_lesson
            )
            if lesson:
                if lesson.teacher_id == teacher.id:
                    text = (
                        f"📝{lesson.name}\n\n"
                        f"{lesson.description}\n\n"
                        f"Количество задач: {len(lesson.tasks)}\n"
                        f"✍🏻Количество проходящих {len(lesson.in_progress_lessons)} \n"
                        f"🥇Количество пройденных {count_complete_lesson}"
                    )
                    await message.answer(
                        text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
                    )
                else:
                    await message.answer(text="Вы не можете смотреть чужие уроки!")
            else:
                await message.answer(text="Такого урока нет")


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
        text = (
            f"📝{lesson.name}\n\n"
            f"{lesson.description}\n\n"
            f"Количество задач / \n"
            f"✍🏻Количество проходящих / \n"
            f"🥇Количество пройденных /"
        )
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
        text = (
            f"📝{lesson.name}\n\n"
            f"{lesson.description}\n\n"
            f"Количество задач / \n"
            f"✍🏻Количество проходящих / \n"
            f"🥇Количество пройденных /"
        )
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(
                text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
            )
        else:
            await call.message.edit_text(
                text=text, reply_markup=lessons.info_lesson(id_lesson=id_lesson)
            )


@router.message(F.text == "/search_lesson")
async def student_search_lessons(message: Message, state: FSMContext):
    await message.answer("Введите что вы хотите найти...")
    await state.clear()
    await state.set_state(SearchLesson.search)


@router.callback_query(F.data == "search_lesson")
async def student_search_lessons(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите что вы хотите найти...")
    await state.clear()
    await state.set_state(SearchLesson.search)


@router.message(SearchLesson.search)
async def get_search_lessons(message: Message, state: FSMContext):
    search = message.text
    await state.update_data(search=search)
    async with session_factory() as session:
        lessons, count_lessons = await search_lessons(
            session=session, search=search, limit=3
        )

        count_page = (
            count_lessons // 3 + 1 if count_lessons % 3 != 0 else count_lessons // 3
        )
        if 0 < count_lessons <= 3:
            text = []
            for lesson in lessons:
                text.append(
                    f"""📝 {lesson.name}
Преподаватель:{lesson.teacher.first_name} {lesson.teacher.last_name}
Количество задач: {len(lesson.tasks)}\n
/info_lesson_{lesson.id}"""
                )
            await message.answer(
                text="\n\n".join(text), reply_markup=pagination.repeat_search_lesson
            )
        elif count_lessons > 3:
            text = []
            for lesson in lessons:
                text.append(
                    f"""📝 {lesson.name}
Преподаватель:{lesson.teacher.first_name} {lesson.teacher.last_name}
Количество задач: {len(lesson.tasks)}\n
/info_lesson_{lesson.id}"""
                )
            await message.answer(
                text="\n\n".join(text),
                reply_markup=pagination.pagination(
                    back_callback="search_lesson",
                    back_text="Повторить поиск",
                    name_nex_action="next_page_search_lessons",
                    count_page=count_page,
                ),
            )
        else:
            await message.answer(
                text="Ничего не было найдено",
                reply_markup=pagination.repeat_search_lesson,
            )


@router.callback_query(
    pagination.Pagination.filter(
        F.action.in_(["prev_page_search_lessons", "next_page_search_lessons"])
    )
)
async def paginator_service(
    call: CallbackQuery, callback_data: pagination.Pagination, state: FSMContext
):
    left = "prev_page_search_lessons"
    right = "next_page_search_lessons"
    if callback_data.action == "prev_page_search_lessons":
        if callback_data.page > 1:
            page = callback_data.page - 1
            if page <= 1:
                left = None
                right = "next_page_search_lessons"
        else:
            page = callback_data.page
            left = None
            right = "next_page_search_lessons"
    elif callback_data.action == "next_page_search_lessons":
        if callback_data.page < callback_data.count_page:
            page = callback_data.page + 1
            if page >= callback_data.count_page:
                left = "prev_page_search_lessons"
                right = None
        else:
            page = callback_data.page
            left = "prev_page_search_lessons"
            right = None
    async with session_factory() as session:
        data = await state.get_data()
        lessons, count_lessons = await search_lessons(
            session=session, search=data["search"], limit=3, offset=page
        )

        count_page = (
            count_lessons // 3 + 1 if count_lessons % 3 != 0 else count_lessons // 3
        )
        text = []
        for lesson in lessons:
            text.append(
                f"""📝 {lesson.name}
Преподаватель:{lesson.teacher.first_name} {lesson.teacher.last_name}
Количество задач: {len(lesson.tasks)}\n
/info_lesson_{lesson.id}"""
            )
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            text="\n\n".join(text),
            reply_markup=pagination.pagination(
                back_callback="search_lesson",
                back_text="Повторить поиск",
                count_page=count_page,
                page=page,
                name_prev_action=left,
                name_nex_action=right,
            ),
        )


@router.callback_query(F.data.startswith("add_lesson_"))
async def start_taking_lesson(call: CallbackQuery):
    id_lesson = int(call.data.split("_")[-1])
    async with session_factory() as session:
        student = await get_student_by_tg_id(session=session, tg_id=call.from_user.id)
        if not student:
            await call.message.answer("У вас нету профиля студента")
        else:
            in_progress_lesson, status = await start_lesson(
                session=session, id_lesson=id_lesson, id_student=student.id
            )
            if status:
                await call.message.edit_text(
                    "Добавлено",
                    reply_markup=lessons.start_work_lesson(
                        id_lesson=in_progress_lesson.id
                    ),
                )
            else:
                await call.message.edit_text(
                    "Вы уже добавили его к себе в список",
                    reply_markup=lessons.continue_work_lesson(
                        id_lesson=in_progress_lesson.id
                    ),
                )


@router.callback_query(
    F.data.in_(["back_list_student_lessons", "view_student_lessons"])
)
async def view_lessons_teacher(call: CallbackQuery):
    async with session_factory() as session:
        student = await get_student_by_tg_id(session=session, tg_id=call.from_user.id)
        student_lessons, count_lessons = await get_student_lessons(
            session=session, student_=student, limit=2
        )
        count_page = (
            count_lessons // 2 + 1 if count_lessons % 2 != 0 else count_lessons // 2
        )
    if 0 < count_lessons <= 2:
        text = []
        for lesson in student_lessons:
            text.append(f"""📝 {lesson.name}\n/info_student_lesson_{lesson.id}""")
        await call.message.delete()
        await call.message.answer(
            text="\n\n".join(text), reply_markup=pagination.back_teacher_profile
        )
    elif count_lessons > 2:
        text = []
        for lesson in student_lessons:
            text.append(f"""📝 {lesson.name}\n/info_student_lesson_{lesson.id}""")
        await call.message.delete()
        await call.message.answer(
            text="\n\n".join(text),
            reply_markup=pagination.pagination(
                back_callback="profiled_student",
                name_nex_action="next_page_student_lessons",
                count_page=count_page,
            ),
        )
    else:
        await call.message.answer(text="Уроки еще не был созданы")


@router.callback_query(
    pagination.Pagination.filter(
        F.action.in_(["prev_page_student_lessons", "next_page_student_lessons"])
    )
)
async def paginator_service(call: CallbackQuery, callback_data: pagination.Pagination):
    left = "prev_page_student_lessons"
    right = "next_page_student_lessons"
    if callback_data.action == "prev_page_student_lessons":
        if callback_data.page > 1:
            page = callback_data.page - 1
            if page <= 1:
                left = None
                right = "next_page_student_lessons"
        else:
            page = callback_data.page
            left = None
            right = "next_page_student_lessons"
    elif callback_data.action == "next_page_student_lessons":
        if callback_data.page < callback_data.count_page:
            page = callback_data.page + 1
            if page >= callback_data.count_page:
                left = "prev_page_student_lessons"
                right = None
        else:
            page = callback_data.page
            left = "prev_page_student_lessons"
            right = None
    async with session_factory() as session:
        student = await get_student_by_tg_id(session=session, tg_id=call.from_user.id)
        student_lessons, count_lessons = await get_student_lessons(
            session=session, student_=student, limit=2, offset=page
        )
        count_page = (
            count_lessons // 2 + 1 if count_lessons % 2 != 0 else count_lessons // 2
        )
    text = []
    for lesson in student_lessons:
        text.append(f"""📝 {lesson.name}\n/info_student_lesson_{lesson.id}""")
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            reply_markup=pagination.pagination(
                count_page=count_page,
                page=page,
                name_prev_action=left,
                name_nex_action=right,
                back_callback="profiled_student",
            ),
            text="\n\n".join(text),
        )


@router.message(F.text.startswith("/info_student_lesson_"))
async def info_lesson(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    id_lesson = int(message.text.split("_")[-1])
    async with session_factory() as session:
        lesson = await get_in_progress_lesson_full(session=session, id_lesson=id_lesson)
        if lesson:
            text = (
                f"📝{lesson.name}\n\n"
                f"{lesson.description}\n\n"
                f"Количество задач {len(lesson.in_progress_tasks)}"
            )
            await message.answer(
                text=text, reply_markup=lessons.info_student_lesson(id_lesson=id_lesson)
            )
        else:
            await message.answer(text="Такого урока нет")


@router.callback_query(F.data.startswith("delete_student_lesson_"))
async def delete_lesson(call: CallbackQuery):
    id_lesson = int(call.data.split("_")[-1])
    async with session_factory() as session:
        await delete_student_lesson_by_id(session=session, id_lesson=id_lesson)
    await call.message.edit_text("Урок удален")
