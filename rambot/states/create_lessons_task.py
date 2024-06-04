from aiogram.fsm.state import StatesGroup, State


class CreateLesson(StatesGroup):
    name_lesson = State()
