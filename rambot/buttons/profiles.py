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


back_to_teacher_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вернутся", callback_data="profiled_teacher"),
        ],
    ],
)


back_to_student_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Вернутся", callback_data="profiled_student"),
        ],
    ],
)


def view_teacher_profile(callback_data):
    builder = InlineKeyboardBuilder()
    builder.row(
        # InlineKeyboardButton(text="Создать ключ", callback_data="create_join_token"),
        InlineKeyboardButton(text="Мои уроки", callback_data="view_teacher_lessons"),
        InlineKeyboardButton(
            text="Список для проверки уроков", callback_data="list_for_verify_lesson"
        ),
        InlineKeyboardButton(text="Пересоздать профиль", callback_data=callback_data),
        width=1,
    )
    return builder.as_markup()


def view_student_profile(callback_data):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Мои уроки", callback_data="view_student_lessons"),
        InlineKeyboardButton(text="Пересоздать профиль", callback_data=callback_data),
        width=1,
    )
    return builder.as_markup()
