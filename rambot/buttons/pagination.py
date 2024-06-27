from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Pagination(CallbackData, prefix="pagination"):
    action: str
    page: int
    count_page: int


def pagination(
    back_callback: str,
    back_text: str = "Назад",
    name_prev_action: str | None = None,
    name_nex_action: str | None = None,
    page: int = 1,
    count_page: int = 1,
):
    if name_prev_action and name_nex_action:
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=Pagination(
                    action=name_prev_action, page=page, count_page=count_page
                ).pack(),
            ),
            InlineKeyboardButton(
                text=f"{page} из {count_page} стр.", callback_data="list"
            ),
            InlineKeyboardButton(
                text="➡️",
                callback_data=Pagination(
                    action=name_nex_action, page=page, count_page=count_page
                ).pack(),
            ),
            InlineKeyboardButton(text=back_text, callback_data=back_callback),
            width=3,
        )
        return builder.as_markup()
    elif name_prev_action:
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=Pagination(
                    action=name_prev_action, page=page, count_page=count_page
                ).pack(),
            ),
            InlineKeyboardButton(
                text=f"{page} из {count_page} стр.", callback_data="list"
            ),
            InlineKeyboardButton(text="❎", callback_data="❎"),
            InlineKeyboardButton(text=back_text, callback_data=back_callback),
            width=3,
        )
        return builder.as_markup()
    elif name_nex_action:
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="❎", callback_data="❎"),
            InlineKeyboardButton(
                text=f"{page} из {count_page} стр.", callback_data="list"
            ),
            InlineKeyboardButton(
                text="➡️",
                callback_data=Pagination(
                    action=name_nex_action, page=page, count_page=count_page
                ).pack(),
            ),
            InlineKeyboardButton(text=back_text, callback_data=back_callback),
            width=3,
        )
        return builder.as_markup()
    else:
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="❎", callback_data="❎"),
            InlineKeyboardButton(
                text=f"{page} из {count_page} стр.", callback_data="list"
            ),
            InlineKeyboardButton(text="❎", callback_data="❎"),
            InlineKeyboardButton(text=back_text, callback_data=back_callback),
            width=3,
        )
        return builder.as_markup()


repeat_search_lesson = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Повторить поиск", callback_data="search_lesson"),
        ],
    ],
)
