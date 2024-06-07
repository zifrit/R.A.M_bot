from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def task_types_inline(task_types: list):
    builder = InlineKeyboardBuilder()
    for task_type in task_types:
        builder.row(
            InlineKeyboardButton(
                text=task_type.name, callback_data=f"task_type_{task_type.id}"
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
