from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

profiles = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Профиль ученика", callback_data="profiled_student"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Профиль учителя", callback_data="profiled_teacher"
            ),
        ],
    ],
)
