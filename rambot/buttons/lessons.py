from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def info_lesson(id_lesson):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить", callback_data=f"delete_lesson_{id_lesson}"
        ),
        InlineKeyboardButton(
            text="Изменить название", callback_data=f"update_lesson_name_{id_lesson}"
        ),
        InlineKeyboardButton(
            text="Добавить задачу", callback_data=f"add_task_to_lesson_{id_lesson}"
        ),
        width=2,
    )
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="back_list_lessons"),
    )
    return builder.as_markup()
