from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

fio = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Из личного профиля", callback_data="fio_from_account"
            ),
        ],
        [
            InlineKeyboardButton(text="Ввести самому", callback_data="get_fio_user"),
        ],
    ],
)

y_n_fio = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data="agree_fio"),
        ],
        [
            InlineKeyboardButton(text="Отклонить", callback_data="disagree_fio"),
        ],
    ],
)
