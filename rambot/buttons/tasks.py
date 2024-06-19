from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def task_types_inline(task_types: list):
    builder = InlineKeyboardBuilder()
    for task_type in task_types:
        builder.row(
            InlineKeyboardButton(
                text=task_type.name,
                callback_data=f"task_type_{task_type.id}_{task_type.name}",
            )
        )
    builder.row(
        InlineKeyboardButton(text="Отмена Создания", callback_data="stop_create_task"),
    )
    return builder.as_markup()


def completed_tasks_inline(task):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="+ 1", callback_data=f"create_next_task_{task.id}_{task.lesson_id}"
        ),
        InlineKeyboardButton(text="Вернутся", callback_data="stop_create_task"),
        width=2,
    )
    return builder.as_markup()


back_lesson = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вернутся", callback_data="stop_create_task"),
        ],
    ],
)


def task_answers_inline(next_tasks_id: int = None, answers: list = None):
    builder = InlineKeyboardBuilder()
    if answers:
        for answer in answers:
            builder.row(
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"next_tasks_{next_tasks_id}_{answer}",
                )
            )
    builder.row(
        InlineKeyboardButton(text="Остановить урок", callback_data="stop_work_task"),
    )
    return builder.as_markup()


def last_task_answers_inline(last_task_id: int = None, answers: list = None):
    builder = InlineKeyboardBuilder()
    if answers:
        for answer in answers:
            builder.row(
                InlineKeyboardButton(
                    text=answer,
                    callback_data=f"finish_work_lesson_{last_task_id}_{answer}",
                )
            )
    builder.row(
        InlineKeyboardButton(text="Остановить урок", callback_data="stop_work_task"),
    )
    return builder.as_markup()
