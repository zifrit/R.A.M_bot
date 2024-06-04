from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Pagination(CallbackData, prefix="pagination"):
    action: str
    page: int
    count_page: int


def many_page(
    back_callback: str,
    name_prev_action: str,
    name_nex_action: str,
    page: int = 1,
    count_page: int = 1,
):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=Pagination(
                action=name_prev_action, page=page, count_page=count_page
            ).pack(),
        ),
        InlineKeyboardButton(text=f"{page} из {count_page} стр.", callback_data="list"),
        InlineKeyboardButton(
            text="➡️",
            callback_data=Pagination(
                action=name_nex_action, page=page, count_page=count_page
            ).pack(),
        ),
        InlineKeyboardButton(text="Назад", callback_data=back_callback),
        width=3,
    )
    return builder.as_markup()


def many_page_without_left(
    back_callback: str, name_nex_action: str, page: int = 1, count_page: int = 1
):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="❎", callback_data="❎"),
        InlineKeyboardButton(text=f"{page} из {count_page} стр.", callback_data="list"),
        InlineKeyboardButton(
            text="➡️",
            callback_data=Pagination(
                action=name_nex_action, page=page, count_page=count_page
            ).pack(),
        ),
        InlineKeyboardButton(text="Назад", callback_data=back_callback),
        width=3,
    )
    return builder.as_markup()


def many_page_without_right(
    back_callback: str, name_prev_action: str, page: int = 1, count_page: int = 1
):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=Pagination(
                action=name_prev_action, page=page, count_page=count_page
            ).pack(),
        ),
        InlineKeyboardButton(text=f"{page} из {count_page} стр.", callback_data="list"),
        InlineKeyboardButton(text="❎", callback_data="❎"),
        InlineKeyboardButton(text="Назад", callback_data=back_callback),
        width=3,
    )
    return builder.as_markup()


back_teacher_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="profiled_teacher"),
        ],
    ],
)
