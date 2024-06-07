import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from handlers import (
    start,
    create_profile_teacher,
    create_profile_student,
    join_to_teacher,
    lessons,
    tasks,
)

commands = [
    types.BotCommand(command="start", description="запуск бота"),
    types.BotCommand(command="create_lesson", description="создать урок"),
    types.BotCommand(command="profiles", description="Профили"),
]


async def main():
    bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        create_profile_teacher.router,
        create_profile_student.router,
        join_to_teacher.router,
        lessons.router,
        tasks.router,
    )
    await bot.set_my_commands(commands=commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
