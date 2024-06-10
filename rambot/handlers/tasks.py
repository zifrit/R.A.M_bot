from contextlib import suppress

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from base.db import session_factory
from services.crud.tasks import (
    get_task_types,
    create_lessons_task,
    get_last_lessons_task,
    get_lessons_tasks,
)
from buttons.tasks import task_types_inline, completed_tasks_inline, back_lesson
from buttons.pagination import pagination, Pagination
from states.create_lessons_task import CreateLessonTask

router = Router()


@router.callback_query(F.data.startswith("add_task_to_lesson"))
async def add_task_to_lesson(call: CallbackQuery, state: FSMContext):
    id_lesson = int(call.data.split("_")[-1])
    await state.update_data(id_lesson=id_lesson)
    async with session_factory() as session:
        last_task = await get_last_lessons_task(session=session, id_lesson=id_lesson)
        if last_task:
            await state.update_data(previous=last_task.id)
        task_types = await get_task_types(session=session)
    await call.message.edit_text(
        "Какого вида задачу хотите создать ?",
        reply_markup=task_types_inline(task_types),
    )


@router.callback_query(F.data.startswith("create_next_task_"))
async def add_task_to_lesson(call: CallbackQuery, state: FSMContext):
    id_lesson = int(call.data.split("_")[-1])
    id_task = int(call.data.split("_")[-2])
    await state.update_data(id_lesson=id_lesson)
    await state.update_data(previous=id_task)
    async with session_factory() as session:
        task_types = await get_task_types(session=session)
    await call.message.edit_text(
        "Какого вида задачу хотите создать ?",
        reply_markup=task_types_inline(task_types),
    )


@router.callback_query(F.data.startswith("task_type"))
async def choice_task_type(call: CallbackQuery, state: FSMContext):
    task_type_id = int(call.data.split("_")[-2])
    task_type_name = call.data.split("_")[-1]
    await state.update_data(task_type_id=task_type_id)
    if task_type_name == "Картинка":
        await call.message.edit_text("Отправьте фото задания")
        await state.set_state(CreateLessonTask.img)
    else:
        await call.message.edit_text("Отправьте само задание")
        await state.set_state(CreateLessonTask.question)


@router.message(~F.photo, CreateLessonTask.img)
async def process_image_invalid(message: Message):
    await message.reply("Это не фото. Пожалуйста, отправь фото.")


