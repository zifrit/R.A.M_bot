from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def info_lesson(id_lesson, search: bool = False, have_tasks: bool = False):
    builder = InlineKeyboardBuilder()
    if search:
        if have_tasks:
            builder.row(
                InlineKeyboardButton(
                    text="Добавить к себе", callback_data=f"add_lesson_{id_lesson}"
                )
            )
        builder.row(
            InlineKeyboardButton(text="Повторить поиск", callback_data="search_lesson"),
        )
    else:
        builder.row(
            InlineKeyboardButton(
                text="Удалить", callback_data=f"delete_lesson_{id_lesson}"
            ),
            InlineKeyboardButton(
                text="Изменить название",
                callback_data=f"update_lesson_name_{id_lesson}",
            ),
            InlineKeyboardButton(
                text="Список задач", callback_data=f"list_tasks_lesson_{id_lesson}"
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


def start_work_lesson(id_lesson: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Начать проходить",
            callback_data=f"start_work_lesson_tasks_{id_lesson}",
        ),
    )
    return builder.as_markup()


def continue_work_lesson(id_lesson: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Продолжить проходить",
            callback_data=f"continue_work_lesson_tasks_{id_lesson}",
        ),
    )
    return builder.as_markup()
