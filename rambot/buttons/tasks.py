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


def verify_tasks_inline(
    next_task_id: int = None,
    prev_task_id: int = None,
    finish: bool = False,
    id_lesson: int = None,
):
    builder = InlineKeyboardBuilder()
    if next_task_id:
        builder.row(
            InlineKeyboardButton(
                text="➡️", callback_data=f"next_verify_task_{next_task_id}"
            ),
        )
    if prev_task_id:
        builder.row(
            InlineKeyboardButton(
                text="⬅️", callback_data=f"prev_verify_task_{next_task_id}"
            ),
        )
    if finish:
        builder.row(
            InlineKeyboardButton(
                text="Завершить проверку",
                callback_data=f"finish_verify_lesson_{id_lesson}",
            ),
        )
    builder.row(
        InlineKeyboardButton(text="Назад", callback_data="back_list_for_verify_lesson")
    )
    return builder.as_markup()