@router.message(CreateLessonTask.img)
async def get_task_question(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(img=message.photo[-1].file_id)
        await message.answer("Отправьте описания для задания")
        await state.set_state(CreateLessonTask.question)
    else:
        await message.answer("Задача может быть только вида фото")


@router.message(CreateLessonTask.question)
async def get_task_question(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(question=message.text)
        await state.set_state(CreateLessonTask.answer)
        await message.answer("Через пробел отправьте варианты ответов")
    else:
        await message.answer("Задача может быть только вида текст")


@router.message(CreateLessonTask.answer)
async def get_task_answer(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(answer=list(message.text.split(" ")))
        await state.set_state(CreateLessonTask.right_answer)
        await message.answer("Отправьте правильный ответ")
    else:
        await message.answer("Ответ может быть только в виде текста")


@router.message(CreateLessonTask.right_answer)
async def get_task_answer(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(right_answer=message.text)
        await state.set_state(CreateLessonTask.right_answer)
        async with session_factory() as session:
            data = await state.get_data()
            task = await create_lessons_task(
                session=session,
                id_lesson=data["id_lesson"],
                question=data["question"],
                answer=data["answer"],
                right_answer=data["right_answer"],
                task_type_id=data["task_type_id"],
                previous=data.get("previous", None),
                img=data.get("img", None),
            )
            await message.answer(
                "Задача успешно создана",
                reply_markup=completed_tasks_inline(task=task),
            )
        await state.clear()
        await state.update_data(id_lesson=data["id_lesson"])
    else:
        await message.answer("Правильный ответ может быть только в виде текста")


@router.callback_query(F.data.startswith("list_tasks_lesson"))
async def get_list_tasks_lesson(call: CallbackQuery, state: FSMContext):
    id_lesson = int(call.data.split("_")[-1])
    await state.update_data(id_lesson=id_lesson)
    async with session_factory() as session:
        tasks, count_tasks = await get_lessons_tasks(
            session=session, id_lesson=id_lesson
        )
        if tasks:
            if tasks[0].img:
                await call.message.delete()
                await call.message.answer_photo(
                    photo=tasks[0].img,
                    caption=f"{tasks[0].question}\n\n"
                    f"Варианты ответов: {', '.join(tasks[0].answer)}\n"
                    f"Правильный ответ: {tasks[0].right_answer}",
                    reply_markup=(
                        pagination(
                            count_page=count_tasks,
                            back_callback="stop_create_task",
                            name_nex_action="next_page_tasks",
                        )
                        if count_tasks > 1
                        else pagination(
                            count_page=count_tasks, back_callback="stop_create_task"
                        )
                    ),
                )
            else:
                await call.message.edit_text(
                    text=f"{tasks[0].question}\n\n"
                    f"Варианты ответов: {', '.join(tasks[0].answer)}\n"
                    f"Правильный ответ: {tasks[0].right_answer}",
                    reply_markup=(
                        pagination(
                            count_page=count_tasks,
                            back_callback="stop_create_task",
                            name_nex_action="next_page_tasks",
                        )
                        if count_tasks > 1
                        else pagination(
                            count_page=count_tasks, back_callback="stop_create_task"
                        )
                    ),
                )
        else:
            await call.message.edit_text(
                "Задач в данном уроке нету", reply_markup=back_lesson
            )


@router.callback_query(
    Pagination.filter(F.action.in_(["prev_page_tasks", "next_page_tasks"]))
)
async def paginator_tasks(
    call: CallbackQuery, callback_data: Pagination, state: FSMContext
):
    left = "prev_page_tasks"
    right = "next_page_tasks"
    if callback_data.action == "prev_page_tasks":
        if callback_data.page > 1:
            page = callback_data.page - 1
            if page <= 1:
                left = None
                right = "next_page_tasks"
        else:
            page = callback_data.page
            left = None
            right = "next_page_tasks"
    elif callback_data.action == "next_page_tasks":
        if callback_data.page < callback_data.count_page:
            page = callback_data.page + 1
            if page >= callback_data.count_page:
                left = "prev_page_tasks"
                right = None
        else:
            page = callback_data.page
            left = "prev_page_tasks"
            right = None
    async with session_factory() as session:
        data = await state.get_data()
        id_lesson = data["id_lesson"]
        tasks, count_tasks = await get_lessons_tasks(
            session=session, id_lesson=id_lesson, offset=page
        )
    with suppress(TelegramBadRequest):
        if tasks[0].img:
            await call.message.delete()
            await call.message.answer_photo(
                photo=tasks[0].img,
                caption=f"{tasks[0].question}\n\n"
                f"Варианты ответов: {', '.join(tasks[0].answer)}\n"
                f"Правильный ответ: {tasks[0].right_answer}",
                reply_markup=(
                    pagination(
                        count_page=count_tasks,
                        back_callback="stop_create_task",
                        name_nex_action=right,
                        name_prev_action=left,
                        page=page,
                    )
                ),
            )
        else:
            if call.message.photo:
                await call.message.delete()
                await call.message.answer(
                    text=f"{tasks[0].question}\n\n"
                    f"Варианты ответов: {', '.join(tasks[0].answer)}\n"
                    f"Правильный ответ: {tasks[0].right_answer}",
                    reply_markup=(
                        pagination(
                            count_page=count_tasks,
                            back_callback="stop_create_task",
                            name_nex_action=right,
                            name_prev_action=left,
                            page=page,
                        )
                    ),
                )
            else:
                await call.message.edit_text(
                    text=f"{tasks[0].question}\n\n"
                    f"Варианты ответов: {', '.join(tasks[0].answer)}\n"
                    f"Правильный ответ: {tasks[0].right_answer}",
                    reply_markup=(
                        pagination(
                            count_page=count_tasks,
                            back_callback="stop_create_task",
                            name_nex_action=right,
                            name_prev_action=left,
                            page=page,
                        )
                    ),
                )
