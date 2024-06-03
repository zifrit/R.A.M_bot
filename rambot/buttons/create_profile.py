from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

create_profiles_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать профиль учителя", callback_data="create_profiled_teacher"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Создать профиль ученика", callback_data="create_profiled_student"
            ),
        ],
    ],
)
create_profiles_student_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать профиль ученика", callback_data="create_profiled_student"
            )
        ]
    ]
)
create_profile_teacher_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Создать профиль учителя", callback_data="create_profiled_teacher"
            )
        ]
    ]
)

fio_teacher = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Из личного профиля", callback_data="fio_from_account_teacher"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Ввести самому", callback_data="get_fio_user_teacher"
            ),
        ],
    ],
)

y_n_fio_teacher = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data="agree_fio_teacher"),
        ],
        [
            InlineKeyboardButton(
                text="Отклонить", callback_data="disagree_fio_teacher"
            ),
        ],
    ],
)

fio_student = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Из личного профиля", callback_data="fio_from_account_student"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Ввести самому", callback_data="get_fio_user_student"
            ),
        ],
    ],
)

y_n_fio_student = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data="agree_fio_student"),
        ],
        [
            InlineKeyboardButton(
                text="Отклонить", callback_data="disagree_fio_student"
            ),
        ],
    ],
)


def view_profile(callback_data):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Пересоздать профиль", callback_data=callback_data),
        InlineKeyboardButton(text="Назад", callback_data="back_choice_profile"),
        width=1,
    )
    return builder.as_markup()
