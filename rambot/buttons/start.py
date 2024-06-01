from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

create_profiles = InlineKeyboardMarkup(
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

fio = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Из профиля", callback_data="fio_from_account"),
        ],
        [
            InlineKeyboardButton(text="Ввести самому", callback_data="get_fio_user"),
        ],
    ],
)
