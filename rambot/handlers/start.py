from aiogram import types, F, Router
from aiogram.types import Message

from base.db import session_factory
from services.crud.users import create_users, get_user_by_tg_id

router = Router()


@router.message(F.text == "/start")
async def start_handler(msg: Message):
    async with session_factory() as session:
        user = await get_user_by_tg_id(session=session, tg_id=msg.from_user.id)
        if user:
            pass
        else:
            await create_users(
                session=session,
                username=msg.from_user.username,
                tg_id=msg.from_user.id,
            )
    await msg.answer("Привет")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")
